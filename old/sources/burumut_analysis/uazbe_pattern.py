"""
PHASE 1.6: UAZBE - DAS GOLDENE MUSTER

UAZBE erscheint 4 mal in BURUMUT an den Positionen 32, 46, 66, 80.
Das ist kein Zufall - das ist eine REPETITIVE STRUKTUR.

Fragen:
1. Welche Sequenz umgibt UAZBE jeweils?
2. Welche Differenzen gibt es zwischen den UAZBE-Vorkommen?
3. Welche Trigramm-Positionen wiederholen sich?
"""
import math
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPSUAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

print("="*70)
print("PHASE 1.6.1: UAZBE-POSITIONEN IM DETAIL")
print("="*70)

# Suche nach allen Vorkommen mit Kontext
positions = []
start = 0
while True:
    idx = BURUMUT_FULL.find("UAZBE", start)
    if idx == -1: break
    positions.append(idx)
    start = idx + 1

print(f"UAZBE-Positionen: {positions}")
print(f"Differenzen: {[positions[i+1] - positions[i] for i in range(len(positions)-1)]}")
print(f"  32 → 46: Differenz 14")
print(f"  46 → 66: Differenz 20")
print(f"  66 → 80: Differenz 14")
print()

# Zeige vollen Kontext um jede UAZBE
print("Voller Kontext (15 Zeichen vor und nach UAZBE):")
for p in positions:
    before = BURUMUT_FULL[max(0, p-15):p]
    after = BURUMUT_FULL[p:p+20]
    print(f"  Position {p}:")
    print(f"    VORHER: {before}")
    print(f"    UAZBE: {BURUMUT_FULL[p:p+5]}")
    print(f"    NACHHER: {after}")
    print()
print()

print("="*70)
print("PHASE 1.6.2: DIE 5 BUCHSTABEN VOR UAZBE")
print("="*70)
# Was steht jeweils VOR UAZBE?
for p in positions:
    before5 = BURUMUT_FULL[p-5:p] if p >= 5 else ""
    print(f"  Position {p}: '{before5}' + UAZBE")
print()

# Nach UAZBE schauen
print("Was steht jeweils NACH UAZBE?")
for p in positions:
    after20 = BURUMUT_FULL[p+5:p+25]
    print(f"  Position {p}: UAZBE + '{after20}'")
print()

print("="*70)
print("PHASE 1.6.3: DAS MAGISCHE MUSTER - 4 UAZBE-BLOECKE")
print("="*70)
# Trenne BURUMUT in 4 Bloecke (vor jedem UAZBE):
# Block 0: BURUMUTREFAMTUNURESUTREGUMFAYAPS  (32 Zeichen)
# Block 1: HIER1LAZANR  (10 Zeichen)
# Block 2: HIER2NOMBAMZHQRSAN  (15 Zeichen)
# Block 3: HIER3HIMLAZANR  (12 Zeichen)
# Block 4: HIER4ENOMBARAZHQRSAN  (17 Zeichen)

block0 = BURUMUT_FULL[:32]
block1 = BURUMUT_FULL[32+5:46]
block2 = BURUMUT_FULL[46+5:66]
block3 = BURUMUT_FULL[66+5:80]
block4 = BURUMUT_FULL[80+5:]

print(f"Block 0 (vor 1. UAZBE): '{block0}' ({len(block0)} Zeichen)")
print(f"Block 1 (zwischen 1. und 2. UAZBE, ohne UAZBE): '{block1}' ({len(block1)} Zeichen)")
print(f"Block 2 (zwischen 2. und 3. UAZBE, ohne UAZBE): '{block2}' ({len(block2)} Zeichen)")
print(f"Block 3 (zwischen 3. und 4. UAZBE, ohne UAZBE): '{block3}' ({len(block3)} Zeichen)")
print(f"Block 4 (nach 4. UAZBE): '{block4}' ({len(block4)} Zeichen)")
print()

# Block 1 vs Block 3 sind beide 'HIMLAZANR' (10+12 Zeichen, leicht versetzt)
print("Block 1 vs Block 3:")
print(f"  B1: {block1}")
print(f"  B3: {block3}")
if block1 in block3 or block3 in block1:
    print("  → SIND IDENTISCH ODER TEILMENGE!")
print()

# Was steht jeweils nach UAZBE: H I M L A Z A N R U (B1) bzw. N O M B A M Z (B2)
print("Die Sequenz unmittelbar nach UAZBE:")
for p in positions:
    after5 = BURUMUT_FULL[p+5:p+10]
    print(f"  Position {p}: UAZBE + {after5}")
print()

print("="*70)
print("PHASE 1.6.4: UAZBE ALS REKURSIONS-ANKER")
print("="*70)
# Was wenn UAZBE der 'Reset-Code' ist?
# Wir testen: Wie oft kommt jeder Buchstabe VOR UAZBE und NACH UAZBE vor?

count_before = Counter()
count_after = Counter()
for p in positions:
    before = BURUMUT_FULL[:p]
    after = BURUMUT_FULL[p+5:]
    count_before.update(before)
    count_after.update(after)

