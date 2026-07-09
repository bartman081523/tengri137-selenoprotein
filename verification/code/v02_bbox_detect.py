"""
v02_bbox_detect.py — Phase 1: BBox-Detection via OpenCV.

Methode (eigene, unabhängig von phase1_pixel_v4.py):
  1. Original-PNG → Graustufen → Otsu-Threshold
  2. cv2.findContours(RETR_EXTERNAL) auf Binarisierung
  3. Filter: bbox muss in [8, 200] px Breite und [8, 200] px Höhe sein
  4. fill_ratio = dark_pixels_in_bbox / bbox_area (>= 0.10)
  5. region_id = "pNN_R{k}" mit Zeilen-Sortierung (top-to-bottom, left-to-right)

Methoden-Referenz (NICHT als Quelle benutzt):
  - phase1_pixel_v4.py: nutzte cv2.findContours + Mindestgröße 8x8.
  - phase1_pixel.py: ähnlich, mit morphologischen Operationen.

Output:
  - verification/data/bboxes/pNN.json: [{region_id, bbox, area, fill_ratio}]
  - verification/data/bboxes_summary.json: {pNN: {n_regions, n_large, ...}}
"""
import json
import logging
from pathlib import Path
from datetime import datetime

import cv2
import numpy as np
from PIL import Image

cv2.setNumThreads(1)
np.random.seed(137)

REPO = Path('/run/media/julian/ML4/tengri137')
ORIG_1 = REPO / 'original_sources/137'
ORIG_2 = REPO / 'original_sources/p011_p023_originals'
DATA = REPO / 'verification' / 'data' / 'bboxes'
LOGS = REPO / 'verification' / 'logs'
DATA.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOGS / 'v02.log', mode='w'), logging.StreamHandler()],
)
log = logging.getLogger(__name__)

# Filter-Konstanten
MIN_W, MAX_W = 8, 200
MIN_H, MAX_H = 8, 200
MIN_FILL = 0.10


def orig_path(n: int) -> Path:
    p = ORIG_1 / f'P{n:03d}.png'
    return p if p.exists() else ORIG_2 / f'P{n:03d}.png'


def detect_bboxes(img_path: Path) -> list[dict]:
    """Detect bboxes with OpenCV. Returns list of dicts sorted top-to-bottom, left-to-right."""
    im = Image.open(img_path).convert('L')
    arr = np.array(im)

    # Otsu-Threshold
    blur = cv2.GaussianBlur(arr, (3, 3), 0)
    _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Morphologische Operation: kleine Noise entfernen
    kernel = np.ones((2, 2), np.uint8)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if not (MIN_W <= w <= MAX_W and MIN_H <= h <= MAX_H):
            continue
        # fill_ratio
        roi = th[y:y+h, x:x+w]
        fill = (roi > 0).sum() / (w * h)
        if fill < MIN_FILL:
            continue
        boxes.append({
            'bbox': [int(x), int(y), int(w), int(h)],
            'area': int(w * h),
            'fill_ratio': round(float(fill), 3),
        })

    # Sort: top-to-bottom, dann left-to-right
    boxes.sort(key=lambda b: (b['bbox'][1] // 50, b['bbox'][0]))
    # Re-Index als region_id
    for i, b in enumerate(boxes):
        b['region_id'] = f"p{img_path.stem[1:3]}_R{i+1}"
    return boxes


def main():
    log.info('=' * 60)
    log.info('PHASE 1: BBox-Detection aller 23 Original-PNGs')
    log.info(f'Start: {datetime.now().isoformat()}')
    log.info('=' * 60)

    summary = {}
    for n in range(1, 24):
        p = orig_path(n)
        boxes = detect_bboxes(p)
        out = DATA / f'p{n:02d}.json'
        out.write_text(json.dumps(boxes, indent=2))

        # Summary
        n_total = len(boxes)
        n_large = sum(1 for b in boxes if b['area'] > 5000)
        n_small = sum(1 for b in boxes if b['area'] < 500)
        n_dense = sum(1 for b in boxes if b['fill_ratio'] > 0.5)
        summary[f'p{n:02d}'] = {
            'n_regions': n_total,
            'n_large_gt5000px': n_large,
            'n_small_lt500px': n_small,
            'n_dense_fill_gt50pct': n_dense,
            'avg_fill_ratio': round(float(np.mean([b['fill_ratio'] for b in boxes])), 3) if boxes else 0.0,
        }
        log.info(
            f"  p{n:02d}: n_regions={n_total:3d}, large={n_large:2d}, "
            f"small={n_small:3d}, dense={n_dense:2d}, "
            f"avg_fill={summary[f'p{n:02d}']['avg_fill_ratio']:.3f}"
        )

    (DATA.parent / 'bboxes_summary.json').write_text(json.dumps(summary, indent=2))
    log.info('')
    log.info(f'✓ BBox-Detection fertig: {sum(s["n_regions"] for s in summary.values())} Regionen total')


if __name__ == '__main__':
    main()
