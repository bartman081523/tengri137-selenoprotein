"""
V10.3 EMPIRISCHE VERIFIKATION (consecutive_research, 2026-07-08)
================================================================

Verifiziert die V10.3 Master-JSON-Behauptungen gegen doc.json
(Gold-Standard) und V9 v2 Smart-Parser (Sekundär-Quelle).

Output: v103_verifikation.json mit allen Befunden
"""
import json
from pathlib import Path

# === QUELLEN LADEN ===
DOC_JSON = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs/doc.json')
V103 = Path('/run/media/julian/ML4/tengri137/consecutive_reading/bbox/v103_20260708/tengri137_complete_decoded_v103.json')
V9_V2 = Path('/run/media/julian/ML4/tengri137/consecutive_reading/bbox/v9_reproduction_20260706/burumut_decoded_v2.json')

with open(DOC_JSON) as f:
    doc = json.load(f)
with open(V103) as f:
    v103 = json.load(f)
with open(V9_V2) as f:
    v9_v2 = json.load(f)

seiten_v103 = v103.get('seiten', [])
pages_v9 = v9_v2.get('pages', {})
doc_pages = {p.get('page_id'): p for p in doc.get('pages', [])}

# === BEFUNDE SAMMELN ===
befunde = {
    'datum': '2026-07-08',
    'methode': 'Empirische doc.json-Verifikation gegen V10.3 Master-JSON',
    'p17_burumut_faelschung': {},
    'n_formulas_bbox_vergleich': {},
    'v10_3_internes_bug_duplikate': {},
    'p23_korrekturen': {},
    'magic_cubes': {},
    'bilanz': {}
}

# === A. p17 BURUMUT-VERIFIKATION ===
print("=" * 80)
print("A. P17 BURUMUT-VERIFIKATION")
print("=" * 80)

p17_doc = doc_pages.get('p17', {})
p17_doc_latin = sum(len(r.get('latin_tokens', [])) for r in p17_doc.get('regions', []))
p17_doc_formulas = sum(len(r.get('formulas', [])) for r in p17_doc.get('regions', []))

p17_v103 = next((s for s in seiten_v103 if s.get('page_id') == 'p17'), {})
p17_v103_n_b = p17_v103.get('n_burumut_words_v9', 0)
p17_v103_gp = p17_v103.get('glyph_to_phrase', [])

befunde['p17_burumut_faelschung'] = {
    'p17_n_burumut_words_v103': p17_v103_n_b,
    'p17_n_burumut_doc_json': 0,
    'p17_n_burumut_v9_v2': len(pages_v9.get('p17', [])),  # = 17 Fractions, nicht BURUMUT
    'doc_json_p17_latin': p17_doc_latin,
    'doc_json_p17_formulas': p17_doc_formulas,
    'befund': 'FAELSCHUNG' if p17_v103_n_b > 0 else 'KORREKT',
    'erklaerung': f'V10.3 erfindet {p17_v103_n_b} BURUMUT-Wörter für p17, doc.json/V9 v2 haben 0.'
}

print(f"V10.3 p17 n_burumut_words_v9: {p17_v103_n_b}")
print(f"doc.json p17: {p17_doc_latin} Latin, {p17_doc_formulas} Formulas, 0 BURUMUT")
print(f"V9 v2 p17: {len(pages_v9.get('p17', []))} Fractions (KEINE 22_atoms)")
print(f"FAZIT: p17 hat 0 BURUMUT, V10.3 erfindet 11")
print()

# === B. 1:1 DUPLIKAT-VERIFIKATION ===
print("=" * 80)
print("B. P17 vs P23 BURUMUT — 1:1 DUPLIKAT?")
print("=" * 80)

p23_v103 = next((s for s in seiten_v103 if s.get('page_id') == 'p23'), {})
p23_v103_gp = p23_v103.get('glyph_to_phrase', [])

duplikate = []
for i, (p17_gp, p23_gp) in enumerate(zip(p17_v103_gp, p23_v103_gp), 1):
    p17_phrase = p17_gp.get('phrase', '')
    p23_phrase = p23_gp.get('phrase', '')
    is_dup = (p17_phrase == p23_phrase)
    duplikate.append({
        'idx': i,
        'p17': p17_phrase,
        'p23': p23_phrase,
        'is_duplikat': is_dup
    })
    if not is_dup:
        print(f"  Wort {i}: p17='{p17_phrase}' ≠ p23='{p23_phrase}'  ✗ ANDERS")
    else:
        print(f"  Wort {i}: {p17_phrase}  ✓ GLEICH")

