"""
v13_test_sequenz_faltung.py
V13 PHASE 4 — SEQUENZ/FALTUNGS-TEST (TDD)

Hypothese: p1-p16 ist deterministische Expansion/Faltung der p17-23 Sequenz.
Methode: V12 Cross-Layer-Kohärenz (BNYZTSOYNKS↔BURUMUT 11/11) erweitert.
          Rank-Korrelation. Verschiedene Faltungs-Kernel.

Run: python3 v13_test_sequenz_faltung.py
"""
import json
import math
import sys
from pathlib import Path


def spearman_rho(x, y):
    """Pure-Python Spearman Rangkorrelation."""
    n = len(x)
    if n != len(y) or n < 2:
        return 0.0, 1.0

    def rank(values):
        sorted_idx = sorted(range(n), key=lambda i: values[i])
        ranks = [0] * n
        for r, i in enumerate(sorted_idx):
            ranks[i] = r + 1
        return ranks
    rx = rank(x)
    ry = rank(y)
    mean_rx = sum(rx) / n
    mean_ry = sum(ry) / n
    num = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n))
    den_x = sum((rx[i] - mean_rx) ** 2 for i in range(n)) ** 0.5
    den_y = sum((ry[i] - mean_ry) ** 2 for i in range(n)) ** 0.5
    if den_x == 0 or den_y == 0:
        return 0.0, 1.0
    rho = num / (den_x * den_y)
    return rho, 0.0


def cosine_similarity(a, b):
    """Cosine-Similarity."""
    if len(a) != len(b) or len(a) == 0:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def convolve(signal, kernel):
    """1D-Faltung signal ⊛ kernel (gleiche Länge Output)."""
    n = len(signal)
    k = len(kernel)
    if k == 0 or n == 0:
        return []
    half = k // 2
    result = []
    for i in range(n):
        val = 0.0
        for j in range(k):
            idx = i - half + j
            if 0 <= idx < n:
                val += signal[idx] * kernel[j]
        result.append(val)
    return result


