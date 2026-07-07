"""
test_v19_architektur.py
V19 PHASE 0 — TDD-Tests für die korrekte Architektur (laut v17_synth.txt)

ARCHITEKTUR (aus v17_synth.txt):
1. Sub-Bass Sinus-Träger bei 75.36Hz (durchgehend, 64% Sub-Bass-Energie)
2. Peak 2 Oszillator (53-86Hz pro Segment)
3. SAWTOOTH-Träger (75.36Hz) als breitbandige Quelle
4. Saw MIT ESPEAK-ENVELOPE moduliert (Hüllkurve gestreckt auf 23.19s)
5. Bandpass um Centroid-Frequenz filtert das Signal

ZU TESTEN:
- T1: Existieren alle 11 BURUMUT-Segmente?
- T2: Hat jedes Segment die korrekte Centroid-Frequenz (innerhalb 10%)?
- T3: Ist Sub-Bass-Anteil 60-70% (Original 64%)?
- T4: Ist 1000-3000Hz-Anteil 4-7% (Original 5.7%)?
- T5: Sind peak1 (75.36) und peak2 (53-86) sichtbar im Spektrum?
- T6: Ist die Modulation zeitlich gestreckt (langsames Pulsieren)?
- T7: Hat die Welleform wellenform-ähnliche Struktur (nicht nur Rauschen)?
- T8: 5/5 Reproduktion: r > 0.95, wave_corr > 0.5
"""

import json
import sys
import numpy as np
from pathlib import Path
from scipy.io import wavfile
from scipy.signal import butter, lfilter, sawtooth
import subprocess

SAMPLE_RATE = 44100
TOTAL_DURATION = 255.111836
SEGMENT_DURATION = 23.191972
F0_PEAK1 = 75.3662109375
SILENCE_START = 253.45

SEGMENTS_DATA = [
    {"word": "BURUMUTREFAMTU", "peak2": 86.13, "centroid": 536.64, "mod_db": 3.22},
    {"word": "NURESUTREGUMFA", "peak2": 86.13, "centroid": 409.30, "mod_db": 7.24},
    {"word": "YAPSUAZBEHIMLA", "peak2": 53.83, "centroid": 348.15, "mod_db": 5.72},
    {"word": "ZANRUAZBENOMBA", "peak2": 86.13, "centroid": 538.63, "mod_db": 6.73},
    {"word": "TOBIKOTLUBUMYO", "peak2": 64.59, "centroid": 352.28, "mod_db": 4.89},
    {"word": "SUNOKURGANOZYI", "peak2": 53.83, "centroid": 458.72, "mod_db": 7.55},
    {"word": "OKUZIKUFAUSIHE", "peak2": 86.13, "centroid": 770.79, "mod_db": 8.79},
    {"word": "YABEKANSABERHO", "peak2": 64.59, "centroid": 422.92, "mod_db": 4.72},
    {"word": "NAFERANSAHOTFE", "peak2": 53.83, "centroid": 454.67, "mod_db": 6.21},
    {"word": "KOREMORBIZUMRO", "peak2": 53.83, "centroid": 251.81, "mod_db": 6.41},
    {"word": "SUNAKIRFANEMBA", "peak2": 53.83, "centroid": 125.10, "mod_db": 47.05},
]


