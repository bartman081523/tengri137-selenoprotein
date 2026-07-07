"""
v13_generative.py
V13 PHASE 3 — GENERATIVE-IMPLEMENTIERUNG (empirisch, mit Verdict)

Methode: 3 Mapping-Funktionen testen (digit→glyph, hash→glyph, Klartext→glyph).
Hit-Rate gegen p1-16. Zufalls-Baseline.

Output: bbox/v13_generative_20260707/generative_verdict.json
"""
import json
import random
import string
from pathlib import Path
from datetime import datetime

OUT_DIR = Path("bbox/v13_generative_20260707")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("=" * 80)
    print("V13 GENERATIVE — EMPIRISCHE ANALYSE")
    print("=" * 80)
    print()
    print("Hypothese: Es gibt F: p17-23 → p1-16 (deterministisches Mapping)")
    print()

    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_inv = json.load(open("bbox/v11_p1_p16_20260706/glyph_word_inventory.json"))
    glyph_total = p1_16_inv["per_glyph_total"]
    glyphs = sorted(glyph_total.keys())
    n_glyphs = len(glyphs)
    p1_16_glyphs = set(glyph_total.keys())

    # =========================================================================
    # TEST 1: Digit → Glyph (mod n_glyphs)
    # =========================================================================
    print("=" * 80)
    print("TEST 1: DIGIT → GLYPH (mod n_glyphs)")
    print("=" * 80)
    digits = p17["v7_lateinische_ziffern"]["values"]
    predicted = [glyphs[d % n_glyphs] for d in digits]
    actual_top = sorted(glyph_total.keys(), key=lambda g: -glyph_total[g])[:10]
    hits1 = sum(1 for p in predicted if p in actual_top)
    rate1 = hits1 / len(predicted)

    # Zufalls-Baseline: 10k
    random.seed(42)
    baseline_rates = []
    for _ in range(10000):
        rnd_pred = [glyphs[random.randint(0, n_glyphs - 1)] for _ in digits]
        rnd_hits = sum(1 for p in rnd_pred if p in actual_top)
        baseline_rates.append(rnd_hits / len(digits))
    n_better = sum(1 for b in baseline_rates if b <= rate1)
    p1_value = (n_better + 1) / 10001
    random_median1 = sorted(baseline_rates)[5000]

    print(f"  p17-Ziffern:         {digits}")
    print(f"  Vorhersage-Glyphen:  {predicted}")
    print(f"  Tatsächliche Top-10: {actual_top}")
    print(f"  Hit-Rate:            {rate1:.3f} ({hits1}/{len(predicted)})")
    print(f"  Random-Baseline (Median): {random_median1:.3f}")
    print(f"  p-Wert vs Zufall:    {p1_value:.4f}")
    print(f"  Schwelle:            > 0.5")
    test1_gestuetzt = rate1 > 0.5
    test1_verdict = "GESTÜTZT" if test1_gestuetzt else "FALSIFIZIERT"
    print(f"  → {test1_verdict}")
    print()

    # =========================================================================
    # TEST 2: BURUMUT-Hash → Glyph
    # =========================================================================
    print("=" * 80)
    print("TEST 2: BURUMUT-HASH → GLYPH")
    print("=" * 80)
    burumut_words = [w["wort"] for w in p23["woerter"]]

    def word_hash(word):
        return sum(ord(c) for c in word.upper()) % n_glyphs

    predicted2 = [glyphs[word_hash(w)] for w in burumut_words]
    hits2 = sum(1 for p in predicted2 if p in p1_16_glyphs)
    rate2 = hits2 / len(predicted2)

    print(f"  BURUMUT-Wörter:      {len(burumut_words)}")
    print(f"  Vorhersage-Glyphen:  {predicted2}")
    print(f"  Hits in p1-16:       {hits2}/{len(predicted2)} = {rate2:.3f}")
    print(f"  Schwelle:            > 0.5")
    test2_gestuetzt = rate2 > 0.5
    test2_verdict = "GESTÜTZT" if test2_gestuetzt else "FALSIFIZIERT"
    print(f"  → {test2_verdict}")
    print()

    # =========================================================================
    # TEST 3: Tappeiner-Klartext → Glyph
    # =========================================================================
    print("=" * 80)
    print("TEST 3: TAPPEINER-KLARTEXT → GLYPH")
    print("=" * 80)
    klartext_zeilen = p17["tappeiner_brueche_klartext"]["klartext_zeilen"]
    first_words = [line.split()[0] for line in klartext_zeilen]

    def word_to_glyph(word):
        return glyphs[sum(ord(c) for c in word.upper()) % n_glyphs]

    predicted3 = [word_to_glyph(w) for w in first_words]
    hits3 = sum(1 for p in predicted3 if p in p1_16_glyphs)
    rate3 = hits3 / len(predicted3)

    print(f"  Klartext-Zeilen:     {len(klartext_zeilen)}")
    print(f"  Erste Wörter:        {first_words}")
    print(f"  Vorhersage-Glyphen:  {predicted3}")
    print(f"  Hits in p1-16:       {hits3}/{len(predicted3)} = {rate3:.3f}")
    print(f"  Schwelle:            > 0.5")
    test3_gestuetzt = rate3 > 0.5
    test3_verdict = "GESTÜTZT" if test3_gestuetzt else "FALSIFIZIERT"
    print(f"  → {test3_verdict}")
    print()

    # =========================================================================
    # GESAMT-VERDICT
    # =========================================================================
    print("=" * 80)
    print("GESAMT-VERDICT: GENERATIVE")
    print("=" * 80)
    n_gestuetzt = sum([test1_gestuetzt, test2_gestuetzt, test3_gestuetzt])
    if n_gestuetzt == 3:
        gesamt_verdict = "GESTÜTZT (3/3): Deterministisches Mapping existiert"
    elif n_gestuetzt >= 2:
        gesamt_verdict = f"TEILWEISE GESTÜTZT ({n_gestuetzt}/3)"
    else:
        gesamt_verdict = f"FALSIFIZIERT ({n_gestuetzt}/3)"
    print(f"  {gesamt_verdict}")
    print()

    out = {
        "metadata": {
            "phase": "V13 / Phase 3",
            "datum": datetime.now().isoformat(),
            "hypothese": "F: p17-23 → p1-16 (deterministisches Mapping)",
            "methode": "3 Mapping-Funktionen + Hit-Rate vs Zufalls-Baseline",
        },
        "test_1_digit": {
            "hit_rate": round(rate1, 4),
            "p_value_vs_random": round(p1_value, 4),
            "random_median": round(random_median1, 4),
            "verdict": test1_verdict,
        },
        "test_2_burumut_hash": {
            "hit_rate": round(rate2, 4),
            "n_hits": hits2,
            "n_total": len(predicted2),
            "verdict": test2_verdict,
        },
        "test_3_klartext": {
            "hit_rate": round(rate3, 4),
            "n_hits": hits3,
            "n_total": len(predicted3),
            "verdict": test3_verdict,
        },
        "gesamt_verdict": gesamt_verdict,
        "n_gestuetzt": n_gestuetzt,
        "n_total": 3,
    }
    out_path = OUT_DIR / "generative_verdict.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"✓ Output: {out_path}")


if __name__ == "__main__":
    main()
