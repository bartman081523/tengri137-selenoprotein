"""
v18_phase4_ziel_spektrum.py
V18 PHASE 4 — ZIEL-SPEKTRUM-EXTRAKTION + iterative Annäherung

LEHRE AUS PHASE 1-3:
- v1: r=0.339, Centroid 1.36 (zu hell)
- v2: r=0.335, Centroid 0.65 (zu bass)
- v3: r=0.351, Centroid 0.74 (sub-bass fehlt, low-mid überschüssig)
- Manuelle Amplituden-Tuning ist LANGSAM

NEUER ANSATZ:
1. Extrahiere Original-Spektrum-Profil (5 Bänder: 0-100, 100-300, 300-1000, 1000-3000, 3000+)
2. Berechne Ziel-Amplituden so dass jeder Band im Synth den Original-Anteil hat
3. Iterative Anpassung mit spektrum-Matching

TDD:
- T1: Ziel-Spektrum-Profil extrahiert
- T2: Synth-Band-Verteilung < 10% Abweichung pro Band
- T3: Spektrum-r > 0.5
- T4: BURUMUT noch platziert
- T5: Centroid-Ratio 0.85-1.15
"""
import json
import sys
import numpy as np
from pathlib import Path
from scipy.io import wavfile


def lade_mp3():
    sr, audio = wavfile.read("bbox/v17_20260707/tengri137_full.wav")
    return sr, audio.astype(np.float32) / 32768.0


def spektrum_analyse(audio, sr, n_fft=8192, hop=None):
    if hop is None:
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


def generiere_band_fill(dauer_s, sr, freq, amp, puls_s=23.19, puls_amp=0.5):
    """Sinus-Ton mit BURUMUT-Pulsation."""
    t = np.linspace(0, dauer_s, int(dauer_s * sr), endpoint=False)
    puls = (1 - puls_amp) + puls_amp * np.abs(np.sin(2 * np.pi * 1.0/puls_s * t))
    return (puls * np.sin(2 * np.pi * freq * t)).astype(np.float32) * amp


