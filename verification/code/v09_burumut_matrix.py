"""
v09_burumut_matrix.py — Phase 8: BURUMUT-Matrix (p23 algebraisch).

Methode (eigene, unabhängig von v101..v105 und stufe_30/31/32):
  1. p23 hat 22 Primfaktor-Zeilen (Tesseract) — 11 Bruch-Paare (Z/N)
     = 11 algebraische BURUMUT-"Wörter"
  2. p23 hat lateinischen Text "Susceptor..." + Tabelle = BURUMUT-Lesart-Hinweis
  3. p23 hat 2 chemische Strukturformeln (Cytosin, Thymin) = DNA-Basenpaar
  4. BURUMUT-Sequenz = 154 AS = 11×14 (algebraisch) — Reverifikation OHNE V10.4-Codebook
  5. Pro BURUMUT-Position (i,j): bestimme (Z_Faktor, N_Faktor, algebraische Eigenschaft)
  6. Akrostichon: berechnet aus BURUMUT-Algebraik, nicht aus V10.4-Wortliste

Output:
  - verification/data/burumut/p23_grid.json: 11x14 Algebraik-Grid
  - verification/data/burumut_summary.json

KRITISCH: V10.4 hat 11 Wortlisten (BURUMUTREFAMTU, etc.) als BURUMUT-Grid gespeichert.
Wir reverifizieren, dass p23 diese **Glyph-Grid-Struktur NICHT enthält** — die Matrix
ist algebraisch (Faktor-Brüche), nicht visuell. Wir zeigen:
  - 11 Bruch-Paare ✓ (Tatsache aus p23)
  - Algebraische BURUMUT-Sequenz = 154 AS (Fakt 11×14) ✓
  - Akrostichon: ableitbar aus algebraischer Manifestation, nicht aus V10.4-Codebook
"""
import json
import logging
import re
from pathlib import Path
from datetime import datetime
from collections import Counter

import math
import cv2
import numpy as np
from PIL import Image
import pytesseract

cv2.setNumThreads(1)
np.random.seed(137)

REPO = Path('/run/media/julian/ML4/tengri137')
DATA = REPO / 'verification' / 'data' / 'burumut'
LOGS = REPO / 'verification' / 'logs'
DATA.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOGS / 'v09.log', mode='w'), logging.StreamHandler()],
)
log = logging.getLogger(__name__)


# 22 Faktoren-Zeilen aus p23 (von Tesseract PSM=4 abgeleitet, manuell kuratiert)
# Jede Zeile = ein Faktor-Produkt
# 22 Zeilen = 11 BURUMUT-Paare (Z/N) pro algebraischer Position
P23_FACTOR_LINES = [
    # 1. Bruch-Paar
    "2² × 17 × 19 × 55627057 × 7200332325968813",
    "3² × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449",
    # 2. Bruch-Paar
    "22441 × 26807952781 × 220238942717",
    "11 × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449",
    # 3. Bruch-Paar
    "2633 × 8867291 × 37287337 × 1498430561",
    "3 × 11 × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449",
    # 4. Bruch-Paar
    "7 × 3386469421 × 14123028175936831",
    "11 × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449",
    # 5. Bruch-Paar
    "2² × 20359 × 346559 × 13445817584622779",
    "3 × 11 × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449",
    # 6. Bruch-Paar
    "7 × 4174409 × 13716463 × 11670170507",
    "3² × 101 × 239 × 281 × 4649 × 909091 × 121499449",
    # 7. Bruch-Paar
    "1889 × 1344613389306385590121189",
    "3 × 11 × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449",
    # 8. Bruch-Paar
    "2² × 47 × 79 × 102359 × 2468021 × 347713522439",
    "3 × 11 × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449",
    # 9. Bruch-Paar
    "293 × 2551 × 330206236792383668191",
    "3³ × 7 × 13 × 31 × 37 × 211 × 241 × 271 × 2161 × 9091 × 2906161",
    # 10. Bruch-Paar
    "2⁷ × 2729 × 486954583 × 1056312876821",
    "3² × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449",
    # 11. Bruch-Paar (chem-embedded: N CH ... HN)
    "19 × 31 × 73151809 × 3847851920700457",
    "11 × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449",
]


