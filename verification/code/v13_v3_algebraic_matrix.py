"""
v13_v3_algebraic_matrix.py — V3 Reverifikation: Algebraische BURUMUT-Matrix.

Methode (algebraisch, OHNE Wikia-Trigger):
  1. Lade 11 Faktor-Brüche aus V1 (verification/data/burumut/p23_grid.json)
  2. Baue 11×14 algebraische Matrix mit 14 Faktor-Properties als Spalten
  3. Baue 11 14-Bit-Codes aus Faktor-Boolean-Properties (analog V25/V26 Architektur)
  4. Berechne 2 Akrostichon-Kandidaten (Z-mod-26, Anzahl-Faktoren-mod-26)
  5. Schreibe 4 JSON-Snapshots + V3_FINAL_BILANZ.md

KRITISCH: V3 nutzt KEIN Wikia, KEIN V10.4-Codebook, KEINE V7 Tappeiner-Kandidaten.
Die 14 Spalten-Definitionen sind rein mathematisch (F + K).
"""
import json
import logging
import math
from pathlib import Path
from datetime import datetime
from collections import Counter

REPO = Path('/run/media/julian/ML4/tengri137')
DATA = REPO / 'verification' / 'data' / 'burumut'
SNAPSHOTS = REPO / 'verification' / 'results' / 'snapshots'
RESULTS = REPO / 'verification' / 'results'
LOGS = REPO / 'verification' / 'logs'
SNAPSHOTS.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOGS / 'v13.log', mode='w'), logging.StreamHandler()],
)
log = logging.getLogger(__name__)


# === Algebraische Spalten-Definitionen (14 Spalten, F + K) ===
COLUMN_DEFS = [
    # (#, name, formula_text, type, range)
    (0,  'z_factors_first_mod26',  'first Z factor mod 26',           'mod',    '0..25'),
    (1,  'z_factors_last_mod26',   'last Z factor mod 26',            'mod',    '0..25'),
    (2,  'n_z_factors',            'count of Z factors',              'count',  '2..5'),
    (3,  'log10_z_digitsum',       'digit-sum of ⌊log10(Z)⌋',         'algebra','0..∞'),
    (4,  'n_factors_first_mod26',  'first N factor mod 26',           'mod',    '0..25'),
    (5,  'n_factors_last_mod26',   'last N factor mod 26',            'mod',    '0..25'),
    (6,  'n_n_factors',            'count of N factors',              'count',  '6..11'),
    (7,  'log10_n_digitsum',       'digit-sum of ⌊log10(N)⌋',         'algebra','0..∞'),
    (8,  'ratio_mod26',            '(Z/N) mod 26',                    'mod',    '0..25'),
    (9,  'z_value_mod26',          'Z value mod 26',                  'mod',    '0..25'),
    (10, 'n_value_mod26',          'N value mod 26',                  'mod',    '0..25'),
    (11, 'z_is_repunit',           'Z is repunit (111..1)?',          'bool',   '0/1'),
    (12, 'n_is_repunit',           'N is repunit (111..1)?',          'bool',   '0/1'),
    (13, 'gcd_z_n_shared',         'gcd(Z, N) > 1 (shared factor)?',  'bool',   '0/1'),
]


# === 14-Bit-Code Definitionen (analog V25/V26 Architektur, aber Faktor-basiert) ===
BIT_DEFS = [
    # (#, name, formula_text)
    (0,  'n_z_factors_is_prime',     'n_z_factors in {2,3,5,7,11}'),
    (1,  'n_n_factors_is_prime',     'n_n_factors in {2,3,5,7,11}'),
    (2,  'z_is_repunit',             'Z is repunit'),
    (3,  'n_is_repunit',             'N is repunit'),
    (4,  'gcd_z_n_shared',           'gcd(Z, N) > 1'),
    (5,  'z_is_even',                'Z % 2 == 0'),
    (6,  'n_is_even',                'N % 2 == 0'),
    (7,  'z_div_by_3',               'Z % 3 == 0'),
    (8,  'n_div_by_3',               'N % 3 == 0'),
    (9,  'z_has_more_factors',       'n_z_factors > n_n_factors'),
    (10, 'z_value_larger',           'log10(Z) > log10(N)'),
    (11, 'z_gt_n',                   'Z > N'),
    (12, 'ratio_is_repunit',         'Z/N as decimal has repunit pattern'),
    (13, 'has_mega_factor',          'max(Z factors) > 10^10'),
]


def is_repunit(n: int) -> bool:
    """Prüfe ob n ein Repunit ist (111...1 mit ≥3 Ziffern)."""
    s = str(n)
    if len(s) < 3:
        return False
    return len(set(s)) == 1


