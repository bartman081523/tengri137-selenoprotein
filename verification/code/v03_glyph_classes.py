"""
v03_glyph_classes.py — Phase 2: BBox → Glyph-Klasse via phash-Clustering.

Methode (eigene, unabhängig von phase1d_train_v6.py / phase1e_template_similarity.py):
  1. Lade BBox-Listen aus v02
  2. Für jede BBox: crop aus Original-PNG, berechne phash (8x8 DCT-Hash)
  3. Cluster: phash-Hamming-Distanz < 8 = gleiche Klasse
  4. Pro Cluster: Klassen-Benennung deterministisch via Geometrie:
       - Höhe/Breite-Verhältnis > 3 = latein (Textzeile)
       - Quadratisch + hoher fill_ratio = Glyph (Tengri)
       - Klein (BBox < 25x25) = digit/symbol
       - Fallback: 'unknown'
  5. KEIN LLM, KEIN externes Modell.

Methoden-Referenz (NICHT als Quelle):
  - phase1d_train_v6.py: nutzte Triplet-Loss + ResNet18-Embeddings
  - phase1e_template_similarity.py: cv2.matchTemplate

Output:
  - verification/data/glyphs/pNN.json: [{region_id, bbox, phash, cluster_id, glyph_class}]
  - verification/data/glyphs_summary.json: {pNN: {n_glyphs, n_latin, n_digits, n_symbols, n_unknown}}
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
ORIG_1 = REPO / 'original_sources/137'
ORIG_2 = REPO / 'original_sources/p011_p023_originals'
DATA = REPO / 'verification' / 'data'
BBOX_DIR = DATA / 'bboxes'
GLYPH_DIR = DATA / 'glyphs'
LOGS = REPO / 'verification' / 'logs'
GLYPH_DIR.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOGS / 'v03.log', mode='w'), logging.StreamHandler()],
)
log = logging.getLogger(__name__)


def orig_path(n: int) -> Path:
    p = ORIG_1 / f'P{n:03d}.png'
    return p if p.exists() else ORIG_2 / f'P{n:03d}.png'


def phash_8x8(crop: np.ndarray) -> int:
    """Berechnet 8x8 DCT-basierten phash → 64-bit Integer."""
    # Resize auf 32x32 (Standard für phash)
    img = cv2.resize(crop, (32, 32), interpolation=cv2.INTER_AREA)
    # 2D DCT
    dct = cv2.dct(np.float32(img))
    # Nur 8x8 oben-links
    dct_small = dct[:8, :8]
    # Median (DC ausgenommen)
    med = np.median(dct_small.flatten()[1:])
    # Bits: 1 wenn > median, sonst 0
    bits = (dct_small > med).astype(int).flatten()
    # 64-bit Integer
    h = 0
    for b in bits:
        h = (h << 1) | int(b)
    return h


def hamming(h1: int, h2: int) -> int:
    return bin(h1 ^ h2).count('1')


def classify_bbox(bbox: list, fill_ratio: float, phash: int) -> str:
    """Deterministische Geometrie-basierte Klassifikation. KEIN LLM."""
    x, y, w, h = bbox
    aspect = h / w if w > 0 else 1.0

    # Latein: lang + schmal (Buchstabe oder Wort)
    if aspect > 2.5 and w < 60 and h > 20:
        return 'latin_letter'
    # Latein-Wort: lang, breit
    if aspect < 0.5 and w > 60 and h < 50:
        return 'latin_word_fragment'
    # Digit: sehr klein und quadratisch
    if w < 30 and h < 30 and fill_ratio > 0.4:
        return 'digit'
    # Tengri-Glyph: quadratisch, mittelgroß, hoher fill
    if 0.7 < aspect < 1.4 and 15 < w < 100 and 15 < h < 100 and fill_ratio > 0.3:
        return 'tengri_glyph'
    # Magic-Cube-Komponente: sehr großer Fill, mittelgroß
    if w > 100 or h > 100:
        return 'large_component'
    return 'unknown'


def cluster_glyphs(glyph_data: list) -> list:
    """Einfaches phash-Clustering: gleicher Cluster wenn Hamming < 8."""
    clusters = []  # list of (centroid_hash, members)
    for g in glyph_data:
        ph = g['phash']
        assigned = False
        for cidx, (centroid, members) in enumerate(clusters):
            if hamming(ph, centroid) < 8:
                members.append(g)
                assigned = True
                break
        if not assigned:
            clusters.append((ph, [g]))
    # Map members to cluster_ids
    out = []
    for cidx, (_, members) in enumerate(clusters):
        cluster_id = f"C{cidx:04d}"
        for m in members:
            new_g = dict(m)
            new_g['cluster_id'] = cluster_id
            new_g['cluster_size'] = len(members)
            out.append(new_g)
    return out


def process_page(n: int) -> dict:
    bbox_file = BBOX_DIR / f'p{n:02d}.json'
    if not bbox_file.exists():
        return {}
    boxes = json.load(open(bbox_file))
    if not boxes:
        return {'n_glyphs': 0, 'n_latin': 0, 'n_digits': 0, 'n_symbols': 0, 'n_unknown': 0}

    im = Image.open(orig_path(n)).convert('L')
    arr = np.array(im)

    glyph_data = []
    for b in boxes:
        x, y, w, h = b['bbox']
        crop = arr[y:y+h, x:x+w]
        if crop.size == 0:
            continue
        ph = phash_8x8(crop)
        gclass = classify_bbox(b['bbox'], b['fill_ratio'], ph)
        glyph_data.append({
            'region_id': b['region_id'],
            'bbox': b['bbox'],
            'fill_ratio': b['fill_ratio'],
            'phash': ph,
            'glyph_class': gclass,
        })

    # Clustering
    clustered = cluster_glyphs(glyph_data)
    (GLYPH_DIR / f'p{n:02d}.json').write_text(json.dumps(clustered, indent=2))

    # Summary
    classes = [g['glyph_class'] for g in clustered]
    summary = {
        'n_total': len(clustered),
        'n_tengri_glyph': classes.count('tengri_glyph'),
        'n_latin_letter': classes.count('latin_letter'),
        'n_latin_word_fragment': classes.count('latin_word_fragment'),
        'n_digit': classes.count('digit'),
        'n_large_component': classes.count('large_component'),
        'n_unknown': classes.count('unknown'),
    }
    # n_glyphs = was V10.4 als Glyphen zählt
    summary['n_glyphs'] = summary['n_tengri_glyph']
    summary['n_latin'] = summary['n_latin_letter'] + summary['n_latin_word_fragment']
    return summary


def main():
    log.info('=' * 60)
    log.info('PHASE 2: Glyph-Klassifikation via phash-Clustering')
    log.info(f'Start: {datetime.now().isoformat()}')
    log.info('=' * 60)

    overall = {}
    for n in range(1, 24):
        s = process_page(n)
        overall[f'p{n:02d}'] = s
        log.info(
            f"  p{n:02d}: total={s.get('n_total',0):4d}, "
            f"glyph={s.get('n_tengri_glyph',0):3d}, "
            f"latin={s.get('n_latin',0):3d}, "
            f"digit={s.get('n_digit',0):2d}, "
            f"large={s.get('n_large_component',0):2d}, "
            f"unk={s.get('n_unknown',0):3d}"
        )

    (GLYPH_DIR.parent / 'glyphs_summary.json').write_text(json.dumps(overall, indent=2))
    log.info('')
    total_glyphs = sum(s.get('n_glyphs', 0) for s in overall.values())
    total_latin = sum(s.get('n_latin', 0) for s in overall.values())
    log.info(f'✓ Glyph-Klassifikation: {total_glyphs} Glyphen, {total_latin} Latein-Komp. total')


if __name__ == '__main__':
    main()
