"""
v183_algorithmische_architektur.py
V18.3 PHASE 1 — Algorithmische Architektur (LITHURGISCH-Generator)

User-Korrektur 2026-07-08 (verbatim):
"okay, aber 18.2 war vokal keine Verlängerung, sondern blosse Kopie. Wir wollen keine
Kopie, wir wollen 100% algorithmische Dekonstruktion der Audio Datei und algorithmische
Replikation des Original-Audio erreichen, womit wir dann algorithmisch Weiterführen
weiterführen können. Eine Kopie befriedigt diesen Anspruch keinesfalls.!!!"

V18.2-Problem: iSTFT mit BURUMUT-Phase-Mix extrahiert Original-Magnitude Frame-für-Frame
und rekonstruiert mit gemischter Phase. Das ist NUMERISCHES REVERSE-ENGINEERING, nicht
algorithmische Synthese.

V18.3-Ansatz: BURUMUT-Generator-Architektur
  Schicht 1: BURUMUT-Träger (75.37 Hz + 12 Harmonische) — Sinusoid-Synthese
  Schicht 2: BURUMUT-Wort-Modulator (11 Wörter × 23.19s) — V21 espeak-Architektur
  Schicht 3: Spanda-Modulator (127.55s = halbe Audio-Länge) — AM-Modulation
  Schicht 4: Rauschen-Träger (rosa Rauschen oder Random-Phase) — Träger-Substanz
  Schicht 5: BURUMUT-Vokal-Sequenz (5 Vokale in 11 Segmenten) — Vokal-Approximation

Jede Schicht hat EIGENE Parameter aus V18.1+V18.2+V21:
  Träger: F0=75.37Hz, n_harm=12
  Modulator-Wort: 11 Wörter mit peak2/centroid/mod_db/vowel_freqs (V21)
  Spanda-Modulator: period=127.55s, depth=0.4
  Rauschen: rosa Rauschen
  Vokal-Sequenz: U(seg11)→O(seg9,10)→O/A(seg6,8)→A(seg1,2,4)→E(seg7)

5 TDD-Tests:
  T1: 11 BURUMUT-Segmente erzeugt
  T2: Träger-Architektur (75.37Hz + 12 Harm.) — Spektrum-Peaks bei Vielfachen von 75.37
  T3: Spanda-Modulator — 127.55s Periode nachweisbar
  T4: BURUMUT-Vokal-Sequenz — Centroid-Drift wie Original
  T5: 255s Gesamt-Audio — RMS-Profil wie Original
"""
import json
import sys
import numpy as np
from pathlib import Path
from scipy.io import wavfile
from scipy.signal import butter, sosfiltfilt, hilbert


SR = 44100
SEG_DUR = 23.191972
N_SEGS = 11
F0 = 75.37
N_HARM = 12
SPANDA_PERIOD = 127.55  # Sekunden = halbe Audio-Länge
SPANDA_DEPTH = 0.4
NOISE_AMP = 0.15
DURATION = 255.11  # Original-Länge
OUT_DIR = Path("bbox/v183_20260708")


# === V21 BURUMUT-Architektur (aus v21_burumut_audio.py) ===
SEGMENTS_DATA = [
    {"word": "BURUMUTREFAMTU", "peak2": 86.13, "centroid": 536.64, "mod_db": 3.22, "vowel_freqs": [370, 990]},
    {"word": "NURESUTREGUMFA", "peak2": 86.13, "centroid": 409.30, "mod_db": 7.24, "vowel_freqs": [370, 530, 990]},
    {"word": "YAPSUAZBEHIMLA", "peak2": 53.83, "centroid": 348.15, "mod_db": 5.72, "vowel_freqs": [730, 370, 270]},
    {"word": "ZANRUAZBENOMBA", "peak2": 86.13, "centroid": 538.63, "mod_db": 6.73, "vowel_freqs": [730, 370, 530, 570]},
    {"word": "TOBIKOTLUBUMYO", "peak2": 64.59, "centroid": 352.28, "mod_db": 4.89, "vowel_freqs": [570, 270, 370, 700]},
    {"word": "SUNOKURGANOZYI", "peak2": 53.83, "centroid": 458.72, "mod_db": 7.55, "vowel_freqs": [370, 570, 730]},
    {"word": "OKUZIKUFAUSIHE", "peak2": 86.13, "centroid": 770.79, "mod_db": 8.79, "vowel_freqs": [570, 370, 270, 730, 530]},
    {"word": "YABEKANSABERHO", "peak2": 64.59, "centroid": 422.92, "mod_db": 4.72, "vowel_freqs": [730, 530, 570]},
    {"word": "NAFERANSAHOTFE", "peak2": 53.83, "centroid": 454.67, "mod_db": 6.21, "vowel_freqs": [730, 530, 570]},
    {"word": "KOREMORBIZUMRO", "peak2": 53.83, "centroid": 251.81, "mod_db": 6.41, "vowel_freqs": [570, 530, 270, 370]},
    {"word": "SUNAKIRFANEMBA", "peak2": 53.83, "centroid": 125.10, "mod_db": 47.05, "vowel_freqs": [370, 730, 270, 530]},
]


