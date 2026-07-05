#!/usr/bin/env python3
"""
phase1c_extract_token_crops.py — V6 Phase 1c: Extrahiere Token-Crops für Training.

Wir nehmen den V6 Token-Stream (1746 Tokens aus 14 Pages) und schneiden aus den
Original-PNGs die entsprechenden Crops an den Match-Positionen aus. Plus etwas
Padding (8 px) für saubere Bbox.

Output: bbox/token_crops_20260706_V6/{glyph_id}/{n}.png
        bbox/token_crops_20260706_V6/dataset.json  (Liste aller Crops mit Labels)
"""
import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokenstream", type=Path, required=True,
                    help="bbox/tokenstream_20260706_V6_v2/")
    ap.add_argument("--pages-png", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/token_crops_20260706_V6/")
    ap.add_argument("--padding", type=int, default=8)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    # Pro Glyph-ID ein Unterordner
    crops_by_glyph = {}

    n_total = 0
    n_skipped = 0
    for f in sorted(args.tokenstream.glob("p*.json")):
        d = json.loads(f.read_text())
        pid = d["page_id"]
        page_num = int(pid[1:])
        page_png = args.pages_png / f"page-{page_num:02d}.png"
        if not page_png.exists():
            continue
        page_img = np.array(Image.open(page_png).convert("L"))

        for token in d["tokens"]:
            gid = token["glyph_id"]
            x, y, w, h = token["x"], token["y"], token["w"], token["h"]
            x0 = max(0, x - args.padding)
            y0 = max(0, y - args.padding)
            x1 = min(page_img.shape[1], x + w + args.padding)
            y1 = min(page_img.shape[0], y + h + args.padding)
            crop = page_img[y0:y1, x0:x1]

            # Skip leere/zu-kleine Crops
            if crop.size == 0 or crop.shape[0] < 5 or crop.shape[1] < 5:
                n_skipped += 1
                continue

            crops_by_glyph.setdefault(gid, []).append({
                "page_id": pid,
                "bbox": [int(x), int(y), int(w), int(h)],
                "conf": float(token["conf"]),
            })
            n_total += 1

    # Speichern als PNGs
    dataset = []
    for gid, items in sorted(crops_by_glyph.items()):
        glyph_dir = args.out / gid
        glyph_dir.mkdir(exist_ok=True)
        for i, item in enumerate(items):
            x, y, w, h = item["bbox"]
            x0 = max(0, x - args.padding)
            y0 = max(0, y - args.padding)
            x1 = min(page_img.shape[1] if False else 9999, x + w + args.padding)  # safety
            # Reload der Page nicht noetig - schon in items vorhanden; aber wir haben die crops nicht persistiert
            # Vereinfachung: skip detailed reconstruction, nutze stattdessen die Token-Stream-PNG-Position
            pass

    # Sauberer Ansatz: zweite Schleife mit Page-Re-Load
    crops_by_glyph = {}
    dataset = []
    for f in sorted(args.tokenstream.glob("p*.json")):
        d = json.loads(f.read_text())
        pid = d["page_id"]
        page_num = int(pid[1:])
        page_png = args.pages_png / f"page-{page_num:02d}.png"
        page_img = np.array(Image.open(page_png).convert("L"))
        ph, pw = page_img.shape

        for idx, token in enumerate(d["tokens"]):
            gid = token["glyph_id"]
            x, y, w, h = token["x"], token["y"], token["w"], token["h"]
            x0 = max(0, x - args.padding)
            y0 = max(0, y - args.padding)
            x1 = min(pw, x + w + args.padding)
            y1 = min(ph, y + h + args.padding)
            crop = page_img[y0:y1, x0:x1]

            if crop.size == 0 or crop.shape[0] < 5 or crop.shape[1] < 5:
                continue

            glyph_dir = args.out / gid
            glyph_dir.mkdir(exist_ok=True)
            crop_path = glyph_dir / f"{idx:04d}.png"
            Image.fromarray(crop).save(crop_path)
            dataset.append({
                "path": str(crop_path.relative_to(args.out)),
                "glyph_id": gid,
                "page_id": pid,
                "conf": float(token["conf"]),
            })

    # Dataset-JSON
    with (args.out / "dataset.json").open("w") as fp:
        json.dump(dataset, fp, indent=2, ensure_ascii=False)

    # Statistik
    counts = Counter(item["glyph_id"] for item in dataset)
    print(f"Total token crops: {len(dataset)}")
    print(f"\nPer-glyph distribution:")
    for gid, c in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {gid}: {c}")
    print(f"\nWrote {args.out}/")
    print(f"  dataset.json ({len(dataset)} entries)")
    print(f"  {len(counts)} glyph-subdirs with crops")


if __name__ == "__main__":
    main()
