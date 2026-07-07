"""
Stufe 23b — Versteckte Purin-Basen finden (schnellere Version).
"""
import json
from pathlib import Path

doc_path = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs/doc.json')
with open(doc_path) as f:
    doc = json.load(f)
pages = doc.get('pages', [])

print("=" * 80)
print("P22_R3 — DETAILANALYSE")
print("=" * 80)
print()
for p in pages:
    if p.get('page_id') == 'p22':
        for region in p.get('regions', []):
            if region.get('region_id') == 'p22_R3':
                for f in region.get('formulas', []):
                    print(f"Formel: {f.get('raw')}")
                print()
                for g in region.get('graphics', []):
                    print(f"Graphic: type={g.get('type')}")
                    print(f"  description: {g.get('description')}")
                print()
                print("  Latin tokens:")
                for t in region.get('latin_tokens', []):
                    print(f"    '{t.get('text')}'")
                break
        break

print()
print("=" * 80)
print("P21 — ALLE FORMELN (gekürzt)")
print("=" * 80)
print()
for p in pages:
    if p.get('page_id') == 'p21':
        for region in p.get('regions', []):
            rid = region.get('region_id', '')
            for f in region.get('formulas', []):
                raw = f.get('raw', '')
                print(f"  {rid}: {raw[:100]}")
        break
print()

# === p23 Region 1-4 ===
for rid_target in ['p23_R1', 'p23_R2', 'p23_R3', 'p23_R4', 'p23_R17']:
    print()
    print("=" * 80)
    print(f"{rid_target} — DETAILS")
    print("=" * 80)
    print()
    for p in pages:
        if p.get('page_id') == 'p23':
            for region in p.get('regions', []):
                if region.get('region_id') == rid_target:
                    print(f"  region_type: {region.get('region_type')}")
                    print(f"  description: {region.get('description', '')[:200]}")
                    print()
                    print(f"  Latin tokens ({len(region.get('latin_tokens', []))}):")
                    for t in region.get('latin_tokens', [])[:20]:
                        print(f"    '{t.get('text')}'")
                    print()
                    print(f"  Formulas ({len(region.get('formulas', []))}):")
                    for f in region.get('formulas', []):
                        print(f"    {f.get('raw')[:100]}")
                    print()
                    print(f"  Graphics ({len(region.get('graphics', []))}):")
                    for g in region.get('graphics', [])[:10]:
                        print(f"    type={g.get('type')}: {g.get('description', '')[:200]}")
                    break
            break

# === Suche alle Beschreibungen mit "N" und chemischen Begriffen ===
print()
print("=" * 80)
print("ALLE ATOM-LABELS IN V4 DOC")
print("=" * 80)
print()
atom_descriptions = []
for p in pages:
    page_id = p.get('page_id', '')
    for region in p.get('regions', []):
        rid = region.get('region_id', '')
        for g in region.get('graphics', []):
            desc = g.get('description', '')
            # Suche nach "atom" oder chemischen Beschreibungen
            if 'atom' in desc.lower() or 'bind' in g.get('type', '').lower() or 'pyrimidin' in desc.lower() or 'cytosin' in desc.lower() or 'thymin' in desc.lower():
                atom_descriptions.append((page_id, rid, g.get('type'), desc[:300]))

for page_id, rid, gtype, desc in atom_descriptions:
    print(f"{page_id} {rid} ({gtype}):")
    print(f"  {desc}")
    print()

# === Atom-Labels aller Regionen ===
print()
print("=" * 80)
print("ATOM-LABELS IN ALLEN p23-REGIONEN")
print("=" * 80)
print()
for p in pages:
    if p.get('page_id') == 'p23':
        for region in p.get('regions', []):
            rid = region.get('region_id', '')
            tokens = region.get('latin_tokens', [])
            if tokens:
                print(f"  {rid} ({len(tokens)} tokens): {', '.join(t.get('text', '') for t in tokens[:25])}")
        break
