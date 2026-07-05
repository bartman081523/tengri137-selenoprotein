"""
phase20_burumut_baseline.py
V7 Phase 20 — Periodensystem-Baseline-Kalibrierung

Frage: Hat der Tengri-Autor die Primzahlen so konstruiert, dass die BURUMUT-Wörter
phonetisch lesbar werden? Oder ist alles Periodensystem-Rauschen?

Methode:
1. 10.000 zufällige Dinome (01-118) generieren
2. Auf Element-Anfangsbuchstaben mappen
3. IC, Konsonanten-Ratio, Buchstabenverteilung der chemischen Baseline berechnen
4. Mit BURUMUT-Verteilung vergleichen
5. Anomalie = signifikante Abweichung von der Baseline
"""
import json
import random
from collections import Counter
from pathlib import Path
import math

OUT = Path("bbox/burumut_20260707_V7")

PERIODIC = {1:'H', 2:'He', 3:'Li', 4:'Be', 5:'B', 6:'C', 7:'N', 8:'O', 9:'F', 10:'Ne',
    11:'Na', 12:'Mg', 13:'Al', 14:'Si', 15:'P', 16:'S', 17:'Cl', 18:'Ar', 19:'K', 20:'Ca',
    21:'Sc', 22:'Ti', 23:'V', 24:'Cr', 25:'Mn', 26:'Fe', 27:'Co', 28:'Ni', 29:'Cu', 30:'Zn',
    31:'Ga', 32:'Ge', 33:'As', 34:'Se', 35:'Br', 36:'Kr', 37:'Rb', 38:'Sr', 39:'Y', 40:'Zr',
    41:'Nb', 42:'Mo', 43:'Tc', 44:'Ru', 45:'Rh', 46:'Pd', 47:'Ag', 48:'Cd', 49:'In', 50:'Sn',
    51:'Sb', 52:'Te', 53:'I', 54:'Xe', 55:'Cs', 56:'Ba', 57:'La', 58:'Ce', 59:'Pr', 60:'Nd',
    61:'Pm', 62:'Sm', 63:'Eu', 64:'Gd', 65:'Tb', 66:'Dy', 67:'Ho', 68:'Er', 69:'Tm', 70:'Yb',
    71:'Lu', 72:'Hf', 73:'Ta', 74:'W', 75:'Re', 76:'Os', 77:'Ir', 78:'Pt', 79:'Au', 80:'Hg',
    81:'Tl', 82:'Pb', 83:'Bi', 84:'Po', 85:'At', 86:'Rn', 87:'Fr', 88:'Ra', 89:'Ac', 90:'Th',
    91:'Pa', 92:'U', 93:'Np', 94:'Pu', 95:'Am', 96:'Cm', 97:'Bk', 98:'Cf', 99:'Es', 100:'Fm',
    101:'Md', 102:'No', 103:'Lr', 104:'Rf', 105:'Db', 106:'Sg', 107:'Bh', 108:'Hs', 109:'Mt', 110:'Ds',
    111:'Rg', 112:'Cn', 113:'Nh', 114:'Fl', 115:'Mc', 116:'Lv', 117:'Ts', 118:'Og'}

# Erste Buchstaben-Extraktion
ELEMENT_INITIALS = {}
for n, sym in PERIODIC.items():
    ELEMENT_INITIALS[n] = sym[0].upper()

vowels = set("AEIOU")

# BURUMUT-Texts
with open(OUT / "burumut_texts.json") as f:
    data = json.load(f)
burumut_texts = []
for bnr, texts in data["burumut_texts"].items():
    for t in texts:
        burumut_texts.append(t)

# BURUMUT Buchstaben (nur gültige, ohne '?')
burumut_chars = ''.join(c for c in ''.join(burumut_texts) if c != '?')
burumut_chars_clean = ''.join(c for c in burumut_chars if c.isalpha())

