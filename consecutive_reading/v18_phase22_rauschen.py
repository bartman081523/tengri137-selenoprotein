"""
v18_phase22_rauschen.py
V18 PHASE 22 — FORENSISCH + RAUSCHEN-SCHICHT (Mid-Band füllen)

LEHRE AUS PHASE 20-21:
- Forensischer Ansatz: max_diff 24-36%
- Sub-Bass dominiert IMMER (75-99%)
- Centroid-Bandpass füllt 100-1000Hz-Band nicht genug

NEUE STRATEGIE:
- Sub-Bass-Träger: 30% (von 70%)
- Centroid-Layer: 30% (von 15%)
- NEU: Rauschen-Schicht (gefiltert 200-2000Hz) BURUMUT-moduliert: 40%
"""
import json
import sys
import numpy as np
from pathlib import Path
from scipy.io import wavfile
from scipy.signal import butter, lfilter, sawtooth
import subprocess
import os


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


def butter_bandpass(center_freq, fs, order=2, bw=150):
    nyq = 0.5 * fs
    low = max(20, center_freq - bw) / nyq
    high = min(nyq - 1, center_freq + bw) / nyq
    if low >= high:
        high = low + 0.01
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_range(lo, hi, fs, order=2):
    nyq = 0.5 * fs
    low = max(20, lo) / nyq
    high = min(nyq - 1, hi) / nyq
    if low >= high:
        high = low + 0.01
    b, a = butter(order, [low, high], btype='band')
    return b, a


def get_espeak_envelope(word, target_samples, fs):
    temp_file = "temp_espeak_v22.wav"
    try:
        subprocess.run(["espeak", "-v", "en-us", "-w", temp_file, word],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       timeout=10)
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


