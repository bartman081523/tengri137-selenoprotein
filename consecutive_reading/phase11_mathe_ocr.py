"""
phase11_mathe_ocr.py
V7 Phase 2 — Mathe-OCR p17 (und p18-p21, soweit möglich)

Methode: Pixel-basierte Bruchstrich-Detektion + Ziffern-Clustering
Da wir kein Tesseract-OCR und keine Glyph-zu-Ziffer-Mapping haben:
1. Detektiere horizontale Bruchstriche (lange, dunkle Linien)
2. Finde Ziffern-Cluster oberhalb und unterhalb jedes Bruchstrichs
3. Versuche, Ziffernformen manuell den 0-9 zuzuordnen
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image

OUT = Path("bbox/mathe_ocr_20260707_V7")
OUT.mkdir(parents=True, exist_ok=True)

# Lade p17
img = Image.open("pages_png/page-17.png").convert("L")
arr = np.array(img)
H, W = arr.shape
print(f"p17 size: {W}x{H}, mean brightness: {arr.mean():.1f}")

# 1. Bruchstrich-Detektion
# Ein Bruchstrich ist eine lange, dunkle, horizontale Linie
# Wir suchen Zeilen mit vielen dunklen Pixeln
threshold = 100  # dunkle Pixel
dark_per_row = (arr < threshold).sum(axis=1)

# Bruchstrich-Kandidaten: Zeilen mit >= 30% dunklen Pixeln in einer Reihe
candidates = []
for y in range(H):
    if dark_per_row[y] > 0.3 * W:
        candidates.append((y, dark_per_row[y]))

# Gruppiere benachbarte Kandidaten
groups = []
if candidates:
    cur_group = [candidates[0]]
    for c in candidates[1:]:
        if c[0] - cur_group[-1][0] <= 2:
            cur_group.append(c)
        else:
            y_start = cur_group[0][0]
            y_end = cur_group[-1][0]
            if y_end - y_start >= 1:  # mind. 1px hoch
                groups.append({
                    "y_start": y_start,
                    "y_end": y_end,
                    "y_center": (y_start + y_end) / 2,
                    "n_pixels": sum(c[1] for c in cur_group),
                    "mean_dark_per_row": np.mean([c[1] for c in cur_group]),
                })
            cur_group = [c]
    # Letzte Gruppe
    y_start = cur_group[0][0]
    y_end = cur_group[-1][0]
    if y_end - y_start >= 1:
        groups.append({
            "y_start": y_start,
            "y_end": y_end,
            "y_center": (y_start + y_end) / 2,
            "n_pixels": sum(c[1] for c in cur_group),
            "mean_dark_per_row": np.mean([c[1] for c in cur_group]),
        })

print(f"\nBruchstrich-Kandidaten: {len(groups)}")
for g in groups[:15]:
    print(f"  y={g['y_start']}-{g['y_end']} (center={g['y_center']:.0f}), dark-px={g['n_pixels']}")

# 2. Ziffern-Detektion: Finde Cluster zwischen den Bruchstrichen
# Wir definieren Segmente: Bereich zwischen zwei aufeinanderfolgenden Bruchstrichen
# ist ein "Rechnungs-Block" mit potentiellen Ziffern oberhalb und unterhalb

# Wenn nur ein Bruchstrich pro Block: Zähler oben, Nenner unten
# Wenn kein Bruchstrich: einfach horizontaler Text

# Filtere Bruchstrich-Kandidaten: Linien mit >= 20% Breite und konsistent dunkel
bruch_strich = [g for g in groups if g["mean_dark_per_row"] > 0.3 * W]
print(f"\nEchte Bruchstriche: {len(bruch_strich)}")

# Definiere Blöcke: Bereich zwischen Bruchstrich-Paaren
blocks = []
if bruch_strich:
    # Block vor erstem Bruchstrich (Titel/Zahl)
    blocks.append({
        "type": "PRE",
        "y_start": 0,
        "y_end": bruch_strich[0]["y_start"],
        "n_lines": 0,
    })
    # Zwischen Blöcke
    for i in range(len(bruch_strich) - 1):
        blocks.append({
            "type": "BETWEEN",
            "y_start": bruch_strich[i]["y_end"],
            "y_end": bruch_strich[i+1]["y_start"],
            "n_lines": 1,
            "between_two_fractions": True,
        })
    # Block nach letztem Bruchstrich
    blocks.append({
        "type": "POST",
        "y_start": bruch_strich[-1]["y_end"],
        "y_end": H,
        "n_lines": 0,
    })

print(f"\nBlöcke: {len(blocks)}")
for b in blocks[:15]:
    print(f"  {b['type']}: y={b['y_start']}-{b['y_end']} (h={b['y_end']-b['y_start']})")

# 3. Ziffern-Cluster pro Block
# Ein "Ziffern-Cluster" ist eine zusammenhängende Region dunkler Pixel
from scipy import ndimage

def find_clusters(arr_region, threshold=100, min_size=20):
    """Finde zusammenhängende dunkle Regionen"""
    binary = (arr_region < threshold).astype(int)
    labeled, n = ndimage.label(binary)
    clusters = []
    for i in range(1, n+1):
        mask = (labeled == i)
        size = mask.sum()
        if size >= min_size:
            ys, xs = np.where(mask)
            clusters.append({
                "x_start": int(xs.min()),
                "x_end": int(xs.max()),
                "y_start_local": int(ys.min()),
                "y_end_local": int(ys.max()),
                "size": int(size),
                "n_pixels": int(size),
            })
    return clusters

# Für jeden Block: finde Ziffern-Cluster
print("\n" + "=" * 60)
print("ZIFFERN-CLUSTER PRO BLOCK")
print("=" * 60)

all_results = []
for i, b in enumerate(blocks):
    region = arr[b["y_start"]:b["y_end"], :]
    clusters = find_clusters(region, threshold=100, min_size=20)
    # Sortiere nach X-Position
    clusters = sorted(clusters, key=lambda c: c["x_start"])
    print(f"\nBlock {i} ({b['type']}, y={b['y_start']}-{b['y_end']}): {len(clusters)} Cluster")
    for j, c in enumerate(clusters):
        # Versuche, Cluster zu charakterisieren
        cluster_img = region[c["y_start_local"]:c["y_end_local"]+1, c["x_start"]:c["x_end"]+1]
        h = cluster_img.shape[0]
        w = cluster_img.shape[1]
        aspect = w / max(h, 1)
        density = c["n_pixels"] / (h * w)
        # Globale Koordinaten
        c["x_global"] = c["x_start"]
        c["y_global"] = b["y_start"] + c["y_start_local"]
        c["height"] = h
        c["width"] = w
        c["aspect"] = round(aspect, 2)
        c["density"] = round(density, 3)
        print(f"  Cluster {j}: x={c['x_global']}, y={c['y_global']}, w={w}xh={h}, aspect={aspect:.2f}, density={density:.2f}, n_px={c['n_pixels']}")
    all_results.append({
        "block": b,
        "clusters": clusters,
    })

# Speichern
with open(OUT / "p17_mathe_analysis.json", "w") as f:
    json.dump({
        "metadata": {
            "phase": "V7 / Phase 2",
            "method": "Pixel-basierte Bruchstrich-Detektion + Ziffern-Clustering",
            "page": "p17",
        },
        "bruch_strich_count": len(bruch_strich),
        "blocks": all_results,
    }, f, indent=2, ensure_ascii=False)

print(f"\nOutput: {OUT}/p17_mathe_analysis.json")
