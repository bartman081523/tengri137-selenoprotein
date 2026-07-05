#!/usr/bin/env python3
"""
phase0_substrat.py — Inken-Substrat-Extraktion (DevMind, TDD).

V5 PIVOT: Phase 0 produziert NUR das rohe Inken-Substrat (Connected-Components
auf der Inken-Maske), OHNE Glyph-Gruppierung. Das ist der Input für
CryptanalysisMind (Phase 1).

WICHTIG: V4 hat bereits Substrate unter bbox/components_20260704_V4/p{NN}/
erzeugt (identische Datenstruktur). Phase 0 hier produziert eine formale
V5-Reproduktion mit eigenem TS-Ordner (Reproduzierbarkeits-Regel).

Input:  pages_png/page-NN.png  (150 DPI, 1125×1625)
Output: bbox/substrat_20260705_V5/p{NN}.json
        {
          "page_id": "p01",
          "image_size": [1125, 1625],
          "ink_threshold": 200,
          "n_components": 584,
          "n_micro": 71,    // size < 100
          "n_meso": 512,    // 100 <= size < 2000
          "n_macro": 1,     // size >= 2000
          "components": [
            {"id": 1, "bbox": [x, y, w, h], "size_px": 1263, "fill_ratio": 0.36,
             "centroid": [x, y], "bounding_box_aspect": 0.39, "level": "meso"}
          ]
        }

Tests (DevMind):
- p01 muss 584 ± 5 Komponenten liefern (Regression gegen V4-Substrat)
- Größen-Klassifikation: micro (<100), meso (100-2000), macro (>=2000)
- Keine Glyph-Gruppierung in Phase 0
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


def detect_ink_components(png_path: Path, ink_threshold: int = 200) -> dict:
    """Extrahiere Connected-Components aus der Inken-Maske einer PNG-Seite."""
    img = Image.open(png_path).convert("L")
    arr = np.array(img)
    h, w = arr.shape

    # Inken-Maske: Pixel < Threshold = Tinte
    ink = arr < ink_threshold
    labeled, n = ndimage.label(ink)

    components = []
    for label_id in range(1, n + 1):
        ys, xs = np.where(labeled == label_id)
        if len(ys) == 0:
            continue
        x0, x1 = int(xs.min()), int(xs.max())
        y0, y1 = int(ys.min()), int(ys.max())
        bw, bh = x1 - x0 + 1, y1 - y0 + 1
        # Rand-Komponenten verwerfen (Kopier-Artefakte, < 5 px)
        if bw < 5 or bh < 5:
            continue
        size_px = int(len(ys))
        bbox_area = bw * bh
        fill_ratio = size_px / bbox_area if bbox_area > 0 else 0.0
        centroid = [float(xs.mean()), float(ys.mean())]
        bbox_aspect = bw / bh if bh > 0 else 1.0

        if size_px < 100:
            level = "micro"
        elif size_px < 2000:
            level = "meso"
        else:
            level = "macro"

        components.append({
            "id": int(label_id),
            "bbox": [x0, y0, int(bw), int(bh)],
            "size_px": size_px,
            "fill_ratio": round(fill_ratio, 4),
            "centroid": [round(centroid[0], 2), round(centroid[1], 2)],
            "bounding_box_aspect": round(bbox_aspect, 3),
            "level": level,
        })

    n_micro = sum(1 for c in components if c["level"] == "micro")
    n_meso = sum(1 for c in components if c["level"] == "meso")
    n_macro = sum(1 for c in components if c["level"] == "macro")

    return {
        "page_id": png_path.stem.replace("page-", "p"),
        "image_size": [w, h],
        "ink_threshold": ink_threshold,
        "n_components": len(components),
        "n_micro": n_micro,
        "n_meso": n_meso,
        "n_macro": n_macro,
        "components": components,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=Path, required=True,
                    help="pages_png/  (enthält page-NN.png)")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/substrat_20260705_V5/")
    ap.add_argument("--ink-threshold", type=int, default=200,
                    help="Binarisierungs-Schwelle (default: 200)")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    n_total_components = 0
    n_pages = 0
    for i in range(1, 24):
        png_path = args.pages / f"page-{i:02d}.png"
        if not png_path.exists():
            print(f"  p{i:02d}: SKIP ({png_path} existiert nicht)", file=sys.stderr)
            continue
        result = detect_ink_components(png_path, ink_threshold=args.ink_threshold)
        out_path = args.out / f"p{i:02d}.json"
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        n_total_components += result["n_components"]
        n_pages += 1
        print(f"  p{i:02d}: {result['n_components']:3d} Komponenten "
              f"(micro={result['n_micro']}, meso={result['n_meso']}, "
              f"macro={result['n_macro']})")

    print(f"\nTotal: {n_pages} pages, {n_total_components} Komponenten")


if __name__ == "__main__":
    main()