def main():
    print("=" * 80)
    print("V18 PHASE 22 — FORENSISCH + RAUSCHEN-SCHICHT")
    print("=" * 80)

    out_dir = Path("bbox/v18_20260707")
    sr = SAMPLE_RATE
    bands_def = [(0, 100), (100, 300), (300, 1000), (1000, 3000), (3000, 8000)]

    sr_orig, orig = wavfile.read("bbox/v17_20260707/tengri137_full.wav")
    orig = orig.astype(np.float32) / 32768.0
    spec_o = spektrum_analyse(orig, sr)
    freqs_long = np.fft.rfftfreq(8192, 1.0/sr)
    log_o = np.log10(spec_o + 1e-12)
    cent_o = float(np.sum(freqs_long * spec_o) / np.sum(spec_o))
    orig_bands = band_verteilung(spec_o, freqs_long, bands_def)

    # Balance
    SUB_BASS_AMP = 0.30
    PEAK2_AMP = 0.10
    CENTROID_AMP = 0.30
    NOISE_AMP = 0.40  # NEU

    # Rauschen (gefiltert 200-2000Hz) — global
    print("Generiere globales Rauschen (200-2000Hz)...")
    rng = np.random.default_rng(42)
    n_total = int(np.ceil(TOTAL_DURATION * SAMPLE_RATE))
    white_noise = rng.standard_normal(n_total).astype(np.float32) * 0.3
    b_noise, a_noise = butter_bandpass_range(200, 2000, sr)
    noise_layer = lfilter(b_noise, a_noise, white_noise).astype(np.float32)

    # Hochfrequenz-Rauschen (3000-8000Hz)
    print("Generiere Höhen-Rauschen (3000-8000Hz)...")
    hf_noise = rng.standard_normal(n_total).astype(np.float32) * 0.2
    b_hf, a_hf = butter_bandpass_range(3000, 8000, sr)
    hf_layer = lfilter(b_hf, a_hf, hf_noise).astype(np.float32)

    total_samples = n_total
    master_audio = np.zeros(total_samples, dtype=np.float32)
    time_array = np.arange(total_samples) / SAMPLE_RATE
    sub_bass_carrier = np.sin(2 * np.pi * F0_PEAK1 * time_array).astype(np.float32)

    for i, seg in enumerate(SEGMENTS_DATA):
        print(f"  Segment {i+1}/11 ({seg['word']}) -> Centroid {seg['centroid']:.0f}Hz")

        start_idx = int(i * SEGMENT_DURATION * SAMPLE_RATE)
        end_idx = int((i + 1) * SEGMENT_DURATION * SAMPLE_RATE)
        if i == 10:
            end_idx = total_samples
        seg_samples = end_idx - start_idx
        t_seg = time_array[start_idx:end_idx]

        peak2_osc = np.sin(2 * np.pi * seg['peak2'] * t_seg).astype(np.float32)
        saw_carrier = sawtooth(2 * np.pi * F0_PEAK1 * t_seg).astype(np.float32)
        espeak_env = get_espeak_envelope(seg['word'], seg_samples, sr)
        mod_strength = min(seg['mod_db'] / 10.0, 1.0)
        modulated_saw = (saw_carrier * (1.0 + espeak_env * mod_strength)).astype(np.float32)

        b, a = butter_bandpass(seg['centroid'], sr, bw=250)
        filtered_centroid_layer = lfilter(b, a, modulated_saw).astype(np.float32)

        # Rauschen mit BURUMUT-Hüllkurve moduliert
        noise_seg = noise_layer[start_idx:end_idx] * espeak_env

        # Segment-Mix
        segment_mix = (
            (sub_bass_carrier[start_idx:end_idx] * SUB_BASS_AMP) +
            (peak2_osc * PEAK2_AMP) +
            (filtered_centroid_layer * CENTROID_AMP) +
            (noise_seg * NOISE_AMP) +
            (hf_layer[start_idx:end_idx] * 0.05)
        ).astype(np.float32)

        master_audio[start_idx:end_idx] = segment_mix

    # Fade + Stille
    silence_idx = int(SILENCE_START * SAMPLE_RATE)
    fade_start = silence_idx - int(1.5 * SAMPLE_RATE)
    fade_curve = np.linspace(1.0, 0.0, silence_idx - fade_start).astype(np.float32)
    master_audio[fade_start:silence_idx] *= fade_curve
    master_audio[silence_idx:] = 0.0

    max_val = np.max(np.abs(master_audio))
    if max_val > 0:
        master_audio = master_audio / max_val * 0.95

    out_wav = out_dir / "synthese_v22_rauschen.wav"
    wavfile.write(out_wav, sr, (master_audio * 32767).astype(np.int16))

    spec_s = spektrum_analyse(master_audio, sr)
    log_s = np.log10(spec_s + 1e-12)
    r = float(np.corrcoef(log_s, log_o)[0, 1])
    synth_bands = band_verteilung(spec_s, freqs_long, bands_def)
    cent_s = float(np.sum(freqs_long * spec_s) / np.sum(spec_s))
    ratio = cent_s / cent_o
    max_diff = max(abs(synth_bands[b] - orig_bands[b]) for b in orig_bands)
    min_len = min(len(master_audio), len(orig))
    wave_corr = float(np.corrcoef(master_audio[:min_len], orig[:min_len])[0, 1])

    print()
    print("VERGLEICH")
    print("-" * 80)
    print(f"  r = {r:.3f}, wave_corr = {wave_corr:.3f}, ratio = {ratio:.3f}")
    for band in orig_bands:
        s = synth_bands[band]
        o = orig_bands[band]
        print(f"    {band:>10s}: Synth={s*100:5.1f}%  Orig={o*100:5.1f}%  Diff={(s-o)*100:+5.1f}%")

    # TDD
    print()
    print("TDD-TESTS")
    print("-" * 80)
    tests = []
    tests.append({"name": "T1_wav", "pass": bool(out_wav.exists()),
                  "befund": f"{out_wav.stat().st_size/1024:.0f}KB",
                  "was_sagt_es_uns": "WAV erstellt."})
    tests.append({"name": "T2_bands", "pass": bool(max_diff < 0.05),
                  "befund": f"max_diff={max_diff*100:.1f}%",
                  "was_sagt_es_uns": f"Band-Match: {'OK' if max_diff < 0.05 else 'ABWEICHUNG'}."})
    tests.append({"name": "T3_r", "pass": bool(r > 0.7),
                  "befund": f"r={r:.3f}",
                  "was_sagt_es_uns": f"Spektrum-Form: {'OK' if r > 0.7 else 'SCHWACH'}."})
    tests.append({"name": "T4_centroid", "pass": bool(0.85 <= ratio <= 1.15),
                  "befund": f"ratio={ratio:.3f}",
                  "was_sagt_es_uns": f"Centroid: {'ZENTRIERT' if 0.85 <= ratio <= 1.15 else 'daneben'}."})
    tests.append({"name": "T5_wave_corr", "pass": bool(wave_corr > 0.1),
                  "befund": f"wave_corr={wave_corr:.3f}",
                  "was_sagt_es_uns": f"Wellenform: {'NICHT NULL' if wave_corr > 0.1 else 'NULL'}."})

    n_pass = int(sum(1 for t in tests if t["pass"]))
    out_json = out_dir / "phase22_rauschen.json"
    output = {
        "phase": "V18 Phase 22 — Forensisch + Rauschen",
        "n_pass": n_pass,
        "n_tests": len(tests),
        "spektrum_r": float(r),
        "wave_corr": float(wave_corr),
        "centroid_ratio": float(ratio),
        "max_band_diff": float(max_diff),
        "synth_bands": synth_bands,
        "orig_bands": orig_bands,
        "balance": {"sub": SUB_BASS_AMP, "peak2": PEAK2_AMP, "centroid": CENTROID_AMP, "noise": NOISE_AMP},
        "tests": tests,
        "verdict": f"V18 Phase 22: {n_pass}/{len(tests)} PASS. r={r:.3f}, wave_corr={wave_corr:.3f}, ratio={ratio:.3f}.",
    }
    with open(out_json, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    for t in tests:
        mark = "✓" if t["pass"] else "✗"
        print(f"  {mark} {t['name']}: {t['was_sagt_es_uns']}")
    print()
    print(f"Output: {out_json}")
    print(f"Verdict: {output['verdict']}")
    return 0 if n_pass == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())
