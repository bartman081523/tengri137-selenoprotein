"""
v04_latin_ocr.py — Phase 3: Latein-OCR via Tesseract.

Methode (eigene, unabhängig von phase4_ocr.py):
  1. Tesseract auf ganzes PNG (pytesseract.image_to_string mit psm=3)
  2. Filter: Wörter mit ≥3 lateinischen Buchstaben werden behalten
  3. KEIN Tesseract für Tengri-Glyphen (gemäß V4-Methoden-Referenz: PIVOT)
  4. KEINE externes Modell (WIKIA, Schmeh) als Quelle

Methoden-Referenz (NICHT als Quelle):
  - phase4_ocr.py: pytesseract mit config='--psm 3 -l eng'
  - V4 PIVOT: Tesseract NICHT für Glyphen, nur für Latein (wir machen das genauso)

Output:
  - verification/data/latin/pNN.json: {words: [{text, bbox, confidence}], n_words}
  - verification/data/latin_summary.json
"""
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

import cv2
import numpy as np
from PIL import Image

cv2.setNumThreads(1)
np.random.seed(137)

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

REPO = Path('/run/media/julian/ML4/tengri137')
ORIG_1 = REPO / 'original_sources/137'
ORIG_2 = REPO / 'original_sources/p011_p023_originals'
DATA = REPO / 'verification' / 'data' / 'latin'
LOGS = REPO / 'verification' / 'logs'
DATA.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOGS / 'v04.log', mode='w'), logging.StreamHandler()],
)
log = logging.getLogger(__name__)


def orig_path(n: int) -> Path:
    p = ORIG_1 / f'P{n:03d}.png'
    return p if p.exists() else ORIG_2 / f'P{n:03d}.png'


def ocr_page(n: int) -> dict:
    if not TESSERACT_AVAILABLE:
        log.warning('pytesseract nicht verfügbar — fallback: nur Heuristik')
        return {'words': [], 'n_words': 0, 'method': 'unavailable'}

    p = orig_path(n)
    im = Image.open(p).convert('L')
    arr = np.array(im)

    # Binarisierung
    _, th = cv2.threshold(arr, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Tesseract: data-Mode (mit Positionen)
    try:
        data = pytesseract.image_to_data(
            th,
            config='--psm 3 -l eng',
            output_type=pytesseract.Output.DICT,
        )
    except Exception as e:
        log.error(f'  p{n:02d}: Tesseract-Fehler: {e}')
        return {'words': [], 'n_words': 0, 'method': 'error'}

    words = []
    n_boxes = len(data['text'])
    for i in range(n_boxes):
        text = data['text'][i].strip()
        if not text:
            continue
        # Filter: muss ≥3 lateinische Buchstaben enthalten
        alpha = sum(1 for c in text if c.isalpha() and ord(c) < 128)
        if alpha < 3:
            continue
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        conf = data['conf'][i]
        words.append({
            'text': text,
            'bbox': [int(x), int(y), int(w), int(h)],
            'confidence': int(conf) if isinstance(conf, (int, str)) else 0,
        })

    out = {
        'page_id': f'p{n:02d}',
        'method': 'tesseract_psm3_eng',
        'n_words': len(words),
        'n_boxes_total': n_boxes,
        'words': words,
    }
    (DATA / f'p{n:02d}.json').write_text(json.dumps(out, indent=2))
    return out


def main():
    log.info('=' * 60)
    log.info('PHASE 3: Latein-OCR via Tesseract')
    log.info(f'Tesseract verfügbar: {TESSERACT_AVAILABLE}')
    log.info('=' * 60)

    if not TESSERACT_AVAILABLE:
        log.error('pytesseract NICHT installiert — bitte `pip install pytesseract` ausführen')
        log.error('UND `apt install tesseract-ocr` (für die Binary)')
        return

    overall = {}
    for n in range(1, 24):
        r = ocr_page(n)
        overall[f'p{n:02d}'] = {
            'n_words': r.get('n_words', 0),
            'n_boxes_total': r.get('n_boxes_total', 0),
        }
        log.info(
            f"  p{n:02d}: words={r.get('n_words',0):4d}, "
            f"boxes_total={r.get('n_boxes_total',0):4d}"
        )

    (DATA.parent / 'latin_summary.json').write_text(json.dumps(overall, indent=2))
    log.info('')
    total_words = sum(s['n_words'] for s in overall.values())
    log.info(f'✓ Latein-OCR: {total_words} lateinische Wörter total extrahiert')


if __name__ == '__main__':
    main()