# BURUMUT-Wort (14 Zeichen pro Phrase)
burumut_phrases = [t for t in burumut_texts if '?' not in t]
print(f"BURUMUT: {len(burumut_phrases)} Phrasen, {len(burumut_chars_clean)} Zeichen")

# =================================================================
# PERIODENSYSTEM-BASELINE
# =================================================================
print("=" * 80)
print("PERIODENSYSTEM-BASELINE: 10.000 zufällige Dinome")
print("=" * 80)

# Generiere 100.000 Zeichen (≈ 7000 BURUMUT-Wörter)
# Wir wollen genug Samples für stabile Statistik
N_SAMPLES = 100000
random.seed(42)  # Reproduzierbarkeit

baseline_atoms = [random.randint(1, 118) for _ in range(N_SAMPLES)]
baseline_chars = ''.join(ELEMENT_INITIALS[a] for a in baseline_atoms)

# Baseline: BURUMUT-Struktur simulieren (14 Zeichen pro Phrase)
baseline_phrases = []
for i in range(0, len(baseline_chars) - 13, 14):
    baseline_phrases.append(baseline_chars[i:i+14])

print(f"Baseline: {len(baseline_phrases)} Phrasen à 14 Zeichen = {len(baseline_chars)} Zeichen")

# =================================================================
# STATISTIK-VERGLEICH
# =================================================================
print()
print("=" * 80)
print("VERGLEICH BURUMUT vs PERIODENSYSTEM-BASELINE")
print("=" * 80)

def calc_stats(text, label):
    """Berechne IC, Entropie, Konsonanten-Verhältnis"""
    total = len(text)
    freq = Counter(text)
    # IC
    ic = sum(n * (n - 1) for n in freq.values()) / (total * (total - 1)) if total > 1 else 0
    # Entropie
    prob = {c: n/total for c, n in freq.items()}
    entropy = -sum(p * math.log2(p) for p in prob.values())
    # Konsonanten
    consonants = sum(n for c, n in freq.items() if c not in vowels)
    vowel_count = sum(n for c, n in freq.items() if c in vowels)
    ratio = consonants / vowel_count if vowel_count else float('inf')
    # Rein konsonantische "Wörter" simulieren
    return {
        "label": label,
        "n_chars": total,
        "n_unique": len(freq),
        "ic": round(ic, 4),
        "entropy": round(entropy, 3),
        "consonants": consonants,
        "vowels": vowel_count,
        "ratio": round(ratio, 2),
    }

# Berechne für BURUMUT
burumut_phrase_text = ''.join(burumut_phrases)
burumut_stats = calc_stats(burumut_phrase_text, "BURUMUT")

# Berechne für Baseline
baseline_phrase_text = ''.join(baseline_phrases)
baseline_stats = calc_stats(baseline_phrase_text, "Baseline (10k Dinome)")

print(f"\n{'Metrik':<35} {'BURUMUT':>12} {'Baseline':>12} {'Delta':>10}")
print("-" * 75)
for key in ["n_chars", "n_unique", "ic", "entropy", "consonants", "vowels", "ratio"]:
    b_val = burumut_stats[key]
    bl_val = baseline_stats[key]
    delta = b_val - bl_val
    print(f"{key:<35} {b_val:>12} {bl_val:>12} {delta:>+10.4f}")

# =================================================================
# BUCHSTABEN-VERTEILUNGS-VERGLEICH
# =================================================================
print()
print("=" * 80)
print("BUCHSTABEN-VERTEILUNG: BURUMUT vs BASELINE")
print("=" * 80)

# Wahrscheinlichkeiten berechnen
burumut_freq = Counter(burumut_phrase_text)
bl_freq = Counter(baseline_phrase_text)
all_letters = sorted(set(burumut_freq) | set(bl_freq))

