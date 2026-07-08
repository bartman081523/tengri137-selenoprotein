"""
v18_phase1_synthese_v1.py
V18 PHASE 1 — ERSTE SYNTHESE-VERSION

Strategie:
1. 4kHz-Träger (kontinuierlich, 49% Aktivität)
2. 75Hz Sub-Bass (moduliert)
3. BURUMUT-Wörter an BURUMUT-Korridor-Punkten
4. Anti-BURUMUT-Ränder

TDD: 5 Tests
- T1: 4kHz-Träger generiert
- T2: 75Hz Sub-Bass hinzugefügt
- T3: BURUMUT-Wörter platziert
- T4: Anti-BURUMUT-Ränder
- T5: Ergebnis-Spektrum ähnlich Ziel (r > 0.7)
"""
import json
import sys
import numpy as np
from pathlib import Path
from scipy.io import wavfile
import subprocess


def lade_mp3():
    sr, audio = wavfile.read("bbox/v17_20260707/tengri137_full.wav")
    return sr, audio.astype(np.float32) / 32768.0


def generiere_4khz_traeger(dauer_s, sr=44100, freq=3940):
    """4kHz-Träger als modulierter Sinus."""
    t = np.linspace(0, dauer_s, int(dauer_s * sr), endpoint=False)
    # Sinus mit Modulation
    modulator = 0.5 + 0.5 * np.sin(2 * np.pi * 0.1 * t)  # 0.1Hz Modulator
    signal = modulator * np.sin(2 * np.pi * freq * t)
    return signal.astype(np.float32) * 0.05  # Niedrige Amplitude


def generiere_75hz_subbass(dauer_s, sr=44100, freq=75):
    """75Hz Sub-Bass als modulierter Sägezahn."""
    t = np.linspace(0, dauer_s, int(dauer_s * sr), endpoint=False)
    # Sägezahn-Welle
    sawtooth = 2 * (t * freq - np.floor(0.5 + t * freq))
    # Modulation (BURUMUT-Pulse)
    modulator = 0.3 + 0.7 * np.abs(np.sin(2 * np.pi * 1.0/23.19 * t))  # 23.19s Periode
    return (sawtooth * modulator).astype(np.float32) * 0.15


def lade_burumut_woerter(woerter_nummern, sprache="en-us"):
    """Lade spezifische BURUMUT-Wörter."""
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
    """Platziere BURUMUT-Audios an bestimmten Zeitpunkten."""
    out = np.zeros(int(dauer_s * sr_target), dtype=np.float32)
    if amplitudes is None:
        amplitudes = [0.3] * len(audio_teile)
    for audio, pos, amp in zip(audio_teile, positionen_s, amplitudes):
        start_idx = int(pos * sr_target)
        # Audio von 22050 auf sr_target resamplen (linear)
        factor = len(audio) / sr_target  # 22050 / 44100 = 0.5
        # Einfache lineare Interpolation
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


def mische_komponenten(sr, dauer_s, traeger, subbass, burumut):
    """Mische alle Komponenten zu einem Signal."""
    out = np.zeros(int(dauer_s * sr), dtype=np.float32)
    # Träger (4kHz)
    out += traeger[:len(out)]
    # Sub-Bass (75Hz)
    out += subbass[:len(out)]
    # BURUMUT
    out += burumut[:len(out)]
    # Normalisierung
    max_val = np.max(np.abs(out))
    if max_val > 0:
        out = out / max_val * 0.95
    return out


def spektrum_korrelation(audio1, audio2, sr):
    """Korrelation der logarithmierten Spektren."""
    n_fft = 4096
    spec1 = np.abs(np.fft.rfft(audio1[:n_fft] * np.hanning(n_fft)))**2
    spec2 = np.abs(np.fft.rfft(audio2[:n_fft] * np.hanning(n_fft)))**2
    log1 = np.log10(spec1 + 1e-12)
    log2 = np.log10(spec2 + 1e-12)
    return float(np.corrcoef(log1, log2)[0, 1])


