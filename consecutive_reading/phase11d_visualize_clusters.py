"""
phase11d_visualize_clusters.py
V7 Phase 2d — Visualisiere Ziffern-Cluster auf p17
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

OUT = Path("bbox/mathe_ocr_20260707_V7")
data = json.loads((OUT / "p17_ziffern.json").read_text())
clusters = data["clusters"]

# Annotiere p17
img = Image.open("pages_png/page-17.png").convert("RGB")
draw = ImageDraw.Draw(img)

for i, c in enumerate(clusters):
    x1, y1, x2, y2 = c["x_start"], c["y_start"], c["x_end"], c["y_end"]
    color = "red" if c["aspect"] > 5 else "blue"  # rot = Strich, blau = Ziffer
    draw.rectangle([x1, y1, x2, y2], outline=color, width=2)
    draw.text((x1, max(0, y1-15)), f"{i}", fill=color)

img.save(OUT / "p17_clusters_visualized.png")
print(f"Visualisierung gespeichert: {OUT}/p17_clusters_visualized.png")
print(f"  Rote Boxen = horizontale Striche (Cluster 0,1,...)")
print(f"  Blaue Boxen = echte Ziffern (rechte Spalte)")
