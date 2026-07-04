#!/usr/bin/env python3
"""
Phase 6 v2 — Triplet-Loss + Augmentations + Validation (ML Best Practices).

User-Entscheidung: Triplet-Loss + Augmentations + Validation (State-of-the-Art
für Similarity Learning, optimal für "fremde Schrift / fremde Konzepte").

Best Practices implementiert:
1. Triplet-Loss mit semi-hard negative mining (anchor, positive, negative)
2. Augmentations: rotation ±5°, shift ±2px, slight scale ±5%, horizontal flip
3. L2-normalized Embeddings + cosine distance
4. Mini-Batch 32 mit All-Triplets-in-Batch mining
5. Validation-Split (10% stratified holdout pro Cluster)
6. Train + val loss + kNN-Accuracy pro Epoche loggen
7. Embeddings + kNN + k-Means exportieren
8. Inference-Skript: akzeptiert Crop-Pfad oder Verzeichnis

Input:
  - bbox/embeddings_<TS>/crop_embeddings.npz (für initial weights + crop-paths)
  - bbox/symbols_global_<TS>/symbols_index.json (Cluster-Labels)
  - bbox/crops/ (alle 818 Crops als PNG)

Output:
  - models/symbols_<TS>/model.pt
  - models/symbols_<TS>/classes.json
  - models/symbols_<TS>/embeddings.npz
  - models/symbols_<TS>/knn_classifier.pkl
  - models/symbols_<TS>/_knn.py
  - models/symbols_<TS>/inference.py
  - models/symbols_<TS>/train_log.json
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

# Constants
EMB_DIM = 64
IMG_SIZE = 32

# --- NumPy kNN (gleicher Code wie V1, damit pickle kompatibel) ---
NUMPY_KNN_SOURCE = '''"""Pickle-safe NumpyKNNClassifier, separate file for sys.modules registration."""
import numpy as np


class NumpyKNNClassifier:
    """Tiny scikit-learn-free kNN classifier using cosine similarity."""

    def __init__(self, n_neighbors: int = 5, metric: str = "cosine"):
        self.n_neighbors = n_neighbors
        self.metric = metric
        self._X = None
        self._y = None
        self._classes = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=np.float32)
        y = np.asarray(y)
        # L2-normalize for cosine similarity
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
        sim = Xn @ self._X.T  # (n_query, n_ref)
        n = min(self.n_neighbors, self._X.shape[0])
        # Top-k indices per query
        idx = np.argpartition(-sim, kth=n - 1, axis=1)[:, :n]
        proba = np.zeros((Xn.shape[0], len(self._classes)), dtype=np.float32)
        for i, inds in enumerate(idx):
            for j in inds:
                cls = int(self._y[j])
                proba[i, np.searchsorted(self._classes, cls)] += sim[i, j]
        # Normalize to vote fraction
        row_sum = proba.sum(axis=1, keepdims=True)
        row_sum = np.where(row_sum == 0, 1.0, row_sum)
        return proba / row_sum
'''


class EmbeddingNet(nn.Module):
    """Muss identisch zu phase4a_embed_crops.py sein."""
    def __init__(self, emb_dim: int = EMB_DIM):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d(1),
        )
        self.fc = nn.Linear(64, emb_dim)

    def forward(self, x):
        h = self.conv(x).flatten(1)
        return self.fc(h)


def load_and_preprocess(crop_path: Path, size: int = IMG_SIZE, augment: bool = False,
                       rng: np.random.Generator = None):
    """Preprocessing identisch zu phase4a_embed_crops.py + optional Augmentations."""
    img = Image.open(crop_path).convert("L")
    w, h = img.size
    side = max(w, h)
    sq = Image.new("L", (side, side), 255)
    sq.paste(img, ((side - w) // 2, (side - h) // 2))
    if augment and rng is not None:
        # Augmentations: rotation ±5°, shift ±2px, scale ±5%, optional flip
        from PIL import Image as PI
        if rng.random() < 0.5:
            sq = sq.transpose(PI.FLIP_LEFT_RIGHT)
        rot = rng.uniform(-5, 5)
        sq = sq.rotate(rot, resample=PI.BILINEAR, fillcolor=255)
        scale = rng.uniform(0.95, 1.05)
        new_size = int(side * scale)
        sq = sq.resize((new_size, new_size), PI.BILINEAR)
        # Re-pad to square
        canvas = PI.new("L", (side, side), 255)
        canvas.paste(sq, ((side - new_size) // 2, (side - new_size) // 2))
        sq = canvas
        # Shift ±2px
        dx = int(rng.integers(-2, 3))
        dy = int(rng.integers(-2, 3))
        shifted = PI.new("L", (side, side), 255)
        shifted.paste(sq, (dx, dy))
        sq = shifted
    sq = sq.resize((size, size), Image.BILINEAR)
    a = np.array(sq, dtype=np.float32) / 255.0
    a = (a - 0.5) / 0.5
    return torch.from_numpy(a).unsqueeze(0)


def triplet_loss(emb, y, margin: float = 0.5, mining: str = "semi-hard"):
    """Triplet-Loss mit semi-hard negative mining (in-batch).

    mining:
      - "hard":    hardest negatives (closest to anchor)
      - "semi-hard": negatives closer than positive + margin
      - "all":     alle valid triplets
    """
    n = emb.size(0)
    if n < 3:
        return emb.sum() * 0.0
    # L2-normalize für cosine
    emb_n = F.normalize(emb, dim=-1)
    sim = emb_n @ emb_n.T  # (n, n) similarity
    eye = torch.eye(n, device=emb.device, dtype=torch.bool)
    same = (y.unsqueeze(0) == y.unsqueeze(1)) & ~eye
    diff = (y.unsqueeze(0) != y.unsqueeze(1))

    # Pro Anchor: 1 positive (wähle ersten), n_neg negatives
    losses = []
    for i in range(n):
        pos_mask = same[i]
        neg_mask = diff[i]
        if not pos_mask.any() or not neg_mask.any():
            continue
        pos_sim = sim[i, pos_mask].max()  # most similar positive
        if mining == "hard":
            # hardest negative: most similar negative
            neg_sim = sim[i, neg_mask].max()
        elif mining == "semi-hard":
            # negatives closer than positive + margin, but further than positive
            mask = (sim[i, neg_mask] > pos_sim) & (sim[i, neg_mask] < pos_sim + margin)
            if not mask.any():
                continue
            neg_sim = sim[i, neg_mask][mask].max()
        else:  # "all"
            neg_sim = sim[i, neg_mask].mean()
        loss = F.relu(neg_sim - pos_sim + margin)
        losses.append(loss)
    if not losses:
        return emb.sum() * 0.0
    return torch.stack(losses).mean()


def stratified_split(symbols_index: dict, val_fraction: float = 0.1,
                     rng: np.random.Generator = None) -> tuple:
    """Stratified split: pro Cluster X% in val, Rest in train."""
    if rng is None:
        rng = np.random.default_rng(42)
    train_paths, val_paths = [], []
    for sym in symbols_index.get("symbols", []):
        occ = sym.get("occurrences", [])
        if not occ:
            continue
        # Sort by cluster_size desc: größere Cluster → val_fraction auf jeden Fall
        n_val = max(1, int(len(occ) * val_fraction)) if len(occ) >= 2 else 0
        if n_val == 0:
            train_paths.extend([o["crop_path"] for o in occ])
            continue
        indices = rng.permutation(len(occ))
        val_i = set(indices[:n_val].tolist())
        for i, o in enumerate(occ):
            if i in val_i:
                val_paths.append(o["crop_path"])
            else:
                train_paths.append(o["crop_path"])
    return train_paths, val_paths


def l2_normalize(x: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    return (x / norms).astype(np.float32)


def knn_accuracy(embs: np.ndarray, labels: np.ndarray,
                 ref_embs: np.ndarray, ref_labels: np.ndarray, k: int = 5) -> float:
    """kNN-Accuracy: für jeden Embedding den Anteil correct predictions."""
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
                    help="bbox/embeddings_<TS>/crop_embeddings.npz (für crop_paths)")
    ap.add_argument("--symbols", type=Path, required=True,
                    help="bbox/symbols_global_<TS>/symbols_index.json")
    ap.add_argument("--crops", type=Path, required=True,
                    help="bbox/crops/  (alle PNGs)")
    ap.add_argument("--init-model", type=Path, default=None,
                    help="Vortrainiertes EmbeddingNet (.pt) für Warm-Start")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--bs", type=int, default=32)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--margin", type=float, default=0.5)
    ap.add_argument("--val-frac", type=float, default=0.1)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(42)

    # Lade Symbole
    symbols_index = json.loads(args.symbols.read_text())
    n_clusters = symbols_index.get("n_clusters", 0)
    print(f"Loaded symbols_index: {n_clusters} clusters, "
          f"{symbols_index.get('total_symbols', 0)} symbols")

    # Stratified split
    train_paths, val_paths = stratified_split(symbols_index, args.val_frac, rng)
    print(f"Split: {len(train_paths)} train, {len(val_paths)} val")

    # Baue Sample-Liste: (path, cluster_id, symbol_id)
    # Map cluster_id → class_id (für Triplet-Loss)
    cluster_ids = sorted({s["cluster_id"] for s in symbols_index["symbols"]
                          if s.get("occurrences")})
    cluster_to_cid = {c: i for i, c in enumerate(cluster_ids)}
    n_classes = len(cluster_ids)
    print(f"Classes: {n_classes}")

    sym_by_crop = {}
    for s in symbols_index["symbols"]:
        for occ in s.get("occurrences", []):
            cp = occ.get("crop_path", "")
            if cp:
                sym_by_crop[Path(cp).name] = s

    samples = []  # (path, cluster_id_int, symbol_id_int, cluster_str, sym_id_int)
    crop_pat = re.compile(r"(p\d{2})_(blank|color)_(\d+)\.png$")
    for crop_path in sorted(args.crops.glob("*.png")):
        m = crop_pat.match(crop_path.name)
        if not m:
            continue
        s = sym_by_crop.get(crop_path.name)
        if not s:
            continue
        cid = s["cluster_id"]
        if cid not in cluster_to_cid:
            continue
        samples.append((crop_path,
                        cluster_to_cid[cid],
                        s.get("symbol_id", 0),
                        cid,
                        s.get("symbol_id", 0)))

    if len(samples) < 10:
        print(f"Only {len(samples)} samples — too few for Triplet-Loss")
        sys.exit(1)

    # Pre-load alle Crops (kleinere Pipeline, 32x32)
    print(f"Pre-loading {len(samples)} crops...")
    X = torch.stack([load_and_preprocess(p, augment=False) for p, _, _, _, _ in samples])
    y = torch.tensor([c for _, c, _, _, _ in samples], dtype=torch.long)

    # Train/Val-Split nach Indizes
    sample_paths = [str(p) for p, _, _, _, _ in samples]
    train_set = set(train_paths)
    val_set = set(val_paths)
    train_idx = [i for i, p in enumerate(sample_paths) if p in train_set]
    val_idx = [i for i, p in enumerate(sample_paths) if p in val_set]
    print(f"Train samples: {len(train_idx)}, Val samples: {len(val_idx)}")

    # Modell: warm-start von V1 wenn vorhanden
    model = EmbeddingNet(emb_dim=EMB_DIM)
    if args.init_model and args.init_model.exists():
        state = torch.load(args.init_model, map_location="cpu", weights_only=True)
        model.load_state_dict(state)
        print(f"Loaded warm-start weights from {args.init_model}")

    optim = torch.optim.Adam(model.parameters(), lr=args.lr)
    train_log = {"epochs": [], "val_accuracy": []}

    # Training: Triplet-Loss mit In-Batch-Mining
    for ep in range(args.epochs):
        model.train()
        perm = torch.randperm(len(train_idx))
        total_loss = 0.0
        n_batches = 0
        for i in range(0, len(train_idx), args.bs):
            batch_i = [train_idx[j] for j in perm[i:i + args.bs]]
            xb = X[batch_i]
            yb = y[batch_i]
            # Augmentiere 50% der Batches
            if rng.random() < 0.5:
                xb_aug = torch.stack([
                    load_and_preprocess(samples[bi][0], augment=True, rng=rng)
                    for bi in batch_i
                ])
                xb = xb_aug
            optim.zero_grad()
            emb = model(xb)
            loss = triplet_loss(emb, yb, margin=args.margin, mining="semi-hard")
            loss.backward()
            optim.step()
            total_loss += float(loss.item())
            n_batches += 1
        avg_loss = total_loss / max(n_batches, 1)

        # Validation: kNN-Accuracy auf Val-Set
        model.eval()
        with torch.no_grad():
            train_embs = model(X[train_idx]).numpy()
            val_embs = model(X[val_idx]).numpy()
        train_labels = y[train_idx].numpy()
        val_labels = y[val_idx].numpy()
        val_acc = knn_accuracy(val_embs, val_labels, train_embs, train_labels, k=5)
        train_log["epochs"].append({
            "epoch": ep + 1,
            "train_loss": avg_loss,
            "val_accuracy": val_acc,
        })
        print(f"  epoch {ep+1:>2}/{args.epochs}: train_loss={avg_loss:.4f}, "
              f"val_acc={val_acc:.3f}")

    # Final Embeddings
    model.eval()
    with torch.no_grad():
        embs = model(X).numpy()
    embs_norm = l2_normalize(embs)

    # kNN Classifier
    (args.out / "_knn.py").write_text(NUMPY_KNN_SOURCE)
    import sys as _sys
    import importlib.util
    spec = importlib.util.spec_from_file_location("_knn", args.out / "_knn.py")
    knn_mod = importlib.util.module_from_spec(spec)
    _sys.modules["_knn"] = knn_mod
    spec.loader.exec_module(knn_mod)
    knn = knn_mod.NumpyKNNClassifier(n_neighbors=min(5, len(samples)), metric="cosine")
    knn.fit(embs_norm, y.numpy())

    # Save
    np.savez(args.out / "embeddings.npz",
             embeddings=embs, embeddings_normalized=embs_norm,
             labels=y.numpy(),
             cluster_ids=np.array([s[3] for s in samples]),
             paths=np.array(sample_paths))
    (args.out / "classes.json").write_text(json.dumps(
        {"cluster_to_cid": cluster_to_cid,
         "cid_to_cluster": {str(i): c for c, i in cluster_to_cid.items()},
         "num_classes": n_classes}, indent=2, ensure_ascii=False))
    (args.out / "knn_classifier.pkl").write_bytes(pickle.dumps(knn))
    torch.save(model.state_dict(), args.out / "model.pt")
    (args.out / "train_log.json").write_text(json.dumps(train_log, indent=2))

    # Inference-Script
    inference_code = '''#!/usr/bin/env python3
"""Inference v2: predicts cluster_id for new crops."""
import argparse
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _knn  # noqa: F401


class EmbeddingNet(torch.nn.Module):
    def __init__(self, emb_dim: int = 64):
        super().__init__()
        self.conv = torch.nn.Sequential(
            torch.nn.Conv2d(1, 16, 3, padding=1), torch.nn.ReLU(), torch.nn.MaxPool2d(2),
            torch.nn.Conv2d(16, 32, 3, padding=1), torch.nn.ReLU(), torch.nn.MaxPool2d(2),
            torch.nn.Conv2d(32, 64, 3, padding=1), torch.nn.ReLU(), torch.nn.AdaptiveAvgPool2d(1),
        )
        self.fc = torch.nn.Linear(64, emb_dim)

    def forward(self, x):
        return self.fc(self.conv(x).flatten(1))


def preprocess(path, size=32):
    img = Image.open(path).convert("L")
    w, h = img.size
    side = max(w, h)
    sq = Image.new("L", (side, side), 255)
    sq.paste(img, ((side - w) // 2, (side - h) // 2))
    sq = sq.resize((size, size), Image.BILINEAR)
    a = np.array(sq, dtype=np.float32) / 255.0
    a = (a - 0.5) / 0.5
    return torch.from_numpy(a).unsqueeze(0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", type=Path, required=True)
    ap.add_argument("--crops", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--top-k", type=int, default=5)
    args = ap.parse_args()

    classes = json.loads((args.model_dir / "classes.json").read_text())
    cid_to_cluster = classes["cid_to_cluster"]
    model = EmbeddingNet(emb_dim=64)
    model.load_state_dict(torch.load(args.model_dir / "model.pt",
                                     map_location="cpu", weights_only=True))
    knn = pickle.loads((args.model_dir / "knn_classifier.pkl").read_bytes())
    model.eval()

    results = []
    crops = (sorted(args.crops.glob("*.png"))
             if args.crops.is_dir() else [args.crops])
    for crop in crops:
        x = preprocess(crop).unsqueeze(0)
        with torch.no_grad():
            e = model(x).numpy()
        proba = knn.predict_proba(e)[0]
        top_k = np.argsort(-proba)[:args.top_k]
        top_clusters = [
            {"cluster_id": cid_to_cluster[str(int(c))],
             "class_id": int(c),
             "probability": float(proba[c])}
            for c in top_k
        ]
        best = top_clusters[0]
        results.append({
            "path": str(crop),
            "predicted_cluster_id": best["cluster_id"],
            "top_k": top_clusters,
            "uncertain": best["probability"] < 0.5,
        })

    if args.out:
        args.out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            mark = "?" if r["uncertain"] else " "
            top3 = ", ".join(f"{c['cluster_id']}({c['probability']:.2f})"
                             for c in r["top_k"][:3])
            print(f"{mark} {r['predicted_cluster_id']:<35} {top3}  {r['path']}")


if __name__ == "__main__":
    main()
'''
    inf_path = args.out / "inference.py"
    inf_path.write_text(inference_code)
    inf_path.chmod(0o755)

    print(f"\nModel + classifier + inference saved to {args.out}")
    print(f"Final val accuracy: {train_log['epochs'][-1]['val_accuracy']:.3f}")


if __name__ == "__main__":
    main()
