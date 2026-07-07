"""
v13_sequenz_faltung.py
V13 PHASE 4 — SEQUENZ/FALTUNGS-IMPLEMENTIERUNG (empirisch, mit Verdict)

Methode: V12 Cross-Layer-Kohärenz erweitert. Rank-Korrelation. Faltungs-Kernel
(uniform, gaussian, exponential). Spiral-Position-Funktion (1/n, log, fib).

Output: bbox/v13_sequenz_faltung_20260707/sequenz_verdict.json
"""
import json
import math
from pathlib import Path
from datetime import datetime

OUT_DIR = Path("bbox/v13_sequenz_faltung_20260707")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def spearman_rho(x, y):
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
    if len(a) != len(b) or len(a) == 0:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def convolve(signal, kernel):
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
    if kernel_type == "uniform":
        return [1.0 / size] * size
    elif kernel_type == "gaussian":
        sigma = size / 3.0
        return [math.exp(-((i - size//2) ** 2) / (2 * sigma ** 2)) for i in range(size)]
    elif kernel_type == "exponential":
        decay = 0.3
        return [math.exp(-abs(i - size//2) * decay) for i in range(size)]
    return [1.0] * size


def main():
    print("=" * 80)
    print("V13 SEQUENZ/FALTUNG — EMPIRISCHE ANALYSE")
    print("=" * 80)
    print()
    print("Hypothese: p1-p16 = p17-23 ⊛ Kernel (Spiral/Faltung)")
    print()

    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p1_16_inv = json.load(open("bbox/v11_p1_p16_20260706/glyph_word_inventory.json"))
    bw = json.load(open("bbox/v12_bewusst_20260707/bewusst_verdict.json"))

    # =========================================================================
    # TEST 1: Akrostichon-Rank ↔ p1-16 Glyph-Frequenz-Rank
    # =========================================================================
    print("=" * 80)
    print("TEST 1: AKROSTICHON-RANK ↔ p1-16 GLYPH-FREQUENZ-RANK")
    print("=" * 80)
    akrostichon = p17["akrostichon_der_11_glyphen"]["string"]
    glyph_freq = p1_16_inv["per_glyph_total"]
    perfect_match_v12 = bw["test_3_cross_layer"]["n_perfect_sequence"]
    n_perfect_total = len(bw["test_3_cross_layer"]["first_letters_burumut"])

    glyphs_by_freq = sorted(glyph_freq.keys(), key=lambda g: -glyph_freq[g])
    freq_rank = {g: i + 1 for i, g in enumerate(glyphs_by_freq)}

    akrostichon_ranks = [ord(c) - ord('A') + 1 for c in akrostichon]
    p1_16_ranks = [freq_rank.get(g, 0) for g in sorted(glyph_freq.keys())]

    rho, _ = spearman_rho(akrostichon_ranks[:11], p1_16_ranks[:11])

    print(f"  V12-Befund:          {perfect_match_v12}/{n_perfect_total} BURUMUT first letters = BNYZTSOYNKS")
    print(f"  Akrostichon-Ränge:   {akrostichon_ranks}")
    print(f"  p1-16 Ränge:         {p1_16_ranks}")
    print(f"  Spearman ρ:          {rho:+.3f}")
    print(f"  Schwelle:            |ρ| > 0.3")
    test1_gestuetzt = abs(rho) > 0.3
    test1_verdict = "GESTÜTZT" if test1_gestuetzt else "FALSIFIZIERT"
    print(f"  → {test1_verdict}")
    print()

    # =========================================================================
    # TEST 2: Faltungs-Hypothese
    # =========================================================================
    print("=" * 80)
    print("TEST 2: FALTUNGS-HYPOTHESE (uniform/gaussian/exponential)")
    print("=" * 80)
    digits = p17["v7_lateinische_ziffern"]["values"]
    n_glyphs = len(glyph_freq)
    p17_signal = [d % n_glyphs for d in digits]

    glyphs = sorted(glyph_freq.keys())
    p1_16_signal = [glyph_freq[g] for g in glyphs]

    s17_sum = sum(p17_signal) or 1
    s16_sum = sum(p1_16_signal) or 1
    p17_signal_n = [s / s17_sum for s in p17_signal]
    p1_16_signal_n = [s / s16_sum for s in p1_16_signal]

    similarities = {}
    for kernel_type in ["uniform", "gaussian", "exponential"]:
        kernel = make_kernel(kernel_type, size=11)
        conv = convolve(p17_signal_n, kernel)
        sim = cosine_similarity(conv, p1_16_signal_n[:11])
        similarities[kernel_type] = sim
        print(f"  Kernel {kernel_type:12s}: Cosine-Sim = {sim:.4f}")

    avg_sim = sum(similarities.values()) / len(similarities)
    print(f"  Durchschnitt:        {avg_sim:.4f}")
    print(f"  Schwelle:            > 0.3")
    test2_gestuetzt = avg_sim > 0.3
    test2_verdict = "GESTÜTZT" if test2_gestuetzt else "FALSIFIZIERT"
    print(f"  → {test2_verdict}")
    print()

    # =========================================================================
    # TEST 3: Spiral-Position-Funktion
    # =========================================================================
    print("=" * 80)
    print("TEST 3: SPIRAL-POSITION-FUNKTION (1/n, log, fib)")
    print("=" * 80)
    sorted_glyphs = sorted(glyph_freq.keys(), key=lambda g: -glyph_freq[g])
    frequencies = [glyph_freq[g] for g in sorted_glyphs]
    positions = list(range(1, len(frequencies) + 1))

    n_test = len(frequencies)
    if n_test > 1:
        f_inv_n = [1.0 / i for i in positions]
        f_log = [1.0 / math.log(2 + i) for i in positions]
        f_fib = [1.0 / ((1.618 ** i) - ((-0.618) ** i)) / math.sqrt(5) for i in positions]

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
    best_function = ["1/n", "log", "fib"][[sim_inv_n, sim_log, sim_fib].index(max_sim)]

    print(f"  Cosine-Sim 1/n:      {sim_inv_n:.4f}")
    print(f"  Cosine-Sim log:      {sim_log:.4f}")
    print(f"  Cosine-Sim fib:      {sim_fib:.4f}")
    print(f"  Max-Similarity:      {max_sim:.4f} (Funktion: {best_function})")
    print(f"  Schwelle:            > 0.7")
    test3_gestuetzt = max_sim > 0.7
    test3_verdict = "GESTÜTZT" if test3_gestuetzt else "FALSIFIZIERT"
    print(f"  → {test3_verdict}")
    print()

    # =========================================================================
    # GESAMT-VERDICT
    # =========================================================================
    print("=" * 80)
    print("GESAMT-VERDICT: SEQUENZ/FALTUNG")
    print("=" * 80)
    n_gestuetzt = sum([test1_gestuetzt, test2_gestuetzt, test3_gestuetzt])
    if n_gestuetzt == 3:
        gesamt_verdict = "GESTÜTZT (3/3): Spiral/Faltungs-Hypothese bestätigt"
    elif n_gestuetzt >= 2:
        gesamt_verdict = f"TEILWEISE GESTÜTZT ({n_gestuetzt}/3)"
    else:
        gesamt_verdict = f"FALSIFIZIERT ({n_gestuetzt}/3)"
    print(f"  {gesamt_verdict}")
    print()

    out = {
        "metadata": {
            "phase": "V13 / Phase 4",
            "datum": datetime.now().isoformat(),
            "hypothese": "p1-p16 = p17-23 ⊛ Kernel (Spiral/Faltung)",
            "methode": "Rank-Korrelation + Faltungs-Kernel + Position-Funktion",
        },
        "test_1_akrostichon_rank": {
            "rho": round(rho, 4),
            "schwelle": 0.3,
            "v12_burumut_perfect_match": f"{perfect_match_v12}/{n_perfect_total}",
            "verdict": test1_verdict,
        },
        "test_2_faltung": {
            "kernel_similarities": {k: round(v, 4) for k, v in similarities.items()},
            "avg_similarity": round(avg_sim, 4),
            "schwelle": 0.3,
            "verdict": test2_verdict,
        },
        "test_3_spiral_position": {
            "sim_1_n": round(sim_inv_n, 4),
            "sim_log": round(sim_log, 4),
            "sim_fib": round(sim_fib, 4),
            "best_function": best_function,
            "max_similarity": round(max_sim, 4),
            "schwelle": 0.7,
            "verdict": test3_verdict,
        },
        "gesamt_verdict": gesamt_verdict,
        "n_gestuetzt": n_gestuetzt,
        "n_total": 3,
    }
    out_path = OUT_DIR / "sequenz_verdict.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"✓ Output: {out_path}")


if __name__ == "__main__":
    main()
