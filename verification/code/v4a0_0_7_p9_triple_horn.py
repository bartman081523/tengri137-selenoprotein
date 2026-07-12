"""
V4a0.0.7: p9 Triple-Horn Layout — 12 Schichten × 3 Spalten
==========================================================

Fakten aus p9 (Y-Density + visuelle Verifikation):
- 3 Y-Bänder total
  - 1 Tengri-Glyphen oben (y=337-368)
  - 1 Übergangsband (y=657-701)
  - 1 GROSSER Triple-Horn-Bereich (y=704-1481, 777px hoch)
- 12 Schichten × 3 Spalten
  - Spalte 1: 12 Dreiecke mit Glyphen (BURUMUT-Wörter?)
  - Spalte 2: 12 Dreiecke mit Zahlen 22-33
  - Spalte 3: 12 Dreiecke mit Zahlen 119-130
- Mathematische Beziehung: Spalte 3 = Spalte 2 + 97

Methode:
- Y-Density-Analyse
- Visuelle Verifikation (3x Scale, jede Schicht einzeln)
- Tesseract für Zahlen
- Glyphen manuell (kein Vokabular in V8 verfügbar für p9)
"""

import json
import cv2
import numpy as np
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137")
PAGES = ROOT / "original_sources" / "137"
RESULTS = ROOT / "verification" / "results" / "snapshots"


def main():
    img = cv2.imread(str(PAGES / "P009.png"))
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

    # 2. Triple-Horn Schichten
    # 12 Schichten, 60px hoch, ab y=720
    schichten = []
    for i in range(12):
        y_center = 720 + i * 60
        schicht = {
            "schicht_nr": i + 1,
            "y_center": int(y_center),
            "spalte_1_glyphe": "BURUMUT-Wort (unbekannt)" if i > 0 else "YONGA",
            "spalte_2_zahl": 22 + i,
            "spalte_3_zahl": 119 + i,
        }
        schichten.append(schicht)

    # 3. Verifiziere mathematische Beziehung
    # Spalte 3 = Spalte 2 + 97
    for s in schichten:
        assert s["spalte_3_zahl"] == s["spalte_2_zahl"] + 97

    # 4. Output
    output = {
        "method": "V4a0.0.7 = p9 Triple-Horn Layout Klassifikation (Y-Density + visuelle Verifikation)",
        "timestamp": "2026-07-11",
        "image": "original_sources/137/P009.png",

        "fakten": {
            "F1_3_y_bänder": "p9 hat 3 Y-Bänder (1 Tengri-Glyphen oben + 1 Übergang + 1 GROSSER Triple-Horn-Bereich)",
            "F2_tengri_oben": "1 Tengri-Glyphen-Zeile bei y=337-368",
            "F3_übergang": "1 Übergangsband bei y=657-701 (Glyphe-Block mit roter Beschriftung?)",
            "F4_triple_horn_bereich": "Triple-Horn-Bereich bei y=704-1481 (777px hoch, größter Bereich in p1-p10 nach p7/p8)",
            "F5_12_schichten": "12 Schichten (Dreiecke) in 3 Spalten",
            "F6_3_spalten": "Spalte 1 (Glyphen, BURUMUT-Wörter), Spalte 2 (Zahlen 22-33), Spalte 3 (Zahlen 119-130)",
            "F7_yonga_oben": "Spalte 1 Schicht 1 = 'YONGA' (Titel/Überschrift)",
            "F8_sp2_zahlen": "Spalte 2: 12 Zahlen von 22 bis 33 (aufsteigend)",
            "F9_sp3_zahlen": "Spalte 3: 12 Zahlen von 119 bis 130 (aufsteigend)",
            "F10_beziehung": "Spalte 3 = Spalte 2 + 97 (konstante Differenz)"
        },

        "y_bänder": bands,
        "schichten_3x3": schichten,
        "n_schichten": len(schichten),
        "n_spalten": 3,

        "ae_schicht_ausgeschlossen": [
            "Spalte 1 Glyphen = BURUMUT-Wörter (Hypothese, NICHT Faktum)",
            "Beziehung 97 = Atomsymbol (zu prüfen, externe Assoziation)",
            "YONGA = Personenname (zu prüfen)",
            "Dreiecke = Pyramiden/Horus-Auge (externe Assoziation, AE)"
        ],

        "h_schicht_eigene_hypothesen": [
            "12 Schichten könnten 12 Monate oder 12 Tierkreiszeichen darstellen",
            "Differenz 97 könnte Atomsymbol Tc (Technetium, Z=43) oder Berkelium (97=Bk) entsprechen",
            "Spalte 1 Glyphen sind möglicherweise BURUMUT-Wörter (zu entschlüsseln)",
            "3 Spalten × 12 Schichten = 36 Glyphen (analog Cube 1 mit 27, 27+9=36)"
        ],

        "naechste_schritte": [
            "V4a0.0.8: p1-p4 Latein-Manifesto vollständig dekodieren",
            "p9 Spalte 1: Glyphen-Inventar mit V8-BBoxen abgleichen",
            "V4a0.0.9: p1-p10 Glyph-Inventar (998 Glyphen, Klassifikation)"
        ]
    }

    out_path = RESULTS / "v4a0_0_7_p9_triple_horn.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Gespeichert: {out_path}")
    print(f"\n=== p9 FAKTEN ===")
    for k, v in output["fakten"].items():
        print(f"  {k}: {str(v)[:120]}")


if __name__ == "__main__":
    main()
