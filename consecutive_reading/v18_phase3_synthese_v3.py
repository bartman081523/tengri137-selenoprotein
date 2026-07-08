"""
v18_phase3_synthese_v3.py
V18 PHASE 3 — SYNTHESE v3 (GOLDILOCKS)

LEHRE AUS PHASE 1+2:
- v1: Centroid 1.36 (zu höhenlastig) — 4kHz zu laut
- v2: Centroid 0.65 (zu basslastig) — Sub-Bass zu fett
- ZIEL: Centroid-Ratio ≈ 1.0
- Original Band-Verteilung: 64% Sub / 12% Bass / 16% Low-Mid / 6% Mid / 4% High
- v2: 75% / 13% / 8% / 3% / 1% — 11% Sub-Bass ÜBERSCHUSS, 8% Low-Mid DEFIZIT

FIX-STRATEGIE:
- Sub-Bass reduzieren (40+75+150): 0.4+0.35+0.15 = 0.9 → 0.25+0.20+0.10 = 0.55
- 300Hz Mittelschicht: 0.08 → 0.18 (verstärken)
- 600Hz Schicht NEU: 0.12 (um Low-Mid-Band zu füllen)
- 4kHz Träger: 0.005 (beibehalten)
- BURUMUT: 0.15 (beibehalten)

TDD: 5 Tests, mit Fokus auf Centroid-Zentrierung
"""
import json
import sys
import numpy as np
from pathlib import Path
from scipy.io import wavfile


def lade_mp3():
    sr, audio = wavfile.read("bbox/v17_20260707/tengri137_full.wav")
    return sr, audio.astype(np.float32) / 32768.0


def generiere_traeger(dauer_s, sr=44100, freq=3940, amp=0.005):
    t = np.linspace(0, dauer_s, int(dauer_s * sr), endpoint=False)
    modulator = 0.3 + 0.7 * np.sin(2 * np.pi * 0.1 * t)
    return (modulator * np.sin(2 * np.pi * freq * t)).astype(np.float32) * amp


def generiere_subbass(dauer_s, sr=44100, freqs=(40, 75, 150), amps=(0.25, 0.20, 0.10)):
    t = np.linspace(0, dauer_s, int(dauer_s * sr), endpoint=False)
    out = np.zeros_like(t)
    puls = 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 1.0/23.19 * t))
    for freq, amp in zip(freqs, amps):
        saw = 2 * (t * freq - np.floor(0.5 + t * freq))
        out += (saw * puls).astype(np.float32) * amp
    return out


def generiere_mittelschicht(dauer_s, sr=44100, freq=300, amp=0.18, puls_s=7.0):
    t = np.linspace(0, dauer_s, int(dauer_s * sr), endpoint=False)
    puls = 0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 1.0/puls_s * t))
    return (puls * np.sin(2 * np.pi * freq * t)).astype(np.float32) * amp


def generiere_lowmid(dauer_s, sr=44100, freq=600, amp=0.12, puls_s=11.7):
    t = np.linspace(0, dauer_s, int(dauer_s * sr), endpoint=False)
    puls = 0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 1.0/puls_s * t))
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


def mische(sr, dauer_s, *schichten):
    out = np.zeros(int(dauer_s * sr), dtype=np.float32)
    for s in schichten:
        out += s[:len(out)]
    max_val = np.max(np.abs(out))
    if max_val > 0:
        out = out / max_val * 0.95
    return out


def spektrum_analyse(audio, sr, n_fft=8192, hop=None):
    if hop is None:
        hop = n_fft // 2
    n_frames = (len(audio) - n_fft) // hop
    specs = []
    for i in range(n_frames):
        frame = audio[i*hop:i*hop+n_fft] * np.hanning(n_fft)
        spec = np.abs(np.fft.rfft(frame))**2
        specs.append(spec)
    return np.mean(specs, axis=0)


