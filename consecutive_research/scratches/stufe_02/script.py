"""
Stufe 2 — Vision-Kinds Taxonomie + Geometrie.

Frage: Welche Vision-Kinds sind CONTAINER, INHALT, MATH, IKONEN, TRENNER?

Methode:
  1) Vision-Kind × Region-Typ Matrix
  2) Vision-Kind × Page Verteilung
  3) Vision-Kind × Geometrie (size_px, fill_ratio, n_components)
  4) Vision-Kind × Cluster-ID
  5) Klassifikations-Vorschlag
"""
import json
from collections import Counter, defaultdict
from pathlib import Path
import statistics

BASE = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs')
with open(BASE / 'doc.json') as f:
    doc = json.load(f)

# Sammler
vk_region = defaultdict(Counter)  # vk -> {rt: count}
vk_page = defaultdict(Counter)  # vk -> {pid: count}
vk_size = defaultdict(list)
vk_fill = defaultdict(list)
vk_nc = defaultdict(list)
vk_cluster = defaultdict(Counter)  # vk -> {cluster_id: count}
vk_count = Counter()  # vk -> total

# Alle Vision-Kinds
all_vk = set()

for p in doc['pages']:
    pid = p['page_id']
    for r in p['regions']:
        rt = r.get('region_type', '?')
        for g in r.get('glyphs', []):
            vk = g.get('vision_kind')
            if vk is None:
                continue
            all_vk.add(vk)
            vk_count[vk] += 1
            vk_region[vk][rt] += 1
            vk_page[vk][pid] += 1
            sp = g.get('size_px', 0)
            fr = g.get('fill_ratio', 0)
            nc = g.get('n_components', 0)
            if sp: vk_size[vk].append(sp)
            if fr: vk_fill[vk].append(fr)
            if nc: vk_nc[vk].append(nc)
            cid = g.get('cluster_id', '?')
            vk_cluster[vk][cid] += 1

# === REPORT ===
print("=" * 80)
print("STUFE 2 — VISION-KINDS TAXONOMIE + GEOMETRIE")
print("=" * 80)
print()

# 1) Region-Typ × Vision-Kind
print("=" * 80)
print("1) VISION-KIND × REGION-TYP (Top Kombinationen)")
print("=" * 80)
combo = Counter()
for vk, rts in vk_region.items():
    for rt, c in rts.items():
        combo[(vk, rt)] = c
for (vk, rt), c in combo.most_common(30):
    print(f"  {vk:35s} × {rt:20s}: {c:3d}")
print()

# 2) Vision-Kind × Page
print("=" * 80)
print("2) VISION-KIND × PAGE (welche Vkinds auf welchen Seiten?)")
print("=" * 80)
print(f"{'Vk':<35}" + "".join(f"{p:>5}" for p in sorted({pid for vks in vk_page.values() for pid in vks.keys()})))
for vk in sorted(vk_count.keys(), key=lambda x: -vk_count[x]):
    pages = vk_page[vk]
    cells = "".join(f"{pages.get(p, 0):>5}" for p in sorted(pages.keys()))
    total = sum(pages.values())
    print(f"{vk:<35}{cells}  ={total}")
print()

