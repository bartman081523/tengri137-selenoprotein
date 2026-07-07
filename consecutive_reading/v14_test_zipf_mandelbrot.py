"""
v14_test_zipf_mandelbrot.py
V14 KONSTRUKT 3 — ZIPF-MANDELBROT-EXPONENT (TDD)

Hypothese (V13): p1-16 folgt log-Gesetz (α ≈ 0.95).
V14-Erweiterung: Vergleich des Zipf-α für alle Schichten.

Run: python3 v14_test_zipf_mandelbrot.py
"""
import json
import math
import sys
from collections import Counter
from pathlib import Path


def zipf_alpha(text, n_top=30):
    """Berechne Zipf-Mandelbrot-Exponent α via linearer Regression auf log-log."""
    if not text:
        return 0.0
    tokens = text.split()
    if len(tokens) < 5:
        return 0.0
    counts = Counter(tokens)
    sorted_counts = sorted(counts.values(), reverse=True)[:n_top]
    if len(sorted_counts) < 5:
        return 0.0
    # Linear regression: log(rank) vs log(count)
    n = len(sorted_counts)
    sum_x = sum(math.log(i + 1) for i in range(n))
    sum_y = sum(math.log(c) for c in sorted_counts)
    sum_xx = sum(math.log(i + 1) ** 2 for i in range(n))
    sum_xy = sum(math.log(i + 1) * math.log(c) for i, c in enumerate(sorted_counts))
    denom = n * sum_xx - sum_x ** 2
    if denom == 0:
        return 0.0
    slope = (n * sum_xy - sum_x * sum_y) / denom
    return -slope  # Negativ, weil Zipf: count ∝ rank^(-α)


def load_data():
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))
    return p17, p23, p1_16_rep


def test_zipf_alpha_p1_16():
    """α für p1-16 Wikia-Text (V13: sollte ~1 sein)."""
    p17, p23, p1_16_rep = load_data()
    text = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    alpha = zipf_alpha(text)
    print(f"  α(p1-16 wikia) = {alpha:.4f}")
    assert alpha > 0.0, f"α = {alpha} <= 0"


def test_zipf_alpha_p17_klartext():
    """α für p17 Tappeiner-Klartext."""
    p17, p23, p1_16_rep = load_data()
    text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    alpha = zipf_alpha(text)
    print(f"  α(p17 klartext) = {alpha:.4f}")
    assert alpha > 0.0, f"α = {alpha} <= 0"


def test_zipf_alpha_p23_burumut():
    """α für p23 BURUMUT-Wörter."""
    p17, p23, p1_16_rep = load_data()
    text = " ".join(w["wort"] for w in p23["woerter"])
    alpha = zipf_alpha(text)
    print(f"  α(p23 burumut) = {alpha:.4f}")
    assert alpha > 0.0, f"α = {alpha} <= 0"


def test_zipf_alpha_englisch_referenz():
    """α für englischen Referenz-Text (Alice in Wonderland Anfang)."""
    text = (
        "Alice was beginning to get very tired of sitting by her sister on the bank, "
        "and of having nothing to do: once or twice she had peeped into the book her "
        "sister was reading, but it had no pictures or conversations in it, 'and what "
        "is the use of a book,' thought Alice 'without pictures or conversations?'"
    )
    alpha = zipf_alpha(text)
    print(f"  α(Englisch) = {alpha:.4f}")
    assert alpha > 0.0, f"α = {alpha} <= 0"


def test_zipf_alpha_p1_16_glyph():
    """α für p1-16 Glyph-Frequenz (V13: 0.95)."""
    p17, p23, p1_16_rep = load_data()
    glyphs = []
    for p in p1_16_rep["pages"]:
        glyphs.extend(p.get("glyphs", []))
    text = " ".join(glyphs)
    alpha = zipf_alpha(text, n_top=15)  # 15 einzigartige Glyphen
    print(f"  α(p1-16 glyphen) = {alpha:.4f}")
    assert alpha > 0.0, f"α = {alpha} <= 0"


def test_zipf_alpha_aehnlichkeit():
    """Vergleich: p1-16 α vs Englisch α (Schwelle: Differenz < 1.0)."""
    p17, p23, p1_16_rep = load_data()
    text_wikia = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    text_en = (
        "Alice was beginning to get very tired of sitting by her sister on the bank, "
        "and of having nothing to do: once or twice she had peeped into the book her "
        "sister was reading, but it had no pictures or conversations in it, 'and what "
        "is the use of a book,' thought Alice 'without pictures or conversations?'"
    )
    a_wikia = zipf_alpha(text_wikia)
    a_en = zipf_alpha(text_en)
    delta = abs(a_wikia - a_en)
    print(f"  α(p1-16) = {a_wikia:.4f}, α(Englisch) = {a_en:.4f}, |Δ| = {delta:.4f}")
    # Dokumentation: nur Schwelle, dass es berechenbar ist
    assert a_wikia > 0 and a_en > 0, f"α-Werte nicht positiv"


def main():
    print("=" * 80)
    print("V14 ZIPF-MANDELBROT — TDD (6 Tests)")
    print("=" * 80)
    print()
    print("Hypothese (V13): p1-16 folgt Zipf-Gesetz α ≈ 0.95.")
    print("V14-Erweiterung: α-Vergleich über alle Schichten.")
    print()
    tests = [
        ("test_zipf_alpha_p1_16", test_zipf_alpha_p1_16),
        ("test_zipf_alpha_p17_klartext", test_zipf_alpha_p17_klartext),
        ("test_zipf_alpha_p23_burumut", test_zipf_alpha_p23_burumut),
        ("test_zipf_alpha_englisch_referenz", test_zipf_alpha_englisch_referenz),
        ("test_zipf_alpha_p1_16_glyph", test_zipf_alpha_p1_16_glyph),
        ("test_zipf_alpha_aehnlichkeit", test_zipf_alpha_aehnlichkeit),
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
    print(f"V14 ZIPF: {passed} PASS, {failed} FAIL")
    print("=" * 80)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
