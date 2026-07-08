"""
v18_phase25_sub_bass_pulse.py
V18 PHASE 25 — Sub-Bass-Puls (Sinus mit AM-Modulation)

LEHRE AUS PHASE 24:
- Centroid ratio 1.118 (ZENTRIERT)
- 23.5% Sub-Bass (zu wenig), 43% 100-300Hz (zu viel)
- Sägezahn hat 1/f-Spektrum → zu viel 100-300Hz

NEUE STRATEGIE:
- Sinus-Sub-Bass-Träger (75.36Hz) mit AM-Modulation durch BURUMUT-Hüllkurve
- AM erzeugt 75Hz-Träger + Seitenbänder bei 75±f_mod
- f_mod = espeak-Hüllkurven-Frequenz (10-100Hz)
- 75Hz Träger dominiert → 60-70% Sub-Bass
- Seitenbänder in 100-300Hz-Band (gewünscht)
- Zusätzlich: Centroid-Bandpass auf 2. Harmonische (150Hz)
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


def butter_bandpass(center_freq, fs, order=2, bw=150):
    nyq = 0.5 * fs
    low = max(20, center_freq - bw) / nyq
    high = min(nyq - 1, center_freq + bw) / nyq
    if low >= high:
        high = low + 0.01
    b, a = butter(order, [low, high], btype='band')
    return b, a


def get_espeak_envelope(word, target_samples, fs):
    temp_file = "temp_espeak_v25.wav"
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


def espeak_zu_modulationsfrequenz(word, target_samples, fs, base_freq=10):
    """espeak-Hüllkurve als Modulator-Signal im base_freq bis 100Hz-Bereich."""
    env = get_espeak_envelope(word, target_samples, fs)
    # Map env (0-1) zu Modulations-Frequenz (10-100Hz)
    # Höhere env-Werte → höhere Modulations-Frequenz
    # Indem wir env direkt mit einem Sinus bei freq mischen
    t = np.arange(target_samples) / fs
    mod_freq = base_freq + env * 90  # 10-100Hz
    modulator = np.sin(2 * np.pi * np.cumsum(mod_freq) / fs).astype(np.float32) * env
    return modulator


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
    print("V18 PHASE 25 — Sub-Bass-Puls (Sinus mit AM-Modulation)")
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

    SUB_BASS_AMP = 0.60  # Träger dominiert
    HARMONIC_AMP = 0.30  # 2. Harmonische (150Hz)
    MID_AMP = 0.20  # Mitten
    HIGH_AMP = 0.10  # Höhen

    total_samples = int(np.ceil(TOTAL_DURATION * SAMPLE_RATE))
    master_audio = np.zeros(total_samples, dtype=np.float32)
    time_array = np.arange(total_samples) / SAMPLE_RATE

    # Träger
    sub_bass_carrier = np.sin(2 * np.pi * F0_PEAK1 * time_array).astype(np.float32)
    harmonic_carrier = np.sin(2 * np.pi * 2 * F0_PEAK1 * time_array).astype(np.float32)  # 150Hz

    for i, seg in enumerate(SEGMENTS_DATA):
        print(f"  Segment {i+1}/11 ({seg['word']})")

        start_idx = int(i * SEGMENT_DURATION * SAMPLE_RATE)
        end_idx = int((i + 1) * SEGMENT_DURATION * SAMPLE_RATE)
        if i == 10:
            end_idx = total_samples
        seg_samples = end_idx - start_idx
        t_seg = time_array[start_idx:end_idx]

        espeak_env = get_espeak_envelope(seg['word'], seg_samples, sr)
        mod_strength = min(seg['mod_db'] / 10.0, 1.0)

        # AM-modulierter Sub-Bass: Träger * (1 + espeak_env * mod)
        am_sub = sub_bass_carrier[start_idx:end_idx] * (1.0 + espeak_env * mod_strength)
        am_harmonic = harmonic_carrier[start_idx:end_idx] * (1.0 + espeak_env * mod_strength * 0.5)

        # Centroid-Ton (Sinus bei seg.centroid)
        centroid_tone = np.sin(2 * np.pi * seg['centroid'] * t_seg).astype(np.float32)
        # Moduliert mit espeak_env
        mod_centroid = centroid_tone * (1.0 + espeak_env * mod_strength * 0.3)

        segment_mix = (
            (am_sub * SUB_BASS_AMP) +
            (am_harmonic * HARMONIC_AMP) +
            (mod_centroid * MID_AMP)
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

    out_wav = out_dir / "synthese_v25_sub_bass_pulse.wav"
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
    out_json = out_dir / "phase25_sub_bass_pulse.json"
    output = {
        "phase": "V18 Phase 25 — Sub-Bass-Puls",
        "n_pass": n_pass,
        "n_tests": len(tests),
        "spektrum_r": float(r),
        "wave_corr": float(wave_corr),
        "centroid_ratio": float(ratio),
        "max_band_diff": float(max_diff),
        "synth_bands": synth_bands,
        "orig_bands": orig_bands,
        "balance": {"sub": SUB_BASS_AMP, "harmonic": HARMONIC_AMP, "mid": MID_AMP, "high": HIGH_AMP},
        "tests": tests,
        "verdict": f"V18 Phase 25: {n_pass}/{len(tests)} PASS. r={r:.3f}, wave_corr={wave_corr:.3f}, ratio={ratio:.3f}.",
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
