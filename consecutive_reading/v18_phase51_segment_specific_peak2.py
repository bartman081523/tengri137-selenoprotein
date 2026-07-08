"""
v18_phase51_segment_specific_peak2.py
V18 PHASE 51 — Pro Segment eigener peak2-Träger

LEHRE AUS PHASE 50:
- 3/5 PASS, r=0.861, max_diff 2.3%
- Centroid ratio 0.748
- Bisher: nur peak1 (75Hz) als Träger für ALLE Segmente

ZIEL: Pro Segment peak1 UND peak2 als Träger verwenden
- Original: jedes Segment hat peak2 zwischen 53-86Hz
"""
import json
import sys
import numpy as np
from pathlib import Path
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import subprocess


SAMPLE_RATE = 44100
TOTAL_DURATION = 255.111836
SEGMENT_DURATION = 23.191972
SILENCE_START = 253.45

# Peak2 pro Segment (aus V17 Spanda-Daten)
SEGMENTS_DATA = [
    {"word": "BURUMUTREFAMTU", "peak1": 75.37, "peak2": 86.13, "centroid": 536.64, "mod_db": 3.22},
    {"word": "NURESUTREGUMFA", "peak1": 75.37, "peak2": 86.13, "centroid": 409.30, "mod_db": 7.24},
    {"word": "YAPSUAZBEHIMLA", "peak1": 75.37, "peak2": 53.83, "centroid": 348.15, "mod_db": 5.72},
    {"word": "ZANRUAZBENOMBA", "peak1": 75.37, "peak2": 86.13, "centroid": 538.63, "mod_db": 6.73},
    {"word": "TOBIKOTLUBUMYO", "peak1": 75.37, "peak2": 64.60, "centroid": 352.28, "mod_db": 4.89},
    {"word": "SUNOKURGANOZYI", "peak1": 75.37, "peak2": 53.83, "centroid": 458.72, "mod_db": 7.55},
    {"word": "OKUZIKUFAUSIHE", "peak1": 75.37, "peak2": 86.13, "centroid": 770.79, "mod_db": 8.79},
    {"word": "YABEKANSABERHO", "peak1": 75.37, "peak2": 64.60, "centroid": 422.92, "mod_db": 4.72},
    {"word": "NAFERANSAHOTFE", "peak1": 75.37, "peak2": 53.83, "centroid": 454.67, "mod_db": 6.21},
    {"word": "KOREMORBIZUMRO", "peak1": 75.37, "peak2": 53.83, "centroid": 251.81, "mod_db": 6.41},
    {"word": "SUNAKIRFANEMBA", "peak1": 75.37, "peak2": 53.83, "centroid": 125.10, "mod_db": 47.05},
]


def butter_bandpass_range(lo, hi, fs, order=2):
    nyq = 0.5 * fs
    low = max(20, lo) / nyq
    high = min(nyq - 1, hi) / nyq
    if low >= high:
        high = low + 0.01
    b, a = butter(order, [low, high], btype='band')
    return b, a


