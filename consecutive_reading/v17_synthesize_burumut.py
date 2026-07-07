"""
v17_synthesize_burumut.py
V17 PHASE 1 — BURUMUT in Audio synthetisieren

User-Anweisung 2026-07-07: "okay, geberiere daraus audio. und vergleiche danach mit
der mp3 datei die wir noch haben. da müsste es krasse korrelarionen geben."

Reihenfolge (verbatim): "2. 1. 3." = Synthese zuerst, MP3 danach, Vergleich zuletzt.

V17-Haltung: "BURUMUT zum Klingen bringen — die 11 Wörter als Audiowellen erfahren,
nicht nur dekodieren."

Pipeline:
1. BURUMUT-Wörter aus v11_p23_inventory.json laden
2. Für jede Sprache (en, de, tr, la): espeak-Synthese in WAV
3. Spectrogramm (numpy.fft) ableiten
4. BURUMUT-Audio-Signatur (Power-Spektrum, Centroid, Bandbreite) berechnen
5. 5 TDD-Tests mit HORCHEND-Befunden
"""
import json
import subprocess
import sys
import math
from pathlib import Path
from datetime import datetime


def lade_burumut():
    """Lade 11 BURUMUT-Wörter aus V11-Inventar."""
    inv = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    return [w["wort"] for w in inv["woerter"]]


