"""
phase11f_save_crops.py
V7 Phase 2f — Schneide die Rechen-Glyphen aus p17 aus und speichere sie

Damit wir visuell (oder per Code) prüfen können, ob es Ziffern 0-9 sind
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image

OUT = Path("bbox/mathe_ocr_20260707_V7")
OUT.mkdir(parents=True, exist_ok=True)

img = Image.open("pages_png/page-17.png").convert("L")
arr = np.array(img)

# Glyphen aus phase11e (in Reihenfolge Y, X)
glyphs = [
    {"y1": 261, "y2": 290, "x1": 889, "x2": 930, "label": "G1"},
    {"y1": 300, "y2": 390, "x1": 843, "x2": 950, "label": "G2"},
    {"y1": 370, "y2": 460, "x1": 843, "x2": 959, "label": "G3"},
    {"y1": 440, "y2": 530, "x1": 865, "x2": 945, "label": "G4"},
    {"y1": 510, "y2": 600, "x1": 862, "x2": 924, "label": "G5"},
    {"y1": 640, "y2": 730, "x1": 824, "x2": 906, "label": "G6"},
    {"y1": 1040, "y2": 1140, "x1": 854, "x2": 892, "label": "G7"},
    {"y1": 1240, "y2": 1430, "x1": 834, "x2": 878, "label": "G8"},
    {"y1": 1393, "y2": 1430, "x1": 812, "x2": 831, "label": "G9"},
]

for g in glyphs:
    crop = arr[g["y1"]:g["y2"], g["x1"]:g["x2"]]
    img_crop = Image.fromarray(crop)
    path = OUT / f"p17_{g['label']}.png"
    img_crop.save(path)
    # Statistik
    binary = (crop < 120).astype(int)
    n_white = binary.sum()
    n_total = crop.size
    fill_ratio = n_white / n_total
    print(f"{g['label']}: y={g['y1']}-{g['y2']}, x={g['x1']}-{g['x2']}, w={g['x2']-g['x1']}, h={g['y2']-g['y1']}, fill={fill_ratio:.2%}")

# Auch: Vergleiche mit Tengri-Glyphen-Größe (34px) vs Rechen-Glyphen-Größe (90px)
print(f"\nTengri-Fließtext-Glyphe (von p01): ~34x34px")
print(f"Rechen-Glyphen (p17): 90x90px = 2.6x größer")
print(f"Schluss: Rechen-Glyphen sind ein EIGENES Subsystem")

# Auch: Rechenstriche
striche = [
    {"y1": 273, "y2": 273, "x1": 183, "x2": 386, "label": "S1"},
    {"y1": 338, "y2": 338, "x1": 183, "x2": 638, "label": "S2"},
    {"y1": 403, "y2": 403, "x1": 183, "x2": 624, "label": "S3"},
    {"y1": 468, "y2": 468, "x1": 183, "x2": 579, "label": "S4"},
    {"y1": 533, "y2": 533, "x1": 183, "x2": 647, "label": "S5"},
    {"y1": 668, "y2": 668, "x1": 183, "x2": 560, "label": "S6"},
    {"y1": 1071, "y2": 1071, "x1": 184, "x2": 433, "label": "S7"},
    {"y1": 1274, "y2": 1274, "x1": 183, "x2": 600, "label": "S8"},
    {"y1": 1339, "y2": 1339, "x1": 183, "x2": 485, "label": "S9"},
    {"y1": 1404, "y2": 1404, "x1": 183, "x2": 592, "label": "S10"},
]
for s in striche:
    print(f"  Strich {s['label']}: x={s['x1']}-{s['x2']} (Länge={s['x2']-s['x1']})")