def get_espeak_envelope(word, target_samples, fs):
    temp_file = "temp_espeak_v51.wav"
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
    print("V18 PHASE 51 — Peak2 pro Segment")
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

    SUB_BASS_AMP = 0.35
    PEAK2_AMP = 0.15  # Neu: pro Segment peak2 als Träger
    MID_NOISE_AMP = 0.50
    MID_HIGH_NOISE_AMP = 1.40
    CENTROID_AMP = 0.20
    HIGH_AMP = 0.40
    MID_TONE_AMP = 0.10

    print("Generiere Rauschen-Schichten...")
    rng = np.random.default_rng(42)
    n_total = int(np.ceil(TOTAL_DURATION * SAMPLE_RATE))
    white_noise_1 = rng.standard_normal(n_total).astype(np.float32) * 0.3
    b_mid, a_mid = butter_bandpass_range(300, 1000, sr)
    mid_noise = lfilter(b_mid, a_mid, white_noise_1).astype(np.float32)

    white_noise_2 = rng.standard_normal(n_total).astype(np.float32) * 0.3
    b_mh, a_mh = butter_bandpass_range(1000, 3000, sr)
    mid_high_noise = lfilter(b_mh, a_mh, white_noise_2).astype(np.float32)

    hf_noise = rng.standard_normal(n_total).astype(np.float32) * 0.3
    b_hf, a_hf = butter_bandpass_range(3000, 12000, sr)
    hf_layer = lfilter(b_hf, a_hf, hf_noise).astype(np.float32)

    total_samples = n_total
    master_audio = np.zeros(total_samples, dtype=np.float32)
    time_array = np.arange(total_samples) / SAMPLE_RATE

    for i, seg in enumerate(SEGMENTS_DATA):
        print(f"  Segment {i+1}/11 ({seg['word']}) - peak2={seg['peak2']}Hz")

        start_idx = int(i * SEGMENT_DURATION * SAMPLE_RATE)
        end_idx = int((i + 1) * SEGMENT_DURATION * SAMPLE_RATE)
        if i == 10:
            end_idx = total_samples
        seg_samples = end_idx - start_idx
        t_seg = time_array[start_idx:end_idx]

        espeak_env = get_espeak_envelope(seg['word'], seg_samples, sr)
        mod_strength = min(seg['mod_db'] / 10.0, 1.0)

        # Peak1 Träger (75.37Hz für alle)
        peak1_carrier = np.sin(2 * np.pi * seg['peak1'] * t_seg).astype(np.float32)
        am_peak1 = peak1_carrier * (1.0 + espeak_env * mod_strength * 0.5)

        # Peak2 Träger (pro Segment verschieden)
        peak2_carrier = np.sin(2 * np.pi * seg['peak2'] * t_seg).astype(np.float32)
        am_peak2 = peak2_carrier * (1.0 + espeak_env * mod_strength * 0.3)

        # Centroid-Sinus
        centroid_tone = np.sin(2 * np.pi * seg['centroid'] * t_seg).astype(np.float32)
        mod_centroid = centroid_tone * (1.0 + espeak_env * mod_strength * 0.4)

        # Rausch-Schichten
        mid_seg = mid_noise[start_idx:end_idx] * (0.3 + espeak_env * mod_strength * 0.7)
        mid_high_seg = mid_high_noise[start_idx:end_idx] * (0.3 + espeak_env * mod_strength * 0.7)
        hf_seg = hf_layer[start_idx:end_idx] * espeak_env * 0.3

        # Mid-Tones (400/600/800Hz)
        mid_tone_400 = np.sin(2 * np.pi * 400 * t_seg).astype(np.float32)
        mid_tone_600 = np.sin(2 * np.pi * 600 * t_seg).astype(np.float32)
        mid_tone_800 = np.sin(2 * np.pi * 800 * t_seg).astype(np.float32)
        mid_tone_mix = (mid_tone_400 + mid_tone_600 + mid_tone_800) / 3.0

        segment_mix = (
            (am_peak1 * SUB_BASS_AMP) +
            (am_peak2 * PEAK2_AMP) +
            (mid_seg * MID_NOISE_AMP) +
            (mid_high_seg * MID_HIGH_NOISE_AMP) +
            (mod_centroid * CENTROID_AMP) +
            (hf_seg * HIGH_AMP) +
            (mid_tone_mix * MID_TONE_AMP)
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

    out_wav = out_dir / "synthese_v51_peak2_pro_seg.wav"
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
    out_json = out_dir / "phase51_peak2_pro_seg.json"
    output = {
        "phase": "V18 Phase 51 — Peak2 pro Segment",
        "n_pass": n_pass,
        "n_tests": len(tests),
        "spektrum_r": float(r),
        "wave_corr": float(wave_corr),
        "centroid_ratio": float(ratio),
        "max_band_diff": float(max_diff),
        "synth_bands": synth_bands,
        "orig_bands": orig_bands,
        "balance": {"sub": SUB_BASS_AMP, "peak2": PEAK2_AMP, "mid_noise": MID_NOISE_AMP, "mid_high_noise": MID_HIGH_NOISE_AMP, "centroid": CENTROID_AMP, "high": HIGH_AMP, "mid_tone": MID_TONE_AMP, "high_band": "3000-12000Hz", "per_segment_peak2": True},
        "tests": tests,
        "verdict": f"V18 Phase 51: {n_pass}/{len(tests)} PASS. r={r:.3f}, wave_corr={wave_corr:.3f}, ratio={ratio:.3f}.",
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
