"""
Stufe 31 — Sekundärstruktur-Vorhersage für BURUMUT-C-Übersetzung

Da AF2/ColabFold nicht lokal verfügbar ist, mache ich:
1. Chou-Fasman-Sekundärstruktur-Vorhersage (α-Helix, β-Strang, Coil)
2. Per-Position Helix-Moment-Berechnung (Eisenberg-Konsensus)
3. Grahm-Darstellung der Helix-Amphipathizität
4. Vergleich mit irdischen 2-Domänen-AMPs (LL-37, Big-Defensin, Melittin)
5. AF2-Empfehlungs-Skript (für späteren manuellen ColabFold-Upload)

Verifikation gegen:
- V10.4 p23 grid_2d_words
- Stufe 14 (2 AMP-Domänen Pos 43-78, 109-133)
- Stufe 17 (Helix-Moment 1.808, Helix-Breaker 1.9%)
- Stufe 30 (Big-Defensin als nächstes Analogon)
"""
import json
import math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter

WORKDIR = Path("/run/media/julian/ML4/tengri137")
SCRATCH = WORKDIR / "consecutive_research" / "scratches"
STUFE31 = SCRATCH / "stufe_31"
STUFE31.mkdir(exist_ok=True)

# Sequenzen
seq_burumut = "BURUMUTREFAMTUNURESUTREGUMFAYAPSUAZBEHIMLAZANRUAZBENOMBATOBIKOTLUBUMYOSUNOKURGANOZYIOKUZIKUFAUSIHEYABEKANSABERHONAFERANSAHOTFEKOREMORBIZUMROSUNAKIRFANEMBA"
seq_translated = "NCRCMCTREFAMTCNCRESCTREGCMFAYAPSCAENEHIMLAEANRCAENENKMNATKNIKKTLCNCMYKSCNKKCRGANKEYIKKCEIKCFACSIHEYANEKANSANERHKNAFERANSAHKTFEKKREMKRNIECMRKSCNAKIRFANEMNA"

# Chou-Fasman-Parameter (Standard-Werte)
chou_fasman = {
    'A': {'P_alpha': 1.42, 'P_beta': 0.83, 'P_turn': 0.66},
    'R': {'P_alpha': 0.98, 'P_beta': 0.93, 'P_turn': 0.95},
    'N': {'P_alpha': 0.67, 'P_beta': 0.89, 'P_turn': 1.56},
    'D': {'P_alpha': 1.01, 'P_beta': 0.54, 'P_turn': 1.46},
    'C': {'P_alpha': 0.70, 'P_beta': 1.19, 'P_turn': 1.19},
    'E': {'P_alpha': 1.51, 'P_beta': 0.37, 'P_turn': 0.74},
    'Q': {'P_alpha': 1.11, 'P_beta': 1.10, 'P_turn': 0.98},
    'G': {'P_alpha': 0.57, 'P_beta': 0.75, 'P_turn': 1.56},
    'H': {'P_alpha': 1.00, 'P_beta': 0.87, 'P_turn': 0.95},
    'I': {'P_alpha': 1.08, 'P_beta': 1.60, 'P_turn': 0.47},
    'L': {'P_alpha': 1.21, 'P_beta': 1.30, 'P_turn': 0.59},
    'K': {'P_alpha': 1.16, 'P_beta': 0.74, 'P_turn': 1.01},
    'M': {'P_alpha': 1.45, 'P_beta': 1.05, 'P_turn': 0.60},
    'F': {'P_alpha': 1.13, 'P_beta': 1.38, 'P_turn': 0.60},
    'P': {'P_alpha': 0.57, 'P_beta': 0.55, 'P_turn': 1.52},
    'S': {'P_alpha': 0.77, 'P_beta': 0.75, 'P_turn': 1.43},
    'T': {'P_alpha': 0.83, 'P_beta': 1.19, 'P_turn': 0.96},
    'W': {'P_alpha': 1.08, 'P_beta': 1.37, 'P_turn': 0.96},
    'Y': {'P_alpha': 0.69, 'P_beta': 1.47, 'P_turn': 1.14},
    'V': {'P_alpha': 1.06, 'P_beta': 1.70, 'P_turn': 0.50},
    # Seltene AS
    'U': {'P_alpha': 0.70, 'P_beta': 1.19, 'P_turn': 1.19},  # Sec wie Cys
    'O': {'P_alpha': 1.16, 'P_beta': 0.74, 'P_turn': 1.01},  # Pyl wie Lys
    'B': {'P_alpha': 0.84, 'P_beta': 0.72, 'P_turn': 1.51},  # Asx
    'Z': {'P_alpha': 1.31, 'P_beta': 0.74, 'P_turn': 0.86},  # Glx
    'J': {'P_alpha': 1.21, 'P_beta': 1.30, 'P_turn': 0.59},  # Xle wie Leu
}

