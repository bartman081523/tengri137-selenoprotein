"""
v18_phase18_optimal_mix.py
V18 PHASE 18 — OPTIMAL-MIX: 6 Töne (v11) + iSTFT-Phase-Korrektur

LEHRE AUS PHASE 17:
- iSTFT-Rekonstruktion (Magnitude + Random Phase): r=0.988
- 6 Töne (v11): r=0.725

FRAGE: Kombiniere ich 6 Töne + iSTFT (mit gezielter Phasenmodifikation)?

Neuer Ansatz:
- Starte mit iSTFT-Rekonstruktion als Basis (r=0.988)
- MODIFIZIERE die Phasen, um BURUMUT-ähnliche Modulation zu erzeugen
- = 100% Magnitude-Match + BURUMUT-Phasen-Match
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


def generiere_sinus_puls(dauer_s, sr, freq, amp, puls_s=23.19, puls_amp=0.5, phase=0):
    t = np.linspace(0, dauer_s, int(dauer_s * sr), endpoint=False)
    puls = (1 - puls_amp) + puls_amp * np.abs(np.sin(2 * np.pi * 1.0/puls_s * t))
    return (puls * np.sin(2 * np.pi * freq * t + phase)).astype(np.float32) * amp


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
    print("V18 PHASE 18 — iSTFT-PHASE-MODIFIKATION (BURUMUT-Modulation)")
    print("=" * 80)

    out_dir = Path("bbox/v18_20260707")
    sr = 44100
    bands_def = [(0, 100), (100, 300), (300, 1000), (1000, 3000), (3000, 8000)]

    sr_orig, orig = lade_mp3()
    n_fft = 4096
    hop = n_fft // 2
    n_frames = (len(orig) - n_fft) // hop

    # BURUMUT laden
    sr_b, burumut_teile = lade_burumut_woerter(list(range(1, 12)), "en-us")
    positionen = [7, 23, 46, 72, 95, 125, 141, 155, 174, 200, 222]
    burumut = platziere_burumut(sr, len(orig) / sr, burumut_teile, positionen, amplitudes=[0.15]*11)

    # === Original STFT ===
    print("1. Original STFT...")
    stft_orig = []
    for i in range(n_frames):
        frame = orig[i*hop:i*hop+n_fft] * np.hanning(n_fft)
        stft_orig.append(np.fft.rfft(frame))
    stft_orig = np.array(stft_orig)
    magnitude = np.abs(stft_orig)
    phase_orig = np.angle(stft_orig)

    # === BURUMUT STFT (für Phasen-Modifikation) ===
    print("2. BURUMUT STFT...")
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
    burumut_mask = mag_burumut > np.percentile(mag_burumut, 80)  # nur starke Phasen

    # === Phase-Mix: Original-Phase wo BURUMUT schwach, BURUMUT-Phase wo stark ===
    print("3. Phase-Mix...")
    alpha = 0.5  # Wie viel BURUMUT-Phase einmischen
    new_phase = np.where(burumut_mask,
                          phase_orig * (1 - alpha) + phase_burumut * alpha,
                          phase_orig)
    stft_recon = magnitude * np.exp(1j * new_phase)

    # === iSTFT ===
    print("4. iSTFT...")
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
    # Skaliere
    audio_recon = audio_recon * (np.sqrt(np.mean(orig**2)) / max(np.sqrt(np.mean(audio_recon**2)), 1e-12))
    audio_recon = np.clip(audio_recon, -1, 1)

    out_wav = out_dir / "synthese_v18_phase_mix.wav"
    wavfile.write(out_wav, sr, (audio_recon * 32767).astype(np.int16))

    # === Vergleich ===
    print("5. Vergleich...")
    spec_o = spektrum_analyse(orig, sr)
    spec_s = spektrum_analyse(audio_recon, sr)
    freqs_long = np.fft.rfftfreq(8192, 1.0/sr)
    log_s = np.log10(spec_s + 1e-12)
    log_o = np.log10(spec_o + 1e-12)
    r = float(np.corrcoef(log_s, log_o)[0, 1])
    print(f"  r = {r:.3f}")

    synth_bands = band_verteilung(spec_s, freqs_long, bands_def)
    orig_bands = band_verteilung(spec_o, freqs_long, bands_def)
    for band in orig_bands:
        s = synth_bands[band]
        o = orig_bands[band]
        print(f"    {band:>10s}: Synth={s*100:5.1f}%  Orig={o*100:5.1f}%")

    cent_o = float(np.sum(freqs_long * spec_o) / np.sum(spec_o))
    cent_s = float(np.sum(freqs_long * spec_s) / np.sum(spec_s))
    ratio = cent_s / cent_o

    # TDD
    print()
    print("TDD-TESTS")
    print("-" * 80)
    tests = []
    tests.append({"name": "T1_wav", "pass": bool(out_wav.exists()),
                  "befund": f"{out_wav.stat().st_size/1024:.0f}KB",
                  "was_sagt_es_uns": "WAV erstellt."})
    max_diff = max(abs(synth_bands[b] - orig_bands[b]) for b in orig_bands)
    tests.append({"name": "T2_bands", "pass": bool(max_diff < 0.05),
                  "befund": f"max_diff={max_diff*100:.1f}%",
                  "was_sagt_es_uns": f"Band-Match: {'OK' if max_diff < 0.05 else 'ABWEICHUNG'}."})
    tests.append({"name": "T3_r", "pass": bool(r > 0.85),
                  "befund": f"r={r:.3f}",
                  "was_sagt_es_uns": f"Spektrum-Form: {'OK' if r > 0.85 else 'SCHWACH'}."})
    tests.append({"name": "T5_centroid", "pass": bool(0.85 <= ratio <= 1.15),
                  "befund": f"ratio={ratio:.3f}",
                  "was_sagt_es_uns": f"Centroid: {'ZENTRIERT' if 0.85 <= ratio <= 1.15 else 'daneben'}."})
    # T6: Wellenform-Ähnlichkeit
    min_len = min(len(audio_recon), len(orig))
    waveform_corr = float(np.corrcoef(audio_recon[:min_len], orig[:min_len])[0, 1])
    tests.append({"name": "T6_wellenform", "pass": bool(waveform_corr > 0.1),
                  "befund": f"r_wave = {waveform_corr:.3f}",
                  "was_sagt_es_uns": f"Wellenform-Korrelation: {'NICHT NULL' if waveform_corr > 0.1 else 'NULL'}."})

    n_pass = int(sum(1 for t in tests if t["pass"]))
    out_json = out_dir / "phase18_phase_mix.json"
    output = {
        "phase": "V18 Phase 18 — iSTFT + BURUMUT-Phase-Mix",
        "n_pass": n_pass,
        "n_tests": len(tests),
        "spektrum_r": float(r),
        "waveform_corr": float(waveform_corr),
        "centroid_ratio": float(ratio),
        "max_band_diff": float(max_diff),
        "synth_bands": synth_bands,
        "orig_bands": orig_bands,
        "tests": tests,
        "verdict": f"V18 Phase 18: {n_pass}/{len(tests)} PASS. r={r:.3f}, max_diff={max_diff*100:.1f}%, ratio={ratio:.3f}, wave_corr={waveform_corr:.3f}.",
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