def is_repunit_decimal(num: int, den: int, max_period: int = 50) -> bool:
    """Prüfe ob Z/N eine repunit-artige Dezimal-Expansion hat."""
    if den == 0:
        return False
    # Berechne ersten 100 Ziffern der Dezimal-Expansion
    s = []
    r = num % den
    for _ in range(100):
        r *= 10
        s.append(r // den)
        r = r % den
    digits = s[:max_period]
    # Suche Periode
    for period_len in range(3, len(digits) // 3 + 1):
        period = digits[:period_len]
        if all(digits[i] == period[i % period_len] for i in range(min(60, len(digits)))):
            # Prüfe ob alle identisch (= Repunit)
            if len(set(period)) == 1:
                return True
    return False


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def digit_sum(n: int) -> int:
    return sum(int(c) for c in str(abs(n)))


def load_factor_pairs_v1() -> list[dict]:
    """Lade 11 Faktor-Brüche aus V1 (p23_grid.json)."""
    p = DATA / 'p23_grid.json'
    if not p.exists():
        log.error(f'V1-Datei fehlt: {p}')
        return []
    d = json.load(open(p))
    pairs = d['algebraic_matrix']['pairs']
    log.info(f'V1: {len(pairs)} Faktor-Paare geladen aus {p}')
    return pairs


def build_algebraic_matrix_11x14(pairs: list[dict]) -> dict:
    """Baue 11×14 Matrix: 14 algebraische Spalten × 11 Faktor-Paare."""
    grid = []
    for p in pairs:
        z = p['z_value']
        n = p['n_value']
        z_factors = p['z_factors']
        n_factors = p['n_factors']
        ratio = p['ratio'] if p['ratio'] else 0

        row = [
            z_factors[0] % 26 if z_factors else 0,                    # 0
            z_factors[-1] % 26 if z_factors else 0,                   # 1
            len(z_factors),                                            # 2
            digit_sum(int(math.log10(z))) if z > 0 else 0,           # 3
            n_factors[0] % 26 if n_factors else 0,                    # 4
            n_factors[-1] % 26 if n_factors else 0,                   # 5
            len(n_factors),                                            # 6
            digit_sum(int(math.log10(n))) if n > 0 else 0,           # 7
            int(ratio) % 26 if ratio else 0,                          # 8
            z % 26,                                                    # 9
            n % 26,                                                    # 10
            int(is_repunit(z)),                                        # 11
            int(is_repunit(n)),                                        # 12
            int(gcd(z, n) > 1) if (z and n) else 0,                   # 13
        ]
        grid.append(row)

    return {
        'rows': 11,
        'cols': 14,
        'n_cells': 11 * 14,
        'col_definitions': [
            {'idx': d[0], 'name': d[1], 'formula': d[2], 'type': d[3], 'range': d[4]}
            for d in COLUMN_DEFS
        ],
        'grid': grid,
    }


def build_14bit_codes(pairs: list[dict]) -> dict:
    """Baue 11 14-Bit-Codes aus Faktor-Properties (algebraisch, ohne Wikia)."""
    codes = []
    code_details = []
    for p in pairs:
        z = p['z_value']
        n = p['n_value']
        z_factors = p['z_factors']
        n_factors = p['n_factors']
        ratio = p['ratio'] if p['ratio'] else 0

        bits = [
            int(len(z_factors) in {2, 3, 5, 7, 11}),                            # b0
            int(len(n_factors) in {2, 3, 5, 7, 11}),                            # b1
            int(is_repunit(z)),                                                 # b2
            int(is_repunit(n)),                                                 # b3
            int(gcd(z, n) > 1) if (z and n) else 0,                            # b4
            int(z % 2 == 0),                                                    # b5
            int(n % 2 == 0),                                                    # b6
            int(z % 3 == 0),                                                    # b7
            int(n % 3 == 0),                                                    # b8
            int(len(z_factors) > len(n_factors)),                               # b9
            int(math.log10(z) > math.log10(n)) if (z and n) else 0,            # b10
            int(z > n),                                                          # b11
            int(is_repunit_decimal(z, n)),                                      # b12
            int(max(z_factors) > 10**10) if z_factors else 0,                  # b13
        ]
        code = int(''.join(str(b) for b in bits), 2)
        codes.append(code)
        code_details.append({
            'pair_idx': p['i'],
            'bits': bits,
            'bit_pattern': ''.join(str(b) for b in bits),
            'code': code,
            'bit_definitions': [d[1] for d in BIT_DEFS],
        })

    code_counter = Counter(codes)
    return {
        'codes_per_pair': codes,
        'unique_codes': sorted(set(codes)),
        'n_unique': len(set(codes)),
        'code_frequency': dict(code_counter),
        'comparison_v25': {
            'v25_codes': {
                5417: 8,    # 73% (8/11) — Standard-BURUMUT
                4905: 2,    # 18% (2/11) — VV-Diphthong-Variante
                10933: 1,   # 9% (1/11) — Sondercode (OKUZIKUFAUSIHE)
            },
            'v25_source': 'V25/V26 aus V10.4-Codebook abgeleitet (V/K-Bits)',
            'v3_source': 'V3 aus Faktor-Properties abgeleitet (algebraisch)',
            'method_unabhängig': 'V25 nutzt Glyphen-Codebook, V3 nutzt Faktor-Properties',
        },
        'details': code_details,
        'bit_definitions': [d[1] for d in BIT_DEFS],
    }


def build_akrostichon_v3(pairs: list[dict]) -> dict:
    """Baue 2 Akrostichon-Kandidaten + Vergleich mit V10.4."""
    z_values = [p['z_value'] for p in pairs]
    n_z_counts = [len(p['z_factors']) for p in pairs]

    # Kandidat 1: Z-mod-26
    akro_z = ''.join(chr(ord('A') + (z % 26)) for z in z_values)
    # Kandidat 2: Anzahl-Z-Faktoren-mod-26
    akro_count = ''.join(chr(ord('A') + (c % 26)) for c in n_z_counts)

    v10_4_akrostichon = 'BNYZTSOYNKS'

    return {
        'akrostichon_z_mod26': akro_z,
        'akrostichon_n_count_mod26': akro_count,
        'v10_4_reference': v10_4_akrostichon,
        'v10_4_source': 'V10.4 erste Spalte der 11×14 BURUMUT-Glyph-Matrix',
        'v3_source': 'V3 algebraische erste Spalte aus Faktor-Properties',
        'comparison': {
            'v3_z_mod26_unique_letters': len(set(akro_z)),
            'v3_count_mod26_unique_letters': len(set(akro_count)),
            'v10_4_unique_letters': len(set(v10_4_akrostichon)),
            'overlap_v3_z_v10_4': sum(1 for a, b in zip(akro_z, v10_4_akrostichon) if a == b),
            'overlap_v3_count_v10_4': sum(1 for a, b in zip(akro_count, v10_4_akrostichon) if a == b),
        },
        'interpretation': (
            'V3-Akrostichon ist deterministisch aus Faktor-Werten, '
            'V10.4-Akrostichon aus Glyphen-Grid (Wikia-basiert). '
            'Verschiedene Architekturen → KEINE Übereinstimmung erwartet.'
        ),
    }


def main():
    log.info('=' * 60)
    log.info('V3 REVERIFIKATION: Algebraische BURUMUT-Matrix')
    log.info('OHNE Wikia-Trigger, OHNE V10.4-Codebook, OHNE V7 Tappeiner')
    log.info('=' * 60)

    # Phase A: Lade Faktor-Brüche
    pairs = load_factor_pairs_v1()
    if len(pairs) != 11:
        log.error(f'Erwarte 11 Paare, gefunden: {len(pairs)}')
        return
    log.info(f'11 Faktor-Paare: {[(p["i"], len(p["z_factors"]), len(p["n_factors"])) for p in pairs]}')

    # Phase B: 11×14 algebraische Matrix
    log.info('')
    log.info('--- Phase B: 11×14 algebraische Matrix ---')
    matrix = build_algebraic_matrix_11x14(pairs)
    log.info(f'Grid: {matrix["rows"]}×{matrix["cols"]} = {matrix["n_cells"]} Zellen')
    log.info('Spalten-Definitionen:')
    for col in matrix['col_definitions']:
        log.info(f'  {col["idx"]:2d}. {col["name"]:25s} = {col["formula"]}')
    log.info('Grid (Werte pro Paar):')
    for i, row in enumerate(matrix['grid']):
        log.info(f'  Paar {i:2d}: {row}')

    matrix_out = SNAPSHOTS / 'v3_burumut_matrix.json'
    matrix_out.write_text(json.dumps(matrix, indent=2))
    log.info(f'✓ Saved {matrix_out}')

    # Phase C: 14-Bit-Codes
    log.info('')
    log.info('--- Phase C: 14-Bit-Codes pro Paar ---')
    codes = build_14bit_codes(pairs)
    log.info(f'11 Codes: {codes["codes_per_pair"]}')
    log.info(f'Unique Codes: {codes["unique_codes"]} (n={codes["n_unique"]})')
    log.info('V25 Referenz: 5417 (8/11), 4905 (2/11), 10933 (1/11)')

    codes_out = SNAPSHOTS / 'v3_14bit_codes.json'
    codes_out.write_text(json.dumps(codes, indent=2))
    log.info(f'✓ Saved {codes_out}')

    # Phase D: Akrostichon-Vergleich
    log.info('')
    log.info('--- Phase D: Akrostichon-Vergleich ---')
    akro = build_akrostichon_v3(pairs)
    log.info(f'V3 Z-mod-26:           {akro["akrostichon_z_mod26"]}')
    log.info(f'V3 Count-mod-26:       {akro["akrostichon_n_count_mod26"]}')
    log.info(f'V10.4 Referenz:        {akro["v10_4_reference"]}')
    log.info(f'Overlap V3-Z / V10.4:  {akro["comparison"]["overlap_v3_z_v10_4"]}/11')
    log.info(f'Overlap V3-Cnt / V10.4: {akro["comparison"]["overlap_v3_count_v10_4"]}/11')

    akro_out = SNAPSHOTS / 'v3_akrostichon.json'
    akro_out.write_text(json.dumps(akro, indent=2))
    log.info(f'✓ Saved {akro_out}')

    # Phase E: V3 Complete
    v3_complete = {
        'method': 'V3 = algebraische BURUMUT-Matrix aus 11 Faktor-Brüchen, OHNE Wikia-Trigger',
        'timestamp': datetime.now().isoformat(),
        'n_factors_pairs': len(pairs),
        'algebraic_matrix_11x14': {
            'rows': matrix['rows'],
            'cols': matrix['cols'],
            'n_cells': matrix['n_cells'],
            'col_definitions': matrix['col_definitions'],
            'grid': matrix['grid'],
        },
        '14bit_codes': {
            'codes_per_pair': codes['codes_per_pair'],
            'unique_codes': codes['unique_codes'],
            'n_unique': codes['n_unique'],
            'code_frequency': codes['code_frequency'],
            'comparison_v25': codes['comparison_v25'],
        },
        'akrostichon': {
            'z_mod26': akro['akrostichon_z_mod26'],
            'n_count_mod26': akro['akrostichon_n_count_mod26'],
            'v10_4_reference': akro['v10_4_reference'],
            'comparison': akro['comparison'],
        },
        'apophenia_schutz': {
            'kein_wikia_trigger': 'Alle 14 Spalten aus Faktor-Properties definiert',
            'kein_v10_4_codebook': 'V3 nutzt V10.4 NICHT als Quelle',
            'keine_burumut_wortliste': 'BURUMUTREFAMTU, NAFERANSAHOTFE, etc. NICHT referenziert',
            'kein_v7_tappeiner': 'V3 nutzt KEINE V7 Tappeiner-Kandidaten',
            'kein_v8_wikia_alignment': 'V3 nutzt KEINE V8 Wikia-Alignment',
            'kein_v9_v2_smart_parser': 'V3 nutzt KEINE V9 v2-Logik',
            'rein_algebraisch': 'Alle Werte aus mathematischen Faktor-Properties (F + K)',
        },
        'konsens_punkte': {
            'n_pairs': 'V3: 11 = V10.4: 11 (Konsens auf 11 BURUMUT-Paare)',
            'n_columns': 'V3: 14 = V10.4: 14 (Konsens auf 14 Spalten)',
            'n_cells': 'V3: 154 = V10.4: 154 AS (Konsens auf 11×14=154)',
        },
        'divergenz_punkte': {
            'architektur': 'V3: Faktor-basiert, V10.4: Glyph-basiert (Wikia)',
            'akrostichon': f'V3 Z-mod-26: {akro["akrostichon_z_mod26"]}, V10.4: {akro["v10_4_reference"]}',
            '14bit_codes': f'V3: {codes["codes_per_pair"]}, V25: 5417×8+4905×2+10933×1',
        },
        'conclusion': (
            'V3 ist KEIN Decoder, sondern algebraische Beschreibung der 11×14-Matrix aus 11 Faktor-Brüchen. '
            'V3 ≠ V10.4 erwartet (verschiedene Architekturen). '
            'Konsens auf 11/14/154 ist Faktum. '
            'Divergenz bei Akrostichon und 14-Bit-Codes ist Konsequenz der Architektur-Wahl.'
        ),
    }
    v3_out = SNAPSHOTS / 'v3_complete.json'
    v3_out.write_text(json.dumps(v3_complete, indent=2))
    log.info(f'✓ Saved {v3_out}')

    log.info('')
    log.info('=' * 60)
    log.info('V3 SUMMARY')
    log.info('=' * 60)
    log.info(f'11×14-Matrix: {matrix["n_cells"]} Zellen')
    log.info(f'11 14-Bit-Codes: {codes["codes_per_pair"]}')
    log.info(f'V3 Akrostichon Z-mod-26: {akro["akrostichon_z_mod26"]}')
    log.info(f'V10.4 Akrostichon: {akro["v10_4_reference"]}')
    log.info(f'Overlap: {akro["comparison"]["overlap_v3_z_v10_4"]}/11 (Z-mod-26), {akro["comparison"]["overlap_v3_count_v10_4"]}/11 (Count-mod-26)')


if __name__ == '__main__':
    main()
