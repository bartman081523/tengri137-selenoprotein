#!/usr/bin/env python3
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
