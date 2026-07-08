"""
v18_phase8_multi_objektiv.py
V18 PHASE 8 — MULTI-OBJEKTIV-OPTIMIERUNG (Band-Match + r)

LEHRE AUS PHASE 7:
- Numerische Optimierung erreicht r=0.751 mit NEGATIVEN Amplituden
- r korreliert logarithmische Power-Spektren — Form, nicht absolute Werte
- Band-Match ist nicht in der Kostenfunktion

NEUE KOSTENFUNKTION:
- cost = w1 * (1 - band_match) + w2 * (1 - r) + w3 * abs(centroid_ratio - 1.0)
- Alle Amplituden >= 0

ARCHITEKTUR: 5 Sinus-Töne, 1 BURUMUT
- 50Hz (Sub), 200Hz (Bass), 600Hz (Low-Mid), 1500Hz (Mid), 3500Hz (High)
- Amplitude je Band ≈ sqrt(orig_band_power) — wenn orig 64% im Sub, dann a_sub ≈ 0.8
"""
import json
import sys
import numpy as np
from pathlib import Path
from scipy.io import wavfile
from scipy.optimize import minimize


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
    print("V18 PHASE 8 — MULTI-OBJEKTIV-OPTIMIERUNG (keine negativen Amplituden)")
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
    band_array_o = np.array(list(orig_bands.values()))

    print("Original:")
    for band, val in orig_bands.items():
        print(f"  {band:>10s}: {val*100:5.1f}%")

    # === BURUMUT laden ===
    sr_b, burumut_teile = lade_burumut_woerter(list(range(1, 12)), "en-us")
    positionen = [7, 23, 46, 72, 95, 125, 141, 155, 174, 200, 222]
    burumut = platziere_burumut(sr, dauer_s, burumut_teile, positionen, amplitudes=[0.15]*11)
    burumut_spec = spektrum_analyse(burumut, sr)
    burumut_bands = band_verteilung(burumut_spec, freqs, bands_def)
    burumut_share = burumut_bands.copy()  # Was BURUMUT zum Spektrum beiträgt
    print("\nBURUMUT:")
    for band, val in burumut_bands.items():
        print(f"  {band:>10s}: {val*100:5.1f}%")

    # 5 Sinus-Töne
    freqs_target = [50, 200, 600, 1500, 3500]

    # Kostenfunktion: Gewichteter Mix aus Band-Match + Spektrum-r
    # - Wir wollen, dass synth_bands[i] ≈ orig_bands[i]
    # - Aber auch r hoch
    # - Und centroid passt

    def cost(amps_raw):
        # Clamp auf >= 0
        amps = np.maximum(amps_raw, 0)
        out = burumut.copy()
        for f, a in zip(freqs_target, amps):
            if a > 0.001:
                out += generiere_sinus_puls(dauer_s, sr, f, a)
        spec_s = spektrum_analyse(out, sr)
        # Band-Match
        synth_bands = band_verteilung(spec_s, freqs, bands_def)
        band_array = np.array(list(synth_bands.values()))
        band_diff = np.sum(np.abs(band_array - band_array_o))
        # r
        log_s = np.log10(spec_s + 1e-12)
        r = float(np.corrcoef(log_s, log_o)[0, 1])
        # Centroid
        cent_s = float(np.sum(freqs * spec_s) / np.sum(spec_s))
        cent_diff = abs(cent_s - cent_o) / cent_o
        # Multi-Objektiv
        return 0.5 * band_diff + 0.3 * (1 - r) + 0.2 * cent_diff + 0.1 * np.sum(np.maximum(-amps_raw, 0))

    # Initiale Amplituden — schätze aus orig_bands / 5
    amps0 = np.array([0.5, 0.2, 0.15, 0.05, 0.01])
    print(f"\nInitiale Amplituden: {amps0}")
    print(f"Initial cost = {cost(amps0):.3f}")

    result = minimize(cost, amps0, method='Nelder-Mead',
                       options={'maxiter': 200, 'xatol': 0.001, 'fatol': 0.001})
    amps_opt = np.maximum(result.x, 0)
    print(f"Optimierte Amplituden: {dict(zip(freqs_target, amps_opt))}")
    print(f"Final cost = {cost(amps_opt):.3f}")

    # Baue Synthese
    out = burumut.copy()
    for f, a in zip(freqs_target, amps_opt):
        if a > 0.001:
            out += generiere_sinus_puls(dauer_s, sr, f, a)
    max_val = np.max(np.abs(out))
    if max_val > 0:
        out = out / max_val * 0.95

    out_wav = out_dir / "synthese_v8.wav"
    wavfile.write(out_wav, sr, (out * 32767).astype(np.int16))

    spec_s = spektrum_analyse(out, sr)
    synth_bands = band_verteilung(spec_s, freqs, bands_def)
    log_s = np.log10(spec_s + 1e-12)
    r = float(np.corrcoef(log_s, log_o)[0, 1])
    cent_s = float(np.sum(freqs * spec_s) / np.sum(spec_s))
    ratio = cent_s / cent_o

    print()
    print("-" * 80)
    print("VERGLEICH")
    print("-" * 80)
    print(f"  r={r:.3f}, ratio={ratio:.3f}")
    for band in orig_bands:
        s = synth_bands[band]
        o = orig_bands[band]
        print(f"    {band:>10s}: Synth={s*100:5.1f}%  Orig={o*100:5.1f}%  Diff={(s-o)*100:+5.1f}%")

    # TDD
    print()
    print("-" * 80)
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
    # T6: keine negativen Amplituden
    no_neg = bool(np.all(amps_opt >= 0))
    tests.append({"name": "T6_keine_negativen_amps", "pass": no_neg,
                  "befund": f"min_amp = {float(np.min(amps_opt)):.4f}",
                  "was_sagt_es_uns": f"Amplituden physikalisch sinnvoll: {'JA' if no_neg else 'NEIN'}."})

    n_pass = int(sum(1 for t in tests if t["pass"]))
    out_json = out_dir / "phase8_multi_objektiv.json"
    output = {
        "phase": "V18 Phase 8 — Multi-Objektiv",
        "n_pass": n_pass,
        "n_tests": len(tests),
        "spektrum_r": float(r),
        "centroid_ratio": float(ratio),
        "max_band_diff": float(max_diff),
        "synth_bands": synth_bands,
        "orig_bands": orig_bands,
        "amps_opt": {str(f): float(a) for f, a in zip(freqs_target, amps_opt)},
        "tests": tests,
        "verdict": f"V18 Phase 8: {n_pass}/{len(tests)} PASS. r={r:.3f}, max_diff={max_diff*100:.1f}%, ratio={ratio:.3f}.",
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
