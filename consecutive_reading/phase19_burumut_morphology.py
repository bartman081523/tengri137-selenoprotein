"""
phase19_burumut_morphology.py
V7 Phase 19 — BURUMUT-Morphologie-Sonde

Harte linguistische Tests:
1. Vokalharmonie-Test (altaisch: e,i/i vs. a,o,u mischen sich nicht)
2. N-Gramm-Agglutination (Suffix-Häufigkeit)
3. Entropie / Isogramm-Check
"""
import json
from collections import Counter
from pathlib import Path
import math

OUT = Path("bbox/burumut_20260707_V7")
OUT.mkdir(parents=True, exist_ok=True)

# Alle 76 BURUMUT-Texte
with open(OUT / "burumut_texts.json") as f:
    data = json.load(f)

# Sammle alle BURUMUT-Buchstaben
all_texts = []
for bnr, texts in data["burumut_texts"].items():
    for t in texts:
        all_texts.append(t)

all_chars = ''.join(all_texts).upper()
print("=" * 80)
print("BURUMUT-MORPHOLOGIE-SONDE")
print("=" * 80)
print(f"\nGesamtzahl BURUMUT-Phrasen: {len(all_texts)}")
print(f"Gesamtzahl Zeichen: {len(all_chars)}")
print(f"Unique Zeichen: {len(set(all_chars))}")
print(f"Buchstaben-Frequenz (Top 20):")
freq = Counter(all_chars)
for c, n in freq.most_common(20):
    print(f"  {c}: {n} ({100*n/len(all_chars):.1f}%)")

# =================================================================
# TEST 1: Vokalharmonie
# =================================================================
print()
print("=" * 80)
print("TEST 1: VOKALHARMONIE (Altaisch-typisch)")
print("=" * 80)

# Türkisch/Mongolisch hat:
# - Helle Vokale: E, I, Ö, Ü
# - Dunkle Vokale: A, O, U
# In einem Wort sollten nur helle ODER nur dunkle vorkommen
# (mit Ausnahmen wie /ɯ/)

vowels = set("AEIOU")
bright = set("EI")  # vereinfacht (ohne Ö/Ü)
dark = set("AOU")

def classify_vowel(c):
    if c in bright: return "hell"
    if c in dark: return "dunkel"
    return None

# Analysiere pro BURUMUT-Wort
violations = 0
total_words_with_vowels = 0
mixed_examples = []

for word in all_texts:
    word_vowels = [c for c in word if c in vowels]
    if not word_vowels:
        continue
    total_words_with_vowels += 1
    bright_count = sum(1 for v in word_vowels if v in bright)
    dark_count = sum(1 for v in word_vowels if v in dark)
    if bright_count > 0 and dark_count > 0:
        violations += 1
        if len(mixed_examples) < 15:
            mixed_examples.append((word, word_vowels, bright_count, dark_count))

print(f"\nWörter mit Vokalen: {total_words_with_vowels}")
print(f"Wörter mit Vokal-MIX (hell + dunkel): {violations}")
print(f"Vokalharmonie-Verletzungsrate: {100*violations/total_words_with_vowels:.1f}%")
print(f"\nVergleich:")
print(f"  Reines Türkisch: ~0-5% Verletzungen (strenge Harmonie)")
print(f"  BURUMUT: {100*violations/total_words_with_vowels:.1f}%")
print()
print("Beispiele gemischter Wörter:")
for word, vw, b, d in mixed_examples:
    print(f"  {word:20s} → Vokale {vw} (hell={b}, dunkel={d})")

# =================================================================
# TEST 2: N-Gramm-Agglutination
# =================================================================
print()
print("=" * 80)
print("TEST 2: N-GRAMM-AGGLUTINATION")
print("=" * 80)

# Agglutinierende Sprachen haben häufige Suffixe
# Suche nach 2-3-Buchstaben-Suffixen (Wortende)

def ngrams(text, n):
    return [text[i:i+n] for i in range(len(text) - n + 1)]

