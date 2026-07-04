"""
Stufe 7 — Geometrische Familien.

Frage: Welche Glyphen 'gehören zusammen' jenseits der 24 Cluster?

Methode:
  1) Größen-/fill_ratio-/n_components-Verteilungen pro Cluster
  2) Identifikation von geometrischen Familien (size/fill/nc)
  3) Korrelation Cluster × Vision-Kind × type_hint
  4) Sub-Cluster-Analyse der grossen Cluster
"""
import json
from collections import Counter, defaultdict
from pathlib import Path
import statistics

BASE = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs')
with open(BASE / 'doc.json') as f:
    doc = json.load(f)

# Sammler pro Cluster
cluster_data = defaultdict(lambda: {'sizes': [], 'fills': [], 'ncs': [],
                                     'vk': Counter(), 'th': Counter(), 'count': 0})

# Sammler pro Vision-Kind
vk_data = defaultdict(lambda: {'sizes': [], 'fills': [], 'ncs': []})

# Sammler pro type_hint
th_data = defaultdict(lambda: {'sizes': [], 'fills': [], 'ncs': []})

all_glyphs = []

for p in doc['pages']:
    pid = p['page_id']
    for r in p['regions']:
        for g in r.get('glyphs', []):
            cid = g.get('cluster_id', '?')
            vk = g.get('vision_kind')
            th = g.get('type_hint', '?')
            sp = g.get('size_px', 0)
            fr = g.get('fill_ratio', 0)
            nc = g.get('n_components', 0)

            cluster_data[cid]['sizes'].append(sp)
            cluster_data[cid]['fills'].append(fr)
            cluster_data[cid]['ncs'].append(nc)
            cluster_data[cid]['vk'][vk] += 1 if vk else 0
            cluster_data[cid]['th'][th] += 1
            cluster_data[cid]['count'] += 1

            if vk:
                vk_data[vk]['sizes'].append(sp)
                vk_data[vk]['fills'].append(fr)
                vk_data[vk]['ncs'].append(nc)

            th_data[th]['sizes'].append(sp)
            th_data[th]['fills'].append(fr)
            th_data[th]['ncs'].append(nc)

            all_glyphs.append({
                'page': pid,
                'region': r['region_id'],
                'glyph_index': g.get('glyph_index'),
                'cluster': cid,
                'vk': vk,
                'th': th,
                'size_px': sp,
                'fill_ratio': fr,
                'n_components': nc,
            })

# === REPORT ===
print("=" * 80)
print("STUFE 7 — GEOMETRISCHE FAMILIEN")
print("=" * 80)
print()

