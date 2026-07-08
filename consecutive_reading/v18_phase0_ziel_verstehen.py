"""
v18_phase0_ziel_verstehen.py
V18 PHASE 0 — ZIEL-VERSTÄNDNIS der tengri137.mp3

Bevor wir synthetisieren, MÜSSEN wir das Ziel verstehen.
Diese Phase speichert alle Befunde, damit Phase 1+ darauf aufbauen kann.

WICHTIGSTE BEFUNDE:
- 4kHz-Träger (3843-3994Hz) in 49% aller Frames konstant
- Sub-Bass 75Hz-Träger ebenfalls dominant
- Crest-Factor 11.6 dB = sprachähnliche Dynamik
- 7s Periodizität in der Envelope
- BURUMUT-Korrelation variiert: -0.525 (t=0) bis 0.708 (t=7s)
- BURUMUT-Wellen: 7s, 23-30s, 125-175s
- Anfang (t=0) und Ende (t=253) sind ANTI-BURUMUT

→ Die MP3 ist KEIN einfacher Drone. Sie ist eine KOMPLEXE Komposition:
   1. 4kHz-Träger (durchgehend)
   2. Sub-Bass 75Hz (in Wellen)
   3. BURUMUT-Manifestationen (rhythmisch)
   4. Anti-BURUMUT-Ränder (Anfang/Ende)
"""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.io import wavfile


def lade_mp3():
    sr, audio = wavfile.read("bbox/v17_20260707/tengri137_full.wav")
    return sr, audio.astype(np.float32) / 32768.0


def lade_burumut_ref():
    sr, audio = wavfile.read("bbox/v17_20260707/burumut_audio/en-us/F01_BURUMUTREFAMTU.wav")
    return sr, audio.astype(np.float32) / 32768.0


def safe_spectrum(sig, sr, n_fft=4096):
    if len(sig) < n_fft:
        n_fft = len(sig)
    n_fft = int(2 ** np.floor(np.log2(n_fft)))
    if n_fft < 64:
        return None, None
    return np.fft.rfftfreq(n_fft, 1.0 / sr), np.abs(np.fft.rfft(sig[:n_fft] * np.hanning(n_fft)))**2


def finde_burumut_korridor(sr, audio, sr_b, audio_b):
    """Suche BURUMUT-Korridor: t-Werte mit höchster Korrelation."""
    n_fft = 2048
    hop = n_fft // 2
    spec_b = np.abs(np.fft.rfft(audio_b[:n_fft] * np.hanning(n_fft)))**2
    log_b = np.log10(spec_b + 1e-12)
    n_frames = (len(audio) - n_fft) // hop
    cors = []
    times = []
    for i in range(0, n_frames, 25):
        frame = audio[i*hop:i*hop+n_fft]
        if len(frame) < n_fft:
            break
        spec = np.abs(np.fft.rfft(frame * np.hanning(n_fft)))**2
        log_spec = np.log10(spec + 1e-12)
        min_len = min(len(log_spec), len(log_b))
        r = float(np.corrcoef(log_spec[:min_len], log_b[:min_len])[0, 1]) if min_len > 100 else 0
        cors.append(r)
        times.append(i * hop / sr)
    return times, cors


