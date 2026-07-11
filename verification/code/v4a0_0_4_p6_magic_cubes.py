"""
V4a0.0.4: p6 Magic Cubes systematisch erfassen
==============================================

Korrektur (User-Feedback 2026-07-11):
- 2 Magic Cubes, je 3 Ebenen (3x3-Grid mit 9 Zahlen)
- Pro Magic Cube: 27 arabische Zahlen
- Beschriftung: Rote Tengri-Glyphen-Zeile + Punkt + arabische Ziffer (1 oder 2)
- Zwischen den Cubes: 3 Zeilen schwarze Tengri-Glyphen
- Hebräisch ist HALLUZINATION

Methode:
1. Finde die 6 Ebenen-Container (500x166 aus V4a0.0.2)
2. Pro Ebene: 3x3 Sub-Container (9 Zahlen)
3. Tesseract psm 8 (digits only) auf jede Zahl-Zelle
4. Visuelle Verifikation + cross-check mit Vision
"""

import json
import sys
from pathlib import Path
import numpy as np
import cv2
import pytesseract

ROOT = Path("/run/media/julian/ML4/tengri137")
PAGES = ROOT / "original_sources" / "137"
RESULTS = ROOT / "verification" / "results" / "snapshots"
CROPS = RESULTS / "v4a0_0_4_p6_cubes"
CROPS.mkdir(parents=True, exist_ok=True)


def find_3x3_grids_in_region(img, region):
    """Suche 3x3-Grid-Container in einer Region"""
    x, y, w, h = region['x'], region['y'], region['w'], region['h']
    sub = img[y:y+h, x:x+w]
    gray = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY) if len(sub.shape) == 3 else sub

    # Threshold
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Finde Connected Components (Zahlen + Glyphen)
    n_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)

    # Suche Zahlen-CCs: height ~30-50, width ~20-40, keine Glyphen-Bereiche
    numbers = []
    for i in range(1, n_labels):
        xx, yy, ww, hh, area = stats[i]
        if 15 < hh < 60 and 8 < ww < 50 and 50 < area < 2000:
            # Tesseract psm 8 versuchen
            cell = sub[yy:yy+hh, xx:xx+ww]
            # preprocess
            cell_gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY) if len(cell.shape) == 3 else cell
            _, cell_binary = cv2.threshold(cell_gray, 180, 255, cv2.THRESH_BINARY)
            cell_scaled = cv2.resize(cell_binary, (ww*3, hh*3), interpolation=cv2.INTER_CUBIC)
            try:
                txt = pytesseract.image_to_string(
                    cell_scaled,
                    config='--psm 8 -c tessedit_char_whitelist=0123456789'
                ).strip()
            except:
                txt = ""
            numbers.append({
                "local_x": int(xx), "local_y": int(yy), "w": int(ww), "h": int(hh),
                "area": int(area),
                "global_x": int(xx + x), "global_y": int(yy + y),
                "ocr": txt
            })
    return numbers


def main():
    page_num = 6
    png_path = PAGES / f"P00{page_num}.png"
    print(f"Lade {png_path}...")
    img = cv2.imread(str(png_path))
    if img is None:
        sys.exit(1)

    h, w = img.shape[:2]
    print(f"Bild: {w}x{h}")

    # 6 Ebenen-Container aus V4a0.0.2 (y=1158, 1312, 1479, dann gestapelt für 2. Cube)
    # Tatsächlich sind 3 Container sichtbar (CC#63, #91, #132) — das ist 1 Magic Cube mit 3 Ebenen
    # Der 2. Magic Cube müsste darunter oder davor liegen
    # Lass uns die Y-Positionen systematisch finden

    # Connected Components für große Container
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    n_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)

    # Große rechteckige Container (Magic-Cube-Ebenen)
    big_containers = []
    for i in range(1, n_labels):
        x, y, ww, hh, area = stats[i]
        # Magic-Cube-Ebene: ~500x150, area > 5000
        if area > 4000 and ww > 200 and hh > 100 and abs(ww/hh - 3) < 1.0:  # 3:1 ratio
            big_containers.append({
                "label": int(i),
                "x": int(x), "y": int(y), "w": int(ww), "h": int(hh),
                "area": int(area),
                "aspect": float(ww/hh)
            })
    big_containers_sorted = sorted(big_containers, key=lambda r: (r['y'], r['x']))
    print(f"\nMagic-Cube-Ebenen-Container gefunden: {len(big_containers_sorted)}")
    for c in big_containers_sorted:
        print(f"  CC#{c['label']}: ({c['x']},{c['y']}) {c['w']}x{c['h']} aspect={c['aspect']:.2f}")

    # Pro Container: Zahlen extrahieren
    cubes_data = []
    for c in big_containers_sorted:
        numbers = find_3x3_grids_in_region(img, c)
        # Sortiere nach Y dann X
        numbers_sorted = sorted(numbers, key=lambda n: (n['local_y'], n['local_x']))

        # Gruppiere in 3x3-Grid
        if len(numbers_sorted) >= 9:
            # Finde 3 Zeilen (clustering auf y)
            ys = [n['local_y'] for n in numbers_sorted]
            row_clusters = []
            current_cluster = [numbers_sorted[0]]
            for n in numbers_sorted[1:]:
                if n['local_y'] - current_cluster[-1]['local_y'] < 30:
                    current_cluster.append(n)
                else:
                    row_clusters.append(current_cluster)
                    current_cluster = [n]
            row_clusters.append(current_cluster)

            print(f"\n  Container CC#{c['label']} (y={c['y']}): {len(row_clusters)} Zeilen-Cluster, "
                  f"{len(numbers_sorted)} Zahlen total")
            grid = []
            for ri, row in enumerate(row_clusters[:3]):
                row_sorted = sorted(row, key=lambda n: n['local_x'])
                row_data = []
                for n in row_sorted[:3]:
                    print(f"    R{ri}: ({n['global_x']},{n['global_y']}) ocr={n['ocr']!r}")
                    row_data.append(n)
                grid.append(row_data)

            cubes_data.append({
                "container": c,
                "n_numbers_total": len(numbers_sorted),
                "n_rows": len(row_clusters),
                "grid_3x3": [[n['ocr'] for n in row] for row in grid],
                "all_numbers": numbers_sorted
            })

    # Speichere
    output = {
        "method": "V4a0.0.4 = Magic-Cube-Ebenen-Detection auf p6 (Refactor: User-Korrektur: 2 Cubes à 3 Ebenen × 9 Zahlen = 54 Zahlen total, KEIN Hebräisch)",
        "timestamp": "2026-07-11",
        "image": str(png_path.relative_to(ROOT)),
        "user_correction": "2 Magic Cubes mit je 3 Ebenen (3x3-Grid, 9 Zahlen pro Ebene). "
                           "Beschriftung: rote Tengri-Glyphen + Punkt + arabische Ziffer 1/2. "
                           "3 Zeilen schwarze Tengri-Glyphen zwischen den Cubes. "
                           "Hebräisch ist Halluzination.",
        "containers_detected": big_containers_sorted,
        "cubes_data": cubes_data,
        "faktum_status": "Falls 6 Ebenen-Container gefunden: 2 Cubes × 27 Zahlen = 54 Zahlen verifiziert. "
                          "Falls nur 3: nur 1 Cube erfasst, 2. Cube noch offen."
    }

    out_path = RESULTS / "v4a0_0_4_p6_magic_cubes.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Gespeichert: {out_path}")


if __name__ == "__main__":
    main()
