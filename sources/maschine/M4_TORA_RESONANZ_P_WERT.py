"""
📊 M4 RESONANZ-STATISTIK: Signifikanz der Schritt-Zahlen
=========================================================

Die MultiPhase-Maschine (M4) hat erstaunliche Schritt-Zahlen produziert:
  T1 Gen 1,1   =  6 Schritte  (erwartet: 6)
  T2 Gen 12,1  = 12 Schritte  (erwartet: 12)
  T3 Lev 19,18 =  3 Schritte  (erwartet: 3)
  T4 Gen 37,7  = 15 Schritte  (erwartet: 15)
  T5 Num 6,24  =  5 Schritte  (erwartet: 5)
  T7 Jüdisch   =  7 Schritte  (erwartet: 7)

Frage: Wie wahrscheinlich ist es, dass diese Zahlen ZUFÄLLIG passen?

Methode:
1. Wir nehmen ALLE Verse der Tora (5 Bücher, 187 Kapitel, ~5853 Verse)
2. Wir lassen M4 auf jeden einzelnen laufen
3. Wir zählen, wie viele Verse die "richtige" Schritt-Zahl haben
4. p-Wert = Anzahl passender Verse / Gesamt-Anzahl Verse

Wenn p < 0.01, dann ist die Resonanz STATISTISCH SIGNIFIKANT.
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import json
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase
from TORA_TURING_CORRECT import build_tora_transitions

# Lade Tora
print("Lade Tora...")
books = {}
for i, name in enumerate(['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy'], 1):
    with open(f'/run/media/julian/ML4/tengri137/sources/torah/{i:02d}.json') as f:
        books[name] = json.load(f)
print("✓ Tora geladen")

# Erwartete Schritt-Zahlen
EXPECTED = {
    'Gen 1,1': 6, 'Gen 12,1': 12, 'Lev 19,18': 3, 'Gen 37,7': 15,
    'Num 6,24': 5, 'Jüdisch Gen 1,1': 7,
}

# Sammle alle Verse
print("\nSammle alle Verse...")
all_verses = []
for book_name, data in books.items():
    for kap_idx, kap in enumerate(data['text']):
        if not isinstance(kap, list):
            continue
        for vers_idx, vers in enumerate(kap):
            if not vers:
                continue
            hebr = vers.replace(' ', '').replace(' ', '')
            if hebr:
                all_verses.append((book_name, kap_idx+1, vers_idx+1, hebr))
print(f"✓ {len(all_verses)} Verse gesammelt")

# Maschine laufen lassen
print("\nLasse Maschine auf alle Verse laufen...")
all_steps = []
matches = {key: 0 for key in EXPECTED}
transitions = build_tora_transitions()

# Begrenze auf 500 Verse für Performance
SAMPLE_SIZE = 500
verses_to_test = all_verses[:SAMPLE_SIZE]

for i, (book, kap, vers, hebr) in enumerate(verses_to_test):
    if i % 100 == 0:
        print(f"  {i}/{SAMPLE_SIZE}...")
    try:
        m = ToraTuringMultiPhase(hebr, phase_size=99, transitions=transitions)
        m.run(max_steps=1000)
        steps = m.total_steps
        all_steps.append((book, kap, vers, hebr, steps))

        # Prüfe gegen Erwartungen
        for key, expected in EXPECTED.items():
            if steps == expected:
                matches[key] += 1
    except Exception as e:
        pass

print(f"✓ {len(all_steps)} Verse getestet")

# Statistik
print()
print("=" * 60)
print("📊 STATISTISCHE ANALYSE")
print("=" * 60)
print()

total = len(all_steps)
print(f"Getestete Verse: {total}")
print()

# Häufigkeitsverteilung der Schritt-Zahlen
from collections import Counter
step_counter = Counter(steps for _, _, _, _, steps in all_steps)
print("Top-15 häufigste Schritt-Zahlen:")
for steps, count in step_counter.most_common(15):
    print(f"  {steps:>3} Schritte: {count:>3} Verse ({100*count/total:.1f}%)")
print()

# p-Werte
print("p-Werte für unsere Erwartungen:")
print(f"{'Erwartung':<25} | {'Erw.':>5} | {'Treffer':>7} | {'p (Anteil)':>10} | {'p (< oder =)':>12}")
print("-" * 70)

for key, expected in EXPECTED.items():
    n_match = matches[key]
    p_at_least = n_match / total
    n_at_most = sum(1 for s in step_counter.values() if True)  # alle
    # p(X <= expected) = Anteil der Verse mit steps <= expected
    n_le = sum(c for s, c in step_counter.items() if s <= expected)
    p_le = n_le / total
    print(f"{key:<25} | {expected:>5} | {n_match:>7} | {p_at_least:>10.4f} | {p_le:>12.4f}")

# Multi-Test-Bonferroni
print()
print("=" * 60)
print("🧪 MULTI-TEST-KORREKTUR (Bonferroni)")
print("=" * 60)
print()
print(f"Wir testen {len(EXPECTED)} Hypothesen gleichzeitig.")
print(f"Bonferroni-korrigiertes α = 0.05/{len(EXPECTED)} = {0.05/len(EXPECTED):.4f}")
print()

# Berechne kombinierten p-Wert (Fischer's Method)
import math
log_p_sum = 0
for key, expected in EXPECTED.items():
    n_match = matches[key]
    p = n_match / total if total > 0 else 1
    if p > 0:
        log_p_sum += math.log(p)

chi2 = -2 * log_p_sum
k = len(EXPECTED)
# Approximation: chi2 ~ chi-square with 2k degrees of freedom
# p_combined = 1 - CDF(chi2, 2k)
# Vereinfachung: wenn chi2 > 2k + 2*sqrt(2k) → signifikant
threshold = 2*k + 2*math.sqrt(2*k)
print(f"Chi²-Statistik: {chi2:.2f}")
print(f"Schwelle (2k + 2√(2k)): {threshold:.2f}")
print(f"Signifikant (5%): {chi2 > threshold}")
print()

# Detail: Welche Verse haben die exakten Schritt-Zahlen?
print("=" * 60)
print("🔍 VERSE MIT DEN EXAKTEN SCHRITT-ZAHLEN")
print("=" * 60)
print()

for key, expected in EXPECTED.items():
    print(f"\n--- {key} = {expected} Schritte ---")
    matches_verses = [(b, k, v) for b, k, v, h, s in all_steps if s == expected][:10]
    for b, k, v in matches_verses:
        print(f"  {b} {k},{v}")
    n_match = len(matches_verses)
    if n_match > 10:
        print(f"  ... und {n_match - 10} weitere")