def band_verteilung(spec, freqs):
    bands = [(0, 100), (100, 300), (300, 1000), (1000, 3000), (3000, 8000)]
    total = np.sum(spec)
    return {
        f"{lo}-{hi}Hz": float(np.sum(spec[(freqs >= lo) & (freqs < hi)]) / total) if total > 0 else 0
        for lo, hi in bands
    }


def main():
    print("=" * 80)
    print("V18 PHASE 3 — SYNTHESE v3 (GOLDILOCKS)")
    print("=" * 80)
    print("""
LEHRE:
- v1 Centroid 1.36 (zu hell) — 4kHz zu laut
- v2 Centroid 0.65 (zu bass) — Sub-Bass zu fett
- v2 75% Sub-Bass vs Original 64% → 11% Überschuss
- v2 7.7% Low-Mid vs Original 15.5% → 8% Defizit

FIX: Sub-Bass halbieren, 300Hz verdoppeln, 600Hz NEU dazu
""")

    out_dir = Path("bbox/v18_20260707")
    sr = 44100
    dauer_s = 255.11

    print("-" * 80)
    print("1. KOMPONENTEN GENERIEREN")
    print("-" * 80)
    traeger = generiere_traeger(dauer_s, sr=sr, freq=3940, amp=0.005)
    subbass = generiere_subbass(dauer_s, sr=sr, freqs=(40, 75, 150), amps=(0.25, 0.20, 0.10))
    mittel = generiere_mittelschicht(dauer_s, sr=sr, freq=300, amp=0.18)
    lowmid = generiere_lowmid(dauer_s, sr=sr, freq=600, amp=0.12)
    print(f"  4kHz-Träger: RMS={np.sqrt(np.mean(traeger**2)):.4f}")
    print(f"  Sub-Bass:    RMS={np.sqrt(np.mean(subbass**2)):.4f}")
    print(f"  300Hz:       RMS={np.sqrt(np.mean(mittel**2)):.4f}")
    print(f"  600Hz:       RMS={np.sqrt(np.mean(lowmid**2)):.4f}")

    sr_b, burumut_teile = lade_burumut_woerter(list(range(1, 12)), "en-us")
    positionen = [7, 23, 46, 72, 95, 125, 141, 155, 174, 200, 222]
    burumut = platziere_burumut(sr, dauer_s, burumut_teile, positionen, amplitudes=[0.15]*11)
    print(f"  BURUMUT:     RMS={np.sqrt(np.mean(burumut**2)):.4f}")

    print()
    print("-" * 80)
    print("2. MISCHEN")
    print("-" * 80)
    synth = mische(sr, dauer_s, traeger, subbass, mittel, lowmid, burumut)
    print(f"  Synth: {len(synth)} samples, RMS={np.sqrt(np.mean(synth**2)):.4f}")

    out_wav = out_dir / "synthese_v3.wav"
    audio_int16 = (synth * 32767).astype(np.int16)
    wavfile.write(out_wav, sr, audio_int16)
    print(f"  Gespeichert: {out_wav}")

    print()
    print("-" * 80)
    print("3. VERGLEICH MIT ORIGINAL")
    print("-" * 80)
    sr_orig, orig = lade_mp3()
    min_len = min(len(synth), len(orig))
    synth_t = synth[:min_len]
    orig_t = orig[:min_len]

    spec_s = spektrum_analyse(synth_t, sr)
    spec_o = spektrum_analyse(orig_t, sr)
    freqs = np.fft.rfftfreq(8192, 1.0/sr)
    log_s = np.log10(spec_s + 1e-12)
    log_o = np.log10(spec_o + 1e-12)
    r = float(np.corrcoef(log_s, log_o)[0, 1])
    cent_s = float(np.sum(freqs * spec_s) / np.sum(spec_s))
    cent_o = float(np.sum(freqs * spec_o) / np.sum(spec_o))
    ratio = cent_s / cent_o

    print(f"  Spektrum-Form-Korrelation: r = {r:.3f}")
    print(f"  Centroid: Synth={cent_s:.0f}Hz, Orig={cent_o:.0f}Hz, ratio={ratio:.3f}")

    bands_s = band_verteilung(spec_s, freqs)
    bands_o = band_verteilung(spec_o, freqs)
    print(f"  Band-Verteilung:")
    for band in bands_s:
        print(f"    {band:>10s}: Synth={bands_s[band]*100:5.1f}%  Orig={bands_o[band]*100:5.1f}%  Diff={(bands_s[band]-bands_o[band])*100:+5.1f}%")

    print()
    print("-" * 80)
    print("4. TDD-TESTS")
    print("-" * 80)
    tests = []

    t1_pass = bool(out_wav.exists() and out_wav.stat().st_size > 0)
    tests.append({"name": "T1_wav_erstellt", "pass": t1_pass,
                  "befund": f"{out_wav.stat().st_size / 1024:.0f} KB",
                  "was_sagt_es_uns": "Reproduzierbare WAV-Datei vorhanden."})

    spec_short = np.abs(np.fft.rfft(traeger[:2048] * np.hanning(2048)))**2
    freqs_short = np.fft.rfftfreq(2048, 1.0/sr)
    idx_4k = np.argmin(np.abs(freqs_short - 3940))
    power_4k = float(spec_short[idx_4k])
    t2_pass = bool(power_4k > 1e-7)
    tests.append({"name": "T2_4khz_traeger_power", "pass": t2_pass,
                  "befund": f"Power @ 3940Hz: {power_4k:.2e}",
                  "was_sagt_es_uns": "4kHz-Träger hat messbare Power."})

    spec_sb = np.abs(np.fft.rfft(subbass[:2048] * np.hanning(2048)))**2
    idx_75 = np.argmin(np.abs(freqs_short - 75))
    power_75 = float(spec_sb[idx_75])
    t3_pass = bool(power_75 > 0.5)
    tests.append({"name": "T3_75hz_subbass_power", "pass": t3_pass,
                  "befund": f"Power @ 75Hz: {power_75:.2e}",
                  "was_sagt_es_uns": "75Hz Sub-Bass hat messbare Power."})

    burumut_rms = float(np.sqrt(np.mean(burumut**2)))
    t4_pass = bool(burumut_rms > 0.001)
    tests.append({"name": "T4_burumut_platziert", "pass": t4_pass,
                  "befund": f"BURUMUT-RMS: {burumut_rms:.4f}",
                  "was_sagt_es_uns": "BURUMUT-Wörter sind im Signal platziert."})

    t5_pass = bool(0.8 <= ratio <= 1.2)
    tests.append({"name": "T5_centroid_zentriert", "pass": t5_pass,
                  "befund": f"ratio = {ratio:.3f} (Ziel: 0.8-1.2)",
                  "was_sagt_es_uns": f"Centroid {ratio:.3f} - {'ZENTRIERT' if t5_pass else 'AUSSERHALB'}."})

    n_pass = int(sum(1 for t in tests if t["pass"]))

    output = {
        "phase": "V18 Phase 3 — Synthese v3 (Goldilocks)",
        "n_tests": len(tests),
        "n_pass": n_pass,
        "spektrum_korrelation": float(r),
        "centroid_synth_hz": float(cent_s),
        "centroid_orig_hz": float(cent_o),
        "centroid_ratio": float(ratio),
        "band_verteilung_synth": bands_s,
        "band_verteilung_orig": bands_o,
        "tests": tests,
        "verdict": f"V18 Phase 3: {n_pass}/{len(tests)} PASS. r={r:.3f}, Centroid-ratio={ratio:.3f}.",
        "lehr_aus_phase1_2": "v1=1.36 (hell), v2=0.65 (bass). v3: Sub-Bass halbiert, 300Hz verdoppelt, 600Hz neu.",
    }

    out_json = out_dir / "phase3_synthese_v3.json"
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