# Sammle Suffixe (2, 3, 4) am Wortende
suffixes_2 = Counter()
suffixes_3 = Counter()
suffixes_4 = Counter()

for word in all_texts:
    if len(word) >= 2:
        suffixes_2[word[-2:]] += 1
    if len(word) >= 3:
        suffixes_3[word[-3:]] += 1
    if len(word) >= 4:
        suffixes_4[word[-4:]] += 1

print("\nTop 20 Wort-Suffixe (2 Zeichen):")
for s, c in suffixes_2.most_common(20):
    print(f"  -{s}: {c}x")

print("\nTop 20 Wort-Suffixe (3 Zeichen):")
for s, c in suffixes_3.most_common(20):
    print(f"  -{s}: {c}x")

print("\nTop 15 Wort-Suffixe (4 Zeichen):")
for s, c in suffixes_4.most_common(15):
    print(f"  -{s}: {c}x")

# Was wenn wir die Wörter nach gemeinsamen Suffix gruppieren?
print("\n" + "=" * 80)
print("WORT-GRUPPIERUNG nach gemeinsamen 4-Zeichen-Suffixen")
print("=" * 80)
groups_4 = {}
for s, c in suffixes_4.most_common(30):
    group = [w for w in all_texts if w.endswith(s)]
    if len(group) >= 2:
        groups_4[s] = group

for s, group in sorted(groups_4.items(), key=lambda x: -len(x[1]))[:15]:
    print(f"\nSuffix '-{s}' ({len(group)} Wörter):")
    for w in group:
        print(f"  {w}")

# =================================================================
# TEST 3: Entropie / Information
# =================================================================
print()
print("=" * 80)
print("TEST 3: ENTROPIE / ISOGRAMM-CHECK")
print("=" * 80)

# Buchstaben-Entropie (Shannon)
total = len(all_chars)
char_freq = Counter(all_chars)
char_prob = {c: n/total for c, n in char_freq.items()}

entropy = -sum(p * math.log2(p) for p in char_prob.values())
print(f"\nBuchstaben-Entropie (Shannon): {entropy:.3f} bits/Zeichen")
print(f"Vergleichswerte:")
print(f"  Englisch: ~4.0-4.5 bits/Zeichen")
print(f"  Deutsch: ~4.0-4.3 bits/Zeichen")
print(f"  Türkisch: ~4.2-4.5 bits/Zeichen")
print(f"  Zufällig (26 Buchstaben): ~4.7 bits/Zeichen")
print(f"  BURUMUT (25 unique Buchstaben): {entropy:.3f} bits")

# Bigramm-Entropie
bigrams = Counter()
for word in all_texts:
    bigrams.update(ngrams(word, 2))

bigram_total = sum(bigrams.values())
bigram_prob = {b: n/bigram_total for b, n in bigrams.items()}
bigram_entropy = -sum(p * math.log2(p) for p in bigram_prob.values())
print(f"\nBigramm-Entropie: {bigram_entropy:.3f} bits/Bigramm")
print(f"  (1. Normalisierte Bigramm-Entropie = bigram_entropy / 2)")

# Wortlängen-Verteilung
print("\nWortlängen-Verteilung:")
lengths = Counter(len(w) for w in all_texts)
for l, c in sorted(lengths.items()):
    print(f"  {l} Zeichen: {c} Wörter ({100*c/len(all_texts):.1f}%)")

# Index of Coincidence (IC)
print("\n" + "=" * 80)
print("TEST 4: INDEX OF COINCIDENCE (IC)")
print("=" * 80)
# IC = Summe n_i*(n_i-1) / (N*(N-1))
# Niedriges IC ≈ Sprache mit vielen Buchstaben
# Hohes IC ≈ Sprache mit wenigen Buchstaben oder Poly-Alphabet
# Englisch: 0.067, Deutsch: 0.076, Türkisch: ~0.06-0.08, Zufallig: 0.038

