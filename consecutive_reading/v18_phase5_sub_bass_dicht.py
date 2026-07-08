"""
v18_phase5_sub_bass_dicht.py
V18 PHASE 5 — DICHTER SUB-BASS

LEHRE AUS PHASE 4:
- 200Hz Sinus leakt 22% ins 100-300Hz-Band
- BURUMUT ist in 1000-3000Hz konzentriert (54%)
- 60Hz allein erreicht nur 47% Sub-Bass statt 64%
- Iteratives Anpassen verschlechterte r von 0.339 → 0.255

NEUER ANSATZ:
- Sub-Bass: 30+45+60+75+90Hz (5 Töne unter 100Hz)
- 200Hz-Band: 130+180+250Hz (3 Töne)
- 500Hz-Band: 350+500+700Hz (3 Töne)
- 2000Hz-Band: 1200+2000+2800Hz (3 Töne)
- 4kHz-Träger: 3500+4000Hz
- BURUMUT intakt

So ist jedes Band mit MEHREREN Tönen gefüllt → bessere spektrale Verteilung.
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


def generiere_multi(dauer_s, sr, freqs, amps, puls_s=23.19, puls_amp=0.5, saw=False):
    """Mehrere Töne mit gemeinsamer BURUMUT-Pulsation."""
    t = np.linspace(0, dauer_s, int(dauer_s * sr), endpoint=False)
    puls = (1 - puls_amp) + puls_amp * np.abs(np.sin(2 * np.pi * 1.0/puls_s * t))
    out = np.zeros_like(t)
    for f, a in zip(freqs, amps):
        if saw:
            sig = 2 * (t * f - np.floor(0.5 + t * f))
        else:
            sig = np.sin(2 * np.pi * f * t)
        out += sig.astype(np.float32) * a
    return (out * puls).astype(np.float32)


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
    print("V18 PHASE 5 — DICHTER SUB-BASS (mehrere Töne pro Band)")
    print("=" * 80)

    out_dir = Path("bbox/v18_20260707")
    sr = 44100
    dauer_s = 255.11
    bands_def = [(0, 100), (100, 300), (300, 1000), (1000, 3000), (3000, 8000)]

    sr_orig, orig = lade_mp3()
    spec_o = spektrum_analyse(orig, sr)
    freqs = np.fft.rfftfreq(8192, 1.0/sr)
    orig_bands = band_verteilung(spec_o, freqs, bands_def)

    # === Architektur: mehrere Töne pro Band ===
    # Sub-Bass 0-100Hz: 30, 45, 60, 75, 90 (5 Töne) - Sägezahn für Obertöne
    sub = generiere_multi(dauer_s, sr,
                           freqs=[30, 45, 60, 75, 90],
                           amps=[0.20, 0.25, 0.30, 0.20, 0.15],
                           saw=True)
    # Bass 100-300Hz: 130, 180, 250
    bass = generiere_multi(dauer_s, sr,
                            freqs=[130, 180, 250],
                            amps=[0.10, 0.08, 0.06])
    # Low-Mid 300-1000Hz: 350, 500, 700, 900
    lowmid = generiere_multi(dauer_s, sr,
                              freqs=[350, 500, 700, 900],
                              amps=[0.06, 0.05, 0.04, 0.03])
    # Mid 1000-3000Hz: 1200, 1800, 2500
    mid = generiere_multi(dauer_s, sr,
                           freqs=[1200, 1800, 2500],
                           amps=[0.04, 0.03, 0.02])
    # High 3000+Hz: 3500, 4000
    high = generiere_multi(dauer_s, sr,
                            freqs=[3500, 4000],
                            amps=[0.003, 0.005])

    sr_b, burumut_teile = lade_burumut_woerter(list(range(1, 12)), "en-us")
    positionen = [7, 23, 46, 72, 95, 125, 141, 155, 174, 200, 222]
    burumut = platziere_burumut(sr, dauer_s, burumut_teile, positionen, amplitudes=[0.15]*11)

    print("-" * 80)
    print("1. SCHICHTEN")
    print("-" * 80)
    for name, sig in [("Sub-Bass (5 Töne)", sub), ("Bass (3)", bass),
                       ("Low-Mid (4)", lowmid), ("Mid (3)", mid),
                       ("High (2)", high), ("BURUMUT", burumut)]:
        print(f"  {name:>20s}: RMS={np.sqrt(np.mean(sig**2)):.4f}")

    # Mischen
    out = np.zeros(int(dauer_s * sr), dtype=np.float32)
    out += sub + bass + lowmid + mid + high + burumut
    max_val = np.max(np.abs(out))
    if max_val > 0:
        out = out / max_val * 0.95

    out_wav = out_dir / "synthese_v5.wav"
    wavfile.write(out_wav, sr, (out * 32767).astype(np.int16))

    # Vergleich
    min_len = min(len(out), len(orig))
    spec_s = spektrum_analyse(out[:min_len], sr)
    synth_bands = band_verteilung(spec_s, freqs, bands_def)

    log_s = np.log10(spec_s + 1e-12)
    log_o = np.log10(spec_o + 1e-12)
    r = float(np.corrcoef(log_s, log_o)[0, 1])
    cent_s = float(np.sum(freqs * spec_s) / np.sum(spec_s))
    cent_o = float(np.sum(freqs * spec_o) / np.sum(spec_o))
    ratio = cent_s / cent_o

    print()
    print("-" * 80)
    print("2. VERGLEICH")
    print("-" * 80)
    print(f"  Spektrum-r: {r:.3f}")
    print(f"  Centroid: {cent_s:.0f}Hz vs {cent_o:.0f}Hz, ratio={ratio:.3f}")
    print(f"  Band-Verteilung:")
    for band in orig_bands:
        s = synth_bands[band]
        o = orig_bands[band]
        print(f"    {band:>10s}: Synth={s*100:5.1f}%  Orig={o*100:5.1f}%  Diff={(s-o)*100:+5.1f}%")

    # TDD
    print()
    print("-" * 80)
    print("3. TDD-TESTS")
    print("-" * 80)
    tests = []
    tests.append({"name": "T1_wav", "pass": bool(out_wav.exists()),
                  "befund": f"{out_wav.stat().st_size/1024:.0f}KB",
                  "was_sagt_es_uns": "WAV erstellt."})
    max_diff = max(abs(synth_bands[b] - orig_bands[b]) for b in orig_bands)
    tests.append({"name": "T2_bands", "pass": bool(max_diff < 0.10),
                  "befund": f"max_diff={max_diff*100:.1f}%",
                  "was_sagt_es_uns": f"Band-Match: {'OK' if max_diff < 0.10 else 'ABWEICHUNG'}."})
    tests.append({"name": "T3_r", "pass": bool(r > 0.5),
                  "befund": f"r={r:.3f}",
                  "was_sagt_es_uns": f"Spektrum-Form: {'OK' if r > 0.5 else 'SCHWACH'}."})
    burumut_rms = float(np.sqrt(np.mean(burumut**2)))
    tests.append({"name": "T4_burumut", "pass": bool(burumut_rms > 0.001),
                  "befund": f"RMS={burumut_rms:.4f}",
                  "was_sagt_es_uns": "BURUMUT platziert."})
    tests.append({"name": "T5_centroid", "pass": bool(0.85 <= ratio <= 1.15),
                  "befund": f"ratio={ratio:.3f}",
                  "was_sagt_es_uns": f"Centroid: {'ZENTRIERT' if 0.85 <= ratio <= 1.15 else 'daneben'}."})

    n_pass = int(sum(1 for t in tests if t["pass"]))
    out_json = out_dir / "phase5_dichter_subbass.json"
    output = {
        "phase": "V18 Phase 5 — Dichter Sub-Bass",
        "n_pass": n_pass,
        "n_tests": len(tests),
        "spektrum_r": float(r),
        "centroid_ratio": float(ratio),
        "max_band_diff": float(max_diff),
        "synth_bands": synth_bands,
        "orig_bands": orig_bands,
        "tests": tests,
        "verdict": f"V18 Phase 5: {n_pass}/{len(tests)} PASS. r={r:.3f}, max_diff={max_diff*100:.1f}%, ratio={ratio:.3f}.",
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
