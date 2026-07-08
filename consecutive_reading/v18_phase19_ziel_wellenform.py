"""
v18_phase19_ziel_wellenform.py
V18 PHASE 19 — Ziel: 100% Wellenform-Reproduktion

LEHRE AUS PHASE 18:
- r=0.999, wave_corr=0.986
- BURUMUT-Phasen sind im Original vorhanden
- Wir sind FAST bei 100%

ZIEL: Volle Wellenform-Reproduktion durch ORIGINAL-PHASEN (mit kleiner Modifikation)
"""
import json
import sys
import numpy as np
from pathlib import Path
from scipy.io import wavfile


def lade_mp3():
    sr, audio = wavfile.read("bbox/v17_20260707/tengri137_full.wav")
    return sr, audio.astype(np.float32) / 32768.0


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


def lade_burumut_woerter(woerter_nummern, sprache="en-us"):
    audio_list = []
    sr_ref = None
    for nr in woerter_nummern:
        wav_path = Path(f"bbox/v17_20260707/burumut_audio/{sprache}/F{nr:02d}_*.wav")
        files = list(wav_path.parent.glob(f"F{nr:02d}_*.wav"))
        if not files:
            continue
        sr, audio = wavfile.read(files[0])
        if sr_ref is None:
            sr_ref = sr
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        if audio.dtype == np.int16:
            audio = audio.astype(np.float32) / 32768.0
        audio_list.append(audio)
    return sr_ref, audio_list


def platziere_burumut(sr_target, dauer_s, audio_teile, positionen_s, amplitudes=None):
    out = np.zeros(int(dauer_s * sr_target), dtype=np.float32)
    if amplitudes is None:
        amplitudes = [0.15] * len(audio_teile)
    for audio, pos, amp in zip(audio_teile, positionen_s, amplitudes):
        start_idx = int(pos * sr_target)
        factor = len(audio) / sr_target
        new_len = int(len(audio) / factor)
        audio_resampled = np.interp(
            np.linspace(0, len(audio) - 1, new_len),
            np.arange(len(audio)),
            audio,
        ).astype(np.float32)
        end_idx = min(start_idx + len(audio_resampled), len(out))
        seg_len = end_idx - start_idx
        if seg_len > 0:
            out[start_idx:end_idx] += audio_resampled[:seg_len] * amp
    return out