# 3) Geometrie pro Vision-Kind
print("=" * 80)
print("3) GEOMETRIE PRO VISION-KIND")
print("=" * 80)
print(f"{'Vk':<35} {'n':>4}  {'size_med':>10}  {'fill_med':>10}  {'nc_med':>8}")
for vk in sorted(vk_count.keys(), key=lambda x: -vk_count[x]):
    sizes = vk_size[vk]
    fills = vk_fill[vk]
    ncs = vk_nc[vk]
    if sizes:
        size_med = sorted(sizes)[len(sizes)//2]
    else:
        size_med = 0
    if fills:
        fill_med = sorted(fills)[len(fills)//2]
    else:
        fill_med = 0
    if ncs:
        nc_med = sorted(ncs)[len(ncs)//2]
    else:
        nc_med = 0
    print(f"{vk:<35} {vk_count[vk]:>4}  {size_med:>10}  {fill_med:>10.3f}  {nc_med:>8}")
print()

# 4) Vision-Kind × Cluster-ID
print("=" * 80)
print("4) VISION-KIND × CLUSTER-ID (Top Kombinationen)")
print("=" * 80)
vk_cluster_combo = Counter()
for vk, cids in vk_cluster.items():
    for cid, c in cids.items():
        vk_cluster_combo[(vk, cid)] = c
for (vk, cid), c in vk_cluster_combo.most_common(20):
    print(f"  {vk:30s} × {cid:50s}: {c:3d}")
print()

# 5) Klassifikations-Vorschlag
print("=" * 80)
print("5) KLASSIFIKATIONS-VERSUCH (CONTAINER / INHALT / MATH / IKONE / TRENNER / UNKLAR)")
print("=" * 80)

# Heuristik:
# CONTAINER: oft in latin_text, oft Page-übergreifend, hohe Anzahl
# INHALT: hohe Anzahl, über Pages verteilt
# MATH: spezielle Namen, niedrige Anzahl, oft in formula_block
# IKONE: sehr niedrige Anzahl, oft in graphic_line oder magic_cube
# TRENNER: linienartig

classification = {}
for vk in sorted(vk_count.keys(), key=lambda x: -vk_count[x]):
    n = vk_count[vk]
    regions = vk_region[vk]
    pages = vk_page[vk]
    n_pages = len(pages)

    # IKONE: < 3 Glyphen
    if n <= 3 and 'magic' in vk or 'horn' in vk:
        classification[vk] = 'IKONE'
    # MATH: math_*
    elif vk.startswith('math_'):
        classification[vk] = 'MATH'
    # CONTAINER: geometric_bracket (Klammern)
    elif 'bracket' in vk:
        classification[vk] = 'CONTAINER'
    # TRENNER: line
    elif vk == 'line':
        classification[vk] = 'TRENNER'
    # IKONE: magic_cube, horn
    elif 'cube' in vk or 'horn' in vk:
        classification[vk] = 'IKONE'
    # INHALT: digits
    elif vk == 'digit':
        classification[vk] = 'INHALT-ZAHL'
    # INHALT: turkic, diamond, circle, square, punctum
    elif vk in ('turkic_round_rune', 'geometric_diamond', 'geometric_diamond_with_dot',
                'geometric_circle', 'geometric_circle_with_dot', 'geometric_filled_square',
                'punctum'):
        classification[vk] = 'INHALT'
    else:
        classification[vk] = 'UNKLAR'

for vk in sorted(vk_count.keys(), key=lambda x: -vk_count[x]):
    print(f"  {vk:35s} n={vk_count[vk]:3d}  →  {classification[vk]}")
print()

# 6) Spezielle 1er-Glyphen
print("=" * 80)
print("6) SPEZIELLE 1-er VISION-KINDS (Ikone, Sonderfälle)")
print("=" * 80)
for vk in [v for v, c in vk_count.items() if c <= 5]:
    pages = vk_page[vk]
    regions = vk_region[vk]
    print(f"  {vk} (n={vk_count[vk]})")
    for p, c in pages.items():
        for rt, rc in regions.items():
            print(f"    → {p} × {rt}: {rc}×")
print()

# JSON Export
out = {
    'vk_count': dict(vk_count),
    'vk_region': {vk: dict(rts) for vk, rts in vk_region.items()},
    'vk_page': {vk: dict(pages) for vk, pages in vk_page.items()},
    'vk_size_median': {vk: sorted(s)[len(s)//2] if s else 0 for vk, s in vk_size.items()},
    'vk_fill_median': {vk: sorted(f)[len(f)//2] if f else 0 for vk, f in vk_fill.items()},
    'vk_nc_median': {vk: sorted(n)[len(n)//2] if n else 0 for vk, n in vk_nc.items()},
    'vk_cluster': {vk: dict(cids) for vk, cids in vk_cluster.items()},
    'classification': classification,
}
with open(BASE.parent / 'scratches' / 'stufe_02' / 'vision_taxonomie.json', 'w') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"Taxonomie-JSON: scratches/stufe_02/vision_taxonomie.json")
