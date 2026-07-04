#!/usr/bin/env python3
"""
classify_crops.py — Use a trained embedding model to classify new crops.

Loads a model from models/embedding_<TS>/, embeds every crop in
bbox/crops/ and prints clusters of crops whose embeddings are
nearest-neighbors of each other. Useful for finding recurring glyphs
across pages.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")
sys.path.insert(0, str(ROOT))
from train_embedding import EmbeddingNet, CropDataset  # type: ignore


@torch.no_grad()
def embed_all(model, ds, device):
    model.eval()
    paths, embs, labels = [], [], []
    for i in range(len(ds)):
        x, y, p = ds[i]
        x = x.unsqueeze(0).to(device)
        e = model(x).cpu().numpy()[0]
        paths.append(p); embs.append(e); labels.append(int(y))
    return paths, np.stack(embs), np.array(labels)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", type=Path, required=True)
    ap.add_argument("--top-k", type=int, default=8)
    ap.add_argument("--min-sim", type=float, default=0.85)
    args = ap.parse_args()

    classes = json.loads((args.model_dir / "classes.json").read_text())
    idx_to_class = {v: k for k, v in classes.items()}

    # Load model
    model = EmbeddingNet(emb_dim=64)
    model.load_state_dict(torch.load(args.model_dir / "model.pt",
                                      map_location="cpu"))
    device = "cpu"

    # Load crops
    crops_dir = ROOT / "bbox" / "crops"
    ds = CropDataset(crops_dir, classes)
    paths, embs, labels = embed_all(model, ds, device)

    # Cosine similarity matrix
    norms = np.linalg.norm(embs, axis=1, keepdims=True)
    e = embs / np.maximum(norms, 1e-9)
    sim = e @ e.T
    np.fill_diagonal(sim, -1.0)

    # Group by approximate label
    by_class = {}
    for i, lbl in enumerate(labels):
        by_class.setdefault(lbl, []).append(i)

    print(f"Loaded {len(embs)} embeddings across {len(by_class)} classes.")
    print(f"Top-{args.top_k} nearest neighbours per class:\n")
    for lbl, idxs in sorted(by_class.items(), key=lambda x: -len(x[1])):
        cls_name = idx_to_class[lbl]
        for i in idxs[:3]:  # first 3 crops per class
            top = np.argsort(-sim[i])[:args.top_k]
            top = [j for j in top if sim[i, j] >= args.min_sim]
            if not top:
                continue
            print(f"  {cls_name} :: {Path(paths[i]).name}")
            for j in top:
                print(f"      sim={sim[i,j]:.3f}  {Path(paths[j]).name}")
            print()


if __name__ == "__main__":
    main()
