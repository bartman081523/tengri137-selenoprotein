"""
Stufe 11 — Hidden Math (π, ^, ×).

Frage: Wo sind die math-Operatoren im Dokument?

Methode:
  1) Sammle alle math_*-Glyphen
  2) Verteilung pro Seite
  3) Vision-Description-Texte der math-Glyphen lesen
  4) Vergleich mit Schmehs Transkription (welche Seiten haben Formeln
     laut Schmeh, welche laut V4?)
  5) Hidden math: wo sieht V4 math_X, aber Schmeh NICHT?
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs')
with open(BASE / 'doc.json') as f:
    doc = json.load(f)

# === REPORT ===
print("=" * 80)
print("STUFE 11 — HIDDEN MATH (π, ^, ×)")
print("=" * 80)
print()

# 1) Alle math_*-Glyphen sammeln
print("=" * 80)
print("1) ALLE MATH_*-GLYPHEN IM DOKUMENT")
print("=" * 80)
print()

math_glyphs = []
for p in doc['pages']:
    for r in p['regions']:
        for g in r.get('glyphs', []):
            vk = g.get('vision_kind') or ''
            if vk.startswith('math_'):
                bbox = g.get('bbox', [0,0,0,0])
                x,y,w,h = bbox
                math_glyphs.append({
                    'page': p['page_id'],
                    'region': r['region_id'],
                    'idx': g.get('glyph_index'),
                    'vk': vk,
                    'cx': x + w/2, 'cy': y + h/2,
                    'w': w, 'h': h, 'size': g.get('size_px', 0),
                    'cluster': g.get('cluster_id'),
                    'vd': g.get('vision_description') or '',
                })

math_glyphs.sort(key=lambda g: (g['page'], g['cy'], g['cx']))

print(f"GESAMT: {len(math_glyphs)} math_*-Glyphen")
print()

# Verteilung
vk_counter = Counter(g['vk'] for g in math_glyphs)
print("Verteilung nach Operator:")
for vk, c in vk_counter.most_common():
    print(f"  {vk:30s}: {c}")
print()

# Pro Seite
page_counter = Counter(g['page'] for g in math_glyphs)
print("Verteilung nach Seite:")
for p, c in sorted(page_counter.items()):
    print(f"  {p}: {c} math_*-Glyphen")
print()

# 2) Detaillierte Liste
print("=" * 80)
print("2) DETAILLIERTE LISTE (sortiert nach Seite, y, x)")
print("=" * 80)
print()

for g in math_glyphs:
    vd_short = (g['vd'] or '(none)')[:80]
    print(f"  {g['page']:5s} {g['region']:12s} idx={g['idx']:3d}  ({g['cx']:6.0f},{g['cy']:6.0f})  "
          f"size={g['size']:5d}  vk={g['vk']:25s}  vd='{vd_short}'")
print()

# 3) Vision-Descriptions genau lesen (volle Länge)
print("=" * 80)
print("3) VISION-DESCRIPTIONS VOLLSTÄNDIG")
print("=" * 80)
print()

for g in math_glyphs:
    print(f"--- {g['page']} {g['region']} idx={g['idx']} vk={g['vk']} ---")
    print(f"  Vision: {g['vd'] or '(none)'}")
    print()

# 4) Vergleich V4 vs Schmeh: Welche Seiten haben Formeln?
print("=" * 80)
print("4) VERGLEICH: V4-FORMEL-GLYPHEN vs SCHMEH-TRANSKRIPTION")
print("=" * 80)
print()

# Welche Seiten haben laut V4 math_times?
v4_formula_pages = set(g['page'] for g in math_glyphs if g['vk'] == 'math_times')
v4_math_pi_pages = set(g['page'] for g in math_glyphs if g['vk'] == 'math_pi')
v4_math_exp_pages = set(g['page'] for g in math_glyphs if g['vk'] == 'math_exponentiation')

# Schmehs Transkription: Welche Seiten haben 'math_content' (π, ^, ×, Zahlen)?
# p14: π7π^7
# p17-p18: Primfaktorzerlegungen mit *
# p19-p23: Text only (laut Schmeh), aber p23 hat BURUMUT-Matrix

schmeh_formula_pages = {'p14', 'p17', 'p18'}  # p14 hat π, p17-18 haben Primfaktorzerlegungen
# p19-p22 sind laut Schmeh "no sigils" (also keine Formeln)
# p23 hat BURUMUT-Matrix (auch Formel)

print(f"V4 sieht math_times auf Seiten: {sorted(v4_formula_pages)}")
print(f"V4 sieht math_pi auf Seiten: {sorted(v4_math_pi_pages)}")
print(f"V4 sieht math_exponentiation auf Seiten: {sorted(v4_math_exp_pages)}")
print()

# HIDDEN MATH: V4 sieht math_X, aber Schmeh transkribiert KEINE Formel
hidden_math = v4_formula_pages - schmeh_formula_pages
print(f"HIDDEN MATH (V4-ja, Schmeh-nein): {sorted(hidden_math)}")
print()

# 5) Detail pro hidden math Seite
for pid in sorted(hidden_math):
    p = None
    for pp in doc['pages']:
        if pp['page_id'] == pid:
            p = pp
            break
    n_glyphs = sum(len(r.get('glyphs', [])) for r in p['regions'])
    n_complex = sum(1 for r in p['regions'] for g in r.get('glyphs', []) if g.get('type_hint') == 'complex_symbol')
    n_latin = sum(len(r.get('text', '').split()) for r in p['regions'])
    n_lines = sum(1 for r in p['regions'] if r.get('text'))
    print(f"  {pid}: {n_glyphs} Glyphen, {n_complex} complex_symbol, {n_latin} Latin-Tokens, {n_lines} Text-Regionen")
print()

# 6) p14: math_pi-Detail
print("=" * 80)
print("6) p14: math_pi-GLYPHE")
print("=" * 80)
print()
for g in math_glyphs:
    if g['vk'] == 'math_pi':
        print(f"  idx={g['idx']}  region={g['region']}  ({g['cx']:.0f}, {g['cy']:.0f})  size={g['size']}  cluster={g['cluster']}")
        print(f"  Vision: {g['vd']}")
print()

# 7) p19: math_exponentiation-Detail + 3 vertikale Linien
print("=" * 80)
print("7) p19: math_exponentiation + 3 vertikale Linien")
print("=" * 80)
print()
for g in math_glyphs:
    if g['page'] == 'p19' and g['vk'] == 'math_exponentiation':
        print(f"  math_exp: idx={g['idx']}  region={g['region']}  ({g['cx']:.0f}, {g['cy']:.0f})")
        print(f"  Vision: {g['vd']}")

# 3 vertikale Linien
for p in doc['pages']:
    if p['page_id'] == 'p19':
        for r in p['regions']:
            for g in r.get('glyphs', []):
                th = g.get('type_hint', '')
                if th == 'vertical_line':
                    bbox = g.get('bbox', [0,0,0,0])
                    print(f"  vert_line: idx={g.get('glyph_index')}  bbox={bbox}  cluster={g.get('cluster_id')}")
                    print(f"  Vision: {g.get('vision_description') or '(none)'}")
print()

# JSON-Export
out = {
    'n_math_glyphs': len(math_glyphs),
    'vk_distribution': dict(vk_counter),
    'page_distribution': dict(page_counter),
    'math_glyphs': [{
        'page': g['page'], 'region': g['region'], 'idx': g['idx'],
        'vk': g['vk'], 'cx': g['cx'], 'cy': g['cy'],
        'size': g['size'], 'cluster': g['cluster'],
        'vd': g['vd'][:200] if g['vd'] else None,
    } for g in math_glyphs],
    'hidden_math_pages': sorted(hidden_math),
}
with open(BASE.parent / 'scratches' / 'stufe_11' / 'math_glyphs.json', 'w') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"\nJSON-Export: scratches/stufe_11/math_glyphs.json")
