"""
v13_test_generative.py
V13 PHASE 3 — GENERATIVE-TEST (TDD)

Hypothese: Es gibt eine Funktion F: p17-23 → p1-p16, die die Glyphen-Sequenz
approximativ erzeugt. Verschiedene Mapping-Funktionen testen.

Run: python3 v13_test_generative.py
"""
import json
import sys
from pathlib import Path


def load_data():
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_inv = json.load(open("bbox/v11_p1_p16_20260706/glyph_word_inventory.json"))
    return p17, p23, p1_16_inv


def test_digit_to_glyph_mapping_predicts():
    """Ziffer-Index in p17 → Glyph-Index in p1-16?

    p17 hat 10 Ziffern, p1-16 hat 15 Glyphen.
    Mapping: z_i mod 15 → Glyph-Index
    """
    p17, p23, p1_16_inv = load_data()
    digits = p17["v7_lateinische_ziffern"]["values"]
    glyph_total = p1_16_inv["per_glyph_total"]

    glyphs = sorted(glyph_total.keys())
    n_glyphs = len(glyphs)

    # Vorhersage: jeder Ziffer → Glyph-Index
    predicted = [glyphs[d % n_glyphs] for d in digits]

    # Tatsächliche Top-10 Glyphen in p1-16 (nach Frequenz)
    actual_top = sorted(glyph_total.keys(), key=lambda g: -glyph_total[g])[:10]

    # Hit-Rate
    hits = sum(1 for p in predicted if p in actual_top)
    hit_rate = hits / len(predicted)

    # Zufalls-Baseline: erwartet ~10/15 = 0.667
    random_baseline = 10 / n_glyphs

    print(f"  p17-Ziffern:        {digits}")
    print(f"  Vorhersage-Glyphen: {predicted}")
    print(f"  Tatsächliche Top-10: {actual_top}")
    print(f"  Hit-Rate:           {hit_rate:.3f} ({hits}/{len(predicted)})")
    print(f"  Random-Baseline:    {random_baseline:.3f}")
    if hit_rate > 0.5:
        print(f"  → Hit-Rate > 0.5 (Hypothese GESTÜTZT)")
    else:
        print(f"  → Hit-Rate {hit_rate:.3f} <= 0.5 (Hypothese FALSIFIZIERT)")
    assert hit_rate > 0.5, f"Hit-Rate {hit_rate:.3f} <= 0.5"


def test_burumut_hash_to_glyph():
    """BURUMUT-Wort-Hash → Glyph-Code?"""
    p17, p23, p1_16_inv = load_data()
    burumut_words = [w["wort"] for w in p23["woerter"]]
    glyph_total = p1_16_inv["per_glyph_total"]

    glyphs = sorted(glyph_total.keys())
    n_glyphs = len(glyphs)

    # Hash: Summe der Buchstaben-Werte
    def word_hash(word):
        return sum(ord(c) for c in word.upper()) % n_glyphs

    # Vorhersage
    predicted = [glyphs[word_hash(w)] for w in burumut_words]

    # Tatsächliche Glyphen in p1-16
    p1_16_glyphs = set(glyph_total.keys())

    # Hit-Rate
    hits = sum(1 for p in predicted if p in p1_16_glyphs)
    hit_rate = hits / len(predicted)

    print(f"  BURUMUT-Wörter:     {len(burumut_words)}")
    print(f"  Vorhersage-Glyphen: {predicted}")
    print(f"  Hits in p1-16:      {hits}/{len(predicted)} = {hit_rate:.3f}")
    if hit_rate > 0.5:
        print(f"  → Hash-Mapping > 50% (Hypothese GESTÜTZT)")
    else:
        print(f"  → Hash-Mapping {hit_rate:.3f} (Hypothese FALSIFIZIERT)")
    assert hit_rate > 0.5, f"Hit-Rate {hit_rate:.3f} <= 0.5"


def test_tappeiner_cleartext_to_glyph():
    """Tappeiner-Klartext 'TIME FOR THE TRUTH' → Glyph-Mapping?"""
    p17, p23, p1_16_inv = load_data()
    klartext_zeilen = p17["tappeiner_brueche_klartext"]["klartext_zeilen"]
    glyph_total = p1_16_inv["per_glyph_total"]

    glyphs = sorted(glyph_total.keys())
    n_glyphs = len(glyphs)

    # Erstes Wort jeder Klartext-Zeile
    first_words = [line.split()[0] for line in klartext_zeilen]
    # Wort → Glyph
    def word_to_glyph(word):
        return glyphs[sum(ord(c) for c in word.upper()) % n_glyphs]

    predicted = [word_to_glyph(w) for w in first_words]
    p1_16_glyphs = set(glyph_total.keys())
    hits = sum(1 for p in predicted if p in p1_16_glyphs)
    hit_rate = hits / len(predicted)

    print(f"  Klartext-Zeilen:    {len(klartext_zeilen)}")
    print(f"  Erste Wörter:       {first_words}")
    print(f"  Vorhersage-Glyphen: {predicted}")
    print(f"  Hits in p1-16:      {hits}/{len(predicted)} = {hit_rate:.3f}")
    if hit_rate > 0.5:
        print(f"  → Klartext-Mapping > 50% (Hypothese GESTÜTZT)")
    else:
        print(f"  → Klartext-Mapping {hit_rate:.3f} (Hypothese FALSIFIZIERT)")
    assert hit_rate > 0.5, f"Hit-Rate {hit_rate:.3f} <= 0.5"


def main():
    print("=" * 80)
    print("V13 GENERATIVE — TDD-TESTS (3 Tests)")
    print("=" * 80)
    print()
    print("Hypothese: Es gibt F: p17-23 → p1-16 (deterministisches Mapping)")
    print()

    tests = [
        ("test_digit_to_glyph_mapping_predicts", test_digit_to_glyph_mapping_predicts),
        ("test_burumut_hash_to_glyph", test_burumut_hash_to_glyph),
        ("test_tappeiner_cleartext_to_glyph", test_tappeiner_cleartext_to_glyph),
    ]

    passed = 0
    failed = 0
    for name, fn in tests:
        print("=" * 80)
        print(f"RUN: {name}")
        print("=" * 80)
        try:
            fn()
            print(f"✓ PASS: {name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ FAIL (expected): {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️  ERROR: {e}")
            failed += 1
        print()

    print("=" * 80)
    print(f"V13 GENERATIVE: {passed} PASS, {failed} expected FAIL")
    print("=" * 80)
    if failed > 0:
        print("ℹ️  TDD-Disziplin: Fail = Hypothese FALSIFIZIERT")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
