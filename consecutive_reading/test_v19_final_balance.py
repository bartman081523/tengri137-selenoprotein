"""
test_v19_final_balance.py
V19 PHASE 0f — Finale Balance-Suche mit Vokalen + Didgeridoo

BESTE BASIS aus test_v19_saw_bei_centroid.py:
- sub50_p2_10_saw30 SAW BEI CENTROID: Centroid 1.015, max_diff 7.8%

NEUE ZIELE mit Vokalen + Didgeridoo:
- Sub-Bass 0.40-0.50
- 1000-3000Hz 4-7% (Original 5.7%)
- Centroid ratio 0.85-1.15
- r > 0.7
- wave_corr > 0.1
- max_diff < 5%
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
    {"word": "BURUMUTREFAMTU", "peak2": 86.13, "centroid": 536.64, "mod_db": 3.22,
     "vowel_freqs": [370, 990]},
    {"word": "NURESUTREGUMFA", "peak2": 86.13, "centroid": 409.30, "mod_db": 7.24,
     "vowel_freqs": [370, 530, 990]},
    {"word": "YAPSUAZBEHIMLA", "peak2": 53.83, "centroid": 348.15, "mod_db": 5.72,
     "vowel_freqs": [730, 370, 270]},
    {"word": "ZANRUAZBENOMBA", "peak2": 86.13, "centroid": 538.63, "mod_db": 6.73,
     "vowel_freqs": [730, 370, 530, 570]},
    {"word": "TOBIKOTLUBUMYO", "peak2": 64.59, "centroid": 352.28, "mod_db": 4.89,
     "vowel_freqs": [570, 270, 370, 700]},
    {"word": "SUNOKURGANOZYI", "peak2": 53.83, "centroid": 458.72, "mod_db": 7.55,
     "vowel_freqs": [370, 570, 730]},
    {"word": "OKUZIKUFAUSIHE", "peak2": 86.13, "centroid": 770.79, "mod_db": 8.79,
     "vowel_freqs": [570, 370, 270, 730, 530]},
    {"word": "YABEKANSABERHO", "peak2": 64.59, "centroid": 422.92, "mod_db": 4.72,
     "vowel_freqs": [730, 530, 570]},
    {"word": "NAFERANSAHOTFE", "peak2": 53.83, "centroid": 454.67, "mod_db": 6.21,
     "vowel_freqs": [730, 530, 570]},
    {"word": "KOREMORBIZUMRO", "peak2": 53.83, "centroid": 251.81, "mod_db": 6.41,
     "vowel_freqs": [570, 530, 270, 370]},
    {"word": "SUNAKIRFANEMBA", "peak2": 53.83, "centroid": 125.10, "mod_db": 47.05,
     "vowel_freqs": [370, 730, 270, 530]},
]

VOWEL_F2 = 990  # Standard F2 für /u/


def get_espeak_envelope(word, target_samples, fs):
    temp_file = "temp_espeak_fb.wav"
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


def synthese_final(sub_amp, didg_amp, vowel_amp, saw_amp, peak2_amp, out_dir):
    n_total = int(np.ceil(TOTAL_DURATION * SAMPLE_RATE))
    master_audio = np.zeros(n_total, dtype=np.float32)
    time_array = np.arange(n_total) / SAMPLE_RATE

    sub_bass = np.sin(2 * np.pi * F0_PEAK1 * time_array).astype(np.float32)

    # Didgeridoo: obertonreicher Träger
    didgeridoo = (
        np.sin(2 * np.pi * F0_PEAK1 * time_array) * 0.5 +
        sawtooth(2 * np.pi * F0_PEAK1 * time_array) * 0.25 +
        np.sin(2 * np.pi * 2 * F0_PEAK1 * time_array) * 0.3 +
        np.sin(2 * np.pi * 3 * F0_PEAK1 * time_array) * 0.15 +
        np.sin(2 * np.pi * 4 * F0_PEAK1 * time_array) * 0.1
    ).astype(np.float32)
    didgeridoo = didgeridoo / max(np.max(np.abs(didgeridoo)), 1e-12)

    for i, seg in enumerate(SEGMENTS_DATA):
        start_idx = int(i * SEGMENT_DURATION * SAMPLE_RATE)
        end_idx = int((i + 1) * SEGMENT_DURATION * SAMPLE_RATE)
        if i == 10:
            end_idx = n_total
        seg_samples = end_idx - start_idx
        t_seg = time_array[start_idx:end_idx]

        espeak_env = get_espeak_envelope(seg['word'], seg_samples, SAMPLE_RATE)
        mod_strength = min(seg['mod_db'] / 10.0, 1.0)

        peak2 = np.sin(2 * np.pi * seg['peak2'] * t_seg).astype(np.float32)

        # Vokale: Sinus bei Vokal-Formanten
        vowel_signal = np.zeros(seg_samples, dtype=np.float32)
        for freq in seg['vowel_freqs']:
            vowel_signal += np.sin(2 * np.pi * freq * t_seg).astype(np.float32)
        if np.max(np.abs(vowel_signal)) > 0:
            vowel_signal = vowel_signal / np.max(np.abs(vowel_signal))
        vowel_mod = vowel_signal * (1.0 + espeak_env * mod_strength * 0.5)

        # Saw bei Centroid
        saw = sawtooth(2 * np.pi * seg['centroid'] * t_seg).astype(np.float32)
        saw_mod = saw * (1.0 + espeak_env * mod_strength * 0.3)

        seg_mix = (
            sub_bass[start_idx:end_idx] * sub_amp +
            didgeridoo[start_idx:end_idx] * didg_amp +
            peak2 * peak2_amp +
            vowel_mod * vowel_amp +
            saw_mod * saw_amp
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

    out_dir = Path("bbox/v18_20260707")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("FINALE BALANCE (Vokale + Didgeridoo + Saw bei Centroid)")
    print(f"{'Name':<35} {'r':<7} {'wave':<10} {'ratio':<7} {'diff':<8} {'0-100':<8} {'1-3k':<8} {'3-8k':<8}")
    print("-" * 100)

    tests = [
        # sub, didg, vow, saw, p2
        (0.45, 0.15, 0.20, 0.20, 0.05, "balanced_A"),
        (0.40, 0.20, 0.25, 0.20, 0.05, "balanced_B"),
        (0.40, 0.15, 0.30, 0.20, 0.05, "balanced_C"),
        (0.35, 0.20, 0.30, 0.20, 0.05, "balanced_D"),
        (0.40, 0.10, 0.35, 0.20, 0.05, "balanced_E"),
        (0.30, 0.25, 0.35, 0.20, 0.05, "balanced_F"),
        (0.35, 0.15, 0.40, 0.20, 0.05, "balanced_G"),
        (0.30, 0.20, 0.40, 0.20, 0.05, "balanced_H"),
        (0.25, 0.25, 0.40, 0.20, 0.05, "balanced_I"),
        (0.30, 0.20, 0.45, 0.15, 0.05, "balanced_J"),
    ]

    best_n_pass = 0
    best_name = ""
    for sub, didg, vow, saw, p2, name in tests:
        synth = synthese_final(sub, didg, vow, saw, p2, out_dir)
        r, ratio, max_diff, wave_corr, sb, ob = evaluiere(synth, orig)

        n_pass = (
            (0.60 <= sb['0-100Hz'] <= 0.70) +
            (0.04 <= sb['1000-3000Hz'] <= 0.08) +
            (r > 0.7) +
            (0.85 <= ratio <= 1.15) +
            (wave_corr > 0.1) +
            (max_diff < 0.05)
        )

        if n_pass > best_n_pass:
            best_n_pass = n_pass
            best_name = name

        print(f"{name:<35} {r:.3f}   {wave_corr:+.4f}   {ratio:.3f}   {max_diff*100:5.1f}%   "
              f"{sb['0-100Hz']*100:5.1f}%   {sb['1000-3000Hz']*100:5.1f}%   "
              f"{sb['3000-8000Hz']*100:5.1f}%  [{n_pass}/6]")

        out_wav = out_dir / f"synthese_v19_fb_{name}.wav"
        wavfile.write(out_wav, SAMPLE_RATE, (synth * 32767).astype(np.int16))

    print()
    print(f"BEST: {best_name} mit {best_n_pass}/6 Tests")


if __name__ == "__main__":
    main()
