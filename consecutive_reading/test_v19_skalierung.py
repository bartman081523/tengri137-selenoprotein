"""
test_v19_skalierung.py
V19 PHASE 0b — Skalierungs-Tests für die Architektur

HYPOTHESE: Das v17_synth.txt-Skript war ein Hypothesen-Skript mit:
- Sub-Bass: 0.70 (ZU HOCH)
- Peak2: 0.15
- Saw-moduliert: 0.15 (ZU NIEDRIG)

ZU TESTEN: Welche Skalierung bringt:
- Sub-Bass 60-70% (Original 63.5%)
- 1000-3000Hz 4-8% (Original 5.7%)
- Centroid ratio 0.85-1.15
- wave_corr > 0.1

METHODE: Iterative Skalierungstests
"""

import json
import sys
import numpy as np
from pathlib import Path
from scipy.io import wavfile
from scipy.signal import butter, lfilter, sawtooth
import subprocess
import itertools

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
    nyq = 0.5 * fs
    low = max(20, center_freq - 150) / nyq
    high = min(nyq - 1, center_freq + 150) / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def get_espeak_envelope(word, target_samples, fs):
    temp_file = "temp_espeak_skal.wav"
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


def synthese_mit_skalierung(sub_amp, peak2_amp, saw_amp, out_dir):
    """Synthese mit vorgegebener Skalierung"""
    n_total = int(np.ceil(TOTAL_DURATION * SAMPLE_RATE))
    master_audio = np.zeros(n_total, dtype=np.float32)
    time_array = np.arange(n_total) / SAMPLE_RATE

    sub_bass = np.sin(2 * np.pi * F0_PEAK1 * time_array).astype(np.float32)

    for i, seg in enumerate(SEGMENTS_DATA):
        start_idx = int(i * SEGMENT_DURATION * SAMPLE_RATE)
        end_idx = int((i + 1) * SEGMENT_DURATION * SAMPLE_RATE)
        if i == 10:
            end_idx = n_total
        seg_samples = end_idx - start_idx
        t_seg = time_array[start_idx:end_idx]

        peak2 = np.sin(2 * np.pi * seg['peak2'] * t_seg).astype(np.float32)
        saw = sawtooth(2 * np.pi * F0_PEAK1 * t_seg).astype(np.float32)
        espeak_env = get_espeak_envelope(seg['word'], seg_samples, SAMPLE_RATE)
        mod_strength = min(seg['mod_db'] / 10.0, 1.0)
        modulated_saw = saw * (1.0 + espeak_env * mod_strength * 0.5)
        b, a = butter_bandpass(seg['centroid'], SAMPLE_RATE)
        filtered = lfilter(b, a, modulated_saw).astype(np.float32)

        seg_mix = (
            sub_bass[start_idx:end_idx] * sub_amp +
            peak2 * peak2_amp +
            filtered * saw_amp
        ).astype(np.float32)

        master_audio[start_idx:end_idx] = seg_mix

    silence_idx = int(SILENCE_START * SAMPLE_RATE)
    fade_start = silence_idx - int(1.5 * SAMPLE_RATE)
    fade_curve = np.linspace(1.0, 0.0, silence_idx - fade_start).astype(np.float32)
    master_audio[fade_start:silence_idx] *= fade_curve
    master_audio[silence_idx:] = 0.0

    max_val = np.max(np.abs(master_audio))
    if max_val > 0:
        master_audio = master_audio / max_val * 0.95
    return master_audio


def evaluiere(synth_audio, orig):
    spec_o = spektrum_analyse(orig, SAMPLE_RATE)
    spec_s = spektrum_analyse(synth_audio, SAMPLE_RATE)
    freqs_long = np.fft.rfftfreq(8192, 1.0/SAMPLE_RATE)
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
    return r, ratio, max_diff, wave_corr, synth_bands, orig_bands


def main():
    sr_o, orig = wavfile.read("bbox/v17_20260707/tengri137_full.wav")
    orig = orig.astype(np.float32) / 32768.0

    # Skalierungs-Tests
    skalierungen = [
        # (sub, peak2, saw, name)
        (0.40, 0.10, 0.30, "sub40_p2_10_saw30"),
        (0.35, 0.10, 0.40, "sub35_p2_10_saw40"),
        (0.30, 0.10, 0.50, "sub30_p2_10_saw50"),
        (0.30, 0.05, 0.60, "sub30_p2_05_saw60"),
        (0.25, 0.05, 0.70, "sub25_p2_05_saw70"),
        (0.20, 0.05, 0.80, "sub20_p2_05_saw80"),
        (0.30, 0.10, 0.70, "sub30_p2_10_saw70"),
    ]

    print(f"{'Name':<25} {'r':<7} {'wave_corr':<10} {'ratio':<7} {'max_diff':<10} {'0-100Hz':<10} {'1000-3kHz':<10}")
    print("-" * 90)

    out_dir = Path("bbox/v18_20260707")
    results = []
    for sub_amp, peak2_amp, saw_amp, name in skalierungen:
        synth = synthese_mit_skalierung(sub_amp, peak2_amp, saw_amp, out_dir)
        r, ratio, max_diff, wave_corr, sb, ob = evaluiere(synth, orig)
        sub_pct = sb['0-100Hz'] * 100
        mh_pct = sb['1000-3000Hz'] * 100
        print(f"{name:<25} {r:.3f}   {wave_corr:+.4f}     {ratio:.3f}   {max_diff*100:5.1f}%     "
              f"{sub_pct:5.1f}%     {mh_pct:5.1f}%")
        results.append((name, r, ratio, max_diff, wave_corr, sub_pct, mh_pct))

        out_wav = out_dir / f"synthese_v19_skal_{name}.wav"
        wavfile.write(out_wav, SAMPLE_RATE, (synth * 32767).astype(np.int16))

    # Beste Skalierung identifizieren
    print()
    print("BESTE SKALIERUNG (höchste n_pass)")
    print("-" * 90)
    for name, r, ratio, max_diff, wave_corr, sub_pct, mh_pct in results:
        n_pass = (
            (0.60 <= sub_pct/100 <= 0.70) +
            (0.04 <= mh_pct/100 <= 0.08) +
            (r > 0.7) +
            (0.85 <= ratio <= 1.15) +
            (wave_corr > 0.1) +
            (max_diff < 0.05)
        )
        print(f"  {name}: {n_pass}/6 pass")


if __name__ == "__main__":
    main()
