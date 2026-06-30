"""
OFFENE FRAGE 5: Wer hat BURUMUT designed?

Tengri behauptet:
- 'WE HAVE EMBEDDED THESE SKILLS IN OURR GENES'
- 'WHO HAS THE CORRECT GENETIC CODING WILL UNDERSTAND THIS TEXT'
- 'GENETICALLY ENCRYPTED'

Wenn BURUMUT 'genetisch codiert' ist, dann:
1. Sind die statistischen Eigenschaften konsistent mit
   algorithmischer Generierung?
2. Gibt es Hinweise auf biologische Quellen (DNA, Protein)?
3. Ist die Markov-Entropie (1.62) konsistent mit einem Design?

Methoden:
1. Runs-Test (ob die Sequenz zufällig erscheint)
2. Auto-Korrelation (zyklische Muster)
3. Vergleich mit echten DNA-Sequenzen
4. Vergleich mit random.org-Generator
"""
import math
from collections import Counter
import random

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# 1. Runs-Test: Wie oft wechselt der Buchstabe?
def runs_test(seq):
    """Zaehlt Buchstaben-Wechsel in einer Sequenz."""
    if len(seq) < 2: return 0
    runs = 1
    for i in range(1, len(seq)):
        if seq[i] != seq[i-1]:
            runs += 1
    return runs

# Erwartete Anzahl Runs bei Zufall
# E(R) = 1 + 2*n*(n-1) / (2n-1) ≈ 2n/3 für große n
# Fuer n=99 Zeichen: E ≈ 65-66 Runs

n = len(BURUMUT_FULL)
observed_runs = runs_test(BURUMUT_FULL)
expected_runs = 1 + 2 * n * (n-1) / (2*n - 1)
z_score = (observed_runs - expected_runs) / math.sqrt((2*n * (2*n - 3)) / ((2*n - 1)**2))

print("="*70)
print("Q5.1: RUNS-TEST")
print("="*70)
print(f"BURUMUT-Laenge: {n}")
print(f"Beobachtete Runs: {observed_runs}")
print(f"Erwartete Runs (Zufall): {expected_runs:.2f}")
print(f"Z-Score: {z_score:.2f}")
print(f"-> Falls |Z| > 2: signifikant nicht-zufaellig")

# 2. Vergleich mit echtem Random
print()
print("="*70)
print("Q5.2: VERGLEICH MIT PSEUDO-RANDOM (random.seed)")
print("="*70)
random_runs_list = []
for seed in range(100):
    random.seed(seed)
    rand_seq = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=99))
    random_runs_list.append(runs_test(rand_seq))
print(f"100 random Strings (Laenge 99):")
print(f"  Mittelwert Runs: {sum(random_runs_list)/100:.2f}")
print(f"  Min Runs: {min(random_runs_list)}")
print(f"  Max Runs: {max(random_runs_list)}")
print(f"  BURUMUT Runs: {observed_runs}")

# 3. Autokorrelation: Wiederholungen?
print()
print("="*70)
print("Q5.3: AUTOKORRELATION (Periodizitaets-Test)")
print("="*70)
def autocorrelation(seq, lag):
    """Berechne Pearson-Korrelation zwischen seq und seq[lag:]."""
    if lag >= len(seq): return 0
    a = [ord(c) - ord('A') for c in seq[:-lag]]
    b = [ord(c) - ord('A') for c in seq[lag:]]
    n = len(a)
    mean_a = sum(a) / n
    mean_b = sum(b) / n
    num = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(n))
    den_a = math.sqrt(sum((a[i] - mean_a)**2 for i in range(n)))
    den_b = math.sqrt(sum((b[i] - mean_b)**2 for i in range(n)))
    if den_a == 0 or den_b == 0: return 0
    return num / (den_a * den_b)