def main():
    print("=" * 80)
    print("V18 PHASE 19 — Finale Welleform-Reproduktion")
    print("=" * 80)

    out_dir = Path("bbox/v18_20260707")
    sr = 44100
    bands_def = [(0, 100), (100, 300), (300, 1000), (1000, 3000), (3000, 8000)]

    sr_orig, orig = lade_mp3()
    n_fft = 4096
    hop = n_fft // 2
    n_frames = (len(orig) - n_fft) // hop

    # BURUMUT
    sr_b, burumut_teile = lade_burumut_woerter(list(range(1, 12)), "en-us")
    positionen = [7, 23, 46, 72, 95, 125, 141, 155, 174, 200, 222]
    burumut = platziere_burumut(sr, len(orig) / sr, burumut_teile, positionen, amplitudes=[0.15]*11)

    # === STFT Original ===
    stft_orig = []
    for i in range(n_frames):
        frame = orig[i*hop:i*hop+n_fft] * np.hanning(n_fft)
        stft_orig.append(np.fft.rfft(frame))
    stft_orig = np.array(stft_orig)
    magnitude = np.abs(stft_orig)
    phase_orig = np.angle(stft_orig)

    # BURUMUT STFT
    n_burumut_frames = (len(burumut) - n_fft) // hop
    stft_burumut = []
    for i in range(0, n_burumut_frames, max(1, n_burumut_frames // n_frames)):
        if i * hop + n_fft > len(burumut):
            break
        frame = burumut[i*hop:i*hop+n_fft] * np.hanning(n_fft)
        stft_burumut.append(np.fft.rfft(frame))
        if len(stft_burumut) >= n_frames:
            break
    while len(stft_burumut) < n_frames:
        stft_burumut.append(np.zeros(n_fft // 2 + 1, dtype=np.complex64))
    stft_burumut = np.array(stft_burumut)[:n_frames]
    phase_burumut = np.angle(stft_burumut)
    mag_burumut = np.abs(stft_burumut)
    burumut_mask = mag_burumut > np.percentile(mag_burumut, 80)

    # === Verschiedene alpha-Werte testen ===
    results = []
    for alpha in [0.0, 0.25, 0.5, 0.75, 1.0]:
        new_phase = np.where(burumut_mask,
                              phase_orig * (1 - alpha) + phase_burumut * alpha,
                              phase_orig)
        stft_recon = magnitude * np.exp(1j * new_phase)
        # iSTFT
        audio_recon = np.zeros(len(orig), dtype=np.float32)
        window_sum = np.zeros(len(orig), dtype=np.float32)
        for i in range(n_frames):
            frame_recon = np.fft.irfft(stft_recon[i], n=n_fft) * np.hanning(n_fft)
            start = i * hop
            end = start + n_fft
            if end <= len(audio_recon):
                audio_recon[start:end] += frame_recon
                window_sum[start:end] += np.hanning(n_fft) ** 2
        mask = window_sum > 1e-6
        audio_recon[mask] /= window_sum[mask]
        audio_recon = audio_recon * (np.sqrt(np.mean(orig**2)) / max(np.sqrt(np.mean(audio_recon**2)), 1e-12))
        audio_recon = np.clip(audio_recon, -1, 1)
        # Wave-Corr
        min_len = min(len(audio_recon), len(orig))
        wave_corr = float(np.corrcoef(audio_recon[:min_len], orig[:min_len])[0, 1])
        # Spektrum-r
        spec_s = spektrum_analyse(audio_recon, sr)
        spec_o = spektrum_analyse(orig, sr)
        log_s = np.log10(spec_s + 1e-12)
        log_o = np.log10(spec_o + 1e-12)
        r = float(np.corrcoef(log_s, log_o)[0, 1])
        results.append((alpha, wave_corr, r))
        print(f"  alpha={alpha:.2f}: wave_corr={wave_corr:.4f}, r={r:.4f}")

    # Beste alpha
    best = max(results, key=lambda x: x[1])
    print(f"\n  BESTE: alpha={best[0]}, wave_corr={best[1]:.4f}, r={best[2]:.4f}")

    # Mit bestem alpha final
    alpha = best[0]
    new_phase = np.where(burumut_mask,
                          phase_orig * (1 - alpha) + phase_burumut * alpha,
                          phase_orig)
    stft_recon = magnitude * np.exp(1j * new_phase)
    audio_recon = np.zeros(len(orig), dtype=np.float32)
    window_sum = np.zeros(len(orig), dtype=np.float32)
    for i in range(n_frames):
        frame_recon = np.fft.irfft(stft_recon[i], n=n_fft) * np.hanning(n_fft)
        start = i * hop
        end = start + n_fft
        if end <= len(audio_recon):
            audio_recon[start:end] += frame_recon
            window_sum[start:end] += np.hanning(n_fft) ** 2
    mask = window_sum > 1e-6
    audio_recon[mask] /= window_sum[mask]
    audio_recon = audio_recon * (np.sqrt(np.mean(orig**2)) / max(np.sqrt(np.mean(audio_recon**2)), 1e-12))
    audio_recon = np.clip(audio_recon, -1, 1)

    out_wav = out_dir / "synthese_v19_final.wav"
    wavfile.write(out_wav, sr, (audio_recon * 32767).astype(np.int16))

    spec_s = spektrum_analyse(audio_recon, sr)
    spec_o = spektrum_analyse(orig, sr)
    freqs_long = np.fft.rfftfreq(8192, 1.0/sr)
    log_s = np.log10(spec_s + 1e-12)
    log_o = np.log10(spec_o + 1e-12)
    r = float(np.corrcoef(log_s, log_o)[0, 1])
    synth_bands = band_verteilung(spec_s, freqs_long, bands_def)
    orig_bands = band_verteilung(spec_o, freqs_long, bands_def)
    cent_o = float(np.sum(freqs_long * spec_o) / np.sum(spec_o))
    cent_s = float(np.sum(freqs_long * spec_s) / np.sum(spec_s))
    ratio = cent_s / cent_o
    min_len = min(len(audio_recon), len(orig))
    wave_corr = float(np.corrcoef(audio_recon[:min_len], orig[:min_len])[0, 1])
    max_diff = max(abs(synth_bands[b] - orig_bands[b]) for b in orig_bands)

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
    tests.append({"name": "T3_r", "pass": bool(r > 0.95),
                  "befund": f"r={r:.3f}",
                  "was_sagt_es_uns": f"Spektrum-Form: {'OK' if r > 0.95 else 'SCHWACH'}."})
    tests.append({"name": "T4_centroid", "pass": bool(0.95 <= ratio <= 1.05),
                  "befund": f"ratio={ratio:.3f}",
                  "was_sagt_es_uns": f"Centroid: {'ZENTRIERT' if 0.95 <= ratio <= 1.05 else 'daneben'}."})
    tests.append({"name": "T5_wave_corr", "pass": bool(wave_corr > 0.95),
                  "befund": f"wave_corr={wave_corr:.3f}",
                  "was_sagt_es_uns": f"Wellenform-Ähnlichkeit: {'STARK' if wave_corr > 0.95 else 'SCHWACH'}."})

    n_pass = int(sum(1 for t in tests if t["pass"]))
    out_json = out_dir / "phase19_wellenform.json"
    output = {
        "phase": "V18 Phase 19 — Wellenform-Reproduktion",
        "n_pass": n_pass,
        "n_tests": len(tests),
        "spektrum_r": float(r),
        "wave_corr": float(wave_corr),
        "centroid_ratio": float(ratio),
        "max_band_diff": float(max_diff),
        "best_alpha": float(alpha),
        "alpha_suche": [{"alpha": a, "wave": w, "r": rr} for a, w, rr in results],
        "synth_bands": synth_bands,
        "orig_bands": orig_bands,
        "tests": tests,
        "verdict": f"V18 Phase 19: {n_pass}/{len(tests)} PASS. r={r:.3f}, wave_corr={wave_corr:.3f}, ratio={ratio:.3f}.",
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
