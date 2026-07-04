"""
Stufe 10 — p18, die "tabula rasa"-Seite.

Frage: Was ist die Struktur von p18?

Methode:
  1) p18 Glyphen extrahieren (mit x,y,size,vk,type_hint)
  2) Sortiert nach (y, x) ausgeben — Reihen sichtbar machen
  3) Spezielle Suche: 3 math_times, 1 vertical_line, 16 große Strukturen
  4) Vergleich mit p17
  5) ASCII-Plot der Glyphen-Verteilung
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs')
with open(BASE / 'doc.json') as f:
    doc = json.load(f)

# p18 heraussuchen
p18 = None
for p in doc['pages']:
    if p['page_id'] == 'p18':
        p18 = p
        break

# Glyphen in Reihenfolge (x, y)
glyphs = []
for r in p18['regions']:
    for g in r.get('glyphs', []):
        bbox = g.get('bbox', [0, 0, 0, 0])
        x, y, w, h = bbox
        glyphs.append({
            'idx': g.get('glyph_index'),
            'region': r['region_id'],
            'x': x, 'y': y, 'w': w, 'h': h,
            'cx': x + w/2, 'cy': y + h/2,
            'cluster': g.get('cluster_id'),
            'vk': g.get('vision_kind'),
            'th': g.get('type_hint'),
            'size': g.get('size_px', 0),
            'fill': g.get('fill_ratio', 0),
        })

# Sortiere nach (y, x)
glyphs.sort(key=lambda g: (g['cy'], g['cx']))

# === REPORT ===
print("=" * 80)
print("STUFE 10 — p18, DIE 'TABULA RASA'-SEITE")
print("=" * 80)
print()

print(f"p18: {len(glyphs)} Glyphen, {len(p18['regions'])} Regionen")
print()

# 1) Glyphen-Liste sortiert nach (y, x)
print("=" * 80)
print("1) GLYPHEN p18 (sortiert nach y, x)")
print("=" * 80)
print(f"{'idx':>4s}  {'region':12s}  {'cx':>6s}  {'cy':>6s}  {'w':>5s}  {'h':>5s}  {'size':>7s}  {'vk':30s}  {'th':18s}  cluster")
for g in glyphs:
    vk = g['vk'] or ''
    th = g['th'] or ''
    print(f"{g['idx']:4d}  {g['region']:12s}  {g['cx']:6.0f}  {g['cy']:6.0f}  {g['w']:5d}  {g['h']:5d}  {g['size']:7d}  {vk:30s}  {th:18s}  {g['cluster']}")
print()

# 2) Vision-Kinds auf p18
print("=" * 80)
print("2) VISION-KINDS AUF p18")
print("=" * 80)
vk_counter = Counter(g['vk'] for g in glyphs if g['vk'])
for vk, c in vk_counter.most_common():
    print(f"  {vk:30s}: {c}")
print()

# 3) math_times-Glyphen auf p18
print("=" * 80)
print("3) MATH_TIMES-GLYPHEN AUF p18")
print("=" * 80)
for g in glyphs:
    if g['vk'] == 'math_times':
        print(f"  idx={g['idx']}  ({g['cx']:.0f}, {g['cy']:.0f})  size={g['size']}  region={g['region']}  th={g['th']}")
print()

# 4) 49755 px Glyphe
print("=" * 80)
print("4) 49755 px GLYPHE AUF p18")
print("=" * 80)
for g in glyphs:
    if g['size'] == 49755:
        print(f"  idx={g['idx']}  region={g['region']}  ({g['cx']:.0f}, {g['cy']:.0f})  w={g['w']}  h={g['h']}  th={g['th']}  cluster={g['cluster']}")
print()

# 5) ASCII-Plot
print("=" * 80)
print("5) ASCII-PLOT p18")
print("=" * 80)

WIDTH = 60
HEIGHT = 25
grid = [[' '] * WIDTH for _ in range(HEIGHT)]

if glyphs:
    xs = [g['cx'] for g in glyphs]
    ys = [g['cy'] for g in glyphs]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    x_range = x_max - x_min if x_max > x_min else 1
    y_range = y_max - y_min if y_max > y_min else 1

    for g in glyphs:
        col = int((g['cx'] - x_min) / x_range * (WIDTH - 1))
        row = int((g['cy'] - y_min) / y_range * (HEIGHT - 1))
        col = max(0, min(WIDTH - 1, col))
        row = max(0, min(HEIGHT - 1, row))
        if g['vk'] == 'math_times':
            grid[row][col] = '×'
        elif g['vk'] == 'line':
            grid[row][col] = '-'
        elif g['vk'] == 'vertical_line' or (g['th'] == 'vertical_line'):
            grid[row][col] = '|'
        elif g['vk'] in ('other', 'unknown'):
            grid[row][col] = '?'
        elif g['vk']:
            grid[row][col] = '#'
        else:
            grid[row][col] = '.'

for row in grid:
    print(''.join(row))
print(f"  Legende: × = math_times, - = line, | = vertikal, ? = other/unknown, # = andere vk, . = ohne vk")
print()

# 6) p18 vs p17 (Struktur-Vergleich)
print("=" * 80)
print("6) p18 vs p17 — STRUKTURVERGLEICH")
print("=" * 80)
p17 = None
for p in doc['pages']:
    if p['page_id'] == 'p17':
        p17 = p
        break

def page_stats(p, label):
    glyphs_p = []
    for r in p['regions']:
        for g in r.get('glyphs', []):
            glyphs_p.append(g)
    vk_p = Counter(g.get('vision_kind') for g in glyphs_p if g.get('vision_kind'))
    return {
        'n': len(glyphs_p),
        'math_times': vk_p.get('math_times', 0),
        'line': vk_p.get('line', 0),
        'other': vk_p.get('other', 0),
        'unknown': vk_p.get('unknown', 0),
    }

p17_stats = page_stats(p17, 'p17')
p18_stats = page_stats(p18, 'p18')

print(f"  {'Metric':25s}  {'p17':>5s}  {'p18':>5s}")
for k in ['n', 'math_times', 'line', 'other', 'unknown']:
    print(f"  {k:25s}  {p17_stats[k]:5d}  {p18_stats[k]:5d}")
print()

# 7) Spezielle Suche: gleiche Glyphe (idx 825 + idx 849) auf beiden Seiten
print("=" * 80)
print("7) ZWILLINGS-GLYPHE p17/p18 (size 49755)")
print("=" * 80)
for pp_id, pp in [('p17', p17), ('p18', p18)]:
    for r in pp['regions']:
        for g in r.get('glyphs', []):
            if g.get('size_px') == 49755:
                bbox = g.get('bbox', [0, 0, 0, 0])
                print(f"  {pp_id} {r['region_id']:12s}  idx={g.get('glyph_index'):3d}  cx={bbox[0]+bbox[2]/2:.0f}  cy={bbox[1]+bbox[3]/2:.0f}  cluster={g.get('cluster_id')}")
print()

# JSON-Export
out = {
    'page': 'p18',
    'n_glyphs': len(glyphs),
    'n_regions': len(p18['regions']),
    'vk_counter': dict(vk_counter),
    'math_times': [{'idx': g['idx'], 'cx': g['cx'], 'cy': g['cy'], 'size': g['size']} for g in glyphs if g['vk'] == 'math_times'],
    'colossal_49755': [{'idx': g['idx'], 'region': g['region'], 'cx': g['cx'], 'cy': g['cy'], 'w': g['w'], 'h': g['h']} for g in glyphs if g['size'] == 49755],
    'p17_stats': p17_stats,
    'p18_stats': p18_stats,
}
with open(BASE.parent / 'scratches' / 'stufe_10' / 'p18.json', 'w') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"\np18-JSON: scratches/stufe_10/p18.json")
