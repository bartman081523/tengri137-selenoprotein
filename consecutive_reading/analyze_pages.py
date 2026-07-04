#!/usr/bin/env python3
"""
Tengri137 PNG analysis pipeline
================================

1) Latin text + numbers via tesseract (already done -> bbox/p{NN}.tsv)
2) Saturated (non-grayscale) ink detection — finds red/blue/green labels
3) Helligkeits-basierte Inversions-Maske — findet weiße Blobs (Sigill-Regionen)
4) Crops speichern (blank + colored)
5) Perceptual Hash + Ähnlichkeitssuche über alle Crops
   -> gruppiert wiederkehrende Glyphen (z. B. Raute+Punkt)
"""
import json
import csv
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")
PNG_DIR = ROOT / "pages_png"
TSV_DIR = ROOT / "bbox"
OUT_PAGES = ROOT / "bbox" / "pages"
OUT_CROPS = ROOT / "bbox" / "crops"
OUT_HASHES = ROOT / "bbox" / "hashes.json"
OUT_PAGES.mkdir(parents=True, exist_ok=True)
OUT_CROPS.mkdir(parents=True, exist_ok=True)


def parse_tsv(path):
    """Return list of word-level tokens: {text, left, top, width, height, conf}."""
    out = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)
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
            out.append({
                "text": text, "left": left, "top": top,
                "width": width, "height": height, "conf": conf,
            })
    return out


def detect_ink_mask(a_l):
    """Brightness-based ink mask: True = ink (dark), False = white."""
    return a_l < 200


def detect_color_mask(a_rgb):
    """Saturation-based colored-ink mask: True = colored, False = gray/white."""
    r = a_rgb[..., 0].astype(int)
    g = a_rgb[..., 1].astype(int)
    b = a_rgb[..., 2].astype(int)
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = (mx - mn).astype(float) / np.maximum(mx, 1)
    bright_enough = mx > 60  # ignore near-black
    return (sat > 0.25) & bright_enough


def find_components(mask, min_area=80, min_dim=10, exclude_outer_margins=True):
    """Connected components; returns list of dicts."""
    lbl, n = ndimage.label(mask)
    out = []
    h, w = mask.shape
    for i in range(1, n + 1):
        ys, xs = np.where(lbl == i)
        area = len(ys)
        if area < min_area:
            continue
        x0, x1 = xs.min(), xs.max()
        y0, y1 = ys.min(), ys.max()
        rw, rh = x1 - x0 + 1, y1 - y0 + 1
        if rw < min_dim or rh < min_dim:
            continue
        if exclude_outer_margins:
            if x0 < 30 and rw > 800:
                continue
            if x1 > w - 30 and rw > 800:
                continue
            if y0 < 30 and rh > 1400:
                continue
        out.append({
            "left": int(x0), "top": int(y0),
            "width": int(rw), "height": int(rh),
            "area_px": int(area),
        })
    return out


def phash(crop_pil, hash_size=16):
    """Perceptual hash (simple): resize, mean, threshold."""
    g = crop_pil.convert("L").resize((hash_size, hash_size), Image.LANCZOS)
    a = np.array(g, dtype=float)
    avg = a.mean()
    bits = (a > avg).astype(np.uint8).flatten()
    # pack into bytes
    h = 0
    for b in bits:
        h = (h << 1) | int(b)
    return f"{h:0{2 * len(bits) // 8}x}"


def hamming_hex(a, b):
    ha, hb = int(a, 16), int(b, 16)
    return bin(ha ^ hb).count("1")


