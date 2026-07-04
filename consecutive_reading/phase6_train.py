#!/usr/bin/env python3
"""
Phase 6 — ML-Training auf dem globalen Symbol-Index.

Liest:
  - bbox/symbols_global_<TS>/symbols_index.json
  - bbox/symbols_global_<TS>/p{NN}_symbols.json
  - bbox/crops/  (vorbereitete Crops aus analyze_pages.py)

Schreibt:
  - models/symbols_<TS>/model.pt
  - models/symbols_<TS>/classes.json
  - models/symbols_<TS>/embeddings.npz
  - models/symbols_<TS>/knn_classifier.pkl
  - models/symbols_<TS>/inference.py
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image


class NumpyKNNClassifier:
    """Tiny scikit-learn-free kNN classifier using cosine similarity.

    Implements the same surface used by `phase6_train.py` callers:
      - .fit(X, y) stores the reference embeddings + labels
      - .predict(X) returns argmax-vote labels for each row
      - .predict_proba(X) returns the vote-fraction (max-class prob) per row
    """

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
        self._X = X / norms
        self._y = y
        self._classes = np.unique(y)
        return self

    def _sim(self, X):
        X = np.asarray(X, dtype=np.float32)
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        Xn = X / norms
        return Xn @ self._X.T  # (n_query, n_train)

    def predict(self, X):
        sim = self._sim(X)
        k = min(self.n_neighbors, sim.shape[1])
        # Top-k indices per row
        idx = np.argpartition(-sim, k - 1, axis=1)[:, :k]
        # Sort within top-k
        rows = np.arange(sim.shape[0])[:, None]
        sub = sim[rows, idx]
        order = np.argsort(-sub, axis=1)
        idx = idx[rows, order]
        labels = self._y[idx]
        # Majority vote; ties broken by smallest label
        out = np.empty(sim.shape[0], dtype=self._y.dtype)
        for i in range(sim.shape[0]):
            vals, counts = np.unique(labels[i], return_counts=True)
            top = counts.max()
            cand = vals[counts == top]
            out[i] = cand.min()
        return out

    def predict_proba(self, X):
        sim = self._sim(X)
        k = min(self.n_neighbors, sim.shape[1])
        idx = np.argpartition(-sim, k - 1, axis=1)[:, :k]
        rows = np.arange(sim.shape[0])[:, None]
        sub = sim[rows, idx]
        order = np.argsort(-sub, axis=1)
        idx = idx[rows, order]
        labels = self._y[idx]
        proba = np.zeros((sim.shape[0], len(self._classes)), dtype=np.float32)
        for i in range(sim.shape[0]):
            vals, counts = np.unique(labels[i], return_counts=True)
            for v, c in zip(vals, counts):
                j = np.searchsorted(self._classes, v)
                proba[i, j] = c / k
        return proba

    @property
    def classes_(self):
        return self._classes

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


# Source of the NumpyKNNClassifier bundled into inference.py / _knn.py
NUMPY_KNN_SOURCE = '''"""Tiny scikit-learn-free kNN classifier for embedding-vector inference.

