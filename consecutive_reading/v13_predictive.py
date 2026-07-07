"""
v13_predictive.py
V13 PHASE 2 — PREDICTIVE-IMPLEMENTIERUNG (empirisch, mit Verdict)

Methode: Korrelation p17-Features vs p1-16 Glyph-Frequenz. Train/Test p1-p10 / p11-p16.
Edit-Distanz BNYZTSOYNKS vs Top-11 p1-16 Glyphen.

Output: bbox/v13_predictive_20260707/predictive_verdict.json
"""
import json
import math
from pathlib import Path
from datetime import datetime

OUT_DIR = Path("bbox/v13_predictive_20260707")
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
    if abs(rho) >= 0.9999:
        return rho, 0.0
    t_stat = rho * math.sqrt((n - 2) / (1 - rho ** 2)) if abs(rho) < 1.0 else 0
    p_value = 2 * (1 - min(1.0, abs(t_stat) / 10))
    return rho, p_value


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def cosine_similarity(a, b):
    if len(a) != len(b) or len(a) == 0:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def main():
    print("=" * 80)
    print("V13 PREDICTIVE — EMPIRISCHE ANALYSE")
    print("=" * 80)
    print()
    print("Hypothese: p17-Strukturen sagen p1-16 Glyph-Frequenz voraus")
    print()

    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p1_16_inv = json.load(open("bbox/v11_p1_p16_20260706/glyph_word_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))

    # =========================================================================
    # TEST 1: Spearman-Korrelation Ziffern ↔ Glyph-Frequenz
    # =========================================================================
    print("=" * 80)
    print("TEST 1: SPEARMAN-KORRELATION ZIFFERN ↔ GLYPH-FREQUENZ")
    print("=" * 80)
    digits = p17["v7_lateinische_ziffern"]["values"]
    glyph_total = p1_16_inv["per_glyph_total"]
    glyphs = sorted(glyph_total.keys())
    n_glyphs = len(glyphs)
    freq_vector = [glyph_total.get(g, 0) for g in glyphs]

    if len(digits) >= n_glyphs:
        feature_vector = [d % n_glyphs for d in digits[:n_glyphs]]
    else:
        feature_vector = [d % n_glyphs for d in digits] + [0] * (n_glyphs - len(digits))

    rho, p_val = spearman_rho(feature_vector, freq_vector)

    print(f"  Glyphen in p1-16:     {n_glyphs}")
    print(f"  Frequenz-Vektor:      {freq_vector}")
    print(f"  Feature-Vektor:       {feature_vector}")
    print(f"  Spearman ρ:           {rho:+.3f}")
    print(f"  p-Wert:               {p_val:.4f}")
    print(f"  Schwelle:             |ρ| > 0.5")
    test1_gestuetzt = abs(rho) > 0.5
    test1_verdict = "GESTÜTZT" if test1_gestuetzt else "FALSIFIZIERT"
    print(f"  → {test1_verdict}")
    print()

    # =========================================================================
    # TEST 2: Edit-Distanz BNYZTSOYNKS vs Top-11 p1-16 Glyphen
    # =========================================================================
    print("=" * 80)
    print("TEST 2: EDIT-DISTANZ BNYZTSOYNKS vs TOP-11 GLYPHEN")
    print("=" * 80)
    akrostichon = p17["akrostichon_der_11_glyphen"]["string"]
    sorted_glyphs = sorted(glyph_total.keys(), key=lambda g: -glyph_total[g])
    top_glyph_ids = sorted_glyphs[:11]

    def glyph_to_letter(g):
        n = int(g[1:])
        return chr(ord('A') + (n - 1) % 26)
    top_as_letters = "".join(glyph_to_letter(g) for g in top_glyph_ids)
    edit_dist = levenshtein(akrostichon, top_as_letters)

    print(f"  Akrostichon:          {akrostichon}")
    print(f"  Top-11 Glyphen-IDs:   {top_glyph_ids}")
    print(f"  Top-11 als Letter:    {top_as_letters}")
    print(f"  Edit-Distanz:         {edit_dist}")
    print(f"  Schwelle:             < 6")
    test2_gestuetzt = edit_dist < 6
    test2_verdict = "GESTÜTZT" if test2_gestuetzt else "FALSIFIZIERT"
    print(f"  → {test2_verdict}")
    print()

    # =========================================================================
    # TEST 3: Train/Test-Konsistenz p1-p10 vs p11-p16
    # =========================================================================
    print("=" * 80)
    print("TEST 3: TRAIN/TEST-KONSISTENZ p1-p10 vs p11-p16")
    print("=" * 80)
    train_pages = [p for p in p1_16_rep["pages"] if int(p["page_id"][1:]) <= 10]
    test_pages = [p for p in p1_16_rep["pages"] if int(p["page_id"][1:]) > 10]

    # Echte Glyphen-Verteilung pro Seite aus Token-Streams
    import os
    train_glyph_counts = {}
    test_glyph_counts = {}
    for p_num in range(1, 17):
        ts_path = Path(f"bbox/tokenstream_20260706_V6_v3_17glyphs/p{p_num:02d}.json")
        if ts_path.exists():
            p_data = json.load(open(ts_path))
            is_train = p_num <= 10
            for tok in p_data.get("tokens", []):
                gid = tok["glyph_id"]
                if gid == "G25":
                    continue  # Delimiter ignorieren
                if is_train:
                    train_glyph_counts[gid] = train_glyph_counts.get(gid, 0) + 1
                else:
                    test_glyph_counts[gid] = test_glyph_counts.get(gid, 0) + 1

    # Glyphen-Vektoren (gleiche Reihenfolge)
    all_glyphs = sorted(set(list(train_glyph_counts.keys()) + list(test_glyph_counts.keys())))
    train_vec = [train_glyph_counts.get(g, 0) for g in all_glyphs]
    test_vec = [test_glyph_counts.get(g, 0) for g in all_glyphs]

    # Normalisierung
    s_tr = sum(train_vec) or 1
    s_te = sum(test_vec) or 1
    train_n = [v / s_tr for v in train_vec]
    test_n = [v / s_te for v in test_vec]

    consistency = cosine_similarity(train_n, test_n)

    print(f"  Glyphen (Train p1-p10): {len(train_pages)} Seiten")
    print(f"  Glyphen (Test p11-p16):  {len(test_pages)} Seiten")
    print(f"  Cosine-Konsistenz:     {consistency:.4f}")
    print(f"  Schwelle:              > 0.7")
    test3_gestuetzt = consistency > 0.7
    test3_verdict = "GESTÜTZT" if test3_gestuetzt else "FALSIFIZIERT"
    print(f"  → {test3_verdict}")
    print()

    # =========================================================================
    # GESAMT-VERDICT
    # =========================================================================
    print("=" * 80)
    print("GESAMT-VERDICT: PREDICTIVE")
    print("=" * 80)
    n_gestuetzt = sum([test1_gestuetzt, test2_gestuetzt, test3_gestuetzt])
    if n_gestuetzt == 3:
        gesamt_verdict = "GESTÜTZT (3/3): p17-Strukturen sagen p1-16 voraus"
    elif n_gestuetzt >= 2:
        gesamt_verdict = f"TEILWEISE GESTÜTZT ({n_gestuetzt}/3)"
    else:
        gesamt_verdict = f"FALSIFIZIERT ({n_gestuetzt}/3)"
    print(f"  {gesamt_verdict}")
    print()

    out = {
        "metadata": {
            "phase": "V13 / Phase 2",
            "datum": datetime.now().isoformat(),
            "hypothese": "p17-Strukturen → p1-16 Glyph-Frequenz",
            "methode": "Spearman-ρ + Edit-Distanz + Train/Test-Konsistenz",
        },
        "test_1_spearman": {
            "rho": round(rho, 4),
            "p_value": round(p_val, 4),
            "schwelle": 0.5,
            "verdict": test1_verdict,
        },
        "test_2_edit_distance": {
            "akrostichon": akrostichon,
            "top_11_glyphs": top_glyph_ids,
            "top_11_letters": top_as_letters,
            "edit_dist": edit_dist,
            "schwelle": 6,
            "verdict": test2_verdict,
        },
        "test_3_train_test": {
            "n_train_pages": len(train_pages),
            "n_test_pages": len(test_pages),
            "consistency": round(consistency, 4),
            "schwelle": 0.7,
            "verdict": test3_verdict,
        },
        "gesamt_verdict": gesamt_verdict,
        "n_gestuetzt": n_gestuetzt,
        "n_total": 3,
    }
    out_path = OUT_DIR / "predictive_verdict.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"✓ Output: {out_path}")


if __name__ == "__main__":
    main()
