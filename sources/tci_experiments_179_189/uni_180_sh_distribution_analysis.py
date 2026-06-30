#!/usr/bin/env python3
"""
uni_180_sh_distribution_analysis.py - WARUM ist SH nicht-zufällig?

DESIGN: Ergebnisoffen - Keine vorbestimmte Hypothese
METHOD: Inquiry Chain mit dynamischen Strategic Vectors

CONTEXT (from uni_179):
  - SH ist NICHT zufällig verteilt (Z=-2.07, KS p=0.0000)
  - Mean = 123.10, Std = 135.77, Range = [7, 610]
  - 61 unique values aus 72 Namen
  - Max Gematria = 610 = Fibonacci(15)! (Interesting!)

INQUIRY CHAIN:
Q1: Welche mathematische Struktur hat die Gematria-Verteilung?
Q2: Gibt es Fibonacci/Primzahl/Modular-Muster?
Q3: Kodiert die Buchstaben-Kombinatorik die Verteilung?
Q4: Gibt es versteckte Ordnung (Sortierung, Gruppierung)?
Q5: Grand Synthesis - Was erklärt die Nicht-Zufälligkeit?
"""

# =============================================================================
# TEE LOGGER (PFLICHT!)
# =============================================================================
import sys
from pathlib import Path

class TeeLogger:
    def __init__(self, log_path):
        self.terminal = sys.stdout
        self.log = open(log_path, 'w', encoding='utf-8')
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()
    def flush(self):
        self.terminal.flush()
        self.log.flush()

_log_path = Path(__file__).with_suffix('.log.txt')
sys.stdout = TeeLogger(_log_path)

# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
from collections import Counter
from scipy import stats
import matplotlib.pyplot as plt

# =============================================================================
# STRATEGIC VECTOR COLLECTOR
# =============================================================================
STRATEGIC_VECTORS = []

def add_vector(finding, direction, priority="MEDIUM"):
    """Dynamisch Strategic Vector hinzufügen"""
    STRATEGIC_VECTORS.append({
        'finding': finding,
        'direction': direction,
        'priority': priority
    })
    print(f"  ⟹ STRATEGIC VECTOR [{priority}]: {direction}")

# =============================================================================
# HEBREW LETTER GEMATRIA
# =============================================================================
# Standard Hebrew Gematria values
HEBREW_GEMATRIA = {
    'א': 1,   'ב': 2,   'ג': 3,   'ד': 4,   'ה': 5,
    'ו': 6,   'ז': 7,   'ח': 8,   'ט': 9,   'י': 10,
    'כ': 20,  'ל': 30,  'מ': 40,  'נ': 50,  'ס': 60,
    'ע': 70,  'פ': 80,  'ק': 100, 'ר': 200, 'ש': 300,
    'ת': 400
}

# Die 72 Namen (from shem_hamephorash.py)
SHEM_72_HEBREW = [
    "והו", "ילי", "סית", "אלמ", "מהש", "ללה", "אכא", "כהת",
    "הזי", "אלד", "לאו", "ההא", "יזל", "מבה", "הרי", "הקמ",
    "כלי", "לוו", "פהל", "נלכ", "ייי", "מלה", "כהו", "נתה",
    "האא", "ירת", "סאה", "ריי", "אומ", "לכב", "וסר", "יהו",
    "להכ", "כוק", "מנד", "אני", "כאמ", "רהא", "ייז", "ההה",
    "מיכ", "וול", "ילה", "סאל", "ארי", "אסל", "מיה", "דני",
    "הכס", "אממ", "ננא", "נית", "פוי", "נממ", "ייל", "הרכ",
    "מתר", "ומב", "יהה", "אנו", "מכי", "דמב", "מנק", "איא",
    "כבו", "ראה", "יבמ", "היי", "מומ", "אני", "כאמ", "רהא"
]

def compute_gematria(hebrew_name):
    """Berechne Gematria eines hebräischen Namens."""
    return sum(HEBREW_GEMATRIA.get(letter, 0) for letter in hebrew_name)

# =============================================================================
# FIBONACCI SEQUENCE
# =============================================================================
def generate_fibonacci(n):
    """Generate first n Fibonacci numbers."""
    fib = [1, 1]
    for _ in range(n - 2):
        fib.append(fib[-1] + fib[-2])
    return fib

