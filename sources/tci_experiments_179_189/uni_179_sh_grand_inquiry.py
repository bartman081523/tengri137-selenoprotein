#!/usr/bin/env python3
"""
uni_179_sh_grand_inquiry.py - Shem Hamephorash: Offene Grand Unification

DESIGN PRINCIPLES (SciMind4 Ergebnisoffen):
1. Keine vorbestimmte Hypothese - wir FRAGEN, was die Daten zeigen
2. Strategische Vektoren werden WÄHREND des Experiments generiert
3. Jeder Fund bestimmt die Richtung des nächsten Tests
4. Am Ende: Was ist die stärkste empirische Aussage zu SH?

INQUIRY CHAIN:
Q1: Hat SH-Gematria überhaupt Struktur? (vs Random)
Q2: Korreliert SH mit bekannter Physik? (α, φ, π)
Q3: Zeigt SH topologische Signaturen? (Winding, Clusters)
Q4: Kann SH als Kommunikations-Basis dienen? (Mutual Info)
Q5: Grand Synthesis - Was folgt?
"""

# ==============================================================================
# TEE LOGGER
# ==============================================================================
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
    def close(self):
        self.log.close()

_log_path = Path(__file__).with_suffix('.log.txt')
sys.stdout = TeeLogger(_log_path)

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter

print("="*70)
print("UNI-179: SHEM HAMEPHORASH - OFFENE GRAND INQUIRY")
print("="*70)
print("\nDESIGN: Ergebnisoffen - Daten bestimmen Richtung")
print("METHOD: Inquiry Chain mit dynamischen Strategic Vectors\n")

# ==============================================================================
# SHEM HAMEPHORASH DATA
# ==============================================================================

SHEM_72 = [
    ("והו", "Vehu", 1), ("ילי", "Yeli", 2), ("סיט", "Sit", 3), ("עלם", "Alam", 4),
    ("מהש", "Mahash", 5), ("ללה", "Lelah", 6), ("אכא", "Akha", 7), ("כהת", "Kahat", 8),
    ("הזי", "Hazi", 9), ("אלד", "Elad", 10), ("לאו", "Lav", 11), ("ההע", "Haha", 12),
    ("יזל", "Yazal", 13), ("מבה", "Mabeh", 14), ("הרי", "Hari", 15), ("הקמ", "Hakam", 16),
    ("לאו", "Lav2", 17), ("כלי", "Keli", 18), ("לוו", "Lev", 19), ("פהל", "Pehel", 20),
    ("נלכ", "Nalak", 21), ("ייי", "Yeye", 22), ("מלה", "Melah", 23), ("חהו", "Chahu", 24),
    ("נתה", "Nitah", 25), ("האא", "Haa", 26), ("ירת", "Yarat", 27), ("שאה", "Shaah", 28),
    ("ריי", "Riyi", 29), ("אום", "Aum", 30), ("לכב", "Lekab", 31), ("ושר", "Veshar", 32),
    ("יחו", "Yecho", 33), ("להח", "Lehach", 34), ("כוק", "Kavak", 35), ("מנד", "Manad", 36),
    ("אני", "Ani", 37), ("חעם", "Chaam", 38), ("רהע", "Raha", 39), ("ייז", "Yayaz", 40),
    ("ההה", "Hahah", 41), ("מיכ", "Mikh", 42), ("וול", "Veval", 43), ("ילה", "Yalah", 44),
    ("סאל", "Sael", 45), ("ערי", "Ari", 46), ("עשל", "Ashal", 47), ("מיה", "Miyah", 48),
    ("והו", "Vehu2", 49), ("דני", "Dani", 50), ("החש", "Hachash", 51), ("עמם", "Amam", 52),
    ("ננא", "Nana", 53), ("נית", "Nit", 54), ("מבה", "Mabeh2", 55), ("פוי", "Poi", 56),
    ("נמם", "Namam", 57), ("ייל", "Yayel", 58), ("הרח", "Harach", 59), ("מצר", "Matzar", 60),
    ("ומב", "Umab", 61), ("יהה", "Yehah", 62), ("ענו", "Anu", 63), ("מחי", "Machi", 64),
    ("דמב", "Damab", 65), ("מנק", "Manak", 66), ("איע", "Aya", 67), ("חבו", "Chavu", 68),
    ("ראה", "Raah", 69), ("יבם", "Yabam", 70), ("היי", "Hayi", 71), ("מום", "Mum", 72)
]

