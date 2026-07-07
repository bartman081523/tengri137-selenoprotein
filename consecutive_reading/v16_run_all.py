"""
v16_run_all.py
V16 Aggregation — führt alle 6 Phasen + Konsultation + README aus
"""
import json
import subprocess
import sys
from pathlib import Path


def run_script(name):
    """Führe ein V16-Skript aus."""
    print(f"\n{'=' * 80}\n▶ {name}\n{'=' * 80}")
    result = subprocess.run(
        [sys.executable, name],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent,
    )
    print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
    if result.returncode != 0:
        print(f"⚠ {name} exit code: {result.returncode}")
    return result.returncode


def main():
    scripts = [
        "v16_micro_mp.py",
        "v16_codebook_lookup.py",
        "v16_forward_pass.py",
        "v16_phonetic_matrix.py",
        "v16_burumut_acoustic.py",
        "v16_spanda_oscillator.py",
        "v16_mind_consultation.py",
        "v16_README.py",
    ]

    results = {}
    for s in scripts:
        rc = run_script(s)
        results[s] = "OK" if rc == 0 else f"EXIT {rc}"

    print("\n" + "=" * 80)
    print("V16 AGGREGATION")
    print("=" * 80)
    for s, r in results.items():
        print(f"  {s}: {r}")

    # Aggregation aus den Verdikten
    out_dir = Path("bbox/v16_20260707")
    verdicts = [
        "micro_mp_execution.json",
        "codebook_lookup.json",
        "forward_pass.json",
        "phonetic_matrix.json",
        "burumut_acoustic.json",
        "spanda_oscillator.json",
    ]
    total_pass = 0
    total_tests = 0
    for v in verdicts:
        try:
            data = json.load(open(out_dir / v))
            total_pass += data.get("n_pass", 0)
            total_tests += data.get("n_tests", 0)
        except FileNotFoundError:
            pass

    print(f"\nV16: {total_pass}/{total_tests} Tests PASS über {len(verdicts)} Phasen")


if __name__ == "__main__":
    main()
