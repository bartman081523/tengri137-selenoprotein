"""
v18_phase17_istft_rekonstruktion.py
V18 PHASE 17 — iSTFT-REKONSTRUKTION (Original-Spektrum direkt)

LEHRE AUS PHASE 16:
- r=0.709 (leicht schlechter als v11)
- Mit BURUMUT-Wörtern komme ich nicht über r=0.73

NEUE IDEE: iSTFT-REKONSTRUKTION
- Nimm das Original-Spektrum
- Behalte Magnitude, zufällige Phasen
- iSTFT zurück zu WAV
- Ergibt: gleiche spektrale Verteilung wie Original

Frage: Ergibt das r=1.0? NEIN — die Phasen sind anders.
ABER: spektrale Leistungsverteilung sollte 1:1 sein.

Methode:
1. Original-Audio in Frames teilen
2. STFT berechnen
3. Magnitude-Spektrum behalten, Phase randomisieren (oder Glätten)
4. iSTFT zurück
5. Vergleichen mit Original

Wenn r ≈ 1.0: Spektrum-Reproduktion ist trivial — wir brauchen die PHASE-Information.
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


def main():
    print("=" * 80)
    print("V18 PHASE 17 — iSTFT-REKONSTRUKTION (Original-Spektrum)")
    print("=" * 80)

    out_dir = Path("bbox/v18_20260707")
    sr = 44100
    bands_def = [(0, 100), (100, 300), (300, 1000), (1000, 3000), (3000, 8000)]

    sr_orig, orig = lade_mp3()
    n_fft = 4096
    hop = n_fft // 2
    n_frames = (len(orig) - n_fft) // hop
    freqs = np.fft.rfftfreq(n_fft, 1.0/sr)

    # === 1. Original STFT ===
    print("1. Original STFT berechnen...")
    stft_orig = []
    for i in range(n_frames):
        frame = orig[i*hop:i*hop+n_fft] * np.hanning(n_fft)
        stft_orig.append(np.fft.rfft(frame))
    stft_orig = np.array(stft_orig)

    # === 2. Magnitude + Random Phase ===
    print("2. Magnitude + zufällige Phase...")
    rng = np.random.default_rng(42)
    magnitude = np.abs(stft_orig)
    phase = rng.uniform(0, 2*np.pi, size=stft_orig.shape)
    stft_recon = magnitude * np.exp(1j * phase)

    # === 3. iSTFT ===
    print("3. iSTFT zurück...")
    audio_recon = np.zeros(len(orig), dtype=np.float32)
    window_sum = np.zeros(len(orig), dtype=np.float32)
    for i in range(n_frames):
        frame_recon = np.fft.irfft(stft_recon[i], n=n_fft) * np.hanning(n_fft)
        start = i * hop
        end = start + n_fft
        if end <= len(audio_recon):
            audio_recon[start:end] += frame_recon
            window_sum[start:end] += np.hanning(n_fft) ** 2
    # Normalisierung (Overlap-Add)
    mask = window_sum > 1e-6
    audio_recon[mask] /= window_sum[mask]

    # Skaliere auf ähnliche RMS
    audio_recon = audio_recon * (np.sqrt(np.mean(orig**2)) / max(np.sqrt(np.mean(audio_recon**2)), 1e-12))
    audio_recon = np.clip(audio_recon, -1, 1)

    out_wav = out_dir / "synthese_v17_istft.wav"
    wavfile.write(out_wav, sr, (audio_recon * 32767).astype(np.int16))

    # === 4. Vergleich ===
    print("4. Vergleich...")
    spec_o = spektrum_analyse(orig, sr)
    spec_s = spektrum_analyse(audio_recon, sr)
    freqs_long = np.fft.rfftfreq(8192, 1.0/sr)
    log_s = np.log10(spec_s + 1e-12)
    log_o = np.log10(spec_o + 1e-12)
    r = float(np.corrcoef(log_s, log_o)[0, 1])
    print(f"  r = {r:.3f}")

    # Auch: r zwischen BURUMUT-Wörtern und Original, plus iSTFT vs Original
    synth_bands = band_verteilung(spec_s, freqs_long, bands_def)
    orig_bands = band_verteilung(spec_o, freqs_long, bands_def)
    print(f"  Band-Verteilung:")
    for band in orig_bands:
        s = synth_bands[band]
        o = orig_bands[band]
        print(f"    {band:>10s}: Synth={s*100:5.1f}%  Orig={o*100:5.1f}%  Diff={(s-o)*100:+5.1f}%")

    # Centroid
    cent_o = float(np.sum(freqs_long * spec_o) / np.sum(spec_o))
    cent_s = float(np.sum(freqs_long * spec_s) / np.sum(spec_s))
    ratio = cent_s / cent_o
    print(f"  Centroid: synth={cent_s:.0f}Hz, orig={cent_o:.0f}Hz, ratio={ratio:.3f}")

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

    n_pass = int(sum(1 for t in tests if t["pass"]))
    out_json = out_dir / "phase17_istft.json"
    output = {
        "phase": "V18 Phase 17 — iSTFT-Rekonstruktion",
        "n_pass": n_pass,
        "n_tests": len(tests),
        "spektrum_r": float(r),
        "centroid_ratio": float(ratio),
        "max_band_diff": float(max_diff),
        "synth_bands": synth_bands,
        "orig_bands": orig_bands,
        "tests": tests,
        "verdict": f"V18 Phase 17: {n_pass}/{len(tests)} PASS. r={r:.3f}, max_diff={max_diff*100:.1f}%, ratio={ratio:.3f}.",
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
