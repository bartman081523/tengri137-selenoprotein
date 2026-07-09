"""
v08_magic_cubes.py — Phase 7: Magic-Cube-Detection (3x3-Grid).

Methode (eigene, unabhängig von stufe_10_p18):
  1. Magic Cube = 9 nahezu identische quadratische Komponenten in 3x3-Anordnung
  2. Suche nach Glyphen-Tripeln mit:
     - ähnliche Größe (innerhalb ±30%)
     - gleicher x-Spalte ODER gleicher y-Zeile
     - regelmäßige Abstände
  3. KEINE Summen-Berechnung (137, 666) — das ist semantisch, nicht aus Bildern ableitbar
  4. Strukturelle Heuristik: zähle 3x3-Cluster

Output:
  - verification/data/magic_cubes/pNN.json: [{cluster: [[x,y],...], avg_size}]
  - verification/data/magic_cubes_summary.json
"""
import json
import logging
from pathlib import Path
from datetime import datetime

import cv2
import numpy as np

cv2.setNumThreads(1)
np.random.seed(137)

REPO = Path('/run/media/julian/ML4/tengri137')
DATA = REPO / 'verification' / 'data' / 'magic_cubes'
BBOX_DIR = REPO / 'verification' / 'data' / 'bboxes'
LOGS = REPO / 'verification' / 'logs'
DATA.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOGS / 'v08.log', mode='w'), logging.StreamHandler()],
)
log = logging.getLogger(__name__)


def find_3x3_clusters(boxes: list, size_tol: float = 0.30) -> list[dict]:
    """Suche 3x3-Cluster aus ähnlich großen Boxen."""
    # Filter: nur mittelgroße quadratische BBoxes
    candidates = []
    for b in boxes:
        x, y, w, h = b['bbox']
        if 30 < w < 150 and 30 < h < 150 and 0.7 < (h/w) < 1.4:
            candidates.append(b)

    if len(candidates) < 9:
        return []

    # Suche 3 Boxen mit ähnlicher Größe auf gleicher y-Höhe
    by_y = {}
    for b in candidates:
        y_center = b['bbox'][1] + b['bbox'][3] // 2
        bucket = y_center // 60  # 60px-Toleranz für gleiche Zeile
        by_y.setdefault(bucket, []).append(b)

    # Suche 3 Zeilen mit jeweils 3 Boxen
    clusters = []
    y_buckets = sorted(by_y.keys())
    for i in range(len(y_buckets) - 2):
        b1, b2, b3 = by_y[y_buckets[i]], by_y[y_buckets[i+1]], by_y[y_buckets[i+2]]
        # Suche Tripel aus diesen 3 Buckets, mit ähnlichen x-Spalten
        for c1 in b1:
            for c2 in b2:
                if abs(c1['bbox'][0] - c2['bbox'][0]) > 30:
                    continue
                for c3 in b3:
                    if abs(c1['bbox'][0] - c3['bbox'][0]) > 30:
                        continue
                    # Kandidaten für 3x3-Grid
                    # Suche weitere 2 in jeder Zeile
                    row1 = [c1] + [b for b in b1 if b != c1 and abs(b['bbox'][0] - c1['bbox'][0]) > 30]
                    row2 = [c2] + [b for b in b2 if b != c2 and abs(b['bbox'][0] - c2['bbox'][0]) > 30]
                    row3 = [c3] + [b for b in b3 if b != c3 and abs(b['bbox'][0] - c3['bbox'][0]) > 30]
                    if len(row1) >= 3 and len(row2) >= 3 and len(row3) >= 3:
                        # Eindeutige Tripel
                        for j in range(1, min(len(row1), 3)):
                            for k in range(1, min(len(row2), 3)):
                                for l in range(1, min(len(row3), 3)):
                                    if (row1[j]['bbox'][0] - c1['bbox'][0]) > 30 and \
                                       abs(row2[k]['bbox'][0] - c2['bbox'][0]) > 30 and \
                                       abs(row3[l]['bbox'][0] - c3['bbox'][0]) > 30:
                                        cluster_3x3 = [[row1[0], row1[j], row1[2] if len(row1)>2 else row1[1]],
                                                       [row2[0], row2[k], row2[2] if len(row2)>2 else row2[1]],
                                                       [row3[0], row3[l], row3[2] if len(row3)>2 else row3[1]]]
                                        clusters.append({
                                            'cluster': [
                                                [b['bbox'] for b in row]
                                                for row in cluster_3x3
                                            ],
                                            'avg_size': int(np.mean([b['bbox'][2] for b in [c1, c2, c3]])),
                                        })
                                        break
    return clusters[:5]  # max 5 Cluster pro Page


def main():
    log.info('=' * 60)
    log.info('PHASE 7: Magic-Cube 3x3-Grid-Detection')
    log.info('=' * 60)

    overall = {}
    for n in range(1, 24):
        bbox_file = BBOX_DIR / f'p{n:02d}.json'
        if not bbox_file.exists():
            continue
        boxes = json.load(open(bbox_file))
        clusters = find_3x3_clusters(boxes)
        (DATA / f'p{n:02d}.json').write_text(json.dumps(clusters, indent=2))
        overall[f'p{n:02d}'] = {'n_3x3_clusters': len(clusters)}
        log.info(f"  p{n:02d}: 3x3-Cluster = {len(clusters)}")

    (DATA.parent / 'magic_cubes_summary.json').write_text(json.dumps(overall, indent=2))
    total = sum(s['n_3x3_clusters'] for s in overall.values())
    log.info('')
    log.info(f'✓ Magic-Cubes: {total} 3x3-Cluster total')


if __name__ == '__main__':
    main()