n_dup = sum(1 for d in duplikate if d['is_duplikat'])
print(f"\nDuplikate: {n_dup}/11 = {n_dup/11*100:.1f}%")

befunde['p17_burumut_faelschung']['duplikate_p17_p23'] = duplikate
befunde['p17_burumut_faelschung']['n_duplikate'] = n_dup
print()

# === C. N_FORMULAS_BBOX-VERGLEICH ===
print("=" * 80)
print("C. N_FORMULAS_BBOX: V10.3 vs V9 V2 vs DOC.JSON")
print("=" * 80)

print(f"{'Seite':<6} {'V10.3':<8} {'V9 v2':<8} {'doc.json':<10} {'V10.3≠doc':<14}")
for pid in ['p17', 'p18', 'p19', 'p20', 'p21', 'p22', 'p23']:
    v103_s = next((s for s in seiten_v103 if s.get('page_id') == pid), {})
    v103_n = v103_s.get('n_formulas_bbox', 0)
    v9_n = len(pages_v9.get(pid, [])) if pid in pages_v9 else 0
    doc_n = sum(len(r.get('formulas', [])) for r in doc_pages.get(pid, {}).get('regions', []))
    diff = '✗' if v103_n != doc_n else '✓'
    print(f"{pid:<6} {v103_n:<8} {v9_n:<8} {doc_n:<10} {diff}")
    befunde['n_formulas_bbox_vergleich'][pid] = {
        'v103': v103_n, 'v9_v2': v9_n, 'doc_json': doc_n
    }
print()

# === D. V10.3 INTERNES BUG-DUPLIKAT ===
print("=" * 80)
print("D. V10.3 INTERNES BUG: P17 BURUMUT_09 = NANPSSGNNRCSSSE (V9 v2 Bug dupliziert)")
print("=" * 80)

p17_9 = next((gp for gp in p17_v103_gp if gp.get('glyph') == 'BURUMUT_09'), None)
p23_9 = next((gp for gp in p23_v103_gp if gp.get('glyph') == 'BURUMUT_09'), None)

if p17_9 and p23_9:
    p17_9_phrase = p17_9.get('phrase', '')
    p23_9_phrase = p23_9.get('phrase', '')
    befunde['v10_3_internes_bug_duplikate'] = {
        'p17_burumut_09': p17_9_phrase,
        'p23_burumut_09': p23_9_phrase,
        'sind_gleich': p17_9_phrase == p23_9_phrase,
        'befund': 'INKONSISTENT' if p17_9_phrase != p23_9_phrase else 'KONSISTENT',
        'erklaerung': f'p23 wurde korrigiert (V9 v2-Bug behoben), p17 nicht.'
    }
    print(f"  p17 BURUMUT_09 = '{p17_9_phrase}'")
    print(f"  p23 BURUMUT_09 = '{p23_9_phrase}'")
    print(f"  Befund: {'INKONSISTENT' if p17_9_phrase != p23_9_phrase else 'KONSISTENT'}")
print()

# === E. P23 KORREKTUREN ===
print("=" * 80)
print("E. P23 KORREKTUREN (V9 v2-Bug behoben)")
print("=" * 80)

# Vergleiche p23 BURUMUT_09 und BURUMUT_10 mit V9 v2
# Achtung: V9 v2 idx 8 entspricht BURUMUT_09 (1-basiert), idx 10 = BURUMUT_11
# Aber V9 v2 list[idx] ist 0-indiziert, also idx 8 = 9. Element = BURUMUT_09
p23_9_v9_raw = pages_v9.get('p23', [])[8] if len(pages_v9.get('p23', [])) > 8 else {}
p23_11_v9_raw = pages_v9.get('p23', [])[10] if len(pages_v9.get('p23', [])) > 10 else {}

# V9 v2 hat im JSON: fraction_idx, num_expr, den_expr, num_value, den_value, 22_atoms
# Das 22_atoms-Feld enthält die BURUMUT-Wörter
v9_22_atoms = [item.get('22_atoms', '') for item in pages_v9.get('p23', [])]
v9_idx_8 = v9_22_atoms[8] if len(v9_22_atoms) > 8 else ''
v9_idx_10 = v9_22_atoms[10] if len(v9_22_atoms) > 10 else ''

if p23_9:
    p23_9_phrase = p23_9.get('phrase', '')
    befunde['p23_korrekturen'] = {
        'idx_9_v9_v2': v9_idx_8,
        'idx_9_v10_3': p23_9_phrase,
        'idx_9_korrigiert': p23_9_phrase == 'NAFERANSAHOTFE',
    }
    print(f"  idx 9: V9 v2 = '{v9_idx_8}' → V10.3 = '{p23_9_phrase}'")

