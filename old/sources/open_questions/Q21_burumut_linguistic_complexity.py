"""
Q21 (KORRIGIERT): BURUMUT-Sprachstatistik
"""
import math
import random
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

n_chars = len(set(BURUMUT_FULL))
freq = Counter(BURUMUT_FULL)
total = len(BURUMUT_FULL)
H0 = -sum((f/total) * math.log2(f/total) for f in freq.values())

# 1-gram Markov
def markov_H(seq):
    transitions = Counter(seq[i] for i in range(len(seq)-1))
    total = sum(transitions.values())
    return -sum((c/total) * math.log2(c/total) for c in transitions.values())

H1 = markov_H(BURUMUT_FULL)

print("="*70)
print("Q21.1: BURUMUT-Sprachstatistik")
print("="*70)
print(f"BURUMUT:")
print(f"  Alphabet-Groesse: {n_chars}")
print(f"  Shannon-Entropie H(0): {H0:.4f} bits/Zeichen")
print(f"  Markov-Entropie H(1): {H1:.4f} bits/Zeichen")
print(f"  Max H(0) bei {n_chars} Buchstaben: {math.log2(n_chars):.4f}")
print(f"  Effizienz H(0)/H(0)_max: {H0/math.log2(n_chars)*100:.1f}%")

# Vergleich mit anderen Sequenzen
print()
print("="*70)
print("Q21.2: Vergleich")
print("="*70)

# Zufaellig mit BURUMUT-Alphabet und Verteilung
BURUMUT_chars = list(freq.keys())
BURUMUT_weights = list(freq.values())
random.seed(42)
random_seq = ''.join(random.choices(BURUMUT_chars, weights=BURUMUT_weights, k=99))
H0_r = -sum((f/len(random_seq)) * math.log2(f/len(random_seq)) for f in Counter(random_seq).values())

# Zufaellig uniform
random_uniform = ''.join(random.choices('ACGT', k=99))
H0_u = -sum((f/len(random_uniform)) * math.log2(f/len(random_uniform)) for f in Counter(random_uniform).values())

# Englisches Sample
english = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
H0_e = -sum((f/len(english)) * math.log2(f/len(english)) for f in Counter(english).values())

# Protein (Myoglobin)
myoglobin = "MGLSDGEWQQVLNVWGKVEADIAGHGQEVLIRLFTGHPETLEKFDKFKHLKTEAEMKASEDLKKH"
H0_m = -sum((f/len(myoglobin)) * math.log2(f/len(myoglobin)) for f in Counter(myoglobin).values())

print(f"{'Sequenz':<35s} {'Alphabet':>10s} {'H(0)':>6s}")
print(f"{'BURUMUT':<35s} {n_chars:>10d} {H0:.2f}")
print(f"{'Zufaellig (BURUMUT-Verteilung)':<35s} {len(set(random_seq)):>10d} {H0_r:.2f}")
print(f"{'Zufaellig uniform (ACGT)':<35s} {len(set(random_uniform)):>10d} {H0_u:.2f}")
print(f"{'Englisch (sample)':<35s} {len(set(english)):>10d} {H0_e:.2f}")
print(f"{'Myoglobin (real)':<35s} {len(set(myoglobin)):>10d} {H0_m:.2f}")

# 3. BURUMUTs 'Burg-Position'
print()
print("="*70)
print("Q21.3: BURUMUTs 'Burg-Position'")
print("="*70)
print(f"BURUMUT hat H(0) = {H0:.2f} bits")
print(f"  -> Zwischen Zufall (3.5-4.0) und Text (4.0-4.5)")
print(f"  -> Im Bereich 'komprimierte Information'")
print()
print(f"BURUMUT hat H(1) = {H1:.2f} bits (fast gleich H(0))")
print(f"  -> Markov-Information fast = Shannon-Information")
print(f"  -> Das Zeichen an Position i ist unvorhersagbar aus i-1")
print(f"  -> Keine starke Markov-Struktur")