# Berechne IC für die Gesamtheit
N = len(all_chars)
ic_numerator = sum(n * (n - 1) for n in char_freq.values())
ic = ic_numerator / (N * (N - 1))
print(f"\nIC (gesamt): {ic:.4f}")
print(f"  Englisch: ~0.067")
print(f"  Deutsch: ~0.076")
print(f"  Türkisch: ~0.063")
print(f"  Zufällig (25 Zeichen): {1/25:.4f}")

# IC pro BURUMUT-Wort (gepoolt)
# Berechne IC nur für BURUMUT-Wörter der Länge >= 8
ic_pool = 0
ic_count = 0
for word in all_texts:
    if len(word) < 8:
        continue
    word_freq = Counter(word)
    n = len(word)
    if n < 2:
        continue
    word_ic = sum(c * (c - 1) for c in word_freq.values()) / (n * (n - 1))
    ic_pool += word_ic
    ic_count += 1
ic_avg = ic_pool / ic_count if ic_count > 0 else 0
print(f"IC (gepoolt über Wörter ≥ 8 Zeichen): {ic_avg:.4f}")

# =================================================================
# TEST 5: WORT-INNENSTRUKTUR
# =================================================================
print()
print("=" * 80)
print("TEST 5: WORT-INNENSTRUKTUR")
print("=" * 80)

# Ist BURUMUT konsonantisch? (Wie Semitisch?)
# Bestimme ob Wörter "Gerippe" haben (Konsonanten ohne Vokale)
def is_consonantal_skeleton(word, vowels=set("AEIOU")):
    return all(c not in vowels for c in word)

consonantal = sum(1 for w in all_texts if is_consonantal_skeleton(w))
print(f"\nRein konsonantische Wörter: {consonantal}/{len(all_texts)} ({100*consonantal/len(all_texts):.1f}%)")

# Verteilung der Vokale pro Wort
vowel_counts = []
for w in all_texts:
    v = sum(1 for c in w if c in vowels)
    vowel_counts.append(v)
vowel_dist = Counter(vowel_counts)
print(f"\nVokal-Anzahl pro Wort:")
for n, c in sorted(vowel_dist.items()):
    print(f"  {n} Vokale: {c} Wörter")

# Ist das Verhältnis Konsonanten:Vokale ähnlich einer natürlichen Sprache?
consonants = sum(1 for c in all_chars if c not in vowels)
vowel_total = sum(1 for c in all_chars if c in vowels)
ratio = consonants / vowel_total if vowel_total else 0
print(f"\nKonsonanten:Vokale = {consonants}:{vowel_total} = {ratio:.2f}:1")
print(f"Vergleich:")
print(f"  Englisch: ~2.5:1")
print(f"  Türkisch: ~1.4:1 (agglutinierend, viele Vokale in Suffixen)")
print(f"  Arabisch: ~3.5:1 (konsonantisch)")
print(f"  BURUMUT: {ratio:.2f}:1")

# =================================================================
# Zusammenfassung
# =================================================================
print()
print("=" * 80)
print("ZUSAMMENFASSUNG")
print("=" * 80)
summary = {
    "vokalharmonie_verletzungen_pct": round(100*violations/total_words_with_vowels, 1),
    "buchstaben_entropie": round(entropy, 3),
    "bigramm_entropie": round(bigram_entropy, 3),
    "ic_gesamt": round(ic, 4),
    "ic_pool": round(ic_avg, 4),
    "konsonantische_woerter": consonantal,
    "konsonanten_vokale_ratio": round(ratio, 2),
    "top_suffixe_3": [s for s, c in suffixes_3.most_common(10)],
    "top_suffixe_count_3": dict(suffixes_3.most_common(10)),
}
print(json.dumps(summary, indent=2, ensure_ascii=False))

with open(OUT / "burumut_morphology.json", "w") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
print(f"\n✓ Gespeichert: {OUT}/burumut_morphology.json")