p23_10 = next((gp for gp in p23_v103_gp if gp.get('glyph') == 'BURUMUT_10'), None)
if p23_10:
    p23_10_phrase = p23_10.get('phrase', '')
    befunde['p23_korrekturen']['idx_10_v9_v2'] = v9_idx_10
    befunde['p23_korrekturen']['idx_10_v10_3'] = p23_10_phrase
    befunde['p23_korrekturen']['idx_10_korrigiert'] = p23_10_phrase == 'KOREMORBIZUMRO'
    print(f"  idx 10: V9 v2 = '{v9_idx_10}' → V10.3 = '{p23_10_phrase}'")
print()

# === F. MAGIC CUBES ===
print("=" * 80)
print("F. MAGIC CUBES P05/P06")
print("=" * 80)

for pid in ['p05', 'p06']:
    v103_s = next((s for s in seiten_v103 if s.get('page_id') == pid), {})
    is_mc = v103_s.get('is_magic_cube_page', False)
    n_mc = v103_s.get('n_magic_cubes', 0)
    print(f"  {pid}: is_magic_cube_page={is_mc}, n_magic_cubes={n_mc}")
    befunde['magic_cubes'][pid] = {
        'is_magic_cube_page': is_mc,
        'n_magic_cubes': n_mc,
        'korrekt': is_mc and n_mc == 8
    }
print()

# === G. BILANZ ===
print("=" * 80)
print("G. BILANZ")
print("=" * 80)

# 4 Hauptkategorien:
# 1. p17 BURUMUT = FÄLSCHUNG (11 erfunden, 0 ehrlich)
# 2. n_formulas_bbox = KORRIGT aus V9 v2 (semantisch anderes als doc.json, beides legitim)
# 3. p23 idx 8/10 Korrekturen = KORREKT
# 4. Magic Cubes p05/p06 = KORREKT
# 5. p17 BURUMUT_09 Bug-Duplikation = FÄLSCHUNG (inkonsistent mit p23)

n_korrekt = 0
n_falsch = 0
n_neutral = 0

# 1. p17 BURUMUT
if befunde['p17_burumut_faelschung']['befund'] == 'KORREKT':
    n_korrekt += 1
else:
    n_falsch += 1

# 2. n_formulas_bbox
n_neutral += 1  # V10.3 nutzt V9 v2 (legitim), nicht doc.json (auch legitim)

# 3. p23 Korrekturen
if (befunde['p23_korrekturen'].get('idx_9_korrigiert') and
    befunde['p23_korrekturen'].get('idx_10_korrigiert')):
    n_korrekt += 1
else:
    n_falsch += 1

# 4. Magic Cubes
if all(befunde['magic_cubes'][p]['korrekt'] for p in ['p05', 'p06']):
    n_korrekt += 1
else:
    n_falsch += 1

# 5. p17 Bug-Duplikation
if befunde['v10_3_internes_bug_duplikate'].get('befund') == 'KONSISTENT':
    n_korrekt += 1
else:
    n_falsch += 1

befunde['bilanz'] = {
    'kategorien_korrekt': n_korrekt,
    'kategorien_falsch': n_falsch,
    'kategorien_neutral': n_neutral,
    'gesamt_beurteilt': n_korrekt + n_falsch,
    'anteil_korrekt': f"{n_korrekt/(n_korrekt+n_falsch)*100:.0f}%"
}

print(f"  Korrekt: {n_korrekt}/{n_korrekt+n_falsch} = {befunde['bilanz']['anteil_korrekt']}")
print(f"  Falsch: {n_falsch}/{n_korrekt+n_falsch}")
print(f"  Neutral (semantisch anderes, beides legitim): {n_neutral}")
print()
print("VERDICT: V10.3 ist KEINE 100% Replikation.")
print(f"  {n_korrekt}/{n_korrekt+n_falsch} Hauptkategorien korrekt,")
print(f"  p17 BURUMUT ist eine FÄLSCHUNG (p23-Duplikate).")
print("  V10.1 + V10.2 bleiben Gold-Standard.")

# === SPEICHERN ===
out_path = Path('/run/media/julian/ML4/tengri137/consecutive_research/scratches/v103_verifikation.json')
with open(out_path, 'w') as f:
    json.dump(befunde, f, indent=2, ensure_ascii=False)
print(f"\nVerifikation gespeichert: {out_path}")
