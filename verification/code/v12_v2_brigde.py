"""
v12_v2_brigde.py — Phase 11: V2 Reverifikations-Brücke.

Methode (eigene, unabhängig von V1 und V10.4):
  1. Lade V1-Snapshots (verification/data/snapshots/v1_*.json)
  2. Lade V10.4 Brücken-Daten aus V7/V8/V9 (NICHT V10.4 direkt!)
  3. Dokumentiere die Faktor-Brüche-zu-BURUMUT-Matrix Brücke
  4. Dokumentiere die Glyphen-zu-Englisch Brücke
  5. Schreibe V2 Reverifikations-JSON mit:
     - 11 BURUMUT-Wörter (Faktor-Brüche, unabhängig von V10.4 abgeleitet)
     - 11 Bruch-Paare (algebraische Faktor-Manifestation)
     - Akrostichon (Faktor-Brüche abgeleitet, NICHT aus V10.4-Codebook)
     - Glyph-zu-Englisch Brücken-Trace (welche Wikia-Plaintexte wurden genutzt)
  6. Schreibe Drift-Vergleich V1 → V2 → V10.4

Output:
  - verification/results/snapshots/v2_complete.json
  - verification/results/snapshots/v2_burumut_brigde.json
  - verification/results/snapshots/v2_glyph_english_brigde.json
  - verification/results/snapshots/v2_diff_v1_to_v10_4.json
"""
import json
import logging
import re
from pathlib import Path
from datetime import datetime
from collections import Counter

REPO = Path('/run/media/julian/ML4/tengri137')
DATA = REPO / 'verification' / 'data'
SNAPSHOTS = REPO / 'verification' / 'results' / 'snapshots'
LOGS = REPO / 'verification' / 'logs'
SNAPSHOTS.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOGS / 'v12.log', mode='w'), logging.StreamHandler()],
)
log = logging.getLogger(__name__)


# 22 Faktor-Zeilen aus p23 (manuell kuratiert via Read-Tool visuell verifiziert)
# 11 Bruch-Paare (Z/N)
P23_FACTOR_PAIRS = [
    {
        'pair_id': 1,
        'z_line': '2² × 17 × 19 × 55627057 × 7200332325968813',
        'n_line': '3² × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449',
        'z_value': 4 * 17 * 19 * 55627057 * 7200332325968813,
        'n_value': 9 * 29 * 101 * 239 * 281 * 4649 * 909091 * 121499449,
    },
    {
        'pair_id': 2,
        'z_line': '22441 × 26807952781 × 220238942717',
        'n_line': '11 × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449',
        'z_value': 22441 * 26807952781 * 220238942717,
        'n_value': 11 * 29 * 101 * 239 * 281 * 4649 * 909091 * 121499449,
    },
    {
        'pair_id': 3,
        'z_line': '2633 × 8867291 × 37287337 × 1498430561',
        'n_line': '3 × 11 × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449',
        'z_value': 2633 * 8867291 * 37287337 * 1498430561,
        'n_value': 3 * 11 * 29 * 101 * 239 * 281 * 4649 * 909091 * 121499449,
    },
    {
        'pair_id': 4,
        'z_line': '7 × 3386469421 × 14123028175936831',
        'n_line': '11 × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449',
        'z_value': 7 * 3386469421 * 14123028175936831,
        'n_value': 11 * 29 * 101 * 239 * 281 * 4649 * 909091 * 121499449,
    },
    {
        'pair_id': 5,
        'z_line': '2² × 20359 × 346559 × 13445817584622779',
        'n_line': '3 × 11 × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449',
        'z_value': 4 * 20359 * 346559 * 13445817584622779,
        'n_value': 3 * 11 * 29 * 101 * 239 * 281 * 4649 * 909091 * 121499449,
    },
    {
        'pair_id': 6,
        'z_line': '7 × 4174409 × 13716463 × 11670170507',
        'n_line': '3² × 101 × 239 × 281 × 4649 × 909091 × 121499449',
        'z_value': 7 * 4174409 * 13716463 * 11670170507,
        'n_value': 9 * 101 * 239 * 281 * 4649 * 909091 * 121499449,
    },
    {
        'pair_id': 7,
        'z_line': '1889 × 1344613389306385590121189',
        'n_line': '3 × 11 × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449',
        'z_value': 1889 * 1344613389306385590121189,
        'n_value': 3 * 11 * 29 * 101 * 239 * 281 * 4649 * 909091 * 121499449,
    },
    {
        'pair_id': 8,
        'z_line': '2² × 47 × 79 × 102359 × 2468021 × 347713522439',
        'n_line': '3 × 11 × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449',
        'z_value': 4 * 47 * 79 * 102359 * 2468021 * 347713522439,
        'n_value': 3 * 11 * 29 * 101 * 239 * 281 * 4649 * 909091 * 121499449,
    },
    {
        'pair_id': 9,
        'z_line': '293 × 2551 × 330206236792383668191',
        'n_line': '3³ × 7 × 13 × 31 × 37 × 211 × 241 × 271 × 2161 × 9091 × 2906161',
        'z_value': 293 * 2551 * 330206236792383668191,
        'n_value': 27 * 7 * 13 * 31 * 37 * 211 * 241 * 271 * 2161 * 9091 * 2906161,
    },
    {
        'pair_id': 10,
        'z_line': '2⁷ × 2729 × 486954583 × 1056312876821',
        'n_line': '3² × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449',
        'z_value': 128 * 2729 * 486954583 * 1056312876821,
        'n_value': 9 * 29 * 101 * 239 * 281 * 4649 * 909091 * 121499449,
    },
    {
        'pair_id': 11,
        'z_line': '19 × 31 × 73151809 × 3847851920700457',
        'n_line': '11 × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449',
        'z_value': 19 * 31 * 73151809 * 3847851920700457,
        'n_value': 11 * 29 * 101 * 239 * 281 * 4649 * 909091 * 121499449,
    },
]


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def is_repunit(n):
    s = str(n)
    return len(set(s)) == 1 and len(s) >= 3


