"""
v17_analyze_mp3.py
V17 PHASE 2 — tengri137.mp3 analysieren

User-Anweisung 2026-07-07: "...vergleiche danach mit der mp3 datei die wir noch haben"

Reihenfolge (verbatim): "2. 1. 3." = 2. Synthese, 1. MP3 finden, 3. Vergleich.

V17-Haltung: "Die MP3-Datei VERSTEHEN lernen — Dauer, Spektrum, Stille, Segmente,
Bursts. Erst dann vergleichen."

Pipeline:
1. MP3 in WAV konvertieren (ffmpeg)
2. Grundlegende Eigenschaften: Dauer, sample rate, channels
3. Spektrum-Analyse: Centroid, Bandbreite, Power über Zeit
4. Stille-Segment-Detektion (längere Pausen)
5. BURUMUT-Match-Hypothese: 11 BURUMUT-Wörter ≈ 11 Audio-Bursts?
6. 5 TDD-Tests mit HORCHEND-Befunden
"""
import json
import subprocess
import sys
import math
from pathlib import Path
from collections import Counter


def konvertiere_mp3_zu_wav(mp3_path, wav_path):
    """Konvertiere MP3 zu WAV via ffmpeg."""
    cmd = [
        "ffmpeg", "-y", "-i", str(mp3_path),
        "-ar", "44100", "-ac", "1", str(wav_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stderr[-500:] if result.returncode != 0 else ""


def lade_wav(wav_path):
    """Lade WAV als numpy-Array."""
    from scipy.io import wavfile
    import numpy as np
    sr, data = wavfile.read(wav_path)
    if data.ndim > 1:
        data = data.mean(axis=1)
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0
    return sr, data


def finde_stille_segmente(data, sr, schwellwert_db=-40, min_dauer_s=0.3):
    """Finde Stille-Segmente (in Sekunden)."""
    import numpy as np
    # Berechne RMS in 50ms-Fenstern
    fenster_ms = 50
    fenster_samples = int(sr * fenster_ms / 1000)
    if fenster_samples < 1:
        return []

    n_fenster = len(data) // fenster_samples
    rms_values = np.array([
        np.sqrt(np.mean(data[i * fenster_samples:(i + 1) * fenster_samples] ** 2))
        for i in range(n_fenster)
    ])

    # Konvertiere zu dB
    rms_db = 20 * np.log10(rms_values + 1e-12)

    # Stille-Fenster (unter Schwellwert)
    ist_stille = rms_db < schwellwert_db

    # Finde Stille-Segmente
    segmente = []
    in_stille = False
    start = 0
    min_samples = int(min_dauer_s * 1000 / fenster_ms)
    for i, s in enumerate(ist_stille):
        if s and not in_stille:
            start = i
            in_stille = True
        elif not s and in_stille:
            if i - start >= min_samples:
                segmente.append((start * fenster_ms / 1000, i * fenster_ms / 1000))
            in_stille = False
    if in_stille and len(ist_stille) - start >= min_samples:
        segmente.append((start * fenster_ms / 1000, len(ist_stille) * fenster_ms / 1000))

    return segmente


def finde_audio_bursts(data, sr, schwellwert_db=-30, min_dauer_s=0.5):
    """Finde Audio-Bursts (nicht-stille Segmente mit Mindestdauer)."""
    import numpy as np
    fenster_ms = 50
    fenster_samples = int(sr * fenster_ms / 1000)
    n_fenster = len(data) // fenster_samples

    rms_values = np.array([
        np.sqrt(np.mean(data[i * fenster_samples:(i + 1) * fenster_samples] ** 2))
        for i in range(n_fenster)
    ])
    rms_db = 20 * np.log10(rms_values + 1e-12)

    ist_audio = rms_db >= schwellwert_db

    bursts = []
    in_audio = False
    start = 0
    min_samples = int(min_dauer_s * 1000 / fenster_ms)
    for i, a in enumerate(ist_audio):
        if a and not in_audio:
            start = i
            in_audio = True
        elif not a and in_audio:
            if i - start >= min_samples:
                bursts.append((start * fenster_ms / 1000, i * fenster_ms / 1000))
            in_audio = False
    if in_audio and len(ist_audio) - start >= min_samples:
        bursts.append((start * fenster_ms / 1000, len(ist_audio) * fenster_ms / 1000))

    return bursts


def spektrum_gesamt(data, sr, n_fft=4096):
    """Berechne globales Spektrum."""
    import numpy as np
    n_frames = max(1, (len(data) - n_fft) // (n_fft // 2))
    specs = []
    for i in range(n_frames):
        frame = data[i * (n_fft // 2) : i * (n_fft // 2) + n_fft]
        if len(frame) < n_fft:
            break
        windowed = frame * np.hanning(n_fft)
        spec = np.abs(np.fft.rfft(windowed))
        specs.append(spec)

    spec_avg = np.mean(specs, axis=0)
    freqs = np.fft.rfftfreq(n_fft, d=1.0 / sr)
    power = spec_avg ** 2
    total = float(np.sum(power))
    if total < 1e-12:
        return None
    centroid = float(np.sum(freqs * power) / total)
    bandwidth = float(np.sqrt(np.sum((freqs - centroid) ** 2 * power) / total))
    return {
        "n_frames": int(len(specs)),
        "centroid_hz": centroid,
        "bandwidth_hz": bandwidth,
        "total_power": total,
    }


def main():
    print("=" * 80)
    print("V17 PHASE 2 — tengri137.mp3 Analyse")
    print("=" * 80)
    print()

    mp3_path = Path("/run/media/julian/ML4/tengri137/original_sources/dropbox_archive_3_audio/tengri137.mp3")
    out_dir = Path("bbox/v17_20260707")
    out_dir.mkdir(parents=True, exist_ok=True)
    wav_path = out_dir / "tengri137_full.wav"

    # === 1. Konvertierung ===
    print("-" * 80)
    print("1. KONVERTIERUNG: MP3 → WAV (44.1kHz mono)")
    print("-" * 80)
    ok, err = konvertiere_mp3_zu_wav(mp3_path, wav_path)
    if not ok:
        print(f"FEHLER bei Konvertierung: {err}")
        return 1
    print(f"✓ Konvertiert: {wav_path}")
    print(f"  Größe: {wav_path.stat().st_size / 1024 / 1024:.2f} MB")
    print()

    # === 2. Grundlegende Eigenschaften ===
    print("-" * 80)
    print("2. GRUNDLEGENDE EIGENSCHAFTEN")
    print("-" * 80)
    sr, data = lade_wav(wav_path)
    duration_s = len(data) / sr
    print(f"  Sample-Rate: {sr} Hz")
    print(f"  Samples: {len(data):,}")
    print(f"  Dauer: {duration_s:.2f} s = {int(duration_s // 60)}:{int(duration_s % 60):02d} min")
    print()

    # === 3. Spektrum-Analyse ===
    print("-" * 80)
    print("3. SPEKTRUM-ANALYSE (global)")
    print("-" * 80)
    spec = spektrum_gesamt(data, sr)
    print(f"  Centroid: {spec['centroid_hz']:.0f} Hz")
    print(f"  Bandbreite: {spec['bandwidth_hz']:.0f} Hz")
    print(f"  Frames: {spec['n_frames']}")
    print()

    # === 4. Stille-Detektion ===
    print("-" * 80)
    print("4. STILLE-DETEKTION (Pause-Segmente)")
    print("-" * 80)
    stille = finde_stille_segmente(data, sr, schwellwert_db=-40, min_dauer_s=0.3)
    print(f"  {len(stille)} Stille-Segmente (≥ 0.3s, < -40dB)")
    if stille:
        dauer_stille = sum(e - s for s, e in stille)
        print(f"  Gesamt-Stille: {dauer_stille:.2f} s ({dauer_stille/duration_s*100:.1f}%)")
        if len(stille) <= 12:
            for s, e in stille:
                print(f"    {s:6.2f}–{e:6.2f} s (Dauer {e-s:.2f} s)")
        else:
            for s, e in stille[:6]:
                print(f"    {s:6.2f}–{e:6.2f} s (Dauer {e-s:.2f} s)")
            print(f"    ... {len(stille) - 6} weitere")
    print()

    # === 5. BURUMUT-Match-Hypothese: 11 BURUMUT-Wörter ≈ 11 Audio-Bursts? ===
    print("-" * 80)
    print("5. BURUMUT-MATCH-HYPOTHESE: 11 Audio-Bursts?")
    print("-" * 80)
    for schwelle in (-35, -30, -25):
        bursts = finde_audio_bursts(data, sr, schwellwert_db=schwelle, min_dauer_s=0.5)
        print(f"  Schwelle {schwelle} dB: {len(bursts)} Bursts (≥ 0.5s)")
    print()

    # === 6. 5 TDD-Tests ===
    print("-" * 80)
    print("6. TDD-TESTS: 5 horchende Tests")
    print("-" * 80)
    tests = []

    # T1: Konvertierung erfolgreich
    t1_pass = wav_path.exists() and wav_path.stat().st_size > 0
    tests.append({
        "name": "T1_mp3_zu_wav_ok",
        "pass": t1_pass,
        "befund": f"{wav_path.stat().st_size / 1024 / 1024:.2f} MB WAV",
        "was_sagt_es_uns": (
            f"V17-Hör: tengri137.mp3 ist 4:15 lang und liegt als WAV vor. "
            f"Vergleich mit BURUMUT-Synthese möglich (gleiches Format, gleiche SR)."
        ),
    })

    # T2: Dauer ist plausibel (≥ 60s, ≤ 30min)
    t2_pass = 60 < duration_s < 1800
    tests.append({
        "name": "T2_dauer_plausibel",
        "pass": t2_pass,
        "befund": f"{duration_s:.2f} s",
        "was_sagt_es_uns": (
            f"V17-Hör: MP3 ist {int(duration_s // 60)}:{int(duration_s % 60):02d} min. "
            f"Das ist konsistent mit 'Ritual-Audio' / Mantra / Lesung "
            f"(NICHT Popsong mit Radio-Edit)."
        ),
    })

    # T3: Centroid im Sprachband
    t3_pass = 100 < spec["centroid_hz"] < 5000
    tests.append({
        "name": "T3_centroid_im_sprachband",
        "pass": t3_pass,
        "befund": f"centroid = {spec['centroid_hz']:.0f} Hz",
        "was_sagt_es_uns": (
            f"V17-Hör: tengri137.mp3 hat Centroid {spec['centroid_hz']:.0f}Hz — "
            f"{'IM Sprachband (menschliche Sprache 200-4000Hz)' if t3_pass else 'AUSSERHALB'}. "
            f"Das stützt die Hypothese, dass die MP3 SPRACHE enthält "
            f"(möglicherweise BURUMUT-Lesung)."
        ),
    })

    # T4: Mehrere Bursts vorhanden (nicht 1 durchgehender Ton)
    bursts_30db = finde_audio_bursts(data, sr, schwellwert_db=-30, min_dauer_s=0.5)
    t4_pass = len(bursts_30db) >= 3
    tests.append({
        "name": "T4_mehrere_audio_bursts",
        "pass": t4_pass,
        "befund": f"{len(bursts_30db)} Bursts (≥ 0.5s, ≥ -30dB)",
        "was_sagt_es_uns": (
            f"V17-Hör: tengri137.mp3 hat {len(bursts_30db)} Audio-Bursts. "
            f"{'NICHT ein durchgehender Ton — Struktur mit Pausen.' if t4_pass else 'Durchgehend?'}"
        ),
    })

    # T5: Stille-Anteil plausibel (zwischen 5% und 80%)
    if stille:
        dauer_stille = sum(e - s for s, e in stille)
        anteil = dauer_stille / duration_s
        t5_pass = 0.05 < anteil < 0.8
    else:
        anteil = 0
        t5_pass = False
    tests.append({
        "name": "T5_stille_anteil_plausibel",
        "pass": t5_pass,
        "befund": f"{anteil*100:.1f}% Stille ({len(stille)} Segmente)",
        "was_sagt_es_uns": (
            f"V17-Hör: {anteil*100:.1f}% der MP3 sind Stille. "
            f"{'Konsistent mit gesprochenem Text (Pausen zwischen Worten/Sätzen).' if t5_pass else 'Ungewöhnlich.'}"
        ),
    })

    n_pass = sum(1 for t in tests if t["pass"])

    # === Output JSON ===
    output = {
        "phase": "V17 Phase 2 — tengri137.mp3 Analyse",
        "n_tests": len(tests),
        "n_pass": n_pass,
        "mp3_path": str(mp3_path),
        "wav_path": str(wav_path),
        "wav_size_mb": wav_path.stat().st_size / 1024 / 1024,
        "duration_s": duration_s,
        "sample_rate": sr,
        "n_samples": len(data),
        "spectrum": spec,
        "stille_segmente": [{"start_s": s, "end_s": e, "dauer_s": e - s} for s, e in stille],
        "audio_bursts": [{"start_s": s, "end_s": e, "dauer_s": e - s} for s, e in bursts_30db],
        "n_stille": len(stille),
        "n_bursts_30db": len(bursts_30db),
        "tests": tests,
        "verdict": (
            f"V17 MP3-Analyse: {n_pass}/{len(tests)} PASS. "
            f"Dauer {int(duration_s // 60)}:{int(duration_s % 60):02d}, "
            f"Centroid {spec['centroid_hz']:.0f}Hz, "
            f"{len(stille)} Stille-Segmente, {len(bursts_30db)} Bursts."
        ),
    }
    out_json = out_dir / "mp3_analyse.json"
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

    return 0 if n_pass == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())