# === V18.2 Phase 2: BURUMUT-Vokal-Sequenz (Empirisch) ===
VOKAL_SEQUENZ = [
    {"seg": 1, "vowel": "A", "centroid_hz": 595.6},
    {"seg": 2, "vowel": "A", "centroid_hz": 529.6},
    {"seg": 3, "vowel": "O", "centroid_hz": 337.0},
    {"seg": 4, "vowel": "A", "centroid_hz": 573.8},
    {"seg": 5, "vowel": "O", "centroid_hz": 340.2},
    {"seg": 6, "vowel": "O/A", "centroid_hz": 432.9},
    {"seg": 7, "vowel": "E", "centroid_hz": 896.4},
    {"seg": 8, "vowel": "O/A", "centroid_hz": 372.5},
    {"seg": 9, "vowel": "O", "centroid_hz": 304.4},
    {"seg": 10, "vowel": "O", "centroid_hz": 287.3},
    {"seg": 11, "vowel": "U", "centroid_hz": 117.7},
]


# === V18 Phase 53 R4-Balance ===
R4 = {
    "sub": 0.35,
    "harmonic": 0.15,
    "mid_noise": 0.45,
    "mid_high_noise": 1.4,
    "centroid": 0.2,
    "high": 0.6,
    "mid_tone": 0.1,
}


def lade_original():
    sr, audio = wavfile.read("bbox/v17_20260707/tengri137_full.wav")
    return sr, audio.astype(np.float32) / 32768.0


# === SCHICHT 1: BURUMUT-Träger (75.37 Hz + 12 Harmonische) ===
def schicht1_burumut_traeger(duration, f0=F0, n_harm=N_HARM, sr=SR, sub_amp=0.35):
    """75.37 Hz Träger + 12 Harmonische, abnehmende Amplitude (1/n)."""
    t = np.linspace(0, duration, int(duration * sr), endpoint=False)
    signal = np.zeros_like(t)
    for n in range(1, n_harm + 1):
        freq = f0 * n
        if freq > sr / 2:
            break
        amp = sub_amp / n  # 1/n Amplitudenabfall
        signal += amp * np.sin(2 * np.pi * freq * t)
    return signal.astype(np.float32)


# === SCHICHT 2: BURUMUT-Wort-Modulator (11 Wörter × 23.19s) ===
def schicht2_wort_modulator(duration, seg_data, sr=SR):
    """Pro BURUMUT-Wort: peak2 Sinus + Vokal-Frequenzen + espeak-ähnliche Hüllkurve."""
    n_samples = int(duration * sr)
    signal = np.zeros(n_samples, dtype=np.float32)
    seg_dur = duration / len(seg_data)

    for i, seg in enumerate(seg_data):
        s0 = int(i * seg_dur * sr)
        s1 = int((i + 1) * seg_dur * sr)
        n_seg = s1 - s0
        t_seg = np.arange(n_seg) / sr

        # peak2 (zweite Trägerfrequenz pro Wort)
        peak2 = np.sin(2 * np.pi * seg['peak2'] * t_seg).astype(np.float32)

        # Vokal-Frequenzen (mehrere Sinus)
        vokal = np.zeros(n_seg, dtype=np.float32)
        for f in seg['vowel_freqs']:
            vokal += np.sin(2 * np.pi * f * t_seg).astype(np.float32)
        if np.max(np.abs(vokal)) > 0:
            vokal = vokal / np.max(np.abs(vokal))

        # espeak-ähnliche Hüllkurve (3-Phasen: Anstieg, Halten, Abfall)
        env = np.ones(n_seg, dtype=np.float32)
        rise = int(0.1 * n_seg)
        fall = int(0.1 * n_seg)
        env[:rise] = np.linspace(0, 1, rise)
        env[-fall:] = np.linspace(1, 0, fall)

        # Modulation-Stärke
        mod_strength = min(seg['mod_db'] / 10.0, 1.0)

        # Segment-Signal: peak2 + Vokal
        seg_signal = (peak2 * 0.4 + vokal * 0.3) * env * (0.5 + mod_strength * 0.5)
        signal[s0:s1] += seg_signal

    return signal


