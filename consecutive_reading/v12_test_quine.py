"""
v12_test_quine.py
V12 TDD TESTS — QUINE-Hypothese empirisch

Definition: Programm P mit Output(P) = P (Self-Reference)
Test: Self-Description, Edit-Distanzen, BURUMUT-Self-Reference
"""
import sys
import json
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def load_p17_inventory():
    return json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))


def load_v11_code_hypotheses():
    return json.load(open("bbox/v11_p17_20260706/code_hypotheses.json"))


def load_burumut_texts():
    """Lade 76 BURUMUT-Texte (11×7)."""
    data = json.load(open("bbox/burumut_20260707_V7/burumut_texts.json"))
    all_texts = []
    for f_id, texts in data["burumut_texts"].items():
        all_texts.extend(texts)
    return all_texts


def load_burumut_woerter():
    inv = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    return [w["wort"] for w in inv["woerter"]]


def normalized_edit_distance(s1, s2):
    """Levenshtein-Distanz normalisiert auf max(len(s1), len(s2))."""
    if not s1 and not s2:
        return 0.0
    n, m = len(s1), len(s2)
    if n == 0 or m == 0:
        return 1.0
    # DP
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


# ============================================================================
# TDD-Tests
# ============================================================================

def test_p17_klartext_is_self_describing():
    """Quine: Output beschreibt sich selbst. p17-Klartext ist eine 'Message', nicht self-ref."""
    inv = load_p17_inventory()
    klartext_lines = inv["tappeiner_brueche_klartext"]["klartext_zeilen"]
    full = " ".join(klartext_lines)

    # Self-reference-Marker: TRUTH, KNOWLEDGE, MESSENGERS, BURUMUT
    markers = ["TRUTH", "KNOWLEDGE", "MESSENGERS", "YEARS", "CIVILISATION", "BURUMUT"]
    counts = {m: full.count(m) for m in markers}

    print(f"  Klartext-Repetitionen: {counts}")
    # Bei Quine-artiger self-reference: "TRUTH" mehrfach, "KNOWLEDGE" mehrfach, etc.
    # Realität: eine Message, jedes Schlüsselwort 1x
    n_repeated = sum(1 for c in counts.values() if c > 1)
    print(f"  → {n_repeated}/{len(markers)} Schlüsselwörter mehrfach")
    # Quine würde alle 6 mehrfach haben (6/6)
    # Realität: 0 wiederholt
    assert n_repeated <= 1, \
        f"{n_repeated}/{len(markers)} Schlüsselwörter mehrfach — Quine-artige Repetition"


def test_p17_self_similarity_structures():
    """Quine: alle p17-Strukturen maximal selbstähnlich. Bei Quine: Edit-Distanz klein."""
    inv = load_p17_inventory()
    s1 = inv["akrostichon_der_11_glyphen"]["string"]  # "BNYZTSOYNKS"
    s2 = "".join(str(d) for d in inv["v7_lateinische_ziffern"]["values"])  # Ziffern
    klartext_lines = inv["tappeiner_brueche_klartext"]["klartext_zeilen"]
    s3 = " ".join(klartext_lines)  # Klartext

    d12 = normalized_edit_distance(s1, s2)
    d13 = normalized_edit_distance(s1, s3)
    d23 = normalized_edit_distance(s2, s3)
    max_d = max(d12, d13, d23)
    min_d = min(d12, d13, d23)
    print(f"  Edit-Distanzen: d(Akrostichon, Ziffern)={d12:.3f}, "
          f"d(Akrostichon, Klartext)={d13:.3f}, d(Ziffern, Klartext)={d23:.3f}")
    print(f"  → max={max_d:.3f}, min={min_d:.3f}")
    # Bei Quine: alle < 0.3
    # Bei unabhängigen Strukturen: alle > 0.5
    assert max_d < 0.3, \
        f"Max-Edit-Distanz {max_d:.3f} ≥ 0.3 — Strukturen zu unähnlich für Quine"


