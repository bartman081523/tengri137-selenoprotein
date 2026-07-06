"""
v11_test_v7_lueckenschluss.py
V11 TDD TESTS — V7 Phase 21, 22, 23 (Lückenschluss)

DIESE TESTS VALIDIEREN die empirische V7-Lückenschluss.
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def test_phase_21_p17_ocr():
    """V7 Phase 21: p17 OCR-Ground-Truth (10 Ziffern + 11 Glyphen)."""
    out = Path("bbox/v11_v7_lueckenschluss_20260706/v7_lueckenschluss.json")
    assert out.exists(), "V7-Lückenschluss muss existieren"
    data = json.load(open(out))
    p21 = data["phase_21_p17_ocr"]
    assert p21["status"] == "BESTÄTIGT", f"Phase 21 Status: {p21['status']}"
    assert p21["v11_verifikation"]["n_ziffern"] == 10, "10 lateinische Ziffern erwartet"
    assert p21["v11_verifikation"]["n_glyphen"] == 11, "11 Tengri-Glyphen erwartet"


def test_phase_22_caesar_shift():
    """V7 Phase 22: Caesar-Shift BNYZTSOYNKS — 0/26 ergeben Englisch."""
    out = Path("bbox/v11_v7_lueckenschluss_20260706/v7_lueckenschluss.json")
    assert out.exists()
    data = json.load(open(out))
    p22 = data["phase_22_caesar_shift"]
    # 26 Caesar-Shifts getestet
    assert p22["v11_verifikation"]["n_shifts_tested"] == 26
    # Kein Shift ergibt ein echtes englisches Wort (≥ 4 Zeichen)
    best = p22["v11_verifikation"]["best_english_word"]
    assert best is None or len(best) < 4, \
        f"Best Shift gibt '{best}', aber sollte < 4 Zeichen sein"


def test_phase_23_burumut_constraint():
    """V7 Phase 23: 11/11 BURUMUT-Wörter haben 7 Dinome, L1-These FALSIFIZIERT."""
    out = Path("bbox/v11_v7_lueckenschluss_20260706/v7_lueckenschluss.json")
    assert out.exists()
    data = json.load(open(out))
    p23 = data["phase_23_burumut_constraint"]
    assert p23["status"] == "BESTÄTIGT", f"Phase 23 Status: {p23['status']}"
    # 11/11 Wörter haben 7 Dinome
    assert p23["v11_verifikation"]["n_periode_7_match"] == 11, \
        f"Erwartet 11/11, gefunden {p23['v11_verifikation']['n_periode_7_match']}/11"
    # L1-These: 0/11 BURUMUT-Wörter sind 7-Zeichen-Englisch
    assert p23["v11_verifikation"]["l1_these_match"] == 0, \
        "L1-These sollte FALSIFIZIERT sein"


if __name__ == "__main__":
    import traceback

    tests = [
        test_phase_21_p17_ocr,
        test_phase_22_caesar_shift,
        test_phase_23_burumut_constraint,
    ]

    print("=" * 80)
    print("V11 TDD: V7-Lückenschluss (Phase 21-23)")
    print("=" * 80)
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
