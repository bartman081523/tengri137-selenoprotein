"""
Stufe 9 — Co-Occurrence Matrix.

Frage: Welche Vision-Kinds erscheinen IMMER zusammen, welche NIE?

Methode:
  1) Pro Region: alle Vision-Kinds sammeln
  2) Co-Occurrence-Matrix (welche Paarungen kommen zusammen vor)
  3) Pflicht-Paarungen (immer zusammen)
  4) Verbotene Paarungen (nie zusammen, obwohl einzeln häufig)
"""
import json
from collections import Counter, defaultdict
from pathlib import Path
import itertools

BASE = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs')
with open(BASE / 'doc.json') as f:
    doc = json.load(f)

# Sammle pro Region die Vision-Kinds (als SET)
region_vks = defaultdict(set)
region_vk_list = defaultdict(list)  # multiset für Häufigkeit
for p in doc['pages']:
    for r in p['regions']:
        for g in r.get('glyphs', []):
            vk = g.get('vision_kind')
            if vk:
                region_vks[r['region_id']].add(vk)
                region_vk_list[r['region_id']].append(vk)

# Vision-Kind-Vorkommen
vk_count = Counter()
for vks in region_vk_list.values():
    for vk in vks:
        vk_count[vk] += 1

# === REPORT ===
print("=" * 80)
print("STUFE 9 — CO-OCCURRENCE MATRIX DER VISION-KINDS")
print("=" * 80)
print()

# 1) Vision-Kind-Vorkommen
print("=" * 80)
print("1) VISION-KIND VORKOMMEN")
print("=" * 80)
for vk, c in vk_count.most_common():
    print(f"  {vk:35s}: {c:3d} Glyphen")
print()

# 2) Co-Occurrence (SET-basiert, d.h. paarweise in derselben Region)
print("=" * 80)
print("2) CO-OCCURRENCE (gleiche Region, paarweise)")
print("=" * 80)
coocc = Counter()
for rid, vks in region_vks.items():
    vks_list = sorted(vks)
    for i, vk1 in enumerate(vks_list):
        for vk2 in vks_list[i+1:]:
            coocc[(vk1, vk2)] += 1

for (vk1, vk2), c in coocc.most_common(30):
    print(f"  {vk1:30s} + {vk2:30s}: {c}")
print()

# 3) Vollständige Co-Occurrence-Matrix
print("=" * 80)
print("3) VOLLSTÄNDIGE CO-OCCURRENCE-MATRIX (Zeilen × Spalten)")
print("=" * 80)
all_vks = sorted(vk_count.keys(), key=lambda x: -vk_count[x])
# Header
header = "VK".ljust(15) + "".join(vk[:6].ljust(7) for vk in all_vks)
print(header)
# Matrix
for vk1 in all_vks:
    row = vk1[:14].ljust(15)
    for vk2 in all_vks:
        if vk1 == vk2:
            row += "  -   "
        else:
            c = coocc.get(tuple(sorted([vk1, vk2])), 0)
            row += f"{c:>6} "
    print(row)
print()

# 4) Jaccard-Index: wie ähnlich sind die Regions-Sets?
print("=" * 80)
print("4) JACCARD-ÄHNLICHKEIT DER VISION-KIND-VERTEILUNGEN")
print("=" * 80)
# Welche Vision-Kinds kommen in den GLEICHEN Regionen vor?
vk_in_regions = defaultdict(set)
for rid, vks in region_vks.items():
    for vk in vks:
        vk_in_regions[vk].add(rid)

print("\nTop Jaccard-Paarungen (≥0.3):")
pairings = []
for vk1, vk2 in itertools.combinations(all_vks, 2):
    r1 = vk_in_regions[vk1]
    r2 = vk_in_regions[vk2]
    if r1 and r2:
        j = len(r1 & r2) / len(r1 | r2)
        if j >= 0.2:
            pairings.append((vk1, vk2, j, len(r1 & r2), len(r1 | r2)))
pairings.sort(key=lambda x: -x[2])
for vk1, vk2, j, common, union in pairings[:20]:
    print(f"  {vk1:30s} + {vk2:30s}: J={j:.3f}  (common={common}, union={union})")
print()

# 5) Verbotene Paarungen (einzeln häufig, aber nie zusammen)
print("=" * 80)
print("5) 'VERBOTENE' PAARUNGEN (einzeln ≥5 Vorkommen, aber 0× zusammen)")
print("=" * 80)
for vk1, vk2 in itertools.combinations(all_vks, 2):
    if vk_count[vk1] >= 5 and vk_count[vk2] >= 5:
        if coocc.get(tuple(sorted([vk1, vk2])), 0) == 0:
            print(f"  {vk1:30s} + {vk2:30s}:  NIE zusammen (vk1={vk_count[vk1]}, vk2={vk_count[vk2]})")
print()

# 6) Welche Regionen haben die meisten Vks?
print("=" * 80)
print("6) REGIONEN MIT MEISTEN VISION-KINDS")
print("=" * 80)
region_vk_count = [(rid, len(vks), vks) for rid, vks in region_vks.items()]
for rid, n, vks in sorted(region_vk_count, key=lambda x: -x[1])[:15]:
    print(f"  {rid:25s}: {n} Vks  ({', '.join(sorted(vks))})")
print()

# 7) Pflicht-Paarungen
print("=" * 80)
print("7) PFLICHT-Paarungen (≥80% zusammen)")
print("=" * 80)
for vk1 in all_vks:
    r1 = vk_in_regions[vk1]
    for vk2 in all_vks:
        if vk1 == vk2:
            continue
        r2 = vk_in_regions[vk2]
        common = r1 & r2
        if r1 and len(common) / len(r1) >= 0.8 and len(common) >= 3:
            print(f"  {vk1:30s}: {len(common)}/{len(r1)} = {100*len(common)/len(r1):.0f}% seiner Regionen haben auch {vk2}")

# JSON Export
out = {
    'vk_count': dict(vk_count),
    'coocc': {f"{k[0]}|{k[1]}": v for k, v in coocc.items()},
    'vk_in_regions': {vk: sorted(rids) for vk, rids in vk_in_regions.items()},
    'region_vk_count': sorted([(rid, n) for rid, n in region_vk_count], key=lambda x: -x[1]),
}
with open(BASE.parent / 'scratches' / 'stufe_09' / 'coocc.json', 'w') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"\nCoOcc-JSON: scratches/stufe_09/coocc.json")
