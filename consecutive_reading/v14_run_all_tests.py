"""
v14_run_all_tests.py
V14 FINALE TEST-SUITE — Alle V14-Tests zusammen

Run: python3 v14_run_all_tests.py
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
    # Print full output for shorter tests, tail for longer
    for line in output_lines[-12:]:
        print(line)
    return result.returncode == 0, result.stdout


def main():
    print("=" * 80)
    print("V14 FINALE TEST-SUITE — 8 informationstheoretische Konstrukte")
    print("=" * 80)
    print()
    print("Konsultation: CryptanalysisMind + DevMind + ITAnalyserMind + PhiMind")
    print()
    print("Konstrukte:")
    print("  1. Kolmogorov Multi-Kompressor (gzip/bz2/lzma/zstd)")
    print("  2. Shannon-Heatmap (5 Schichten, paarweise MI)")
    print("  3. Zipf-Mandelbrot-Exponent (6 Schichten)")
    print("  4. Markov-KL (Ordnungen 1/2, asymmetrisch)")
    print("  5. Source-Coding (Huffman + LZW)")
    print("  6. n-gram-Überlappung (Sampling, n=2/3/4)")
    print("  7. Turing-Maschine OFFEN (11/64 Zustände, Counter/Tag)")
    print("  8. Kompilat/Quine OFFEN (1:n, n:m, semantischer Quine)")
    print()

    here = Path(__file__).parent
    test_files = [
        here / "v14_test_kolmogorov_multi.py",
        here / "v14_test_shannon_heatmap.py",
        here / "v14_test_zipf_mandelbrot.py",
        here / "v14_test_markov_kl.py",
        here / "v14_test_source_coding.py",
        here / "v14_test_ngram_overlap.py",
        here / "v14_test_turing_offener.py",
        here / "v14_test_kompilat_quine_offener.py",
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
        print("✅ ALLE V14-TESTS BESTANDEN")
    else:
        print("ℹ️  TDD-Disziplin: Einige Tests dokumentieren Befunde (FAIL ≠ Fehler).")
        print("   Tests schlagen fehl, wenn die Hypothese FALSIFIZIERT ist — das ist gewollt.")
    print("=" * 80)
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