def generiere_band_fill_saw(dauer_s, sr, freq, amp, puls_s=23.19, puls_amp=0.5):
    """Sägezahn-Ton mit BURUMUT-Pulsation (für Sub-Bass)."""
    t = np.linspace(0, dauer_s, int(dauer_s * sr), endpoint=False)
    puls = (1 - puls_amp) + puls_amp * np.abs(np.sin(2 * np.pi * 1.0/puls_s * t))
    saw = 2 * (t * freq - np.floor(0.5 + t * freq))
    return (saw * puls).astype(np.float32) * amp


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
    print("V18 PHASE 4 — ZIEL-SPEKTRUM-EXTRAKTION + iterativer Match")
    print("=" * 80)

    out_dir = Path("bbox/v18_20260707")
    sr = 44100
    dauer_s = 255.11
    bands_def = [(0, 100), (100, 300), (300, 1000), (1000, 3000), (3000, 8000)]

    # === 1. Original-Profil ===
    print("-" * 80)
    print("1. ORIGINAL-SPEKTRUM-PROFIL EXTRAHIEREN")
    print("-" * 80)
    sr_orig, orig = lade_mp3()
    spec_o = spektrum_analyse(orig, sr)
    freqs = np.fft.rfftfreq(8192, 1.0/sr)
    orig_bands = band_verteilung(spec_o, freqs, bands_def)
    print("  Original Band-Verteilung:")
    for band, val in orig_bands.items():
        print(f"    {band:>10s}: {val*100:5.1f}%")

    # === 2. BURUMUT laden ===
    print()
    print("-" * 80)
    print("2. BURUMUT LADEN")
    print("-" * 80)
    sr_b, burumut_teile = lade_burumut_woerter(list(range(1, 12)), "en-us")
    positionen = [7, 23, 46, 72, 95, 125, 141, 155, 174, 200, 222]
    burumut = platziere_burumut(sr, dauer_s, burumut_teile, positionen, amplitudes=[0.15]*11)
    burumut_spec = spektrum_analyse(burumut, sr)
    burumut_bands = band_verteilung(burumut_spec, freqs, bands_def)
    print("  BURUMUT Band-Verteilung:")
    for band, val in burumut_bands.items():
        print(f"    {band:>10s}: {val*100:5.1f}%")

    # === 3. Ziel-Amplituden berechnen (iterativ) ===
    print()
    print("-" * 80)
    print("3. ZIEL-AMPLITUDEN (manuell justiert für 5 Bänder)")
    print("-" * 80)
    # 5 Bänder, jeder braucht ein "Center-Tone" + Amplitude
    # Band 0-100Hz: 60Hz (Sub-Bass), Sägezahn
    # Band 100-300Hz: 200Hz (Bass), Sinus
    # Band 300-1000Hz: 500Hz (Low-Mid), Sinus
    # Band 1000-3000Hz: 2000Hz (Mid), Sinus
    # Band 3000+Hz: 4000Hz (High), Sinus
    # + BURUMUT

    # Initiale Amplituden (empirisch)
    amplitudes = {
        "60Hz_sub": 0.45,    # Sägezahn
        "200Hz_bass": 0.15,
        "500Hz_lowmid": 0.12,
        "2000Hz_mid": 0.04,
        "4000Hz_high": 0.005,
        "BURUMUT": 0.15,
    }
    # BURUMUT-Anteil am Spektrum: aus burumut_bands
    # Anteil in jedem Band = (BURUMUT_amp**2 * burumut_band_anteil) / total

    print(f"  Initiale Amplituden: {amplitudes}")

    # === 4. Synthese mit diesen Amplituden ===
    print()
    print("-" * 80)
    print("4. SYNTHESE MIT GEWÄHLTEN AMPLITUDEN")
    print("-" * 80)

    def baue_synth(amps):
        out = np.zeros(int(dauer_s * sr), dtype=np.float32)
        out += generiere_band_fill_saw(dauer_s, sr, 60, amps["60Hz_sub"])
        out += generiere_band_fill(dauer_s, sr, 200, amps["200Hz_bass"])
        out += generiere_band_fill(dauer_s, sr, 500, amps["500Hz_lowmid"])
        out += generiere_band_fill(dauer_s, sr, 2000, amps["2000Hz_mid"])
        out += generiere_band_fill(dauer_s, sr, 4000, amps["4000Hz_high"])
        out += burumut * amps["BURUMUT"]
        max_val = np.max(np.abs(out))
        if max_val > 0:
            out = out / max_val * 0.95
        return out

    synth = baue_synth(amplitudes)
    spec_s = spektrum_analyse(synth, sr)
    synth_bands = band_verteilung(spec_s, freqs, bands_def)

    print("  Vergleich Synth vs Original:")
    for band in orig_bands:
        s = synth_bands[band]
        o = orig_bands[band]
        diff = (s - o) * 100
        print(f"    {band:>10s}: Synth={s*100:5.1f}%  Orig={o*100:5.1f}%  Diff={diff:+5.1f}%")

    # === 5. Iterative Anpassung (5 Iterationen) ===
    print()
    print("-" * 80)
    print("5. ITERATIVE ANPASSUNG")
    print("-" * 80)
    for it in range(5):
        # Anpassung: factor = orig / synth für jedes Band
        # Aber wir haben 5 Tones für 5 Bänder - direkter Match
        factors = {}
        for band_name, tone_key in [
            ("0-100Hz", "60Hz_sub"),
            ("100-300Hz", "200Hz_bass"),
            ("300-1000Hz", "500Hz_lowmid"),
            ("1000-3000Hz", "2000Hz_mid"),
            ("3000-8000Hz", "4000Hz_high"),
        ]:
            if synth_bands[band_name] > 0.001:
                factors[tone_key] = orig_bands[band_name] / synth_bands[band_name]
            else:
                factors[tone_key] = 1.0
        # Dämpfe Anpassung (Lernrate 0.3)
        lr = 0.3
        for k in factors:
            amplitudes[k] *= (factors[k] ** lr)
        # BURUMUT lassen
        amplitudes["BURUMUT"] = 0.15

        # Neu synthetisieren
        synth = baue_synth(amplitudes)
        spec_s = spektrum_analyse(synth, sr)
        synth_bands = band_verteilung(spec_s, freqs, bands_def)

        # Metriken
        log_s = np.log10(spec_s + 1e-12)
        log_o = np.log10(spec_o + 1e-12)
        r = float(np.corrcoef(log_s, log_o)[0, 1])
        cent_s = float(np.sum(freqs * spec_s) / np.sum(spec_s))
        cent_o = float(np.sum(freqs * spec_o) / np.sum(spec_o))
        ratio = cent_s / cent_o
        max_diff = max(abs(synth_bands[b] - orig_bands[b]) for b in orig_bands)
        print(f"  Iter {it+1}: r={r:.3f}, ratio={ratio:.3f}, max_diff={max_diff*100:.1f}%")

    # === 6. Final speichern ===
    out_wav = out_dir / "synthese_v4.wav"
    audio_int16 = (synth * 32767).astype(np.int16)
    wavfile.write(out_wav, sr, audio_int16)
    print(f"\n  Gespeichert: {out_wav}")

    # === 7. TDD-Tests ===
    print()
    print("-" * 80)
    print("6. TDD-TESTS")
    print("-" * 80)
    tests = []

    t1_pass = bool(out_wav.exists() and out_wav.stat().st_size > 0)
    tests.append({"name": "T1_wav_erstellt", "pass": t1_pass,
                  "befund": f"{out_wav.stat().st_size / 1024:.0f} KB",
                  "was_sagt_es_uns": "Reproduzierbare WAV-Datei vorhanden."})

    # T2: Band-Abweichung < 10% pro Band
    band_diffs = [abs(synth_bands[b] - orig_bands[b]) for b in orig_bands]
    max_band_diff = max(band_diffs)
    t2_pass = bool(max_band_diff < 0.10)
    tests.append({"name": "T2_band_match", "pass": t2_pass,
                  "befund": f"max_diff = {max_band_diff*100:.1f}%",
                  "was_sagt_es_uns": f"Band-Verteilung: max Abweichung {max_band_diff*100:.1f}% ({'OK' if t2_pass else '>10%'})."})

    # T3: Spektrum-r > 0.5
    t3_pass = bool(r > 0.5)
    tests.append({"name": "T3_spektrum_korr", "pass": t3_pass,
                  "befund": f"r = {r:.3f}",
                  "was_sagt_es_uns": f"Spektrum-Form: {'STARK KORRELIERT' if t3_pass else 'zu schwach'}."})

    # T4: BURUMUT
    burumut_rms = float(np.sqrt(np.mean(burumut**2)))
    t4_pass = bool(burumut_rms > 0.001)
    tests.append({"name": "T4_burumut", "pass": t4_pass,
                  "befund": f"BURUMUT-RMS: {burumut_rms:.4f}",
                  "was_sagt_es_uns": "BURUMUT-Wörter platziert."})

    # T5: Centroid-Ratio
    t5_pass = bool(0.85 <= ratio <= 1.15)
    tests.append({"name": "T5_centroid", "pass": t5_pass,
                  "befund": f"ratio = {ratio:.3f}",
                  "was_sagt_es_uns": f"Centroid: {'ZENTRIERT' if t5_pass else 'daneben'}."})

    n_pass = int(sum(1 for t in tests if t["pass"]))

    output = {
        "phase": "V18 Phase 4 — Ziel-Spektrum + iterativer Match",
        "n_tests": len(tests),
        "n_pass": n_pass,
        "synthese_path": str(out_wav),
        "spektrum_korrelation": float(r),
        "centroid_synth_hz": float(cent_s),
        "centroid_orig_hz": float(cent_o),
        "centroid_ratio": float(ratio),
        "band_verteilung_synth": synth_bands,
        "band_verteilung_orig": orig_bands,
        "max_band_diff": float(max_band_diff),
        "final_amplitudes": amplitudes,
        "tests": tests,
        "verdict": f"V18 Phase 4: {n_pass}/{len(tests)} PASS. r={r:.3f}, max_band_diff={max_band_diff*100:.1f}%, ratio={ratio:.3f}.",
    }

    out_json = out_dir / "phase4_ziel_spektrum.json"
    with open(out_json, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print()
    for t in tests:
        mark = "✓" if t["pass"] else "✗"
        print(f"  {mark} {t['name']}: {t['was_sagt_es_uns']}")
    print()
    print(f"Output: {out_json}")
    print(f"Verdict: {output['verdict']}")
    return 0 if n_pass == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())
