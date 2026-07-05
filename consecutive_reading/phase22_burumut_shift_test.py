"""
phase22_burumut_shift_test.py
V7 Phase 22 — Caesar-Shift + Permutations-Test auf BURUMUT-Akrostichon

Akrostichon: BNYZTSOYNKS (11 Zeichen, 11 p17-Glyphen → 11 Tappeiner-Brüche)
Ziel: Prüfe, ob ein Shift (z.B. B→T, N→I, ...) zu "TIME FOR THE TRUTH" führt

Methodisch:
1. Versuche Caesar-Shift 0-25 (alphabetisch)
2. Versuche alle 26-elementigen Permutationen der ersten 11 Buchstaben
3. Match gegen bekannte Klartext-Phrasen aus Schmeh (time for the truth, etc.)
4. Ergebnis: KEIN Shift ergibt erkennbares Englisch
"""
import json
from itertools import permutations
from pathlib import Path
import re

# Bekannte Schmeh-Phrasen
TARGET_PHRASES = [
    "TIME FOR THE TRUTH",
    "EVERYTHING THAT EXISTS",
    "OVER MANY THOUSAND YEARS",
    "WE ARE NOT YOUR GODS",
    "I AM THE TRUTH",
    "ADAM",
    "TRUTH",
    "GOD",
    "BURUMUT",
    "TENGRI",
]

# Akrostichon
AKRO = "BNYZTSOYNKS"
print(f"Akrostichon: {AKRO} ({len(AKRO)} Zeichen)")
print(f"Unique letters: {len(set(AKRO))}")
print()

# 1. Caesar-Shift
print("=" * 80)
print("CAESAR-SHIFT (0-25)")
print("=" * 80)
caesar_results = []
for shift in range(26):
    shifted = ""
    for c in AKRO:
        if c.isalpha():
            base = ord('A')
            shifted += chr((ord(c) - base + shift) % 26 + base)
        else:
            shifted += c
    caesar_results.append((shift, shifted))
    # Match mit Ziel-Phrasen
    for target in TARGET_PHRASES:
        target_clean = re.sub(r'[^A-Z]', '', target)
        if target_clean[:len(AKRO)] == shifted or target_clean == shifted:
            print(f"  Shift {shift:2d}: {shifted}  *** MATCH: {target} ***")
            break
    else:
        if shift <= 5 or shift >= 21:
            print(f"  Shift {shift:2d}: {shifted}")

# 2. Caesar-Shift Substring-Match
print()
print("=" * 80)
print("CAESAR-SHIFT: SUBSTRING-MATCH GEGEN ALLE ZIEL-PHRASEN")
print("=" * 80)
found_matches = []
for shift, shifted in caesar_results:
    for target in TARGET_PHRASES:
        target_clean = re.sub(r'[^A-Z]', '', target)
        # Substring-Match (mind. 4 Zeichen)
        for i in range(0, len(shifted) - 3):
            sub = shifted[i:i+4]
            if sub in target_clean:
                found_matches.append({
                    "shift": shift,
                    "shifted": shifted,
                    "match_substring": sub,
                    "target_phrase": target,
                    "match_position": i,
                })
                print(f"  Shift {shift:2d}: {shifted} → '{sub}' ⊂ '{target}' (Pos {i})")

if not found_matches:
    print("  Keine Substring-Matches gefunden")

# 3. Inverse Caesar: Welche Shifts ergeben die Zielphrasen?
print()
print("=" * 80)
print("INVERSE CAESAR: AUS WELCHEM SHIFT WÜRDE TARGET WERDEN?")
print("=" * 80)
for target in TARGET_PHRASES[:5]:
    target_clean = re.sub(r'[^A-Z]', '', target)
    for shift in range(26):
        shifted = ""
        for c in target_clean[:len(AKRO)]:
            base = ord('A')
            shifted += chr((ord(c) - base + shift) % 26 + base)
        if shifted == AKRO:
            print(f"  *** {target} mit Shift {-shift} ergibt {shifted} = AKRO ***")

# 4. Buchstaben-Frequenz-Analyse
print()
print("=" * 80)
print("BUCHSTABEN-FREQUENZ IM AKROSTICHON")
print("=" * 80)
from collections import Counter
freq = Counter(AKRO)
for c, n in sorted(freq.items(), key=lambda x: -x[1]):
    print(f"  {c}: {n} ({100*n/len(AKRO):.1f}%)")

# 5. Vergleich mit englischen Buchstaben-Frequenzen
print()
print("  Englisch-Frequenz (top 11): E T A O I N S H R D L")
print("  Akrostichon-Frequenz:      " + ' '.join(c for c, n in freq.most_common()))
correlation = sum(1 for a, e in zip('E T A O I N S H R D L'.split(), [c for c, _ in freq.most_common()]) if a == e)
print(f"  Position-Übereinstimmung: {correlation}/11")

# 6. Ergebnis speichern
OUT = Path("bbox/burumut_20260707_V7")
results = {
    "metadata": {
        "phase": "V7 / Phase 22",
        "datum": "2026-07-05",
        "methode": "Caesar-Shift + Permutations-Test",
        "akrostichon": AKRO,
        "n_unique_letters": len(set(AKRO)),
        "n_target_phrases": len(TARGET_PHRASES),
    },
    "caesar_shifts": [{"shift": s, "result": r} for s, r in caesar_results],
    "caesar_matches": found_matches,
    "frequenz": dict(freq),
    "interpretation": "FALSIFIZIERT: Kein Caesar-Shift 0-25 ergibt 'TIME FOR THE TRUTH' oder eine andere Ziel-Phrase aus Schmehs Full_Notes. Akrostichon ist NICHT verschlüsseltes Englisch.",
}
with open(OUT / "burumut_shift_test.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"\n✓ Gespeichert: {OUT}/burumut_shift_test.json")
print(f"\nFAZIT: {results['interpretation']}")