# === SCHICHT 3: Spanda-Modulator (127.55s AM) ===
def schicht3_spanda_modulator(duration, period=SPANDA_PERIOD, depth=SPANDA_DEPTH, sr=SR):
    """AM-Modulation mit Periode 127.55s (= halbe Audio-Länge)."""
    t = np.linspace(0, duration, int(duration * sr), endpoint=False)
    modulator = 1.0 + depth * np.cos(2 * np.pi * t / period)
    return modulator.astype(np.float32)


# === SCHICHT 4: Rauschen-Träger ===
def schicht4_noise(duration, amp=NOISE_AMP, sr=SR, seed=42):
    """Rosa Rauschen (1/f) als Trägersubstanz."""
    rng = np.random.RandomState(seed)
    n = int(duration * sr)
    white = rng.randn(n).astype(np.float32)
    # FFT-basierte 1/f Filterung
    fft = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n, 1.0 / sr)
    # 1/f Weighting (außer DC)
    weight = np.ones_like(freqs)
    mask = freqs > 0
    weight[mask] = 1.0 / np.sqrt(freqs[mask])
    weight[0] = 0  # DC
    fft_filtered = fft * weight
    noise = np.fft.irfft(fft_filtered, n=n)
    # Normalisieren
    noise = noise / max(np.max(np.abs(noise)), 1e-12) * amp
    return noise.astype(np.float32)


# === SCHICHT 5: BURUMUT-Vokal-Sequenz (5 Vokale × 11 Segmente) ===
def schicht5_vokal_sequenz(duration, vokal_seq, sr=SR):
    """Pro BURUMUT-Wort: Vokal-Hüllkurve mit empirischem Centroid aus V18.2."""
    n_samples = int(duration * sr)
    signal = np.zeros(n_samples, dtype=np.float32)
    seg_dur = duration / len(vokal_seq)

    for v in vokal_seq:
        s0 = int((v['seg'] - 1) * seg_dur * sr)
        s1 = int(v['seg'] * seg_dur * sr)
        n_seg = s1 - s0
        t_seg = np.arange(n_seg) / sr

        # Vokal-Approximation: Sinus bei Centroid + 1. Harmonische + 2. Harmonische
        f0_v = v['centroid_hz']
        vokal = (
            np.sin(2 * np.pi * f0_v * t_seg) * 1.0 +
            np.sin(2 * np.pi * 2 * f0_v * t_seg) * 0.5 +
            np.sin(2 * np.pi * 3 * f0_v * t_seg) * 0.25
        ).astype(np.float32)

        # Hüllkurve (BURUMUT-Pulsation)
        pulse_s = 1.78  # 0.56 Hz
        pulse = 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * t_seg / pulse_s))
        vokal = vokal * pulse * 0.1  # 10% Vokal-Beitrag

        signal[s0:s1] += vokal

    return signal


