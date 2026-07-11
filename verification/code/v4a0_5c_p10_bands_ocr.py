"""
V4a0.5c: p10 Visuelle Crop + Re-OCR der 7 Rechen-Bänder
========================================================

- Crop jeden Rechen-Band als eigenes PNG
- Größere Auflösung + adaptive Threshold + Multi-PSM-OCR
- Ziel: präzise 1. Rechnung (Faktor-Zerlegung) extrahieren
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
CROPS = RESULTS / "v4a0_5c_crops"
CROPS.mkdir(parents=True, exist_ok=True)


def preprocess_band(img):
    """Adaptive Threshold + Denoising für bessere OCR"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    # Adaptive Threshold
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    # Skalierung 2x
    h, w = binary.shape
    scaled = cv2.resize(binary, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
    return scaled


def main():
    img = cv2.imread(str(ORIGINAL))
    if img is None:
        sys.exit(1)

    bands = [
        (1142, 1172, "band15_factor_decomposition"),
        (1295, 1328, "band16_rechnung_2"),
        (1349, 1381, "band17_rechnung_3"),
        (1402, 1434, "band18_rechnung_4"),
        (1455, 1488, "band19_rechnung_5"),
        (1562, 1594, "band20_rechnung_6"),
        (1615, 1648, "band21_rechnung_7"),
    ]

    output = {
        "method": "V4a0.5c = Adaptive-Threshold + 2x-Scale + Multi-PSM-OCR auf p10-Rechen-Bänder",
        "timestamp": "2026-07-11",
        "bands": []
    }

    for y1, y2, name in bands:
        sub = img[y1:y2, :]
        # Speichere Original-Crop
        crop_path = CROPS / f"{name}_raw.png"
        cv2.imwrite(str(crop_path), sub)

        # Preprocess
        processed = preprocess_band(sub)
        proc_path = CROPS / f"{name}_processed.png"
        cv2.imwrite(str(proc_path), processed)

        # Multi-PSM-OCR auf processed
        ocr_results = {}
        for psm in [3, 4, 6, 7, 11, 12]:
            try:
                text = pytesseract.image_to_string(processed, config=f'--psm {psm}').strip()
                ocr_results[f'psm{psm}'] = text
            except Exception as e:
                ocr_results[f'psm{psm}'] = f"ERROR: {e}"

        # Auch mit char_whitelist für Zahlen/Mathe
        for psm in [6, 7]:
            try:
                text = pytesseract.image_to_string(
                    processed,
                    config=f'--psm {psm} -c tessedit_char_whitelist=0123456789.^×÷π- '
                ).strip()
                ocr_results[f'psm{psm}_math'] = text
            except Exception as e:
                ocr_results[f'psm{psm}_math'] = f"ERROR: {e}"

        print(f"\n=== {name} (y={y1}-{y2}) ===")
        for psm, text in ocr_results.items():
            print(f"  {psm}: {text!r}")

        # Suche Faktoren (Zahlen >= 2 Stellen)
        import re
        all_text = " ".join(ocr_results.values())
        numbers = re.findall(r'\d{2,6}', all_text)
        unique_numbers = sorted(set(numbers), key=lambda x: int(x) if x.isdigit() else 0)

        output["bands"].append({
            "name": name,
            "y_start": y1, "y_end": y2,
            "ocr_results": ocr_results,
            "extracted_numbers": unique_numbers,
            "crop_path": str(crop_path.relative_to(ROOT)),
            "processed_path": str(proc_path.relative_to(ROOT))
        })

    out_path = RESULTS / "v4a0_5c_p10_bands_ocr.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Gespeichert: {out_path}")
    print(f"✓ Crops: {CROPS}")


if __name__ == "__main__":
    main()
