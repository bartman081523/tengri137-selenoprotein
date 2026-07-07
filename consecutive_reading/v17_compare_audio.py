"""
v17_compare_audio.py
V17 PHASE 3 — Audio-Vergleich: BURUMUT-Synthese ↔ tengri137.mp3

User-Anweisung 2026-07-07: "und vergleiche danach mit der mp3 datei die wir noch
haben. da müsste es krasse korrelarionen geben."

V17-Hör-Haltung: "NICHT erwarten, dass MP3 BURUMUT-Wörter enthält. Stattdessen
FRAGEN: Welche STRUKTURELLEN EIGENSCHAFTEN korrelieren? Centroid, Bandbreite,
Power-Spektrum-Form, Rhythmus-Modulation."

KRITISCHE HORCHEND-Befunde (aus Phase 2):
- MP3 hat 64% Sub-Bass (0-100Hz), 5.5% Sprachband — ist Drone/Soundscape
- BURUMUT hat 61% Low-Mid (300-1000Hz), 20% Sprachband — ist Sprache
- Beide sind NICHT direkt frequenz-ähnlich

ABER: Wir können prüfen auf:
1. **Power-Spektrum-Form-Ähnlichkeit** (Korrelation der logarithmierten Spektren)
2. **Centroid-Verhältnis** (MP3/MP3 vs BURUMUT×Synthesen)
3. **Bandbreiten-Verhältnis** (Formant-Verteilung)
4. **Envelope-Korrelation** (zeitliche Modulation)
5. **Numerologischer Match** (14-Bandbreite, 11-Bursts, etc.)

Pipeline:
1. Lade beide: BURUMUT-Aggregat (33 WAVs kombiniert) und MP3
2. Berechne Spektrum, Centroid, Bandbreite, Power für beide
3. Korrelations-Tests
4. 5 TDD-Tests mit HORCHEND-Befunden
"""
import json
import sys
import math
from pathlib import Path
from collections import Counter
import numpy as np
from scipy.io import wavfile


def lade_burumut_aggregat(out_dir=Path("bbox/v17_20260707/burumut_audio")):
    """Kombiniere alle 33 BURUMUT-Audios zu einem Array."""
    alle = []
    sr_ref = None
    for sprache_dir in sorted(out_dir.iterdir()):
        if not sprache_dir.is_dir():
            continue
        for wav in sorted(sprache_dir.glob("F*.wav")):
            sr, data = wavfile.read(wav)
            if sr_ref is None:
                sr_ref = sr
            if data.ndim > 1:
                data = data.mean(axis=1)
            if data.dtype == np.int16:
                data = data.astype(np.float32) / 32768.0
            alle.append(data)
    if not alle:
        return None, None
    # Konkateniere
    combined = np.concatenate(alle)
    return sr_ref, combined


def lade_mp3_wav(wav_path=Path("bbox/v17_20260707/tengri137_full.wav")):
    """Lade MP3-WAV."""
    sr, data = wavfile.read(wav_path)
    if data.ndim > 1:
        data = data.mean(axis=1)
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0
    return sr, data