Stored as a sibling module so pickle can find the class at load time,
independent of the entry-point script.
"""
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
        self._X = X / norms
        self._y = y
        self._classes = np.unique(y)
        return self

    def _sim(self, X):
        X = np.asarray(X, dtype=np.float32)
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        Xn = X / norms
        return Xn @ self._X.T

    def predict(self, X):
        sim = self._sim(X)
        k = min(self.n_neighbors, sim.shape[1])
        idx = np.argpartition(-sim, k - 1, axis=1)[:, :k]
        rows = np.arange(sim.shape[0])[:, None]
        sub = sim[rows, idx]
        order = np.argsort(-sub, axis=1)
        idx = idx[rows, order]
        labels = self._y[idx]
        out = np.empty(sim.shape[0], dtype=self._y.dtype)
        for i in range(sim.shape[0]):
            vals, counts = np.unique(labels[i], return_counts=True)
            top = counts.max()
            cand = vals[counts == top]
            out[i] = cand.min()
        return out

    def predict_proba(self, X):
        sim = self._sim(X)
        k = min(self.n_neighbors, sim.shape[1])
        idx = np.argpartition(-sim, k - 1, axis=1)[:, :k]
        rows = np.arange(sim.shape[0])[:, None]
        sub = sim[rows, idx]
        order = np.argsort(-sub, axis=1)
        idx = idx[rows, order]
        labels = self._y[idx]
        proba = np.zeros((sim.shape[0], len(self._classes)), dtype=np.float32)
        for i in range(sim.shape[0]):
            vals, counts = np.unique(labels[i], return_counts=True)
            for v, c in zip(vals, counts):
                j = int(np.searchsorted(self._classes, v))
                proba[i, j] = c / k
        return proba

    @property
    def classes_(self):
        return self._classes
'''


class EmbeddingNet(nn.Module):
    def __init__(self, emb_dim: int = 64):
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


def contrastive_loss(emb, y, margin: float = 0.5):
    n = emb.size(0)
    if n < 2:
        return emb.sum() * 0.0
    sim = F.cosine_similarity(emb.unsqueeze(0), emb.unsqueeze(1), dim=-1)
    eye = torch.eye(n, device=emb.device, dtype=torch.bool)
    same = (y.unsqueeze(0) == y.unsqueeze(1)) & ~eye
    diff = (y.unsqueeze(0) != y.unsqueeze(1))
    pos_loss = (1.0 - sim[same]).pow(2).mean() if same.any() else 0.0
    neg_loss = F.relu(sim[diff] - margin).pow(2).mean() if diff.any() else 0.0
    return pos_loss + neg_loss


def load_and_preprocess(crop_path: Path, size: int = 32):
    img = Image.open(crop_path).convert("L")
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
    ap.add_argument("--symbols", type=Path, required=True,
                    help="bbox/symbols_global_<TS>/ with symbols_index.json")
    ap.add_argument("--crops", type=Path, required=True,
                    help="bbox/crops/")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--bs", type=int, default=32)
    ap.add_argument("--lr", type=float, default=1e-3)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    # Build sample list: for each symbol, find at least one crop with
    # matching bbox.
    idx = json.loads((args.symbols / "symbols_index.json").read_text())
    symbol_to_id = {s["symbol_index"]: i for i, s in enumerate(idx["symbols"])}
    id_to_symbol = {i: s["symbol_index"] for i, s in enumerate(idx["symbols"])}

    samples = []
    # Map bbox to symbol_index by scanning per-page symbol files
    page_to_symbols = {}
    for pf in sorted(args.symbols.glob("p*_symbols.json")):
        m = re.match(r"(p\d{2})_symbols\.json", pf.name)
        if not m:
            continue
        page_id = m.group(1)
        page_to_symbols[page_id] = json.loads(pf.read_text())

    crop_pat = re.compile(r"(p\d{2})_(blank|color)_(\d+)\.png$")
    for crop_path in sorted(args.crops.glob("*.png")):
        m = crop_pat.match(crop_path.name)
        if not m:
            continue
        page_id, kind, idx_str = m.groups()
        crop_idx = int(idx_str)
        if page_id not in page_to_symbols:
            continue
        # Find the symbol entry in this page that has matching index
        # In analyze_pages.py, blank_000 maps to the first blank in pixel data
        # which is the first symbol in the page's symbols list.
        page_syms = page_to_symbols[page_id]
        if crop_idx >= len(page_syms):
            continue
        s = page_syms[crop_idx]
        if "symbol_index" not in s or s["symbol_index"] is None:
            continue
        if s["symbol_index"] not in symbol_to_id:
            continue
        samples.append((crop_path, symbol_to_id[s["symbol_index"]],
                        s["symbol_index"]))

    if not samples:
        print("No samples found!")
        sys.exit(1)
    print(f"Loaded {len(samples)} samples across {len(set(s[1] for s in samples))} classes")

    # Pre-load all
    X = torch.stack([load_and_preprocess(p) for p, _, _ in samples])
    y = torch.tensor([c for _, c, _ in samples], dtype=torch.long)
    sym_idx = np.array([s for _, _, s in samples])

    device = "cpu"
    model = EmbeddingNet(emb_dim=64).to(device)
    optim = torch.optim.Adam(model.parameters(), lr=args.lr)

    for ep in range(args.epochs):
        model.train()
        perm = torch.randperm(len(X))
        total_loss = 0.0
        for i in range(0, len(X), args.bs):
            batch = perm[i:i + args.bs]
            xb = X[batch].to(device)
            yb = y[batch].to(device)
            optim.zero_grad()
            emb = model(xb)
            loss = contrastive_loss(emb, yb, margin=0.5)
            loss.backward()
            optim.step()
            total_loss += float(loss.item()) * len(batch)
        print(f"  epoch {ep+1:>2}/{args.epochs}: loss = {total_loss/len(X):.4f}")

    # Embeddings + kNN
    # Re-import the kNN class from a sibling module (`_knn.py`) so pickle
    # stores `_knn.NumpyKNNClassifier` as the qualified name. The inference
    # script does `import _knn` first, which makes unpickling work without
    # depending on the entry-point script's globals.
    (args.out / "_knn.py").write_text(NUMPY_KNN_SOURCE)
    import sys as _sys
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_knn", args.out / "_knn.py")
    knn_mod = importlib.util.module_from_spec(spec)
    _sys.modules["_knn"] = knn_mod  # register so pickle can find it
    spec.loader.exec_module(knn_mod)

    model.eval()
    with torch.no_grad():
        embs = model(X).numpy()
    knn = knn_mod.NumpyKNNClassifier(n_neighbors=min(5, len(samples)),
                                     metric="cosine")
    knn.fit(embs, y.numpy())

    # Save
    np.savez(args.out / "embeddings.npz",
             embeddings=embs, labels=y.numpy(), symbol_index=sym_idx,
             paths=np.array([str(p) for p, _, _ in samples]))
    (args.out / "classes.json").write_text(json.dumps(
        {"id_to_symbol": id_to_symbol,
         "symbol_to_id": symbol_to_id,
         "num_classes": len(id_to_symbol)},
        indent=2, ensure_ascii=False))
    import pickle
    (args.out / "knn_classifier.pkl").write_bytes(pickle.dumps(knn))
    torch.save(model.state_dict(), args.out / "model.pt")

    # Write inference.py
    inference_code = '''#!/usr/bin/env python3
"""Inference: given a directory of crops, predict symbol_index for each."""
import argparse
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image

# Register NumpyKNNClassifier so the pickled classifier unpickles cleanly,
# regardless of which script invokes this entry point.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _knn  # noqa: F401, E402  (registers NumpyKNNClassifier)


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
    args = ap.parse_args()

    classes = json.loads((args.model_dir / "classes.json").read_text())
    id_to_symbol = classes["id_to_symbol"]
    model = EmbeddingNet(emb_dim=64)
    model.load_state_dict(torch.load(args.model_dir / "model.pt",
                                     map_location="cpu"))
    knn = pickle.loads((args.model_dir / "knn_classifier.pkl").read_bytes())
    model.eval()

    results = []
    for crop in sorted(args.crops.glob("*.png")):
        x = preprocess(crop).unsqueeze(0)
        with torch.no_grad():
            e = model(x).numpy()
        pred = knn.predict(e)[0]
        proba = knn.predict_proba(e)[0]
        confidence = float(proba.max())
        sym_idx = id_to_symbol[str(pred)]
        results.append({
            "path": str(crop),
            "predicted_class_id": int(pred),
            "symbol_index": sym_idx,
            "confidence": confidence,
            "uncertain": confidence < 0.5,
        })

    if args.out:
        args.out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            mark = "?" if r["uncertain"] else " "
            print(f"{mark} sym#{r['symbol_index']:>4}  "
                  f"conf={r['confidence']:.2f}  {r['path']}")


if __name__ == "__main__":
    main()
'''
    # Re-import the kNN class from the sibling module so pickle stores
    # `_knn.NumpyKNNClassifier` as the qualified name. The inference script
    # does `from _knn import NumpyKNNClassifier` first to make unpickling
    # work without depending on the entry-point script's globals.
    (args.out / "inference.py").chmod(0o755)
    print(f"\nModel + classifier saved to {args.out}")


if __name__ == "__main__":
    main()
