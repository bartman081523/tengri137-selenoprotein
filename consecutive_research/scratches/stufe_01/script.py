"""
Stufe 1 — Page × Region-Typ Matrix.

Frage: Welche Seiten sind lateinlastig, glyphenlastig, hybrid?

Methode: Für jede Seite zähle ich:
  - Anzahl Regionen pro Region-Typ
  - Anzahl Glyphen
  - Anzahl Latin-Tokens
  - Verhältnis Glyphen/Latin

Output:
  - Matrix-Print
  - Klassifikation pro Seite
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs')
with open(BASE / 'doc.json') as f:
    doc = json.load(f)

# Page × Region-Typ
page_region = defaultdict(Counter)  # pid -> {rt: count}
page_glyphs = Counter()
page_latin = Counter()
page_formulas = Counter()  # speziell formula_block-Regionen
page_specific = defaultdict(list)  # pid -> [('magic_cube', region_id), ('burumut_block', region_id), ...]

# Region-Typ-Liste
all_region_types = set()

for p in doc['pages']:
    pid = p['page_id']
    for r in p['regions']:
        rt = r.get('region_type', '?')
        all_region_types.add(rt)
        page_region[pid][rt] += 1
        page_glyphs[pid] += len(r.get('glyphs', []))
        page_latin[pid] += len(r.get('latin_tokens', []))
        if rt == 'formula_block':
            page_formulas[pid] += 1
        if rt in ('magic_cube', 'burumut_block', 'numeric_table'):
            page_specific[pid].append((rt, r['region_id']))

# Matrix ausgeben
print("=" * 80)
print("STUFE 1 — PAGE × REGION-TYP MATRIX")
print("=" * 80)
print()

# Sortierte Region-Typen (nach Häufigkeit)
rt_order = ['latin_text', 'formula_block', 'footer', 'graphic_line',
            'glyph_block', 'numeric_table', 'single_glyph', 'glyph_raster',
            'header', 'magic_cube', 'burumut_block']

# Header
print(f"{'Page':<6}" + "".join(f"{rt[:9]:>10}" for rt in rt_order) + f"{'Sum':>6}  {'G':>5}  {'L':>5}  G/L")
print("-" * 110)

# Daten
for pid in sorted(page_region.keys()):
    row = page_region[pid]
    cells = "".join(f"{row.get(rt, 0):>10}" for rt in rt_order)
    total = sum(row.values())
    g = page_glyphs[pid]
    l = page_latin[pid]
    ratio = f"{g/max(l,1):.2f}"
    print(f"{pid:<6}{cells}{total:>6}  {g:>5}  {l:>5}  {ratio}")

print()

# Klassifikation
print("=" * 80)
print("KLASSIFIKATION DER SEITEN")
print("=" * 80)
print()

# Schwellen: glyph-dominant wenn G > 50 UND L < 10
# latein-dominant wenn L > 15 UND G < 30
# hybrid sonst
for pid in sorted(page_region.keys()):
    g = page_glyphs[pid]
    l = page_latin[pid]
    formulas = page_formulas[pid]
    specific = page_specific[pid]

    classes = []
    if g > 50 and l < 10:
        classes.append("GLYPH-DOMINANT")
    elif l > 15 and g < 30:
        classes.append("LATIN-DOMINANT")
    elif g < 5 and l < 5:
        classes.append("MINIMAL")
    else:
        classes.append("HYBRID")

    if formulas >= 3:
        classes.append(f"FORMEL-REICH ({formulas})")

    special_notes = []
    for rt, rid in specific:
        special_notes.append(f"{rt}@{rid}")
    if special_notes:
        classes.append("SPEZIAL: " + ", ".join(special_notes))

    if g == 0 and l == 0:
        classes.append("LEER")

    classification = " | ".join(classes)
    print(f"  {pid}: G={g:3d}  L={l:3d}  →  {classification}")

print()

# Latin/Glyph Ratio-Verteilung
print("=" * 80)
print("G/L RATIO VERTEILUNG")
print("=" * 80)
ratios = []
for pid in sorted(page_region.keys()):
    g = page_glyphs[pid]
    l = page_latin[pid]
    if l > 0:
        ratios.append((pid, g/l))
    else:
        ratios.append((pid, float('inf') if g > 0 else 0))

for pid, r in ratios:
    if r == float('inf'):
        print(f"  {pid}: G/L = ∞  (Glyphen ohne Latin)")
    else:
        print(f"  {pid}: G/L = {r:.2f}")

print()

# Welcher Region-Typ ist auf welcher Seite dominant?
print("=" * 80)
print("DOMINANTER REGION-TYP PRO SEITE")
print("=" * 80)
for pid in sorted(page_region.keys()):
    row = page_region[pid]
    if row:
        dom = row.most_common(1)[0]
        print(f"  {pid}: {dom[0]} ({dom[1]})")

# JSON Export
import json
out = {
    'page_region_matrix': {pid: dict(row) for pid, row in page_region.items()},
    'page_glyphs': dict(page_glyphs),
    'page_latin': dict(page_latin),
    'page_formulas': dict(page_formulas),
    'page_specific': {pid: specific for pid, specific in page_specific.items()},
}
with open(BASE.parent / 'scratches' / 'stufe_01' / 'page_matrix.json', 'w') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"\nMatrix-JSON: scratches/stufe_01/page_matrix.json")
