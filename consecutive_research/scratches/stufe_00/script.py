"""
Stufe 0 — Topologie der V4-Daten.

Was wir haben:
  - 23 Seiten, jede mit regions[] (glyphs + latin_tokens)
  - 17 vision_kinds (Symbol-Typologie)
  - 24 distinkte Cluster-IDs
  - 456 Latin-Tokens aus 3 Quellen
  - 997 Glyphen total

Frage: Wie verteilen sich diese Dinge?
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs')
with open(BASE / 'doc.json') as f:
    doc = json.load(f)

# Collectors
region_types = Counter()
vision_kinds = Counter()
cluster_ids = Counter()
glyph_type_hints = Counter()
latin_sources = Counter()
glyphs_per_page = Counter()
glyphs_per_region_type = Counter()
glyphs_per_vision_kind = Counter()
glyphs_per_cluster = defaultdict(list)  # cluster_id -> [glyph_index, ...]

# Latin-Token-Geometrie: source × region_type
latin_geo = Counter()  # (source, region_type) -> count

# Vision-Token pro Page
vision_latin_per_page = Counter()

# Geometrie: size_px und fill_ratio Verteilungen
sizes = []
ratios = []
n_components_dist = Counter()

# Glyphen ohne Vision-Description
glyphs_no_vision = 0
glyphs_with_vision = 0

# Latin-Tokens mit hohem Vision-Conf (>0.8)
high_conf_vision_latin = []

for p in doc['pages']:
    pid = p['page_id']
    for r in p['regions']:
        rt = r.get('region_type', '?')
        region_types[rt] += 1
        for g in r.get('glyphs', []):
            glyphs_per_page[pid] += 1
            glyphs_per_region_type[rt] += 1
            vk = g.get('vision_kind')
            if vk:
                vision_kinds[vk] += 1
                glyphs_per_vision_kind[vk] += 1
            cid = g.get('cluster_id', '?')
            cluster_ids[cid] += 1
            glyphs_per_cluster[cid].append(g.get('glyph_index'))
            glyph_type_hints[g.get('type_hint', '?')] += 1
            sp = g.get('size_px', 0)
            fr = g.get('fill_ratio', 0)
            if sp:
                sizes.append(sp)
            if fr:
                ratios.append(fr)
            nc = g.get('n_components', 0)
            n_components_dist[nc] += 1
            if g.get('vision_description'):
                glyphs_with_vision += 1
            else:
                glyphs_no_vision += 1
        for lt in r.get('latin_tokens', []):
            src = lt.get('source', '?')
            latin_sources[src] += 1
            latin_geo[(src, rt)] += 1
            if src == 'vision' and lt.get('conf', 0) > 0.8:
                high_conf_vision_latin.append((pid, r['region_id'], lt.get('text', ''), lt.get('conf')))

# === REPORT ===
print("=" * 70)
print("STUFE 0 — TOPOLOGIE DER V4-DATEN")
print("=" * 70)
print()
print(f"Pages: {len(doc['pages'])}")
print(f"Schema version: {doc['schema_version']}")
print(f"Pipeline: {doc['document'].get('pipeline_version')}")
print(f"Run: {doc['document'].get('processing_run')}")
print()

print("=" * 70)
print("1) REGION-TYPES (über alle Seiten)")
print("=" * 70)
for rt, c in region_types.most_common():
    print(f"  {rt:25s}: {c:4d}  ({100*c/sum(region_types.values()):.1f}%)")
print(f"  TOTAL: {sum(region_types.values())} Regionen")
print()

print("=" * 70)
print("2) VISION-KINDS (Symbol-Taxonomie, 17 distinkt)")
print("=" * 70)
for vk, c in vision_kinds.most_common():
    print(f"  {vk:35s}: {c:4d}  ({100*c/sum(vision_kinds.values()):.1f}%)")
print(f"  TOTAL: {sum(vision_kinds.values())} Glyphen MIT Vision-Description")
print(f"  Glyphen OHNE Vision-Description: {glyphs_no_vision}")
print()

print("=" * 70)
print("3) GLYPH-TYPE-HINTS (geometry classification)")
print("=" * 70)
for th, c in glyph_type_hints.most_common():
    print(f"  {th:25s}: {c:4d}")
print()

print("=" * 70)
print("4) LATIN-TOKEN-QUELLEN")
print("=" * 70)
for src, c in latin_sources.most_common():
    print(f"  {src:25s}: {c:4d}")
print(f"  TOTAL: {sum(latin_sources.values())} Latin-Tokens")
print()

print("=" * 70)
print("5) LATIN × REGION-TYPE (Top 15 Kombinationen)")
print("=" * 70)
for (src, rt), c in latin_geo.most_common(15):
    print(f"  {src:20s} × {rt:25s}: {c:4d}")
print()

print("=" * 70)
print("6) GLYPHEN PRO PAGE")
print("=" * 70)
for pid in sorted(glyphs_per_page.keys()):
    print(f"  {pid}: {glyphs_per_page[pid]:4d} Glyphen")
print()

print("=" * 70)
print("7) CLUSTER-IDS (24 distinkt, mit Größe)")
print("=" * 70)
for cid, c in sorted(cluster_ids.items(), key=lambda x: -x[1]):
    print(f"  {cid:50s}: {c:4d}  (glyph_index {min(glyphs_per_cluster[cid])}-{max(glyphs_per_cluster[cid])})")
print()

print("=" * 70)
print("8) GEOMETRIE-VERTEILUNGEN (size_px, fill_ratio, n_components)")
print("=" * 70)
print(f"  size_px:     n={len(sizes)}, min={min(sizes)}, max={max(sizes)}, median={sorted(sizes)[len(sizes)//2]}")
print(f"  fill_ratio:  n={len(ratios)}, min={min(ratios):.3f}, max={max(ratios):.3f}, median={sorted(ratios)[len(ratios)//2]:.3f}")
print(f"  n_components: {dict(n_components_dist)}")
print()

print("=" * 70)
print("9) HIGH-CONFIDENCE VISION-LATIN (conf > 0.8)")
print("=" * 70)
for pid, rid, txt, conf in high_conf_vision_latin[:20]:
    print(f"  {pid} {rid} conf={conf}: {txt[:80]}")
print(f"  ... ({len(high_conf_vision_latin)} total)")
print()

# JSON export für weitere Stufen
import json
out = {
    'totals': {
        'pages': len(doc['pages']),
        'regions': sum(region_types.values()),
        'glyphs_total': sum(glyphs_per_page.values()),
        'glyphs_with_vision': glyphs_with_vision,
        'glyphs_without_vision': glyphs_no_vision,
        'latin_tokens': sum(latin_sources.values()),
    },
    'region_types': dict(region_types),
    'vision_kinds': dict(vision_kinds),
    'cluster_ids': dict(cluster_ids),
    'glyph_type_hints': dict(glyph_type_hints),
    'latin_sources': dict(latin_sources),
    'glyphs_per_page': dict(glyphs_per_page),
    'glyphs_per_region_type': dict(glyphs_per_region_type),
    'glyphs_per_vision_kind': dict(glyphs_per_vision_kind),
    'latin_geo': {f"{s}|{rt}": c for (s, rt), c in latin_geo.items()},
    'high_conf_vision_latin': [
        {'page': pid, 'region': rid, 'text': txt, 'conf': conf}
        for pid, rid, txt, conf in high_conf_vision_latin
    ],
}
with open(BASE.parent / 'scratches' / 'stufe_00' / 'topologie.json', 'w') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"\nTopologie-JSON: scratches/stufe_00/topologie.json")
