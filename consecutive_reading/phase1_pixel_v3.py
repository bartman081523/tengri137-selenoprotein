#!/usr/bin/env python3
"""
Phase 1 v3 — Pixel-Analyse + page_type detection.

Unterschiede zu phase1_pixel.py:
- Fügt page_type hinzu (text_dense / formula_dense / sigill_dense / mixed)
- Setzt min_area=50 (war 200) für feinere Crops
- Schreibt bbox/pages_pixel_<TS>/p{NN}.json mit page_type, blank_density, formulas[]

Heuristik page_type:
  - text_dense:    n_text_words >= 100 AND blanks=0 AND colored=0
  - formula_dense: n_formulas >= 5 AND blanks < 5
  - sigill_dense:  n_blanks >= 10 AND text_words/blanks > 30
  - sonst:         mixed

Beispiel-Output p{NN}.json (zusätzlich zu V2-Feldern):
  "page_type": "text_dense",
  "blank_density": 0.0,
  "vision_classification": null,
  "formulas": [{"raw": "...", "bbox": [..], "symbols": [..], "color": "black"}, ...],
  "digits": [{"value": "3", "bbox": [..], "color": "black"}, ...]
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")
PNG_DIR = ROOT / "pages_png"
TSV_DIR = ROOT / "bbox"


def detect_color_for_box(a_rgb, left, top, width, height):
    """Return dominant color of ink pixels inside a bbox."""
    x0 = max(0, left); y0 = max(0, top)
    x1 = min(a_rgb.shape[1], left + width); y1 = min(a_rgb.shape[0], top + height)
    if x1 <= x0 or y1 <= y0:
        return "unknown"
    sub = a_rgb[y0:y1, x0:x1]
    r = sub[..., 0].astype(int); g = sub[..., 1].astype(int); b = sub[..., 2].astype(int)
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = (mx - mn) / np.maximum(mx, 1)
    bright = (sat > 0.5) & (mx > 150)
    if bright.sum() < 5:
        l = (0.299*r + 0.587*g + 0.114*b)
        ml = float(l.mean())
        if ml < 80:
            return "black"
        elif ml < 160:
            return "dark_grey"
        return "light_grey"
    bright_pixels = sub[bright]
    rr = bright_pixels[:, 0].astype(int)
    gg = bright_pixels[:, 1].astype(int)
    bb = bright_pixels[:, 2].astype(int)
    if bool((rr > gg + 50).all()) and bool((rr > bb + 50).all()):
        return "red"
    if bool((gg > rr + 30).all()) and bool((gg > bb + 30).all()):
        return "green"
    if bool((bb > rr + 30).all()) and bool((bb > gg + 30).all()):
        return "blue"
    if bool((rr > 150).all()) and bool((gg > 100).all()) and bool((bb < 80).all()):
        return "orange"
    if bool((rr > 200).all()) and bool((gg > 200).all()) and bool((bb < 100).all()):
        return "yellow"
    return "other"


def parse_tsv(path):
    out = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)
        for row in reader:
            if len(row) < 12:
                continue
            try:
                if int(row[0]) != 5:
                    continue
                left = int(row[6]); top = int(row[7])
                width = int(row[8]); height = int(row[9])
                conf = float(row[10])
            except ValueError:
                continue
            text = row[11].strip()
            out.append({
                "text": text, "left": left, "top": top,
                "width": width, "height": height, "conf": conf,
            })
    return out


def find_blank_components(img, min_area=50, min_dim=12):
    """V3: min_area 50 (war 200 in V2) — fängt 2-3 zusätzliche Mikro-Regionen."""
    g = np.array(img.convert("L"))
    ink = g < 200
    blank = ~ink
    lbl, n = ndimage.label(blank)
    out = []
    h, w = blank.shape
    for i in range(1, n + 1):
        ys, xs = np.where(lbl == i)
        if len(ys) < min_area:
            continue
        x0, x1 = xs.min(), xs.max()
        y0, y1 = ys.min(), ys.max()
        rw, rh = x1 - x0 + 1, y1 - y0 + 1
        if rw < min_dim or rh < min_dim:
            continue
        if x0 < 30 and rw > 800: continue
        if x1 > w - 30 and rw > 800: continue
        if y0 < 30 and rh > 1400: continue
        out.append({
            "left": int(x0), "top": int(y0),
            "width": int(rw), "height": int(rh),
            "area_px": int(len(ys)),
            "bbox_area": int(rw * rh),
            "fill_ratio": float(len(ys) / max(1, rw * rh)),
        })
    return out


def find_colored_components(img, min_area=200, min_dim=12):
    a_rgb = np.array(img.convert("RGB"))
    r = a_rgb[..., 0].astype(int); g = a_rgb[..., 1].astype(int); b = a_rgb[..., 2].astype(int)
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = (mx - mn) / np.maximum(mx, 1)
    mask = (sat > 0.25) & (mx > 60)
    lbl, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lbl == i)
        if len(ys) < min_area:
            continue
        x0, x1 = xs.min(), xs.max()
        y0, y1 = ys.min(), ys.max()
        rw, rh = x1 - x0 + 1, y1 - y0 + 1
        if rw < min_dim or rh < min_dim:
            continue
        sub = a_rgb[y0:y1, x0:x1]
        rr = sub[..., 0].astype(int); gg = sub[..., 1].astype(int); bb = sub[..., 2].astype(int)
        mxx = np.maximum(np.maximum(rr, gg), bb)
        mnn = np.minimum(np.minimum(rr, gg), bb)
        ss = (mxx - mnn) / np.maximum(mxx, 1)
        if ss.max() < 0.85 or ss.mean() < 0.5 or (mxx > 200).mean() < 0.05:
            continue
        bright = sub[(ss > 0.5) & (mxx > 150)]
        if (bright[:, 0] > bright[:, 1] + 30).all() and (bright[:, 0] > bright[:, 2] + 30).all():
            color = "red"
        elif (bright[:, 2] > bright[:, 0] + 30).all():
            color = "blue"
        elif (bright[:, 1] > bright[:, 0] + 30).all():
            color = "green"
        else:
            color = "other"
        out.append({
            "left": int(x0), "top": int(y0),
            "width": int(rw), "height": int(rh),
            "area_px": int(len(ys)),
            "color": color,
        })
    return out


DIGIT_RE = re.compile(r"^\d+$")
FORMULA_RE = re.compile(
    r"^[\d\s×x\*\^\-/+\.()A-Za-zπµ_]+$"
)


def classify_page(n_words: int, n_blanks: int, n_colored: int, n_formulas: int):
    """V3: page_type Heuristik.
    Returns: page_type, blank_density
    """
    if n_words >= 100 and n_blanks == 0 and n_colored == 0:
        return "text_dense", 0.0
    if n_formulas >= 5 and n_blanks < 5:
        return "formula_dense", (n_blanks / max(1, n_words))
    if n_blanks >= 10 and n_words / max(1, n_blanks) > 30:
        return "sigill_dense", (n_blanks / max(1, n_words))
    return "mixed", (n_blanks / max(1, n_words))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    for i in range(1, 24):
        png = PNG_DIR / f"page-{i:02d}.png"
        tsv = TSV_DIR / f"p{i:02d}.tsv"
        if not png.exists() or not tsv.exists():
            print(f"  p{i:02d}: SKIP (missing input)")
            continue
        img = Image.open(png)
        a_rgb = np.array(img.convert("RGB"))
        words = parse_tsv(tsv)
        # Determine per-word color
        for w in words:
            w["color"] = detect_color_for_box(a_rgb, w["left"], w["top"],
                                               w["width"], w["height"])
        blanks = find_blank_components(img)
        colored = find_colored_components(img)

        # Digits and formulas
        sorted_words = sorted(words, key=lambda x: (x["top"], x["left"]))
        digits = []
        formulas = []
        cur_digits = []
        for w in sorted_words:
            t = w["text"]
            if DIGIT_RE.match(t):
                cur_digits.append(w)
            else:
                if cur_digits:
                    x0 = min(d["left"] for d in cur_digits)
                    y0 = min(d["top"] for d in cur_digits)
                    x1 = max(d["left"] + d["width"] for d in cur_digits)
                    y1 = max(d["top"] + d["height"] for d in cur_digits)
                    value = "".join(d["text"] for d in cur_digits)
                    if len(value) >= 2 and len(value) <= 5 and int(value) < 100000:
                        digits.append({
                            "value": value,
                            "bbox": [x0, y0, x1 - x0, y1 - y0],
                            "color": cur_digits[0]["color"],
                        })
                    cur_digits = []
        # Formulas per row
        rows = {}
        for w in sorted_words:
            key = w["top"] // 20
            rows.setdefault(key, []).append(w)
        for key, row_words in rows.items():
            row_text = "".join(w["text"] for w in sorted(row_words, key=lambda x: x["left"]))
            if any(c in row_text for c in ["^", "π", "×"]) and DIGIT_RE.search(row_text):
                x0 = min(w["left"] for w in row_words)
                y0 = min(w["top"] for w in row_words)
                x1 = max(w["left"] + w["width"] for w in row_words)
                y1 = max(w["top"] + w["height"] for w in row_words)
                symbols = re.findall(r"\d+|[A-Za-z]+|[^\sA-Za-z0-9]", row_text)
                formulas.append({
                    "raw": row_text,
                    "bbox": [x0, y0, x1 - x0, y1 - y0],
                    "symbols": symbols,
                    "color": row_words[0]["color"],
                })

        # V3: page_type classification
        page_type, blank_density = classify_page(
            n_words=len(words),
            n_blanks=len(blanks),
            n_colored=len(colored),
            n_formulas=len(formulas),
        )

        # Convert text_words to schema format
        text_words = [{
            "text": w["text"],
            "bbox": [w["left"], w["top"], w["width"], w["height"]],
            "conf_tesseract": w["conf"],
            "color": w["color"],
            "verified_by_vision": False,
        } for w in words]

        out = {
            "page": f"p{i:02d}",
            "image_size": list(img.size),
            "page_type": page_type,
            "blank_density": blank_density,
            "n_text_words": len(words),
            "n_blanks": len(blanks),
            "n_colored": len(colored),
            "n_digits": len(digits),
            "n_formulas": len(formulas),
            "text_words": text_words,
            "blank_regions": blanks,
            "colored_regions": colored,
            "digits": digits,
            "formulas": formulas,
        }
        (args.out / f"p{i:02d}.json").write_text(
            json.dumps(out, indent=2, ensure_ascii=False))
        print(f"  p{i:02d}: type={page_type}, "
              f"words={len(words)}, blanks={len(blanks)}, "
              f"colored={len(colored)}, formulas={len(formulas)}, "
              f"digits={len(digits)}")


if __name__ == "__main__":
    main()
