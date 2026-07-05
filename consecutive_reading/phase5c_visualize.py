#!/usr/bin/env python3
"""
phase5c_visualize.py — V6 Phase 5c: Wortgrenzen-Visualisierung auf p01.

Zeichnet die segmentierten Wörter auf p01 als farbige Boxen, damit
visuell verifizierbar ist, dass die Gap-basierten Wortgrenzen sinnvoll sind.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page-png", type=Path, required=True)
    ap.add_argument("--tokenstream", type=Path, required=True)
    ap.add_argument("--page", type=str, default="p01")
    ap.add_argument("--gap-threshold", type=int, default=80)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    ts_path = args.tokenstream / f"{args.page}.json"
    d = json.loads(ts_path.read_text())
    toks = sorted(d["tokens"], key=lambda t: (t["y"], t["x"]))

    # Segmentiere
    words = []
    if toks:
        cur = [toks[0]]
        for i in range(1, len(toks)):
            prev, cur_tok = toks[i-1], toks[i]
            gap = cur_tok["x"] - (prev["x"] + prev["w"])
            if gap > args.gap_threshold:
                words.append(cur)
                cur = [cur_tok]
            else:
                cur.append(cur_tok)
        words.append(cur)

    print(f"Page {args.page}: {len(toks)} tokens, {len(words)} Wörter")

    # Bild mit Annotationen
    img = Image.open(args.page_png).convert("RGB")
    draw = ImageDraw.Draw(img)

    colors = [
        (255, 0, 0), (0, 200, 0), (0, 0, 255), (255, 165, 0),
        (128, 0, 128), (0, 200, 200), (200, 0, 200), (100, 100, 0),
    ]

    for w_idx, word in enumerate(words):
        color = colors[w_idx % len(colors)]
        for t in word:
            x, y, w, h = t["x"], t["y"], t["w"], t["h"]
            # Bbox zeichnen
            draw.rectangle([x-2, y-2, x+w+2, y+h+2], outline=color, width=2)
        # Wort-Label
        if word:
            first = word[0]
            label = f"W{w_idx+1}"
            draw.text((first["x"] - 30, first["y"] - 15), label, fill=color)

    # Wort-Zusammenfassung
    summary_lines = [f"Page {args.page}: {len(words)} Wörter (Gap > {args.gap_threshold}px)"]
    for w_idx, word in enumerate(words[:30]):  # Erste 30
        glyphs = "+".join(t["glyph_id"] for t in word)
        summary_lines.append(f"  W{w_idx+1}: {glyphs}")
    if len(words) > 30:
        summary_lines.append(f"  ... ({len(words) - 30} more)")

    # Summary in neues Bild schreiben
    sum_w, sum_h = 600, max(800, 20 * len(summary_lines) + 30)
    sum_img = Image.new("RGB", (sum_w, sum_h), "white")
    sum_draw = ImageDraw.Draw(sum_img)
    for i, line in enumerate(summary_lines):
        sum_draw.text((10, 10 + i * 18), line, fill="black")
    sum_img.save(args.out.parent / f"{args.page}_word_summary.png")

    img.save(args.out)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
