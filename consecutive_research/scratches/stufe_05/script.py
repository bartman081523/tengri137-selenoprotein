"""
Stufe 5 — Magic Cube 3x3 und Ring-Sigille.

Frage: Welche Glyphen bilden die Ring-/Würfel-Sigille? Was ist ihre Geometrie?

Methode:
  1) magic_cube-Region p08_R15 (die EINZIGE magic_cube-Region)
  2) Große Unbekannte auf p09 (idx 473, 754x727) und anderswo
  3) "9 RINGS" / "7 RINGS" — wo sind die ring-förmigen Glyphen?
  4) Latin-Text auf p08_R15: KEIN lateinischer Text, aber 9 Glyphen in einer Reihe
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs')

# p08_R15 — die magic_cube-Region
with open(BASE / 'pages/p08.json') as f:
    p8 = json.load(f)

print("=" * 80)
print("P08_R15 — magic_cube-Region")
print("=" * 80)
print()

# Suche die Region
mc_region = None
for r in p8['regions']:
    if r.get('region_type') == 'magic_cube':
        mc_region = r
        break

if mc_region:
    print(f"Region: {mc_region['region_id']}")
    print(f"bbox: {mc_region.get('bbox')}")
    print(f"description: {mc_region.get('description', '')}")
    print(f"glyphs: {len(mc_region.get('glyphs', []))}")
    print(f"latin_tokens: {len(mc_region.get('latin_tokens', []))}")
    print()
    print("Glyphen (idx, x, y, w, h, vision_kind, cluster_id, type_hint, size):")
    print("-" * 80)
    for g in mc_region['glyphs']:
        bbox = g.get('bbox', [0, 0, 0, 0])
        x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
        print(f"  idx={g.get('glyph_index'):3d}  x={x:4d} y={y:4d} w={w:3d} h={h:3d}  vk={g.get('vision_kind')}  cluster={g.get('cluster_id'):50s}  th={g.get('type_hint')}")
    print()
    # Position-Sortierung
    sorted_glyphs = sorted(mc_region['glyphs'], key=lambda x: x.get('bbox', [0,0,0,0])[0])
    print("Sortiert nach X-Position (von links nach rechts):")
    for g in sorted_glyphs:
        x = g.get('bbox', [0,0,0,0])[0]
        print(f"  x={x:4d}  idx={g.get('glyph_index'):3d}  th={g.get('type_hint')}")
    print()

# === Suche nach "Ring-Glyphen" auf allen Seiten ===
print("=" * 80)
print("SUCHE: RING/ROSENKRANZ-ARTIGE GLYPHEN AUF ALLEN SEITEN")
print("=" * 80)
print()
print("Kriterien: cluster enthaelt 'CIRCLE' ODER 'TURKIC' UND (size>500 UND fill_ratio<0.4)")
print()

with open(BASE / 'doc.json') as f:
    doc = json.load(f)

# Suche alle glyphen mit großer size und CIRCLE-Cluster
for p in doc['pages']:
    pid = p['page_id']
    for r in p['regions']:
        for g in r.get('glyphs', []):
            cid = g.get('cluster_id', '')
            th = g.get('type_hint', '')
            sp = g.get('size_px', 0)
            fr = g.get('fill_ratio', 0)
            # Ringe: sehr groß, luftig
            if sp > 1000 and 'CIRCLE' in cid and fr < 0.5 and th == 'unknown':
                bbox = g.get('bbox', [0,0,0,0])
                print(f"  {pid} {r['region_id']:25s}  idx={g.get('glyph_index'):3d}  size={sp:5d}  fill={fr:.3f}  bbox={bbox}  cluster={cid}")

print()

# === Große Unbekannte (kolossale Glyphen) ===
print("=" * 80)
print("KOLOSSALE UNBEKANNTE (>10000 px size, fill < 0.3)")
print("=" * 80)
for p in doc['pages']:
    pid = p['page_id']
    for r in p['regions']:
        for g in r.get('glyphs', []):
            sp = g.get('size_px', 0)
            fr = g.get('fill_ratio', 0)
            th = g.get('type_hint', '')
            cid = g.get('cluster_id', '')
            if sp > 10000 and th == 'unknown' and fr < 0.3:
                bbox = g.get('bbox', [0,0,0,0])
                print(f"  {pid} {r['region_id']:25s}  idx={g.get('glyph_index'):3d}  size={sp:5d}  fill={fr:.3f}  bbox={bbox}  cluster={cid}")

print()

# === Vergleich p08_R15 mit p09_R6 ===
print("=" * 80)
print("P09_R6 — die '7 RINGS'-Region?")
print("=" * 80)
print()
with open(BASE / 'pages/p09.json') as f:
    p9 = json.load(f)
for r in p9['regions']:
    if r['region_id'] == 'p09_R6':
        print(f"Region: {r['region_id']}")
        print(f"bbox: {r.get('bbox')}")
        print(f"description: {r.get('description', '')}")
        print(f"glyphs: {len(r.get('glyphs', []))}")
        for g in r.get('glyphs', []):
            print(f"  glyph idx={g.get('glyph_index'):3d}  bbox={g.get('bbox')}  vk={g.get('vision_kind')}  th={g.get('type_hint')}  cluster={g.get('cluster_id')}  size={g.get('size_px')}  fill={g.get('fill_ratio')}  nc={g.get('n_components')}")
        print(f"latin: {[(t.get('text'), t.get('source'), t.get('conf')) for t in r.get('latin_tokens', [])]}")

print()

# Suche auch p10, p11, p12 nach RING-Strukturen
print("=" * 80)
print("RING-VERDÄCHTIGE GLYPHEN PRO SEITE")
print("=" * 80)
print()
for pid in ['p09', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15', 'p16', 'p17', 'p18', 'p19', 'p20']:
    with open(BASE / 'pages' / f'{pid}.json') as f:
        p_data = json.load(f)
    rings = []
    for r in p_data['regions']:
        for g in r.get('glyphs', []):
            bbox = g.get('bbox', [0,0,0,0])
            sp = g.get('size_px', 0)
            th = g.get('type_hint', '')
            # Suche nach glyph mit großer Höhe (vertikal ausgedehnt) ODER Quadrat
            if bbox[3] > 100 and bbox[2] > 100 and th == 'unknown':
                rings.append((r['region_id'], g.get('glyph_index'), bbox, g.get('cluster_id'), sp))
    if rings:
        print(f"  {pid}: {len(rings)} unbekannte Glyphen mit bbox > 100x100")
        for r in rings[:5]:
            print(f"    {r[0]} idx={r[1]:3d} bbox={r[2]} cluster={r[3]} size={r[4]}")