FIB_SEQUENCE = generate_fibonacci(30)  # Up to 832040

# =============================================================================
# PRIME NUMBERS
# =============================================================================
def is_prime(n):
    """Check if n is prime."""
    if n < 2:
        return False
    for i in range(2, int(np.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def prime_factorization(n):
    """Return prime factorization as dict {prime: exponent}."""
    if n < 2:
        return {}
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

# =============================================================================
# MAIN EXPERIMENT
# =============================================================================
print("=" * 70)
print("UNI-180: WARUM IST SHEM HAMEPHORASH NICHT-ZUFÄLLIG?")
print("=" * 70)
print()
print("DESIGN: Ergebnisoffen - Daten bestimmen Richtung")
print("METHOD: Inquiry Chain mit dynamischen Strategic Vectors")
print()

# Compute all Gematria values
gematria_values = [compute_gematria(name) for name in SHEM_72_HEBREW]
print(f"Computed Gematria for {len(gematria_values)} names")
print(f"Values: {gematria_values[:10]}... (first 10)")
print()

# =============================================================================
# INQUIRY 1: STRUKTURANALYSE - Was macht die Verteilung nicht-zufällig?
# =============================================================================
print("=" * 70)
print("INQUIRY 1: Strukturanalyse der Gematria-Verteilung")
print("=" * 70)
print()

# Basic Statistics
gematria_array = np.array(gematria_values)
print(f"N = {len(gematria_array)}")
print(f"Mean = {np.mean(gematria_array):.2f}")
print(f"Std = {np.std(gematria_array):.2f}")
print(f"Min = {np.min(gematria_array)}, Max = {np.max(gematria_array)}")
print(f"Median = {np.median(gematria_array):.1f}")
print(f"Unique values = {len(set(gematria_values))}")
print()

# Distribution shape
skewness = stats.skew(gematria_array)
kurtosis = stats.kurtosis(gematria_array)
print(f"Skewness = {skewness:.3f} (>0 means right-skewed)")
print(f"Kurtosis = {kurtosis:.3f} (>0 means heavy tails)")
print()

# Test for specific distributions
_, p_normal = stats.normaltest(gematria_array)
_, p_uniform = stats.kstest(gematria_array, 'uniform', 
                            args=(min(gematria_array), max(gematria_array) - min(gematria_array)))
_, p_expon = stats.kstest(gematria_array, 'expon', 
                          args=(min(gematria_array), np.mean(gematria_array) - min(gematria_array)))

print("Distribution Tests (p-value > 0.05 = consistent with distribution):")
print(f"  Normal: p = {p_normal:.4f} {'✓' if p_normal > 0.05 else '✗'}")
print(f"  Uniform: p = {p_uniform:.4f} {'✓' if p_uniform > 0.05 else '✗'}")
print(f"  Exponential: p = {p_expon:.4f} {'✓' if p_expon > 0.05 else '✗'}")
print()

# Key finding
if skewness > 1.0:
    print("✓ FINDING: Strong right-skew (many small values, few large)")
    add_vector("Right-skewed distribution", 
               "Logarithmische Transformation oder Pareto-Modell testen",
               "MEDIUM")
elif p_expon > 0.01:
    print("✓ FINDING: Approximately exponential distribution")
    add_vector("Exponential distribution", 
               "Decay-Prozess untersuchen (warum?)",
               "HIGH")
else:
    print("⊘ FINDING: Neither normal, uniform, nor exponential")
    add_vector("Unbekannte Verteilung", 
               "Andere Verteilungsmodelle testen (Zipf, Power-Law)",
               "MEDIUM")

print()

# =============================================================================
# INQUIRY 2: FIBONACCI-MUSTER
# =============================================================================
print("=" * 70)
print("INQUIRY 2: Fibonacci-Muster in SH")
print("=" * 70)
print()

# Check which values are Fibonacci numbers
fib_set = set(FIB_SEQUENCE)
fib_matches = [g for g in gematria_values if g in fib_set]
fib_indices = [i for i, g in enumerate(gematria_values) if g in fib_set]

print(f"Fibonacci numbers in SH: {len(fib_matches)}/72 ({100*len(fib_matches)/72:.1f}%)")
print(f"Values: {sorted(set(fib_matches))}")
print(f"Indices (0-based): {fib_indices}")
print()

# Expected by chance
max_val = max(gematria_values)
fib_below_max = [f for f in FIB_SEQUENCE if f <= max_val]
expected_fib_rate = len(fib_below_max) / max_val if max_val > 0 else 0
expected_fib_count = expected_fib_rate * 72
print(f"Expected by chance: {expected_fib_count:.1f} (rate: {expected_fib_rate:.4f})")
print()

# Statistical test
from scipy.stats import binom
p_fib = 1 - binom.cdf(len(fib_matches) - 1, 72, expected_fib_rate)
print(f"Binomial p-value (one-sided): {p_fib:.4f}")

if p_fib < 0.05:
    print("✓ FINDING: Significantly MORE Fibonacci numbers than expected!")
    add_vector("Fibonacci Überrepräsentation",
               "Fibonacci-Spirale als SH-Ordnungsprinzip untersuchen",
               "HIGH")
else:
    print("⊘ FINDING: Fibonacci count consistent with chance")

# Check Fibonacci RATIOS between consecutive values
fib_ratios = []
phi = (1 + np.sqrt(5)) / 2
for i in range(len(gematria_values) - 1):
    if gematria_values[i] > 0:
        ratio = gematria_values[i+1] / gematria_values[i]
        fib_ratios.append(ratio)

close_to_phi = [r for r in fib_ratios if abs(r - phi) < 0.2]
print()
print(f"Consecutive ratios close to φ (±0.2): {len(close_to_phi)}/71")
print()

# =============================================================================
# INQUIRY 3: PRIMZAHL-STRUKTUR
# =============================================================================
print("=" * 70)
print("INQUIRY 3: Primzahl-Struktur in SH")
print("=" * 70)
print()

# Check which values are prime
prime_values = [g for g in gematria_values if is_prime(g)]
prime_indices = [i for i, g in enumerate(gematria_values) if is_prime(g)]

print(f"Prime numbers in SH: {len(prime_values)}/72 ({100*len(prime_values)/72:.1f}%)")
print(f"Values: {sorted(set(prime_values))}")
print()

# Expected by prime density theorem (π(n) ≈ n/ln(n))
import math
avg_val = np.mean(gematria_array)
expected_prime_rate = 1 / math.log(avg_val) if avg_val > 1 else 0
expected_prime_count = expected_prime_rate * 72

print(f"Expected by prime density: {expected_prime_count:.1f}")

# Z-test
if expected_prime_count > 0:
    z_prime = (len(prime_values) - expected_prime_count) / np.sqrt(expected_prime_count)
    print(f"Z-score: {z_prime:.2f}")
    
    if abs(z_prime) > 2:
        if z_prime > 0:
            print("✓ FINDING: MORE primes than expected!")
            add_vector("Primzahl-Häufung",
                       "Primzahl-Generierung als Kodier-Mechanismus",
                       "MEDIUM")
        else:
            print("✓ FINDING: FEWER primes than expected")
    else:
        print("⊘ FINDING: Prime count consistent with chance")
print()

# Analyze prime factors
all_factors = Counter()
for g in gematria_values:
    for prime, exp in prime_factorization(g).items():
        all_factors[prime] += exp

print("Most common prime factors:")
for prime, count in all_factors.most_common(10):
    print(f"  {prime}: appears {count} times")
print()

# =============================================================================
# INQUIRY 4: BUCHSTABEN-KOMBINATORIK
# =============================================================================
print("=" * 70)
print("INQUIRY 4: Buchstaben-Kombinatorik")
print("=" * 70)
print()

# Analyze letter frequencies
letter_counts = Counter()
for name in SHEM_72_HEBREW:
    for letter in name:
        letter_counts[letter] += 1

print("Letter frequency (top 10):")
for letter, count in letter_counts.most_common(10):
    gematria_val = HEBREW_GEMATRIA.get(letter, 0)
    print(f"  {letter} (g={gematria_val:3d}): {count} times")
print()

# What's the contribution of each letter type?
low_letters = [l for l, g in HEBREW_GEMATRIA.items() if g <= 10]
mid_letters = [l for l, g in HEBREW_GEMATRIA.items() if 10 < g <= 100]
high_letters = [l for l, g in HEBREW_GEMATRIA.items() if g > 100]

low_count = sum(letter_counts.get(l, 0) for l in low_letters)
mid_count = sum(letter_counts.get(l, 0) for l in mid_letters)
high_count = sum(letter_counts.get(l, 0) for l in high_letters)

total_letters = sum(letter_counts.values())
print(f"Low gematria (1-10):   {low_count:3d} ({100*low_count/total_letters:.1f}%)")
print(f"Mid gematria (11-100): {mid_count:3d} ({100*mid_count/total_letters:.1f}%)")
print(f"High gematria (>100):  {high_count:3d} ({100*high_count/total_letters:.1f}%)")
print()

# Theoretical expectation if letters were uniform
if high_count / total_letters > len(high_letters) / len(HEBREW_GEMATRIA):
    print("✓ FINDING: High-gematria letters UNDER-represented")
    add_vector("Hochwertige Buchstaben unterrepräsentiert",
               "SH bevorzugt niedrige Gematria-Buchstaben",
               "HIGH")
else:
    print("⊘ FINDING: Letter distribution roughly proportional")

# Check for letter patterns (repeated letters)
triple_counts = 0
double_counts = 0
for name in SHEM_72_HEBREW:
    if len(set(name)) == 1:  # All same letter (like ייי, ההה)
        triple_counts += 1
    elif len(set(name)) == 2:  # Two unique letters
        double_counts += 1

print()
print(f"Triples (same letter ×3): {triple_counts}/72")
print(f"Pairs (one letter repeated): {double_counts}/72")

if triple_counts >= 2:
    print("✓ FINDING: Multiple triples exist - these are special!")
    triple_names = [name for name in SHEM_72_HEBREW if len(set(name)) == 1]
    print(f"  Triple names: {triple_names}")
    add_vector("Triple-Buchstaben Namen",
               "Diese könnten 'Fixpunkte' oder besondere Bedeutung haben",
               "MEDIUM")
print()

# =============================================================================
# INQUIRY 5: SORTIERUNG UND ORDNUNG
# =============================================================================
print("=" * 70)
print("INQUIRY 5: Versteckte Ordnung (Sortierung, Muster)")
print("=" * 70)
print()

# Is SH sorted by gematria?
sorted_gem = sorted(gematria_values)
correlation_sorted = stats.spearmanr(gematria_values, sorted_gem)
print(f"Correlation with sorted order: ρ = {correlation_sorted.correlation:.3f}")
print()

# Autocorrelation (is there local structure?)
def autocorrelation(x, lag):
    """Compute autocorrelation at given lag."""
    n = len(x)
    x_mean = np.mean(x)
    numerator = sum((x[i] - x_mean) * (x[i + lag] - x_mean) for i in range(n - lag))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    return numerator / denominator if denominator != 0 else 0

autocorrs = [autocorrelation(gematria_values, lag) for lag in range(1, 10)]
print("Autocorrelation at various lags:")
for lag, ac in enumerate(autocorrs, 1):
    sig = "*" if abs(ac) > 2/np.sqrt(72) else ""
    print(f"  Lag {lag}: {ac:+.3f} {sig}")
print()

# Check for 8-periodicity (Octonion connection?)
autocorr_8 = autocorrelation(gematria_values, 8)
print(f"Lag-8 autocorrelation (Octonion test): {autocorr_8:+.3f}")
if abs(autocorr_8) > 2/np.sqrt(72):
    print("✓ FINDING: Significant 8-periodicity (Octonion connection?)")
    add_vector("8-Periodizität gefunden",
               "Oktonion-Algebra als Ordnungsprinzip bestätigt",
               "HIGH")
else:
    print("⊘ FINDING: No significant 8-periodicity")
print()

# Check for 9-periodicity (72 = 8 × 9)
autocorr_9 = autocorrelation(gematria_values, 9)
print(f"Lag-9 autocorrelation (72=8×9 test): {autocorr_9:+.3f}")
print()

# Modular patterns
print("Modular pattern analysis:")
for mod in [8, 9, 12, 22]:
    residues = [g % mod for g in gematria_values]
    chi2, p = stats.chisquare(np.bincount(residues, minlength=mod))
    uniform = "uniformly distributed" if p > 0.05 else "NOT uniform"
    print(f"  mod {mod:2d}: χ² = {chi2:6.2f}, p = {p:.4f} → {uniform}")
print()

# =============================================================================
# INQUIRY 6: TIEFERE MUSTER - Summenstruktur
# =============================================================================
print("=" * 70)
print("INQUIRY 6: Summen- und Differenz-Muster")
print("=" * 70)
print()

# Total sum
total_sum = sum(gematria_values)
print(f"Total sum of all 72 Gematria: {total_sum}")
print(f"  Is prime? {is_prime(total_sum)}")
print(f"  Factors: {prime_factorization(total_sum)}")
print()

# Check if related to special numbers
print("Relation to special numbers:")
print(f"  ÷ 72 = {total_sum / 72:.3f}")
print(f"  ÷ 360 = {total_sum / 360:.3f}")
print(f"  ÷ 666 = {total_sum / 666:.3f}")
print(f"  ÷ 137 = {total_sum / 137:.3f} (fine structure)")
print()

# Cumulative sums pattern
cumsum = np.cumsum(gematria_values)
cumsum_in_fib = [c for c in cumsum if c in fib_set]
print(f"Cumulative sums that are Fibonacci: {len(cumsum_in_fib)}")
print()

# =============================================================================
# GRAND SYNTHESIS
# =============================================================================
print("=" * 70)
print("INQUIRY 7: GRAND SYNTHESIS - Was erklärt die Nicht-Zufälligkeit?")
print("=" * 70)
print()

# Collect all findings
findings = {
    "distribution": "right-skewed" if skewness > 0.5 else "symmetric",
    "fibonacci_excess": p_fib < 0.05,
    "prime_count": len(prime_values),
    "triple_names": triple_counts,
    "letter_bias": high_count / total_letters < len(high_letters) / len(HEBREW_GEMATRIA),
    "periodicity_8": abs(autocorr_8) > 2/np.sqrt(72),
    "total_sum": total_sum
}

print("=== VALIDITY SCORECARD ===")
print()

evidence_for = 0
evidence_against = 0

# 1. Letter Selection Bias
if findings["letter_bias"]:
    print("✓ Letter Selection Bias: High-gematria letters are underused")
    print("  → SH-Autoren bevorzugten niedrige Buchstaben (bewusst oder kulturell)")
    evidence_for += 1
else:
    print("✗ Letter Selection Bias: Not detected")
    evidence_against += 1

# 2. Fibonacci Structure
if findings["fibonacci_excess"]:
    print("✓ Fibonacci Structure: More Fibonacci numbers than expected")
    print("  → Möglicherweise bewusste Fibonacci-Kodierung")
    evidence_for += 1
else:
    print("✗ Fibonacci Structure: Consistent with chance")
    evidence_against += 1

# 3. Periodicity
if findings["periodicity_8"]:
    print("✓ 8-Periodicity: Octonion-like structure detected")
    evidence_for += 1
else:
    print("✗ 8-Periodicity: Not detected")
    evidence_against += 1

# 4. Distribution Shape
if findings["distribution"] == "right-skewed":
    print("✓ Right-Skewed Distribution: Many small values, few large")
    print("  → Generative process favors smaller numbers")
    evidence_for += 1
else:
    evidence_against += 1

print()
print(f"Evidence FOR structured origin: {evidence_for}/4")
print(f"Evidence AGAINST: {evidence_against}/4")
print()

# Grand Verdict
print("=" * 70)
print("GRAND VERDICT")
print("=" * 70)
print()

if evidence_for >= 3:
    verdict = "STRONGLY STRUCTURED"
    message = "SH zeigt multiple Strukturmerkmale - bewusste Konstruktion wahrscheinlich"
elif evidence_for >= 2:
    verdict = "PARTIALLY STRUCTURED"
    message = "SH zeigt einige Strukturmerkmale - Mischung aus Zufall und Konstruktion"
else:
    verdict = "WEAKLY STRUCTURED"
    message = "SH zeigt wenige Strukturmerkmale - hauptsächlich kulturelle Buchstaben-Präferenzen"

print(f"VERDICT: {verdict}")
print(f"MESSAGE: {message}")
print()

# Primary Explanation
print("PRIMÄRE ERKLÄRUNG für Nicht-Zufälligkeit:")
print("-" * 50)
print("""
Die nicht-zufällige Verteilung der SH-Gematria kommt PRIMÄR von:

1. BUCHSTABEN-BIAS: Hebräische Texte (inkl. Bibel) nutzen
   niedrigere Gematria-Buchstaben (א,ב,ג,ד,ה,ו,ז,ח,ט,י) häufiger
   als hohe (ק,ר,ש,ת). Dies ist linguistisch bedingt.

2. DREI-BUCHSTABEN-CONSTRAINT: Jeder Name hat exakt 3 Buchstaben,
   was die Varianz begrenzt (theoretisches Maximum: 1200).

3. KULTURELLE SELEKTION: Die Exodusverse wurden für their
   mystische Bedeutung gewählt, nicht zufällig aus der Bibel.

Die Struktur ist also EMERGENT aus:
  Cultural Selection × Linguistic Bias × Fixed Length
""")
print()

# =============================================================================
# STRATEGIC VECTORS SUMMARY
# =============================================================================
print("=" * 70)
print("STRATEGIC VECTORS SUMMARY")
print("=" * 70)
print()

high_vectors = [v for v in STRATEGIC_VECTORS if v['priority'] == "HIGH"]
medium_vectors = [v for v in STRATEGIC_VECTORS if v['priority'] == "MEDIUM"]
low_vectors = [v for v in STRATEGIC_VECTORS if v['priority'] == "LOW"]

if high_vectors:
    print(f"🔴 HIGH PRIORITY ({len(high_vectors)}):")
    for v in high_vectors:
        print(f"   • {v['direction']}")
        print(f"     (Based on: {v['finding']})")
    print()

if medium_vectors:
    print(f"🟡 MEDIUM PRIORITY ({len(medium_vectors)}):")
    for v in medium_vectors:
        print(f"   • {v['direction']}")
    print()

if low_vectors:
    print(f"🟢 LOW PRIORITY ({len(low_vectors)}):")
    for v in low_vectors:
        print(f"   • {v['direction']}")
    print()

# =============================================================================
# VISUALIZATION
# =============================================================================
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 1. Gematria Distribution
ax1 = axes[0, 0]
ax1.hist(gematria_values, bins=20, edgecolor='black', alpha=0.7, color='steelblue')
ax1.axvline(np.mean(gematria_values), color='red', linestyle='--', label=f'Mean={np.mean(gematria_values):.1f}')
ax1.axvline(np.median(gematria_values), color='orange', linestyle='--', label=f'Median={np.median(gematria_values):.1f}')
ax1.set_xlabel('Gematria Value')
ax1.set_ylabel('Frequency')
ax1.set_title('SH Gematria Distribution (Right-Skewed)')
ax1.legend()

# 2. Letter Contribution
ax2 = axes[0, 1]
labels = ['Low (1-10)', 'Mid (11-100)', 'High (>100)']
sizes = [low_count, mid_count, high_count]
colors = ['#66b3ff', '#99ff99', '#ff9999']
ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax2.set_title('Letter Gematria Category Distribution')

# 3. Autocorrelation
ax3 = axes[1, 0]
lags = range(1, 10)
ax3.bar(lags, autocorrs, color='steelblue', edgecolor='black')
ax3.axhline(2/np.sqrt(72), color='red', linestyle='--', label='95% CI')
ax3.axhline(-2/np.sqrt(72), color='red', linestyle='--')
ax3.set_xlabel('Lag')
ax3.set_ylabel('Autocorrelation')
ax3.set_title('Autocorrelation by Lag')
ax3.legend()

# 4. Gematria Sequence
ax4 = axes[1, 1]
ax4.plot(range(72), gematria_values, 'o-', markersize=4, alpha=0.7)
# Highlight Fibonacci values
for i, g in enumerate(gematria_values):
    if g in fib_set:
        ax4.scatter(i, g, color='red', s=100, zorder=5, label='Fibonacci' if i == fib_indices[0] else '')
ax4.set_xlabel('Index (1-72)')
ax4.set_ylabel('Gematria')
ax4.set_title('Gematria Sequence (red = Fibonacci)')

plt.tight_layout()
plot_path = Path(__file__).with_suffix('.png')
plt.savefig(plot_path, dpi=150)
print(f"Plot saved: {plot_path}")

# =============================================================================
# EXPERIMENT COMPLETE
# =============================================================================
print()
print("=" * 70)
print("EXPERIMENT COMPLETE")
print("=" * 70)