# Teste verschiedene lags
print(f"{'lag':>5s} {'BURUMUT':>10s} {'Random (avg)':>15s}")
for lag in [1, 2, 3, 5, 7, 9, 11, 14, 20, 23, 32, 46]:
    b = autocorrelation(BURUMUT_FULL, lag)
    # Vergleich mit 100 random strings
    random.seed(42)
    rand_corrs = []
    for _ in range(100):
        rs = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=99))
        rand_corrs.append(autocorrelation(rs, lag))
    avg_random = sum(rand_corrs) / 100
    marker = " <--!" if abs(b) > 0.2 else ""
    print(f"  {lag:5d} {b:10.4f} {avg_random:15.4f}{marker}")

# 4. Vergleich mit echten DNA-Sequenzen
print()
print("="*70)
print("Q5.4: VERGLEICH MIT DNA (4 Zeichen: A, C, G, T)")
print("="*70)
# Vereinfacht: Mappen wir BURUMUTs 19 Zeichen auf 4
def map_to_dna(seq):
    """Mappe 19 Buchstaben auf A/C/G/T basierend auf Haeufigkeit."""
    freq = Counter(seq)
    sorted_chars = sorted(freq.keys(), key=lambda c: -freq[c])
    bases = 'ACGT'
    mapping = {}
    for i, ch in enumerate(sorted_chars[:4]):
        mapping[ch] = bases[i]
    for ch in sorted_chars[4:]:
        # Verteile restliche Buchstaben pseudo-zufaellig auf die 4 Basen
        mapping[ch] = bases[ord(ch) % 4]
    return ''.join(mapping[c] for c in seq)

dna_seq = map_to_dna(BURUMUT_FULL)
print(f"BURUMUT als DNA (4-Basen-Mapping): {dna_seq}")

# Wie oft kommen die haeufigsten 3-mers vor?
trimer_freq = Counter(dna_seq[i:i+3] for i in range(len(dna_seq) - 2))
print(f"\nTop 10 Trinukleotide:")
for t, n in trimer_freq.most_common(10):
    print(f"  {t}: {n}x")

# Stop-Codons?
stop_codons = {'TAA', 'TAG', 'TGA'}
stops = sum(trimer_freq[sc] for sc in stop_codons)
print(f"\nStop-Codons (TAA, TAG, TGA): {stops}")
print(f"  vs Erwartung bei Zufall: 3/64 * 97 = ~4.5")
print(f"  Mehr als 2x Erwartung koennte biologische Quelle suggerieren")

# 5. Vergleich mit echtem menschlichen Codon-Bias
print()
print("="*70)
print("Q5.5: BIAS-VERGLEICH (BURUMUT vs moegliche Quellen)")
print("="*70)
# Wenn BURUMUT ein 'genetisch codierter' Text ist, sollte er
# die gleiche Buchstaben-Verteilung haben wie Protein-Sequenzen
# oder DNA-Codons.
# In menschlicher DNA: GC-Gehalt ~ 40-45%
# In Protein: mehr Leucin, Alanin, Glycin, Valin

# Hier nur: ist die Verteilung plausibel?
freq = Counter(BURUMUT_FULL)
total = sum(freq.values())
# Normalisierte Haeufigkeiten
norm_freq = {ch: f/total for ch, f in freq.items()}
# Vergleich: Wenn BURUMUT ein Protein ist, sollten
# hydrophobe Reste (A, V, I, L, M, F) ueberwiegen.
hydrophob = ['A', 'V', 'I', 'L', 'M', 'F']  # in BURUMUT-Alphabet
hydrophil = ['R', 'K', 'D', 'E', 'N', 'Q']  # nicht in BURUMUT
print("Amino-Charakter-Verteilung (approximiert):")
hydro_count = sum(norm_freq[ch] for ch in hydrophob if ch in norm_freq)
print(f"  Hydrophob (A, V, I, L, M, F): {hydro_count*100:.1f}%")
print(f"  In echten Proteinen: ~30-35%")
print(f"  BURUMUT: 16+0+2+3+8+2 = 31 von 99 = 31.3%  -- PLAUSIBEL!")
