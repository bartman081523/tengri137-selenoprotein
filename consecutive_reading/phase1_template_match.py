#!/usr/bin/env python3
"""
phase1_template_match.py — V6 Phase 1: Template-Matching (DevMind).

V6 PIVOT: cv2.matchTemplate auf alle 23 Seiten mit den 25 Referenz-Glyphen
aus Phase 0 (glyphs_final.json).

Algorithmus:
1. Lade 25 Template-Crops (PNG, 10-25x20-30 px)
2. Pro Page: lade PNG, konvertiere zu Grayscale
3. Multi-Scale Template-Match: 1.0x, 1.25x, 1.5x (Tengri kann leicht variieren)
4. Threshold 0.80 (streng, um False-Positives zu vermeiden)
5. Non-Max-Suppression: max 1 Match pro 25x25-px-Fenster
6. Output: Token-Stream pro Page

Output: bbox/tokenstream_20260706_V6/p{NN}.json
        {
          "page_id": "p01",
          "n_tokens": 47,
          "tokens": [
            {"glyph_id": "G01", "x": 210, "y": 425, "w": 13, "h": 25, "conf": 0.92},
            ...
          ]
        }
"""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def match_template(page_gray: np.ndarray, template: np.ndarray,
                   threshold: float = 0.80, scales: list = None) -> list:
    """Template-Match mit Multi-Scale + Non-Max-Suppression."""
    if scales is None:
        scales = [1.0]

    all_matches = []
    ph, pw = page_gray.shape
    th, tw = template.shape

    for scale in scales:
        # Skaliere Template
        new_w = int(tw * scale)
        new_h = int(th * scale)
        if new_w < 5 or new_h < 5 or new_w > pw or new_h > ph:
            continue
        scaled = cv2.resize(template, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        # Match
        result = cv2.matchTemplate(page_gray, scaled, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)

        for pt in zip(*locations):
            x, y = pt[1], pt[0]  # (x, y)
            conf = float(result[y, x])
            all_matches.append({
                "x": int(x), "y": int(y),
                "w": int(new_w), "h": int(new_h),
                "conf": round(conf, 3),
                "scale": scale
            })

    # Non-Max-Suppression
    return non_max_suppression(all_matches, overlap_thresh=0.3)


def non_max_suppression(matches: list, overlap_thresh: float = 0.3) -> list:
    """Unterdrücke überlappende Matches (behalte höchste Confidence)."""
    if not matches:
        return []

    # Sortiere nach Confidence (höchste zuerst)
    matches = sorted(matches, key=lambda m: -m["conf"])

    kept = []
    for m in matches:
        # Prüfe ob Match mit einem bereits gehaltenen Match überlappt
        overlap = False
        for k in kept:
            # Berechne IoU
            x1 = max(m["x"], k["x"])
            y1 = max(m["y"], k["y"])
            x2 = min(m["x"] + m["w"], k["x"] + k["w"])
            y2 = min(m["y"] + m["h"], k["y"] + k["h"])
            if x2 <= x1 or y2 <= y1:
                continue
            inter = (x2 - x1) * (y2 - y1)
            area_m = m["w"] * m["h"]
            area_k = k["w"] * k["h"]
            union = area_m + area_k - inter
            iou = inter / union if union > 0 else 0
            if iou > overlap_thresh:
                overlap = True
                break
        if not overlap:
            kept.append(m)

    return kept


def process_page(page_id: str, pages_png_dir: Path, refs_dir: Path,
                 glyphs_final: list, threshold: float = 0.80,
                 scales: list = None) -> dict:
    """Pro Page: Template-Match mit allen Referenz-Glyphen."""
    page_num = int(page_id[1:])
    png_path = pages_png_dir / f"page-{page_num:02d}.png"
    if not png_path.exists():
        return {"page_id": page_id, "n_tokens": 0, "tokens": [], "error": "page_png_missing"}

    page_img = np.array(Image.open(png_path).convert("L"))

    all_tokens = []
    for glyph in glyphs_final:
        gid = glyph["glyph_id"]
        ref_path = refs_dir / f"{gid}.png"
        if not ref_path.exists():
            continue
        template = np.array(Image.open(ref_path).convert("L"))
        if template.size == 0:
            continue

        matches = match_template(page_img, template, threshold=threshold, scales=scales)
        for m in matches:
            all_tokens.append({
                "glyph_id": gid,
                "x": m["x"], "y": m["y"],
                "w": m["w"], "h": m["h"],
                "conf": m["conf"],
                "scale": m["scale"]
            })

    # Sortiere nach Lesereihenfolge (y zuerst, dann x)
    all_tokens.sort(key=lambda t: (t["y"], t["x"]))

    return {
        "page_id": page_id,
        "n_tokens": len(all_tokens),
        "tokens": all_tokens,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glyphs-final", type=Path, required=True,
                    help="bbox/glyph_refs_20260706_V6/glyphs_final.json")
    ap.add_argument("--refs", type=Path, required=True,
                    help="bbox/glyph_refs_20260706_V6/refs/")
    ap.add_argument("--pages-png", type=Path, required=True,
                    help="pages_png/")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/tokenstream_20260706_V6/")
    ap.add_argument("--threshold", type=float, default=0.80)
    ap.add_argument("--scales", type=str, default="1.0",
                    help="Comma-separated scales, e.g. '0.9,1.0,1.1'")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    scales = [float(s) for s in args.scales.split(",")]
    glyphs_final = json.loads(args.glyphs_final.read_text())["glyphs"]
    print(f"Template-Match: {len(glyphs_final)} Glyphen, threshold={args.threshold}, scales={scales}")
    print(f"Refs: {args.refs}")
    print(f"Pages: {args.pages_png}")
    print()

    total_tokens = 0
    for i in range(1, 24):
        page_id = f"p{i:02d}"
        result = process_page(page_id, args.pages_png, args.refs, glyphs_final,
                              threshold=args.threshold, scales=scales)
        n = result["n_tokens"]
        total_tokens += n
        out_path = args.out / f"{page_id}.json"
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        # Glyph-Verteilung
        from collections import Counter
        gid_counts = Counter(t["glyph_id"] for t in result["tokens"])
        top3 = ", ".join(f"{g}={c}" for g, c in gid_counts.most_common(3))
        print(f"  {page_id}: {n:3d} tokens (top: {top3})")

    print(f"\n[Phase 1] Total: {total_tokens} Tokens über 23 Pages")


if __name__ == "__main__":
    main()
