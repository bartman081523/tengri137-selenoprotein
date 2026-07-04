"""
Stufe 8 — Position ist Information.

Frage: Was sagen die x,y-Koordinaten der Glyphen?

Methode:
  1) Pro Seite: Glyphen-Centroids extrahieren
  2) Suche nach Reihen (gleiche y, ähnliche x)
  3) Identische Glyphen auf gleichen Positionen (z.B. 49755px auf p17/p18)
  4) Diagonalen, Spalten
  5) 2D-Visualisierung als Text
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs')
with open(BASE / 'doc.json') as f:
    doc = json.load(f)

# Sammler
page_glyphs = defaultdict(list)  # pid -> [(idx, x, y, w, h, cluster, vk, size, fill), ...]
for p in doc['pages']:
    pid = p['page_id']
    for r in p['regions']:
        for g in r.get('glyphs', []):
            bbox = g.get('bbox', [0, 0, 0, 0])
            x, y, w, h = bbox
            cx = x + w / 2
            cy = y + h / 2
            page_glyphs[pid].append({
                'idx': g.get('glyph_index'),
                'region': r['region_id'],
                'cx': cx, 'cy': cy, 'w': w, 'h': h,
                'cluster': g.get('cluster_id'),
                'vk': g.get('vision_kind'),
                'th': g.get('type_hint'),
                'size': g.get('size_px', 0),
                'fill': g.get('fill_ratio', 0),
            })

# === REPORT ===
print("=" * 80)
print("STUFE 8 — POSITION IST INFORMATION")
print("=" * 80)
print()

# 1) Pro Seite: 2D-Plot (x=Spalte 0-30, y=Zeile 0-15)
print("=" * 80)
print("1) 2D-GLYPHEN-VERTEILUNG PRO SEITE (ASCII-Plot, normalisiert)")
print("=" * 80)
print()

# Wir bauen einen vereinfachten ASCII-Plot
def plot_glyphs(glyphs, width=80, height=20):
    if not glyphs:
        return ""
    xs = [g['cx'] for g in glyphs]
    ys = [g['cy'] for g in glyphs]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    x_range = x_max - x_min if x_max > x_min else 1
    y_range = y_max - y_min if y_max > y_min else 1

    grid = [[' '] * width for _ in range(height)]
    for g in glyphs:
        col = int((g['cx'] - x_min) / x_range * (width - 1))
        row = int((g['cy'] - y_min) / y_range * (height - 1))
        col = max(0, min(width - 1, col))
        row = max(0, min(height - 1, row))
        if g['vk']:
            grid[row][col] = '*'  # MIT Vision
        else:
            grid[row][col] = '.'  # OHNE Vision
    return '\n'.join(''.join(row) for row in grid)

for pid in sorted(page_glyphs.keys()):
    glyphs = page_glyphs[pid]
    print(f"\n  === {pid} ({len(glyphs)} Glyphen) ===")
    print(plot_glyphs(glyphs))
    print(f"  Legende: '*' = MIT Vision-Description, '.' = OHNE")
    print()

# 2) Suche nach Glyphen, die auf MEHREREN Seiten an derselben Position stehen
print("=" * 80)
print("2) GLEICHE GLYPHEN AUF VERSCHIEDENEN SEITEN (gleiche Grösse + gleicher Cluster)")
print("=" * 80)
print()

# Glyphen mit gleicher size UND gleichem Cluster
combo_counter = Counter()
for pid, glyphs in page_glyphs.items():
    for g in glyphs:
        combo_counter[(g['cluster'], g['size'])] += 1

# Welche (cluster, size) Kombinationen kommen auf mehreren Seiten vor?
page_for_combo = defaultdict(set)
for pid, glyphs in page_glyphs.items():
    for g in glyphs:
        page_for_combo[(g['cluster'], g['size'])].add(pid)

multi_page = [(c, n) for c, n in combo_counter.items() if len(page_for_combo[c]) > 1]
print(f"  {len(multi_page)} Cluster-Size-Kombinationen kommen auf mehreren Seiten vor.")
print()

# Top 20 der Mehrfach-Kombinationen
for (cid, sz), n in sorted(multi_page, key=lambda x: -x[1])[:20]:
    pages = sorted(page_for_combo[(cid, sz)])
    print(f"  {cid:55s} size={sz:6d}: {n}x auf {len(pages)} Seiten ({', '.join(pages)})")
print()

# 3) Spezielle Suche: idx 825 (p17_R7) und idx 849 (p18_R7) sind beide 49755px
print("=" * 80)
print("3) DIE ZWEI 49755px-GLYPHEN (p17 + p18)")
print("=" * 80)
print()
for pid, glyphs in page_glyphs.items():
    for g in glyphs:
        if g['size'] == 49755:
            print(f"  {pid} {g['region']:25s} idx={g['idx']:3d} cx={g['cx']:.0f} cy={g['cy']:.0f} w={g['w']} h={g['h']} cluster={g['cluster']}")
print()

# 4) Glyphen auf "gleicher Zeile" (gleiche y ± 5px) — Reihen
print("=" * 80)
print("4) REIHEN: Glyphen mit gleichem y (Toleranz 5px)")
print("=" * 80)
print()

# Auf p08_R15 sind 9 Glyphen mit ähnlichem y. Bereits gezeigt. Was noch?
for pid in ['p05', 'p06', 'p08', 'p13', 'p17', 'p18', 'p19', 'p20', 'p21', 'p22', 'p23']:
    glyphs = page_glyphs[pid]
    # Cluster by y (Toleranz 10)
    y_groups = defaultdict(list)
    for g in glyphs:
        # Runde y auf nächste 30
        y_bucket = round(g['cy'] / 30) * 30
        y_groups[y_bucket].append(g)
    # Drucke Gruppen mit >= 3 Glyphen
    multi_groups = [(y, gs) for y, gs in y_groups.items() if len(gs) >= 3]
    if multi_groups:
        print(f"  {pid}:")
        for y, gs in sorted(multi_groups):
            xs = sorted([int(g['cx']) for g in gs])
            idxs = [g['idx'] for g in gs]
            print(f"    y≈{y:5d}: {len(gs):2d} Glyphen  x={xs}  idx={idxs}")
print()

# 5) Glyphen-Position-Range pro Seite
print("=" * 80)
print("5) POSITION-RANGE PRO SEITE")
print("=" * 80)
for pid in sorted(page_glyphs.keys()):
    glyphs = page_glyphs[pid]
    if glyphs:
        xs = [g['cx'] for g in glyphs]
        ys = [g['cy'] for g in glyphs]
        print(f"  {pid}: x={min(xs):.0f}-{max(xs):.0f} (Δ={max(xs)-min(xs):.0f})  y={min(ys):.0f}-{max(ys):.0f} (Δ={max(ys)-min(ys):.0f})")