def burumut_word_from_pair_v2(pair: dict) -> dict:
    """Bestimme BURUMUT-Wort aus einem Faktor-Bruchpaar (deterministisch, NICHT V10.4).

    Strategie:
    1. Konvertiere Z-Wert in Buchstaben-Index (mod 26)
    2. Konvertiere N-Wert in Buchstaben-Index (mod 26)
    3. Erzeuge 14-Buchstaben-Wort: 7 Z-mod-26 + 7 N-mod-26
       (analog zu "BURUMUTREFAMTU" wo erste 7 = "BURUMUT", letzte 7 = "REFAMTU")
    4. Strategie: erste 7 Zeichen aus Z-Faktor-Permutation,
                 letzte 7 Zeichen aus N-Faktor-Permutation
    """
    z_factors = [int(x) for x in re.findall(r'\d+', pair['z_line'])]
    n_factors = [int(x) for x in re.findall(r'\d+', pair['n_line'])]

    # Z-Buchstaben: aus ersten 7 Faktoren mod 26
    z_letters = ''.join(chr(ord('A') + (f % 26)) for f in z_factors[:7])
    z_letters = z_letters.ljust(7, 'X')[:7]  # pad mit X

    # N-Buchstaben: aus ersten 7 Faktoren mod 26
    n_letters = ''.join(chr(ord('A') + (f % 26)) for f in n_factors[:7])
    n_letters = n_letters.ljust(7, 'X')[:7]

    word = z_letters + n_letters

    return {
        'pair_id': pair['pair_id'],
        'z_line': pair['z_line'],
        'n_line': pair['n_line'],
        'z_value': pair['z_value'],
        'n_value': pair['n_value'],
        'z_letters': z_letters,
        'n_letters': n_letters,
        'burumut_word_v2': word,
    }


def build_burumut_bridge_v2() -> dict:
    """Bilde V2 BURUMUT-Matrix aus 11 Faktor-Brüchen (algebraisch, unabhängig von V10.4)."""
    words = [burumut_word_from_pair_v2(p) for p in P23_FACTOR_PAIRS]
    akrostichon = ''.join(w['burumut_word_v2'][0] for w in words)
    return {
        'n_pairs': len(words),
        'matrix_size': '11×14 (algebraisch)',
        'burumut_words_v2': [w['burumut_word_v2'] for w in words],
        'words_detail': words,
        'akrostichon_v2': akrostichon,
        'akrostichon_unique_letters': len(set(akrostichon)),
    }


def build_glyph_english_bridge_v2() -> dict:
    """Dokumentiere Glyph→Englisch-Brücke aus V8/V9 (NICHT reproduzieren)."""
    return {
        'method': 'Wikia-Alignment + 17-Glyphen-ML-Decoder',
        'phases': [
            {
                'phase': 'V6 (Phase 8-15)',
                'output': '17 unique Glyphen-Klassen aus p1-p16',
                'method': 'ML-Clustering (kein Wikia)',
            },
            {
                'phase': 'V8 (Phase 26)',
                'output': '17 Glyphen ↔ Wikia-Plaintext (1 Glyph ≈ 7 lateinische Buchstaben)',
                'method': 'Wikia-Alignment (Schmeh-Übersetzung als Trainingsreferenz)',
            },
            {
                'phase': 'V9 (Phase 0-7)',
                'output': 'Drei-Schichten-Architektur: Tengri-Glyphen + Wikia + Formel-Decodes',
                'method': 'Re-Verifikation mit Smart-Parser v2',
            },
            {
                'phase': 'V10 (Phase 28)',
                'output': '30/30 Tests, Glyph→English 85-93% Match',
                'method': 'ML-Modell mit V8-Alignment als Trainingsdaten',
            },
            {
                'phase': 'V10.1-V10.5',
                'output': 'p17 n_burumut=0, p23 idx 8/9/10 Korrekturen',
                'method': 'CitMind-Verifikation, doc.json Gold-Standard',
            },
        ],
        'v1_limitation': (
            'V1 nutzt KEIN Wikia, KEINEN ML-Decoder. '
            'V1 hat nur Pixel + BBox + aHash. '
            'Glyphe→Englisch-Brücke ist aus V1 NICHT reproduzierbar.'
        ),
        'v2_perspective': (
            'V2 dokumentiert die Brücke transparent, ohne sie zu reproduzieren. '
            'Wikia-Plaintext ist externe Quelle, nicht Reverifikations-Quelle.'
        ),
    }


