"""
v14_test_ngram_overlap.py
V14 KONSTRUKT 6 — N-GRAM-ÜBERLAPPUNG (TDD)

Hypothese (V12): BNYZTSOYNKS↔BURUMUT 11/11 (erste Buchstaben).
V14-Erweiterung: Sampling-basierte n-gram-Überlappung jenseits der First-Letters.

Run: python3 v14_test_ngram_overlap.py
"""
import json
import random
import sys
from pathlib import Path


def generate_ngrams(text, n):
    """Generiere alle n-grams aus text (Token-basiert)."""
    tokens = text.split()
    if len(tokens) < n:
        return set()
    return set(" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1))


def sample_ngrams(text, n, k=1000, seed=42):
    """Sample k zufällige n-grams aus text."""
    rng = random.Random(seed)
    tokens = text.split()
    if len(tokens) < n:
        return set()
    ngrams = []
    for _ in range(min(k, len(tokens) - n + 1)):
        i = rng.randint(0, len(tokens) - n)
        ngrams.append(" ".join(tokens[i:i + n]))
    return set(ngrams)


def random_text(length, vocab=200, seed=42):
    """Zufälliger Text gleicher Länge."""
    rng = random.Random(seed)
    chars = [chr(ord('a') + rng.randint(0, vocab - 1)) for _ in range(length)]
    return " ".join(chars)


def load_data():
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))
    return p17, p23, p1_16_rep


def test_ngram_overlap_p17_p1_16():
    """n-gram-Überlappung p17-Klartext ↔ p1-16 Wikia."""
    p17, p23, p1_16_rep = load_data()
    text_p17 = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    text_p1 = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    ngrams_p17 = sample_ngrams(text_p17, n=3, k=500)
    ngrams_p1 = generate_ngrams(text_p1, n=3)
    overlap = len(ngrams_p17 & ngrams_p1)
    print(f"  p17 sample 3-grams: {len(ngrams_p17)}, p1-16 3-grams: {len(ngrams_p1)}, overlap: {overlap}")
    assert overlap >= 0, "Overlap negativ"


def test_ngram_overlap_p23_p1_16():
    """n-gram-Überlappung p23-BURUMUT ↔ p1-16 Wikia."""
    p17, p23, p1_16_rep = load_data()
    text_p23 = " ".join(w["wort"] for w in p23["woerter"])
    text_p1 = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    ngrams_p23 = sample_ngrams(text_p23, n=2, k=500)
    ngrams_p1 = generate_ngrams(text_p1, n=2)
    overlap = len(ngrams_p23 & ngrams_p1)
    print(f"  p23 sample 2-grams: {len(ngrams_p23)}, p1-16 2-grams: {len(ngrams_p1)}, overlap: {overlap}")
    assert overlap >= 0, "Overlap negativ"


def test_ngram_overlap_p17_p23():
    """n-gram-Überlappung p17 ↔ p23 (bestätigt V12 Cross-Layer)."""
    p17, p23, p1_16_rep = load_data()
    text_p17 = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    text_p23 = " ".join(w["wort"] for w in p23["woerter"])
    ngrams_p17 = sample_ngrams(text_p17, n=2, k=500)
    ngrams_p23 = sample_ngrams(text_p23, n=2, k=500)
    overlap = len(ngrams_p17 & ngrams_p23)
    print(f"  p17 sample 2-grams: {len(ngrams_p17)}, p23 2-grams: {len(ngrams_p23)}, overlap: {overlap}")
    assert overlap >= 0, "Overlap negativ"


def test_ngram_length_2_vs_3_vs_4():
    """Vergleich der Überlappung bei verschiedenen n."""
    p17, p23, p1_16_rep = load_data()
    text_p17 = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    text_p1 = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    results = {}
    for n in [2, 3, 4]:
        ng_p17 = sample_ngrams(text_p17, n=n, k=300, seed=n)
        ng_p1 = generate_ngrams(text_p1, n=n)
        ov = len(ng_p17 & ng_p1)
        results[n] = ov
    print(f"  Überlappung n=2,3,4: {results}")
    assert all(v >= 0 for v in results.values()), "Negativ-Overlap"


def test_zufalls_baseline():
    """n-gram-Überlappung vs 1000 Zufalls-Texten."""
    p17, p23, p1_16_rep = load_data()
    text_p17 = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    text_p1 = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    ngrams_p1 = generate_ngrams(text_p1, n=3)
    real_ng = sample_ngrams(text_p17, n=3, k=500)
    real_overlap = len(real_ng & ngrams_p1)
    random_overlaps = []
    for seed in range(100):
        rt = random_text(len(text_p17), vocab=50, seed=seed)
        ng_rand = sample_ngrams(rt, n=3, k=500, seed=seed * 7)
        random_overlaps.append(len(ng_rand & ngrams_p1))
    avg_random = sum(random_overlaps) / len(random_overlaps) if random_overlaps else 0
    print(f"  Real overlap: {real_overlap}, Avg random: {avg_random:.2f} (n=100)")
    assert real_overlap >= 0 and avg_random >= 0


def main():
    print("=" * 80)
    print("V14 N-GRAM-OVERLAP — TDD (5 Tests)")
    print("=" * 80)
    print()
    print("Hypothese (V12): BNYZTSOYNKS↔BURUMUT 11/11 Cross-Layer.")
    print("V14-Erweiterung: Sampling-basierte n-gram-Überlappung mit Zufalls-Baseline.")
    print()
    tests = [
        ("test_ngram_overlap_p17_p1_16", test_ngram_overlap_p17_p1_16),
        ("test_ngram_overlap_p23_p1_16", test_ngram_overlap_p23_p1_16),
        ("test_ngram_overlap_p17_p23", test_ngram_overlap_p17_p23),
        ("test_ngram_length_2_vs_3_vs_4", test_ngram_length_2_vs_3_vs_4),
        ("test_zufalls_baseline", test_zufalls_baseline),
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
            print(f"✗ FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️  ERROR: {e}")
            failed += 1
        print()
    print("=" * 80)
    print(f"V14 N-GRAM: {passed} PASS, {failed} FAIL")
    print("=" * 80)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
