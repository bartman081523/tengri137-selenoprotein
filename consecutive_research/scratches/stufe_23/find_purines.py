"""
Stufe 23b — Versteckte Purin-Basen finden.
"""
import json
from pathlib import Path
import math

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
                    if 'labels' in g:
                        print(f"  labels: {g.get('labels')}")
                    print()
                break
        break

print("=" * 80)
print("P21 — ALLE FORMELN")
print("=" * 80)
print()
for p in pages:
    if p.get('page_id') == 'p21':
        for region in p.get('regions', []):
            rid = region.get('region_id', '')
            for f in region.get('formulas', []):
                print(f"  {rid}: {f.get('raw')}")
        break
print()

# === 1881070713468301024893312491 — was ist das? ===
n = 1881070713468301024893312491
print("=" * 80)
print("1881070713468301024893312491 — ANALYSE")
print("=" * 80)
print()
print(f"  Ziffern: {len(str(n))}")
print(f"  = {n}")
print()

def factorize(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

factors = factorize(n)
print(f"  Primfaktoren: {factors}")
print(f"  Produkt: {math.prod(factors)}")
print(f"  Anzahl Faktoren: {len(factors)}")
print()

s = sum(int(c) for c in str(n))
print(f"  Quersumme: {s}")
print(f"  n mod 9: {n % 9}")
print(f"  n mod 7: {n % 7}")
print(f"  n mod 11: {n % 11}")
print(f"  n mod 13: {n % 13}")
print(f"  n mod 137: {n % 137}")
print(f"  n mod 462: {n % 462}")
print(f"  n mod 154: {n % 154}")
print()

# === 1881070713468301024893312491 als chemische Formel? ===
# 28 Ziffern
# 28 / 7 = 4 → könnte ein Tetramer sein (4 Basen)
# 28 / 14 = 2 → könnte ein Dimer sein (2 × 14)
# Wenn wir die Ziffern als Code nehmen, könnten sie sein:
# - 1=A, 8=H, 8=H, 1=A, 0=O, 7=N, 1=A, ... (Atom-Symbole)

# Aber: 28 Ziffern = 14 Zweier-Paare
# 14 = BURUMUT-Spaltenzahl!
print("=" * 80)
print("DEUTUNG: 1881070713468301024893312491")
print("=" * 80)
print()
print("28 Ziffern = 14 Paare")
print("14 = BURUMUT-Spaltenzahl")
print()
# Versuche: A=Adenin, G=Guanin, C=Cytosin, T=Thymin
# 1, 8, 8, 1, 0, 7, 0, 7, 1, 3, 4, 6, 8, 3, 0, 1, 0, 2, 4, 8, 9, 3, 3, 1, 2, 4, 9, 1
digits = str(n)
print(f"  Ziffern: {' '.join(digits)}")
print()

# Atom-Symbole: H, He, Li, Be, B, C, N, O, F, Ne, Na, Mg, ...
# 1=H, 2=He, ... aber 88, 10, 71, ...?
# 1881 = At, oder einfach als 1-8-8-1 interpretieren
# 1=H, 8=O, 8=O, 1=H → H2O2 (Wasserstoffperoxid)? Aber das ergibt keinen Sinn.

# Mathematische Interpretation
print(f"  1881070713468301024893312491 / 462 = {n / 462}")
print(f"  1881070713468301024893312491 / 154 = {n / 154}")
print(f"  1881070713468301024893312491 / 7 = {n / 7}")
print(f"  1881070713468301024893312491 / 14 = {n / 14}")
print(f"  1881070713468301024893312491 / 28 = {n / 28}")
print(f"  1881070713468301024893312491 / 100 = {n / 100}")
print()

# === p23_R2 - Genauere Suche ===
print("=" * 80)
print("P23_R2 — ATOM-LABELS")
print("=" * 80)
print()
for p in pages:
    if p.get('page_id') == 'p23':
        for region in p.get('regions', []):
            if region.get('region_id') == 'p23_R2':
                print(f"  description: {region.get('description', '')[:300]}")
                print()
                print("  Latin tokens:")
                for t in region.get('latin_tokens', []):
                    print(f"    '{t.get('text')}'")
                print()
                for g in region.get('graphics', []):
                    print(f"  type={g.get('type')}: {g.get('description', '')[:300]}")
                break
        break

print()
print("=" * 80)
print("P23_R3 — ATOM-LABELS")
print("=" * 80)
print()
for p in pages:
    if p.get('page_id') == 'p23':
        for region in p.get('regions', []):
            if region.get('region_id') == 'p23_R3':
                print(f"  description: {region.get('description', '')[:300]}")
                print()
                print("  Latin tokens:")
                for t in region.get('latin_tokens', []):
                    print(f"    '{t.get('text')}'")
                print()
                for g in region.get('graphics', []):
                    print(f"  type={g.get('type')}: {g.get('description', '')[:300]}")
                break
        break

# === Suche nach p23_R1 (Peptidbindung) ===
print()
print("=" * 80)
print("P23_R1 — PEPTIDBINDUNG")
print("=" * 80)
print()
for p in pages:
    if p.get('page_id') == 'p23':
        for region in p.get('regions', []):
            if region.get('region_id') == 'p23_R1':
                print(f"  description: {region.get('description', '')[:300]}")
                print()
                print("  Latin tokens:")
                for t in region.get('latin_tokens', []):
                    print(f"    '{t.get('text')}'")
                print()
                for g in region.get('graphics', []):
                    print(f"  type={g.get('type')}: {g.get('description', '')[:300]}")
                break
        break

# === p23_R4 (Amidin-Formeln) ===
print()
print("=" * 80)
print("P23_R4 — AMIDIN-FORMELN")
print("=" * 80)
print()
for p in pages:
    if p.get('page_id') == 'p23':
        for region in p.get('regions', []):
            if region.get('region_id') == 'p23_R4':
                print(f"  description: {region.get('description', '')[:300]}")
                print()
                print("  Latin tokens:")
                for t in region.get('latin_tokens', []):
                    print(f"    '{t.get('text')}'")
                print()
                for g in region.get('graphics', []):
                    print(f"  type={g.get('type')}: {g.get('description', '')[:300]}")
                break
        break