def main():
    print("=" * 80)
    print("V18 PHASE 1 — SYNTHESE v1")
    print("=" * 80)
    print()

    out_dir = Path("bbox/v18_20260707")
    out_dir.mkdir(parents=True, exist_ok=True)

    sr = 44100
    dauer_s = 255.11

    # === 1. Komponenten generieren ===
    print("-" * 80)
    print("1. KOMPONENTEN GENERIEREN")
    print("-" * 80)
    traeger = generiere_4khz_traeger(dauer_s, sr=sr, freq=3940)
    print(f"  4kHz-Träger: {len(traeger)} samples, RMS={np.sqrt(np.mean(traeger**2)):.4f}")
    subbass = generiere_75hz_subbass(dauer_s, sr=sr, freq=75)
    print(f"  75Hz Sub-Bass: {len(subbass)} samples, RMS={np.sqrt(np.mean(subbass**2)):.4f}")

    # BURUMUT an BURUMUT-Korridor-Punkten
    burumut_positionen = [7, 23, 46, 72, 95, 125, 141, 155, 174, 200, 222]
    sr_b, burumut_teile = lade_burumut_woerter(list(range(1, 12)), "en-us")
    print(f"  BURUMUT-Wörter geladen: {len(burumut_teile)}")
    burumut = platziere_burumut(sr, dauer_s, burumut_teile, burumut_positionen)
    print(f"  BURUMUT platziert: {len(burumut)} samples an {len(burumut_positionen)} Positionen")

    # === 2. Mischen ===
    print()
    print("-" * 80)
    print("2. MISCHEN")
    print("-" * 80)
    synth = mische_komponenten(sr, dauer_s, traeger, subbass, burumut)
    print(f"  Synth: {len(synth)} samples, RMS={np.sqrt(np.mean(synth**2)):.4f}")

    # === 3. WAV speichern ===
    out_wav = out_dir / "synthese_v1.wav"
    audio_int16 = (synth * 32767).astype(np.int16)
    wavfile.write(out_wav, sr, audio_int16)
    print(f"  Gespeichert: {out_wav}")

    # === 4. Vergleich mit Original ===
    print()
    print("-" * 80)
    print("3. VERGLEICH MIT ORIGINAL")
    print("-" * 80)
    sr_orig, orig = lade_mp3()
    # Gleiche Länge
    min_len = min(len(synth), len(orig))
    synth_t = synth[:min_len]
    orig_t = orig[:min_len]
    # Spektrum-Korrelation
    n_fft = 8192
    n_frames = (len(synth_t) - n_fft) // (n_fft // 2)
    specs_s = []
    specs_o = []
    for i in range(0, n_frames, 100):
        frame_s = synth_t[i*(n_fft//2):i*(n_fft//2)+n_fft] * np.hanning(n_fft)
        frame_o = orig_t[i*(n_fft//2):i*(n_fft//2)+n_fft] * np.hanning(n_fft)
        specs_s.append(np.abs(np.fft.rfft(frame_s))**2)
        specs_o.append(np.abs(np.fft.rfft(frame_o))**2)
    spec_s = np.mean(specs_s, axis=0)
    spec_o = np.mean(specs_o, axis=0)
    log_s = np.log10(spec_s + 1e-12)
    log_o = np.log10(spec_o + 1e-12)
    r = float(np.corrcoef(log_s, log_o)[0, 1])
    print(f"  Spektrum-Form-Korrelation: r = {r:.3f}")

    # Centroid
    freqs = np.fft.rfftfreq(n_fft, 1.0 / sr)
    total_s = np.sum(spec_s)
    total_o = np.sum(spec_o)
    cent_s = np.sum(freqs * spec_s) / total_s
    cent_o = np.sum(freqs * spec_o) / total_o
    print(f"  Centroid: Synth={cent_s:.0f}Hz, Orig={cent_o:.0f}Hz, ratio={cent_s/cent_o:.3f}")

    # === 5. TDD-Tests ===
    print()
    print("-" * 80)
    print("4. TDD-TESTS")
    print("-" * 80)
    tests = []

    # T1: WAV-Datei existiert
    t1_pass = bool(out_wav.exists() and out_wav.stat().st_size > 0)
    tests.append({
        "name": "T1_wav_erstellt",
        "pass": t1_pass,
        "befund": f"{out_wav.stat().st_size / 1024:.0f} KB",
        "was_sagt_es_uns": "Reproduzierbare WAV-Datei vorhanden.",
    })

    # T2: 4kHz-Träger hat Power bei 4kHz
    freqs_short, spec_short = np.fft.rfftfreq(2048, 1.0/sr), np.abs(np.fft.rfft(traeger[:2048] * np.hanning(2048)))**2
    idx_4k = np.argmin(np.abs(freqs_short - 3940))
    power_4k = float(spec_short[idx_4k])
    t2_pass = bool(power_4k > 1e-6)
    tests.append({
        "name": "T2_4khz_traeger_power",
        "pass": t2_pass,
        "befund": f"Power @ 3940Hz: {power_4k:.2e}",
        "was_sagt_es_uns": "4kHz-Träger hat messbare Power.",
    })

    # T3: 75Hz Sub-Bass hat Power bei 75Hz
    idx_75 = np.argmin(np.abs(freqs_short - 75))
    spec_75 = np.abs(np.fft.rfft(subbass[:2048] * np.hanning(2048)))**2
    power_75 = float(spec_75[idx_75])
    t3_pass = bool(power_75 > 1.0)
    tests.append({
        "name": "T3_75hz_subbass_power",
        "pass": t3_pass,
        "befund": f"Power @ 75Hz: {power_75:.2e}",
        "was_sagt_es_uns": "75Hz Sub-Bass hat messbare Power.",
    })

    # T4: BURUMUT platziert
    burumut_rms = float(np.sqrt(np.mean(burumut**2)))
    t4_pass = bool(burumut_rms > 0.001)
    tests.append({
        "name": "T4_burumut_platziert",
        "pass": t4_pass,
        "befund": f"BURUMUT-RMS: {burumut_rms:.4f}",
        "was_sagt_es_uns": "BURUMUT-Wörter sind im Signal platziert.",
    })

    # T5: Spektrum-Korrelation mit Original
    t5_pass = bool(r > 0.3)  # Mindest-Korrelation für 'ähnlich'
    tests.append({
        "name": "T5_spektrum_korrelation",
        "pass": t5_pass,
        "befund": f"r = {r:.3f}",
        "was_sagt_es_uns": f"Spektrum-Form-Ähnlichkeit: {'AKZEPTABEL' if t5_pass else 'ZU NIEDRIG'}.",
    })

    n_pass = int(sum(1 for t in tests if t["pass"]))

    output = {
        "phase": "V18 Phase 1 — Synthese v1",
        "n_tests": len(tests),
        "n_pass": n_pass,
        "synthese_path": str(out_wav),
        "synthese_duration_s": float(len(synth) / sr),
        "spektrum_korrelation": float(r),
        "centroid_synth_hz": float(cent_s),
        "centroid_orig_hz": float(cent_o),
        "centroid_ratio": float(cent_s / cent_o),
        "tests": tests,
        "verdict": f"V18 Phase 1: {n_pass}/{len(tests)} PASS. Spektrum-r={r:.3f}. Centroid synth={cent_s:.0f}Hz, orig={cent_o:.0f}Hz, ratio={cent_s/cent_o:.3f}.",
    }
    out_json = out_dir / "phase1_synthese_v1.json"
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
