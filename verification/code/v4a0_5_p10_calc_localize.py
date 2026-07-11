"""
V4a0.5: p10 Rechenaufgaben visuell in PNG lokalisieren
======================================================

Ziel: 100% Verständnis p10 — ALLE Rechenaufgaben visuell finden + extrahieren
- Erst-Principles: NUR Original-PNG p10
- Method: BBox-Detection + Tesseract OCR + visuelle Inspektion

Output:
- v4a0_5_p10_calc_localized.json: Jede Rechnung mit BBox + Text
- v4a0_5_p10_calc_bboxes.png: Visualisierung der BBoxes
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
RESULTS.mkdir(parents=True, exist_ok=True)

def find_calc_regions(img):
    """Suche Regionen mit mathematischer Notation (π, ^, ×, ÷, Ziffern-Cluster)"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    h, w = gray.shape

    # Tesseract mit spezieller Konfig: suche mathematische Symbole
    # PSM 6 = Block of text
    data = pytesseract.image_to_data(
        gray,
        config='--psm 6 -c tessedit_char_whitelist=0123456789.^×÷πe=+',
        output_type=pytesseract.Output.DICT
    )

    math_regions = []
    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        if not text:
            continue
        conf = data['conf'][i]
        if conf < 30:
            continue
        x = data['left'][i]
        y = data['top'][i]
        bw = data['width'][i]
        bh = data['height'][i]
        # Mathematische Symbole oder Ziffern-Cluster
        if any(s in text for s in ['π', '^', '×', '÷']) or (text.replace('.', '').isdigit() and len(text) >= 2):
            math_regions.append({
                "text": text,
                "x": int(x), "y": int(y), "w": int(bw), "h": int(bh),
                "conf": int(conf)
            })

    return math_regions


def find_special_symbols(img):
    """Suche nach π-Symbolen, Potenz-Operatoren, Brüchen"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

    # Template-Matching für π (grob: zwei vertikale Striche + Dach)
    # Da Template-Matching fragil, nutzen wir Hough-Lines + Tesseract Full-Page
    pi_candidates = []

    # Full-Page OCR mit psm 4 (Text-Block)
    full_text = pytesseract.image_to_string(gray, config='--psm 4')

    # Suche π-Position via image_to_boxes
    try:
        boxes = pytesseract.image_to_boxes(gray, config='--psm 6 -c tessedit_char_whitelist=π^×÷e')
        for line in boxes.split('\n'):
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 5 and parts[0] in ['π', '^', '×', '÷']:
                pi_candidates.append({
                    "char": parts[0],
                    "x": int(parts[1]),
                    "y": int(parts[2]),
                    "x2": int(parts[3]),
                    "y2": int(parts[4])
                })
    except Exception as e:
        print(f"image_to_boxes failed: {e}", file=sys.stderr)

    return pi_candidates, full_text


def find_y_density_bands(img, min_band_height=20, gap_threshold=15):
    """Suche y-Bänder mit hoher Pixeldichte (Zeilen mit Rechnungen)"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    # Binär-Maske
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    # Y-Density: Summe pro Zeile
    y_density = np.sum(binary > 0, axis=1)

    # Finde zusammenhängende Bänder
    bands = []
    in_band = False
    band_start = 0
    last_dense_y = 0

    for y, density in enumerate(y_density):
        if density > 20:  # Mindest-Dichte
            if not in_band:
                in_band = True
                band_start = y
            last_dense_y = y
        else:
            if in_band and (y - last_dense_y) > gap_threshold:
                band_height = last_dense_y - band_start + 1
                if band_height >= min_band_height:
                    bands.append({
                        "y_start": int(band_start),
                        "y_end": int(last_dense_y + 1),
                        "height": int(band_height),
                        "max_density": int(y_density[band_start:last_dense_y+1].max())
                    })
                in_band = False

    # Letztes Band
    if in_band:
        band_height = last_dense_y - band_start + 1
        if band_height >= min_band_height:
            bands.append({
                "y_start": int(band_start),
                "y_end": int(last_dense_y + 1),
                "height": int(band_height),
                "max_density": int(y_density[band_start:last_dense_y+1].max())
            })

    return bands, y_density.tolist()