GEMATRIA = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
    'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'צ': 90,
    'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400
}

def name_to_gematria(name):
    return sum(GEMATRIA.get(c, 0) for c in name)

# Compute all values
SH_VALUES = [name_to_gematria(name) for name, _, _ in SHEM_72]
SH_NAMES = [name for name, _, _ in SHEM_72]

# Physical constants
PHI = (1 + np.sqrt(5)) / 2
ALPHA = 1 / 137.036
PI = np.pi

# Strategic vectors collector
STRATEGIC_VECTORS = []

def add_vector(finding, direction, priority="MEDIUM"):
    """Add a strategic vector based on experimental finding"""
    STRATEGIC_VECTORS.append({
        'finding': finding,
        'direction': direction,
        'priority': priority
    })
    print(f"  ⟹ STRATEGIC VECTOR [{priority}]: {direction}")

# ==============================================================================
# INQUIRY 1: STRUCTURE TEST
# ==============================================================================

print("\n" + "="*70)
print("INQUIRY 1: Hat SH-Gematria Struktur? (vs Random Baseline)")
print("="*70)

# Null: SH values are random
# Test: Compare distribution properties

sh_mean = np.mean(SH_VALUES)
sh_std = np.std(SH_VALUES)
sh_min = np.min(SH_VALUES)
sh_max = np.max(SH_VALUES)

print(f"\nSH Statistics:")
print(f"  N = {len(SH_VALUES)}")
print(f"  Mean = {sh_mean:.2f}")
print(f"  Std = {sh_std:.2f}")
print(f"  Range = [{sh_min}, {sh_max}]")

# Generate 10000 random samples with same constraints
np.random.seed(42)
random_samples = []
for _ in range(10000):
    # Random 3-letter Hebrew names
    sample = []
    for _ in range(72):
        letters = np.random.choice(list(GEMATRIA.keys()), 3)
        val = sum(GEMATRIA[l] for l in letters)
        sample.append(val)
    random_samples.append(sample)

random_means = [np.mean(s) for s in random_samples]
random_stds = [np.std(s) for s in random_samples]

# Z-scores
z_mean = (sh_mean - np.mean(random_means)) / np.std(random_means)
z_std = (sh_std - np.mean(random_stds)) / np.std(random_stds)

print(f"\nComparison vs Random (n=10000):")
print(f"  Mean Z-score: {z_mean:.2f}")
print(f"  Std Z-score: {z_std:.2f}")

# Kolmogorov-Smirnov test
ks_stat, ks_p = stats.kstest(SH_VALUES, 'uniform', args=(sh_min, sh_max - sh_min))
print(f"  KS test (vs uniform): stat={ks_stat:.3f}, p={ks_p:.4f}")

# Finding
if abs(z_mean) > 2 or abs(z_std) > 2:
    print("\n✓ FINDING: SH distribution is SIGNIFICANTLY different from random")
    add_vector(
        "SH hat nicht-zufällige Verteilung",
        "Untersuche WARUM - Kodiersystem? Mathematische Regel?",
        "HIGH"
    )
else:
    print("\n⊘ FINDING: SH distribution is consistent with random selection")
    add_vector(
        "SH statistisch nicht unterscheidbar von Zufall",
        "Fokus auf lokale Struktur (Nachbarschaft, Sequenzen)",
        "MEDIUM"
    )

# ==============================================================================
# INQUIRY 2: CORRELATION WITH PHYSICS
# ==============================================================================

print("\n" + "="*70)
print("INQUIRY 2: Korreliert SH mit fundamentalen Konstanten?")
print("="*70)

# Test correlations with φ, α, π
indices = np.arange(1, 73)

# Golden Ratio pattern
phi_predicted = indices * PHI % 100 * 5  # Scaled
corr_phi, p_phi = stats.pearsonr(SH_VALUES, phi_predicted[:72])
print(f"\nCorrelation with φ-pattern: r={corr_phi:.3f}, p={p_phi:.4f}")

# Fine structure constant pattern
alpha_predicted = np.sin(indices * ALPHA * 100) * 100 + 100
corr_alpha, p_alpha = stats.pearsonr(SH_VALUES, alpha_predicted[:72])
print(f"Correlation with α-pattern: r={corr_alpha:.3f}, p={p_alpha:.4f}")

# Pi pattern
pi_predicted = (indices * PI) % 100 * 5
corr_pi, p_pi = stats.pearsonr(SH_VALUES, pi_predicted[:72])
print(f"Correlation with π-pattern: r={corr_pi:.3f}, p={p_pi:.4f}")