def main():
    page_records = []
    all_crops = []  # (page, idx, kind, path, phash)

    for i in range(1, 24):
        png = PNG_DIR / f"page-{i:02d}.png"
        if not png.exists():
            continue
        img = Image.open(png)
        a_rgb = np.array(img.convert("RGB"))
        a_l = np.array(img.convert("L"))
        ink = detect_ink_mask(a_l)
        blank = ~ink
        colored = detect_color_mask(a_rgb)

        # Words from tesseract
        tsv = TSV_DIR / f"p{i:02d}.tsv"
        words = parse_tsv(tsv) if tsv.exists() else []

        # Connected components: blanks (sigill candidates) and colored
        blank_comps = find_components(blank, min_area=120, min_dim=12)
        col_comps_raw = find_components(colored, min_area=200, min_dim=12)
        # Re-filter colored components: average saturation inside bbox must
        # be high (kills anti-alias false positives). Also accept only one
        # "colored ink colour" per component (avg hue far from grey).
        col_comps = []
        for c in col_comps_raw:
            x0, y0 = c["left"], c["top"]
            x1, y0 + c["height"] if False else c["left"] + c["width"]
            x1 = c["left"] + c["width"]
            y1 = c["top"] + c["height"]
            sub = a_rgb[y0:y1, x0:x1]
            r = sub[..., 0].astype(int)
            g = sub[..., 1].astype(int)
            b = sub[..., 2].astype(int)
            mx = np.maximum(np.maximum(r, g), b)
            mn = np.minimum(np.minimum(r, g), b)
            sat = (mx - mn) / np.maximum(mx, 1)
            mean_sat = sat.mean()
            max_sat = sat.max()
            # Reject dark, low-sat regions — only accept strongly saturated,
            # bright pixels (pure red, blue, etc.)
            bright = (mx > 200).mean()
            if max_sat < 0.85 or mean_sat < 0.5 or bright < 0.05:
                continue
            c["mean_sat"] = float(mean_sat)
            c["max_sat"] = float(max_sat)
            c["bright_ratio"] = float(bright)
            col_comps.append(c)

        rec = {
            "page": f"p{i:02d}",
            "image_size": list(img.size),
            "words": words,
            "word_count": len(words),
            "blank_regions": blank_comps,
            "blank_region_count": len(blank_comps),
            "colored_regions": col_comps,
            "colored_region_count": len(col_comps),
        }
        page_records.append(rec)
        (OUT_PAGES / f"p{i:02d}.json").write_text(
            json.dumps(rec, indent=2, ensure_ascii=False))

        # Save crops
        for j, b in enumerate(blank_comps):
            x0 = max(0, b["left"] - 15)
            y0 = max(0, b["top"] - 15)
            x1 = min(img.size[0], b["left"] + b["width"] + 15)
            y1 = min(img.size[1], b["top"] + b["height"] + 15)
            crop = img.crop((x0, y0, x1, y1))
            p = OUT_CROPS / f"p{i:02d}_blank_{j:03d}.png"
            crop.save(p)
            all_crops.append({
                "page": f"p{i:02d}",
                "kind": "blank",
                "idx": j,
                "path": str(p.relative_to(ROOT)),
                "bbox": [b["left"], b["top"], b["width"], b["height"]],
                "phash": phash(crop),
            })
        for j, c in enumerate(col_comps):
            x0 = max(0, c["left"] - 15)
            y0 = max(0, c["top"] - 15)
            x1 = min(img.size[0], c["left"] + c["width"] + 15)
            y1 = min(img.size[1], c["top"] + c["height"] + 15)
            crop = img.crop((x0, y0, x1, y1))
            p = OUT_CROPS / f"p{i:02d}_color_{j:03d}.png"
            crop.save(p)
            all_crops.append({
                "page": f"p{i:02d}",
                "kind": "color",
                "idx": j,
                "path": str(p.relative_to(ROOT)),
                "bbox": [c["left"], c["top"], c["width"], c["height"]],
                "phash": phash(crop),
            })
        print(f"p{i:02d}: {len(words)} words, {len(blank_comps)} blank, "
              f"{len(col_comps)} color")

    # Write crops index
    (ROOT / "bbox" / "crops_index.json").write_text(
        json.dumps(all_crops, indent=2, ensure_ascii=False))

    # Similarity search: group crops by hamming distance <= 6 of phash
    clusters = []
    seen = set()
    for i, c in enumerate(all_crops):
        if i in seen:
            continue
        cluster = [i]
        for j in range(i + 1, len(all_crops)):
            if j in seen:
                continue
            if c["phash"] and all_crops[j]["phash"]:
                d = hamming_hex(c["phash"], all_crops[j]["phash"])
                if d <= 6:
                    cluster.append(j)
        for k in cluster[1:]:
            seen.add(k)
        seen.add(i)
        if len(cluster) >= 2:
            clusters.append({
                "size": len(cluster),
                "members": [{
                    "page": all_crops[k]["page"],
                    "kind": all_crops[k]["kind"],
                    "idx": all_crops[k]["idx"],
                    "phash": all_crops[k]["phash"],
                } for k in cluster],
            })

    # Sort clusters by size
    clusters.sort(key=lambda x: -x["size"])
    (ROOT / "bbox" / "similar_clusters.json").write_text(
        json.dumps(clusters, indent=2, ensure_ascii=False))
    print(f"\nTotal crops: {len(all_crops)}")
    print(f"Similar clusters (>= 2 members, hamming <= 6): {len(clusters)}")
    for cl in clusters[:20]:
        pages = sorted({m["page"] for m in cl["members"]})
        print(f"  cluster size={cl['size']:>3}  pages={pages[:5]}"
              f"{'…' if len(pages) > 5 else ''}")


if __name__ == "__main__":
    main()