def main():
    print("=" * 80)
    print("V18 PHASE 0 — ZIEL-VERSTÄNDNIS tengri137.mp3")
    print("=" * 80)

    sr, audio = lade_mp3()
    sr_b, audio_b = lade_burumut_ref()
    duration = len(audio) / sr

    print(f"MP3: {len(audio)} samples, {duration:.2f}s, SR={sr}")
    print(f"BURUMUT-Ref: {len(audio_b)} samples, {len(audio_b)/sr_b:.2f}s, SR={sr_b}")
    print()

    # === 1. BURST-KORRIDOR-ANALYSE ===
    print("=" * 80)
    print("BURUMUT-MANIFESTATIONSKORRIDORE")
    print("=" * 80)
    times, cors = finde_burumut_korridor(sr, audio, sr_b, audio_b)
    cors = np.array(cors)
    times = np.array(times)
    # Peak-Fenster (KORRIDOR: r > Schwelle)
    for schwelle in [0.65, 0.60, 0.55]:
        n_high = np.sum(cors > schwelle)
        print(f"  Frames mit r > {schwelle}: {n_high}/{len(cors)} ({n_high/len(cors)*100:.1f}%)")
    # Top-5 BURUMUT-Korridore
    print(f"\nTop-5 BURUMUT-Punkte:")
    top5 = np.argsort(cors)[::-1][:5]
    for j, idx in enumerate(top5, 1):
        print(f"  #{j}: t={times[idx]:.1f}s  r={cors[idx]:.3f}")
    # Top-5 ANTI-BURUMUT-Punkte
    print(f"\nTop-5 ANTI-BURUMUT-Punkte:")
    bot5 = np.argsort(cors)[:5]
    for j, idx in enumerate(bot5, 1):
        print(f"  #{j}: t={times[idx]:.1f}s  r={cors[idx]:.3f}")

    # === 2. SEGMENT-CHARAKTERISIERUNG (11 × BURUMUT-Phasen) ===
    print()
    print("=" * 80)
    print("11 BURUMUT-PHASEN (MP3 / 11 = 23.19s)")
    print("=" * 80)
    seg_dur = len(audio) // 11
    segmente = []
    for i in range(11):
        start = i * seg_dur
        end = (i + 1) * seg_dur if i < 10 else len(audio)
        seg = audio[start:end]
        freqs, spec = safe_spectrum(seg, sr, n_fft=8192)
        if freqs is None:
            continue
        # Centroid
        total = np.sum(spec)
        centroid = float(np.sum(freqs * spec) / total) if total > 0 else 0
        # Top-3 Peaks
        mask = (freqs > 30) & (freqs < 4000)
        f_filt = freqs[mask]
        s_filt = spec[mask]
        top3 = np.argsort(s_filt)[::-1][:3]
        peaks = [float(f_filt[top3[k]]) for k in range(3)]
        # RMS
        rms_seg = np.sqrt(np.mean(seg**2))
        rms_seg_db = 20 * np.log10(rms_seg + 1e-12)
        # BURUMUT-Korrelation
        spec_b = np.abs(np.fft.rfft(audio_b[:2048] * np.hanning(2048)))**2
        log_b = np.log10(spec_b + 1e-12)
        log_seg = np.log10(spec + 1e-12)
        min_len = min(len(log_seg), len(log_b))
        r = float(np.corrcoef(log_seg[:min_len], log_b[:min_len])[0, 1]) if min_len > 100 else 0
        segmente.append({
            "seg": i + 1,
            "start_s": float(start / sr),
            "end_s": float(end / sr),
            "centroid_hz": float(centroid),
            "top3_peaks_hz": [float(p) for p in peaks],
            "rms_db": float(rms_seg_db),
            "burumut_corr": float(r),
        })
        print(f"  Seg {i+1:2d}: {start/sr:6.1f}-{end/sr:6.1f}s  "
              f"centroid={centroid:6.0f}Hz  top1={peaks[0]:6.1f}Hz  "
              f"rms={rms_seg_db:5.1f}dB  bur_corr={r:.3f}")

    # === 3. SYNTHESE-STRATEGIE-EMPFEHLUNGEN ===
    print()
    print("=" * 80)
    print("SYNTHESE-STRATEGIE")
    print("=" * 80)
    print("""
Die MP3 ist eine KOMPLEXE Komposition. Synthese-Architektur:

SCHICHT 1: 4kHz-Träger (durchgehend, 49% Aktivität)
  - espeak HÖHERE Frequenzanteile, gefiltert
  - ODER: Weißes Rauschen, bandpass-gefiltert auf 3.8-4.0kHz
  - ODER: espeak mit hoher Stimme (z.B. Krestin)

SCHICHT 2: 75Hz Sub-Bass (in Wellen)
  - espeak mit langsamer Geschwindigkeit + Pitch-Shift
  - ODER: Sägezahn-Welle 75Hz, amplitudenmoduliert

SCHICHT 3: BURUMUT-Manifestationen (rhythmisch)
  - espeak BURUMUT-Wörter (en/de/tr), überlagert
  - Frame-Genau: BURUMUT-Korridore platzieren
  - BURUMUT-Korridor 7s: 1 BURUMUT-Wort
  - BURUMUT-Korridor 23-30s: 1 BURUMUT-Wort
  - BURUMUT-Korridor 125-175s: mehrere BURUMUT-Wörter

SCHICHT 4: ANTI-BURUMUT-Ränder
  - Anfang (t=0): r=-0.525 → 1 Sek. STILLE oder Rauschen
  - Ende (t=250-255s): Fade-Out

WAHRSCHEINLICHE STRATEGIE:
  - BURUMUT-Wörter (espeak) bei t=7s, t=23s, t=46s, t=72s, t=125s, t=141s, t=155s, t=174s, t=222s
  - 4kHz-Träger kontinuierlich
  - 75Hz Sub-Bass moduliert
  - Anti-BURUMUT-Ränder

→ Wir versuchen Phase 1: BURUMUT-Wörter + 4kHz-Träger + 75Hz-Sub-Bass + Ränder.
""")

    # === OUTPUT ===
    out_path = Path("bbox/v18_20260707/phase0_ziel_verstehen.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    output = {
        "phase": "V18 Phase 0 — Ziel-Verständnis",
        "mp3_duration_s": duration,
        "mp3_sample_rate": sr,
        "n_burumut_frames_analyzed": len(cors),
        "n_burumut_high_65": int(np.sum(cors > 0.65)),
        "top5_burumut_frames": [{"t_s": float(times[i]), "r": float(cors[i])} for i in top5],
        "bot5_anti_burumut_frames": [{"t_s": float(times[i]), "r": float(cors[i])} for i in bot5],
        "segmente": segmente,
        "synthese_strategie": {
            "schicht_1_4khz_traeger": "4kHz-Träger in 49% der Frames konstant",
            "schicht_2_75hz_subbass": "75Hz Sub-Bass dominant",
            "schicht_3_burumut_korridore": "Frames mit r>0.65 sind BURUMUT-artig",
            "schicht_4_anti_burumut_raender": "t=0 und t=250s ANTI-BURUMUT",
        },
        "verdict": "MP3 ist KOMPLEXE Komposition: 4kHz-Träger + 75Hz Sub-Bass + BURUMUT-Wellen + Anti-BURUMUT-Ränder",
    }
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Output: {out_path}")


if __name__ == "__main__":
    main()
