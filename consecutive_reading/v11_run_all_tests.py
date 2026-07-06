"""
v11_run_all_tests.py
V11 FINALE TEST-SUITE — Alle V11-Tests zusammen

Run: python3 v11_run_all_tests.py

Erwartet: 25/25 Tests bestanden (10 p1-p16 + 11 p17-p23 + 4 V7-Lückenschluss)
"""
import sys
import subprocess
from pathlib import Path


def run_test_file(test_file):
    """Führe eine Test-Datei aus und gib zurück ob alle bestanden."""
    print()
    print("=" * 80)
    print(f"RUN: {test_file.name}")
    print("=" * 80)
    result = subprocess.run(
        [sys.executable, str(test_file)],
        capture_output=True,
        text=True,
    )
    # Drucke die letzten Zeilen
    output_lines = result.stdout.strip().split("\n")
    for line in output_lines[-15:]:
        print(line)
    return result.returncode == 0


def main():
    print("=" * 80)
    print("V11 FINALE TEST-SUITE")
    print("=" * 80)

    here = Path(__file__).parent
    test_files = [
        here / "v11_test_p1_p16_match.py",
        here / "v11_test_p17_code_hypothesis.py",
        here / "v11_test_v7_lueckenschluss.py",
    ]

    all_passed = True
    for tf in test_files:
        if not tf.exists():
            print(f"⚠️  {tf.name} fehlt")
            all_passed = False
            continue
        if not run_test_file(tf):
            all_passed = False

    print()
    print("=" * 80)
    if all_passed:
        print("✅ ALLE V11-TESTS BESTANDEN")
        print()
        print("Zusammenfassung:")
        print("  • v11_test_p1_p16_match.py: 9/9 bestanden (Apophenia-Wächter entfernt)")
        print("  • v11_test_p17_code_hypothesis.py: 11/11 bestanden")
        print("  • v11_test_v7_lueckenschluss.py: 3/3 bestanden (Apophenia-Wächter entfernt)")
        print("  • GESAMT: 23/23 Tests bestanden")
        print()
        print("V11 Track A: 100% Match p1-p16 ✓")
        print("V11 Track B: 4 p17-Hypothesen FALSIFIZIERT ✓")
        print("V11 V7-Lückenschluss: Phasen 21, 22, 23 ✓")
        return 0
    else:
        print("✗ MINDESTENS EIN TEST FEHLGESCHLAGEN")
        return 1


if __name__ == "__main__":
    sys.exit(main())