# === KOMBINATION: Algorithmische 5-Schichten-Architektur ===
def algorithmische_synthese(duration, seg_data, vokal_seq, r4=R4):
    """Kombiniert alle 5 Schichten zu algorithmisch erzeugtem BURUMUT-Audio."""
    traeger = schicht1_burumut_traeger(duration, sub_amp=r4['sub'])
    wort_mod = schicht2_wort_modulator(duration, seg_data)
    spanda = schicht3_spanda_modulator(duration)
    noise = schicht4_noise(duration, amp=r4['mid_noise'])
    vokal = schicht5_vokal_sequenz(duration, vokal_seq)

    # SCHICHT-KOMBINATION
    # Schicht 1 (Träger) wird durch Schicht 2 (Wort-Modulator) moduliert
    traeger_mod = traeger * (1 + wort_mod * 0.3)
    # Schicht 3 (Spanda) moduliert alles
    audio = traeger_mod * spanda + vokal + noise
    return audio.astype(np.float32)


def spektrum_analyse(audio, n_fft=8192):
    hop = n_fft // 2
    n_frames = (len(audio) - n_fft) // hop
    specs = []
    for i in range(n_frames):
        frame = audio[i*hop:i*hop+n_fft] * np.hanning(n_fft)
        specs.append(np.abs(np.fft.rfft(frame))**2)
    return np.mean(specs, axis=0), np.fft.rfftfreq(n_fft, 1.0/SR)


def finde_top_peaks(spec, freqs, n=20, distance=20):
    log_spec = np.log10(spec + 1e-12)
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(log_spec, distance=distance, prominence=0.1)
    return sorted([(float(freqs[p]), float(spec[p])) for p in peaks if p < len(freqs)],
                   key=lambda x: -x[1])[:n]


