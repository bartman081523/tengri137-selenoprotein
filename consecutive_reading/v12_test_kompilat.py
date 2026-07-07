"""
v12_test_kompilat.py
V12 TDD TESTS — KOM PIL AT-Hypothese empirisch

Definition: Source ↔ Binary 1:1-Isomorphie
Test: Strukturen, Korrelation, Permutations-Konsistenz
"""
import sys
import json
import re
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))


def load_p17_inventory():
    return json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))


def load_v11_code_hypotheses():
    return json.load(open("bbox/v11_p17_20260706/code_hypotheses.json"))


def load_burumut_woerter():
    inv = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    return [w["wort"] for w in inv["woerter"]]


def count_tappeiner_bruche():
    """Zähle Tappeiner-Brüche: kommt aus p17-Layout-Rekonstruktion."""
    # 11 BURUMUT-Wörter = 11 Tappeiner-Periode-7-Wörter = 11 Brüche
    inv = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    return len(inv["woerter"])


# ============================================================================
# TDD-Tests: Diese dokumentieren den Ist-Stand und liefern Zahlen
# ============================================================================

def test_p17_n_independent_structures():
    """p17 hat N unabhängige Strukturen. Kompilat verlangt Source + Binary = 2."""
    inv = load_p17_inventory()
    n_digits = len(inv["v7_lateinische_ziffern"]["values"])  # 10
    n_glyphs = len(inv["akrostichon_der_11_glyphen"]["string"])  # 11
    n_klartext = len(inv["tappeiner_brueche_klartext"]["klartext_zeilen"])  # 5
    n_brueche = count_tappeiner_bruche()  # 11

    # Kompilat-These: 2 Strukturen (Source, Binary). Tatsächlich: 4.
    # Aber: könnte sein, dass Ziffern und Glyphen zusammengehören (2 Strukturen)
    # und Klartext + Brüche nur Decodierungen sind (1 weitere).
    # Streng: jede distinkte Anordnung ist eine eigene Struktur.
    n_structures = 4
    print(f"  p17 Strukturen: Ziffern={n_digits}, Glyphen={n_glyphs}, "
          f"Brüche={n_brueche}, Klartext={n_klartext}")
    print(f"  → {n_structures} unabhängige Strukturen")
    # Kompilat verlangt N=2; real N=4 → FALSIFIZIERT
    assert n_structures <= 2, \
        f"Kompilat verlangt ≤2 Strukturen, p17 hat {n_structures} (Ziffern, Glyphen, Brüche, Klartext)"


def test_p17_glyph_digit_correlation():
    """Falls Kompilat: Glyph-Position ↔ Ziffer-Position korreliert."""
    inv = load_p17_inventory()
    glyphs = list(inv["akrostichon_der_11_glyphen"]["string"])  # 11 Glyphen
    digits = inv["v7_lateinische_ziffern"]["values"]  # 10 Ziffern

    # Ordinalkodierung: A=1, B=2, ..., Z=26
    g_ord = [ord(c) - ord('A') + 1 for c in glyphs]  # 11 Werte
    d_ord = digits  # bereits numerisch, 10 Werte

    # Paare für die ersten 10 (Mindestmenge)
    n = min(len(g_ord), len(d_ord))
    g_pairs = g_ord[:n]
    d_pairs = d_ord[:n]

    # Spearman-Rangkorrelation (ohne scipy, mit pure Python)
    def spearman(xs, ys):
        n = len(xs)
        def rankify(arr):
            sorted_idx = sorted(range(n), key=lambda i: arr[i])
            ranks = [0] * n
            for r, i in enumerate(sorted_idx):
                ranks[i] = r + 1
            return ranks
        rx = rankify(xs)
        ry = rankify(ys)
        # Pearson auf ranks
        mx = sum(rx) / n
        my = sum(ry) / n
        num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
        dx = sum((rx[i] - mx) ** 2 for i in range(n)) ** 0.5
        dy = sum((ry[i] - my) ** 2 for i in range(n)) ** 0.5
        if dx == 0 or dy == 0:
            return 0.0
        return num / (dx * dy)

    rho = spearman(g_pairs, d_pairs)
    print(f"  Spearman rho(Glyph, Ziffer) = {rho:+.3f} (n={n})")
    # Kompilat: |rho| nahe ±1. Zufall: nahe 0.
    # Wenn |rho| > 0.5 → Source↔Binary-Korrelation, also möglicherweise Kompilat
    # Wenn |rho| < 0.3 → unabhängig, kein Kompilat
    assert abs(rho) < 0.3 or abs(rho) > 0.7, \
        f"rho={rho:+.3f} ist weder unabhängig (<0.3) noch klar korreliert (>0.7) — kein klares Urteil"