# Check for any significant correlation
best_corr = max(abs(corr_phi), abs(corr_alpha), abs(corr_pi))
best_name = "φ" if best_corr == abs(corr_phi) else ("α" if best_corr == abs(corr_alpha) else "π")

if best_corr > 0.3:
    print(f"\n✓ FINDING: Significant correlation with {best_name} (r={best_corr:.3f})")
    add_vector(
        f"SH korreliert mit {best_name}",
        f"Tiefere Analyse der {best_name}-Verbindung: Ableitung aus erster Prinzipien?",
        "HIGH"
    )
else:
    print(f"\n⊘ FINDING: No significant correlation with tested constants")
    # Check for OTHER patterns
    # Modular arithmetic
    mod_12 = [v % 12 for v in SH_VALUES]
    mod_22 = [v % 22 for v in SH_VALUES]  # 22 Hebrew letters
    
    chi_12, p_12 = stats.chisquare([mod_12.count(i) for i in range(12)])
    chi_22, p_22 = stats.chisquare([mod_22.count(i) for i in range(22)])
    
    print(f"  Mod-12 uniformity: χ²={chi_12:.1f}, p={p_12:.4f}")
    print(f"  Mod-22 uniformity: χ²={chi_22:.1f}, p={p_22:.4f}")
    
    if p_12 < 0.05:
        add_vector(
            "SH mod 12 ist nicht-uniform",
            "12-er Struktur untersuchen (Tierkreis? Stämme Israels?)",
            "MEDIUM"
        )
    if p_22 < 0.05:
        add_vector(
            "SH mod 22 ist nicht-uniform",
            "Verbindung zu 22 hebräischen Buchstaben analysieren",
            "MEDIUM"
        )

# ==============================================================================
# INQUIRY 3: TOPOLOGICAL SIGNATURES
# ==============================================================================

print("\n" + "="*70)
print("INQUIRY 3: Topologische Signaturen in SH?")
print("="*70)

# Map SH to 2D phase space
phases = np.array(SH_VALUES) * PHI % (2 * np.pi)
x_coords = np.cos(phases)
y_coords = np.sin(phases)

# Compute winding number (topological invariant)
angles = np.arctan2(y_coords, x_coords)
angle_diffs = np.diff(np.unwrap(angles))
winding = np.sum(angle_diffs) / (2 * np.pi)

print(f"\nPhase Space Analysis:")
print(f"  Points: {len(phases)}")
print(f"  Winding Number: {winding:.3f}")

# Compare to random
random_windings = []
for _ in range(1000):
    rand_phases = np.random.rand(72) * 2 * np.pi
    rand_angles = rand_phases  # Already in [0, 2π]
    rand_diffs = np.diff(np.unwrap(rand_angles))
    rand_winding = np.sum(rand_diffs) / (2 * np.pi)
    random_windings.append(rand_winding)

winding_z = (winding - np.mean(random_windings)) / np.std(random_windings)
print(f"  Winding Z-score vs random: {winding_z:.2f}")

# Clustering analysis
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, fcluster

points = np.column_stack([x_coords, y_coords])
distances = pdist(points)
linkage_matrix = linkage(distances, method='ward')
n_clusters = len(np.unique(fcluster(linkage_matrix, t=3, criterion='maxclust')))

print(f"  Natural clusters (t=3): {n_clusters}")

# Finding
if abs(winding_z) > 2:
    print(f"\n✓ FINDING: Significant topological structure (winding Z={winding_z:.2f})")
    add_vector(
        f"SH hat topologische Signatur (Winding Z={winding_z:.2f})",
        "Verbindung zu Braiding/Knottentheorie untersuchen",
        "HIGH"
    )
else:
    print(f"\n⊘ FINDING: Winding number consistent with random")
    add_vector(
        "Keine globale Topologie aber lokale Cluster möglich",
        "Cluster-Analyse vertiefen: Welche Namen sind nahe beieinander?",
        "LOW"
    )

# ==============================================================================
# INQUIRY 4: COMMUNICATION POTENTIAL
# ==============================================================================

print("\n" + "="*70)
print("INQUIRY 4: Kann SH als Kommunikationsbasis dienen?")
print("="*70)

# Information theoretic analysis
# Entropy of SH values
value_counts = Counter(SH_VALUES)
probs = np.array(list(value_counts.values())) / len(SH_VALUES)
entropy = -np.sum(probs * np.log2(probs))
max_entropy = np.log2(len(set(SH_VALUES)))

