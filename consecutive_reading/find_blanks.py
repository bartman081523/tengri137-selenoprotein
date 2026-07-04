#!/usr/bin/env python3
"""
Find empty / non-text regions on each page by:
  1) loading the PNG,
  2) building a binary mask of "ink" (non-white) pixels,
  3) inverting and finding connected white components,
  4) keeping only those components that are inside the page content area
     and have a non-trivial size.

Outputs bbox/empty_zones/p{NN}.json with regions, plus crops for inspection.
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")
PNG_DIR = ROOT / "pages_png"
OUT_E = ROOT / "bbox" / "empty_zones"
OUT_C = ROOT / "bbox" / "crops"
OUT_E.mkdir(parents=True, exist_ok=True)
OUT_C.mkdir(parents=True, exist_ok=True)

# rough content area (excludes white margins)
CONTENT = {"left": 80, "top": 200, "right": 1045, "bottom": 1500}

def detect_ink(img):
    """Return a boolean mask: True = ink, False = white."""
    g = img.convert("L")
    a = np.array(g)
    return a < 200  # anything darker than light grey = ink

def find_blank_regions(img):
    """Find two kinds of blanks:
       A) big "outer" regions (margins between text blocks, full-line gaps)
       B) small interior blanks (white holes inside glyphs, very compact)
    """
    ink = detect_ink(img)
    blank = ~ink
    lbl, n = ndimage.label(blank)
    regions = []
    for i in range(1, n + 1):
        ys, xs = np.where(lbl == i)
        area = len(ys)
        x0, x1 = xs.min(), xs.max()
        y0, y1 = ys.min(), ys.max()
        w, h = x1 - x0 + 1, y1 - y0 + 1
        if w < 8 or h < 8:
            continue
        if w * h < 64:
            continue
        is_outer_margin = (
            (x0 < 50 and w > 800) or
            (x1 > 1075 and w > 800) or
            (y0 < 50 and h > 1400)
        )
        if is_outer_margin:
            continue
        regions.append({
            "left": int(x0), "top": int(y0),
            "width": int(w), "height": int(h),
            "area_px": int(area),
            "bbox_area": int(w * h),
            "fill_ratio": float(area / max(1, w * h)),
            "kind": "outer" if w * h > 4000 else "inner",
        })
    return regions

def detect_red_text(img):
    """Return bbox of red text regions (red ink mask)."""
    a = np.array(img.convert("RGB"))
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # red: r high, g/b low
    red = (r > 150) & (g < 100) & (b < 100)
    lbl, n = ndimage.label(red)
    regions = []
    for i in range(1, n + 1):
        ys, xs = np.where(lbl == i)
        if len(ys) < 20:
            continue
        x0, x1 = xs.min(), xs.max()
        y0, y1 = ys.min(), ys.max()
        w, h = x1 - x0 + 1, y1 - y0 + 1
        if w < 10 or h < 10:
            continue
        regions.append({
            "left": int(x0), "top": int(y0),
            "width": int(w), "height": int(h),
            "area_px": int(len(ys)),
        })
    # Merge nearby regions on the same horizontal line
    return regions

for i in range(1, 24):
    pth = PNG_DIR / f"page-{i:02d}.png"
    if not pth.exists():
        continue
    img = Image.open(pth)
    blanks = find_blank_regions(img)
    reds = detect_red_text(img)
    out = {"page": f"p{i:02d}", "blank_regions": blanks, "red_text_regions": reds}
    (OUT_E / f"p{i:02d}.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    # Save crops of blank regions for visual inspection
    for j, b in enumerate(blanks):
        # Add 20px padding
        x0 = max(0, b["left"] - 20)
        y0 = max(0, b["top"] - 20)
        x1 = min(img.size[0], b["left"] + b["width"] + 20)
        y1 = min(img.size[1], b["top"] + b["height"] + 20)
        crop = img.crop((x0, y0, x1, y1))
        crop.save(OUT_C / f"p{i:02d}_blank_{j:02d}.png")
    for j, r in enumerate(reds):
        x0 = max(0, r["left"] - 20)
        y0 = max(0, r["top"] - 20)
        x1 = min(img.size[0], r["left"] + r["width"] + 20)
        y1 = min(img.size[1], r["top"] + r["height"] + 20)
        crop = img.crop((x0, y0, x1, y1))
        crop.save(OUT_C / f"p{i:02d}_red_{j:02d}.png")
    print(f"p{i:02d}: {len(blanks)} blanks, {len(reds)} red regions")