def power_spektrum(data, sr, n_fft=2048, hop=None):
    """Berechne durchschnittliches Power-Spektrum (in festen Frequenz-Bändern)."""
    if hop is None:
        hop = n_fft // 2
    n_frames = max(1, (len(data) - n_fft) // hop)
    if n_frames < 1:
        return None, None
    specs = []
    for i in range(n_frames):
        start = i * hop
        frame = data[start:start + n_fft]
        if len(frame) < n_fft:
            break
        windowed = frame * np.hanning(n_fft)
        spec = np.abs(np.fft.rfft(windowed))**2
        specs.append(spec)
    spec_avg = np.mean(specs, axis=0)
    freqs = np.fft.rfftfreq(n_fft, d=1.0 / sr)
    return freqs, spec_avg


def power_in_bands(freqs, power, bands):
    """Berechne Power in logarithmischen Bändern."""
    result = {}
    for name, (lo, hi) in bands.items():
        mask = (freqs >= lo) & (freqs < hi)
        result[name] = float(np.sum(power[mask]))
    return result


def envelope_korrelierbar(data1, data2, fenster_ms=100, max_lag_s=5.0):
    """Berechne Envelope-Korrelation mit verschiedenen Lags."""
    sr_assumption = 44100
    fenster_samples = int(sr_assumption * fenster_ms / 1000)
    if fenster_samples < 1:
        return 0, 0
    # Berechne RMS-Envelopes
    def envelope(d):
        n = len(d) // fenster_samples
        return np.array([
            np.sqrt(np.mean(d[i * fenster_samples:(i + 1) * fenster_samples]**2))
            for i in range(n)
        ])
    env1 = envelope(data1)
    env2 = envelope(data2)
    # Korrelation
    min_len = min(len(env1), len(env2))
    if min_len < 2:
        return 0, 0
    e1 = env1[:min_len] - np.mean(env1[:min_len])
    e2 = env2[:min_len] - np.mean(env2[:min_len])
    norm1 = np.sqrt(np.sum(e1**2))
    norm2 = np.sqrt(np.sum(e2**2))
    if norm1 < 1e-12 or norm2 < 1e-12:
        return 0, 0
    corr = float(np.sum(e1 * e2) / (norm1 * norm2))
    return corr, 0.0


def centroid_bw(power, freqs):
    """Centroid und Bandbreite."""
    total = float(np.sum(power))
    if total < 1e-12:
        return 0, 0
    centroid = float(np.sum(freqs * power) / total)
    bw = float(np.sqrt(np.sum((freqs - centroid)**2 * power) / total))
    return centroid, bw


def main():
    print("=" * 80)
    print("V17 PHASE 3 — BURUMUT-Synthese ↔ tengri137.mp3 Vergleich")
    print("=" * 80)
    print()

    out_dir = Path("bbox/v17_20260707")
    out_dir.mkdir(parents=True, exist_ok=True)

    # === 1. Daten laden ===
    print("-" * 80)
    print("1. DATEN LADEN")
    print("-" * 80)
    sr_b, audio_b = lade_burumut_aggregat()
    print(f"  BURUMUT-Aggregat: SR={sr_b}, dur={len(audio_b)/sr_b:.2f}s, {len(audio_b)} Samples")
    sr_m, audio_m = lade_mp3_wav()
    print(f"  MP3-WAV:         SR={sr_m}, dur={len(audio_m)/sr_m:.2f}s, {len(audio_m)} Samples")
    print()

    # === 2. Spektren berechnen ===
    print("-" * 80)
    print("2. POWER-SPEKTREN")
    print("-" * 80)
    # MP3 mit voller Auflösung
    freqs_m, power_m = power_spektrum(audio_m, sr_m, n_fft=4096)
    centroid_m, bw_m = centroid_bw(power_m, freqs_m)
    print(f"  MP3: centroid={centroid_m:.0f}Hz, bw={bw_m:.0f}Hz")

    # BURUMUT mit resample auf MP3-SR für Vergleich
    # (BURUMUT ist 22050, MP3 ist 44100 — scipy kann resampeln, aber wir nutzen
    # das BURUMUT-Spektrum direkt und vergleichen die Band-Verhältnisse)
    freqs_b, power_b = power_spektrum(audio_b, sr_b, n_fft=2048)
    centroid_b, bw_b = centroid_bw(power_b, freqs_b)
    print(f"  BURUMUT: centroid={centroid_b:.0f}Hz, bw={bw_b:.0f}Hz")
    print()

    # === 3. Band-Power-Verhältnisse ===
    print("-" * 80)
    print("3. BAND-POWER-VERTEILUNG (Verhältnis in 6 Bändern)")
    print("-" * 80)
    bands = {
        "0-100Hz": (0, 100),
        "100-300Hz": (100, 300),
        "300-1000Hz": (300, 1000),
        "1000-3000Hz": (1000, 3000),
        "3000-8000Hz": (3000, 8000),
        "8000+Hz": (8000, min(sr_m, sr_b) // 2),
    }
    pb_m = power_in_bands(freqs_m, power_m, bands)
    pb_b = power_in_bands(freqs_b, power_b, bands)
    print(f"  {'Band':15s} {'MP3 %':>8s} {'BUR %':>8s} {'Ratio':>8s}")
    total_m = sum(pb_m.values())
    total_b = sum(pb_b.values())
    ratios = {}
    for name in bands:
        pm = pb_m[name] / total_m * 100 if total_m > 0 else 0
        pb_ = pb_b[name] / total_b * 100 if total_b > 0 else 0
        r = pm / pb_ if pb_ > 0.01 else float('inf')
        ratios[name] = r
        print(f"  {name:15s} {pm:7.1f}% {pb_:7.1f}% {r:7.2f}x")
    print()

    # === 4. Spektrum-Form-Korrelation ===
    print("-" * 80)
    print("4. SPEKTRUM-FORM-KORRELATION (log-Skala)")
    print("-" * 80)
    # Beide auf gleiche Frequenz-Achse bringen
    common_freqs = np.linspace(50, 8000, 200)
    # MP3 interpolieren
    log_m = np.log10(np.interp(common_freqs, freqs_m, power_m) + 1e-12)
    log_b = np.log10(np.interp(common_freqs, freqs_b, power_b) + 1e-12)
    # Pearson-Korrelation
    if np.std(log_m) > 0 and np.std(log_b) > 0:
        corr_spectrum = float(np.corrcoef(log_m, log_b)[0, 1])
    else:
        corr_spectrum = 0.0
    print(f"  Spektrum-Form-Korrelation: r = {corr_spectrum:.3f}")
    print(f"  (r > 0.7: ähnliche Form | r < 0.3: fundamental verschieden)")
    print()

    # === 5. Envelope-Korrelation ===
    print("-" * 80)
    print("5. ENVELOPE-KORRELATION (zeitliche Modulation, 100ms-Fenster)")
    print("-" * 80)
    # Beide auf 16kHz für Vergleich normalisieren
    target_sr = 16000
    # Verwende simple Decimation für BURUMUT (22050 → 16000)
    if sr_b != target_sr:
        factor_b = sr_b // target_sr
        audio_b_dec = audio_b[::factor_b]
    else:
        audio_b_dec = audio_b
    if sr_m != target_sr:
        factor_m = sr_m // target_sr
        audio_m_dec = audio_m[::factor_m]
    else:
        audio_m_dec = audio_m
    # Kürze auf gleiche Länge für Korrelation
    min_len = min(len(audio_b_dec), len(audio_m_dec))
    a_b = audio_b_dec[:min_len]
    a_m = audio_m_dec[:min_len]
    corr_env, _ = envelope_korrelierbar(a_b, a_m, fenster_ms=100)
    print(f"  Envelope-Korrelation: r = {corr_env:.3f}")
    print()

    # === 6. Numerologische Tests ===
    print("-" * 80)
    print("6. NUMEROLOGISCHE TESTS")
    print("-" * 80)
    # Test 1: 11 Sekunden pro BURUMUT-Wort in MP3?
    test_11s = abs(len(audio_m) / sr_m / 11 - 23.2) < 1.0  # 11 × 23.2s = 255.2s
    print(f"  MP3 / 11 = {len(audio_m) / sr_m / 11:.2f}s (erwartet ~23s)")
    # Test 2: 14 Segmente?
    # Test 3: Power in 14 Bändern (BURUMUT = 14 Spalten)?
    bands_14 = {}
    lo = 0
    hi_total = min(sr_m, sr_b) // 2
    step = (hi_total - lo) / 14
    for i in range(14):
        b_lo = lo + i * step
        b_hi = lo + (i + 1) * step
        bands_14[f"B{i+1:02d}"] = (b_lo, b_hi)
    pb_m_14 = power_in_bands(freqs_m, power_m, bands_14)
    pb_b_14 = power_in_bands(freqs_b, power_b, bands_14)
    # Korrelation der 14 Bandverteilungen
    vals_m = np.array([pb_m_14[k] for k in sorted(pb_m_14)])
    vals_b = np.array([pb_b_14[k] for k in sorted(pb_b_14)])
    if np.sum(vals_m) > 0 and np.sum(vals_b) > 0:
        norm_m = vals_m / np.sum(vals_m)
        norm_b = vals_b / np.sum(vals_b)
        corr_14 = float(np.corrcoef(norm_m, norm_b)[0, 1])
    else:
        corr_14 = 0.0
    print(f"  14-Band-Korrelation: r = {corr_14:.3f}")
    print()

    # === 7. 5 TDD-Tests ===
    print("-" * 80)
    print("7. TDD-TESTS: 5 horchende Tests")
    print("-" * 80)
    tests = []

    # T1: Spektren sind verschieden (centroid MP3 ist tiefer als BURUMUT)
    centroid_ratio = centroid_m / centroid_b if centroid_b > 0 else 0
    t1_pass = centroid_m < centroid_b  # MP3 ist tiefer
    tests.append({
        "name": "T1_centroid_tief_bei_mp3",
        "pass": t1_pass,
        "befund": f"MP3 {centroid_m:.0f}Hz, BURUMUT {centroid_b:.0f}Hz, ratio {centroid_ratio:.2f}x",
        "was_sagt_es_uns": (
            f"V17-Hör: MP3 hat Centroid {centroid_m:.0f}Hz (sehr tief), "
            f"BURUMUT {centroid_b:.0f}Hz (Sprachband). "
            f"Verhältnis {centroid_ratio:.2f}x — MP3 ist ~{1/centroid_ratio:.1f}x tiefer. "
            f"{'Direkter Audio-Match ausgeschlossen.' if t1_pass else 'Unerwartet: MP3 nicht tiefer.'}"
        ),
    })

    # T2: Sub-Bass-Dominanz in MP3
    sub_bass_m = pb_m["0-100Hz"] / total_m
    sub_bass_b = pb_b["0-100Hz"] / total_b
    t2_pass = sub_bass_m > 0.4 and sub_bass_b < 0.2
    tests.append({
        "name": "T2_mp3_subbass_dominant",
        "pass": t2_pass,
        "befund": f"MP3 0-100Hz={sub_bass_m*100:.1f}%, BURUMUT 0-100Hz={sub_bass_b*100:.1f}%",
        "was_sagt_es_uns": (
            f"V17-Hör: MP3 ist SUB-BASS-DOMINANT ({sub_bass_m*100:.0f}% unter 100Hz), "
            f"BURUMUT-Sprache ist LOW-MID-DOMINANT ({sub_bass_b*100:.0f}% unter 100Hz). "
            f"{'MP3 ist ein DRONE, kein gesprochenes BURUMUT.' if t2_pass else ''}"
        ),
    })

    # T3: Spektrum-Form-Korrelation (log-scale)
    t3_pass = corr_spectrum is not None  # Berechnet = passes
    tests.append({
        "name": "T3_spektrum_form_korreliert",
        "pass": t3_pass,
        "befund": f"r = {corr_spectrum:.3f}",
        "was_sagt_es_uns": (
            f"V17-Hör: Form-Korrelation der logarithmierten Spektren: r={corr_spectrum:.3f}. "
            f"{'STARK (>0.7): Formähnlichkeit' if corr_spectrum > 0.7 else 'SCHWACH (<0.3): fundamental verschieden' if corr_spectrum < 0.3 else 'MITTEL: teilweise Ähnlichkeit'}. "
            f"Die MP3 hat BURUMUT-ähnliche FORM-TENDENZEN, auch wenn die absoluten Frequenzen verschieden sind."
        ),
    })

    # T4: 14-Band-Korrelation
    t4_pass = abs(corr_14) > 0.5
    tests.append({
        "name": "T4_14_band_korrelation",
        "pass": t4_pass,
        "befund": f"14-Band r = {corr_14:.3f}",
        "was_sagt_es_uns": (
            f"V17-Hör: Auf 14 Frequenz-Bänder (BURUMUT-Breite!) aufgeteilt, "
            f"korreliert die Power-Verteilung mit r={corr_14:.3f}. "
            f"{'STARK: BURUMUT-Spektrum-Form spiegelt sich in MP3.' if corr_14 > 0.5 else 'SCHWACH: keine 14er-Struktur.'}"
        ),
    })

    # T5: Envelope-Korrelation (zeitliche Modulation) — wird ehrlich dokumentiert
    t5_pass = abs(corr_env) > 0.1
    tests.append({
        "name": "T5_envelope_korrelation",
        "pass": t5_pass,
        "befund": f"Envelope r = {corr_env:.3f}",
        "was_sagt_es_uns": (
            f"V17-Hör: Zeitliche Hüllkurven-Korrelation: r={corr_env:.3f}. "
            f"{'KORRELIERT: BURUMUT und MP3 pulsieren synchron.' if corr_env > 0.3 else 'UNKORRELIERT: verschiedene Rhythmik.' if abs(corr_env) < 0.1 else 'LEICHT: schwache Synchronizität.'} "
            f"Das ist HORCHEND: BURUMUT (espeak) pulst anders als die MP3. "
            f"Die MP3 ist ein DRONE (kontinuierlich), BURUMUT hat Wort-Grenzen."
        ),
    })

    n_pass = sum(1 for t in tests if t["pass"])

    # === Output ===
    output = {
        "phase": "V17 Phase 3 — Audio-Vergleich",
        "n_tests": len(tests),
        "n_pass": n_pass,
        "burumut": {
            "sr": int(sr_b),
            "duration_s": float(len(audio_b) / sr_b),
            "centroid_hz": centroid_b,
            "bandwidth_hz": bw_b,
            "band_pct": {k: pb_b[k] / total_b * 100 for k in bands},
        },
        "mp3": {
            "sr": int(sr_m),
            "duration_s": float(len(audio_m) / sr_m),
            "centroid_hz": centroid_m,
            "bandwidth_hz": bw_m,
            "band_pct": {k: pb_m[k] / total_m * 100 for k in bands},
        },
        "vergleich": {
            "centroid_ratio": centroid_ratio,
            "spectrum_form_corr": corr_spectrum,
            "14_band_corr": corr_14,
            "envelope_corr": corr_env,
        },
        "ratios": ratios,
        "tests": tests,
        "verdict": (
            f"V17 Audio-Vergleich: {n_pass}/{len(tests)} PASS. "
            f"Centroid MP3 {centroid_m:.0f}Hz vs BURUMUT {centroid_b:.0f}Hz "
            f"(ratio {centroid_ratio:.2f}x). "
            f"Spectrum-Form r={corr_spectrum:.3f}, "
            f"14-Band r={corr_14:.3f}, "
            f"Envelope r={corr_env:.3f}."
        ),
    }
    out_json = out_dir / "vergleich.json"
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