# Welche Buchstaben sind VOR UAZBE haeufiger, welche NACH?
all_chars = set(BURUMUT_FULL)
print(f"{'Char':4s} {'Vor':>5s} {'Nach':>5s} {'Ratio':>8s}")
for ch in sorted(all_chars):
    b = count_before.get(ch, 0)
    a = count_after.get(ch, 0)
    total = b + a
    if total > 0:
        ratio = b / total if a > 0 else float('inf')
        print(f"  {ch:4s} {b:5d} {a:5d} {ratio:8.3f}")
print()

print("="*70)
print("PHASE 1.6.5: UAZBE ALS ANKER FUER FIBONACCI-MUSTER")
print("="*70)
# Positionen der UAZBE-Vorkommen: 32, 46, 66, 80
# Differenzen: 14, 20, 14
# Wir testen, ob die Positionen Fibonacci-bezogen sind
fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
print(f"UAZBE-Positionen: {positions}")
print(f"Fibonacci-Zahlen bis 100: {fibs}")
print(f"Differenzen 14, 20, 14: 14 = 13+1 (Fib+1), 20 = 21-1 (Fib-1), 14 = 13+1")
print()
# Berechne auch die BURUMUT-Subsequenz zwischen den UAZBE
seg1 = BURUMUT_FULL[37:46]  # HIER1LAZANR - aber wir wollen das richtige Stueck
# eigentlich Block 1 = BURUMUT_FULL[37:46]
print(f"Subsequenz zwischen 1. und 2. UAZBE (pos 37-45): '{BURUMUT_FULL[37:46]}'")
print(f"Subsequenz zwischen 2. und 3. UAZBE (pos 51-65): '{BURUMUT_FULL[51:66]}'")
print(f"Subsequenz zwischen 3. und 4. UAZBE (pos 71-79): '{BURUMUT_FULL[71:80]}'")
print()

print("="*70)
print("PHASE 1.6.6: DAS 'AZBE'-TRIGRAMM ALS 72-FAKTOR-INDICATOR?")
print("="*70)
phi_local = (1 + math.sqrt(5)) / 2
# AZBE kommt 4x vor (Trigramm-Position 33, 47, 67, 81)
# 33, 47, 67, 81 - Differenzen 14, 20, 14
# Wir interpretieren als: 33, 33+14, 33+14+20, 33+14+20+14 = 33, 47, 67, 81
# Oder: 33*2 = 66 (~67), 33*2.5 = 82.5 (~81)
# Ist 33 ein Spezieller Wert?
print(f"33 / phi = {33/phi_local:.4f}")
print(f"33 + phi = {33+phi_local:.4f}")
print(f"33 * phi = {33*phi_local:.4f}")
print(f"33 / 7 = {33/7:.4f}")
print(f"33 / 11 = {33/11:.4f}")
print(f"33 / 13 = {33/13:.4f}")
print()

print("="*70)
print("PHASE 1.6.7: BURUMUT ALS MARKOV-KETTE")
print("="*70)
# Was wenn BURUMUT einer Markov-Kette folgt?
# Wir bauen die Uebergangsmatrix auf und schauen, ob sie etwas Spezielles hat.

from collections import defaultdict

transitions = defaultdict(Counter)
for i in range(len(BURUMUT_FULL) - 1):
    transitions[BURUMUT_FULL[i]][BURUMUT_FULL[i+1]] += 1

print("Top Transitionen (welcher Buchstabe folgt welchem am haeufigsten):")
all_trans = []
for src, dests in transitions.items():
    for dst, n in dests.items():
        all_trans.append((n, src, dst))
all_trans.sort(reverse=True)
for n, src, dst in all_trans[:15]:
    print(f"  {src} → {dst}: {n}x")
print()

# Berechne die Entropie der Kette
total_trans = sum(n for n, _, _ in all_trans)
entropy = 0
for n, _, _ in all_trans:
    p = n / total_trans
    entropy -= p * math.log2(p)
print(f"Markov-Entropie der BURUMUT-Kette: {entropy:.4f} bits/Zeichen")
print(f"Vergleich: Bei zufaelligem Alphabet (19 Zeichen) waere max Entropie = {math.log2(19):.4f} bits")
print()

print("="*70)
print("PHASE 1.6.8: BUCHSTABEN-POSITIONEN UND DER GOLDENE SCHNITT")
print("="*70)
# Wir pruefen: Gibt es Buchstaben, deren POSITION im BURUMUT nahe an phi*n ist?
phi = (1 + math.sqrt(5)) / 2
print("Position der 'U'-Vorkommen (haeufigster Vokal) und Abstand zu phi*n:")
u_positions = [i for i, c in enumerate(BURUMUT_FULL) if c == 'U']
print(f"U-Positionen: {u_positions}")
for up in u_positions[:15]:
    n = round(up / phi)
    diff = abs(up - n * phi)
    print(f"  pos {up}: n={n}, phi*{n}={n*phi:.2f}, diff={diff:.3f}")
print()

print("="*70)
print("PHASE 1.6 ENDE")
print("="*70)