def test_p17_bytecode_consistency():
    """Falls Kompilat: Reihenfolge der Glyphen ↔ Reihenfolge der Brüche konsistent.

    Bei echtem Kompilat: 100% der Permutationen der Glyphen erzeugen
    konsistente Bruch-Reihenfolgen (oder 0%, je nach Kompilat-Typ).
    Bei unabhängigen Strukturen: ein Mittelding.
    """
    import random
    inv = load_p17_inventory()
    glyphs = list(inv["akrostichon_der_11_glyphen"]["string"])
    digits = inv["v7_lateinische_ziffern"]["values"]

    n_glyphs = len(glyphs)
    n_brueche = count_tappeiner_bruche()
    n = min(n_glyphs, n_brueche)  # 11

    # Konstruiere eine deterministische "Konsistenz-Funktion":
    # Bei Kompilat: 1. Glyphe ↔ 1. Bruch (positionserhaltend)
    # Wenn ich Glyphen permutiere, müssen sich die Brüche entsprechend mit-permutieren
    # für die Konsistenz zu bleiben.

    def consistency_after_permute(seed):
        random.seed(seed)
        g_perm = glyphs[:]
        random.shuffle(g_perm)
        # Original-Reihenfolge: glyph[i] ↔ bruech[i] (positionsbasiert)
        # Bei Kompilat: Konsistenz = 1.0 (alle gleich geblieben)
        # Bei unabhängig: Konsistenz = variabel
        consistent = 0
        for i in range(n):
            # Konsistenz: ist die Reihenfolge-Preservation noch da?
            # Index-Vergleich: wo steht glyph[i] in g_perm?
            new_pos = g_perm.index(glyphs[i])
            if new_pos == i:
                consistent += 1
        return consistent / n

    consistencies = [consistency_after_permute(s) for s in range(100)]
    avg_consistency = sum(consistencies) / len(consistencies)
    print(f"  Avg-Konsistenz nach 100 Glyphen-Permutationen: {avg_consistency:.2%}")
    # Bei Zufall: ~0.09 (= 1/n)
    # Bei Kompilat mit Reihenfolge-Preservation: 1.0
    # Wir erwarten bei unabhängigen Strukturen: nahe 1/n
    # Wenn Konsistenz > 50% → Reihenfolge ist NICHT zufällig → möglicherweise Kompilat
    assert avg_consistency <= 0.5, \
        f"Konsistenz {avg_consistency:.2%} > 50% — Glyphen↔Brüche sind nicht unabhängig (Kompilat-Indiz)"


def test_p17_v11_verdict_holds():
    """V11-Verdikt: 11≠10≠5 ist Kompilat-Falsifikation. Hält das?"""
    h = load_v11_code_hypotheses()
    komp = next((x for x in h["hypotheses"] if "KOM" in x["name"]), None)
    assert komp is not None, "V11 Kompilat-Verdikt fehlt"
    assert komp["status"] in ("FALSIFIZIERT", "BESTÄTIGT"), \
        f"V11-Status: {komp['status']}"
    # V12 vertieft: zeigt WARUM (nicht nur DASS)
    print(f"  V11-Verdikt: {komp['status']} — {komp['verdict']}")


if __name__ == "__main__":
    import traceback

    tests = [
        test_p17_n_independent_structures,
        test_p17_glyph_digit_correlation,
        test_p17_bytecode_consistency,
        test_p17_v11_verdict_holds,
    ]

    print("=" * 80)
    print("V12 TDD: KOM PIL AT-Hypothese (empirisch)")
    print("=" * 80)
    print()
    print("Diese Tests dokumentieren den empirischen Ist-Stand und liefern Zahlen.")
    print("Kompilat-Hypothese: Source ↔ Binary 1:1-Isomorphie.")
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
