#!/usr/bin/env python3
"""
phase1d_train_v6.py — V6 Phase 1d: Triplet-Loss auf 25 V6-Glyphen trainieren.

Trainiert ein Embedding-Netz auf den 1746 Token-Crops (25 Klassen, Pseudo-Labels
aus Template-Matching). 5-fold Cross-Validation zur Bestätigung.

Output: models/symbols_20260706_V6/model.pt, embeddings.npz, eval.json
"""
import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torch.utils.data import Dataset, DataLoader


# V2-EmbeddingNet-Architektur (übernommen)
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
        e = self.conv(x).flatten(1)
        return F.normalize(self.fc(e), dim=-1)  # L2-normalisiert für Cosine


def preprocess(img, size=32, augment=False):
    """Zentriere auf Quadrat, resize zu size×size, normalisiere."""
    w, h = img.size
    side = max(w, h)
    sq = Image.new("L", (side, side), 255)
    sq.paste(img, ((side - w) // 2, (side - h) // 2))
    sq = sq.resize((size, size), Image.BILINEAR)
    a = np.array(sq, dtype=np.float32) / 255.0
    a = (a - 0.5) / 0.5
    t = torch.from_numpy(a).unsqueeze(0)  # (1, H, W)

    if augment:
        # Random shift ±2 px
        if random.random() < 0.5:
            shift_y = random.randint(-2, 2)
            shift_x = random.randint(-2, 2)
            t = torch.roll(t, shifts=(shift_y, shift_x), dims=(1, 2))
        # Random horizontal flip
        if random.random() < 0.3:
            t = torch.flip(t, dims=(2,))
        # Add small Gaussian noise
        if random.random() < 0.3:
            t = t + 0.05 * torch.randn_like(t)
            t = t.clamp(-0.5, 0.5)
    return t


class GlyphDataset(Dataset):
    def __init__(self, root: Path, augment=False):
        self.root = root
        self.augment = augment
        self.items = []
        for p in sorted((root).glob("*/*.png")):
            self.items.append((p, p.parent.name))
        # Index by label for triplet sampling
        self.by_label = defaultdict(list)
        for i, (p, l) in enumerate(self.items):
            self.by_label[l].append(i)
        self.labels = sorted(self.by_label.keys())

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        path, label = self.items[idx]
        img = Image.open(path).convert("L")
        x = preprocess(img, augment=self.augment)
        return x, label


def triplet_indices(ds: GlyphDataset, batch_size: int = 32):
    """Generator für (anchor, positive, negative) Indices."""
    labels = ds.labels
    n_per_label = {l: len(ds.by_label[l]) for l in labels}
    while True:
        # Sample anchor+positive aus gleicher Klasse, negative aus anderer
        anchor_label = random.choice(labels)
        if n_per_label[anchor_label] < 2:
            continue
        a, p = random.sample(ds.by_label[anchor_label], 2)
        neg_label = random.choice([l for l in labels if l != anchor_label])
        n = random.choice(ds.by_label[neg_label])
        yield a, p, n


def train_model(model, ds, device, epochs=20, batch_size=32, lr=1e-3, margin=0.2):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    triplet = nn.TripletMarginLoss(margin=margin, p=2)
    model.train()
    history = []
    # Filter labels mit <2 Crops raus
    valid_labels = [l for l in ds.labels if len(ds.by_label[l]) >= 2]
    print(f"  Trainable labels (>=2 crops): {len(valid_labels)}/{len(ds.labels)}")
    for epoch in range(epochs):
        epoch_loss = 0.0
        n_batches = 0
        n_steps_per_epoch = max(50, len(ds) // batch_size)
        for step in range(n_steps_per_epoch):
            anchors, positives, negatives = [], [], []
            for _ in range(batch_size):
                anchor_label = random.choice(valid_labels)
                a, p = random.sample(ds.by_label[anchor_label], 2)
                neg_label = random.choice([l for l in valid_labels if l != anchor_label])
                n = random.choice(ds.by_label[neg_label])
                anchors.append(a)
                positives.append(p)
                negatives.append(n)
            A = torch.stack([ds[a][0] for a in anchors]).to(device)
            P = torch.stack([ds[p][0] for p in positives]).to(device)
            N = torch.stack([ds[n_][0] for n_ in negatives]).to(device)
            optimizer.zero_grad()
            ea, ep, en = model(A), model(P), model(N)
            loss = triplet(ea, ep, en)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            n_batches += 1
        avg = epoch_loss / max(1, n_batches)
        history.append({"epoch": epoch + 1, "loss": avg})
        print(f"  Epoch {epoch+1:2d}: loss={avg:.4f}")
    return history


def compute_embeddings(model, ds, device, size=32):
    model.eval()
    embs = []
    labels = []
    paths = []
    with torch.no_grad():
        for i in range(len(ds)):
            x, l = ds[i]
            e = model(x.unsqueeze(0).to(device)).cpu().numpy()[0]
            embs.append(e)
            labels.append(l)
            paths.append(str(ds.items[i][0]))
    return np.array(embs), labels, paths


def kNN_accuracy(embs: np.ndarray, labels: list, k=5, n_folds=5):
    """5-fold Cross-Validation kNN-Accuracy@k."""
    from sklearn.model_selection import StratifiedKFold
    from sklearn.neighbors import KNeighborsClassifier
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42)
    accs = []
    for train_idx, test_idx in skf.split(embs, labels):
        knn = KNeighborsClassifier(n_neighbors=min(k, len(train_idx)), metric="cosine")
        knn.fit(embs[train_idx], [labels[i] for i in train_idx])
        pred = knn.predict(embs[test_idx])
        acc = sum(int(p == labels[i]) for p, i in zip(pred, test_idx)) / len(test_idx)
        accs.append(acc)
    return accs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crops", type=Path, required=True,
                    help="bbox/token_crops_20260706_V6/")
    ap.add_argument("--out", type=Path, required=True,
                    help="models/symbols_20260706_V6/")
    ap.add_argument("--epochs", type=int, default=25)
    ap.add_argument("--bs", type=int, default=32)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # Dataset (no augmentation for eval, with for training)
    ds = GlyphDataset(args.crops, augment=True)
    print(f"Dataset: {len(ds)} crops, {len(ds.labels)} classes")
    counts = Counter(l for _, l in ds.items)
    print(f"  Distribution: min={min(counts.values())}, max={max(counts.values())}, "
          f"mean={np.mean(list(counts.values())):.1f}")

    # Model
    model = EmbeddingNet(emb_dim=64).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Model: EmbeddingNet(64), {n_params} params")

    # Training
    print(f"\n=== Training ({args.epochs} epochs) ===")
    history = train_model(model, ds, device, epochs=args.epochs, batch_size=args.bs)

    # Save model
    torch.save(model.state_dict(), args.out / "model.pt")

    # Eval: 5-fold CV kNN
    print(f"\n=== Evaluation (5-fold CV) ===")
    ds_eval = GlyphDataset(args.crops, augment=False)
    embs, labels, paths = compute_embeddings(model, ds_eval, device)
    np.savez(args.out / "embeddings.npz", embeddings=embs, labels=labels, paths=paths)

    accs = kNN_accuracy(embs, labels, k=5, n_folds=5)
    print(f"  kNN@5 5-fold CV: {accs}")
    print(f"  Mean: {np.mean(accs):.4f} ± {np.std(accs):.4f}")

    # Save eval
    eval_data = {
        "metadata": {
            "n_crops": len(ds),
            "n_classes": len(ds.labels),
            "n_params": n_params,
            "epochs": args.epochs,
            "bs": args.bs,
            "device": str(device),
            "method": "TripletMarginLoss(margin=0.2) + Adam(lr=1e-3)",
        },
        "class_distribution": dict(counts),
        "training_history": history,
        "knn_cv_5fold": {
            "k": 5,
            "fold_accuracies": [round(a, 4) for a in accs],
            "mean": round(float(np.mean(accs)), 4),
            "std": round(float(np.std(accs)), 4),
        }
    }
    (args.out / "eval.json").write_text(json.dumps(eval_data, indent=2, ensure_ascii=False))

    # Classes-JSON
    classes = {
        "labels": sorted(set(labels)),
        "n_classes": len(set(labels)),
    }
    (args.out / "classes.json").write_text(json.dumps(classes, indent=2, ensure_ascii=False))

    print(f"\nWrote {args.out}/")
    print(f"  model.pt, embeddings.npz, eval.json, classes.json")


if __name__ == "__main__":
    main()
