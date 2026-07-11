"""
V4a0.0.5: p7 Geometrie — Klassifikation der geometrischen Strukturen
====================================================================

Fakten aus p7 (Y-Density-Analyse + OpenCV CC + HoughCircles):
- 6 Y-Bänder total
  - 5 schmale Tengri-Glyphen-Bänder oben (y=326, 376, 476, 628, 678)
  - 1 großer Geometrie-Bereich unten (y=882-1766, 884px hoch)
- 1 großer Geometrie-Container CC#270 (195, 855) 942×938
- 9 große Hauptkreise (r~180) in 3x3+Anordnung
- ~30 kleinere Kreise (r=15-50) als Verzierungen
- Latein-Text rechts: "YONGA", "ZÄHLUNG DER GLYPHEN", "SEQUENZ EINS/ZWEI/DREI", "ALGORITHMUS"
- Strichmännchen-Symbole links unten

Methode:
- Y-Density-Analyse (np.sum(binary, axis=1))
- Connected Components (OpenCV)
- HoughCircles (param2=30, r_min=80)
- Visuelle Verifikation (3x Scale)
- Manuelle Latein-Text-Lesung (Tesseract scheitert)
"""

import json
import cv2
import numpy as np
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137")
PAGES = ROOT / "original_sources" / "137"
RESULTS = ROOT / "verification" / "results" / "snapshots"


def main():
    img = cv2.imread(str(PAGES / "P007.png"))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # 1. Y-Bänder
    y_density = np.sum(binary > 0, axis=1)
    in_band = False
    start = 0
    bands = []
    for i, d in enumerate(y_density):
        if d > 10 and not in_band:
            in_band = True
            start = i
        elif d <= 10 and in_band:
            in_band = False
            if 30 < i - start:
                bands.append({"y_start": int(start), "y_end": int(i), "height": int(i - start)})

    # 2. CC#270 (großer Geometrie-Container)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
    sorted_stats = sorted([(i, s) for i, s in enumerate(stats) if i > 0], key=lambda x: -x[1][4])
    big_container = None
    for label, s in sorted_stats:
        x, y, w, h, area = s
        if 800 < w < 1100 and 800 < h < 1100 and area > 30000:
            big_container = {"label": int(label), "x": int(x), "y": int(y), "w": int(w), "h": int(h), "area": int(area)}
            break

    # 3. HoughCircles für große Kreise
    sub = img[855:1793, 195:1137]
    sub_gray = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(sub_gray, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                                param1=100, param2=30, minRadius=80, maxRadius=200)
    if circles is not None:
        circles = np.round(circles[0, :]).astype(int)
        big_circles = [{"x_abs": int(x+195), "y_abs": int(y+855), "r": int(r)} for x, y, r in circles if r > 100]
        big_circles.sort(key=lambda c: (c["y_abs"], c["x_abs"]))
    else:
        big_circles = []

    # 4. Latein-Text (rechts, manuell gelesen)
    latin_text = [
        "YONGA",  # Möglicherweise Projektname
        "ZÄHLUNG DER GLYPHEN",
        "SEQUENZ EINS  1",
        "SEQUENZ ZWEI  1",
        "SEQUENZ DREI  1",
        "ALGORITHMUS",
        "ZÄHLUNG DER GLYPHEN"
    ]

    # 5. Output
    output = {
        "method": "V4a0.0.5 = p7 Geometrie Klassifikation (Y-Density + CC + HoughCircles + visuelle Verifikation)",
        "timestamp": "2026-07-11",
        "image": "original_sources/137/P007.png",

        "fakten": {
            "F1_6_y_bänder": "p7 hat 6 Y-Bänder (5 schmale Tengri-Glyphen + 1 großer Geometrie-Bereich)",
            "F2_tengri_glyphen_bänder": [
                {"y": 326, "höhe": 31},
                {"y": 376, "höhe": 31},
                {"y": 476, "höhe": 32},  # Hier ist auch kleine Geometrie ("Stuhl")
                {"y": 628, "höhe": 31},
                {"y": 678, "höhe": 31}
            ],
            "F3_geometry_container": "1 großer Geometrie-Container CC#270 bei (195, 855) 942×938, area=36002",
            "F4_9_große_hauptkreise": "9 große Hauptkreise (r=180-183) in 3×3-Anordnung + 1 oben + 1 unten",
            "F5_kleinere_kreise": "~30 kleinere Verzierungs-Kreise (r=15-50)",
            "F6_latein_text": "Latein-Text rechts: YONGA, ZÄHLUNG DER GLYPHEN, SEQUENZ 1/2/3, ALGORITHMUS",
            "F7_strichmännchen": "Strichmännchen-ähnliche Symbole links unten (Tengri-Glyphen)",
            "F8_stuhl_form": "Kleine 'Stuhl'-Form bei y=476-508 (Glyphe in 5. Tengri-Reihe)"
        },

        "y_bänder": bands,
        "geometry_container": big_container,
        "big_circles": big_circles,
        "n_big_circles": len(big_circles),
        "latin_text_visible": latin_text,

        "ae_schicht_ausgeschlossen": [
            "Hebräisch (Vision-Halluzination)",
            "Tengwar/Ge'ez (Vision-Halluzination)",
            "YONGA könnte ein Personenname sein (zu prüfen, NICHT Faktum)"
        ],

        "h_schicht_eigene_hypothesen": [
            "9 Hauptkreise könnten 3 Ebenen × 3 Stufen darstellen (analog Cube 1)",
            "Latein 'SEQUENZ 1/2/3' deutet auf 3-stufige Algorithmen hin",
            "Kreise + Verbindungslinien könnten Zustandsdiagramm sein (zu prüfen)"
        ],

        "naechste_schritte": [
            "V4a0.0.6: p8 Magic-Square-Layout",
            "V4a0.0.7: p9 Triple-Horn Layout",
            "p7: mehr über Latein-Text-Algorithmus (Zoom auf Beschriftung)"
        ]
    }

    out_path = RESULTS / "v4a0_0_5_p7_geometrie.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Gespeichert: {out_path}")
    print(f"\n=== p7 FAKTEN ===")
    for k, v in output["fakten"].items():
        print(f"  {k}: {str(v)[:120]}")
    print(f"\nGroßkreise gefunden: {len(big_circles)}")


if __name__ == "__main__":
    main()