print(f"\nInformation Theory:")
print(f"  Unique values: {len(set(SH_VALUES))}")
print(f"  Entropy: {entropy:.3f} bits")
print(f"  Max entropy: {max_entropy:.3f} bits")
print(f"  Efficiency: {entropy/max_entropy*100:.1f}%")

# Mutual information with index
# How much does position tell about value?
def mutual_info(x, y, bins=10):
    c_xy, _, _ = np.histogram2d(x, y, bins=bins)
    c_x = np.histogram(x, bins=bins)[0]
    c_y = np.histogram(y, bins=bins)[0]
    
    p_xy = c_xy / np.sum(c_xy)
    p_x = c_x / np.sum(c_x)
    p_y = c_y / np.sum(c_y)
    
    mi = 0
    for i in range(bins):
        for j in range(bins):
            if p_xy[i, j] > 0 and p_x[i] > 0 and p_y[j] > 0:
                mi += p_xy[i, j] * np.log2(p_xy[i, j] / (p_x[i] * p_y[j]))
    return mi

mi_index = mutual_info(indices, SH_VALUES)
print(f"  Mutual Info (index→value): {mi_index:.3f} bits")

# Compare to random
random_mis = []
for _ in range(1000):
    perm = np.random.permutation(SH_VALUES)
    random_mis.append(mutual_info(indices, perm))

mi_z = (mi_index - np.mean(random_mis)) / np.std(random_mis)
print(f"  MI Z-score vs shuffled: {mi_z:.2f}")

# Finding
if mi_z > 2:
    print(f"\n✓ FINDING: Position predicts value - ordered sequence!")
    add_vector(
        "SH-Reihenfolge ist informativ",
        "Die 72 Namen bilden eine sinnvolle SEQUENZ - nicht nur ein Set",
        "HIGH"
    )
elif entropy / max_entropy > 0.9:
    print(f"\n⊘ FINDING: High entropy but no sequential structure")
    add_vector(
        "SH ist informationsreich aber nicht sequentiell geordnet",
        "Als Codebuch (Dictionary) statt als Sequenz nutzen",
        "MEDIUM"
    )
else:
    print(f"\n⊘ FINDING: Low unique values - redundancy in system")
    add_vector(
        "SH hat Redundanz (wiederholte Werte)",
        "Prüfen ob Redundanz absichtlich (Fehlerkorrektur?)",
        "MEDIUM"
    )

# ==============================================================================
# INQUIRY 5: GRAND SYNTHESIS
# ==============================================================================

print("\n" + "="*70)
print("INQUIRY 5: GRAND SYNTHESIS")
print("="*70)

# Compute overall validity score
scores = {
    'structure': 1 if (abs(z_mean) > 2 or abs(z_std) > 2) else 0,
    'physics': 1 if best_corr > 0.3 else 0,
    'topology': 1 if abs(winding_z) > 2 else 0,
    'communication': 1 if mi_z > 2 or entropy/max_entropy > 0.9 else 0
}

total_score = sum(scores.values())

print(f"\nVALIDITY SCORECARD:")
print(f"  Structure (vs Random):    {'✓' if scores['structure'] else '✗'}")
print(f"  Physics Correlation:       {'✓' if scores['physics'] else '✗'}")
print(f"  Topological Signature:     {'✓' if scores['topology'] else '✗'}")
print(f"  Communication Potential:   {'✓' if scores['communication'] else '✗'}")
print(f"  \n  TOTAL: {total_score}/4")

# Grand finding
if total_score >= 3:
    verdict = "STRONGLY CORROBORATED"
    message = "SH zeigt multiple nicht-zufällige Eigenschaften"
elif total_score >= 2:
    verdict = "PARTIALLY CORROBORATED"
    message = "SH zeigt einige interessante Eigenschaften"
elif total_score >= 1:
    verdict = "WEAK EVIDENCE"
    message = "Nur eine Dimension zeigt Nicht-Zufälligkeit"
else:
    verdict = "NOT CORROBORATED"
    message = "Keine statistisch signifikanten Eigenschaften gefunden"

print(f"\nGRAND VERDICT: {verdict}")
print(f"MESSAGE: {message}")

# ==============================================================================
# STRATEGIC VECTORS SUMMARY
# ==============================================================================

print("\n" + "="*70)
print("STRATEGIC VECTORS SUMMARY")
print("="*70)

