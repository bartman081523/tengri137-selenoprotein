"""
v13_information_theory.py
V13 PHASE 1 — INFORMATIONSTHEORIE-IMPLEMENTIERUNG (empirisch, mit Verdict)

Methode: gzip-Kolmogorov-Proxy für p17-Klartext, p23-BURUMUT, p1-16 Wikia.
Vergleich: 10k Zufallsstrings. Verhältnis H(p17+p23) / H(p1-16).

Output: bbox/v13_information_theory_20260707/info_verdict.json
"""
import json
import gzip
import random
import string
from pathlib import Path
from datetime import datetime

OUT_DIR = Path("bbox/v13_information_theory_20260707")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def kolmogorov_proxy(text):
    if not text:
        return 0.0
    raw = text.encode() if isinstance(text, str) else text
    compressed = gzip.compress(raw)
    return len(compressed) / len(raw)


def main():
    print("=" * 80)
    print("V13 INFORMATIONSTHEORIE — EMPIRISCHE ANALYSE")
    print("=" * 80)
    print()
    print("Hypothese: p17-p23 ist komprimierte Source für p1-p16")
    print()

    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))

    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    p23_text = " ".join(w["wort"] for w in p23["woerter"])
    p17_p23 = p17_text + " " + p23_text
    p1_16_text = " ".join(p["wikia"] for p in p1_16_rep["pages"])

    # =========================================================================
    # TEST 1: H(p17+p23) vs H(p1-16)
    # =========================================================================
    print("=" * 80)
    print("TEST 1: H(p17+p23) vs H(p1-16)")
    print("=" * 80)
    h_p17_p23 = kolmogorov_proxy(p17_p23)
    h_p1_16 = kolmogorov_proxy(p1_16_text)
    h_p17 = kolmogorov_proxy(p17_text)
    h_p23 = kolmogorov_proxy(p23_text)
    ratio = h_p17_p23 / h_p1_16 if h_p1_16 > 0 else 0

    print(f"  H(p17-Klartext):   {h_p17:.4f}")
    print(f"  H(p23-BURUMUT):    {h_p23:.4f}")
    print(f"  H(p17+p23):        {h_p17_p23:.4f}")
    print(f"  H(p1-16-Wikia):    {h_p1_16:.4f}")
    print(f"  Verhältnis:        {ratio:.4f}")
    print(f"  Schwelle:          0.8")
    test1_verdict = "GESTÜTZT" if ratio >= 0.8 else "FALSIFIZIERT"
    print(f"  → {test1_verdict}")
    print()

    # =========================================================================
    # TEST 2: Random-Baseline (10k)
    # =========================================================================
    print("=" * 80)
    print("TEST 2: KOLMOGOROV-VERSUS-ZUFALL (10k Zufallsstrings)")
    print("=" * 80)
    real_rate = h_p17_p23
    random.seed(42)
    random_rates = []
    for _ in range(10000):
        rnd = "".join(random.choices(string.ascii_uppercase + " ", k=len(p17_p23)))
        random_rates.append(kolmogorov_proxy(rnd))

    n_better = sum(1 for r in random_rates if r <= real_rate)
    p_value = (n_better + 1) / 10001
    random_median = sorted(random_rates)[5000]
    print(f"  Real-Rate:         {real_rate:.4f}")
    print(f"  Random-Median:     {random_median:.4f}")
    print(f"  n_better_random:   {n_better}/10000")
    print(f"  p-Wert:            {p_value:.4f}")
    test2_verdict = "GESTÜTZT (Komplexität über Zufall)" if p_value < 0.01 else "FALSIFIZIERT"
    print(f"  → {test2_verdict}")
    print()

    # =========================================================================
    # TEST 3: Joint-Complexity p17+p23 vs p1-16
    # =========================================================================
    print("=" * 80)
    print("TEST 3: JOINT-COMPLEXITY p17+p23 vs p1-16")
    print("=" * 80)
    joint_p17_p23 = h_p17 + h_p23
    print(f"  H(p17):            {h_p17:.4f}")
    print(f"  H(p23):            {h_p23:.4f}")
    print(f"  Joint p17+p23:     {joint_p17_p23:.4f}")
    print(f"  H(p1-16):          {h_p1_16:.4f}")
    dominates = joint_p17_p23 >= h_p1_16
    test3_verdict = "GESTÜTZT (p17+p23 dominiert)" if dominates else "FALSIFIZIERT"
    print(f"  → {test3_verdict}")
    print()

    # =========================================================================
    # GESAMT-VERDICT
    # =========================================================================
    print("=" * 80)
    print("GESAMT-VERDICT: INFORMATIONSTHEORIE")
    print("=" * 80)
    n_gestuetzt = sum([
        test1_verdict == "GESTÜTZT",
        test2_verdict.startswith("GESTÜTZT"),
        test3_verdict.startswith("GESTÜTZT"),
    ])

    if n_gestuetzt == 3:
        gesamt_verdict = "GESTÜTZT (3/3): p17-23 ist komprimierte Source für p1-16"
    elif n_gestuetzt >= 2:
        gesamt_verdict = f"TEILWEISE GESTÜTZT ({n_gestuetzt}/3)"
    else:
        gesamt_verdict = f"FALSIFIZIERT ({n_gestuetzt}/3)"

    print(f"  {gesamt_verdict}")
    print()

    # Speichern
    out = {
        "metadata": {
            "phase": "V13 / Phase 1",
            "datum": datetime.now().isoformat(),
            "hypothese": "p17-p23 = komprimierte Source für p1-16",
            "methode": "gzip-Kolmogorov-Proxy + 10k Zufalls-Baseline",
        },
        "test_1_ratio": {
            "h_p17": round(h_p17, 4),
            "h_p23": round(h_p23, 4),
            "h_p17_p23": round(h_p17_p23, 4),
            "h_p1_16": round(h_p1_16, 4),
            "ratio": round(ratio, 4),
            "schwelle": 0.8,
            "verdict": test1_verdict,
        },
        "test_2_random_baseline": {
            "real_rate": round(real_rate, 4),
            "random_median": round(random_median, 4),
            "n_better_random": n_better,
            "n_total_random": 10000,
            "p_value": round(p_value, 4),
            "verdict": test2_verdict,
        },
        "test_3_joint": {
            "joint_p17_p23": round(joint_p17_p23, 4),
            "h_p1_16": round(h_p1_16, 4),
            "dominates": dominates,
            "verdict": test3_verdict,
        },
        "gesamt_verdict": gesamt_verdict,
        "n_gestuetzt": n_gestuetzt,
        "n_total": 3,
    }
    out_path = OUT_DIR / "info_verdict.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"✓ Output: {out_path}")


if __name__ == "__main__":
    main()