# 1) Pro Cluster: Median size/fill/nc + Vision-Kind-Verteilung
print("=" * 80)
print("1) PRO CLUSTER (sortiert nach Grösse)")
print("=" * 80)
print(f"{'Cluster':<55} {'n':>4}  {'size_med':>10}  {'fill_med':>10}  {'nc_med':>8}  {'top_vk':<25}")
for cid in sorted(cluster_data.keys(), key=lambda x: -cluster_data[x]['count']):
    d = cluster_data[cid]
    sizes = sorted(d['sizes'])
    fills = sorted(d['fills'])
    ncs = sorted(d['ncs'])
    s_med = sizes[len(sizes)//2] if sizes else 0
    f_med = fills[len(fills)//2] if fills else 0
    nc_med = ncs[len(ncs)//2] if ncs else 0
    top_vk = d['vk'].most_common(1)[0] if d['vk'] else ('?', 0)
    top_vk_str = f"{top_vk[0]}({top_vk[1]})" if top_vk[0] else 'none'
    print(f"{cid:<55} {d['count']:>4}  {s_med:>10}  {f_med:>10.3f}  {nc_med:>8}  {top_vk_str:<25}")
print()

# 2) Familien-Identifikation nach Grösse/Fill
print("=" * 80)
print("2) GEOMETRISCHE FAMILIEN (size_px × fill_ratio)")
print("=" * 80)
print()
print("Schwellen:")
print("  - winzig: size < 200")
print("  - klein:  200 <= size < 1000")
print("  - mittel: 1000 <= size < 5000")
print("  - gross:  5000 <= size < 20000")
print("  - kolossal: size >= 20000")
print("  - luftig:  fill < 0.2")
print("  - normal:  0.2 <= fill < 0.5")
print("  - voll:    fill >= 0.5")
print()

families = {
    'KOLOSSAL_LUFTIG': [],
    'KOLOSSAL_NORMAL': [],
    'GROSS_LUFTIG': [],
    'GROSS_NORMAL': [],
    'GROSS_VOLL': [],
    'MITTEL_LUFTIG': [],
    'MITTEL_NORMAL': [],
    'MITTEL_VOLL': [],
    'KLEIN_NORMAL': [],
    'KLEIN_VOLL': [],
    'WINZIG': [],
}
for g in all_glyphs:
    s = g['size_px']
    f = g['fill_ratio']
    if s >= 20000 and f < 0.2: families['KOLOSSAL_LUFTIG'].append(g)
    elif s >= 20000: families['KOLOSSAL_NORMAL'].append(g)
    elif s >= 5000 and f < 0.2: families['GROSS_LUFTIG'].append(g)
    elif s >= 5000 and f < 0.5: families['GROSS_NORMAL'].append(g)
    elif s >= 5000: families['GROSS_VOLL'].append(g)
    elif s >= 1000 and f < 0.2: families['MITTEL_LUFTIG'].append(g)
    elif s >= 1000 and f < 0.5: families['MITTEL_NORMAL'].append(g)
    elif s >= 1000: families['MITTEL_VOLL'].append(g)
    elif s >= 200: families['KLEIN_NORMAL'].append(g) if f < 0.5 else families['KLEIN_VOLL'].append(g)
    else: families['WINZIG'].append(g)

for fam, glyphs in families.items():
    if glyphs:
        print(f"  {fam:20s}: {len(glyphs):3d} Glyphen")
print()
print("Beispiele je Familie:")
for fam, glyphs in families.items():
    if glyphs:
        print(f"\n  {fam} ({len(glyphs)}):")
        for g in glyphs[:5]:
            print(f"    {g['page']} {g['region']:25s} idx={g['glyph_index']:3d} size={g['size_px']:5d} fill={g['fill_ratio']:.3f} nc={g['n_components']:3d} cluster={g['cluster']}")
print()

# 3) Korrelation: Vision-Kind vs. Cluster (für die grossen Cluster)
print("=" * 80)
print("3) VISION-KIND × CLUSTER (für die grossen Cluster)")
print("=" * 80)
print()
for cid in ['GEOM_MEDIUM_MATH_TIMES_0018', 'GEOM_MEDIUM_GEOMETRIC_CIRCLE_WIT_0008',
            'GEOM_MEDIUM_PUNCTUM_0013', 'GEOM_MEDIUM_TURKIC_ROUND_RUNE_0010',
            'GEOM_MEDIUM_UNKNOWN_0003', 'GEOM_MEDIUM_UNKNOWN_0002']:
    if cid in cluster_data:
        d = cluster_data[cid]
        vks = d['vk']
        print(f"  {cid}  (n={d['count']})")
        for vk, c in vks.most_common():
            print(f"    vk={vk}: {c}")
        print()

# 4) Sub-Cluster innerhalb MATH_TIMES_0018
print("=" * 80)
print("4) SUB-ANALYSE: MATH_TIMES_0018 (294 Glyphen)")
print("=" * 80)
math_times_glyphs = [g for g in all_glyphs if g['cluster'] == 'GEOM_MEDIUM_MATH_TIMES_0018']
print(f"  Total: {len(math_times_glyphs)}")
# Verteilung n_components
nc_dist = Counter(g['n_components'] for g in math_times_glyphs)
print("  n_components Verteilung:")
for nc, c in sorted(nc_dist.items()):
    print(f"    nc={nc}: {c}")
print()

# Verteilung size_px
size_buckets = Counter()
for g in math_times_glyphs:
    s = g['size_px']
    if s < 200: b = '<200'
    elif s < 1000: b = '200-999'
    elif s < 5000: b = '1000-4999'
    elif s < 20000: b = '5000-19999'
    else: b = '>=20000'
    size_buckets[b] += 1
print("  size_px Verteilung:")
for b in ['<200', '200-999', '1000-4999', '5000-19999', '>=20000']:
    print(f"    {b}: {size_buckets[b]}")
print()

# 5) Vergleich Glyphen MIT vs OHNE Vision-Description
print("=" * 80)
print("5) GLYPHEN MIT vs OHNE VISION-DESCRIPTION")
print("=" * 80)
with_desc = [g for g in all_glyphs if g['vk']]
without_desc = [g for g in all_glyphs if not g['vk']]

print(f"  MIT Vision-Description:  {len(with_desc)}")
sizes_w = sorted([g['size_px'] for g in with_desc])
fills_w = sorted([g['fill_ratio'] for g in with_desc if g['fill_ratio']])
print(f"    size_px median: {sizes_w[len(sizes_w)//2]}")
print(f"    fill_ratio median: {fills_w[len(fills_w)//2]:.3f}")

print(f"  OHNE Vision-Description: {len(without_desc)}")
sizes_wo = sorted([g['size_px'] for g in without_desc])
fills_wo = sorted([g['fill_ratio'] for g in without_desc if g['fill_ratio']])
print(f"    size_px median: {sizes_wo[len(sizes_wo)//2]}")
print(f"    fill_ratio median: {fills_wo[len(fills_wo)//2]:.3f}")
print()

# 6) n_components Verteilung (Achtung: vorher 637 dominierte)
print("=" * 80)
print("6) n_components-VERTEILUNG (AUF 1-100 beschränkt, ohne Ausreisser)")
print("=" * 80)
nc_counter = Counter(g['n_components'] for g in all_glyphs if g['n_components'] <= 100)
for nc in sorted(nc_counter.keys()):
    bar = chr(0x2588) * min(nc_counter[nc], 100)
    print(f"  nc={nc:3d}: {nc_counter[nc]:4d}  {bar}")
print()

# JSON Export
out = {
    'cluster_stats': {
        cid: {
            'count': d['count'],
            'size_med': sorted(d['sizes'])[len(d['sizes'])//2] if d['sizes'] else 0,
            'fill_med': sorted(d['fills'])[len(d['fills'])//2] if d['fills'] else 0,
            'nc_med': sorted(d['ncs'])[len(d['ncs'])//2] if d['ncs'] else 0,
            'vk_top': d['vk'].most_common(3),
            'th_top': d['th'].most_common(3),
        }
        for cid, d in cluster_data.items()
    },
    'families': {fam: len(g) for fam, g in families.items()},
    'with_desc': len(with_desc),
    'without_desc': len(without_desc),
}
with open(BASE.parent / 'scratches' / 'stufe_07' / 'families.json', 'w') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"Familien-JSON: scratches/stufe_07/families.json")
