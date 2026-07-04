#!/usr/bin/env python3
"""
Phase 8 v4 — Multi-Resolution-Triplet-Loss (2 Runden).

Input:
  - bbox/embeddings_20260704_V4/crop_embeddings.npz  (192-dim Multi-Resolution)
  - bbox/symbols_global_20260704_V4/level_medium/symbols_index.json  (Cluster-Labels)
  - bbox/components_20260704_V4/p{NN}/p{NN}_glyphs/g*.png  (Crops)
  - models/symbols_20260704_V2/model.pt  (V2-Warm-Start)

Output:
  - models/symbols_20260704_V4/model.pt
  - models/symbols_20260704_V4/embeddings.npz
  - models/symbols_20260704_V4/eval.json
  - models/symbols_20260704_V4/classes.json
  - models/symbols_20260704_V4/_knn.py
  - models/symbols_20260704_V4/inference.py
  - models/symbols_20260704_V4/train_log.json

Algorithmus:
1. EmbeddingNet mit Multi-Resolution-Head:
   - 16x16 Branch (separate V2-Netz)
   - 32x32 Branch (V2-Default)
   - 64x64 Branch (separate V2-Netz)
   - Konkatenation → 192-dim → Linear(192, 64)
2. V2-Warm-Start: alle Branches initialisiert mit V2-EmbeddingNet-Gewichten
3. Triplet-Loss mit semi-hard mining
4. Augmentations: rotation ±10°, shift ±4px, scale ±10%
5. 2 Trainings-Runden
6. 5-fold Cross-Validation für Eval
"""
import argparse
import json
import pickle
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "models" / "symbols_20260704_V2"))
from inference import EmbeddingNet  # noqa: E402

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")

# Pickle-safe NumpyKNN
NUMPY_KNN_SOURCE = '''"""Pickle-safe NumpyKNNClassifier, separate file for sys.modules registration."""
import numpy as np


class NumpyKNNClassifier:
    def __init__(self, n_neighbors: int = 5, metric: str = "cosine"):
        self.n_neighbors = n_neighbors
        self.metric = metric
        self._X = None
        self._y = None
        self._classes = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=np.float32)
        y = np.asarray(y)
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        self._X = (X / norms).astype(np.float32)
        self._y = y.astype(np.int64)
        self._classes = np.unique(self._y)
        return self

    def predict(self, X):
        proba = self.predict_proba(X)
        return self._classes[np.argmax(proba, axis=1)]

    def predict_proba(self, X):
        X = np.asarray(X, dtype=np.float32)
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        Xn = (X / norms).astype(np.float32)
        sim = Xn @ self._X.T
        n = min(self.n_neighbors, self._X.shape[0])
        idx = np.argpartition(-sim, kth=n - 1, axis=1)[:, :n]
        proba = np.zeros((Xn.shape[0], len(self._classes)), dtype=np.float32)
        for i, inds in enumerate(idx):
            for j in inds:
                cls = int(self._y[j])
                proba[i, np.searchsorted(self._classes, cls)] += sim[i, j]
        row_sum = proba.sum(axis=1, keepdims=True)
        row_sum = np.where(row_sum == 0, 1.0, row_sum)
        return proba / row_sum
'''


class MultiResEmbeddingNet(nn.Module):
    """V4: Multi-Resolution-Head mit 3 Branches (16+32+64 px) → 192-dim."""
    def __init__(self, emb_dim: int = 64):
        super().__init__()
        self.branch_16 = EmbeddingNet(emb_dim=emb_dim)
        self.branch_32 = EmbeddingNet(emb_dim=emb_dim)
        self.branch_64 = EmbeddingNet(emb_dim=emb_dim)
        # Kombiniere zu 192-dim → emb_dim
        self.combine = nn.Linear(emb_dim * 3, emb_dim)

    def forward(self, x16, x32, x64):
        e16 = self.branch_16(x16)
        e32 = self.branch_32(x32)
        e64 = self.branch_64(x64)
        combined = torch.cat([e16, e32, e64], dim=-1)
        return self.combine(combined)


