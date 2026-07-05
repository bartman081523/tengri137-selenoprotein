"""
phase11e_full_extract.py
V7 Phase 2e — Vollständige Ziffern-Extraktion aus p17

Methode: 1) Grobe Lage der Spalten (links/Mitte/rechts)
        2) Pro Spalte: finde alle Glyph-Cluster
        3) Extrahiere Pixel-Muster pro Cluster
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

OUT = Path("bbox/mathe_ocr_20260707_V7")
img = Image.open("pages_png/page-17.png").convert("L")
arr = np.array(img)
H, W = arr.shape

# Pro Y-Band finde Cluster mit größerer Toleranz
rows = [
    (200, 290, "R1"),
    (300, 390, "R2"),
    (370, 460, "R3"),
    (440, 530, "R4"),
    (510, 600, "R5"),
    (640, 730, "R6"),
    (1040, 1140, "R7"),
    (1240, 1430, "R8-10"),
]

# Threshold etwas höher (mehr Glyph-Cluster erlauben)
all_clusters = []
for y1, y2, label in rows:
    region = arr[y1:y2, :]
    binary = (region < 120).astype(int)
    labeled, n = ndimage.label(binary)
    clusters = []
    for i in range(1, n+1):
        mask = (labeled == i)
        size = mask.sum()
        if size >= 100:  # höhere Mindestgröße
            ys, xs = np.where(mask)
            clusters.append({
                "x1": int(xs.min()),
                "x2": int(xs.max()),
                "y1": int(ys.min()) + y1,
                "y2": int(ys.max()) + y1,
                "size": int(size),
                "w": int(xs.max() - xs.min() + 1),
                "h": int(ys.max() - ys.min() + 1),
            })
    clusters = sorted(clusters, key=lambda c: c["x1"])
    print(f"\n{label} (y={y1}-{y2}): {len(clusters)} Cluster")
    for c in clusters:
        c["row"] = label
        c["aspect"] = round(c["w"] / max(c["h"], 1), 2)
        # Klassifiziere: Strich (aspect > 5) vs Glyph
        c["type"] = "STRICH" if c["aspect"] > 5 else "GLYPH"
        print(f"  x={c['x1']}-{c['x2']} (w={c['w']}, h={c['h']}, aspect={c['aspect']:.1f}) [{c['type']}], n_px={c['size']}")
    all_clusters.extend(clusters)

# Strich-Trennung: Finde vertikale Position der "Rechenstriche"
striche = [c for c in all_clusters if c["type"] == "STRICH"]
print(f"\nRechenstriche: {len(striche)}")
for s in striche:
    print(f"  y={s['y1']}-{s['y2']}, x={s['x1']}-{s['x2']}, w={s['w']}")

# Glyphen in der rechten Spalte (x > 800)
glyphs_rechts = [c for c in all_clusters if c["type"] == "GLYPH" and c["x1"] > 800]
print(f"\nGlyphen rechts (Ziffern-Spalte): {len(glyphs_rechts)}")
for g in sorted(glyphs_rechts, key=lambda c: (c["y1"], c["x1"])):
    print(f"  y={g['y1']}, x={g['x1']}-{g['x2']}, w={g['w']}, h={g['h']}, n_px={g['size']}")

# Visualisierung
img_color = Image.open("pages_png/page-17.png").convert("RGB")
draw = ImageDraw.Draw(img_color)
for c in all_clusters:
    color = "red" if c["type"] == "STRICH" else "blue"
    draw.rectangle([c["x1"], c["y1"], c["x2"], c["y2"]], outline=color, width=2)
img_color.save(OUT / "p17_v2_visualized.png")
print(f"\nVisualisierung: {OUT}/p17_v2_visualized.png")
