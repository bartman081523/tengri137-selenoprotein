"""
Stufe 4 — Die 332 Unknown-Glyphen.

Frage: Wo konzentrieren sich die 332 Unbekannten, was unterscheidet sie?

Methode:
  1) Page × Region-Typ für type_hint=unknown
  2) Cluster-ID-Verteilung
  3) Vision-Kind-Verteilung (gibt es welche MIT Vision-Kind aber type_hint=unknown?)
  4) Geometrie (size, fill_ratio, n_components)
  5) Vergleich Unbekannt vs. Bekannt
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs')
with open(BASE / 'doc.json') as f:
    doc = json.load(f)

# Sammler
unknown_page = Counter()
unknown_region = Counter()
unknown_rt = Counter()  # region_type
unknown_vk = Counter()  # vision_kind
unknown_cluster = Counter()
unknown_size = []
unknown_fill = []
unknown_nc = []
unknown_samples = []  # erste 30 für Inspektion

known_page = Counter()
known_count = Counter()

for p in doc['pages']:
    pid = p['page_id']
    for r in p['regions']:
        rt = r.get('region_type', '?')
        for g in r.get('glyphs', []):
            th = g.get('type_hint', '?')
            cid = g.get('cluster_id', '?')
            vk = g.get('vision_kind', '?')
            known_count[th] += 1
            if th == 'unknown':
                unknown_page[pid] += 1
                unknown_rt[rt] += 1
                unknown_cluster[cid] += 1
                if vk and vk != '?':
                    unknown_vk[vk] += 1
                sp = g.get('size_px', 0)
                fr = g.get('fill_ratio', 0)
                nc = g.get('n_components', 0)
                if sp: unknown_size.append(sp)
                if fr: unknown_fill.append(fr)
                if nc: unknown_nc.append(nc)
                if len(unknown_samples) < 30:
                    unknown_samples.append({
                        'page': pid,
                        'region': r['region_id'],
                        'glyph_index': g.get('glyph_index'),
                        'cluster_id': cid,
                        'vision_kind': vk,
                        'size_px': sp,
                        'fill_ratio': fr,
                        'n_components': nc,
                    })
            else:
                known_page[pid] += 1

# === REPORT ===
print("=" * 80)
print("STUFE 4 — DIE 332 UNKNOWN-GLYPHEN")
print("=" * 80)
print()

# 1) Total-Verteilung
print("=" * 80)
print("1) TOTAL-VERTEILUNG type_hint")
print("=" * 80)
for th, c in known_count.most_common():
    print(f"  {th:25s}: {c:4d}  ({100*c/sum(known_count.values()):.1f}%)")
print(f"  TOTAL: {sum(known_count.values())} Glyphen")
print()

# 2) Unknown pro Page
print("=" * 80)
print("2) UNKNOWN PRO PAGE")
print("=" * 80)
print(f"{'Page':<6} {'Unknown':>8} {'Known':>8} {'Total':>8} {'%U':>6}")
for pid in sorted(set(list(unknown_page.keys()) + list(known_page.keys()))):
    u = unknown_page.get(pid, 0)
    k = known_page.get(pid, 0)
    t = u + k
    pct = 100 * u / t if t else 0
    print(f"{pid:<6} {u:>8} {k:>8} {t:>8} {pct:>5.1f}%")
print()

# 3) Unknown pro Region-Type
print("=" * 80)
print("3) UNKNOWN PRO REGION-TYPE")
print("=" * 80)
for rt, c in unknown_rt.most_common():
    print(f"  {rt:25s}: {c:4d}")
print()

# 4) Unknown pro Cluster-ID
print("=" * 80)
print("4) UNKNOWN PRO CLUSTER-ID")
print("=" * 80)
for cid, c in unknown_cluster.most_common():
    print(f"  {cid:50s}: {c:4d}")
print()

# 5) Vision-Kind der Unbekannten
print("=" * 80)
print("5) VISION-KIND DER UNBEKANNTEN")
print("=" * 80)
print(f"  Glyphen MIT Vision-Kind (vk != None):  {sum(unknown_vk.values())}")
print(f"  Glyphen OHNE Vision-Kind:              {sum(known_count.values()) - known_count.get('unknown', 0) - sum(unknown_vk.values())}")
print()
print("  Vision-Kinds der Unbekannten:")
for vk, c in unknown_vk.most_common():
    print(f"    {vk:35s}: {c:4d}")
print()

# 6) Geometrie der Unbekannten
print("=" * 80)
print("6) GEOMETRIE DER UNBEKANNTEN")
print("=" * 80)
if unknown_size:
    s_med = sorted(unknown_size)[len(unknown_size)//2]
    s_min = min(unknown_size)
    s_max = max(unknown_size)
    print(f"  size_px:    n={len(unknown_size)}, min={s_min}, max={s_max}, median={s_med}")
if unknown_fill:
    f_med = sorted(unknown_fill)[len(unknown_fill)//2]
    f_min = min(unknown_fill)
    f_max = max(unknown_fill)
    print(f"  fill_ratio: n={len(unknown_fill)}, min={f_min:.3f}, max={f_max:.3f}, median={f_med:.3f}")
if unknown_nc:
    nc_med = sorted(unknown_nc)[len(unknown_nc)//2]
    nc_min = min(unknown_nc)
    nc_max = max(unknown_nc)
    print(f"  n_components: n={len(unknown_nc)}, min={nc_min}, max={nc_max}, median={nc_med}")
print()

# 7) Stichprobe der Unbekannten
print("=" * 80)
print("7) STICHPROBE (erste 30 Unbekannte)")
print("=" * 80)
for s in unknown_samples:
    print(f"  {s['page']} {s['region']:25s} idx={s['glyph_index']:4d}  cluster={s['cluster_id']:50s}  vk={s['vision_kind']}  size={s['size_px']}  fill={s['fill_ratio']:.3f}  nc={s['n_components']}")
print()

# 8) Frage: p18 komplett unknown?
print("=" * 80)
print("8) P18 — 0 LATIN, 24 GLYPHEN")
print("=" * 80)
p18_glyphs = []
for p in doc['pages']:
    if p['page_id'] == 'p18':
        for r in p['regions']:
            for g in r.get('glyphs', []):
                p18_glyphs.append(g)
print(f"  p18 hat {len(p18_glyphs)} Glyphen")
unknowns_on_p18 = sum(1 for g in p18_glyphs if g.get('type_hint') == 'unknown')
print(f"  davon type_hint=unknown: {unknowns_on_p18}  ({100*unknowns_on_p18/max(len(p18_glyphs),1):.1f}%)")
print()
print("  Verteilung der type_hints auf p18:")
p18_th = Counter()
for g in p18_glyphs:
    p18_th[g.get('type_hint', '?')] += 1
for th, c in p18_th.most_common():
    print(f"    {th:25s}: {c}")
print()
print("  Verteilung der vision_kinds auf p18:")
p18_vk = Counter()
for g in p18_glyphs:
    vk = g.get('vision_kind')
    if vk:
        p18_vk[vk] += 1
for vk, c in p18_vk.most_common():
    print(f"    {vk:35s}: {c}")
print()

# JSON Export
out = {
    'totals': dict(known_count),
    'unknown_per_page': dict(unknown_page),
    'unknown_per_rt': dict(unknown_rt),
    'unknown_per_cluster': dict(unknown_cluster),
    'unknown_with_vk': dict(unknown_vk),
    'samples': unknown_samples,
    'p18_glyphs': len(p18_glyphs),
    'p18_unknown': unknowns_on_p18,
    'p18_type_hints': dict(p18_th),
    'p18_vision_kinds': dict(p18_vk),
}
with open(BASE.parent / 'scratches' / 'stufe_04' / 'unknowns.json', 'w') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"Unknown-JSON: scratches/stufe_04/unknowns.json")