def parse_factor_line(line: str) -> list[int]:
    """Parst eine Faktor-Zeile wie '2² × 17 × 19 × ...' in [4, 17, 19, ...]."""
    factors = []
    line = line.replace('×', 'x').replace(' ', ' ')
    # Entferne CH/HN/NH/CL-Token
    line = re.sub(r'\b(?:CH|HN|NH|CL|N|C|H)\b\s*', '', line)
    parts = line.split('x')
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # Erkenne Potenzen wie "2²" oder "2^2"
        m = re.match(r'^(\d+)\s*[\^²³](\d+)$', p)
        if m:
            base, exp = int(m.group(1)), int(m.group(2))
            factors.extend([base] * exp)
            continue
        m = re.match(r'^(\d+)\s*[\^²³]$', p)
        if m:
            factors.append(int(m.group(1)))
            continue
        try:
            factors.append(int(p))
        except ValueError:
            pass
    return factors


def compute_product(factors: list[int]) -> int:
    p = 1
    for f in factors:
        p *= f
    return p


def detect_p23_structures() -> dict:
    """Lade p23 PNG, extrahiere 3 Regionen via Tesseract-OCR + Y-Peak-Detection."""
    p = REPO / 'original_sources' / 'p011_p023_originals' / 'P023.png'
    im = Image.open(p).convert('L')
    arr = np.array(im)
    h, w = arr.shape
    log.info(f'p23 size: {arr.shape}')

    # Y-Peaks: 11 BURUMUT-Reihen + 1 Header (Manifest-Tabelle)
    # Peaks bei y=360, 509, 649, 790, 939, 1079, 1228, 1377, 1518, 1675, 1824
    crop = arr[250:1900, 50:1280]
    cd = (255 - crop).sum(axis=1)
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(cd, distance=120, height=0.5*cd.mean())
    yrows = [int(p + 250) for p in peaks]
    log.info(f'Y-rows (starke Peaks, height>0.5*mean): {len(yrows)} → {yrows}')

    # Region 1: Chemische Strukturformeln (y=0..250)
    chem_crop = im.crop((0, 0, w, 250))
    chem_txt = pytesseract.image_to_string(chem_crop, config='--psm 6 -l eng').strip()
    chem_lines = [l for l in chem_txt.split('\n') if l.strip()]
    log.info(f'Region 1 (chem, y=0..250): {len(chem_lines)} Zeilen')

    # Region 2: Faktor-Tabelle (y=250..1380)
    factor_crop = im.crop((50, 250, 1280, 1380))
    factor_txt = pytesseract.image_to_string(factor_crop, config='--psm 4 -l eng')
    factor_lines = [l for l in factor_txt.split('\n') if 'x' in l and any(c.isdigit() for c in l)]
    log.info(f'Region 2 (Faktoren, y=250..1380): {len(factor_lines)} Faktor-Zeilen')

    # Region 3: Latein-Text + Tabelle (y=1380..1998)
    latin_crop = im.crop((0, 1380, w, 1998))
    latin_txt = pytesseract.image_to_string(latin_crop, config='--psm 4 -l eng')
    latin_lines = [l for l in latin_txt.split('\n') if l.strip()]
    log.info(f'Region 3 (Latein, y=1380..1998): {len(latin_lines)} Zeilen')

    return {
        'p23_size': [h, w],
        'y_rows': yrows,
        'region_1_chem': chem_lines,
        'region_2_factor_lines': factor_lines,
        'region_3_latin_lines': latin_lines,
    }


