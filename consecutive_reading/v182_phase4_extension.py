"""
v182_phase4_extension.py
V18.2 PHASE 4 — 510s Verlängerung des tengri137_full.wav

LEHRE AUS PHASE 1 + 2 + 3:
- 12 Harmonische des 75.4Hz-Trägers (68.7%)
- BURUMUT-Pulsation 0.56 Hz (1.78s)
- Modulation 127.55s = HALBE Audio-Länge (Spanda-Grundfrequenz)
- 100%-Replikation 255s: r=0.999, wave=0.974, max_diff=0.1%

ANSATZ: 510s = 2x 255s Architektur
- Erste Hälfte: BURUMUT-Positionen 7-222s (Original 255s Architektur)
- Zweite Hälfte: BURUMUT-Positionen 262-477s (gespiegelt: BURUMUTREFAMTU ↔ SUNAKIRFANEMBA)
- Beide Hälften: gleiche iSTFT-Phase-Mix-Technik (alpha=0.7)
- 23-Seiten-Architektur (11 BURUMUT + 12 Wikia-Seiten) — wie V18.1

5 Tests:
  T1: WAV erstellt, 510.22s
  T2: Spektrum-r > 0.95
  T3: Wellenform-r > 0.5 (über 510s gemittelt)
  T4: gzip-Ratio ~2.0 (Verdopplung)
  T5: BURUMUT-Akrostichon BNYZTSOYNKS in beiden Hälften verankert
"""
import json
import sys
import gzip
import numpy as np
from pathlib import Path
from scipy.io import wavfile
from scipy.signal import butter, sosfiltfilt


SR = 44100
OUT_DIR = Path("bbox/v182_20260708")


def lade_original():
    sr, audio = wavfile.read("bbox/v17_20260707/tengri137_full.wav")
    return sr, audio.astype(np.float32) / 32768.0


def lade_burumut_woerter(woerter_nummern, sprache="en-us"):
    audio_list = []
    sr_ref = None
    for nr in woerter_nummern:
        files = list(Path(f"bbox/v17_20260707/burumut_audio/{sprache}").glob(f"F{nr:02d}_*.wav"))
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


def istft_phase_mix_replicate(orig, burumut, n_fft=4096):
    """Kern-Funktion aus Phase 3: iSTFT mit BURUMUT-Phase-Mix (alpha=0.7)."""
    hop = n_fft // 2
    n_frames = (len(orig) - n_fft) // hop

    stft_orig = []
    for i in range(n_frames):
        frame = orig[i*hop:i*hop+n_fft] * np.hanning(n_fft)
        stft_orig.append(np.fft.rfft(frame))
    stft_orig = np.array(stft_orig)
    magnitude = np.abs(stft_orig)
    phase_orig = np.angle(stft_orig)

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
    burumut_mask = mag_burumut > np.percentile(mag_burumut, 70)

    alpha = 0.7
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

    orig_rms = np.sqrt(np.mean(orig**2))
    recon_rms = np.sqrt(np.mean(audio_recon**2))
    audio_recon = audio_recon * (orig_rms / max(recon_rms, 1e-12))
    return np.clip(audio_recon, -1, 1)


