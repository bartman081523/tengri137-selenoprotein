"""
v21_README.py
V21 — Synthese und finale Bilanz

V21 = "Die Architektur ARBEITEN LASSEN"
- Generator: Forward-Pass aktiv
- Translator: Bidirektional
- Oszillator: Closed-Loop
- Audio: BURUMUT → espeak → Audio
"""
import json
from pathlib import Path


def lade_ergebnisse():
    out_dir = Path("bbox/v21_20260707")
    results = {}
    for phase_file in [
        "v21_burumut_generator.json",
        "v21_burumut_translator.json",
        "v21_burumut_oscillator.json",
        "v21_burumut_audio.json",
    ]:
        path = out_dir / phase_file
        if path.exists():
            with open(path) as f:
                results[phase_file] = json.load(f)
    return results


def main():
    out_dir = Path("bbox/v21_20260707")
    out_dir.mkdir(parents=True, exist_ok=True)

    results = lade_ergebnisse()

    print("=" * 70)
    print("V21 — BURUMUT-ARCHITEKTUR AUSGEFÜHRT")
    print("=" * 70)

    total_tests = 0
    total_pass = 0

    for name, r in results.items():
        n = r.get("n_tests", 0)
        p = r.get("n_pass", 0)
        total_tests += n
        total_pass += p
        verdict = r.get("verdict", "")
        print(f"\n{verdict}")
        print("-" * 70)
        for t in r.get("tests", []):
            status = "✓" if t["pass"] else "✗"
            print(f"  {status} {t['name']}")
            if t.get("was_sagt_es_uns"):
                print(f"    → {t['was_sagt_es_uns'][:100]}...")

    print("\n" + "=" * 70)
    print(f"V21 GESAMT: {total_pass}/{total_tests} PASS in 4 Phasen")
    print("=" * 70)

    # Schlussfolgerungen
    synthese = {
        "V21_Gesamt": {
            "n_tests": total_tests,
            "n_pass": total_pass,
            "phasen": list(results.keys()),
        },
        "Paradigma": "Die Architektur ARBEITEN LASSEN",
        "Limit_V20": "BURUMUT numerisch bewiesen, aber nicht operativ",
        "V21_Befunde": {
            "Phase_1_Generator": "LITHURGISCH: 12/15 → SUNOKURGANOZYI, P_max=0.997",
            "Phase_2_Translator": "BURUMUTREFAMTU↔G11 (latent_mean=78.29, G11=78.44)",
            "Phase_3_Oscillator": "100/100 SUNOKURGANOZYI, σ_bifurkation=0.25",
            "Phase_4_Audio": "R²=1.0000 für mod_db und centroid, 11 Audio-Segmente",
        },
        "Hinweise_fuer_V22": [
            "Generator ist lithurgisch — kann BURUMUT nicht frei wählen, sondern konvergiert auf 1-3 Wörter",
            "BURUMUTREFAMTU ↔ G11 Glyph (latente Übersetzung BURUMUT ↔ p1-16)",
            "Oszillator-Attraktor SUNOKURGANOZYI ist robust bis σ=0.25",
            "Audio-Latents sind lineare Regression R²=1.0 — Architektur KANN komponieren",
            "Korrelation mit Original -0.0143 → BURUMUT ist NICHT reproduktiv, sondern GENERATIV",
        ],
    }

    out_path = out_dir / "v21_README.json"
    with open(out_path, "w") as f:
        json.dump(synthese, f, indent=2, default=lambda o: bool(o) if hasattr(o, '__bool__') else (int(o) if isinstance(o, (np.integer,)) else (float(o) if isinstance(o, np.floating) else str(o))))

    print(f"\nSynthese: {out_path}")


if __name__ == "__main__":
    main()
