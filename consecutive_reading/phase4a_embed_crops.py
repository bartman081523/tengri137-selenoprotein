#!/usr/bin/env python3
"""
Phase 4a — Embedding-Berechnung für alle Crops.

Liest:
  - bbox/crops/  (alle 818 Crops)
  - models/symbols_20260704_075228/model.pt  (vortrainiertes EmbeddingNet)

Schreibt:
  - bbox/embeddings_<TS>/crop_embeddings.npz
  - bbox/embeddings_<TS>/embeddings_meta.json
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


class EmbeddingNet(nn.Module):
    """Muss identisch zur Architektur in phase6_train.py sein."""
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


def load_and_preprocess(crop_path: Path, size: int = 32):
    """Preprocessing muss identisch zu phase6_train.py sein."""
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
    ap.add_argument("--crops", type=Path, required=True)
    ap.add_argument("--model", type=Path, required=True,
                    help="path to model.pt (Vortraining)")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--emb-dim", type=int, default=64)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    # Lade Modell
    model = EmbeddingNet(emb_dim=args.emb_dim)
    state = torch.load(args.model, map_location="cpu", weights_only=True)
    model.load_state_dict(state)
    model.eval()
    print(f"Loaded EmbeddingNet from {args.model}")

    # Sammle alle Crops
    crop_pat = re.compile(r"(p\d{2})_(blank|color)_(\d+)\.png$")
    paths = []
    page_ids = []
    crop_indices = []
    kinds = []
    for crop_path in sorted(args.crops.glob("*.png")):
        m = crop_pat.match(crop_path.name)
        if not m:
            continue
        page_id, kind, idx_str = m.groups()
        paths.append(str(crop_path))
        page_ids.append(page_id)
        crop_indices.append(int(idx_str))
        kinds.append(kind)

    if not paths:
        print("No crops found!")
        sys.exit(1)
    print(f"Found {len(paths)} crops")

    # Pre-load alle Crops
    X = torch.stack([load_and_preprocess(Path(p)) for p in paths])

    # Inferenz (CPU, 64 Crops/Batch)
    embs = []
    bbox_data = []
    ink_ratios = []
    areas = []
    aspect_ratios = []
    with torch.no_grad():
        for i in range(0, len(X), 64):
            batch = X[i:i+64]
            e = model(batch).numpy()
            embs.append(e)
            # Berechne bbox + ink_ratio für jeden Crop
            for j, p in enumerate(paths[i:i+64]):
                img = Image.open(p).convert("L")
                w, h = img.size
                area = w * h
                # Inversion: text ist dunkel
                arr = np.array(img, dtype=float) / 255.0
                ink = float((arr < 0.5).mean())
                bbox_data.append([0, 0, w, h])  # placeholder; echte bbox aus pixel
                ink_ratios.append(ink)
                areas.append(area)
                aspect_ratios.append(w / max(h, 1))
    embs = np.concatenate(embs, axis=0).astype(np.float32)
    bbox_data = np.array(bbox_data, dtype=np.int32)
    ink_ratios = np.array(ink_ratios, dtype=np.float32)
    areas = np.array(areas, dtype=np.float32)
    aspect_ratios = np.array(aspect_ratios, dtype=np.float32)

    # L2-normalisierte Embeddings
    norms = np.linalg.norm(embs, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    embs_norm = (embs / norms).astype(np.float32)

    # Speichern
    np.savez(args.out / "crop_embeddings.npz",
             embeddings=embs,
             embeddings_normalized=embs_norm,
             paths=np.array(paths),
             page_id=np.array(page_ids),
             crop_index=np.array(crop_indices),
             kind=np.array(kinds),
             bbox=bbox_data,
             area_px=areas,
             ink_ratio=ink_ratios,
             aspect_ratio=aspect_ratios)
    print(f"Saved embeddings to {args.out / 'crop_embeddings.npz'}")

    # Meta-JSON
    meta = {
        "embedding_model": str(args.model),
        "embedding_dim": args.emb_dim,
        "n_crops": len(paths),
        "n_pages": len(set(page_ids)),
        "n_blanks": sum(1 for k in kinds if k == "blank"),
        "n_colors": sum(1 for k in kinds if k == "color"),
        "embedding_stats": {
            "mean_norm": float(np.linalg.norm(embs, axis=1).mean()),
            "std_norm": float(np.linalg.norm(embs, axis=1).std()),
            "min": float(embs.min()),
            "max": float(embs.max()),
        },
        "per_page_counts": {p: sum(1 for pp in page_ids if pp == p)
                            for p in sorted(set(page_ids))},
    }
    (args.out / "embeddings_meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False))
    print(f"Meta: {meta['n_crops']} crops, "
          f"{meta['n_pages']} pages, "
          f"embedding_dim={args.emb_dim}")


if __name__ == "__main__":
    main()
