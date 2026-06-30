"""
Q19 (NEU): Systematische Wiederholungs-Analyse in BURUMUT

BURUMUT hat MEHRERE Strukturen mit ungewoehnlichen Wiederholungen.
- UAZBE × 4 (Q17, p < 10^-4)
- HIMLAZANR × 2 (Q18, p < 0.0001)
- Welche anderen?

Wir testen fuer jede k in 1..20:
1. Welche k-mere wiederholen sich in BURUMUT?
2. Wie oft verglichen mit Monte Carlo?
"""
import random
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

BURUMUT_FREQ = Counter(BURUMUT_FULL)
chars = list(BURUMUT_FREQ.keys())
weights = list(BURUMUT_FREQ.values())

n_trials = 5000

print("="*70)
print("Q19.1: K-mer-Wiederholungen in BURUMUT vs Random")
print("="*70)
print(f"{'k':>3s} {'MaxRep_BURUMUT':>15s} {'MaxRep_Random':>15s} {'p-Wert':>8s} {'Anzahl_>=2':>10s}")
for k in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 30, 50]:
    n_kmers = len(BURUMUT_FULL) - k + 1
    burumut_kmers = [BURUMUT_FULL[i:i+k] for i in range(n_kmers)]
    burumut_freq = Counter(burumut_kmers)
    burumut_max = max(burumut_freq.values())

    # Monte Carlo
    random_max_dist = []
    random_n_ge2 = 0
    for trial in range(n_trials):
        random.seed(trial)
        seq = ''.join(random.choices(chars, weights=weights, k=99))
        rand_kmers = [seq[i:i+k] for i in range(len(seq) - k + 1)]
        rand_freq = Counter(rand_kmers)
        if rand_freq:
            random_max_dist.append(max(rand_freq.values()))
        if rand_freq and max(rand_freq.values()) >= 2:
            random_n_ge2 += 1

    rand_max = max(random_max_dist)
    p_val = sum(1 for c in random_max_dist if c >= burumut_max) / n_trials
    n_ge2_burumut = sum(1 for n in burumut_freq.values() if n >= 2)
    n_ge2_random = sum(1 for c in random_max_dist if c >= 2) / n_trials
    print(f"  {k:2d}    {burumut_max:10d}     {rand_max:10d}     {p_val:.4f}    {n_ge2_burumut:5d}")

# 2. Welche k-mere wiederholen sich >= 2x in BURUMUT?
print()
print("="*70)
print("Q19.2: BURUMUT-Wiederholungen pro k")
print("="*70)
for k in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20]:
    burumut_kmers = [BURUMUT_FULL[i:i+k] for i in range(len(BURUMUT_FULL) - k + 1)]
    burumut_freq = Counter(burumut_kmers)
    repeats = {km: n for km, n in burumut_freq.items() if n >= 2}
    if repeats:
        print(f"  k={k}: {len(repeats)} k-mere mit >= 2 Wiederholungen")
        for km, n in sorted(repeats.items(), key=lambda x: -x[1])[:5]:
            print(f"    {km}: {n}x")

# 3. Berechne die "Linguistic Density" - ein Mass fuer Komplexitaet
print()
print("="*70)
print("Q19.3: Linguistic Density (Repetitions-Dichte)")
print("="*70)
total_kmers = 0
total_repeats = 0
for k in [3, 4, 5, 6, 7, 8, 9, 10]:
    burumut_kmers = [BURUMUT_FULL[i:i+k] for i in range(len(BURUMUT_FULL) - k + 1)]
    burumut_freq = Counter(burumut_kmers)
    n_kmers = len(burumut_kmers)
    n_repeats = sum(n for n in burumut_freq.values() if n >= 2)
    total_kmers += n_kmers
    total_repeats += n_repeats
print(f"  Gesamt: {total_repeats} Wiederholungen in {total_kmers} k-mer-Slots")
print(f"  Density: {total_repeats/total_kmers*100:.2f}%")

# 4. Vergleich: Natural Language vs Protein vs Random
# English Text hat ~30% Wiederholungen in 3-mers
# Protein hat ~5-15% Wiederholungen
# Random hat ~0% (bei gleicher Alphabet-Groesse)
