"""
v01_pixel_audit.py — Phase 0: Pixel-Statistik pro Page.

Methode (eigene, unabhängig von phase1_pixel_v4.py):
  - Pro Original-PNG (P001-P023):
    * Bildgröße (HxW)
    * Mean / Std / Min / Max / Median Grauwert
    * Schwarzanteil (< 64) und Weißanteil (> 192)
    * Histogramm-Peaks (3 hellste Buckets)
    * 4×6-Tile-Grid mit je Mean, um Layout-Regionen zu erfassen
  - Deterministisch: kein Random, np nur für Aggregationen.

Output:
  - verification/data/audit.json (Liste von 23 Einträgen)
  - verification/data/audit_per_tile/<pN>.json (Tile-Means)
  - verification/logs/v01.log
"""
import json
import logging
from pathlib import Path
from datetime import datetime

import numpy as np
from PIL import Image

REPO = Path('/run/media/julian/ML4/tengri137')
ORIG_1 = REPO / 'original_sources/137'
ORIG_2 = REPO / 'original_sources/p011_p023_originals'
OUT = REPO / 'verification'
DATA = OUT / 'data'
LOGS = OUT / 'logs'

LOGS.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)
(DATA / 'audit_per_tile').mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOGS / 'v01.log', mode='w'),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def orig_path(n: int) -> Path:
    pid = f'P{n:03d}.png'
    p = ORIG_1 / pid
    return p if p.exists() else ORIG_2 / pid


def tile_grid(arr: np.ndarray, rows: int = 4, cols: int = 6) -> np.ndarray:
    """Returns (rows, cols) array of mean gray per tile."""
    H, W = arr.shape
    th, tw = H // rows, W // cols
    out = np.zeros((rows, cols), dtype=np.float32)
    for r in range(rows):
        for c in range(cols):
            tile = arr[r*th:(r+1)*th, c*tw:(c+1)*tw]
            out[r, c] = tile.mean()
    return out


def audit_page(n: int) -> dict:
    p = orig_path(n)
    im = Image.open(p).convert('L')  # Graustufen
    arr = np.array(im)
    H, W = arr.shape

    mean = float(arr.mean())
    std = float(arr.std())
    median = float(np.median(arr))
    minv = int(arr.min())
    maxv = int(arr.max())
    black_frac = float((arr < 64).sum() / arr.size)
    white_frac = float((arr > 192).sum() / arr.size)

    # Histogramm-Peaks (Bins zu 32)
    hist, _ = np.histogram(arr, bins=32, range=(0, 256))
    peak_bins = sorted(range(32), key=lambda b: -hist[b])[:3]
    peak_values = [int(b * 8 + 4) for b in peak_bins]  # Bin-Mitte
    peak_counts = [int(hist[b]) for b in peak_bins]

    # Tile-Means
    tiles = tile_grid(arr, 4, 6)
    # Layout-Cluster: sehr helle Tiles = leerer Rand
    bright_tiles = (tiles > 220).sum()

    return {
        'page_id': f'p{n:02d}',
        'image_path': str(p.relative_to(REPO)),
        'image_size': [H, W],
        'mean_gray': round(mean, 2),
        'std_gray': round(std, 2),
        'median_gray': round(median, 1),
        'min_gray': minv,
        'max_gray': maxv,
        'black_fraction_lt64': round(black_frac, 4),
        'white_fraction_gt192': round(white_frac, 4),
        'histogram_peak_means': peak_values,
        'histogram_peak_counts': peak_counts,
        'tile_grid_4x6': [[round(float(tiles[r, c]), 1) for c in range(6)] for r in range(4)],
        'bright_tiles_gt220': int(bright_tiles),
    }


def main():
    log.info('=' * 60)
    log.info(f'PHASE 0: Pixel-Audit aller 23 Original-PNGs')
    log.info(f'Start: {datetime.now().isoformat()}')
    log.info('=' * 60)

    audit = []
    for n in range(1, 24):
        entry = audit_page(n)
        audit.append(entry)
        # Tile-Means separat speichern
        (DATA / 'audit_per_tile' / f'p{n:02d}.json').write_text(
            json.dumps(entry['tile_grid_4x6'], indent=2)
        )
        log.info(
            f"  p{n:02d}: H×W={entry['image_size']}, "
            f"mean={entry['mean_gray']:.1f}, "
            f"std={entry['std_gray']:.1f}, "
            f"black={entry['black_fraction_lt64']:.3f}, "
            f"bright_tiles={entry['bright_tiles_gt220']}"
        )

    out_path = DATA / 'audit.json'
    out_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False))
    log.info('')
    log.info(f'✓ {len(audit)} Pages auditiert → {out_path}')

    # Sanity-Statistik
    means = [a['mean_gray'] for a in audit]
    blacks = [a['black_fraction_lt64'] for a in audit]
    log.info(f'  Mean gray range: {min(means):.1f} .. {max(means):.1f}')
    log.info(f'  Black frac range: {min(blacks):.3f} .. {max(blacks):.3f}')

    # Heuristik: Magic-Cube-Seiten haben viele Glyphen (= niedriger Mean, hoher Black-Anteil)
    # Wir klassifizieren NICHT, listen nur auf
    log.info('')
    log.info('Heuristik-Warnung: Seiten mit hohem Black-Anteil (>0.10) sind Glyphen-dicht:')
    for a in audit:
        if a['black_fraction_lt64'] > 0.10:
            log.info(f"  {a['page_id']}: black_frac={a['black_fraction_lt64']:.3f}")


if __name__ == '__main__':
    main()
