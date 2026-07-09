"""
v10_latein_text.py — Phase 9: Latein-Text-Komposition.

Methode (eigene, unabhängig von phase4_ocr.py):
  1. Pro Seite: lade latein-Wörter aus v04 (Tesseract-PSM-3)
  2. Sortiere nach Y-Position, gruppiere zu Zeilen (gleiche Y-Höhe ±20px)
  3. Pro Zeile: sortiere nach X-Position → Wort-Reihenfolge
  4. Region-Erkennung: oben/Mitte/unten Drittel

Output:
  - verification/data/text/pNN.json: {lines: [{line_id, line_type, words[]}], n_lines, n_words}
  - verification/data/text_summary.json
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict

import cv2
import numpy as np
from PIL import Image

cv2.setNumThreads(1)
np.random.seed(137)

REPO = Path('/run/media/julian/ML4/tengri137')
DATA = REPO / 'verification' / 'data' / 'text'
LATIN_DIR = REPO / 'verification' / 'data' / 'latin'
LOGS = REPO / 'verification' / 'logs'
DATA.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOGS / 'v10.log', mode='w'), logging.StreamHandler()],
)
log = logging.getLogger(__name__)


def group_words_to_lines(words: list[dict], y_tol: int = 20) -> list[list[dict]]:
    """Gruppiere Wörter nach Y-Position (Toleranz y_tol Pixel)."""
    if not words:
        return []
    sorted_w = sorted(words, key=lambda w: w.get('bbox', [0, 0, 0, 0])[1])
    lines = []
    current = [sorted_w[0]]
    for w in sorted_w[1:]:
        y_curr = current[0].get('bbox', [0, 0, 0, 0])[1]
        y_w = w.get('bbox', [0, 0, 0, 0])[1]
        if abs(y_w - y_curr) <= y_tol:
            current.append(w)
        else:
            current.sort(key=lambda x: x.get('bbox', [0, 0, 0, 0])[0])
            lines.append(current)
            current = [w]
    current.sort(key=lambda x: x.get('bbox', [0, 0, 0, 0])[0])
    lines.append(current)
    return lines


def classify_line(y_top: int, y_bot: int, page_h: int = 1998) -> str:
    """Klassifiziere Zeile nach Y-Position (top/mid/bot)."""
    center = (y_top + y_bot) / 2
    if center < page_h / 3:
        return 'header'
    if center > 2 * page_h / 3:
        return 'footer'
    return 'body'


def compose_page(n: int) -> dict:
    """Komponiere Latein-Text für Seite n."""
    latin_file = LATIN_DIR / f'p{n:02d}.json'
    if not latin_file.exists():
        return {'n_lines': 0, 'n_words': 0, 'lines': []}
    page = json.load(open(latin_file))
    words = page.get('words', [])

    # Falls v04 nicht die "words"-Struktur hat, alternativ parsen
    if not words and 'boxes' in page:
        words = [{'text': b.get('text', ''), 'bbox': b.get('bbox', [0, 0, 0, 0]), 'confidence': b.get('confidence', 0)}
                 for b in page.get('boxes', []) if b.get('text')]

    lines_raw = group_words_to_lines(words, y_tol=20)
    out_lines = []
    for li, line in enumerate(lines_raw):
        y_tops = [w.get('bbox', [0, 0, 0, 0])[1] for w in line]
        y_bots = [w.get('bbox', [0, 0, 0, 0])[1] + w.get('bbox', [0, 0, 0, 0])[3] for w in line]
        y_top, y_bot = min(y_tops), max(y_bots)
        text = ' '.join(w.get('text', '') for w in line).strip()
        out_lines.append({
            'line_id': f'L{li:02d}',
            'y_top': y_top,
            'y_bot': y_bot,
            'line_type': classify_line(y_top, y_bot),
            'n_words': len(line),
            'text': text,
        })
    return {
        'n_lines': len(out_lines),
        'n_words': sum(l['n_words'] for l in out_lines),
        'lines': out_lines,
    }


def main():
    log.info('=' * 60)
    log.info('PHASE 9: Latein-Text-Komposition')
    log.info('=' * 60)

    overall = {}
    total_lines = 0
    total_words = 0
    for n in range(1, 24):
        comp = compose_page(n)
        (DATA / f'p{n:02d}.json').write_text(json.dumps(comp, indent=2))
        overall[f'p{n:02d}'] = {'n_lines': comp['n_lines'], 'n_words': comp['n_words']}
        total_lines += comp['n_lines']
        total_words += comp['n_words']
        if comp['n_lines'] > 0:
            sample = comp['lines'][0]['text'][:60]
            log.info(f"  p{n:02d}: {comp['n_lines']:3d} Zeilen, {comp['n_words']:3d} Wörter, sample='{sample}'")

    (DATA.parent / 'text_summary.json').write_text(json.dumps(overall, indent=2))
    log.info('')
    log.info(f'✓ Latein-Text-Komposition: {total_lines} Zeilen, {total_words} Wörter total')


if __name__ == '__main__':
    main()