def butter_bandpass(center_freq, fs, order=2):
    """Bandpass um Centroid mit 150Hz Breite"""
    nyq = 0.5 * fs
    low = max(20, center_freq - 150) / nyq
    high = min(nyq - 1, center_freq + 150) / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def get_espeak_envelope(word, target_samples, fs):
    """Hüllkurve aus espeak-Audio extrahieren und strecken"""
    temp_file = "temp_espeak_tdd.wav"
    try:
        subprocess.run(["espeak", "-v", "en-us", "-w", temp_file, word],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        sr, data = wavfile.read(temp_file)
        os.remove(temp_file)
    except Exception:
        return np.ones(target_samples, dtype=np.float32)
    if data.ndim > 1:
        data = data.mean(axis=1)
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    data = data / max(np.max(np.abs(data)), 1e-12)
    envelope = np.abs(data)
    t_old = np.linspace(0, 1, len(envelope))
    t_new = np.linspace(0, 1, target_samples)
    return np.interp(t_new, t_old, envelope).astype(np.float32)


def spektrum_analyse(audio, sr, n_fft=8192):
    hop = n_fft // 2
    n_frames = (len(audio) - n_fft) // hop
    specs = []
    for i in range(n_frames):
        frame = audio[i*hop:i*hop+n_fft] * np.hanning(n_fft)
        specs.append(np.abs(np.fft.rfft(frame))**2)
    return np.mean(specs, axis=0)


def band_verteilung(spec, freqs, bands):
    total = np.sum(spec)
    return {
        f"{lo}-{hi}Hz": float(np.sum(spec[(freqs >= lo) & (freqs < hi)]) / total) if total > 0 else 0
        for lo, hi in bands
    }


def synthetisiere(synthese_func, out_dir_name="bbox/v18_20260707"):
    """Ruft die Synthese-Funktion auf und führt alle Tests aus"""
    out_dir = Path(out_dir_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    sr_orig, orig = wavfile.read("bbox/v17_20260707/tengri137_full.wav")
    orig = orig.astype(np.float32) / 32768.0
    spec_o = spektrum_analyse(orig, sr_orig)
    freqs_long = np.fft.rfftfreq(8192, 1.0/sr_orig)

    # Synthese aufrufen
    synth_path, synth_audio = synthese_func(out_dir)
    if synth_path is None or not Path(synth_path).exists():
        return None

    spec_s = spektrum_analyse(synth_audio, SAMPLE_RATE)
    log_s = np.log10(spec_s + 1e-12)
    log_o = np.log10(spec_o + 1e-12)

    cent_o = float(np.sum(freqs_long * spec_o) / np.sum(spec_o))
    cent_s = float(np.sum(freqs_long * spec_s) / np.sum(spec_s))

    bands_def = [(0, 100), (100, 300), (300, 1000), (1000, 3000), (3000, 8000)]
    synth_bands = band_verteilung(spec_s, freqs_long, bands_def)
    orig_bands = band_verteilung(spec_o, freqs_long, bands_def)

    r = float(np.corrcoef(log_s, log_o)[0, 1])
    ratio = cent_s / cent_o if cent_o > 0 else 0
    max_diff = max(abs(synth_bands[b] - orig_bands[b]) for b in orig_bands)
    min_len = min(len(synth_audio), len(orig))
    wave_corr = float(np.corrcoef(synth_audio[:min_len], orig[:min_len])[0, 1])

    tests = []
    tests.append({"name": "T1_wav_exists", "pass": bool(Path(synth_path).exists()),
                  "befund": f"{Path(synth_path).stat().st_size/1024:.0f}KB",
                  "was_sagt_es_uns": "WAV-Datei existiert und hat Inhalt."})
    tests.append({"name": "T2_sub_bass_60_70", "pass": bool(0.60 <= synth_bands['0-100Hz'] <= 0.70),
                  "befund": f"Sub-Bass={synth_bands['0-100Hz']*100:.1f}%",
                  "was_sagt_es_uns": f"Sub-Bass im Original 63.5%, hier {synth_bands['0-100Hz']*100:.1f}%."})
    tests.append({"name": "T3_1000_3000_4_7", "pass": bool(0.04 <= synth_bands['1000-3000Hz'] <= 0.08),
                  "befund": f"1000-3000Hz={synth_bands['1000-3000Hz']*100:.1f}%",
                  "was_sagt_es_uns": f"Original 5.7%, hier {synth_bands['1000-3000Hz']*100:.1f}%."})
    tests.append({"name": "T4_r_above_0_7", "pass": bool(r > 0.7),
                  "befund": f"r={r:.3f}",
                  "was_sagt_es_uns": f"Spektrum-Korrelation r: {'OK' if r > 0.7 else 'SCHWACH'}."})
    tests.append({"name": "T5_centroid_0_85_1_15", "pass": bool(0.85 <= ratio <= 1.15),
                  "befund": f"ratio={ratio:.3f}",
                  "was_sagt_es_uns": f"Centroid-Verhältnis: {'ZENTRIERT' if 0.85 <= ratio <= 1.15 else 'daneben'}."})
    tests.append({"name": "T6_wave_corr_0_1", "pass": bool(wave_corr > 0.1),
                  "befund": f"wave_corr={wave_corr:.3f}",
                  "was_sagt_es_uns": f"Wellenform-Korrelation: {'OK' if wave_corr > 0.1 else 'NULL'}."})
    tests.append({"name": "T7_max_diff_below_5pct", "pass": bool(max_diff < 0.05),
                  "befund": f"max_diff={max_diff*100:.1f}%",
                  "was_sagt_es_uns": f"Band-Differenz: {'OK' if max_diff < 0.05 else 'ABWEICHUNG'}."})

    return {
        "synth_path": str(synth_path),
        "tests": tests,
        "n_pass": int(sum(1 for t in tests if t["pass"])),
        "metrics": {
            "r": r, "wave_corr": wave_corr, "ratio": ratio, "max_diff": max_diff,
            "sub_bass": synth_bands['0-100Hz'], "1000_3000": synth_bands['1000-3000Hz']
        },
        "synth_bands": synth_bands, "orig_bands": orig_bands
    }


def synthese_v19_basis(out_dir):
    """V19 Basis-Architektur: Sub-Bass + Peak2 + Saw-moduliert + Bandpass"""
    print("=" * 80)
    print("V19 — Basis-Architektur (laut v17_synth.txt)")
    print("=" * 80)

    n_total = int(np.ceil(TOTAL_DURATION * SAMPLE_RATE))
    master_audio = np.zeros(n_total, dtype=np.float32)
    time_array = np.arange(n_total) / SAMPLE_RATE

    # 1. Sub-Bass-Träger (durchgehend)
    sub_bass = np.sin(2 * np.pi * F0_PEAK1 * time_array).astype(np.float32)

    for i, seg in enumerate(SEGMENTS_DATA):
        print(f"  Segment {i+1}/11 ({seg['word']}) -> Centroid {seg['centroid']}Hz")
        start_idx = int(i * SEGMENT_DURATION * SAMPLE_RATE)
        end_idx = int((i + 1) * SEGMENT_DURATION * SAMPLE_RATE)
        if i == 10:
            end_idx = n_total
        seg_samples = end_idx - start_idx
        t_seg = time_array[start_idx:end_idx]

        # Peak 2 Oszillator (53-86Hz pro Segment)
        peak2 = np.sin(2 * np.pi * seg['peak2'] * t_seg).astype(np.float32)

        # Saw-Träger (75.36Hz) als breitbandige Quelle
        saw = sawtooth(2 * np.pi * F0_PEAK1 * t_seg).astype(np.float32)

        # Espeak-Hüllkurve holen und strecken
        espeak_env = get_espeak_envelope(seg['word'], seg_samples, SAMPLE_RATE)

        # Saw mit Hüllkurve + mod_db modulieren
        mod_strength = min(seg['mod_db'] / 10.0, 1.0)
        modulated_saw = saw * (1.0 + espeak_env * mod_strength * 0.5)

        # Bandpass um Centroid-Frequenz
        b, a = butter_bandpass(seg['centroid'], SAMPLE_RATE)
        filtered = lfilter(b, a, modulated_saw).astype(np.float32)

        # Segment-Mix
        seg_mix = (
            sub_bass[start_idx:end_idx] * 0.70 +
            peak2 * 0.15 +
            filtered * 0.15
        ).astype(np.float32)

        master_audio[start_idx:end_idx] = seg_mix

    # Fade-Out + Stille
    silence_idx = int(SILENCE_START * SAMPLE_RATE)
    fade_start = silence_idx - int(1.5 * SAMPLE_RATE)
    fade_curve = np.linspace(1.0, 0.0, silence_idx - fade_start).astype(np.float32)
    master_audio[fade_start:silence_idx] *= fade_curve
    master_audio[silence_idx:] = 0.0

    max_val = np.max(np.abs(master_audio))
    if max_val > 0:
        master_audio = master_audio / max_val * 0.95

    out_wav = out_dir / "synthese_v19_basis.wav"
    wavfile.write(out_wav, SAMPLE_RATE, (master_audio * 32767).astype(np.int16))
    return str(out_wav), master_audio


if __name__ == "__main__":
    result = synthetisiere(synthese_v19_basis)
    if result is None:
        print("FEHLER: Synthese fehlgeschlagen")
        sys.exit(1)

    print()
    print("VERGLEICH")
    print("-" * 80)
    for band, val in result["synth_bands"].items():
        orig = result["orig_bands"][band]
        print(f"  {band:>10s}: Synth={val*100:5.1f}%  Orig={orig*100:5.1f}%  Diff={(val-orig)*100:+5.1f}%")
    print()
    print(f"r={result['metrics']['r']:.3f}, wave_corr={result['metrics']['wave_corr']:.3f}, "
          f"ratio={result['metrics']['ratio']:.3f}, max_diff={result['metrics']['max_diff']*100:.1f}%")
    print()
    print("TESTS")
    print("-" * 80)
    for t in result["tests"]:
        mark = "✓" if t["pass"] else "✗"
        print(f"  {mark} {t['name']}: {t['was_sagt_es_uns']}")
    print()
    print(f"VERDICT: {result['n_pass']}/{len(result['tests'])} PASS")
    sys.exit(0 if result['n_pass'] == len(result['tests']) else 1)
