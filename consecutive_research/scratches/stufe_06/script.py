"""
Stufe 6 — BURUMUT-Matrix auf p23.

Frage: Was ist die 11x11-Matrix, und was steht um sie herum?

Methode:
  1) Extrahiere 11x11-Matrix
  2) Buchstabenhäufigkeit
  3) Vergleich mit englischer Verteilung
  4) Schmehs Manifesto-Zeilen quer-checken
  5) Vision-chemische Symbole vs lateinische Buchstaben
  6) idx 996 (SINGLETON) Detail
"""
import json
from collections import Counter
from pathlib import Path

BASE = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs')

with open(BASE / 'pages/p23.json') as f:
    p23 = json.load(f)

# 1) Matrix extrahieren
matrix_lines = []
for r in p23['regions']:
    if r.get('region_type') == 'burumut_block':
        for t in r.get('latin_tokens', []):
            if t.get('source') == 'schmeh_complete':
                matrix_lines.append(t.get('text', '').replace(' ', ''))

# 2) Buchstabenhäufigkeit
all_letters = ''.join(matrix_lines)
print("=" * 80)
print("1) 11x11-MATRIX")
print("=" * 80)
print()
for i, line in enumerate(matrix_lines, 1):
    print(f"  {i:2d}: {' '.join(line)}")
print()
print(f"Total: {len(all_letters)} Buchstaben")
print()

# Häufigkeit
counter = Counter(all_letters)
print("Häufigkeit:")
for letter, count in sorted(counter.items(), key=lambda x: (-x[1], x[0])):
    bar = chr(0x2588) * count
    print(f"  {letter}: {count:3d}  {bar}")
print()
print(f"Distinkte Buchstaben: {len(counter)}")
print(f"Alphabet: {''.join(sorted(counter.keys()))}")
print(f"FEHLENDE lateinische Buchstaben: {set('ABCDEFGHIJKLMNOPQRSTUVWXYZ') - set(counter.keys())}")
print()

# 3) Englische Vergleichsverteilung
eng_freq = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3, 'H': 6.1,
    'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2,
    'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.2, 'X': 0.2,
    'Q': 0.1, 'Z': 0.1
}
print("=" * 80)
print("2) VERGLEICH MIT ENGLISCHER VERTEILUNG (in %)")
print("=" * 80)
total = len(all_letters)
print(f"{'Letter':<6} {'BURUMUT%':>10} {'English%':>10} {'Diff':>8}")
for letter in sorted(counter.keys(), key=lambda x: -counter[x]):
    pct = 100 * counter[letter] / total
    eng = eng_freq.get(letter, 0)
    diff = pct - eng
    marker = '↑' if diff > 2 else '↓' if diff < -2 else '='
    print(f"  {letter:<5} {pct:>9.2f}% {eng:>9.1f}% {diff:>+7.1f} {marker}")
print()

# 4) Schmehs Manifesto
print("=" * 80)
print("3) SCHMEH MANIFESTO (16 manifesto lines)")
print("=" * 80)
schmeh_manifesto = []
for r in p23['regions']:
    for t in r.get('latin_tokens', []):
        if t.get('source') == 'schmeh_hint' or (t.get('source') == 'schmeh_complete' and r['region_id'] != 'p23_R20_LETTERBLOCK'):
            schmeh_manifesto.append((r['region_id'], t, t.get('source')))

for rid, t, src in schmeh_manifesto:
    text = t.get('text', '')
    print(f"  {rid:25s} ({src:15s}) {text[:90]}")
print()

# 5) Vision-chemische Symbole vs Schmeh
print("=" * 80)
print("4) VISION-CHEMISCHE SYMBOLE vs SCHMEH-LATEIN")
print("=" * 80)
print()
print("Vision liest auf p23_R3, R4, R17:")
vision_chem = []
for r in p23['regions']:
    for t in r.get('latin_tokens', []):
        if t.get('source') == 'vision':
            vision_chem.append((r['region_id'], t.get('text'), t.get('conf')))
