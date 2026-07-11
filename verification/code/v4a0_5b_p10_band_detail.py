"""
V4a0.5b: p10 Band 15 Detail-Analyse (Faktor-Zerlegung)
======================================================

Band 15 (y=1142-1172) enthält die 1. Rechnung:
  2^9 × 3^-1 × 5^9 × 197^-1 × 5563^-1 × 41681^-1 = 0.00729735256

- Crop + Zoom + bessere OCR
- Auch: Suche nach der 2./3./4. Rechnung (π-Formeln)
"""

import json
import sys
from pathlib import Path
import numpy as np
import cv2
import pytesseract

ROOT = Path("/run/media/julian/ML4/tengri137")
ORIGINAL = ROOT / "original_sources" / "137" / "P010.png"
RESULTS = ROOT / "verification" / "results" / "snapshots"

def analyze_band(img, y1, y2, name):
    """Detail-Analyse eines Bandes"""
    sub = img[y1:y2, :]
    h, w = sub.shape[:2]

    # Verschiedene OCR-Modi
    results = {}
    for psm in [3, 4, 6, 7, 8, 11, 12, 13]:
        try:
            text = pytesseract.image_to_string(sub, config=f'--psm {psm}').strip()
            results[f'psm{psm}'] = text
        except Exception as e:
            results[f'psm{psm}'] = f"ERROR: {e}"

    # Auch mit char_whitelist für Zahlen/Mathe
    for psm in [6, 7]:
        try:
            text = pytesseract.image_to_string(
                sub,
                config=f'--psm {psm} -c tessedit_char_whitelist=0123456789.^×÷π- '
            ).strip()
            results[f'psm{psm}_math'] = text
        except Exception as e:
            results[f'psm{psm}_math'] = f"ERROR: {e}"

    return results


def main():
    print(f"Lade {ORIGINAL.name}...")
    img = cv2.imread(str(ORIGINAL))
    if img is None:
        sys.exit(1)

    h, w = img.shape[:2]
    print(f"Auflösung: {w}x{h}")

    # Bänder aus V4a0.5
    bands = [
        (1142, 1172, "Band 15 (1. Rechnung: 2^9 × 3^-1 × 5^9 × 197^-1 × 5563^-1 × 41681^-1)"),
        (1295, 1328, "Band 16"),
        (1349, 1381, "Band 17"),
        (1402, 1434, "Band 18"),
        (1455, 1488, "Band 19"),
        (1562, 1594, "Band 20"),
        (1615, 1648, "Band 21"),
    ]

    output = {
        "method": "V4a0.5b = Multi-PSM-OCR auf p10-Bändern (Faktor-Zerlegung Detail)",
        "timestamp": "2026-07-11",
        "bands": []
    }

    for y1, y2, label in bands:
        print(f"\n=== {label} (y={y1}-{y2}) ===")
        results = analyze_band(img, y1, y2, label)
        for psm, text in results.items():
            print(f"  {psm}: {text!r}")

        # Bester Text (längster non-trivial)
        best_psm = max(results.keys(), key=lambda k: len([c for c in results[k] if c.isalnum()]))
        print(f"  → BEST: {best_psm} = {results[best_psm]!r}")

        output["bands"].append({
            "label": label,
            "y_start": y1, "y_end": y2,
            "ocr_results": results,
            "best_psm": best_psm,
            "best_text": results[best_psm]
        })

    # Spezielle Suche: alle Vorkommen von π im Bild
    print("\n=== Spezielle π-Suche (image_to_boxes) ===")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    try:
        # Tesseract kann π manchmal als pi/n erkennen
        for char in ['π', 'pi', 'n']:
            try:
                boxes = pytesseract.image_to_boxes(gray, config=f'--psm 6 -c tessedit_char_whitelist={char}')
                cnt = len(boxes.split('\n')) if boxes.strip() else 0
                print(f"  '{char}': {cnt} Vorkommen")
            except Exception as e:
                print(f"  '{char}': ERROR {e}")
    except Exception as e:
        print(f"  π-Suche fehlgeschlagen: {e}")

    # Auch: Sucht nach '='-Symbolen (für Rechnungs-Ergebnisse)
    print("\n=== '='-Symbol Suche ===")
    for psm in [6, 11]:
        try:
            text = pytesseract.image_to_string(gray, config=f'--psm {psm} -c tessedit_char_whitelist=0123456789.=^×÷π-')
            equals = text.count('=')
            print(f"  psm{psm}: {equals} '=' Symbole")
        except Exception as e:
            print(f"  psm{psm}: ERROR {e}")

    out_path = RESULTS / "v4a0_5b_p10_band_details.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Gespeichert: {out_path}")


if __name__ == "__main__":
    main()
