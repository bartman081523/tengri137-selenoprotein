"""
v13_run_all_tests.py
V13 FINALE TEST-SUITE — Alle V13-Tests zusammen

Run: python3 v13_run_all_tests.py
"""
import sys
import subprocess
from pathlib import Path


def run_test_file(test_file):
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
    for line in output_lines[-12:]:
        print(line)
    return result.returncode == 0, result.stdout


def main():
    print("=" * 80)
    print("V13 FINALE TEST-SUITE — 'p17-23 erzeugt p1-p16' Hypothese")
    print("=" * 80)
    print()
    print("4 Test-Richtungen:")
    print("  1. INFORMATIONSTHEORIE: p17-23 = komprimierte Source?")
    print("  2. PREDICTIVE: p17-Strukturen → p1-16 Glyph-Frequenz?")
    print("  3. GENERATIVE: F: p17-23 → p1-16 (deterministisch)?")
    print("  4. SEQUENZ/FALTUNG: p1-p16 = p17-23 ⊛ Kernel?")
    print()

    here = Path(__file__).parent
    test_files = [
        here / "v13_test_information_theory.py",
        here / "v13_test_predictive.py",
        here / "v13_test_generative.py",
        here / "v13_test_sequenz_faltung.py",
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
        print("✅ ALLE V13-TESTS BESTANDEN (12/12)")
    else:
        print("ℹ️  TDD-Disziplin: Einige Tests schlagen fehl, wenn die Hypothese FALSIFIZIERT ist.")
        print("   Das ist gewollt — Tests dokumentieren die empirische Realität.")
    print("=" * 80)
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