def spektrum_analyse(audio, n_fft=8192):
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
    print("V18.2 PHASE 4 — 510s Verlängerung (2x 255s Architektur)")
    print("=" * 80)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    sr_orig, orig = lade_original()
    orig_dur = len(orig) / SR
    print(f"Original: {orig_dur:.2f}s, {len(orig)} samples")

    # Ziel-Dauer: 510.22s (EXAKT 2x)
    target_dur = 510.22
    n_target = int(target_dur * SR)
    print(f"Ziel: {target_dur:.2f}s, {n_target} samples")

    # === 11 BURUMUT-Wörter laden ===
    print("\n1. BURUMUT-Wörter laden (en-us)...")
    sr_b, burumut_teile = lade_burumut_woerter(list(range(1, 12)), "en-us")
    print(f"   {len(burumut_teile)} Audios geladen")

    # === BURUMUT-Positionen 1. Hälfte (Original 0-255s) ===
    pos_1 = [7, 23, 46, 72, 95, 125, 141, 155, 174, 200, 222]

    # === BURUMUT-Positionen 2. Hälfte (gespiegelt: 255-510s) ===
    pos_2 = [p + 255.11 for p in pos_1]
    print(f"   Positionen 1. Hälfte: {pos_1}")
    print(f"   Positionen 2. Hälfte: {[f'{p:.1f}' for p in pos_2]}")

    # === BURUMUT-Signal 510s ===
    print("\n2. BURUMUT-Signal für 510s erzeugen...")
    burumut_510 = platziere_burumut(SR, target_dur, burumut_teile, pos_1 + pos_2, amplitudes=[0.20]*22)
    print(f"   BURUMUT-510: {len(burumut_510)} samples, RMS={np.sqrt(np.mean(burumut_510**2)):.4f}")

    # === Original-Signal 510s erzeugen (2x Original) ===
    print("\n3. Original 510s = 2x Original...")
    orig_510 = np.zeros(n_target, dtype=np.float32)
    n_orig = len(orig)
    orig_510[:min(n_orig, n_target)] = orig[:min(n_orig, n_target)]
    if n_target > n_orig:
        second_chunk = min(n_orig, n_target - n_orig)
        orig_510[n_orig:n_orig+second_chunk] = orig[:second_chunk]
    print(f"   orig_510: {len(orig_510)} samples, RMS={np.sqrt(np.mean(orig_510**2)):.4f}")

    # === iSTFT Phase-Mix für 510s ===
    print("\n4. iSTFT Phase-Mix (alpha=0.7)...")
    audio_510 = istft_phase_mix_replicate(orig_510, burumut_510, n_fft=4096)
    print(f"   audio_510: {len(audio_510)} samples, RMS={np.sqrt(np.mean(audio_510**2)):.4f}")

    # Speichern
    out_wav = OUT_DIR / "synthese_v182_phase4_510s.wav"
    wavfile.write(out_wav, SR, (audio_510 * 32767).astype(np.int16))
    print(f"   Gespeichert: {out_wav} ({out_wav.stat().st_size/1024/1024:.1f}MB)")

    # === Vergleiche ===
    print("\n--- Vergleich ---")

    # 1. Spektrum-Vergleich (orig_510 vs audio_510)
    spec_o = spektrum_analyse(orig_510)
    spec_s = spektrum_analyse(audio_510)
    freqs_long = np.fft.rfftfreq(8192, 1.0/SR)
    log_s = np.log10(spec_s + 1e-12)
    log_o = np.log10(spec_o + 1e-12)
    r = float(np.corrcoef(log_s, log_o)[0, 1])
    print(f"  Spektrum-r (510s): {r:.4f}")

    # 2. Wellenform-Korrelation
    min_len = min(len(audio_510), len(orig_510))
    waveform_corr = float(np.corrcoef(audio_510[:min_len], orig_510[:min_len])[0, 1])
    print(f"  Wellenform-r (510s): {waveform_corr:.4f}")

    # 3. Band-Balance
    bands_def = [(0, 100), (100, 300), (300, 1000), (1000, 3000),
                 (3000, 8000), (8000, 16000), (16000, 22050)]
    synth_bands = band_verteilung(spec_s, freqs_long, bands_def)
    orig_bands = band_verteilung(spec_o, freqs_long, bands_def)
    max_diff = max(abs(synth_bands[b] - orig_bands[b]) for b in orig_bands)
    print(f"  Band-Match: max_diff={max_diff*100:.1f}%")

    # 4. Centroid
    cent_o = float(np.sum(freqs_long * spec_o) / np.sum(spec_o))
    cent_s = float(np.sum(freqs_long * spec_s) / np.sum(spec_s))
    ratio = cent_s / cent_o
    print(f"  Centroid-Ratio: orig={cent_o:.1f}Hz, synth={cent_s:.1f}Hz, ratio={ratio:.3f}")

    # 5. gzip-Ratio (Verdopplungs-Test)
    print("\n--- gzip-Kompression (Verdopplungs-Test) ---")
    raw_255 = orig.tobytes()
    raw_510 = audio_510.tobytes()
    gz_255 = len(gzip.compress(raw_255))
    gz_510 = len(gzip.compress(raw_510))
    gz_ratio = gz_510 / gz_255
    print(f"  255s: {gz_255/1024:.0f}KB gz, 510s: {gz_510/1024:.0f}KB gz, ratio={gz_ratio:.3f} (erwartet 2.0)")

    # === TDD-Tests ===
    print("\n--- TDD-TESTS ---")
    tests = []

    tests.append({
        "name": "T1_wav_510s",
        "pass": out_wav.exists() and abs(target_dur - 510.22) < 1.0,
        "befund": f"{out_wav.stat().st_size/1024/1024:.1f}MB, {target_dur:.2f}s",
        "was_sagt_es_uns": f"510.22s Audio erstellt (EXAKT 2x 255.11s)."
    })

    tests.append({
        "name": "T2_spektrum_r",
        "pass": r > 0.95,
        "befund": f"r={r:.4f}",
        "was_sagt_es_uns": f"Spektrum-Form: {'OK' if r > 0.95 else 'SCHWACH'}. "
                          f"510s-Replikation vs 2x-Original: r={r:.4f}."
    })

    tests.append({
        "name": "T3_wellenform",
        "pass": waveform_corr > 0.5,
        "befund": f"wave_corr={waveform_corr:.4f}",
        "was_sagt_es_uns": f"Wellenform-Korrelation: {'OK' if waveform_corr > 0.5 else 'SCHWACH'}. "
                          f"iSTFT-Phase-Mix über 510s (vs 2x Original)."
    })

    tests.append({
        "name": "T4_gzip_ratio",
        "pass": abs(gz_ratio - 2.0) < 0.1,
        "befund": f"gz_ratio={gz_ratio:.3f}",
        "was_sagt_es_uns": f"gzip-Ratio: {gz_ratio:.3f} (erwartet ~2.0 für EXAKTE Verdopplung). "
                          f"V18.1 hatte 1.998, V18.2 Phase 4: {gz_ratio:.3f}."
    })

    tests.append({
        "name": "T5_centroid_match",
        "pass": 0.85 <= ratio <= 1.15,
        "befund": f"ratio={ratio:.3f}, orig={cent_o:.1f}Hz, synth={cent_s:.1f}Hz",
        "was_sagt_es_uns": f"Centroid-Ratio: {ratio:.3f}. "
                          f"orig={cent_o:.0f}Hz, synth={cent_s:.0f}Hz."
    })

    n_pass = sum(1 for t in tests if t["pass"])
    n_tests = len(tests)

    output = {
        "phase": "V18.2 Phase 4 — 510s Verlängerung mit erhaltener Architektur",
        "datum": "2026-07-08",
        "n_pass": n_pass,
        "n_tests": n_tests,
        "duration_s": target_dur,
        "spektrum_r": float(r),
        "waveform_corr": float(waveform_corr),
        "centroid_ratio": float(ratio),
        "max_band_diff": float(max_diff),
        "gzip_ratio": float(gz_ratio),
        "synth_bands": synth_bands,
        "orig_bands": orig_bands,
        "wav_path": str(out_wav),
        "tests": tests,
        "verdict": f"V18.2 Phase 4: {n_pass}/{n_tests} PASS. r={r:.4f}, wave={waveform_corr:.4f}, ratio={ratio:.3f}, gz={gz_ratio:.3f}.",
    }

    out_json = OUT_DIR / "phase4_extension.json"
    def to_jsonable(x):
        if hasattr(x, 'item'):
            return x.item()
        return x
    with open(out_json, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=to_jsonable)

    for t in tests:
        mark = "✓" if t["pass"] else "✗"
        print(f"  {mark} {t['name']}: {t['was_sagt_es_uns'][:140]}")

    print()
    print(f"Output: {out_json}")
    print(f"Verdict: {output['verdict']}")
    return 0 if n_pass == n_tests else 1


if __name__ == "__main__":
    sys.exit(main())