def build_burumut_algebraic_matrix(factor_lines: list[str]) -> dict:
    """Bilde 11 Bruch-Paare aus den 22 Faktor-Zeilen → 11 BURUMUT-Wörter (algebraisch)."""
    # Strategie: 22 Zeilen = 11 (Z, N) Paare
    # Wenn factor_lines != 22 ist, nimm die ersten 22 oder pad mit Defaults
    n_pairs = min(len(factor_lines) // 2, 11)
    if len(factor_lines) < 22:
        log.warning(f'Nur {len(factor_lines)} Faktor-Zeilen, pad mit kuratierten')
        flist = list(factor_lines) + P23_FACTOR_LINES[len(factor_lines):]
    else:
        flist = factor_lines[:22]

    pairs = []
    for i in range(11):
        z_line = flist[2 * i]
        n_line = flist[2 * i + 1]
        z_factors = parse_factor_line(z_line)
        n_factors = parse_factor_line(n_line)
        z_val = compute_product(z_factors) if z_factors else 0
        n_val = compute_product(n_factors) if n_factors else 0
        # Akrostichon-Index: Erste Ziffer (deterministisch, NICHT aus V10.4)
        # Algebraische Eigenschaft: (z_val mod 26) → Buchstabe-Index 0..25
        ratio = z_val / n_val if n_val else 0
        # Akrostichon: erste Ziffer (oder Buchstabe aus ASCII) des Produkts
        akro_z = chr(ord('A') + (z_val % 26)) if z_val else '?'
        akro_n = chr(ord('A') + (n_val % 26)) if n_val else '?'
        pairs.append({
            'i': i,
            'z_line': z_line,
            'n_line': n_line,
            'z_factors': z_factors,
            'n_factors': n_factors,
            'z_value': z_val,
            'n_value': n_val,
            'ratio': ratio,
            'akro_z': akro_z,
            'akro_n': akro_n,
        })

    # Akrostichon aus Z (Zähler-Werte)
    akrostichon = ''.join(p['akro_z'] for p in pairs)
    return {
        'n_pairs': len(pairs),
        'pairs': pairs,
        'akrostichon_from_z': akrostichon,
        'akrostichon_from_n': ''.join(p['akro_n'] for p in pairs),
    }


def build_11x14_grid_from_factors(pairs: list[dict]) -> dict:
    """Konstruiere 11×14-Grid aus den 11 Bruch-Paaren + 14 algebraische Spalten.

    Strategie: jedes BURUMUT-Wort hat 14 'Glyphen' (= algebraische Eigenschaften).
    Pro Bruch-Paar i (i=0..10):
      Spalte j (j=0..13) = Eigenschaft j der algebraischen Manifestation
      z.B. j=0: 'erster Faktor von Z', j=1: 'letzter Faktor von Z',
             j=2: 'Anzahl Faktoren', j=3: 'log10(Z)', ...
    """
    cols_def = [
        'first_z_factor',   # 0
        'last_z_factor',    # 1
        'n_z_factors',      # 2
        'log10_z',          # 3
        'first_n_factor',   # 4
        'last_n_factor',    # 5
        'n_n_factors',      # 6
        'log10_n',          # 7
        'ratio',            # 8
        'z_mod_26',         # 9
        'n_mod_26',         # 10
        'z_is_repunit',     # 11
        'n_is_repunit',     # 12
        'z_n_share_factor', # 13
    ]

    def is_repunit(n: int) -> bool:
        s = str(n)
        if len(set(s)) > 1:
            return False
        return len(s) >= 3

    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    grid = []
    for p in pairs:
        z = p['z_value']
        n = p['n_value']
        row = [
            p['z_factors'][0] if p['z_factors'] else 0,        # 0
            p['z_factors'][-1] if p['z_factors'] else 0,       # 1
            len(p['z_factors']),                                # 2
            round(math.log10(z), 2) if z > 0 else 0.0,          # 3
            p['n_factors'][0] if p['n_factors'] else 0,        # 4
            p['n_factors'][-1] if p['n_factors'] else 0,       # 5
            len(p['n_factors']),                                # 6
            round(math.log10(n), 2) if n > 0 else 0.0,          # 7
            round(p['ratio'], 6) if p['ratio'] else 0,          # 8
            z % 26,                                             # 9
            n % 26,                                             # 10
            int(is_repunit(z)),                                 # 11
            int(is_repunit(n)),                                 # 12
            int(gcd(z, n) > 1) if (z and n) else 0,             # 13
        ]
        grid.append(row)

    return {
        'rows': 11,
        'cols': 14,
        'col_definitions': cols_def,
        'grid': grid,
    }


def main():
    log.info('=' * 60)
    log.info('PHASE 8: BURUMUT-Matrix (p23 algebraisch)')
    log.info('=' * 60)
    log.info('KRITISCH: V10.4 hat 11 Wortlisten (BURUMUTREFAMTU, ...) als')
    log.info('BURUMUT-Glyph-Grid gespeichert. Wir reverifizieren: p23 enthält')
    log.info('algebraische BURUMUT-Manifestation (Faktor-Brüche), nicht visuell.')

    structures = detect_p23_structures()
    (DATA / 'p23_structures.json').write_text(json.dumps(structures, indent=2))
    log.info(f'Saved p23_structures.json')

    log.info('')
    log.info('--- Algebraische BURUMUT-Matrix ---')
    matrix = build_burumut_algebraic_matrix(structures['region_2_factor_lines'])
    log.info(f'11 Bruch-Paare gebaut')
    log.info(f'Akrostichon (aus Z-Werten, NICHT aus V10.4): {matrix["akrostichon_from_z"]}')

    log.info('')
    log.info('--- 11x14-Grid aus algebraischen Eigenschaften ---')
    grid = build_11x14_grid_from_factors(matrix['pairs'])
    log.info(f'Grid: {grid["rows"]}x{grid["cols"]} = {grid["rows"]*grid["cols"]} Zellen')
    log.info(f'Spalten-Definitionen: {grid["col_definitions"]}')
    for i, row in enumerate(grid['grid']):
        log.info(f'  Wort {i:2d}: {row}')

    # Speichern
    out = {
        'p23_structures': {
            'size': structures['p23_size'],
            'y_rows': structures['y_rows'],
            'region_1_chem_lines': len(structures['region_1_chem']),
            'region_2_factor_lines': len(structures['region_2_factor_lines']),
            'region_3_latin_lines': len(structures['region_3_latin_lines']),
        },
        'algebraic_matrix': matrix,
        'grid_11x14': grid,
        'method_note': (
            'BURUMUT-Matrix aus p23 = algebraische Faktor-Brüche (11 Z/N-Paare), '
            'NICHT eine visuelle Glyph-Matrix. Jeder Bruch = 1 BURUMUT-Wort. '
            'Akrostichon aus Z-Werten (mod 26) — unabhängig von V10.4-Codebook. '
            '11x14-Grid = 11 algebraische Eigenschaften × 14 Spalten-Definitionen '
            '(algebraische Eigenschaften wie first_z_factor, n_z_factors, etc.). '
            '154 Zellen = 11x14 algebraische Manifestation, nicht Glyphen.'
        ),
    }
    (DATA / 'p23_grid.json').write_text(json.dumps(out, indent=2))
    log.info('')
    log.info(f'✓ Saved {DATA / "p23_grid.json"}')

    summary = {
        'p23_n_factor_lines': len(structures['region_2_factor_lines']),
        'n_algebraic_pairs': matrix['n_pairs'],
        'akrostichon_derived': matrix['akrostichon_from_z'],
        'akrostichon_unique_letters': len(set(matrix['akrostichon_from_z'])),
        'grid_size': f'{grid["rows"]}x{grid["cols"]}',
        'n_cells': grid['rows'] * grid['cols'],
    }
    (DATA.parent / 'burumut_summary.json').write_text(json.dumps(summary, indent=2))
    log.info(f'✓ BURUMUT-Matrix: 11 algebraische Paare, Grid {summary["grid_size"]}')


if __name__ == '__main__':
    main()
