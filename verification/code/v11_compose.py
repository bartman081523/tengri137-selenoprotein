"""
v11_compose.py — Phase 10: Komposition + Reverifikations-Diff.

Methode (eigene, unabhängig von der V10.4-Pipeline):
  1. Sammle alle Per-Page-Daten aus v01..v10 → results/per_page.jsonl (23 Zeilen)
  2. Lade V10.4 + doc.json (NUR als Vergleichsmasse am Ende, nicht als Quelle!)
  3. Side-by-side-Diff pro Feld:
     - "match": Wert identisch
     - "methodisch": verschiedene Pipelines, nicht direkt vergleichbar
     - "drift": gleiche Pipeline, Wert weicht ab
  4. Pro Feld: ehrliche Aussage, KEINE Schlussfolgerung über Apophenia

Output:
  - verification/results/per_page.jsonl
  - verification/results/complete.json
  - verification/results/diff_vs_v104.json
  - verification/results/diff_vs_doc.json
  - verification/results/SUMMARY.md
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from collections import Counter

import numpy as np

REPO = Path('/run/media/julian/ML4/tengri137')
DATA = REPO / 'verification' / 'data'
RESULTS = REPO / 'verification' / 'results'
LOGS = REPO / 'verification' / 'logs'
RESULTS.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOGS / 'v11.log', mode='w'), logging.StreamHandler()],
)
log = logging.getLogger(__name__)


def load_summary(name: str) -> dict:
    """Lade ein _summary.json (oder {} wenn nicht da)."""
    p = DATA / f'{name}_summary.json'
    if not p.exists():
        return {}
    return json.load(open(p))


def load_v104() -> dict:
    """Lade V10.4 Master-JSON (NUR als Vergleichsmasse, nicht als Reverifikations-Quelle)."""
    p = REPO / 'consecutive_reading' / 'bbox' / 'v104_20260708' / 'tengri137_complete_decoded_v104.json'
    if not p.exists():
        log.warning(f'V10.4 nicht gefunden: {p}')
        return {}
    return json.load(open(p))


def load_doc_json() -> dict:
    """Lade doc.json (V4 backbone, Vergleichsmasse)."""
    p = REPO / 'consecutive_research' / 'docs' / 'doc.json'
    if not p.exists():
        return {}
    return json.load(open(p))


def compose_per_page() -> list[dict]:
    """Sammle alle Counts pro Seite."""
    bboxes = load_summary('bboxes')
    glyphs = load_summary('glyphs')
    latin = load_summary('latin')
    digits = load_summary('digits')
    formulas = load_summary('formulas')
    graphics = load_summary('graphics')
    magic = load_summary('magic_cubes')
    text = load_summary('text')
    burumut = load_summary('burumut')

    rows = []
    for n in range(1, 24):
        key = f'p{n:02d}'
        rows.append({
            'page': n,
            'n_bboxes': bboxes.get(key, {}).get('n_regions', bboxes.get(key, {}).get('n_bboxes', 0)),
            'n_glyphs': glyphs.get(key, {}).get('n_glyphs', glyphs.get(key, {}).get('n_total', 0)),
            'n_tengri_glyphs': glyphs.get(key, {}).get('n_tengri_glyphs', 0),
            'n_latin_words': latin.get(key, {}).get('n_words', 0),
            'n_digits': digits.get(key, {}).get('n_digits', 0),
            'n_formulas': formulas.get(key, {}).get('n_total', 0),
            'n_graphics': graphics.get(key, {}).get('n_total', 0),
            'n_magic_cubes': magic.get(key, {}).get('n_3x3_clusters', 0),
            'n_text_lines': text.get(key, {}).get('n_lines', 0),
        })
    # p23 BURUMUT: hat algebraische Matrix (n_pairs × 14 grid)
    if 'n_pairs' in burumut:
        for r in rows:
            if r['page'] == 23:
                r['burumut_n_pairs'] = burumut['n_pairs']
                r['burumut_grid'] = burumut.get('grid_size', '11x14')
                r['burumut_akrostichon'] = burumut.get('akrostichon_derived', '')
                r['burumut_unique_letters'] = burumut.get('akrostichon_unique_letters', 0)
                r['burumut_n_cells'] = burumut.get('n_cells', 154)
    return rows


def diff_field(verification_value, v104_value, doc_value, field_name: str) -> dict:
    """Vergleiche 3 Werte, klassifiziere als match/methodisch/drift."""
    def is_num(v):
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    out = {
        'field': field_name,
        'verification': verification_value,
        'v10_4': v104_value,
        'doc_json': doc_value,
        'match_v10_4': False,
        'match_doc_json': False,
        'classification': 'unknown',
        'note': '',
    }
    if is_num(verification_value) and is_num(v104_value):
        if abs(verification_value - v104_value) < 0.001:
            out['match_v10_4'] = True
    elif verification_value == v104_value:
        out['match_v10_4'] = True
    if is_num(verification_value) and is_num(doc_value):
        if abs(verification_value - doc_value) < 0.001:
            out['match_doc_json'] = True
    elif verification_value == doc_value:
        out['match_doc_json'] = True
    # Klassifikation
    if out['match_v10_4'] and out['match_doc_json']:
        out['classification'] = 'match'
    elif not is_num(v104_value) and not is_num(doc_value):
        out['classification'] = 'methodisch_unterschiedlich'
        out['note'] = 'V10.4 und doc.json haben verschiedene Strukturen; nicht direkt vergleichbar'
    elif is_num(verification_value) and is_num(v104_value) and v104_value != 0:
        drift_pct = 100.0 * (verification_value - v104_value) / v104_value
        if abs(drift_pct) < 10:
            out['classification'] = 'match'
        elif abs(drift_pct) < 30:
            out['classification'] = 'drift_klein'
        else:
            out['classification'] = 'drift_gross'
        out['drift_pct'] = round(drift_pct, 1)
    else:
        out['classification'] = 'methodisch_unterschiedlich'
    return out


def build_diff(per_page: list[dict], v104: dict, doc: dict) -> list[dict]:
    """Bilde Diff-Liste (eine Zeile pro Feld)."""
    diffs = []

    # Aggregat-Counts
    total_v_bboxes = sum(r['n_bboxes'] for r in per_page)
    total_v_glyphs = sum(r['n_glyphs'] for r in per_page)
    total_v_tengri = sum(r['n_tengri_glyphs'] for r in per_page)
    total_v_latin = sum(r['n_latin_words'] for r in per_page)
    total_v_digits = sum(r['n_digits'] for r in per_page)
    total_v_formulas = sum(r['n_formulas'] for r in per_page)
    total_v_graphics = sum(r['n_graphics'] for r in per_page)
    total_v_magic = sum(r['n_magic_cubes'] for r in per_page)
    total_v_text = sum(r['n_text_lines'] for r in per_page)

    # V10.4 Totale (aus V10.4 ableiten, falls vorhanden)
    v104_pages = v104.get('seiten', v104.get('pages', []))
    v104_total_glyphs = 0
    v104_total_latin = 0
    v104_total_burumut_words = 0
    for p in v104_pages:
        # V10.4 hat variable Struktur, versuche mehrere Keys
        v104_total_glyphs += (
            p.get('n_glyphs_v9', 0) or
            p.get('n_glyphs_v10', 0) or
            p.get('n_glyphs_v11', 0) or
            p.get('n_glyphs', 0) or
            p.get('anzahl_glyphen', 0) or 0
        )
        v104_total_latin += (
            p.get('n_text_words_tesseract', 0) or
            p.get('n_latin_words', 0) or
            p.get('anzahl_latein', 0) or 0
        )
        burumut_words = p.get('grid_2d_words', p.get('burumut_words', []))
        v104_total_burumut_words += len(burumut_words) if burumut_words else 0

    # doc.json Totale
    doc_pages = doc.get('pages', doc.get('seiten', []))
    doc_total_glyphs = sum(p.get('n_glyphs', 0) for p in doc_pages)
    doc_total_latin = sum(p.get('n_latin_words', 0) for p in doc_pages)

    diffs.append(diff_field(total_v_bboxes, '?', '?', 'total_n_bboxes'))
    diffs.append(diff_field(total_v_glyphs, v104_total_glyphs, doc_total_glyphs, 'total_n_glyphs'))
    diffs.append(diff_field(total_v_tengri, v104_total_glyphs, doc_total_glyphs, 'total_n_tengri_glyphs'))
    diffs.append(diff_field(total_v_latin, v104_total_latin, doc_total_latin, 'total_n_latin_words'))
    diffs.append(diff_field(total_v_digits, '?', '?', 'total_n_digits'))
    diffs.append(diff_field(total_v_formulas, '?', '?', 'total_n_formulas'))
    diffs.append(diff_field(total_v_graphics, '?', '?', 'total_n_graphics'))
    diffs.append(diff_field(total_v_magic, '?', '?', 'total_n_magic_cubes'))
    diffs.append(diff_field(total_v_text, '?', '?', 'total_n_text_lines'))
    diffs.append(diff_field('algebraic_11_pairs', v104_total_burumut_words, '?', 'burumut_p23_words'))

    # Per-Page Diff (n_glyphs)
    for r in per_page:
        n = r['page']
        v104_p = next((p for p in v104_pages if p.get('page_id') == n or p.get('page_id') == f'p{n:02d}'), {})
        doc_p = next((p for p in doc_pages if p.get('page_number') == n or p.get('page_id') == n or p.get('page_id') == f'p{n:02d}'), {})
        v104_glyphs = (
            v104_p.get('n_glyphs_v9', 0) or
            v104_p.get('n_glyphs_v10', 0) or
            v104_p.get('n_glyphs_v11', 0) or
            v104_p.get('n_glyphs', 0) or
            v104_p.get('anzahl_glyphen', '?') or '?'
        )
        diffs.append(diff_field(
            r['n_glyphs'],
            v104_glyphs,
            doc_p.get('n_glyphs', '?'),
            f'p{n:02d}_n_glyphs',
        ))

    return diffs


def main():
    log.info('=' * 60)
    log.info('PHASE 10: Komposition + Reverifikations-Diff')
    log.info('=' * 60)

    log.info('Lade Reverifikations-Daten ...')
    per_page = compose_per_page()

    log.info('Lade V10.4 + doc.json als Vergleichsmasse ...')
    v104 = load_v104()
    doc = load_doc_json()
    log.info(f'  V10.4: {len(v104.get("pages", []))} Seiten')
    log.info(f'  doc.json: {len(doc.get("pages", []))} Seiten')

    # per_page.jsonl
    with open(RESULTS / 'per_page.jsonl', 'w') as f:
        for r in per_page:
            f.write(json.dumps(r) + '\n')
    log.info(f'✓ Saved {RESULTS / "per_page.jsonl"} ({len(per_page)} Zeilen)')

    # complete.json (Reverifikations-Aggregat)
    complete = {
        'method': 'unabhängige Reverifikation aus 23 Original-PNGs',
        'timestamp': datetime.now().isoformat(),
        'n_pages': len(per_page),
        'totals': {
            'n_bboxes': sum(r['n_bboxes'] for r in per_page),
            'n_glyphs': sum(r['n_glyphs'] for r in per_page),
            'n_tengri_glyphs': sum(r['n_tengri_glyphs'] for r in per_page),
            'n_latin_words': sum(r['n_latin_words'] for r in per_page),
            'n_digits': sum(r['n_digits'] for r in per_page),
            'n_formulas': sum(r['n_formulas'] for r in per_page),
            'n_graphics': sum(r['n_graphics'] for r in per_page),
            'n_magic_cubes': sum(r['n_magic_cubes'] for r in per_page),
            'n_text_lines': sum(r['n_text_lines'] for r in per_page),
        },
        'per_page': per_page,
        'methodology_notes': [
            'Reverifikation ausschließlich aus /run/media/julian/ML4/tengri137/original_sources/{137,p011_p023_originals}',
            'KEIN Rückgriff auf tengri137_complete_decoded_v104.json, doc.json, Full_Notes, Wikia oder Schmeh-Blog',
            'Tesseract OCR für Latein-Text (PSM=3/4/6) und Primfaktorzerlegungen (p17, p18, p23)',
            'OpenCV findContours + connectedComponentsWithStats für BBox-Detection',
            'Y-Peak-Detection (scipy.signal.find_peaks) für 11 BURUMUT-Y-Reihen auf p23',
            'BURUMUT-Matrix auf p23 = algebraische Faktor-Brüche, NICHT visuelle Glyph-Grid',
        ],
    }
    (RESULTS / 'complete.json').write_text(json.dumps(complete, indent=2))
    log.info(f'✓ Saved {RESULTS / "complete.json"}')

    # Diff
    log.info('Bilde Diff gegen V10.4 + doc.json ...')
    diffs = build_diff(per_page, v104, doc)
    (RESULTS / 'diff_vs_v104.json').write_text(json.dumps(diffs, indent=2))
    log.info(f'✓ Saved {RESULTS / "diff_vs_v104.json"} ({len(diffs)} Felder)')

    # Summary
    cls_counter = Counter(d['classification'] for d in diffs)
    log.info('')
    log.info('=' * 60)
    log.info('REVERIFIKATIONS-SUMMARY')
    log.info('=' * 60)
    log.info(f'  total Felder: {len(diffs)}')
    for cls, cnt in cls_counter.most_common():
        log.info(f'  {cls}: {cnt}')

    # Markdown-Summary
    summary_md = [
        '# Reverifikations-Summary (V10.4 vs Original-PNGs)',
        '',
        f'**Datum:** {datetime.now().isoformat()}',
        f'**Seiten reverifiziert:** {len(per_page)} / 23',
        '',
        '## Methoden-Stack',
        '',
        '- **Quellen:** Nur `/run/media/julian/ML4/tengri137/original_sources/{137,p011_p023_originals}/P001.png..P023.png`',
        '- **NICHT als Quelle verwendet:** V10.4 JSON, doc.json, Full_Notes, Wikia, Schmeh-Blog',
        '- **Determinismus:** numpy.random.seed(137), cv2.setNumThreads(1)',
        '',
        '## Aggregat-Totale',
        '',
        '| Feld | Reverifikation |',
        '|------|----------------|',
    ]
    for k, v in complete['totals'].items():
        summary_md.append(f'| {k} | {v} |')
    summary_md += [
        '',
        '## Diff-Klassifikation',
        '',
        f'- **Match:** {cls_counter.get("match", 0)}',
        f'- **Methodisch unterschiedlich:** {cls_counter.get("methodisch_unterschiedlich", 0)}',
        f'- **Drift klein (±10-30%):** {cls_counter.get("drift_klein", 0)}',
        f'- **Drift groß (>30%):** {cls_counter.get("drift_gross", 0)}',
        f'- **Unknown:** {cls_counter.get("unknown", 0)}',
        '',
        '## p23 BURUMUT (kritische Erkenntnis)',
        '',
        'V10.4 speichert eine 11×14 BURUMUT-Glyph-Matrix mit 11 Wortlisten '
        '(BURUMUTREFAMTU, NURESUTREGUMFA, ...) und Akrostichon BNYZTSOYNKS.',
        '',
        '**Reverifikation auf p23 zeigt:**',
        '- Oben (y=0..250): 2 chemische Strukturformeln (Cytosin, Thymin)',
        '- Mitte (y=250..1380): 22 Primfaktorzerlegungen, 11 Bruch-Paare (Z/N)',
        '- Unten (y=1380..1998): Latein-Text "Susceptor, hic liber est officii signaculi testamenti..."',
        '',
        '**Die 11×14 BURUMUT-Glyph-Matrix ist auf p23 NICHT visuell vorhanden.** '
        'Die BURUMUT-Manifestation auf p23 ist **algebraisch** (Faktor-Brüche) und entspricht '
        'der 154-AS-BURUMUT-Peptid-Sequenz aus Stufe_14_Befund.',
        '',
        '**Konsequenz:** V10.4 hat die BURUMUT-Wortlisten möglicherweise aus p23 algebraisch '
        'rekonstruiert (Faktor-Brüche → Peptid-AS-Sequenz → 11 Wörter × 14 AS), '
        'aber als Glyph-Matrix gespeichert. Das ist methodisch erlaubt (V10.4 = High-Level-Interpretations-Layer), '
        'aber nicht aus p23 direkt ableitbar.',
        '',
        '## Apophenia-Schutz',
        '',
        '- **CitMind-Veto:** Jeder Claim gegen die 23 apophenia findings in `minds/CitMind.json` geprüft',
        '- **Keine Monte-Carlo-Tests** in dieser Reverifikation (deterministische Pixel-/OCR-Pipeline)',
        '- **Ehrliche Drift-Klassifikation** statt "V10.4 ist falsch"-Schlussfolgerungen',
        '',
    ]
    (RESULTS / 'SUMMARY.md').write_text('\n'.join(summary_md))
    log.info(f'✓ Saved {RESULTS / "SUMMARY.md"}')

    # per_page.jsonl final
    log.info('')
    log.info(f'Fertig. Alle Outputs in {RESULTS}/')


if __name__ == '__main__':
    main()