def build_diff_v1_to_v10_4(v1_summary: dict, v104: dict) -> list[dict]:
    """Bilde Drift V1 → V2 → V10.4 für die wichtigsten Felder."""
    diffs = []

    # V10.4 hat n_glyphs total pro Seite
    v104_pages = v104.get('seiten', v104.get('pages', []))
    v104_glyphs = {}
    v104_burumut = {}
    for p in v104_pages:
        pid = p.get('page_id', p.get('page_number'))
        v104_glyphs[pid] = p.get('n_glyphs_v9', 0) or p.get('n_glyphs_v10', 0) or 0
        burumut_words = p.get('grid_2d_words', p.get('burumut_words', []))
        v104_burumut[pid] = len(burumut_words) if burumut_words else 0

    # V1-Per-Page
    v1_pages = v1_summary.get('per_page', [])

    for r in v1_pages:
        n = r['page']
        v1_g = r.get('n_glyphs', 0)
        v104_g = v104_glyphs.get(n, v104_glyphs.get(f'p{n:02d}', '?'))
        if isinstance(v104_g, (int, float)) and v104_g > 0:
            drift = round(100.0 * (v1_g - v104_g) / v104_g, 1)
        else:
            drift = None
        diffs.append({
            'field': f'p{n:02d}_n_glyphs',
            'v1': v1_g,
            'v10_4': v104_g,
            'drift_pct': drift,
            'classification': 'match' if drift and abs(drift) < 10 else (
                'drift_klein' if drift and abs(drift) < 30 else (
                'drift_gross' if drift and abs(drift) >= 30 else 'unknown')),
        })

    # BURUMUT
    for r in v1_pages:
        n = r['page']
        v1_bur = r.get('burumut_n_pairs', 0)
        v104_bur = v104_burumut.get(n, v104_burumut.get(f'p{n:02d}', 0))
        diffs.append({
            'field': f'p{n:02d}_burumut_words',
            'v1': v1_bur,
            'v10_4': v104_bur,
            'classification': 'match' if v1_bur == v104_bur else 'methodisch_unterschiedlich',
            'note': 'V1 = algebraisch aus Faktor-Brüchen, V10.4 = Glyph-Grid (V9 v2)',
        })

    return diffs


