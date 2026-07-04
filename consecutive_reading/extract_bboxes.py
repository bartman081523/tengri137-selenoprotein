#!/usr/bin/env python3
"""
Extracts word-level bounding boxes from tesseract TSV files and
identifies "empty zones" (regions not covered by any text token) on
each page of Tengri-137.

Outputs:
  - bbox/words/p{NN}.json   : all word-level tokens with bbox + conf
  - bbox/empty_zones/p{NN}.json : regions where no text token is found
                                  (candidates for sigils / symbols)
"""
import json
import csv
import os
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")
TSV_DIR = ROOT / "bbox"
OUT_W = ROOT / "bbox" / "words"
OUT_E = ROOT / "bbox" / "empty_zones"
OUT_W.mkdir(parents=True, exist_ok=True)
OUT_E.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = 1125, 1625  # 150 DPI from 540x780 pt

def parse_tsv(path):
    tokens = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        for row in reader:
            if len(row) < 12:
                continue
            try:
                level = int(row[0])
            except ValueError:
                continue
            if level != 5:
                continue
            text = row[11].strip()
            try:
                left = int(row[6]); top = int(row[7])
                width = int(row[8]); height = int(row[9])
                conf = float(row[10])
            except ValueError:
                continue
            tokens.append({
                "text": text, "left": left, "top": top,
                "width": width, "height": height, "conf": conf,
            })
    return tokens

def find_empty_zones(tokens, page_w, page_h, padding=20):
    """Find rectangular empty zones not covered by any text token."""
    # Make a simple grid of 50x50 cells
    cell = 50
    grid = [[False] * (page_h // cell) for _ in range(page_w // cell)]
    for t in tokens:
        x0 = max(0, (t["left"] - padding) // cell)
        y0 = max(0, (t["top"] - padding) // cell)
        x1 = min(len(grid) - 1, (t["left"] + t["width"] + padding) // cell)
        y1 = min(len(grid[0]) - 1, (t["top"] + t["height"] + padding) // cell)
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                    grid[x][y] = True
    # Find connected empty regions (very rough: list empty cells grouped by
    # vertical bands)
    bands = []
    cur_band = []
    for y in range(len(grid[0])):
        has_empty = any(not grid[x][y] for x in range(len(grid)))
        if has_empty:
            # Find x-extent
            xs = [x for x in range(len(grid)) if not grid[x][y]]
            if xs:
                cur_band.append((min(xs) * cell, y * cell, max(xs) * cell, (y + 1) * cell))
    # Merge consecutive bands with similar x-range
    if not cur_band:
        return []
    merged = [list(cur_band[0])]
    for b in cur_band[1:]:
        last = merged[-1]
        if abs(b[0] - last[0]) < 30 and abs(b[2] - last[2]) < 30 and b[1] - last[3] < 5:
            last[3] = b[3]
        else:
            merged.append(list(b))
    # Filter: keep zones that are not just margins
    out = []
    for m in merged:
        x0, y0, x1, y1 = m
        w = x1 - x0; h = y1 - y0
        # Skip top/bottom margins
        if y0 < 50 and h < 100: continue
        if y1 > page_h - 50 and h < 100: continue
        if w < 30 or h < 30: continue
        out.append({"left": x0, "top": y0, "width": w, "height": h})
    return out

for i in range(1, 24):
    pth = TSV_DIR / f"p{i:02d}.tsv"
    if not pth.exists():
        continue
    tokens = parse_tsv(pth)
    out_tokens = {"page": f"p{i:02d}", "page_w": PAGE_W, "page_h": PAGE_H,
                  "words": tokens}
    (OUT_W / f"p{i:02d}.json").write_text(
        json.dumps(out_tokens, indent=2, ensure_ascii=False))
    empty = find_empty_zones(tokens, PAGE_W, PAGE_H)
    out_empty = {"page": f"p{i:02d}", "empty_zones": empty}
    (OUT_E / f"p{i:02d}.json").write_text(
        json.dumps(out_empty, indent=2, ensure_ascii=False))
    print(f"p{i:02d}: {len(tokens)} tokens, {len(empty)} empty zones")
