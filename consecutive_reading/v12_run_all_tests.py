"""
v12_run_all_tests.py
V12 FINALE TEST-SUITE — Alle V12-Tests zusammen

Run: python3 v12_run_all_tests.py

Erwartet: 20/20 Tests bestanden (4 Kompilat + 5 Quine + 6 Turing + 5 Bewusst)
Hinweis: Einige Tests MÜSSEN fehlschlagen, wenn die Hypothese FALSIFIZIERT ist
(das ist TDD-Disziplin: Tests dokumentieren die empirische Realität, nicht Wunschdenken).
"""
import sys
import subprocess
from pathlib import Path


def run_test_file(test_file):
    """Führe eine Test-Datei aus."""
    print()
    print("=" * 80)
    print(f"RUN: {test_file.name}")
    print("=" * 80)
    result = subprocess.run(
        [sys.executable, str(test_file)],
        capture_output=True,
        text=True,
    )
    output_lines = result.stdout.strip().split("\n")
    for line in output_lines[-20:]:
        print(line)
    return result.returncode == 0, result.stdout


def main():
    print("=" * 80)
    print("V12 FINALE TEST-SUITE")
    print("=" * 80)
    print()
    print("4 Hypothesen empirisch getestet:")
    print("  1. KOM PIL AT — Source ↔ Binary 1:1")
    print("  2. QUINE — Output(P) = P")
    print("  3. TURING-MASCHINE — FSM, Turing-vollständig")
    print("  4. BEWUSSTER CODE — intentionale Semantik (statistische Signaturen)")
    print()

    here = Path(__file__).parent
    test_files = [
        here / "v12_test_kompilat.py",
        here / "v12_test_quine.py",
        here / "v12_test_turing.py",
        here / "v12_test_bewusst.py",
    ]

    all_passed = True
    for tf in test_files:
        if not tf.exists():
            print(f"⚠️  {tf.name} fehlt")
            all_passed = False
            continue
        passed, output = run_test_file(tf)
        if not passed:
            all_passed = False

    print()
    print("=" * 80)
    if all_passed:
        print("✅ ALLE V12-TESTS BESTANDEN")
    else:
        print("ℹ️  TDD-Disziplin: Einige Tests schlagen fehl, wenn die Hypothese FALSIFIZIERT ist.")
        print("   Das ist gewollt — Tests dokumentieren die empirische Realität.")
    print("=" * 80)
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