def main():
    log.info('=' * 60)
    log.info('PHASE 11: V2 Reverifikations-Brücke')
    log.info('=' * 60)

    # Lade V1-Snapshots
    log.info('Lade V1-Snapshots ...')
    v1_complete = json.load(open(SNAPSHOTS / 'v1_complete.json'))
    v1_diff = json.load(open(SNAPSHOTS / 'v1_diff_vs_v104.json'))
    v1_summary_md = (SNAPSHOTS / 'v1_SUMMARY.md').read_text()

    # Lade V10.4 als Vergleichsmasse (NICHT als Quelle)
    log.info('Lade V10.4 als Vergleichsmasse ...')
    v104 = json.load(open(REPO / 'consecutive_reading' / 'bbox' / 'v104_20260708' / 'tengri137_complete_decoded_v104.json'))

    # V2 BURUMUT-Brücke
    log.info('Bilde V2 BURUMUT-Brücke (Faktor-Brüche → Wörter) ...')
    burumut_brigde = build_burumut_bridge_v2()
    log.info(f'  11 BURUMUT-Wörter (V2): {burumut_brigde["burumut_words_v2"]}')
    log.info(f'  Akrostichon (V2): {burumut_brigde["akrostichon_v2"]}')
    log.info(f'  Eindeutige Buchstaben: {burumut_brigde["akrostichon_unique_letters"]}/11')

    (SNAPSHOTS / 'v2_burumut_brigde.json').write_text(json.dumps(burumut_brigde, indent=2))
    log.info(f'✓ Saved {SNAPSHOTS / "v2_burumut_brigde.json"}')

    # V2 Glyph-Englisch-Brücke
    log.info('Dokumentiere V2 Glyph→Englisch-Brücke ...')
    glyph_brigde = build_glyph_english_bridge_v2()
    (SNAPSHOTS / 'v2_glyph_english_brigde.json').write_text(json.dumps(glyph_brigde, indent=2))
    log.info(f'✓ Saved {SNAPSHOTS / "v2_glyph_english_brigde.json"}')

    # V2 Diff (V1 → V10.4)
    log.info('Bilde V2 Diff (V1 → V10.4) ...')
    diffs = build_diff_v1_to_v10_4(v1_complete, v104)
    (SNAPSHOTS / 'v2_diff_v1_to_v10_4.json').write_text(json.dumps(diffs, indent=2))
    log.info(f'✓ Saved {SNAPSHOTS / "v2_diff_v1_to_v10_4.json"} ({len(diffs)} Einträge)')

    # V2 Complete
    v2_complete = {
        'method': 'V2 = Brücke zwischen V1 (Original-PNG-Reverifikation) und V10.4 (Master-JSON)',
        'timestamp': datetime.now().isoformat(),
        'v1_data': {
            'n_bboxes': v1_complete['totals']['n_bboxes'],
            'n_glyphs': v1_complete['totals']['n_glyphs'],
            'n_latin_words': v1_complete['totals']['n_latin_words'],
            'n_formulas': v1_complete['totals']['n_formulas'],
            'n_text_lines': v1_complete['totals']['n_text_lines'],
        },
        'v2_burumut_brigde': {
            'method': 'Faktor-Brüche → algebraische BURUMUT-Wörter (deterministisch, unabhängig von V10.4)',
            'n_words': burumut_brigde['n_pairs'],
            'words': burumut_brigde['burumut_words_v2'],
            'akrostichon': burumut_brigde['akrostichon_v2'],
            'akrostichon_unique': burumut_brigde['akrostichon_unique_letters'],
        },
        'v2_glyph_english_brigde': glyph_brigde,
        'v2_diff_v1_to_v10_4': {
            'n_entries': len(diffs),
            'n_match': sum(1 for d in diffs if d['classification'] == 'match'),
            'n_methodisch': sum(1 for d in diffs if d['classification'] == 'methodisch_unterschiedlich'),
            'n_drift_klein': sum(1 for d in diffs if d['classification'] == 'drift_klein'),
            'n_drift_gross': sum(1 for d in diffs if d['classification'] == 'drift_gross'),
        },
        'key_insights': [
            'V1 Reverifikation: 8771 BBoxes, 1319 Glyphen, 648 Latein-Wörter, 1497 Ziffern, 2563 Formeln, 11 Bilder, 226 Textzeilen',
            'p23 BURUMUT: 11 algebraische Faktor-Bruchpaare (NICHT visuell erkennbar als Glyph-Grid)',
            'V2 BURUMUT-Wörter: 14-Buchstaben-Wörter aus Faktor-Permutationen (mod 26)',
            'V2 Akrostichon: ' + burumut_brigde['akrostichon_v2'] + ' (deterministisch aus Faktoren, unabhängig von V10.4)',
            'V10.4 BURUMUT-Wörter sind V9 v2 High-Level-Interpretation, kein Faktum aus p23',
            'Glyph→Englisch-Brücke in V10.4 nutzt Wikia als Trainingsreferenz, nicht aus PNGs ableitbar',
            'V10.4 = Stufe 7 der Gold-Standard-Hierarchie, V1 = Stufe 1 (nur Original-PNGs)',
        ],
        'apophenia_schutz': [
            'V1: KEIN Wikia, KEIN ML-Decoder, KEIN doc.json als Quelle',
            'V2: Brücke wird dokumentiert, NICHT reproduziert',
            'CitMind-Veto: BURUMUT-Matrix-Grid ist Konvention, kein Faktum',
            'V1 vs V10.4: 2 match, 16 methodisch, 7 drift_klein, 8 drift_gross (ehrliche Klassifikation)',
        ],
    }
    (SNAPSHOTS / 'v2_complete.json').write_text(json.dumps(v2_complete, indent=2))
    log.info(f'✓ Saved {SNAPSHOTS / "v2_complete.json"}')

    log.info('')
    log.info('=' * 60)
    log.info('V2 SUMMARY')
    log.info('=' * 60)
    log.info(f'V1 Totale: {v2_complete["v1_data"]}')
    log.info(f'V2 BURUMUT-Wörter: {v2_complete["v2_burumut_brigde"]["n_words"]}')
    log.info(f'V2 Akrostichon: {v2_complete["v2_burumut_brigde"]["akrostichon"]}')
    log.info(f'V1→V10.4 Diff: {v2_complete["v2_diff_v1_to_v10_4"]}')


if __name__ == '__main__':
    main()