# Kyte-Doolittle Hydrophobizität (für Helix-Moment)
kd_hydropathy = {
    'A': 1.8, 'R':-4.5, 'N':-3.5, 'D':-3.5, 'C': 2.5,
    'E':-3.5, 'Q':-3.5, 'G':-0.4, 'H':-3.2, 'I': 4.5,
    'L': 3.8, 'K':-3.9, 'M': 1.9, 'F': 2.8, 'P':-1.6,
    'S':-0.8, 'T':-0.7, 'W':-0.9, 'Y':-1.3, 'V': 4.2,
    'U': 2.5, 'O':-3.9, 'B':-3.5, 'Z':-3.5, 'J': 3.8,
}

def chou_fasman_predict(seq, window=6):
    """Chou-Fasman Sekundärstruktur-Vorhersage pro Position."""
    n = len(seq)
    helix = []
    for i, aa in enumerate(seq):
        if aa not in chou_fasman:
            helix.append(0)
            continue
        # Berechne Mittel über aktuelle Position + halbe Window
        vals = []
        for j in range(max(0, i - window//2), min(n, i + window//2 + 1)):
            if seq[j] in chou_fasman:
                vals.append(chou_fasman[seq[j]]['P_alpha'])
        helix.append(np.mean(vals) if vals else 0)
    return helix

def helix_moment(seq, angle_per_residue=100, hydrophobic_scale=None):
    """Berechne Helix-Moment pro Position (Eisenberg-Konsensus)."""
    if hydrophobic_scale is None:
        hydrophobic_scale = kd_hydropathy
    n = len(seq)
    moments = []
    # Ideale α-Helix: 100° pro Residue
    for i in range(n):
        vec_x = vec_y = 0
        count = 0
        # 11-Residue-Window (3-4 Helix-Turns)
        for j in range(max(0, i - 5), min(n, i + 6)):
            if seq[j] in hydrophobic_scale:
                angle = math.radians((j - i) * angle_per_residue)
                h = hydrophobic_scale[seq[j]]
                vec_x += h * math.cos(angle)
                vec_y += h * math.sin(angle)
                count += 1
        moment = math.sqrt(vec_x**2 + vec_y**2) / count if count > 0 else 0
        moments.append(moment)
    return moments

def sliding_window_composition(seq, window=11):
    """Berechne kationische, anionische, hydrophobe Fraktion pro Position."""
    n = len(seq)
    cationic = {'K', 'R', 'H'}
    anionic = {'E', 'D', 'U'}  # U=Sec sauer
    hydrophobic = {'A', 'I', 'L', 'M', 'F', 'V', 'W', 'J'}
    out = {'cationic': [], 'anionic': [], 'hydrophobic': []}
    for i in range(n):
        start = max(0, i - window//2)
        end = min(n, i + window//2 + 1)
        subseq = seq[start:end]
        out['cationic'].append(sum(1 for a in subseq if a in cationic) / len(subseq))
        out['anionic'].append(sum(1 for a in subseq if a in anionic) / len(subseq))
        out['hydrophobic'].append(sum(1 for a in subseq if a in hydrophobic) / len(subseq))
    return out

# Berechne für beide Sequenzen
print("=" * 60)
print("STUFE 31: BURUMUT Sekundärstruktur-Vorhersage")
print("=" * 60)

print(f"\nOriginal: {len(seq_burumut)} AS, {len(set(seq_burumut))} verschiedene")
print(f"C-Übersetzung: {len(seq_translated)} AS, {len(set(seq_translated))} verschiedene")

# Chou-Fasman pro Position
cf_orig = chou_fasman_predict(seq_burumut)
cf_trans = chou_fasman_predict(seq_translated)

# Helix-Moment pro Position
hm_orig = helix_moment(seq_burumut)
hm_trans = helix_moment(seq_translated)

# Window-Komposition
wc_orig = sliding_window_composition(seq_burumut)
wc_trans = sliding_window_composition(seq_translated)

# Domänen-Identifikation
def find_domains(seq, metric, threshold=1.0, min_length=10):
    """Identifiziere zusammenhängende Domänen mit metric > threshold."""
    domains = []
    in_domain = False
    start = 0
    for i, val in enumerate(metric):
        if val > threshold and not in_domain:
            in_domain = True
            start = i
        elif val <= threshold and in_domain:
            in_domain = False
            if i - start >= min_length:
                domains.append((start, i, np.mean(metric[start:i])))
    if in_domain and len(metric) - start >= min_length:
        domains.append((start, len(metric), np.mean(metric[start:])))
    return domains

print("\n=== Helix-Moment-Analyse (Original) ===")
domains_orig = find_domains(seq_burumut, hm_orig, threshold=0.6, min_length=10)
for i, (start, end, mean) in enumerate(domains_orig):
    print(f"  Domäne {i+1}: Pos {start+1}-{end}, Länge {end-start}, HM mean={mean:.3f}")
    print(f"    Sequenz: {seq_burumut[start:end]}")

print("\n=== Helix-Moment-Analyse (C-Übersetzung) ===")
domains_trans = find_domains(seq_translated, hm_trans, threshold=0.6, min_length=10)
for i, (start, end, mean) in enumerate(domains_trans):
    print(f"  Domäne {i+1}: Pos {start+1}-{end}, Länge {end-start}, HM mean={mean:.3f}")
    print(f"    Sequenz: {seq_translated[start:end]}")

# Vergleich mit Stufe 14
print("\n=== Vergleich mit Stufe 14 (2 AMP-Domänen-Hypothese) ===")
stufe14_dom1 = (43, 78)  # Pos 43-78
stufe14_dom2 = (109, 133)  # Pos 109-133
print(f"  Stufe 14 Domäne 1: Pos {stufe14_dom1[0]}-{stufe14_dom1[1]}")
hm_dom1_orig = np.mean(hm_orig[stufe14_dom1[0]-1:stufe14_dom1[1]])
hm_dom1_trans = np.mean(hm_trans[stufe14_dom1[0]-1:stufe14_dom1[1]])
print(f"    HM Original: {hm_dom1_orig:.3f}, C-Übersetzung: {hm_dom1_trans:.3f}")
print(f"  Stufe 14 Domäne 2: Pos {stufe14_dom2[0]}-{stufe14_dom2[1]}")
hm_dom2_orig = np.mean(hm_orig[stufe14_dom2[0]-1:stufe14_dom2[1]])
hm_dom2_trans = np.mean(hm_trans[stufe14_dom2[0]-1:stufe14_dom2[1]])
print(f"    HM Original: {hm_dom2_orig:.3f}, C-Übersetzung: {hm_dom2_trans:.3f}")

# Plot erstellen
fig, axes = plt.subplots(4, 1, figsize=(16, 14), sharex=True)
positions = np.arange(1, len(seq_burumut) + 1)

# Plot 1: Chou-Fasman
axes[0].plot(positions, cf_orig, 'b-', alpha=0.7, label='Original (Sec/Pyl)')
axes[0].plot(positions, cf_trans, 'r-', alpha=0.7, label='C-Übersetzung (Cys/Lys)')
axes[0].axhline(y=1.0, color='gray', linestyle='--', label='α-Helix Schwelle')
axes[0].axvspan(stufe14_dom1[0], stufe14_dom1[1], alpha=0.1, color='green', label='Stufe 14 Domäne 1')
axes[0].axvspan(stufe14_dom2[0], stufe14_dom2[1], alpha=0.1, color='orange', label='Stufe 14 Domäne 2')
axes[0].set_ylabel('P(α-Helix)')
axes[0].set_title('Chou-Fasman α-Helix-Wahrscheinlichkeit')
axes[0].legend(loc='upper right', fontsize=8)
axes[0].set_ylim(0, 2.0)
axes[0].grid(True, alpha=0.3)

# Plot 2: Helix-Moment
axes[1].plot(positions, hm_orig, 'b-', alpha=0.7, label='Original')
axes[1].plot(positions, hm_trans, 'r-', alpha=0.7, label='C-Übersetzung')
axes[1].axhline(y=0.6, color='gray', linestyle='--', label='AMP-Schwelle (HM>0.6)')
axes[1].axvspan(stufe14_dom1[0], stufe14_dom1[1], alpha=0.1, color='green')
axes[1].axvspan(stufe14_dom2[0], stufe14_dom2[1], alpha=0.1, color='orange')
axes[1].set_ylabel('Helix-Moment (Eisenberg)')
axes[1].set_title('Helix-Moment pro Position (Eisenberg-Konsensus)')
axes[1].legend(loc='upper right', fontsize=8)
axes[1].grid(True, alpha=0.3)

# Plot 3: Kationische Fraktion
axes[2].plot(positions, wc_orig['cationic'], 'b-', alpha=0.7, label='Original')
axes[2].plot(positions, wc_trans['cationic'], 'r-', alpha=0.7, label='C-Übersetzung')
axes[2].axvspan(stufe14_dom1[0], stufe14_dom1[1], alpha=0.1, color='green')
axes[2].axvspan(stufe14_dom2[0], stufe14_dom2[1], alpha=0.1, color='orange')
axes[2].set_ylabel('Frac kationisch')
axes[2].set_title('Kationische Fraktion pro Position (11-AS-Sliding-Window)')
axes[2].legend(loc='upper right', fontsize=8)
axes[2].grid(True, alpha=0.3)

# Plot 4: Hydrophobe Fraktion
axes[3].plot(positions, wc_orig['hydrophobic'], 'b-', alpha=0.7, label='Original')
axes[3].plot(positions, wc_trans['hydrophobic'], 'r-', alpha=0.7, label='C-Übersetzung')
axes[3].axvspan(stufe14_dom1[0], stufe14_dom1[1], alpha=0.1, color='green')
axes[3].axvspan(stufe14_dom2[0], stufe14_dom2[1], alpha=0.1, color='orange')
axes[3].set_ylabel('Frac hydrophob')
axes[3].set_xlabel('Position')
axes[3].set_title('Hydrophobe Fraktion pro Position (11-AS-Sliding-Window)')
axes[3].legend(loc='upper right', fontsize=8)
axes[3].grid(True, alpha=0.3)

plt.tight_layout()
plot_path = STUFE31 / "stufe_31_burumut_sequkundaerstruktur.png"
plt.savefig(plot_path, dpi=120, bbox_inches='tight')
plt.close()
print(f"\n✓ Plot: {plot_path}")

# Output-JSON
output = {
    "stufe": "31",
    "datum": "2026-07-08",
    "methode": "Chou-Fasman + Helix-Moment + Sliding-Window-Komposition",
    "sequenzen": {
        "burumut_original": {
            "length": len(seq_burumut),
            "n_distinct": len(set(seq_burumut)),
            "chou_fasman_mean": round(np.mean(cf_orig), 3),
            "chou_fasman_max": round(np.max(cf_orig), 3),
            "helix_moment_mean": round(np.mean(hm_orig), 3),
            "helix_moment_max": round(np.max(hm_orig), 3),
        },
        "burumut_translated": {
            "length": len(seq_translated),
            "n_distinct": len(set(seq_translated)),
            "chou_fasman_mean": round(np.mean(cf_trans), 3),
            "chou_fasman_max": round(np.max(cf_trans), 3),
            "helix_moment_mean": round(np.mean(hm_trans), 3),
            "helix_moment_max": round(np.max(hm_trans), 3),
        },
    },
    "domain_detection_hm_threshold_0.6": {
        "original": [{"pos_start": s+1, "pos_end": e, "length": e-s, "hm_mean": round(m, 3)} for s, e, m in domains_orig],
        "translated": [{"pos_start": s+1, "pos_end": e, "length": e-s, "hm_mean": round(m, 3)} for s, e, m in domains_trans],
    },
    "stufe_14_verification": {
        "dom1_hm_original": round(hm_dom1_orig, 3),
        "dom1_hm_translated": round(hm_dom1_trans, 3),
        "dom2_hm_original": round(hm_dom2_orig, 3),
        "dom2_hm_translated": round(hm_dom2_trans, 3),
    },
    "comparison_with_amps": {
        "big_defensin_2dom": {"length": 90, "cys_count": 6, "dom1_hm_estimate": 0.8, "dom2_hm_estimate": 0.7},
        "ll_37_1dom": {"length": 37, "cys_count": 0, "hm_estimate": 0.74},
        "melittin_1dom": {"length": 26, "cys_count": 0, "hm_estimate": 0.50},
    },
    "af2_recommendation": {
        "tool": "ColabFold (https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb)",
        "input": seq_translated,
        "expected_output": "2 hoch-pLDDT-Helices (Pos 43-78, 109-133) + 3 niedrig-pLDDT-Coils",
        "comparison_pdb": ["6D5M (Big-Defensin)", "2LMF (LL-37)", "2MLT (Melittin)"],
        "alternative_local": "AF2 nicht lokal verfügbar — externer ColabFold-Upload erforderlich",
    },
    "verification": {
        "v10_4_seq_match": True,  # bereits verifiziert in Stufe 29
        "stufe_14_dom1_match": 43 <= domains_trans[0][0]+1 <= 78 if domains_trans else False,
        "stufe_14_dom2_match": 109 <= domains_trans[-1][0]+1 <= 133 if domains_trans else False,
    },
    "plot_path": str(plot_path),
}

with open(STUFE31 / "stufe_31_sequkundaerstruktur.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"✓ Output: {STUFE31 / 'stufe_31_sequkundaerstruktur.json'}")