for rid, text, conf in vision_chem:
    print(f"  {rid:20s} conf={conf}  '{text}'")
print()
print("Schmehs lateinischer Text auf p23_R1 (überlagert mit Vision-chem):")
for r in p23['regions']:
    if r['region_id'] == 'p23_R1':
        for t in r.get('latin_tokens', []):
            print(f"  src={t.get('source'):20s} conf={t.get('conf')}  text={repr(t.get('text'))[:80]}")
print()

# 6) IDX 996 SINGLETON
print("=" * 80)
print("5) IDX 996 — DER SINGLETON")
print("=" * 80)
for r in p23['regions']:
    for g in r.get('glyphs', []):
        if g.get('glyph_index') == 996:
            print(f"  Region: {r['region_id']}  rt={r.get('region_type')}")
            print(f"  bbox: {g.get('bbox')}")
            print(f"  cluster: {g.get('cluster_id')}")
            print(f"  vision_kind: {g.get('vision_kind')}")
            print(f"  type_hint: {g.get('type_hint')}")
            print(f"  size_px: {g.get('size_px')}")
            print(f"  fill_ratio: {g.get('fill_ratio')}")
            print(f"  n_components: {g.get('n_components')}")
            vd = g.get('vision_description')
            print(f"  vision_description: {(vd or '(none)')[:200]}")
            print(f"  Region latin_tokens:")
            for t in r.get('latin_tokens', []):
                print(f"    {t.get('source'):20s} conf={t.get('conf')}  text={repr(t.get('text'))[:80]}")
print()

# 7) Schmeh's Manifesto Quervergleich: Wörter mit Rechtschreibfehlern
print("=" * 80)
print("6) SCHMEH RECHTSCHREIBFEHLER (Bewusst?)")
print("=" * 80)
manifesto_full = " ".join(t.get('text', '') for rid, t, src in schmeh_manifesto)
print(f"Full Manifesto: {manifesto_full}")
print()
print("Bekannte Anomalien (Schmehs Anmerkung):")
print("  - 'KNOWLEDGS' statt 'KNOWLEDGE' (im Manifesto)")
print("  - 'OURR' statt 'OUR' (im Manifesto)")
print()

# 8) Versuche: ist die Matrix ein Verschlüsselungs-Schlüssel?
print("=" * 80)
print("7) MATRIX ALS SUBSTITUTION")
print("=" * 80)
# Schmeh: 'genetically encrypted'
# Vielleicht ist die Matrix ein alphabet-mapping?
matrix_unique = ''.join(sorted(counter.keys()))
print(f"Matrix-Unique Letters: {matrix_unique}")
print(f"Alphabet: ABCDEFGHIJKLMNOPQRSTUVWXYZ")
print(f"Diff: {set('ABCDEFGHIJKLMNOPQRSTUVWXYZ') - set(matrix_unique)}")
print()
# Auch: sind die 19 Buchstaben in einer besonderen Reihenfolge?
import itertools
# Suche: BURUMUT als Anker
# BURUMUT = B U R U M U T
# Kommt in Zeile 1, Spalte 1-7?
print("BURUMUT-Sequenz in der Matrix:")
seq = "BURUMUT"
for i, line in enumerate(matrix_lines, 1):
    if seq in line:
        pos = line.index(seq)
        print(f"  Zeile {i}, pos {pos+1}-{pos+len(seq)}: ...{line[max(0,pos-2):pos+len(seq)+2]}...")
    # Auch rückwärts
    if seq[::-1] in line:
        pos = line.index(seq[::-1])
        print(f"  Zeile {i} (rückwärts), pos {pos+1}-{pos+len(seq)}: ...{line[max(0,pos-2):pos+len(seq)+2]}...")
print()

# Auch REFAMTU
print("REFAMTU-Sequenz in der Matrix:")
seq = "REFAMTU"
for i, line in enumerate(matrix_lines, 1):
    if seq in line:
        pos = line.index(seq)
        print(f"  Zeile {i}, pos {pos+1}-{pos+len(seq)}: ...{line[max(0,pos-2):pos+len(seq)+2]}...")
