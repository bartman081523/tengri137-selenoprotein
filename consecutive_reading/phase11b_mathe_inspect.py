"""
phase11b_mathe_inspect.py
V7 Phase 2b — Genauere Inspektion p17

Methode: Visualisiere p17 mit Heatmap, um zu sehen, wo die "dunklen" Strukturen sind
"""
import numpy as np
from PIL import Image
import json
from pathlib import Path

OUT = Path("bbox/mathe_ocr_20260707_V7")
OUT.mkdir(parents=True, exist_ok=True)

img = Image.open("pages_png/page-17.png").convert("L")
arr = np.array(img)
H, W = arr.shape
print(f"p17 size: {W}x{H}, mean brightness: {arr.mean():.1f}")
print(f"  min: {arr.min()}, max: {arr.max()}")
print(f"  <  50: {(arr < 50).sum()} px (sehr dunkel)")
print(f"  < 100: {(arr < 100).sum()} px (dunkel)")
print(f"  < 150: {(arr < 150).sum()} px (mittel)")
print(f"  < 200: {(arr < 200).sum()} px (hell)")

# Pro Zeile: Anteil dunkler Pixel
print("\nDunkle Pixel pro Zeile (nur Zeilen mit > 20% Dunkelheit):")
for y in range(H):
    dark = (arr[y] < 100).sum()
    if dark > 0.2 * W:
        print(f"  y={y}: {dark}/{W} = {dark/W:.1%}")

# Suche nach HORIZONTALEN Strichen (1-2 px hoch, lang)
print("\nMögliche Bruchstrich-Zeilen (3-5px hoch, mit 30%+ dunklen Pixeln):")
y_candidates = []
for y in range(2, H-2):
    # 5px-Summe
    block = arr[y-2:y+3, :]
    block_dark = (block < 100).sum()
    if block_dark > 5 * 0.3 * W:  # mind. 30% über 5 Zeilen
        y_candidates.append((y, block_dark))

# Gruppiere benachbarte
groups = []
if y_candidates:
    cur = [y_candidates[0]]
    for c in y_candidates[1:]:
        if c[0] - cur[-1][0] <= 3:
            cur.append(c)
        else:
            groups.append(cur)
            cur = [c]
    groups.append(cur)

print(f"\nGefundene Strich-Gruppen: {len(groups)}")
for g in groups:
    y_start = g[0][0]
    y_end = g[-1][0]
    n_dark = sum(c[1] for c in g)
    print(f"  y={y_start}-{y_end} (h={y_end-y_start+1}), total dark={n_dark}")