def make_kernel(kernel_type, size=11):
    """Verschiedene Kernel-Typen."""
    if kernel_type == "uniform":
        return [1.0 / size] * size
    elif kernel_type == "gaussian":
        sigma = size / 3.0
        return [math.exp(-((i - size//2) ** 2) / (2 * sigma ** 2)) for i in range(size)]
    elif kernel_type == "exponential":
        decay = 0.3
        return [math.exp(-abs(i - size//2) * decay) for i in range(size)]
    return [1.0] * size


def load_data():
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p1_16_inv = json.load(open("bbox/v11_p1_p16_20260706/glyph_word_inventory.json"))
    bw = json.load(open("bbox/v12_bewusst_20260707/bewusst_verdict.json"))
    return p17, p1_16_inv, bw


def test_p17_akrostichon_extends_to_p1_16():
    """BNYZTSOYNKS rank-korreliert mit p1-16 Glyph-Frequenz?"""
    p17, p1_16_inv, bw = load_data()
    akrostichon = p17["akrostichon_der_11_glyphen"]["string"]
    glyph_freq = p1_16_inv["per_glyph_total"]

    # V12-Befund: BNYZTSOYNKS = erste Buchstaben aller 11 BURUMUT-Wörter (11/11)
    burumut_first = bw["test_3_cross_layer"]["first_letters_burumut"]
    perfect_match = bw["test_3_cross_layer"]["n_perfect_sequence"]
    print(f"  V12-Befund:         {perfect_match}/11 BURUMUT first letters = BNYZTSOYNKS")

    # Erweitere Frage: Korrelieren p17-Glyphen-Ränge mit p1-16 Glyph-Frequenz-Rängen?
    # p17-Glyphen sind 'B', 'N', 'Y', 'Z', 'T', 'S', 'O', 'Y', 'N', 'K', 'S'
    # p1-16 hat numerische Glyphen G01, G02, ...
    # Mapping: Glyphen → Index basierend auf Frequenz
    glyphs_by_freq = sorted(glyph_freq.keys(), key=lambda g: -glyph_freq[g])
    freq_rank = {g: i + 1 for i, g in enumerate(glyphs_by_freq)}

    # p17-Akrostichon hat 11 Positionen. Pro Position suchen wir den passenden Glyph-Rang.
    # Mapping: A=1, B=2, ..., Z=26 → suche Glyphen mit ähnlichem Rang
    # Vereinfachung: jeder Buchstabe des Akrostichons bekommt einen Rang nach Alphabet
    akrostichon_ranks = [ord(c) - ord('A') + 1 for c in akrostichon]
    # p1-16 Glyphen-Ränge (alle 15)
    p1_16_ranks = [freq_rank.get(g, 0) for g in sorted(glyph_freq.keys())]

    # Korrelation der ersten 11
    rho, _ = spearman_rho(akrostichon_ranks[:11], p1_16_ranks[:11])

    print(f"  Akrostichon-Ränge:  {akrostichon_ranks}")
    print(f"  p1-16 Ränge:        {p1_16_ranks}")
    print(f"  Spearman ρ:         {rho:+.3f}")
    print(f"  Schwelle:           |ρ| > 0.3")
    if abs(rho) > 0.3:
        print(f"  → Rank-Korrelation signifikant (Spiral: GESTÜTZT)")
    else:
        print(f"  → Schwache Korrelation (Spiral: FALSIFIZIERT)")
    assert abs(rho) > 0.3, f"|ρ|={abs(rho):.3f} <= 0.3: keine Rank-Korrelation"


def test_faltung_p17_with_kernel_yields_p1_16():
    """Faltungs-Hypothese: p1-p16 = p17 ⊛ Kernel?

    Wir kodieren p17 als 11-Signal (Ziffern mod 15).
    Wir kodieren p1-16 als 15-Signal (Glyph-Frequenz, normalisiert).
    Verschiedene Kernel: uniform, gaussian, exponential.
    """
    p17, p1_16_inv, _ = load_data()
    digits = p17["v7_lateinische_ziffern"]["values"]
    glyph_total = p1_16_inv["per_glyph_total"]

    # p17-Signal (11 Ziffern mod 15)
    n_glyphs = len(glyph_total)
    p17_signal = [d % n_glyphs for d in digits]

    # p1-16 Glyphen-Frequenz (15 Werte)
    glyphs = sorted(glyph_total.keys())
    p1_16_signal = [glyph_total[g] for g in glyphs]

    # Normalisieren
    s17_sum = sum(p17_signal) or 1
    s16_sum = sum(p1_16_signal) or 1
    p17_signal_n = [s / s17_sum for s in p17_signal]
    p1_16_signal_n = [s / s16_sum for s in p1_16_signal]

    print(f"  p17-Signal (normalisiert):  {p17_signal_n}")
    print(f"  p1-16-Signal (normalisiert): {p1_16_signal_n}")
    print()

    similarities = {}
    for kernel_type in ["uniform", "gaussian", "exponential"]:
        kernel = make_kernel(kernel_type, size=11)
        # Faltung: p17 ⊛ kernel → 11-Werte
        conv = convolve(p17_signal_n, kernel)
        # Vergleiche mit p1-16 (15-Werte): wir nehmen die ersten 11
        sim = cosine_similarity(conv, p1_16_signal_n[:11])
        similarities[kernel_type] = sim
        print(f"  Kernel {kernel_type:12s}: Cosine-Sim = {sim:.4f}")

    avg_sim = sum(similarities.values()) / len(similarities)
    print(f"  Durchschnitt:                  {avg_sim:.4f}")
    print(f"  Schwelle:                      0.3")
    if avg_sim > 0.3:
        print(f"  → Faltungs-Hypothese GESTÜTZT")
    else:
        print(f"  → Faltungs-Hypothese FALSIFIZIERT")
    assert avg_sim > 0.3, f"Avg-Similarity {avg_sim:.3f} <= 0.3"


def test_spiral_unfolding_position_function():
    """Frequenz vs Position: folgt mathematischem Gesetz (1/n, log, fib)?

    Spiral-Hypothese: Häufigkeit der Glyphen folgt einer mathematischen Funktion
    ihrer Position (z.B. Fibonacci-Rang).
    """
    p17, p1_16_inv, _ = load_data()
    glyph_total = p1_16_inv["per_glyph_total"]

    # Sortiere Glyphen nach Frequenz (Top-Down)
    sorted_glyphs = sorted(glyph_total.keys(), key=lambda g: -glyph_total[g])
    frequencies = [glyph_total[g] for g in sorted_glyphs]

    # Position (1, 2, 3, ...)
    positions = list(range(1, len(frequencies) + 1))

    # Test verschiedene Funktionen
    # 1) 1/n: erwartete Frequenz f(i) = C/i
    n_test = len(frequencies)
    if n_test > 1:
        f_inv_n = [1.0 / i for i in positions]
        f_log = [1.0 / math.log(2 + i) for i in positions]
        f_fib = [1.0 / ((1.618 ** i) - ((-0.618) ** i)) / math.sqrt(5) for i in positions]
        # Normalisieren
        def norm(v):
            s = sum(v) or 1
            return [x / s for x in v]
        f_inv_n_n = norm(f_inv_n)
        f_log_n = norm(f_log)
        f_fib_n = norm(f_fib)
        f_actual_n = norm(frequencies)
    else:
        f_inv_n_n = f_log_n = f_fib_n = f_actual_n = frequencies

    sim_inv_n = cosine_similarity(f_inv_n_n, f_actual_n)
    sim_log = cosine_similarity(f_log_n, f_actual_n)
    sim_fib = cosine_similarity(f_fib_n, f_actual_n)

    max_sim = max(sim_inv_n, sim_log, sim_fib)

    print(f"  Glyphen-Frequenzen: {frequencies}")
    print(f"  Cosine-Sim 1/n:     {sim_inv_n:.4f}")
    print(f"  Cosine-Sim log:     {sim_log:.4f}")
    print(f"  Cosine-Sim fib:     {sim_fib:.4f}")
    print(f"  Max-Similarity:     {max_sim:.4f}")
    print(f"  Schwelle:           0.7")
    if max_sim > 0.7:
        print(f"  → Spiral-Hypothese GESTÜTZT (Frequenz folgt mathematischem Gesetz)")
    else:
        print(f"  → Frequenz folgt KEINEM der getesteten Gesetze")
    assert max_sim > 0.7, f"Max-Sim {max_sim:.3f} <= 0.7"


def main():
    print("=" * 80)
    print("V13 SEQUENZ/FALTUNG — TDD-TESTS (3 Tests)")
    print("=" * 80)
    print()
    print("Hypothese: p1-p16 = p17-23 ⊛ Kernel (Spiral/Faltung)")
    print()

    tests = [
        ("test_p17_akrostichon_extends_to_p1_16", test_p17_akrostichon_extends_to_p1_16),
        ("test_faltung_p17_with_kernel_yields_p1_16", test_faltung_p17_with_kernel_yields_p1_16),
        ("test_spiral_unfolding_position_function", test_spiral_unfolding_position_function),
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
    print(f"V13 SEQUENZ/FALTUNG: {passed} PASS, {failed} expected FAIL")
    print("=" * 80)
    if failed > 0:
        print("ℹ️  TDD-Disziplin: Fail = Hypothese FALSIFIZIERT")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
