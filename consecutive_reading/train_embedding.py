#!/usr/bin/env python3
"""
train_embedding.py — Tengri137 symbol embedding model

Trains a small CNN to embed 32x32 cropped symbols into a 64-d
embedding space, such that crops of the same symbol class (according
to symbol_index.tsv) cluster together.

This is a *starter* training script: it uses a per-page weak-label
heuristic (all crops from a given page share the page's primary
symbol class) so we can bootstrap embeddings without a fully
manually-labeled dataset. Once you start hand-labeling crops
(e.g. via a contact sheet inspector), you can extend the
labeling to per-crop and re-run.

Inputs:
  - bbox/crops/*.png  (one crop per file, file name pattern p{NN}_{kind}_{idx}.png)
  - symbol_index.tsv  (class definitions)

Outputs:
  - models/embedding_<TS>/model.pt        (state dict)
  - models/embedding_<TS>/classes.json    (class id -> index)
  - models/embedding_<TS>/embeddings.npz  (paths, embeddings, predicted classes)

Use the embeddings to classify new crops by nearest-neighbor.
"""
import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torch.utils.data import Dataset, DataLoader

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


# -------------------------------------------------------------------
# Labeling heuristic
# -------------------------------------------------------------------
# For each page, we declare a primary "expected" symbol class. Crops
# from that page are assigned that class. This is a weak label and
# only useful for bootstrapping — you should re-label by hand.
PAGE_PRIMARY_CLASS = {
    "p01": "TIAN_ORACLE",
    "p02": "TURKIC_ROUND_RUNE_1",
    "p03": "TURKIC_ROUND_RUNE_2",
    "p04": "TIAN_SEAL",
    "p05": "MAGIC_CUBE_3x3",
    "p06": "MAGIC_CUBE_3x3",
    "p07": "RED_LABEL_2CKRONIK",
    "p08": "RED_LABEL_1KINGS",
    "p09": "RING_7_LINK_R1",
    "p10": "RING_9_LINK_R1",
    "p11": "ODIN_HORN_HORN_1",
    "p12": "BG_ADDRESS_HEX",
    "p13": "LATIN_PRINT",
    "p14": "MATH_PI",
    "p15": "MATH_PI",
    "p16": "MATH_PI",
    "p17": "PRIME_FACTOR_DIGIT",
    "p18": "PRIME_FACTOR_DIGIT",
    "p19": "LATIN_PRINT",
    "p20": "LATIN_PRINT",
    "p21": "LATIN_PRINT",
    "p22": "LATIN_PRINT",
    "p23": "BURUMUT_BLOCK_CHAR_A",
}


# -------------------------------------------------------------------
# Dataset
# -------------------------------------------------------------------
class CropDataset(Dataset):
    def __init__(self, crop_dir: Path, classes: dict, size: int = 32):
        self.size = size
        self.classes = classes  # class_id -> int
        self.idx_to_class = {v: k for k, v in classes.items()}
        self.samples = []
        pat = re.compile(r"(p\d{2})_(blank|color)_(\d+)\.png$")
        for p in sorted(crop_dir.glob("*.png")):
            m = pat.match(p.name)
            if not m:
                continue
            page = m.group(1)
            cls = PAGE_PRIMARY_CLASS.get(page)
            if cls is None or cls not in classes:
                continue
            try:
                img = Image.open(p).convert("L")
            except Exception:
                continue
            self.samples.append((p, classes[cls]))
        if not self.samples:
            raise RuntimeError("no samples found")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, i):
        path, label = self.samples[i]
        img = Image.open(path).convert("L")
        # Pad to square, then resize to size x size
        w, h = img.size
        side = max(w, h)
        sq = Image.new("L", (side, side), 255)
        sq.paste(img, ((side - w) // 2, (side - h) // 2))
        sq = sq.resize((self.size, self.size), Image.BILINEAR)
        a = np.array(sq, dtype=np.float32) / 255.0
        a = (a - 0.5) / 0.5  # normalize to [-1, 1]
        return torch.from_numpy(a).unsqueeze(0), label, str(path)


# -------------------------------------------------------------------
# Model
# -------------------------------------------------------------------
class EmbeddingNet(nn.Module):
    def __init__(self, emb_dim: int = 64):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),  # 16
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),  # 8
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d(1),  # 1
        )
        self.fc = nn.Linear(64, emb_dim)

    def forward(self, x):
        h = self.conv(x).flatten(1)
        return self.fc(h)


