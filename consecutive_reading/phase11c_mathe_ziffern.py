"""
phase11c_mathe_ziffern.py
V7 Phase 2c — Ziffern-Cluster pro Ziffern-Reihe auf p17

Methode: Finde Ziffern-Cluster in den 5+ dunklen Zeilen-Bändern
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

OUT = Path("bbox/mathe_ocr_20260707_V7")
OUT.mkdir(parents=True, exist_ok=True)

img = Image.open("pages_png/page-17.png").convert("L")
arr = np.array(img)
H, W = arr.shape

# Ziffern-Reihen (aus Inspektion)
rows = [
    {"y_start": 260, "y_end": 290, "label": "ROW_1"},   # 435 ?
    {"y_start": 325, "y_end": 355, "label": "ROW_2"},   # 370 ?
    {"y_start": 390, "y_end": 420, "label": "ROW_3"},   # 20 ?
    {"y_start": 455, "y_end": 485, "label": "ROW_4"},   # ...
    {"y_start": 520, "y_end": 550, "label": "ROW_5"},   # 655
    {"y_start": 655, "y_end": 685, "label": "ROW_6"},   # 599
    {"y_start": 1055, "y_end": 1090, "label": "ROW_7"},  # 2.5
    {"y_start": 1260, "y_end": 1290, "label": "ROW_8"},  # ??
    {"y_start": 1325, "y_end": 1355, "label": "ROW_9"},  # ??
    {"y_start": 1390, "y_end": 1420, "label": "ROW_10"},  # ??
]

def find_clusters_in_band(arr, y_start, y_end, x_start=0, x_end=None, threshold=100, min_size=30):
    """Finde zusammenhängende dunkle Cluster in einem Band"""
    if x_end is None:
        x_end = arr.shape[1]
    region = arr[y_start:y_end, x_start:x_end]
    binary = (region < threshold).astype(int)
    labeled, n = ndimage.label(binary)
    clusters = []
    for i in range(1, n+1):
        mask = (labeled == i)
        size = mask.sum()
        if size >= min_size:
            ys, xs = np.where(mask)
            clusters.append({
                "x_start": int(xs.min()) + x_start,
                "x_end": int(xs.max()) + x_start,
                "y_start": int(ys.min()) + y_start,
                "y_end": int(ys.max()) + y_start,
                "size": int(size),
                "w": int(xs.max() - xs.min() + 1),
                "h": int(ys.max() - ys.min() + 1),
                "x_center": int((xs.min() + xs.max()) / 2) + x_start,
                "y_center": int((ys.min() + ys.max()) / 2) + y_start,
            })
    return sorted(clusters, key=lambda c: c["x_start"])

print("=" * 70)
print("ZIFFERN-CLUSTER PRO REIHE (p17)")
print("=" * 70)

all_ziffern = []
for row in rows:
    clusters = find_clusters_in_band(arr, row["y_start"], row["y_end"], min_size=30)
    print(f"\n{row['label']} (y={row['y_start']}-{row['y_end']}): {len(clusters)} Cluster")
    for j, c in enumerate(clusters):
        # Versuche Ziffern-Identifikation
        # Aspekt-Ratio: schmal=1, breit=mehrere Ziffern
        # Einzelne Ziffern: w/h ~ 0.5-0.8
        # Mehrere Ziffern: w/h > 1.5
        ratio = c["w"] / max(c["h"], 1)
        n_digits_est = max(1, round(c["w"] / 25))  # ~25px pro Ziffer
        print(f"  Cluster {j}: x={c['x_start']}-{c['x_end']} (w={c['w']}, h={c['h']}, ratio={ratio:.2f}), n_px={c['size']}, est_digits={n_digits_est}")
        c["row"] = row["label"]
        c["aspect"] = round(ratio, 2)
        c["est_digits"] = n_digits_est
        all_ziffern.append(c)

# Statistik
total_clusters = len(all_ziffern)
total_pixels = sum(c["size"] for c in all_ziffern)
unique_x_positions = set(c["x_center"] // 50 for c in all_ziffern)  # bins
print(f"\n" + "=" * 70)
print("STATISTIK")
print(f"  Cluster total: {total_clusters}")
print(f"  Unique X-Bins (50px): {len(unique_x_positions)}")
print(f"  Geschätzte Ziffern total: {sum(c['est_digits'] for c in all_ziffern)}")

# Save
with open(OUT / "p17_ziffern.json", "w") as f:
    json.dump({
        "metadata": {
            "phase": "V7 / Phase 2c",
            "method": "Ziffern-Cluster pro Band",
            "page": "p17",
        },
        "n_clusters": total_clusters,
        "clusters": all_ziffern,
    }, f, indent=2, ensure_ascii=False)

print(f"\nOutput: {OUT}/p17_ziffern.json")