def main():
    print(f"Lade {ORIGINAL.name}...")
    img = cv2.imread(str(ORIGINAL))
    if img is None:
        print(f"FEHLER: Bild nicht gefunden: {ORIGINAL}")
        sys.exit(1)
    print(f"Bild-Form: {img.shape}")

    h, w = img.shape[:2]
    print(f"Auflösung: {w}x{h}")

    # 1. Mathematische Regionen via Tesseract
    print("\n--- Suche mathematische Regionen ---")
    math_regions = find_calc_regions(img)
    print(f"Gefunden: {len(math_regions)} math. Regionen")
    for r in math_regions[:20]:
        print(f"  ({r['x']},{r['y']}) [{r['w']}x{r['h']}] '{r['text']}' conf={r['conf']}")

    # 2. π-Symbole + Full-OCR
    print("\n--- Suche π-Symbole + Full-OCR ---")
    pi_candidates, full_text = find_special_symbols(img)
    print(f"π-Kandidaten: {len(pi_candidates)}")
    for c in pi_candidates:
        print(f"  '{c['char']}' bei ({c['x']},{c['y']})")
    print(f"\nFull-Page-Text (erste 500 Zeichen):\n{full_text[:500]}")

    # 3. Y-Density Bänder
    print("\n--- Y-Density-Bänder (Textzeilen) ---")
    bands, y_density = find_y_density_bands(img, min_band_height=20)
    print(f"Anzahl Bänder: {len(bands)}")
    for i, b in enumerate(bands):
        print(f"  Band {i+1}: y={b['y_start']}-{b['y_end']} (h={b['height']}, max_density={b['max_density']})")

    # 4. Pro Band: OCR + Subregion
    print("\n--- Pro Band: OCR-Subregion ---")
    band_ocrs = []
    for i, b in enumerate(bands):
        y1, y2 = b['y_start'], b['y_end']
        sub = img[y1:y2, :]
        # OCR pro Band
        sub_text = pytesseract.image_to_string(sub, config='--psm 7').strip()
        if not sub_text:
            sub_text = pytesseract.image_to_string(sub, config='--psm 6').strip()
        # Suche π + Zahlen im Sub-Text
        has_pi = 'π' in sub_text or 'n' in sub_text  # Tesseract erkennt π oft als 'n'
        has_numbers = any(c.isdigit() for c in sub_text)
        has_caret = '^' in sub_text
        is_calc = has_numbers and (has_pi or has_caret or '=' in sub_text or 'x' in sub_text.lower())

        print(f"  Band {i+1} y={y1}-{y2} calc={is_calc}: {sub_text[:80]!r}")
        band_ocrs.append({
            "band_idx": i+1,
            "y_start": y1,
            "y_end": y2,
            "height": b['height'],
            "ocr_text": sub_text,
            "has_pi": has_pi,
            "has_numbers": has_numbers,
            "is_calc": is_calc
        })

    # 5. Calc-Regionen hervorheben + speichern
    output = {
        "method": "V4a0.5 = Tesseract (psm 4, 6, 7) + Y-Density + visuelle Lokalisation auf Original-PNG p10 (P010.png)",
        "timestamp": "2026-07-11",
        "image": {
            "path": str(ORIGINAL.relative_to(ROOT)),
            "width": w,
            "height": h
        },
        "math_regions": math_regions,
        "pi_symbol_candidates": pi_candidates,
        "y_density_bands": bands,
        "band_ocrs": band_ocrs,
        "calc_bands_only": [b for b in band_ocrs if b['is_calc']],
        "full_text_ocr": full_text,
        "faktum": "V4a0.5 FAKTUM: p10 enthält X Rechen-Bänder mit mathematischer Notation (siehe calc_bands_only). Visualisierung in v4a0_5_p10_calc_bboxes.png.",
        "offen_fuer_v4a0_5b": "Welche Rechnung genau in welchem Band steht (numerische Verifikation) — Folge-Aufgabe"
    }

    out_path = RESULTS / "v4a0_5_p10_calc_localized.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Gespeichert: {out_path}")

    # 6. Visualisierung
    vis = img.copy()
    # Math-Regionen: grün
    for r in math_regions:
        cv2.rectangle(vis, (r['x'], r['y']), (r['x']+r['w'], r['y']+r['h']), (0, 255, 0), 2)
    # Bänder: blau
    for b in bands:
        cv2.rectangle(vis, (0, b['y_start']), (w, b['y_end']), (255, 0, 0), 1)
    # Calc-Bänder: rot
    for b in band_ocrs:
        if b['is_calc']:
            cv2.rectangle(vis, (0, b['y_start']), (w, b['y_end']), (0, 0, 255), 3)
            cv2.putText(vis, f"CALC b{b['band_idx']}", (10, b['y_start']+30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # π-Symbole: gelb
    for c in pi_candidates:
        cv2.circle(vis, (c['x'], c['y']), 10, (0, 255, 255), -1)

    vis_path = RESULTS / "v4a0_5_p10_calc_bboxes.png"
    cv2.imwrite(str(vis_path), vis)
    print(f"✓ Visualisierung: {vis_path}")


if __name__ == "__main__":
    main()