# -------------------------------------------------------------------
# Training
# -------------------------------------------------------------------
def train_one_epoch(model, loader, optim, device, num_classes):
    model.train()
    crit = nn.CrossEntropyLoss()
    total_loss = 0.0
    n = 0
    for x, y, _ in loader:
        x = x.to(device); y = y.to(device)
        optim.zero_grad()
        emb = model(x)
        # Use a small linear classifier on top for the loss; we just
        # need the embedding to be class-discriminative.
        logits = emb  # not a real classifier; we use a proxy loss
        # Proxy: pull same-class embeddings together, push different apart
        loss = contrastive_loss(emb, y, margin=0.5)
        loss.backward()
        optim.step()
        total_loss += float(loss.item()) * x.size(0)
        n += x.size(0)
    return total_loss / max(1, n)


def contrastive_loss(emb, y, margin: float = 0.5):
    """Simple supervised contrastive: positive pairs pulled together,
    negatives pushed beyond margin."""
    n = emb.size(0)
    if n < 2:
        return emb.sum() * 0.0
    sim = F.cosine_similarity(emb.unsqueeze(0), emb.unsqueeze(1), dim=-1)
    # We only act on off-diagonal pairs
    eye = torch.eye(n, device=emb.device, dtype=torch.bool)
    same = (y.unsqueeze(0) == y.unsqueeze(1)) & ~eye
    diff = (y.unsqueeze(0) != y.unsqueeze(1))
    pos_loss = (1.0 - sim[same]).pow(2).mean() if same.any() else 0.0
    neg_loss = F.relu(sim[diff] - margin).pow(2).mean() if diff.any() else 0.0
    return pos_loss + neg_loss


# -------------------------------------------------------------------
# Embedding extraction
# -------------------------------------------------------------------
@torch.no_grad()
def extract_embeddings(model, ds, device):
    model.eval()
    paths, embs, labels = [], [], []
    for i in range(len(ds)):
        x, y, p = ds[i]
        x = x.unsqueeze(0).to(device)
        e = model(x).cpu().numpy()[0]
        paths.append(p)
        embs.append(e)
        labels.append(int(y))
    return paths, np.stack(embs), np.array(labels)


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crops", type=Path,
                    default=ROOT / "bbox" / "crops")
    ap.add_argument("--index", type=Path,
                    default=ROOT / "symbol_index.tsv")
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--bs", type=int, default=32)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    # Load class index
    classes = {}
    with open(args.index, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            cid = row["class_id"]
            if cid not in classes:
                classes[cid] = len(classes)
    print(f"Loaded {len(classes)} classes from {args.index}")

    if not args.crops.exists():
        sys.exit(f"error: crops dir {args.crops} does not exist")
    ds = CropDataset(args.crops, classes)
    print(f"Dataset: {len(ds)} samples")
    loader = DataLoader(ds, batch_size=args.bs, shuffle=True, num_workers=0)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = EmbeddingNet(emb_dim=64).to(device)
    optim = torch.optim.Adam(model.parameters(), lr=args.lr)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_dir = args.out or (ROOT / "models" / f"embedding_{ts}")
    out_dir.mkdir(parents=True, exist_ok=True)

    for ep in range(args.epochs):
        loss = train_one_epoch(model, loader, optim, device, len(classes))
        print(f"  epoch {ep+1:>2}/{args.epochs}: loss = {loss:.4f}")

    paths, embs, labels = extract_embeddings(model, ds, device)
    np.savez(out_dir / "embeddings.npz",
             paths=np.array(paths),
             embeddings=embs,
             labels=labels)
    (out_dir / "classes.json").write_text(
        json.dumps(classes, indent=2, ensure_ascii=False))
    torch.save(model.state_dict(), out_dir / "model.pt")
    print(f"Saved model + embeddings to {out_dir}")


if __name__ == "__main__":
    main()
