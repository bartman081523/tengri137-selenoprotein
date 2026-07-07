"""
v13_test_information_theory.py
V13 PHASE 1 — INFORMATIONSTHEORETISCHER TEST (TDD)

Hypothese: p17-p23 ist komprimierte Source für p1-p16.
Methode: gzip-Kompressionsraten vergleichen.

Run: python3 v13_test_information_theory.py
Erwartet: Tests dokumentieren den Ist-Stand (entweder PASS wenn Komplexitäts-Verhältnis
stimmt, oder expected FAIL wenn nicht).
"""
import json
import gzip
import sys
from pathlib import Path


# Daten laden
def load_data():
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    burumut = json.load(open("bbox/burumut_20260707_V7/burumut_texts.json"))
    p1_16_inv = json.load(open("bbox/v11_p1_p16_20260706/glyph_word_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))
    return p17, p23, burumut, p1_16_inv, p1_16_rep


def kolmogorov_proxy(text):
    """gzip-Kompressionsrate als Kolmogorov-Proxy."""
    if not text:
        return 0.0
    raw = text.encode() if isinstance(text, str) else text
    compressed = gzip.compress(raw)
    return len(compressed) / len(raw)


# Konstanten
THRESHOLD = 0.8  # p17-23 sollte mind. 80% der p1-16 Komplexität haben


def test_p17_p23_more_complex_than_p1_p16():
    """Spiral-Hypothese: p17-23 (Source) sollte mind. 80% der p1-16 Komplexität haben.

    Bei einem komprimierten Generator: p17-23 Information ≫ p1-16
    Bei zufälliger Verteilung: p17-23 Information ≈ p1-16
    """
    p17, p23, burumut, p1_16_inv, p1_16_rep = load_data()

    # p17-Klartext (Tappeiner-Brüche)
    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])

    # p23-BURUMUT: alle 11 Wörter
    p23_text = " ".join(w["wort"] for w in p23["woerter"])

    # p17+p23 joint
    p17_p23 = p17_text + " " + p23_text

    # p1-16 Wikia-Plaintexte konkateniert
    p1_16_text = " ".join(p["wikia"] for p in p1_16_rep["pages"])

    h_p17_p23 = kolmogorov_proxy(p17_p23)
    h_p1_16 = kolmogorov_proxy(p1_16_text)
    ratio = h_p17_p23 / h_p1_16 if h_p1_16 > 0 else 0

    print(f"  H(p17+p23):       {h_p17_p23:.4f}")
    print(f"  H(p1-16):         {h_p1_16:.4f}")
    print(f"  Verhältnis:       {ratio:.4f}")
    print(f"  Schwelle:         {THRESHOLD}")
    if ratio >= THRESHOLD:
        print(f"  → p17-23 hat mindestens 80% der p1-16 Komplexität (Source-Hypothese GESTÜTZT)")
    else:
        print(f"  → p17-23 hat nur {ratio:.1%} der p1-16 Komplexität")
        print(f"  → p1-16 ist informativer als p17-23 (Source-Hypothese FALSIFIZIERT)")
    assert ratio >= THRESHOLD, f"Verhältnis {ratio:.3f} < {THRESHOLD}: p17-23 ist NICHT komprimierte Source"


def test_p17_p23_kolmogorov_random_baseline():
    """Kolmogorov-Proxy: ist p17+p23 informativer als Zufall?"""
    import random
    import string

    p17, p23, burumut, p1_16_inv, p1_16_rep = load_data()
    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    p23_text = " ".join(w["wort"] for w in p23["woerter"])
    p17_p23 = p17_text + " " + p23_text

    real_rate = kolmogorov_proxy(p17_p23)

    random.seed(42)
    random_rates = []
    for _ in range(1000):
        rnd = "".join(random.choices(string.ascii_uppercase + " ", k=len(p17_p23)))
        random_rates.append(kolmogorov_proxy(rnd))

    random_median = sorted(random_rates)[500]
    n_better_random = sum(1 for r in random_rates if r <= real_rate)
    p_value = (n_better_random + 1) / 1001

    print(f"  Real-Rate:        {real_rate:.4f}")
    print(f"  Random-Median:    {random_median:.4f}")
    print(f"  n_better_random:  {n_better_random}/1000")
    print(f"  p-Wert:           {p_value:.4f}")
    if p_value < 0.01:
        print(f"  → p17-23 deutlich über Zufall (p<0.01)")
    else:
        print(f"  → p17-23 nicht signifikant über Zufall")
    assert p_value < 0.01, f"p-Wert {p_value:.4f} >= 0.01: p17-23 nicht über Zufall"


def test_joint_complexity_dominates():
    """Gemeinsame Komplexität: p17+23 ≥ p1-16?"""
    p17, p23, burumut, p1_16_inv, p1_16_rep = load_data()

    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    p23_text = " ".join(w["wort"] for w in p23["woerter"])

    p1_16_text = " ".join(p["wikia"] for p in p1_16_rep["pages"])

    h_p17 = kolmogorov_proxy(p17_text)
    h_p23 = kolmogorov_proxy(p23_text)
    h_p1_16 = kolmogorov_proxy(p1_16_text)

    print(f"  H(p17-Klartext):   {h_p17:.4f}")
    print(f"  H(p23-BURUMUT):    {h_p23:.4f}")
    print(f"  H(p1-16-Wikia):    {h_p1_16:.4f}")
    print(f"  Summe p17+p23:     {h_p17 + h_p23:.4f}")
    if (h_p17 + h_p23) >= h_p1_16:
        print(f"  → p17+p23 dominiert (joint ≥ p1-16)")
    else:
        print(f"  → p1-16 dominiert (joint < p1-16)")
    assert (h_p17 + h_p23) >= h_p1_16, "p17+23 Komplexität < p1-16: Hypothese FALSIFIZIERT"


def main():
    print("=" * 80)
    print("V13 INFORMATIONSTHEORIE — TDD-TESTS (3 Tests)")
    print("=" * 80)
    print()
    print("Hypothese: p17-p23 ist komprimierte Source für p1-p16")
    print("Methode: gzip-Kolmogorov-Proxy vergleichen")
    print()

    tests = [
        ("test_p17_p23_more_complex_than_p1_p16", test_p17_p23_more_complex_than_p1_p16),
        ("test_p17_p23_kolmogorov_random_baseline", test_p17_p23_kolmogorov_random_baseline),
        ("test_joint_complexity_dominates", test_joint_complexity_dominates),
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
            print(f"✗ FAIL (expected wenn Hypothese falsifiziert): {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️  ERROR: {e}")
            failed += 1
        print()

    print("=" * 80)
    print(f"V13 INFORMATIONSTHEORIE: {passed} PASS, {failed} expected FAIL")
    print("=" * 80)
    if failed > 0:
        print("ℹ️  TDD-Disziplin: Fail = Hypothese FALSIFIZIERT (das ist gut, wir dokumentieren die Realität)")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
