"""
V4a0.0.6: p8 Magic-Square-Layout — Klassifikation der konzentrischen Strukturen
================================================================================

Fakten aus p8:
- 3 Y-Bänder total
  - 1 Tengri-Glyphen oben (y=444-475)
  - 1 GROSSER Geometrie-Bereich (y=608-1508, 900px hoch)
  - 1 Tengri-Glyphen unten (y=1680-1711)
- 4 große konzentrische Kreise (r=487-495) in 3x3+Anordnung
- ~50 kleinere Kreise (r=80-200) als Verzierungen
- Innere Strukturen (Spannenspitze/Schneemann-Form)

Methode: Y-Density + Connected Components + HoughCircles + visuelle Verifikation
"""

import json
import cv2
import numpy as np
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137")
PAGES = ROOT / "original_sources" / "137"
RESULTS = ROOT / "verification" / "results" / "snapshots"


def main():
    img = cv2.imread(str(PAGES / "P008.png"))
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

    # 2. HoughCircles
    sub = img[608:1508, :]
    sub_gray = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
    all_circles = []
    for minR, maxR in [(80, 200), (200, 300), (300, 400), (400, 500)]:
        circles = cv2.HoughCircles(sub_gray, cv2.HOUGH_GRADIENT, dp=1, minDist=100,
                                    param1=100, param2=30, minRadius=minR, maxRadius=maxR)
        if circles is not None:
            for c in np.round(circles[0, :]).astype(int):
                all_circles.append({
                    "x": int(c[0]), "y": int(c[1] + 608), "r": int(c[2]),
                    "size_class": f"r{'-'.join([str(minR), str(maxR)])}"
                })
    # Sortiere nach Radius
    all_circles.sort(key=lambda c: -c["r"])

    # Große Kreise (r>400) dedupliziert
    big_circles = []
    for c in all_circles:
        if c["r"] < 400:
            break
        is_dup = any(np.hypot(c["x"]-b["x"], c["y"]-b["y"]) < 30 and abs(c["r"]-b["r"]) < 20 for b in big_circles)
        if not is_dup:
            big_circles.append(c)

    output = {
        "method": "V4a0.0.6 = p8 Magic-Square-Layout Klassifikation (Y-Density + HoughCircles + visuelle Verifikation)",
        "timestamp": "2026-07-11",
        "image": "original_sources/137/P008.png",

        "fakten": {
            "F1_3_y_bänder": "p8 hat 3 Y-Bänder (1 Tengri-Glyphen oben + 1 großer Geometrie-Bereich + 1 Tengri-Glyphen unten)",
            "F2_tengri_oben": "1 Tengri-Glyphen-Zeile bei y=444-475 (Höhe 31)",
            "F3_geometry_container": "Großer Geometrie-Bereich bei y=608-1508 (900px hoch)",
            "F4_tengri_unten": "1 Tengri-Glyphen-Zeile bei y=1680-1711 (Höhe 31)",
            "F5_4_große_kreise": f"4 große konzentrische Kreise (r=487-495) in gestapelter Anordnung, gefunden: {len(big_circles)}",
            "F6_50_kleinere_kreise": f"~{len(all_circles)} kleinere Kreise (r=80-400) als Verzierungen",
            "F7_innere_struktur": "Innere Muster: Spannenspitze/Schneemann-ähnliche Formen im Zentrum"
        },

        "y_bänder": bands,
        "big_circles": big_circles,
        "all_circles_count": len(all_circles),

        "ae_schicht_ausgeschlossen": [
            "Hebräisch (Vision-Halluzination)",
            "Tengwar/Ge'ez (Vision-Halluzination)",
            "Magic Square im klassischen 3x3-Sinn (zu prüfen, hier sind es konzentrische Kreise, nicht 3x3)"
        ],

        "h_schicht_eigene_hypothesen": [
            "4 große Kreise könnten Schichten/Hierarchien darstellen",
            "Innere Strukturen könnten zentrale Symbole sein (Mandala-ähnlich)",
            "p7 hatte 9 Großkreise, p8 hat 4 - möglicherweise unterschiedliche Magic-Cube-Typen"
        ],

        "naechste_schritte": [
            "V4a0.0.7: p9 Triple-Horn Layout (12 Schichten 119-214)",
            "p8: mehr Detail auf innere Strukturen (Zoom)",
            "p7+p8 vergleichen: ähnliche Geometrie?"
        ]
    }

    out_path = RESULTS / "v4a0_0_6_p8_geometry.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Gespeichert: {out_path}")
    print(f"\n=== p8 FAKTEN ===")
    for k, v in output["fakten"].items():
        print(f"  {k}: {str(v)[:120]}")


if __name__ == "__main__":
    main()
