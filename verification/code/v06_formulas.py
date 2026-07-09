"""
v06_formulas.py — Phase 5: Formel-Detection.

Methode (eigene, unabhängig von phase12_periodic_decode.py / phase13_search_fractions.py):
  1. 4 Formel-Klassen:
     a) math_times (×) — Suche in Glyph-Liste nach Symbolen mit Aspect ~1, 2 Striche diagonal
     b) math_pi (π) — Symbol mit Bogen oben + 2 Stege
     c) math_exponentiation (^) — Caret-Symbol
     d) fraction — 3 vertikal-gestapelte Komponenten (Zähler, Bruchstrich, Nenner)
  2. KEIN LLM, KEINE Schmeh-Notes.
  3. Heuristik: bbox-Form + Aspekt-Verhältnis + Position (math_times ist SOLO-Operator laut
     UEBERSICHT.md, wir prüfen das empirisch)

Output:
  - verification/data/formulas/pNN.json: [{class, bbox, ascii_mean or None}]
  - verification/data/formulas_summary.json
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from collections import Counter

import cv2
import numpy as np
from PIL import Image

cv2.setNumThreads(1)
np.random.seed(137)

REPO = Path('/run/media/julian/ML4/tengri137')
DATA = REPO / 'verification' / 'data' / 'formulas'
GLYPH_DIR = REPO / 'verification' / 'data' / 'glyphs'
LOGS = REPO / 'verification' / 'logs'
DATA.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOGS / 'v06.log', mode='w'), logging.StreamHandler()],
)
log = logging.getLogger(__name__)

# Formel-Operator ASCII-Mapping (deterministisch, nicht aus V10.4)
FORMULA_SYMBOLS = {
    'math_times': '×',
    'math_pi': 'π',
    'math_exponentiation': '^',
    'math_divide': '/',
    'math_plus': '+',
    'math_minus': '-',
    'math_equals': '=',
}


def classify_formula(crop: np.ndarray, bbox: list) -> str | None:
    """Heuristik: schaue Crop-Pixel an, versuche Symbol zu identifizieren."""
    if crop.size == 0:
        return None
    x, y, w, h = bbox
    aspect = h / w if w > 0 else 1.0

    # math_times: Aspekt ~1, 2 diagonale Striche
    # Heuristik: Anzahl dunkler Pixel im Hauptdiagonal-Band
    if 0.7 < aspect < 1.3 and 8 < w < 40 and 8 < h < 40:
        # Zähle dunkle Pixel in 2 diagonalen Bändern
        h_, w_ = crop.shape
        diag1 = 0
        diag2 = 0
        for r in range(min(h_, w_)):
            if crop[r, r] < 128:
                diag1 += 1
            if crop[r, w_ - 1 - r] < 128:
                diag2 += 1
        if diag1 > 3 and diag2 > 3:
            return 'math_times'

    # math_pi: Aspekt ~1.2, oben Bogen
    if 1.0 < aspect < 1.5 and 10 < w < 50:
        # Top 30% should have a curve (mehr Pixel oben)
        top = crop[:crop.shape[0]//3, :]
        mid = crop[2*crop.shape[0]//3:, :]
        if (top < 128).sum() > (mid < 128).sum() * 0.7:
            return 'math_pi'

    # math_exponentiation: Aspekt < 1, caret-Form
    if aspect < 0.7 and 8 < w < 40 and 8 < h < 30:
        return 'math_exponentiation'

    return None


def detect_formulas_in_page(n: int) -> list[dict]:
    glyph_file = GLYPH_DIR / f'p{n:02d}.json'
    if not glyph_file.exists():
        return []
    glyphs = json.load(open(glyph_file))

    p = REPO / 'original_sources' / '137' / f'P{n:03d}.png'
    if not p.exists():
        p = REPO / 'original_sources' / 'p011_p023_originals' / f'P{n:03d}.png'
    im = Image.open(p).convert('L')
    arr = np.array(im)

    formulas = []
    for g in glyphs:
        # Nur Glyphen mit hoher oder mittlerer Symmetrie
        if g.get('glyph_class') not in ('tengri_glyph', 'digit', 'unknown'):
            continue
        x, y, w, h = g['bbox']
        crop = arr[y:y+h, x:x+w]
        fclass = classify_formula(crop, g['bbox'])
        if fclass:
            formulas.append({
                'class': fclass,
                'symbol': FORMULA_SYMBOLS[fclass],
                'bbox': g['bbox'],
                'region_id': g['region_id'],
            })
    return formulas


def detect_fractions(n: int) -> int:
    """Suche nach Bruchstrukturen: 3 vertikal-gestapelte Glyphen mit ähnlicher Breite."""
    glyph_file = GLYPH_DIR / f'p{n:02d}.json'
    if not glyph_file.exists():
        return 0
    glyphs = json.load(open(glyph_file))
    if not glyphs:
        return 0

    # Gruppiere Glyphen nach ähnlicher x-Position (Spalten)
    by_x = {}
    for g in glyphs:
        x = g['bbox'][0]
        # Runde auf 50px-Bucket
        bucket = x // 50
        by_x.setdefault(bucket, []).append(g)

    fractions = 0
    for bucket, gs in by_x.items():
        # Sortiere nach y
        gs.sort(key=lambda g: g['bbox'][1])
        # Suche 3er-Gruppen mit ähnlicher Breite und vertikalem Abstand
        for i in range(len(gs) - 2):
            g1, g2, g3 = gs[i], gs[i+1], gs[i+2]
            x1, y1, w1, h1 = g1['bbox']
            x2, y2, w2, h2 = g2['bbox']
            x3, y3, w3, h3 = g3['bbox']
            # Kriterien: ähnliche Breite, vertikal gestapelt, kleiner Abstand
            if abs(w1 - w3) < 20 and abs(x1 - x3) < 30 and 5 < (y2 - y1) < 50 and 5 < (y3 - y2) < 50:
                fractions += 1
    return fractions


def main():
    log.info('=' * 60)
    log.info('PHASE 5: Formel-Detection (math_times/pi/exp + Brüche)')
    log.info('=' * 60)

    overall = {}
    for n in range(1, 24):
        formulas = detect_formulas_in_page(n)
        n_fractions = detect_fractions(n)

        # Kombiniere
        all_formulas = formulas + [{'class': 'fraction', 'symbol': '/', 'bbox': [0,0,0,0], 'region_id': f'frac_{i}'}
                                   for i in range(n_fractions)]
        (DATA / f'p{n:02d}.json').write_text(json.dumps(all_formulas, indent=2))

        ctr = Counter([f['class'] for f in formulas])
        overall[f'p{n:02d}'] = {
            'n_math_symbols': len(formulas),
            'n_times': ctr.get('math_times', 0),
            'n_pi': ctr.get('math_pi', 0),
            'n_exponentiation': ctr.get('math_exponentiation', 0),
            'n_fractions': n_fractions,
            'n_total': len(all_formulas),
        }
        log.info(
            f"  p{n:02d}: ×={ctr.get('math_times',0):2d} π={ctr.get('math_pi',0):2d} "
            f"^={ctr.get('math_exponentiation',0):2d} frac={n_fractions:2d} → total={len(all_formulas)}"
        )

    (DATA.parent / 'formulas_summary.json').write_text(json.dumps(overall, indent=2))
    total = sum(s['n_total'] for s in overall.values())
    log.info('')
    log.info(f'✓ Formel-Detection: {total} Formeln total')


if __name__ == '__main__':
    main()