print(f"\n{'Buchstabe':<12} {'BURUMUT %':>12} {'Baseline %':>12} {'Ratio B/Bl':>12} {'Anomalie':>12}")
print("-" * 60)
anomalies = []
for c in all_letters:
    b_pct = 100 * burumut_freq.get(c, 0) / len(burumut_phrase_text)
    bl_pct = 100 * bl_freq.get(c, 0) / len(baseline_phrase_text)
    if bl_pct == 0:
        ratio_str = "∞"
        anomaly = "BASELINE=0"
    else:
        ratio = b_pct / bl_pct
        ratio_str = f"{ratio:.2f}x"
        if ratio > 2.0 or ratio < 0.5:
            anomaly = "** ANOMAL **"
            anomalies.append((c, ratio, b_pct, bl_pct))
        else:
            anomaly = ""
    print(f"  {c:<10} {b_pct:>11.2f}% {bl_pct:>11.2f}% {ratio_str:>12} {anomaly:>12}")

print()
print(f"Anomalien (Ratio > 2.0 oder < 0.5): {len(anomalies)}")
for c, r, b, bl in anomalies:
    print(f"  {c}: {r:.2f}x (BUR: {b:.2f}%, Baseline: {bl:.2f}%)")

# =================================================================
# ENGSTE TESTS: 'BURUMUT'-BUCHSTABEN
# =================================================================
print()
print("=" * 80)
print("FOKUSSIERTER TEST: 'BURUMUT'-BUCHSTABEN")
print("=" * 80)

# Welche Buchstaben braucht 'BURUMUT'?
# B-U-R-U-M-U-T
burumut_chars_needed = set("BURUMUT")

print(f"\nBuchstaben in 'BURUMUT': {sorted(burumut_chars_needed)}")
print()
print(f"{'Buchstabe':<12} {'BURUMUT %':>12} {'Baseline %':>12} {'Ratio B/Bl':>12}")
print("-" * 50)
for c in sorted(burumut_chars_needed):
    b_pct = 100 * burumut_freq.get(c, 0) / len(burumut_phrase_text)
    bl_pct = 100 * bl_freq.get(c, 0) / len(baseline_phrase_text)
    ratio = b_pct / bl_pct if bl_pct > 0 else float('inf')
    print(f"  {c:<10} {b_pct:>11.2f}% {bl_pct:>11.2f}% {ratio:>11.2f}x")

# =================================================================
# CHI-QUADRAT-TEST
# =================================================================
print()
print("=" * 80)
print("CHI-QUADRAT-ANPASSUNGSTEST")
print("=" * 80)
# H0: BURUMUT-Verteilung = Baseline-Verteilung
# Wenn p < 0.05: Verteilungen sind signifikant verschieden (= Engineering!)

# Erwartete Häufigkeiten basierend auf Baseline
expected = {c: bl_freq.get(c, 0) / len(baseline_phrase_text) * len(burumut_phrase_text)
            for c in all_letters}

chi_sq = 0
for c in all_letters:
    obs = burumut_freq.get(c, 0)
    exp = expected[c]
    if exp > 0:
        chi_sq += (obs - exp) ** 2 / exp

# Freiheitsgrade: n_unique - 1
df = len(all_letters) - 1

# Approximation der Chi-Quadrat-Verteilung
# p-Wert: wenn chi_sq > df, dann signifikant
print(f"\nChi-Quadrat: {chi_sq:.2f}")
print(f"Freiheitsgrade: {df}")
print(f"Chi²/df (sollte ≈ 1 sein für gleiche Verteilung): {chi_sq/df:.2f}")
print()
if chi_sq / df > 2.0:
    print("→ VERTEILUNGEN SIND SIGNIFIKANT VERSCHIEDEN")
    print("→ ENGINEERING-THESE BESTÄTIGT")
elif chi_sq / df > 1.5:
    print("→ Verteilungen sind etwas verschieden (schwaches Signal)")
else:
    print("→ Verteilungen sind ähnlich (RAUSCHEN-THESE wahrscheinlich)")