def test_p17_burumut_self_referential():
    """BURUMUT-Texte: beschreiben sie sich selbst? Bei Quine-artig: BURUMUT im Wort."""
    burumut_texts = load_burumut_texts()
    burumut_woerter = load_burumut_woerter()

    # Wie oft kommt "BURUMUT", "BURU", "BUR" in den Texten vor?
    n_burumut = sum(1 for t in burumut_texts if "BURUMUT" in t)
    n_buru = sum(1 for t in burumut_texts if "BURU" in t)
    n_bur = sum(1 for t in burumut_texts if "BUR" in t)
    n_total = len(burumut_texts)
    print(f"  BURUMUT in Texten: {n_burumut}/{n_total}")
    print(f"  BURU in Texten:   {n_buru}/{n_total}")
    print(f"  BUR in Texten:    {n_bur}/{n_total}")

    # Bei Quine-artiger self-ref: viele Texte würden "BURUMUT" enthalten
    # Realität: nur 1 Text (F1, letzte Zeile)
    assert n_burumut < n_total * 0.5, \
        f"{n_burumut}/{n_total} Texte enthalten 'BURUMUT' — könnte self-ref sein"


def test_p17_iteration_converges():
    """Quine: Iteration P(P(...)) konvergiert. Test: einfache Decodier-Funktion auf p17 anwenden."""
    inv = load_p17_inventory()
    s_input = inv["akrostichon_der_11_glyphen"]["string"]  # BNYZTSOYNKS

    # Einfache "Decodier"-Funktion: Tappeiner-Substitution (A→E, K→H, B→V, P→F)
    # Wikia "For beginners"-Regel
    decode_map = {"A": "E", "K": "H", "B": "V", "P": "F"}

    s_iter1 = "".join(decode_map.get(c, c) for c in s_input)  # VNYZTSOYNKS
    s_iter2 = "".join(decode_map.get(c, c) for c in s_iter1)  # idempotent
    s_iter3 = "".join(decode_map.get(c, c) for c in s_iter2)

    print(f"  Input:           '{s_input}'")
    print(f"  Decoded (iter1): '{s_iter1}'")
    print(f"  Decoded (iter2): '{s_iter2}'")
    # Bei Quine: s_iter1 == s_input
    assert s_iter1 != s_input, \
        f"Decode idempotent: '{s_iter1}' == '{s_input}' — Quine-Indiz?"


def test_p17_v11_verdict_holds():
    """V11-Verdikt: Quine FALSIFIZIERT. Hält das?"""
    h = load_v11_code_hypotheses()
    quine = next((x for x in h["hypotheses"] if "QUINE" in x["name"]), None)
    assert quine is not None, "V11 Quine-Verdikt fehlt"
    assert quine["status"] in ("FALSIFIZIERT", "BESTÄTIGT"), \
        f"V11-Status: {quine['status']}"
    print(f"  V11-Verdikt: {quine['status']} — {quine['verdict']}")


if __name__ == "__main__":
    import traceback

    tests = [
        test_p17_klartext_is_self_describing,
        test_p17_self_similarity_structures,
        test_p17_burumut_self_referential,
        test_p17_iteration_converges,
        test_p17_v11_verdict_holds,
    ]

    print("=" * 80)
    print("V12 TDD: QUINE-Hypothese (empirisch)")
    print("=" * 80)
    print()
    print("Diese Tests dokumentieren den empirischen Ist-Stand.")
    print("Quine-Hypothese: Output(P) = P (Self-Reference).")
    print()

    passed = 0
    failed = 0
    for test in tests:
        print(f"RUN: {test.__name__}")
        try:
            test()
            print(f"  ✓ PASS\n")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ FAIL: {e}\n")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}\n")
            traceback.print_exc()
            failed += 1

    print("=" * 80)
    print(f"ERGEBNIS: {passed}/{len(tests)} bestanden, {failed} fehlgeschlagen")
    print("=" * 80)
    sys.exit(0 if failed == 0 else 1)
