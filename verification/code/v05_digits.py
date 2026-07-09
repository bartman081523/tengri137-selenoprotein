"""
v05_digits.py — Phase 4: Ziffern-Detection.

Methode (eigene, unabhängig von phase11c_mathe_ziffern.py):
  1. Suche p17-Header-Region: wo sind die "math"-artigen Glyphen in Reihen
  2. Tesseract mit psm=8 (single word) auf kleinen BBox-Crops
  3. Filter: erkannter Text = 0-9 oder Kombination
  4. Für alle Seiten: durchsuche lateinische BBox-Regionen nach isolierten Ziffern

Output:
  - verification/data/digits/pNN.json: [{text, bbox, source}]
  - verification/data/digits_summary.json
"""
import json
import logging
import re
from pathlib import Path
from datetime import datetime

import cv2
import numpy as np
from PIL import Image
import pytesseract

cv2.setNumThreads(1)
np.random.seed(137)

REPO = Path('/run/media/julian/ML4/tengri137')
ORIG_1 = REPO / 'original_sources/137'
ORIG_2 = REPO / 'original_sources/p011_p023_originals'
DATA = REPO / 'verification' / 'data' / 'digits'
BBOX_DIR = REPO / 'verification' / 'data' / 'bboxes'
LOGS = REPO / 'verification' / 'logs'
DATA.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOGS / 'v05.log', mode='w'), logging.StreamHandler()],
)
log = logging.getLogger(__name__)


def orig_path(n: int) -> Path:
    p = ORIG_1 / f'P{n:03d}.png'
    return p if p.exists() else ORIG_2 / f'P{n:03d}.png'


DIGIT_RE = re.compile(r'^[\d\.\,\-/]+$')  # nur Ziffern, Dezimaltrennzeichen


def detect_digits_in_page(n: int) -> list[dict]:
    """Lade Glyph-Liste (Phase 2), filtere auf 'digit'-Klasse, prüfe Tesseract-Output."""
    glyph_file = REPO / 'verification' / 'data' / 'glyphs' / f'p{n:02d}.json'
    if not glyph_file.exists():
        return []
    glyphs = json.load(open(glyph_file))

    p = orig_path(n)
    im = Image.open(p).convert('L')
    arr = np.array(im)

    digits = []
    for g in glyphs:
        if g.get('glyph_class') != 'digit':
            continue
        x, y, w, h = g['bbox']
        # Padding
        pad = 4
        x0 = max(0, x - pad)
        y0 = max(0, y - pad)
        x1 = min(arr.shape[1], x + w + pad)
        y1 = min(arr.shape[0], y + h + pad)
        crop = arr[y0:y1, x0:x1]
        if crop.size == 0:
            continue
        # Threshold
        _, th = cv2.threshold(crop, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # Tesseract
        try:
            txt = pytesseract.image_to_string(
                th, config='--psm 10 -l eng -c tessedit_char_whitelist=0123456789.,'
            ).strip()
        except Exception:
            txt = ''
        if DIGIT_RE.match(txt) and len(txt) > 0:
            digits.append({
                'text': txt,
                'bbox': g['bbox'],
                'region_id': g['region_id'],
                'glyph_class': 'digit',
                'tesseract_text': txt,
            })
    return digits


def main():
    log.info('=' * 60)
    log.info('PHASE 4: Ziffern-Detection (Tesseract auf digit-BBox-Crops)')
    log.info('=' * 60)

    overall = {}
    for n in range(1, 24):
        digits = detect_digits_in_page(n)
        (DATA / f'p{n:02d}.json').write_text(json.dumps(digits, indent=2))
        overall[f'p{n:02d}'] = {
            'n_digits': len(digits),
            'sample_texts': [d['text'] for d in digits[:5]],
        }
        log.info(f"  p{n:02d}: n_digits={len(digits):3d}, sample={overall[f'p{n:02d}']['sample_texts']}")

    (DATA.parent / 'digits_summary.json').write_text(json.dumps(overall, indent=2))
    total = sum(s['n_digits'] for s in overall.values())
    log.info('')
    log.info(f'✓ Ziffern-Detection: {total} Ziffern total')


if __name__ == '__main__':
    main()