# =================================================================
# REIN KONSONANTISCHE WÖRTER
# =================================================================
print()
print("=" * 80)
print("REIN KONSONANTISCHE 'WÖRTER' (14 Zeichen, keine Vokale)")
print("=" * 80)

burumut_consonantal = [p for p in burumut_phrases if not any(c in vowels for c in p)]
baseline_consonantal = [p for p in baseline_phrases if not any(c in vowels for c in p)]

b_pct = 100 * len(burumut_consonantal) / len(burumut_phrases)
bl_pct = 100 * len(baseline_consonantal) / len(baseline_phrases)
print(f"\nBURUMUT: {len(burumut_consonantal)}/{len(burumut_phrases)} = {b_pct:.2f}%")
print(f"Baseline: {len(baseline_consonantal)}/{len(baseline_phrases)} = {bl_pct:.2f}%")
print(f"Ratio: {b_pct/bl_pct if bl_pct > 0 else 'inf':.2f}x")

# Erwartet für Zufall:
import math
expected_vowel = sum(1 for c in ELEMENT_INITIALS.values() if c in vowels) / 118
prob_no_vowel = (1 - expected_vowel) ** 14
print(f"\nErwartet (theoretisch für Zufall): {100*prob_no_vowel:.2f}%")

# =================================================================
# PHRASEN-DIVERSITÄT
# =================================================================
print()
print("=" * 80)
print("PHRASEN-DIVERSITÄT (Unique/Total)")
print("=" * 80)

b_unique = len(set(burumut_phrases))
bl_unique = len(set(baseline_phrases))
print(f"\nBURUMUT: {b_unique}/{len(burumut_phrases)} = {100*b_unique/len(burumut_phrases):.2f}%")
print(f"Baseline: {bl_unique}/{len(baseline_phrases)} = {100*bl_unique/len(baseline_phrases):.2f}%")

# BURUMUT hat 100% Unique (jede Phrase ist anders)
# Baseline bei 7142 Phrasen: 5-Alphabet-Buchstaben × 14 Stellen = 25^14 = enorm
# Wenn beide ~100% sind, kein aussagekräftiger Unterschied

# =================================================================
# SPEICHERN
# =================================================================
results = {
    "metadata": {
        "phase": "V7 / Phase 20",
        "datum": "2026-07-04",
        "frage": "Engineering vs Rauschen",
        "methode": "Periodensystem-Baseline-Kalibrierung",
        "n_baseline": N_SAMPLES,
    },
    "burumut_stats": burumut_stats,
    "baseline_stats": baseline_stats,
    "anomalien": [{"buchstabe": c, "ratio": round(r, 2), "burumut_pct": round(b, 2), "baseline_pct": round(bl, 2)} for c, r, b, bl in anomalies],
    "chi_quadrat": {
        "chi_sq": round(chi_sq, 2),
        "df": df,
        "chi_sq_per_df": round(chi_sq/df, 2),
    },
    "rein_konsonantische_woerter": {
        "burumut_pct": round(b_pct, 2),
        "baseline_pct": round(bl_pct, 2),
        "ratio": round(b_pct/bl_pct, 2) if bl_pct > 0 else None,
    },
    "interpretation": "TBD",
}

# Interpretation
if chi_sq / df > 2.0:
    results["interpretation"] = "ENGINEERING: BURUMUT-Verteilung signifikant verschieden von Periodensystem-Rauschen. Der Autor hat Primzahlen gezielt konstruiert."
elif chi_sq / df > 1.5:
    results["interpretation"] = "SCHWACHES SIGNAL: Mögliche leichte Engineering-Indizien, aber nicht statistisch signifikant."
else:
    results["interpretation"] = "RAUSCHEN: BURUMUT ist konsistent mit Periodensystem-Zufallsverteilung. Kein Cherry-Picking nachweisbar."

with open(OUT / "burumut_baseline_comparison.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"\n✓ Gespeichert: {OUT}/burumut_baseline_comparison.json")