high_priority = [v for v in STRATEGIC_VECTORS if v['priority'] == 'HIGH']
medium_priority = [v for v in STRATEGIC_VECTORS if v['priority'] == 'MEDIUM']
low_priority = [v for v in STRATEGIC_VECTORS if v['priority'] == 'LOW']

print(f"\n🔴 HIGH PRIORITY ({len(high_priority)}):")
for v in high_priority:
    print(f"   • {v['direction']}")
    print(f"     (Based on: {v['finding']})")

print(f"\n🟡 MEDIUM PRIORITY ({len(medium_priority)}):")
for v in medium_priority:
    print(f"   • {v['direction']}")

print(f"\n🟢 LOW PRIORITY ({len(low_priority)}):")
for v in low_priority:
    print(f"   • {v['direction']}")

# ==============================================================================
# VISUALIZATION
# ==============================================================================

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Plot 1: SH Value Distribution
ax1 = axes[0, 0]
ax1.hist(SH_VALUES, bins=20, color='gold', edgecolor='black', alpha=0.7)
ax1.axvline(sh_mean, color='red', linestyle='--', label=f'Mean: {sh_mean:.0f}')
ax1.set_xlabel('Gematria Value')
ax1.set_ylabel('Count')
ax1.set_title('SH Gematria Distribution')
ax1.legend()

# Plot 2: Phase Space
ax2 = axes[0, 1]
colors = plt.cm.hsv(np.linspace(0, 1, 72))
for i in range(72):
    ax2.scatter(x_coords[i], y_coords[i], c=[colors[i]], s=30)
ax2.set_xlabel('cos(φ·value)')
ax2.set_ylabel('sin(φ·value)')
ax2.set_title(f'Phase Space (Winding Z={winding_z:.2f})')
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)

# Plot 3: Correlations
ax3 = axes[0, 2]
correlations = [corr_phi, corr_alpha, corr_pi]
labels = ['φ', 'α', 'π']
colors_bar = ['gold', 'blue', 'green']
bars = ax3.bar(labels, correlations, color=colors_bar, alpha=0.7)
ax3.axhline(0.3, color='red', linestyle='--', label='Significance threshold')
ax3.axhline(-0.3, color='red', linestyle='--')
ax3.set_ylabel('Pearson r')
ax3.set_title('Correlation with Physical Constants')
ax3.legend()

# Plot 4: Values by Index
ax4 = axes[1, 0]
ax4.plot(indices, SH_VALUES, 'b-', alpha=0.5)
ax4.scatter(indices, SH_VALUES, c=colors, s=20)
ax4.set_xlabel('SH Index (1-72)')
ax4.set_ylabel('Gematria Value')
ax4.set_title('Values by Position')

# Plot 5: Modular Structure
ax5 = axes[1, 1]
mod_values = [v % 22 for v in SH_VALUES]
ax5.hist(mod_values, bins=22, color='purple', edgecolor='black', alpha=0.7)
ax5.set_xlabel('Value mod 22')
ax5.set_ylabel('Count')
ax5.set_title('Mod-22 Distribution (22 Letters)')

# Plot 6: Summary
ax6 = axes[1, 2]
ax6.axis('off')
summary = f"""
GRAND INQUIRY SUMMARY
=====================

VERDICT: {verdict}
SCORE: {total_score}/4

Individual Tests:
  Structure:      {'PASS' if scores['structure'] else 'FAIL'}
  Physics:        {'PASS' if scores['physics'] else 'FAIL'}
  Topology:       {'PASS' if scores['topology'] else 'FAIL'}
  Communication:  {'PASS' if scores['communication'] else 'FAIL'}

Key Statistics:
  Mean Gematria: {sh_mean:.1f}
  Unique Values: {len(set(SH_VALUES))}
  Entropy: {entropy:.2f} bits
  MI(index): {mi_index:.3f} bits

High-Priority Directions:
{chr(10).join(['• ' + v['direction'][:50] for v in high_priority[:3]])}
"""
ax6.text(0.5, 0.5, summary, ha='center', va='center', fontsize=10, 
         family='monospace', transform=ax6.transAxes,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle("uni_179: Shem Hamephorash - Offene Grand Inquiry", fontsize=14, fontweight='bold')
plt.tight_layout()

output_path = Path(__file__).parent / "uni_179_sh_grand_inquiry.png"
plt.savefig(output_path, dpi=150)
print(f"\nPlot saved: {output_path}")

print("\n" + "="*70)
print("EXPERIMENT COMPLETE")
print("="*70)
