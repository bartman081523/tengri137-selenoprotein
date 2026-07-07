"""
v12_quine_analysis.py
V12 PHASE 2 — QUINE-Hypothese empirisch testen

Methode:
1. Self-Description-Test: Klartext-Repetitionen
2. Edit-Distanzen zwischen p17-Strukturen
3. BURUMUT-Self-Reference (76 Texte)
4. Iterations-Test (Decode-Konvergenz)

Output: bbox/v12_quine_20260707/quine_verdict.json
"""
import json
from pathlib import Path
from datetime import datetime

OUT_DIR = Path("bbox/v12_quine_20260707")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def normalized_edit_distance(s1, s2):
    """Levenshtein-Distanz normalisiert."""
    if not s1 and not s2:
        return 0.0
    n, m = len(s1), len(s2)
    if n == 0 or m == 0:
        return 1.0
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[n][m] / max(n, m)


def main():
    print("=" * 80)
    print("V12 QUINE-ANALYSE: EMPIRISCHE TESTS")
    print("=" * 80)

    p17_inv = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    burumut_data = json.load(open("bbox/burumut_20260707_V7/burumut_texts.json"))
    p23_inv = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))

    klartext_lines = p17_inv["tappeiner_brueche_klartext"]["klartext_zeilen"]
    full_klartext = " ".join(klartext_lines)

    # =========================================================================
    # TEST 1: Self-Description-Test
    # =========================================================================
    print("\n" + "=" * 80)
    print("TEST 1: SELF-DESCRIPTION-TEST")
    print("=" * 80)
    markers = ["TRUTH", "KNOWLEDGE", "MESSENGERS", "YEARS", "CIVILISATION", "BURUMUT", "TRUTHS", "KNOWLEDGES"]
    counts = {m: full_klartext.count(m) for m in markers}
    n_repeated = sum(1 for c in counts.values() if c > 1)
    print(f"  Klartext-Repetitionen:")
    for m, c in counts.items():
        print(f"    {m:14}: {c}x")
    print(f"  → {n_repeated}/{len(markers)} Schlüsselwörter mehrfach vorhanden")
    if n_repeated == 0:
        verdict_self = "Message-Struktur (keine Repetition) — kein Quine"
    elif n_repeated < 3:
        verdict_self = "Wenig Repetition — kein klares Quine-Indiz"
    else:
        verdict_self = "Starke Repetition — Quine-Indiz"
    print(f"  → {verdict_self}")

    # =========================================================================
    # TEST 2: Edit-Distanzen zwischen p17-Strukturen
    # =========================================================================
    print("\n" + "=" * 80)
    print("TEST 2: EDIT-DISTANZEN ZWISCHEN P17-STRUKTUREN")
    print("=" * 80)
    s_glyphs = p17_inv["akrostichon_der_11_glyphen"]["string"]  # BNYZTSOYNKS
    s_digits = "".join(str(d) for d in p17_inv["v7_lateinische_ziffern"]["values"])
    s_klartext = full_klartext

    d12 = normalized_edit_distance(s_glyphs, s_digits)
    d13 = normalized_edit_distance(s_glyphs, s_klartext)
    d23 = normalized_edit_distance(s_digits, s_klartext)
    max_d = max(d12, d13, d23)
    min_d = min(d12, d13, d23)
    print(f"  d(Akrostichon='{s_glyphs}', Ziffern='{s_digits[:20]}...')  = {d12:.3f}")
    print(f"  d(Akrostichon, Klartext)  = {d13:.3f}")
    print(f"  d(Ziffern, Klartext)      = {d23:.3f}")
    print(f"  Max: {max_d:.3f}, Min: {min_d:.3f}")
    if max_d < 0.3:
        verdict_edit = "Strukturen maximal ähnlich — Quine-Indiz"
    elif max_d < 0.6:
        verdict_edit = "Strukturen teils ähnlich"
    else:
        verdict_edit = "Strukturen maximal unähnlich — kein Quine"
    print(f"  → {verdict_edit}")

    # =========================================================================
    # TEST 3: BURUMUT-Self-Reference
    # =========================================================================
    print("\n" + "=" * 80)
    print("TEST 3: BURUMUT-SELF-REFERENCE (76 TEXTE)")
    print("=" * 80)
    all_texts = []
    for f_id, texts in burumut_data["burumut_texts"].items():
        all_texts.extend(texts)
    n_burumut = sum(1 for t in all_texts if "BURUMUT" in t)
    n_buru = sum(1 for t in all_texts if "BURU" in t)
    n_bur = sum(1 for t in all_texts if "BUR" in t)
    n_total = len(all_texts)
    pct_burumut = n_burumut / n_total
    pct_buru = n_buru / n_total
    print(f"  Texte gesamt: {n_total}")
    print(f"  Mit 'BURUMUT':  {n_burumut}/{n_total} = {pct_burumut:.2%}")
    print(f"  Mit 'BURU':     {n_buru}/{n_total} = {pct_buru:.2%}")
    print(f"  Mit 'BUR':      {n_bur}/{n_total} = {n_bur/n_total:.2%}")
    if pct_burumut > 0.5:
        verdict_buru = "Starke Self-Reference — Quine-Indiz"
    elif pct_burumut > 0.1:
        verdict_buru = "Moderate Self-Reference"
    else:
        verdict_buru = "Minimal Self-Reference — kein Quine"
    print(f"  → {verdict_buru}")

    # =========================================================================
    # TEST 4: Iterations-Konvergenz
    # =========================================================================
    print("\n" + "=" * 80)
    print("TEST 4: ITERATIONS-KONVERGENZ")
    print("=" * 80)
    decode_map = {"A": "E", "K": "H", "B": "V", "P": "F"}
    s_input = s_glyphs
    s_iter1 = "".join(decode_map.get(c, c) for c in s_input)
    s_iter2 = "".join(decode_map.get(c, c) for c in s_iter1)
    s_iter3 = "".join(decode_map.get(c, c) for c in s_iter2)
    print(f"  Input:           '{s_input}'")
    print(f"  Decoded (iter1): '{s_iter1}'")
    print(f"  Decoded (iter2): '{s_iter2}' (Fixpunkt)")
    converges = s_iter1 == s_input
    print(f"  Konvergiert zu sich selbst: {converges}")
    if converges:
        verdict_iter = "Decode konvergiert sofort — Quine-Indiz"
    else:
        verdict_iter = "Decode konvergiert nicht — kein Quine"
    print(f"  → {verdict_iter}")

    # =========================================================================
    # GESAMT-VERDICT
    # =========================================================================
    print("\n" + "=" * 80)
    print("GESAMT-VERDICT QUINE-HYPOTHESE")
    print("=" * 80)

    # Quine wäre plausibel wenn:
    # - Mehrere Repetitionen (n_repeated >= 3)
    # - Strukturen ähnlich (max_d < 0.3)
    # - BURUMUT self-referentiell (pct_burumut > 0.5)
    # - Decode konvergiert
    is_quine = (n_repeated >= 3) and (max_d < 0.3) and (pct_burumut > 0.5) and converges
    if is_quine:
        verdict = "BESTÄTIGT"
    else:
        reasons = []
        if n_repeated < 3:
            reasons.append(f"n_repeated={n_repeated} (<3)")
        if max_d >= 0.3:
            reasons.append(f"max_d={max_d:.3f} (≥0.3)")
        if pct_burumut <= 0.5:
            reasons.append(f"pct_burumut={pct_burumut:.2%} (≤50%)")
        if not converges:
            reasons.append("Decode konvergiert nicht")
        verdict = f"FALSIFIZIERT (Gründe: {', '.join(reasons)})"
    print(f"  Status: {verdict}")

    # Speichern
    out = {
        "metadata": {
            "phase": "V12 / Phase 2",
            "datum": datetime.now().isoformat(),
            "hypothese": "QUINE (Output(P) = P)",
            "methode": "Self-Description + Edit-Distanz + Self-Reference + Iterations-Konvergenz",
        },
        "test_1_self_description": {
            "n_repeated": n_repeated,
            "n_markers": len(markers),
            "verdict": verdict_self,
            "details": counts,
        },
        "test_2_edit_distance": {
            "d_glyph_digits": round(d12, 4),
            "d_glyph_klartext": round(d13, 4),
            "d_digits_klartext": round(d23, 4),
            "max_d": round(max_d, 4),
            "min_d": round(min_d, 4),
            "verdict": verdict_edit,
        },
        "test_3_burumut_self_ref": {
            "n_texts": n_total,
            "n_burumut": n_burumut,
            "n_buru": n_buru,
            "n_bur": n_bur,
            "pct_burumut": round(pct_burumut, 4),
            "verdict": verdict_buru,
        },
        "test_4_iteration": {
            "input": s_input,
            "iter1": s_iter1,
            "iter2": s_iter2,
            "converges_to_self": converges,
            "verdict": verdict_iter,
        },
        "gesamt_verdict": verdict,
        "v11_vergleich": {
            "status": "FALSIFIZIERT",
            "v11_verdict": "Output ≠ Input, keine Self-Reference",
            "v12_vertiefung": f"V12 liefert: n_repeated={n_repeated}, max_d={max_d:.3f}, pct_burumut={pct_burumut:.2%}",
        }
    }
    out_path = OUT_DIR / "quine_verdict.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Output: {out_path}")


if __name__ == "__main__":
    main()
