#!/usr/bin/env python3
"""Inference: given a directory of crops, predict symbol_index for each."""
import argparse
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image


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