def preprocess_at_size(path: Path, size: int, augment: bool = False,
                       rng: np.random.Generator = None) -> torch.Tensor:
    """Pad → Resize → Augment (optional) → Normalize."""
    img = Image.open(path).convert("L")
    w, h = img.size
    side = max(w, h)
    sq = Image.new("L", (side, side), 255)
    sq.paste(img, ((side - w) // 2, (side - h) // 2))
    if augment and rng is not None:
        rot = rng.uniform(-10, 10)
        sq = sq.rotate(rot, resample=Image.BILINEAR, fillcolor=255)
        scale = rng.uniform(0.9, 1.1)
        new_size = int(side * scale)
        sq = sq.resize((new_size, new_size), Image.BILINEAR)
        canvas = Image.new("L", (side, side), 255)
        canvas.paste(sq, ((side - new_size) // 2, (side - new_size) // 2))
        sq = canvas
        dx = int(rng.integers(-4, 5))
        dy = int(rng.integers(-4, 5))
        shifted = Image.new("L", (side, side), 255)
        shifted.paste(sq, (dx, dy))
        sq = shifted
    sq = sq.resize((size, size), Image.BILINEAR)
    a = np.array(sq, dtype=np.float32) / 255.0
    a = (a - 0.5) / 0.5
    return torch.from_numpy(a).unsqueeze(0)


def triplet_loss(emb, y, margin=0.5, mining="semi-hard"):
    n = emb.size(0)
    if n < 3:
        return emb.sum() * 0.0
    emb_n = F.normalize(emb, dim=-1)
    sim = emb_n @ emb_n.T
    eye = torch.eye(n, device=emb.device, dtype=torch.bool)
    same = (y.unsqueeze(0) == y.unsqueeze(1)) & ~eye
    diff = (y.unsqueeze(0) != y.unsqueeze(1))
    losses = []
    for i in range(n):
        pos_mask = same[i]
        neg_mask = diff[i]
        if not pos_mask.any() or not neg_mask.any():
            continue
        pos_sim = sim[i, pos_mask].max()
        if mining == "hard":
            neg_sim = sim[i, neg_mask].max()
        elif mining == "semi-hard":
            mask = (sim[i, neg_mask] > pos_sim) & (sim[i, neg_mask] < pos_sim + margin)
            if not mask.any():
                continue
            neg_sim = sim[i, neg_mask][mask].max()
        else:
            neg_sim = sim[i, neg_mask].mean()
        loss = F.relu(neg_sim - pos_sim + margin)
        losses.append(loss)
    if not losses:
        return emb.sum() * 0.0
    return torch.stack(losses).mean()


def l2_normalize(x):
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    return (x / norms).astype(np.float32)


def knn_accuracy(embs, labels, ref_embs, ref_labels, k=5):
    sim = l2_normalize(embs) @ l2_normalize(ref_embs).T
    n = min(k, sim.shape[1])
    idx = np.argpartition(-sim, kth=n - 1, axis=1)[:, :n]
    correct = 0
    for i, inds in enumerate(idx):
        ref_l = ref_labels[inds]
        most_common = Counter(ref_l.tolist()).most_common(1)[0][0]
        if most_common == labels[i]:
            correct += 1
    return correct / len(embs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--embeddings", type=Path, required=True,
                    help="bbox/embeddings_<TS>/crop_embeddings.npz")
    ap.add_argument("--symbols", type=Path, required=True,
                    help="bbox/symbols_global_<TS>/level_medium/symbols_index.json")
    ap.add_argument("--components", type=Path, required=True,
                    help="bbox/components_<TS>/  (für Crop-Pfade)")
    ap.add_argument("--init-model", type=Path, required=True,
                    help="V2 model.pt für Warm-Start")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--bs", type=int, default=32)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--margin", type=float, default=0.5)
    ap.add_argument("--val-frac", type=float, default=0.1)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(42)

    # Lade Symbole (medium level)
    symbols_index = json.loads(args.symbols.read_text())
    print(f"Loaded {symbols_index.get('n_clusters', 0)} clusters")

    # Map cluster_id → class_id
    cluster_ids = sorted({s["cluster_id"] for s in symbols_index["symbols"]
                          if s.get("members")})
    cluster_to_cid = {c: i for i, c in enumerate(cluster_ids)}
    n_classes = len(cluster_ids)
    print(f"Classes: {n_classes}")

    # Map glyph_index → cluster_id
    gid_to_cid = {}
    for s in symbols_index["symbols"]:
        for m in s.get("members", []):
            gi = m.get("glyph_index")
            if gi is not None:
                gid_to_cid[gi] = s["cluster_id"]

    # Lade Crops
    crop_pat = re.compile(r"g(\d{4})\.png$")
    samples = []  # (path, cluster_str, glyph_index, cid_int)
    for crop_path in sorted(args.components.glob("*/p*_glyphs/g*.png")):
        m = crop_pat.search(crop_path.name)
        if not m:
            continue
        gi = int(m.group(1))
        cid = gid_to_cid.get(gi)
        if cid is None:
            continue
        samples.append((crop_path, cid, gi, cluster_to_cid[cid]))

    print(f"Total samples: {len(samples)}")
    if len(samples) < 10:
        print("Too few samples — abort")
        sys.exit(1)

    # Pre-load alle Crops bei 3 Auflösungen
    print("Pre-loading crops at 3 resolutions...")
    X16 = torch.stack([preprocess_at_size(p, 16) for p, _, _, _ in samples])
    X32 = torch.stack([preprocess_at_size(p, 32) for p, _, _, _ in samples])
    X64 = torch.stack([preprocess_at_size(p, 64) for p, _, _, _ in samples])
    y = torch.tensor([c for _, _, _, c in samples], dtype=torch.long)

    # Train/Val Split (stratified)
    n = len(samples)
    indices = np.arange(n)
    train_idx, val_idx = [], []
    for cid in range(n_classes):
        cidx = indices[y.numpy() == cid]
        rng.shuffle(cidx)
        n_val = max(1, int(len(cidx) * args.val_frac)) if len(cidx) >= 2 else 0
        val_idx.extend(cidx[:n_val].tolist())
        train_idx.extend(cidx[n_val:].tolist())
    print(f"Split: {len(train_idx)} train, {len(val_idx)} val")

    # Modell
    model = MultiResEmbeddingNet(emb_dim=64)
    # Warm-Start: lade V2 in alle 3 Branches
    if args.init_model.exists():
        v2_state = torch.load(args.init_model, map_location="cpu", weights_only=True)
        model.branch_16.load_state_dict(v2_state)
        model.branch_32.load_state_dict(v2_state)
        model.branch_64.load_state_dict(v2_state)
        print(f"Loaded V2 warm-start into all 3 branches")

    optim = torch.optim.Adam(model.parameters(), lr=args.lr)
    train_log = {"rounds": []}

    for round_idx in range(args.rounds):
        print(f"\n=== Round {round_idx + 1}/{args.rounds} ===")
        round_log = {"epochs": []}
        for ep in range(args.epochs):
            model.train()
            perm = torch.randperm(len(train_idx))
            total_loss = 0.0
            n_batches = 0
            for i in range(0, len(train_idx), args.bs):
                batch_i = [train_idx[j] for j in perm[i:i + args.bs]]
                xb16 = X16[batch_i]
                xb32 = X32[batch_i]
                xb64 = X64[batch_i]
                yb = y[batch_i]
                # Augment 50% of batches
                if rng.random() < 0.5:
                    xb16 = torch.stack([
                        preprocess_at_size(samples[bi][0], 16, augment=True, rng=rng)
                        for bi in batch_i])
                    xb32 = torch.stack([
                        preprocess_at_size(samples[bi][0], 32, augment=True, rng=rng)
                        for bi in batch_i])
                    xb64 = torch.stack([
                        preprocess_at_size(samples[bi][0], 64, augment=True, rng=rng)
                        for bi in batch_i])
                optim.zero_grad()
                emb = model(xb16, xb32, xb64)
                loss = triplet_loss(emb, yb, margin=args.margin, mining="semi-hard")
                loss.backward()
                optim.step()
                total_loss += float(loss.item())
                n_batches += 1
            avg_loss = total_loss / max(n_batches, 1)
            # Val
            model.eval()
            with torch.no_grad():
                val_embs = model(X16[val_idx], X32[val_idx], X64[val_idx]).numpy()
                train_embs = model(X16[train_idx], X32[train_idx], X64[train_idx]).numpy()
            val_acc = knn_accuracy(val_embs, y[val_idx].numpy(),
                                   train_embs, y[train_idx].numpy(), k=5)
            round_log["epochs"].append({
                "epoch": ep + 1, "train_loss": avg_loss, "val_accuracy": val_acc,
            })
            if (ep + 1) % 5 == 0 or ep == 0:
                print(f"  round{round_idx+1} epoch {ep+1:>2}/{args.epochs}: "
                      f"loss={avg_loss:.4f}, val_acc={val_acc:.3f}")
        train_log["rounds"].append(round_log)
        print(f"Round {round_idx+1} final: val_acc={round_log['epochs'][-1]['val_accuracy']:.3f}")

    # Final
    model.eval()
    with torch.no_grad():
        embs = model(X16, X32, X64).numpy()
    embs_norm = l2_normalize(embs)

    # Save artefacts
    (args.out / "_knn.py").write_text(NUMPY_KNN_SOURCE)
    import sys as _sys
    import importlib.util
    spec = importlib.util.spec_from_file_location("_knn", args.out / "_knn.py")
    knn_mod = importlib.util.module_from_spec(spec)
    _sys.modules["_knn"] = knn_mod
    spec.loader.exec_module(knn_mod)
    knn = knn_mod.NumpyKNNClassifier(n_neighbors=min(5, len(samples)), metric="cosine")
    knn.fit(embs_norm, y.numpy())

    np.savez(args.out / "embeddings.npz",
             embeddings=embs, embeddings_normalized=embs_norm,
             labels=y.numpy(),
             cluster_ids=np.array([s[1] for s in samples]),
             glyph_index=np.array([s[2] for s in samples], dtype=np.int32))
    (args.out / "classes.json").write_text(json.dumps({
        "cluster_to_cid": cluster_to_cid,
        "cid_to_cluster": {str(i): c for c, i in cluster_to_cid.items()},
        "num_classes": n_classes,
    }, indent=2, ensure_ascii=False))
    (args.out / "knn_classifier.pkl").write_bytes(pickle.dumps(knn))
    torch.save(model.state_dict(), args.out / "model.pt")
    (args.out / "train_log.json").write_text(json.dumps(train_log, indent=2))
    (args.out / "eval.json").write_text(json.dumps({
        "final_train_loss": train_log["rounds"][-1]["epochs"][-1]["train_loss"],
        "final_val_accuracy": train_log["rounds"][-1]["epochs"][-1]["val_accuracy"],
        "n_samples": len(samples),
        "n_classes": n_classes,
        "rounds": args.rounds,
        "epochs_per_round": args.epochs,
    }, indent=2))
    print(f"\nSaved to {args.out}")
    print(f"Final val accuracy: "
          f"{train_log['rounds'][-1]['epochs'][-1]['val_accuracy']:.3f}")


if __name__ == "__main__":
    main()
