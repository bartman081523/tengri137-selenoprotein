"""
Q18 (NEU): Was ist HIMLAZANR?

HIMLAZANR kommt 2x in BURUMUT vor (Pos 37-45 und 71-79).
Identische Sequenz! 9 Zeichen lang = 3^2.

Hypothese: HIMLAZANR ist ein 9-mer Protein-Motiv.
Sequenz in 1-Letter Code: H-I-M-L-A-Z-A-N-R
In 3-Letter Code: His-Ile-Met-Leu-Ala-Glx-Asn-Arg

Was wenn die Buchstaben HIMLAZANR nicht zufällig sind,
sondern ein codiertes Wort?

HIMLAZANR = ?
- H, M, L, A, N, R sind echte Aminosäuren
- I, Z sind spezielle Codes (Ile, Glx)
- Wir versuchen: Könnte HIMLAZANR ein Akronym sein?
"""
BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# Finde alle Sub-Sequenzen
print("="*70)
print("Q18.1: HIMLAZANR-Vorkommen in BURUMUT")
print("="*70)
positions = []
for i in range(len(BURUMUT_FULL) - 8):
    if BURUMUT_FULL[i:i+9] == 'HIMLAZANR':
        positions.append(i)
print(f"HIMLAZANR-Positionen: {positions}")
print(f"Beide Vorkommen identisch: {BURUMUT_FULL[positions[0]:positions[0]+9] == BURUMUT_FULL[positions[1]:positions[1]+9]}")

# 2. Zaehle alle 9-mere in BURUMUT
from collections import Counter
nine_mers = [BURUMUT_FULL[i:i+9] for i in range(len(BURUMUT_FULL) - 8)]
nine_freq = Counter(nine_mers)
print(f"\nAlle unique 9-mere: {len(nine_freq)}")
print(f"9-mere mit Haeufigkeit >= 2:")
for nm, n in nine_freq.items():
    if n >= 2:
        print(f"  {nm}: {n}x")

# 3. Monte Carlo: Wie oft kommt ein 9-mer >= 2x in zufaelligen Sequenzen vor?
import random
from collections import Counter
BURUMUT_FREQ = Counter(BURUMUT_FULL)
chars = list(BURUMUT_FREQ.keys())
weights = list(BURUMUT_FREQ.values())

n_trials = 10000
max_count = []
for trial in range(n_trials):
    random.seed(trial)
    seq = ''.join(random.choices(chars, weights=weights, k=99))
    nmers = [seq[i:i+9] for i in range(len(seq) - 8)]
    freq = Counter(nmers)
    if freq:
        max_count.append(max(freq.values()))

print(f"\nMonte Carlo (n={n_trials}):")
print(f"  Max 9-mer Haeufigkeit: Mittelwert = {sum(max_count)/n_trials:.2f}, max = {max(max_count)}")
print(f"  Anzahl mit >= 2: {sum(1 for c in max_count if c >= 2)}")
print(f"  BURUMUT hat 1 9-mer mit 2 Vorkommen (HIMLAZANR)")
p_ge2 = sum(1 for c in max_count if c >= 2) / n_trials
print(f"  p-Wert: {p_ge2:.4f}")

# 4. NOMBA-Motiv
print()
print("="*70)
print("Q18.2: NOMBA und verwandte 5-mere")
print("="*70)
nombas = [BURUMUT_FULL[i:i+5] for i in range(len(BURUMUT_FULL) - 4)]
n_freq = Counter(nombas)
print("NOMBA + Varianten:")
for nm, n in n_freq.items():
    if 'NOMBA' in nm or 'NOMB' in nm or 'MBA' in nm:
        print(f"  {nm}: {n}x")
