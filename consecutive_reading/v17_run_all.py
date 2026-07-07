"""
v17_run_all.py
V17 Aggregation — führt alle 3 Phasen + Konsultation aus
"""
import json
import subprocess
import sys
from pathlib import Path


def run_script(name):
    """Führe ein V17-Skript aus."""
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
        "v17_synthesize_burumut.py",
        "v17_analyze_mp3.py",
        "v17_compare_audio.py",
        "v17_mind_consultation.py",
    ]
    results = {}
    for s in scripts:
        rc = run_script(s)
        results[s] = "OK" if rc == 0 else f"EXIT {rc}"

    print("\n" + "=" * 80)
    print("V17 AGGREGATION")
    print("=" * 80)
    for s, r in results.items():
        print(f"  {s}: {r}")

    # Aggregation
    out_dir = Path("bbox/v17_20260707")
    verdicts = ["synthese.json", "mp3_analyse.json", "vergleich.json"]
    total_pass = 0
    total_tests = 0
    for v in verdicts:
        try:
            data = json.load(open(out_dir / v))
            total_pass += data.get("n_pass", 0)
            total_tests += data.get("n_tests", 0)
        except FileNotFoundError:
            pass

    print(f"\nV17: {total_pass}/{total_tests} Tests PASS über {len(verdicts)} Phasen")


if __name__ == "__main__":
    main()