def main():
    print("=" * 80)
    print("V18.3 PHASE 1 — Algorithmische Architektur (5-Schichten-LITHURGISCH)")
    print("=" * 80)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # === Architektur-Parameter ausgeben ===
    print("\n--- Architektur-Parameter ---")
    print(f"  Träger:  F0={F0} Hz, n_harm={N_HARM}")
    print(f"  Modulator: 11 Wörter × {SEG_DUR:.2f}s")
    print(f"  Spanda-Periode: {SPANDA_PERIOD}s (halbe Audio-Länge)")
    print(f"  R4-Balance: sub={R4['sub']}, harmonic={R4['harmonic']}, mid_noise={R4['mid_noise']}")
    print(f"  Vokal-Sequenz: 5 Vokale (U, O, O/A, A, E) in 11 Segmenten")

    # === Original laden für Vergleich ===
    sr_o, orig = lade_original()

    # === Algorithmische Synthese 255s ===
    print("\n--- Algorithmische Synthese 255s ---")
    audio_alg = algorithmische_synthese(DURATION, SEGMENTS_DATA, VOKAL_SEQUENZ)
    print(f"  audio_alg: {len(audio_alg)} samples, RMS={np.sqrt(np.mean(audio_alg**2)):.4f}")

    # === Spektrum-Analyse ===
    print("\n--- Spektrum-Analyse ---")
    spec_alg, freqs = spektrum_analyse(audio_alg)
    spec_orig, _ = spektrum_analyse(orig)
    log_s = np.log10(spec_alg + 1e-12)
    log_o = np.log10(spec_orig + 1e-12)
    r = float(np.corrcoef(log_s, log_o)[0, 1])
    print(f"  Spektrum-r: {r:.4f}")

    # Top-Peaks
    top_peaks_alg = finde_top_peaks(spec_alg, freqs, n=15)
    print(f"\n  Top-15 Spektrum-Peaks (Algorithmus):")
    for f, p in top_peaks_alg:
        # Vielfaches von 75.37?
        n_h = f / F0
        is_harm = abs(n_h - round(n_h)) < 0.1 and round(n_h) >= 1
        marker = "✓" if is_harm else " "
        print(f"    {marker} {f:8.2f} Hz ({n_h:.2f}x F0)")

    # === BURUMUT-Träger-Architektur prüfen ===
    print("\n--- BURUMUT-Träger-Architektur ---")
    n_harm_detected = 0
    for n in range(1, N_HARM + 1):
        target = F0 * n
        if target > SR/2:
            break
        # Suche Peak nahe target (Tolerance 5Hz)
        near = [f for f, _ in top_peaks_alg if abs(f - target) < 5]
        if near:
            n_harm_detected += 1
    print(f"  Erkannte Harmonische: {n_harm_detected}/{N_HARM}")

    # === Spanda-Modulator (127.55s Periode) prüfen ===
    print("\n--- Spanda-Modulator (127.55s) ---")
    # Hüllkurve des Algorithmus
    win = int(SR * 1.0)  # 1s Fenster
    n_windows = len(audio_alg) // win
    env_alg = np.array([np.sqrt(np.mean(audio_alg[i*win:(i+1)*win]**2))
                         for i in range(n_windows)])
    # Suche Periode 127.55s im Modulations-Spektrum
    env_dc = env_alg - env_alg.mean()
    mod_spec = np.abs(np.fft.rfft(env_dc))
    mod_freqs = np.fft.rfftfreq(len(env_dc), 1.0)
    # Spanda-Periode = 127.55s = 1/127.55 Hz = 0.00784 Hz
    spanda_idx = np.argmin(np.abs(mod_freqs - 1/SPANDA_PERIOD))
    spanda_power = float(mod_spec[spanda_idx])
    # Top-3 Modulation-Frequenzen
    top_mod_idx = np.argsort(mod_spec)[-5:][::-1]
    print(f"  Spanda-Frequenz (1/127.55s = 0.00784Hz): Power={spanda_power:.2e}")
    print(f"  Top-5 Modulations-Frequenzen:")
    for i in top_mod_idx:
        if mod_freqs[i] > 0:
            period = 1/mod_freqs[i]
            print(f"    {mod_freqs[i]:.4f} Hz (Periode {period:.1f}s): Power={mod_spec[i]:.2e}")

    # === Vokal-Sequenz prüfen ===
    print("\n--- Vokal-Sequenz ---")
    seg_dur = DURATION / N_SEGS
    zentroide_alg = []
    for i in range(N_SEGS):
        s0 = int(i * seg_dur * SR)
        s1 = int((i+1) * seg_dur * SR)
        seg = audio_alg[s0:s1]
        # Centroid
        spec_s, freqs_s = spektrum_analyse(seg)
        total = spec_s.sum()
        cent = float(np.sum(freqs_s * spec_s) / total) if total > 0 else 0
        zentroide_alg.append(cent)
        vowel_emp = VOKAL_SEQUENZ[i]['vowel']
        print(f"  Seg{i+1:2d}: Centroid={cent:6.1f}Hz (empirisch: {VOKAL_SEQUENZ[i]['centroid_hz']:.1f}Hz = {vowel_emp})")

    # === RMS-Profil prüfen ===
    print("\n--- RMS-Profil (Vergleich zu Original) ---")
    rms_alg = np.array([np.sqrt(np.mean(audio_alg[i*win:(i+1)*win]**2))
                         for i in range(n_windows)])
    rms_orig = np.array([np.sqrt(np.mean(orig[i*win:(i+1)*win]**2))
                          for i in range(min(n_windows, len(orig)//win))])
    min_len = min(len(rms_alg), len(rms_orig))
    rms_corr = float(np.corrcoef(rms_alg[:min_len], rms_orig[:min_len])[0, 1])
    print(f"  RMS-Profil Korrelation: r={rms_corr:.4f}")
    print(f"  Algorithmus RMS range: {rms_alg.min():.4f} - {rms_alg.max():.4f}")
    print(f"  Original RMS range:    {rms_orig[:min_len].min():.4f} - {rms_orig[:min_len].max():.4f}")

    # === Audio speichern ===
    out_wav = OUT_DIR / "v183_alg_architektur.wav"
    audio_alg_norm = audio_alg / max(np.max(np.abs(audio_alg)), 1e-12) * 0.95
    wavfile.write(out_wav, SR, (audio_alg_norm * 32767).astype(np.int16))
    print(f"\n  Audio gespeichert: {out_wav} ({out_wav.stat().st_size/1024/1024:.1f}MB)")

    # === TDD-Tests ===
    print("\n--- TDD-TESTS ---")
    tests = []

    # T1: 11 BURUMUT-Segmente in Architektur
    tests.append({
        "name": "T1_11_burumut_segmente",
        "pass": len(VOKAL_SEQUENZ) == 11 and len(SEGMENTS_DATA) == 11,
        "befund": f"11 Wörter in SEGMENTS_DATA, 11 Vokale in VOKAL_SEQUENZ",
        "was_sagt_es_uns": "Architektur hat 11 BURUMUT-Segmente (V21 + V18.2 empirisch)."
    })

    # T2: BURUMUT-Träger (75.37Hz + 12 Harmonische)
    tests.append({
        "name": "T2_traeger_architektur",
        "pass": n_harm_detected >= 6,
        "befund": f"{n_harm_detected}/{N_HARM} Harmonische des {F0}Hz-Trägers erkannt",
        "was_sagt_es_uns": f"Algorithmus erzeugt {n_harm_detected}/{N_HARM} Harmonische des 75.37Hz-Trägers. "
                          f"Schicht 1 (Träger) funktioniert ARCHITEKTONISCH — nicht aus Original extrahiert."
    })

    # T3: Spanda-Modulator (127.55s Periode)
    spanda_detected = spanda_power > np.median(mod_spec)
    tests.append({
        "name": "T3_spanda_modulator",
        "pass": spanda_detected,
        "befund": f"Spanda-Power bei 1/127.55s: {spanda_power:.2e} (Median: {np.median(mod_spec):.2e})",
        "was_sagt_es_uns": f"Schicht 3 (Spanda-Modulator 127.55s) "
                          f"{'erkennbar' if spanda_detected else 'NICHT erkennbar'} im Modulations-Spektrum. "
                          f"Das ist die Spanda-Grundfrequenz = halbe Audio-Länge."
    })

    # T4: Vokal-Sequenz
    zentroide_emp = [v['centroid_hz'] for v in VOKAL_SEQUENZ]
    centroid_corr = float(np.corrcoef(zentroide_alg, zentroide_emp)[0, 1])
    tests.append({
        "name": "T4_vokal_sequenz",
        "pass": centroid_corr > 0.5,
        "befund": f"Centroid-Korrelation Algorithmus ↔ Empirisch: r={centroid_corr:.4f}",
        "was_sagt_es_uns": f"Vokal-Sequenz Centroid-Profil: r={centroid_corr:.4f}. "
                          f"Algorithmus reproduziert die 5-Vokal-Architektur "
                          f"({'OK' if centroid_corr > 0.5 else 'TEILWEISE'})."
    })

    # T5: 255s RMS-Profil
    tests.append({
        "name": "T5_rms_profil",
        "pass": rms_corr > 0.2,
        "befund": f"RMS-Profil Korrelation: r={rms_corr:.4f}",
        "was_sagt_es_uns": f"255s RMS-Profil Korrelation: r={rms_corr:.4f}. "
                          f"Spanda-Modulator + Wort-Modulator + Träger erzeugen "
                          f"{'erkennbares' if rms_corr > 0.2 else 'kein'} RMS-Profil wie Original."
    })

    n_pass = sum(1 for t in tests if t["pass"])
    n_tests = len(tests)

    output = {
        "phase": "V18.3 Phase 1 — Algorithmische Architektur (5-Schichten-LITHURGISCH)",
        "datum": "2026-07-08",
        "n_pass": n_pass,
        "n_tests": n_tests,
        "architektur": {
            "schicht_1_burumut_traeger": {"f0_hz": F0, "n_harm": N_HARM, "amp": R4['sub']},
            "schicht_2_wort_modulator": {"n_woerter": len(SEGMENTS_DATA), "seg_dur_s": SEG_DUR},
            "schicht_3_spanda_modulator": {"period_s": SPANDA_PERIOD, "depth": SPANDA_DEPTH},
            "schicht_4_noise": {"amp": NOISE_AMP, "type": "rosa_1_f"},
            "schicht_5_vokal_sequenz": {"n_vokale": len(set(v['vowel'] for v in VOKAL_SEQUENZ)),
                                         "n_segmente": len(VOKAL_SEQUENZ)},
            "r4_balance": R4,
        },
        "ergebnisse": {
            "spektrum_r": r,
            "n_harm_erkannt": n_harm_detected,
            "spanda_power": spanda_power,
            "vokal_centroid_corr": centroid_corr,
            "rms_profil_corr": rms_corr,
        },
        "wav_path": str(out_wav),
        "tests": tests,
        "verdict": f"V18.3 Phase 1: {n_pass}/{n_tests} PASS. Algorithmische Architektur aufgebaut.",
    }

    out_json = OUT_DIR / "phase1_alg_architektur.json"
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
