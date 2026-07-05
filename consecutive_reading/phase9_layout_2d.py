"""
phase9_layout_2d.py
V6 Phase 9 — 2D-Layout-Visualisierung der Bounding-Boxes pro Seite
Methode: Render alle Token-Bboxen mit ihrer Glyph-ID auf die Original-PNG
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

OUT = Path("bbox/layout_2d_20260706_V6")
OUT.mkdir(parents=True, exist_ok=True)

PAGES_PNG = Path("pages_png")
TOKENS = Path("bbox/tokenstream_20260706_V6_v3_17glyphs")

# Farben für Glyphen
COLORS = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8",
    "#FFD93D", "#6BCB77", "#C77DFF", "#FF85A1", "#7AE582",
    "#3A86FF", "#FB5607", "#8338EC", "#FFBE0B", "#00BBF9",
    "#06A77D", "#D62246", "#9B5DE5", "#F15BB5", "#FEE440"
]

def visualize_page(page_id: str):
    """Render Bbox-Layout einer Seite"""
    page_path = PAGES_PNG / f"page-{page_id[1:]}.png"
    token_path = TOKENS / f"{page_id}.json"

    if not page_path.exists():
        print(f"  {page_id}: page image missing")
        return
    if not token_path.exists():
        print(f"  {page_id}: token json missing")
        return

    img = Image.open(page_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    with open(token_path) as f:
        d = json.load(f)

    n = d["n_tokens"]
    if n == 0:
        print(f"  {page_id}: 0 tokens (skipped)")
        return

    # Gruppiere Tokens nach Y-Position (Zeilen)
    tokens = sorted(d["tokens"], key=lambda t: (t["y"], t["x"]))

    # Bbox-Render mit Glyph-ID
    unique_glyphs = sorted(set(t["glyph_id"] for t in tokens))
    color_map = {g: COLORS[i % len(COLORS)] for i, g in enumerate(unique_glyphs)}

    for tok in tokens:
        x, y, w, h = tok["x"], tok["y"], tok["w"], tok["h"]
        gid = tok["glyph_id"]
        c = color_map[gid]
        draw.rectangle([x, y, x+w, y+h], outline=c, width=2)
        # Glyph-ID als Label (klein)
        try:
            draw.text((x+1, y+1), gid, fill=c)
        except Exception:
            pass

    out_path = OUT / f"{page_id}_layout.png"
    img.save(out_path)
    print(f"  {page_id}: {n} tokens, {len(unique_glyphs)} unique glyphs -> {out_path.name}")

    return {
        "page_id": page_id,
        "n_tokens": n,
        "n_unique_glyphs": len(unique_glyphs),
        "glyphs": unique_glyphs,
        "x_range": [min(t["x"] for t in tokens), max(t["x"]+t["w"] for t in tokens)],
        "y_range": [min(t["y"] for t in tokens), max(t["y"]+t["h"] for t in tokens)],
        "tokens": tokens,
    }

# Verarbeite alle Seiten
print("=" * 60)
print("Phase 9: 2D-Layout-Visualisierung")
print("=" * 60)

results = []
for i in range(1, 24):
    page_id = f"p{i:02d}"
    r = visualize_page(page_id)
    if r:
        results.append(r)

# Strukturanalyse: Y-Lücken = Zeilen?
print("\n" + "=" * 60)
print("STRUKTURANALYSE: Zeilen- vs Spalten-Layout")
print("=" * 60)

analysis = []
for r in results:
    toks = r["tokens"]
    if not toks:
        continue
    # Y-Positionen
    ys = [t["y"] for t in toks]
    yh = [t["y"] + t["h"] for t in toks]
    # X-Positionen
    xs = [t["x"] for t in toks]
    xw = [t["x"] + t["w"] for t in toks]

    y_range = max(ys) - min(ys)
    x_range = max(xs) - min(xs)

    # Mittlere Token-Höhe
    heights = [t["h"] for t in toks]
    mean_h = np.mean(heights)

    # Y-Lücken (zur Zeilen-Detektion)
    y_sorted = sorted(set(ys))
    y_gaps = [y_sorted[i+1] - y_sorted[i] for i in range(len(y_sorted)-1)]
    y_gaps_gt_h = [g for g in y_gaps if g > mean_h * 0.5]

    # X-Lücken (innerhalb einer Zeile)
    x_sorted_per_y = {}
    for t in toks:
        yk = t["y"]
        x_sorted_per_y.setdefault(yk, []).append(t["x"])
    x_gaps_all = []
    for yk, xlist in x_sorted_per_y.items():
        xlist = sorted(xlist)
        gaps = [xlist[i+1] - xlist[i] for i in range(len(xlist)-1)]
        x_gaps_all.extend(gaps)
    x_gaps_gt_w = [g for g in x_gaps_all if g > mean_h * 0.3]

    analysis.append({
        "page_id": r["page_id"],
        "n_tokens": r["n_tokens"],
        "x_range": x_range,
        "y_range": y_range,
        "mean_h": round(mean_h, 1),
        "n_y_gaps_large": len(y_gaps_gt_h),
        "n_x_gaps_large": len(x_gaps_gt_w),
        "layout_signature": "COL2D" if x_range > 0 and y_range > 0 and (x_range / max(y_range, 1)) > 2.0 else ("COL-LINEAR" if x_range > 2 * y_range else "ROW-LINEAR"),
    })

print(f"{'Page':<6}{'Tokens':<8}{'X-span':<10}{'Y-span':<10}{'H':<6}{'Y-gaps':<8}{'X-gaps':<8}{'Layout'}")
print("-" * 70)
for a in analysis:
    print(f"{a['page_id']:<6}{a['n_tokens']:<8}{a['x_range']:<10}{a['y_range']:<10}{a['mean_h']:<6}{a['n_y_gaps_large']:<8}{a['n_x_gaps_large']:<8}{a['layout_signature']}")

# Speichern
with open(OUT / "layout_analysis.json", "w") as f:
    json.dump({
        "metadata": {
            "phase": "V6 / Phase 9",
            "method": "2D-Layout-Visualisierung + Strukturanalyse",
            "n_pages_with_tokens": len(results),
        },
        "page_analyses": analysis,
    }, f, indent=2, ensure_ascii=False)

print(f"\nOutput: {OUT}/")
print(f"  - {len(results)} Layout-PNGs (page_XX_layout.png)")
print(f"  - layout_analysis.json")
