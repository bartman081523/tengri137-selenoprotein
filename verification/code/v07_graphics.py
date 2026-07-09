"""
v07_graphics.py — Phase 6: Bilder / Drawings Detection.

Methode (eigene, unabhängig von stufe_12_*):
  1. Suche BBox-Regionen > 100x100 px (oder zusammenhängende Komponenten), die KEINE Glyphe/Latein sind
  2. Strukturelle Heuristik: hohe fill_ratio + komplexe Form = drawing
  3. KEINE chemische Semantik (Cytosin, Amidin) — nur "es ist ein Bild"

Output:
  - verification/data/graphics/pNN.json: [{bbox, area, fill_ratio, kind}]
  - verification/data/graphics_summary.json
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
DATA = REPO / 'verification' / 'data' / 'graphics'
GLYPH_DIR = REPO / 'verification' / 'data' / 'glyphs'
BBOX_DIR = REPO / 'verification' / 'data' / 'bboxes'
LOGS = REPO / 'verification' / 'logs'
DATA.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOGS / 'v07.log', mode='w'), logging.StreamHandler()],
)
log = logging.getLogger(__name__)


def detect_graphics(n: int) -> list[dict]:
    """Großflächige Komponenten, die keine kleinen Glyphen sind."""
    bbox_file = BBOX_DIR / f'p{n:02d}.json'
    if not bbox_file.exists():
        return []
    boxes = json.load(open(bbox_file))

    # Original-PNG
    p = REPO / 'original_sources' / '137' / f'P{n:03d}.png'
    if not p.exists():
        p = REPO / 'original_sources' / 'p011_p023_originals' / f'P{n:03d}.png'
    im = Image.open(p).convert('L')
    arr = np.array(im)

    graphics = []
    for b in boxes:
        x, y, w, h = b['bbox']
        area = w * h
        # Groß = drawing
        if area < 10000:  # mind. 100x100
            continue
        # Wenn fill_ratio zwischen 0.2 und 0.7 → Komposition, nicht nur Schwarz
        if 0.10 < b['fill_ratio'] < 0.80:
            kind = 'graphic'
            # Wenn sehr kreisförmig → Magic-Cube-Komponente oder Siegel
            aspect = h / w if w > 0 else 1.0
            if 0.7 < aspect < 1.4 and b['fill_ratio'] > 0.3:
                kind = 'round_seal_or_cube_component'
            graphics.append({
                'bbox': b['bbox'],
                'area': area,
                'fill_ratio': b['fill_ratio'],
                'kind': kind,
            })
    return graphics


def main():
    log.info('=' * 60)
    log.info('PHASE 6: Bilder / Drawings Detection')
    log.info('=' * 60)

    overall = {}
    for n in range(1, 24):
        g = detect_graphics(n)
        (DATA / f'p{n:02d}.json').write_text(json.dumps(g, indent=2))
        ctr = Counter([x['kind'] for x in g])
        overall[f'p{n:02d}'] = {
            'n_total': len(g),
            'n_round_seal': ctr.get('round_seal_or_cube_component', 0),
            'n_graphic': ctr.get('graphic', 0),
        }
        log.info(f"  p{n:02d}: graphics={len(g):2d} (round={ctr.get('round_seal_or_cube_component',0)}, graphic={ctr.get('graphic',0)})")

    (DATA.parent / 'graphics_summary.json').write_text(json.dumps(overall, indent=2))
    total = sum(s['n_total'] for s in overall.values())
    log.info('')
    log.info(f'✓ Drawings: {total} total')


if __name__ == '__main__':
    main()