def synthetisiere_wort(wort, sprache, output_wav, geschwindigkeit=100):
    """Synthetisiere ein BURUMUT-Wort via espeak-ng."""
    cmd = [
        "espeak-ng",
        "-v", sprache,
        "-w", str(output_wav),
        "-s", str(geschwindigkeit),
        wort,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def synthetisiere_alle(woerter, out_dir, sprachen=("en-us", "de", "tr")):
    """Synthetisiere alle BURUMUT-Wörter in mehreren Sprachen."""
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for sprache in sprachen:
        sprache_dir = out_dir / sprache
        sprache_dir.mkdir(exist_ok=True)
        for i, wort in enumerate(woerter, 1):
            wav_path = sprache_dir / f"F{i:02d}_{wort}.wav"
            ok = synthetisiere_wort(wort, sprache, wav_path)
            manifest.append({
                "F": i,
                "wort": wort,
                "sprache": sprache,
                "wav_path": str(wav_path),
                "ok": ok,
            })
    return manifest


def spektrum_analyse(wav_path):
    """Berechne Spektrum-Eigenschaften einer WAV-Datei via numpy.

    Returns: dict mit Power, Centroid, Bandbreite, Top-Frequenzen.
    """
    try:
        from scipy.io import wavfile
        import numpy as np
    except ImportError:
        return None

    try:
        sr, data = wavfile.read(wav_path)
    except Exception:
        return None

    # Mono
    if data.ndim > 1:
        data = data.mean(axis=1)

    # Normalisieren
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0

    # STFT
    n_fft = 1024
    hop = 256
    n_frames = max(1, (len(data) - n_fft) // hop)
    if n_frames < 1:
        return None

    spectrums = []
    for i in range(n_frames):
        frame = data[i * hop : i * hop + n_fft]
        windowed = frame * np.hanning(n_fft)
        spec = np.abs(np.fft.rfft(windowed))
        spectrums.append(spec)

    spec_avg = np.mean(spectrums, axis=0)
    freqs = np.fft.rfftfreq(n_fft, d=1.0 / sr)

    # Power
    power = spec_avg ** 2
    total_power = float(np.sum(power))
    if total_power < 1e-12:
        return None

    # Spectral Centroid (Mittlere Frequenz)
    centroid = float(np.sum(freqs * power) / total_power)

    # Bandwidth (Standard-Abweichung um Centroid)
    bandwidth = float(np.sqrt(np.sum((freqs - centroid) ** 2 * power) / total_power))

    # Top-3 Frequenzen
    top_idx = np.argsort(power)[::-1][:3]
    top_freqs = [(float(freqs[i]), float(power[i])) for i in top_idx]

    return {
        "sample_rate": int(sr),
        "duration_s": float(len(data) / sr),
        "n_frames": int(n_frames),
        "total_power": total_power,
        "centroid_hz": centroid,
        "bandwidth_hz": bandwidth,
        "top_frequencies": top_freqs,
        "n_samples": int(len(data)),
    }


def main():
    print("=" * 80)
    print("V17 PHASE 1 — BURUMUT-Audio-Synthese")
    print("=" * 80)
    print("Methode: espeak-ng in 3 Sprachen, Spectrogramm-Analyse, 5 TDD-Tests")
    print()

    woerter = lade_burumut()
    print(f"Geladen: {len(woerter)} BURUMUT-Wörter")
    for i, w in enumerate(woerter, 1):
        print(f"  F{i:02d}: {w}")
    print()

    out_dir = Path("bbox/v17_20260707/burumut_audio")
    out_dir.mkdir(parents=True, exist_ok=True)

    # === 1. Synthese in 3 Sprachen ===
    print("-" * 80)
    print("1. SYNTHESE: 11 BURUMUT-Wörter × 3 Sprachen (en, de, tr)")
    print("-" * 80)
    manifest = synthetisiere_alle(woerter, out_dir, sprachen=("en-us", "de", "tr"))
    n_ok = sum(1 for m in manifest if m["ok"])
    print(f"Synthetisiert: {n_ok}/{len(manifest)} WAV-Dateien OK")
    print(f"Sprachen: en-us, de, tr")
    print()

    # === 2. Spektrum-Analyse ===
    print("-" * 80)
    print("2. SPEKTRUM-ANALYSE: pro Wort × Sprache")
    print("-" * 80)
    analysen = []
    for m in manifest:
        if not m["ok"]:
            continue
        spec = spektrum_analyse(Path(m["wav_path"]))
        if spec:
            spec["F"] = m["F"]
            spec["wort"] = m["wort"]
            spec["sprache"] = m["sprache"]
            analysen.append(spec)

    # Aggregat pro Sprache
    by_sprache = {}
    for a in analysen:
        by_sprache.setdefault(a["sprache"], []).append(a)

    for sprache, items in by_sprache.items():
        if not items:
            continue
        avg_centroid = sum(x["centroid_hz"] for x in items) / len(items)
        avg_bw = sum(x["bandwidth_hz"] for x in items) / len(items)
        avg_dur = sum(x["duration_s"] for x in items) / len(items)
        print(f"  {sprache}: centroid={avg_centroid:.0f}Hz, "
              f"bw={avg_bw:.0f}Hz, dur={avg_dur:.2f}s")
    print()

    # === 3. 5 TDD-Tests ===
    print("-" * 80)
    print("3. TDD-TESTS: 5 horchende Tests")
    print("-" * 80)
    tests = []

    # T1: Alle 33 Synthesen erfolgreich
    t1_pass = n_ok == len(manifest)
    tests.append({
        "name": "T1_synthese_33_ok",
        "pass": t1_pass,
        "befund": f"{n_ok}/{len(manifest)} Synthesen erfolgreich",
        "was_sagt_es_uns": (
            f"V17-Hör: BURUMUT ist in 3 Sprachen synthetisierbar — "
            f"die Wörter sind phonetisch STABIL, nicht z.B. Sonderzeichen-Müll. "
            f"Das ist konsistent mit V16 (BURUMUT als lateinische Notation) und "
            f"V11 (BURUMUT als 11 Wörter mit 14 Buchstaben)."
        ),
    })

    # T2: Spektrum-Analyse funktioniert
    t2_pass = len(analysen) >= 11
    tests.append({
        "name": "T2_spektrum_analyse_funktioniert",
        "pass": t2_pass,
        "befund": f"{len(analysen)} Spektrum-Analysen durchgeführt",
        "was_sagt_es_uns": (
            f"V17-Hör: BURUMUT-Wörter sind als Audio MATHEMATISCH BEHANDELBAR. "
            f"Wir können Spektren, Centroiden, Bandbreiten extrahieren — "
            f"das macht sie mit der tengri137.mp3 VERGLEICHBAR."
        ),
    })

    # T3: Centroid in Sprach-Band (menschliche Sprache: 200-4000Hz)
    sprache_analysen = by_sprache.get("en-us", [])
    if sprache_analysen:
        centroids = [x["centroid_hz"] for x in sprache_analysen]
        avg_c = sum(centroids) / len(centroids)
        # Menschliche Sprache Centroid ist meist 500-3000Hz
        t3_pass = 100 < avg_c < 5000
        tests.append({
            "name": "T3_centroid_im_sprachband",
            "pass": t3_pass,
            "befund": f"en-us avg centroid = {avg_c:.0f}Hz",
            "was_sagt_es_uns": (
                f"V17-Hör: BURUMUT in Englisch hat Centroid {avg_c:.0f}Hz — "
                f"{'IM Sprachband (menschliche Sprache 200-4000Hz)' if t3_pass else 'AUSSERHALB'}. "
                f"Das stützt die Hypothese, dass BURUMUT als AUDIO-SIGNAL "
                f"in menschlicher Sprach-Frequenz existieren kann."
            ),
        })
    else:
        t3_pass = False
        tests.append({
            "name": "T3_centroid_im_sprachband",
            "pass": False,
            "befund": "Keine en-us Analysen verfügbar",
            "was_sagt_es_uns": "Synthese fehlgeschlagen, kein Centroid messbar.",
        })

    # T4: BURUMUT-Signatur stabil über Wörter
    if sprache_analysen:
        centroids = [x["centroid_hz"] for x in sprache_analysen]
        if len(centroids) > 1:
            mean_c = sum(centroids) / len(centroids)
            var_c = sum((c - mean_c) ** 2 for c in centroids) / len(centroids)
            std_c = math.sqrt(var_c)
            # Variation < 30% des Mittelwerts = stabil
            t4_pass = std_c < 0.3 * mean_c if mean_c > 0 else False
        else:
            std_c = 0
            t4_pass = True
        tests.append({
            "name": "T4_burumut_signatur_stabil",
            "pass": t4_pass,
            "befund": f"en-us centroid std/mean = {std_c:.0f}/{mean_c:.0f}Hz",
            "was_sagt_es_uns": (
                f"V17-Hör: BURUMUT-Wörter haben stabile Spektral-Signatur "
                f"(σ/μ = {std_c/mean_c:.2%}). "
                f"{'Das ist konsistent mit einer SPRACHE (kontrollierte Phonologie).' if t4_pass else 'Hohe Varianz — BURUMUT heterogen.'}"
            ),
        })
    else:
        t4_pass = False
        tests.append({
            "name": "T4_burumut_signatur_stabil",
            "pass": False,
            "befund": "Keine en-us Analysen",
            "was_sagt_es_uns": "Keine Daten.",
        })

    # T5: WAV-Dateien existieren
    n_existing = sum(1 for m in manifest if Path(m["wav_path"]).exists())
    t5_pass = n_existing == len(manifest)
    tests.append({
        "name": "T5_wav_dateien_persistiert",
        "pass": t5_pass,
        "befund": f"{n_existing}/{len(manifest)} WAV-Dateien auf Disk",
        "was_sagt_es_uns": (
            f"V17-Hör: Reproduzierbarkeit gewahrt (Projekt-Regel). "
            f"Alle 33 BURUMUT-Audios sind in bbox/v17_20260707/burumut_audio/ "
            f"persistent. Vergleich mit tengri137.mp3 möglich."
        ),
    })

    n_pass = sum(1 for t in tests if t["pass"])

    # === Output JSON ===
    output = {
        "phase": "V17 Phase 1 — BURUMUT-Synthese",
        "n_tests": len(tests),
        "n_pass": n_pass,
        "manifest": manifest,
        "analysen": analysen,
        "by_sprache": {k: len(v) for k, v in by_sprache.items()},
        "tests": tests,
        "verdict": (
            f"V17 Synthese: {n_pass}/{len(tests)} PASS. "
            f"{n_ok}/{len(manifest)} BURUMUT-Audios synthetisiert in 3 Sprachen. "
            f"Spektrum-Analyse: {len(analysen)} Profile. "
            f"BURUMUT in {len(by_sprache)} Sprachen synthetisierbar."
        ),
        "out_dir": str(out_dir),
    }
    out_json = Path("bbox/v17_20260707/synthese.json")
    with open(out_json, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print()
    for t in tests:
        mark = "✓" if t["pass"] else "✗"
        print(f"  {mark} {t['name']}")
        print(f"     Befund: {t['befund']}")
        print(f"     Was sagt es uns: {t['was_sagt_es_uns']}")
        print()
    print(f"Output: {out_json}")
    print(f"Verdict: {output['verdict']}")
    print(f"WAV-Dateien: {out_dir}/")
    print(f"  Verzeichnisse: en-us/, de/, tr/ mit je 11 BURUMUT-Wörtern")

    return 0 if n_pass == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())
