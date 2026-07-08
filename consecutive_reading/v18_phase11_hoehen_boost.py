"""
v18_phase11_hoehen_boost.py
V18 PHASE 11 — HÖHEN-BOOST + Band-Justierung

LEHRE AUS PHASE 10:
- r=0.712 (leicht schlechter als v9=0.725)
- Centroid 0.734 (zu tief)
- 3000-8000Hz FEHLT komplett (0.0% vs 3.5%)
- 1000-3000Hz zu viel (7.6% vs 5.7%)

FIX:
- Höhere Höhen-Amplitude (3000+Hz)
- Reduziere 1000-3000Hz
- Höhere Center-Töne für Centroid-Anhebung
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


def generiere_sinus_puls(dauer_s, sr, freq, amp, puls_s=23.19, puls_amp=0.5):
    t = np.linspace(0, dauer_s, int(dauer_s * sr), endpoint=False)
    puls = (1 - puls_amp) + puls_amp * np.abs(np.sin(2 * np.pi * 1.0/puls_s * t))
    return (puls * np.sin(2 * np.pi * freq * t)).astype(np.float32) * amp


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
    print("V18 PHASE 11 — HÖHEN-BOOST + Band-Justierung")
    print("=" * 80)

    out_dir = Path("bbox/v18_20260707")
    sr = 44100
    dauer_s = 255.11
    bands_def = [(0, 100), (100, 300), (300, 1000), (1000, 3000), (3000, 8000)]

    sr_orig, orig = lade_mp3()
    spec_o = spektrum_analyse(orig, sr)
    freqs = np.fft.rfftfreq(8192, 1.0/sr)
    orig_bands = band_verteilung(spec_o, freqs, bands_def)
    log_o = np.log10(spec_o + 1e-12)
    cent_o = float(np.sum(freqs * spec_o) / np.sum(spec_o))

    # BURUMUT
    sr_b, burumut_teile = lade_burumut_woerter(list(range(1, 12)), "en-us")
    positionen = [7, 23, 46, 72, 95, 125, 141, 155, 174, 200, 222]
    burumut = platziere_burumut(sr, dauer_s, burumut_teile, positionen, amplitudes=[0.15]*11)

    # 5 Töne-Gruppen (zurück zu Phase 9 Architektur, aber mit Boost)
    # Sub-Bass: 50Hz (1 Ton, weil Power ohnehin in 0-100Hz konzentriert)
    # Bass: 200Hz
    # Low-Mid: 600Hz
    # Mid: 1500Hz
    # High: 3500Hz + 5000Hz für Höhen-Boost
    freqs_target = [50, 200, 600, 1500, 3500, 5500]
    band_keys = list(orig_bands.keys())

    # Initial-Amplituden: sqrt(orig_bands) * 0.5
    amps = np.array([np.sqrt(orig_bands[b]) * 0.5 for b in band_keys])
    # Plus extra für 5500Hz
    amps = np.append(amps, 0.02)
    print(f"Initiale Amplituden: {dict(zip(freqs_target, amps))}")

    out = burumut.copy()
    for f, a in zip(freqs_target, amps):
        if a > 0.001:
            out += generiere_sinus_puls(dauer_s, sr, f, a)
    max_val = np.max(np.abs(out))
    if max_val > 0:
        out = out / max_val * 0.95

    out_wav = out_dir / "synthese_v11.wav"
    wavfile.write(out_wav, sr, (out * 32767).astype(np.int16))

    spec_s = spektrum_analyse(out, sr)
    synth_bands = band_verteilung(spec_s, freqs, bands_def)
    log_s = np.log10(spec_s + 1e-12)
    r = float(np.corrcoef(log_s, log_o)[0, 1])
    cent_s = float(np.sum(freqs * spec_s) / np.sum(spec_s))
    ratio = cent_s / cent_o
    max_diff = max(abs(synth_bands[b] - orig_bands[b]) for b in orig_bands)

    print()
    print("VERGLEICH")
    print("-" * 80)
    print(f"  r={r:.3f}, ratio={ratio:.3f}, max_diff={max_diff*100:.1f}%")
    for band in orig_bands:
        s = synth_bands[band]
        o = orig_bands[band]
        print(f"    {band:>10s}: Synth={s*100:5.1f}%  Orig={o*100:5.1f}%  Diff={(s-o)*100:+5.1f}%")

    # Skalierungs-Iteration (wie v9)
    print("\nSkalierungs-Iteration:")
    for it in range(5):
        scale = []
        for i, b in enumerate(band_keys):
            if synth_bands[b] > 0.001:
                s = orig_bands[b] / synth_bands[b]
            else:
                s = 1.0
            scale.append(s)
        lr = 0.5
        for i in range(len(band_keys)):
            amps[i] *= scale[i] ** lr
        # Höhen-Ton separat
        if synth_bands["3000-8000Hz"] > 0.001:
            amps[5] *= (orig_bands["3000-8000Hz"] / synth_bands["3000-8000Hz"]) ** lr
        # Neubauen
        out = burumut.copy()
        for f, a in zip(freqs_target, amps):
            if a > 0.001:
                out += generiere_sinus_puls(dauer_s, sr, f, a)
        max_val = np.max(np.abs(out))
        if max_val > 0:
            out = out / max_val * 0.95
        spec_s = spektrum_analyse(out, sr)
        synth_bands = band_verteilung(spec_s, freqs, bands_def)
        log_s = np.log10(spec_s + 1e-12)
        r_new = float(np.corrcoef(log_s, log_o)[0, 1])
        cent_s = float(np.sum(freqs * spec_s) / np.sum(spec_s))
        ratio = cent_s / cent_o
        max_diff = max(abs(synth_bands[b] - orig_bands[b]) for b in orig_bands)
        print(f"  Iter {it+1}: r={r_new:.3f}, ratio={ratio:.3f}, max_diff={max_diff*100:.1f}%")
        r = r_new

    # Final
    out_wav_final = out_dir / "synthese_v11_final.wav"
    wavfile.write(out_wav_final, sr, (out * 32767).astype(np.int16))

    print()
    print("TDD-TESTS")
    print("-" * 80)
    tests = []
    tests.append({"name": "T1_wav", "pass": bool(out_wav_final.exists()),
                  "befund": f"{out_wav_final.stat().st_size/1024:.0f}KB",
                  "was_sagt_es_uns": "WAV erstellt."})
    tests.append({"name": "T2_bands", "pass": bool(max_diff < 0.05),
                  "befund": f"max_diff={max_diff*100:.1f}%",
                  "was_sagt_es_uns": f"Band-Match: {'OK' if max_diff < 0.05 else 'ABWEICHUNG'}."})
    tests.append({"name": "T3_r", "pass": bool(r > 0.6),
                  "befund": f"r={r:.3f}",
                  "was_sagt_es_uns": f"Spektrum-Form: {'OK' if r > 0.6 else 'SCHWACH'}."})
    burumut_rms = float(np.sqrt(np.mean(burumut**2)))
    tests.append({"name": "T4_burumut", "pass": bool(burumut_rms > 0.001),
                  "befund": f"RMS={burumut_rms:.4f}",
                  "was_sagt_es_uns": "BURUMUT platziert."})
    tests.append({"name": "T5_centroid", "pass": bool(0.85 <= ratio <= 1.15),
                  "befund": f"ratio={ratio:.3f}",
                  "was_sagt_es_uns": f"Centroid: {'ZENTRIERT' if 0.85 <= ratio <= 1.15 else 'daneben'}."})

    n_pass = int(sum(1 for t in tests if t["pass"]))
    out_json = out_dir / "phase11_hoehen_boost.json"
    output = {
        "phase": "V18 Phase 11 — Höhen-Boost",
        "n_pass": n_pass,
        "n_tests": len(tests),
        "spektrum_r": float(r),
        "centroid_ratio": float(ratio),
        "max_band_diff": float(max_diff),
        "synth_bands": synth_bands,
        "orig_bands": orig_bands,
        "amps_final": {str(f): float(a) for f, a in zip(freqs_target, amps)},
        "tests": tests,
        "verdict": f"V18 Phase 11: {n_pass}/{len(tests)} PASS. r={r:.3f}, max_diff={max_diff*100:.1f}%, ratio={ratio:.3f}.",
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
