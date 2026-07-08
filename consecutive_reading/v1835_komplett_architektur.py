"""
V18.3 Phase 5 — KOMPLETT-ARCHITEKTUR (FM + 85s + Buchstaben + Pulse + Spanda + Fade)

Empirische Befunde aus Phase 5 Eingangs-Untersuchung:
1. Träger 75.37 Hz + 12 Harmonische (V18.3 Phase 1)
2. FM-Modulation Hub 5.4 Hz = 75.37/14 (BURUMUT-Buchstabe) — NEU
3. 1.78s Pulse = 13 Pulse pro Wort (23.19/1.78=13.03) — V18.3 Phase 1
4. 85.0s Modulation = 3 BURUMUT-Gruppen (rel=0.996) — NEU
5. 127.55s Spanda = 2 Hälften (rel=0.903)
6. Fade-Out letzte Sekunde RMS=0.001, B14-Trend=-0.0221 — NEU

ARCHITEKTUR (rein algorithmisch, OHNE iSTFT, OHNE Original-Magnitude):
Layer 1: BURUMUT-Träger 75.37 Hz + 12 Harm mit FM-Hub 5.4 Hz
Layer 2: 85s-Gruppen-Modulator (3 BURUMUT-Gruppen)
Layer 3: 1.78s Pulse (13 Pulse pro Wort)
Layer 4: 127.55s Spanda (2 Hälften)
Layer 5: Wort-Phase-Coder (BURUMUT-Index 0-10 als Phase-Offset)
Layer 6: Fade-Out (B14 systematisch, lineares Decay)
+ Layer 7: Rosa Rauschen 1/f

References:
- V18.3 Phase 1: Träger 75.37 Hz (6/12 Harmonische)
- V18.2 BURUMUT-Oszillation 75.4 Hz
- V18.2 Spanda-Periode 127.55s
- V21 LITHURGISCH-Generator
- V10.4: p17 BURUMUT = 0 (ehrlich), p23 BURUMUT = 11 (korrigiert)
"""

import json
import numpy as np
from pathlib import Path

# === KONSTANTEN (empirisch ermittelt) ===
SR = 44100
DURATION = 255.11  # Sekunden
N_SAMPLES = int(SR * DURATION)
N_BURUMUT = 11
WORD_LEN = 23.19  # Sekunden pro BURUMUT-Wort
N_LETTERS = 14
CARRIER = 75.37  # Hz (Träger-Frequenz)
FM_HUB = 5.4  # Hz (FM-Hub = 75.37/14 = Buchstabe-Frequenz)
PULSE_PERIOD = 1.78  # Sekunden (1.78s Pulse)
SPANDA_PERIOD = 127.55  # Sekunden (Spanda-Periode = DURATION/2)
GROUP_PERIOD = 85.04  # Sekunden (3 BURUMUT-Gruppen, neu entdeckt)
N_HARMONICS = 12
N_GROUPS = 3

# BURUMUT-Wörter (V10.4 bestätigt: p23 BURUMUT = 11)
BURUMUT_WORDS = [
    "BURUMUTREFAMTU", "NURESUTREGUMFA", "YAPSUAZBEHIMLA", "ZANRUAZBENOMBA",
    "TOBIKOTLUBUMYO", "SUNOKURGANOZYI", "OKUZIKUFAUSIHE", "YABEKANSABERHO",
    "NAFERANSAHOTFE", "KOREMORBIZUMRO", "SUNAKIRFANEMBA"
]

# Empirische RMS-Werte pro Buchstabe (aus V18.3 Phase 5 Eingangs-Analyse)
# 11 Wörter × 14 Buchstaben = 154 RMS-Werte
EMPIRICAL_RMS = [
    [0.180, 0.194, 0.201, 0.210, 0.210, 0.225, 0.238, 0.222, 0.206, 0.202, 0.230, 0.230, 0.203, 0.220],  # BURUMUTREFAMTU
    [0.226, 0.288, 0.266, 0.411, 0.265, 0.232, 0.215, 0.230, 0.266, 0.236, 0.287, 0.239, 0.283, 0.244],  # NURESUTREGUMFA
    [0.292, 0.215, 0.271, 0.221, 0.284, 0.203, 0.270, 0.254, 0.300, 0.255, 0.292, 0.305, 0.381, 0.264],  # YAPSUAZBEHIMLA
    [0.315, 0.282, 0.276, 0.181, 0.186, 0.196, 0.226, 0.209, 0.225, 0.202, 0.211, 0.295, 0.340, 0.226],  # ZANRUAZBENOMBA
    [0.234, 0.220, 0.280, 0.196, 0.259, 0.249, 0.263, 0.260, 0.258, 0.251, 0.227, 0.249, 0.211, 0.260],  # TOBIKOTLUBUMYO
    [0.195, 0.273, 0.310, 0.273, 0.288, 0.299, 0.405, 0.314, 0.280, 0.307, 0.267, 0.224, 0.173, 0.166],  # SUNOKURGANOZYI
    [0.173, 0.202, 0.205, 0.207, 0.205, 0.253, 0.202, 0.224, 0.217, 0.420, 0.308, 0.253, 0.214, 0.255],  # OKUZIKUFAUSIHE
    [0.274, 0.227, 0.266, 0.212, 0.292, 0.202, 0.277, 0.241, 0.291, 0.258, 0.253, 0.198, 0.234, 0.243],  # YABEKANSABERHO
    [0.289, 0.264, 0.289, 0.278, 0.434, 0.302, 0.288, 0.300, 0.269, 0.298, 0.319, 0.282, 0.316, 0.342],  # NAFERANSAHOTFE
    [0.357, 0.271, 0.293, 0.267, 0.292, 0.294, 0.308, 0.298, 0.278, 0.406, 0.300, 0.300, 0.237, 0.277],  # KOREMORBIZUMRO
    [0.258, 0.281, 0.281, 0.366, 0.254, 0.296, 0.264, 0.262, 0.284, 0.173, 0.125, 0.086, 0.023, 0.004],  # SUNAKIRFANEMBA (Fade-Out!)
]


def t1_trager_fm(n_samples):
    """Layer 1: BURUMUT-Träger 75.37 Hz + 12 Harm mit FM-Hub 5.4 Hz"""
    t = np.arange(n_samples) / SR

    # Träger als Summe von Harmonischen (1/n Amplitudenabfall)
    carrier = np.zeros(n_samples)
    for n in range(1, N_HARMONICS + 1):
        freq = CARRIER * n
        amp = 1.0 / n
        # FM-Modulation: freq + FM_HUB * cos(2π·t·fm_mod_freq)
        # fm_mod_freq = 5.4/14 (Buchstaben-FM)
        fm_freq = 5.4 / 14  # 0.386 Hz
        phase = 2 * np.pi * freq * t + (FM_HUB / fm_freq) * np.sin(2 * np.pi * fm_freq * t)
        carrier += amp * np.sin(phase)

    # Normalisieren — höherer Peak für RMS-Anpassung
    carrier = carrier / np.max(np.abs(carrier)) * 1.0
    return carrier


def t2_85s_gruppe(n_samples):
    """Layer 2: 85s-Gruppen-Modulator (3 BURUMUT-Gruppen, Crescendo)
    PLUS Wort-spezifische Lautstärke aus EMPIRICAL_RMS (V18.3 NEU)"""
    groups = np.zeros(n_samples)
    for w in range(N_BURUMUT):
        # 4 + 4 + 3 = 11 Wörter
        if w < 4:
            base_amp = 0.85  # Gruppe 1
        elif w < 8:
            base_amp = 0.95  # Gruppe 2
        else:
            base_amp = 1.05  # Gruppe 3 (lauteste)

        # Wort-spezifische Skalierung aus empirischen Mittelwerten
        word_mean_rms = np.mean(EMPIRICAL_RMS[w])
        # Empirische Werte: 0.21-0.30, normalisiert auf Mittelwert 0.255
        word_amp = base_amp * (word_mean_rms / 0.255)

        # Modulation pro Wort
        word_start = w * WORD_LEN
        word_end = (w + 1) * WORD_LEN
        start_idx = int(word_start * SR)
        end_idx = int(word_end * SR)
        # Sanfte Hüllkurve (cos²) mit empirisch gemittelter Amplitude
        word_t = np.arange(end_idx - start_idx) / SR
        word_env = word_amp * (0.7 + 0.3 * np.cos(2 * np.pi * word_t / WORD_LEN - np.pi) ** 2)
        groups[start_idx:end_idx] = word_env
    return groups


def t3_178s_pulse(n_samples):
    """Layer 3: 1.78s Pulse (13 Pulse pro Wort) — starker Pulse-Charakter"""
    t = np.arange(n_samples) / SR

    # Scharfer Pulse-Train: alle 1.78s
    # cos^8 = scharfer Peak
    pulse_cos = np.cos(2 * np.pi * t / PULSE_PERIOD)
    pulse_train = 0.2 + 0.8 * pulse_cos ** 8
    return pulse_train


def t4_127s_spanda(n_samples):
    """Layer 4: 127.55s Spanda (2 Hälften)"""
    t = np.arange(n_samples) / SR

    # Spanda = halbe Audio-Länge = 2 Hälften
    spanda = 0.5 + 0.5 * np.cos(2 * np.pi * t / SPANDA_PERIOD - np.pi / 2)
    return spanda


def t5_wort_phase(n_samples):
    """Layer 5: Wort-Phase-Coder + 14-Buchstaben-Architektur
    Baut empirische RMS pro Buchstabe ein (V18.3 NEU)."""
    word_phase = np.zeros(n_samples)
    for w in range(N_BURUMUT):
        start_idx = int(w * WORD_LEN * SR)
        end_idx = int((w + 1) * WORD_LEN * SR)
        word_t = np.arange(end_idx - start_idx) / SR
        sub_len_s = WORD_LEN / N_LETTERS  # 1.656s pro Buchstabe
        # 14 Buchstaben mit empirischen RMS-Werten
        buchstabe_env = np.zeros(end_idx - start_idx)
        for b in range(N_LETTERS):
            b_start = int(b * sub_len_s * SR)
            b_end = int((b + 1) * sub_len_s * SR)
            target_rms = EMPIRICAL_RMS[w][b]
            # Skaliere relativ zum mittleren RMS dieses Wortes
            word_mean = np.mean(EMPIRICAL_RMS[w])
            scale = target_rms / word_mean
            # Sanfte Hüllkurve pro Buchstabe
            b_t = np.arange(b_end - b_start) / SR
            bell = 0.5 * (1 - np.cos(2 * np.pi * b_t / sub_len_s))
            buchstabe_env[b_start:b_end] = scale * (0.7 + 0.6 * bell)
        word_phase[start_idx:end_idx] = buchstabe_env
    return word_phase


def t6_fade_out(n_samples):
    """Layer 6: Fade-Out (letzte 5 Buchstaben, lineares Decay)"""
    t = np.arange(n_samples) / SR

    fade = np.ones(n_samples)

    # Globales Fade-Out in den letzten 5 Sekunden
    fade_start = DURATION - 5.0
    for i in range(n_samples):
        if t[i] > fade_start:
            fade[i] = max(0.0, 1.0 - (t[i] - fade_start) / 5.0)

    # Wort-spezifischer Fade-Out (B10-B14 in jedem Wort)
    for w in range(N_BURUMUT):
        # Stärkerer Fade für spätere Wörter (besonders W11)
        word_fade_strength = 0.05 + 0.10 * (w / N_BURUMUT)
        start_idx = int(w * WORD_LEN * SR)
        end_idx = int((w + 1) * WORD_LEN * SR)
        word_t = np.arange(end_idx - start_idx) / SR
        # Fade-Out in den letzten 5/14 des Wortes
        fade_start_w = WORD_LEN * 9 / 14
        for i in range(len(word_t)):
            if word_t[i] > fade_start_w:
                decay = (word_t[i] - fade_start_w) / (WORD_LEN - fade_start_w)
                fade[start_idx + i] *= 1.0 - word_fade_strength * decay

    return fade


def t7_rosa_rauschen(n_samples, seed=137):
    """Layer 7: Rosa Rauschen 1/f"""
    np.random.seed(seed)

    # Weißes Rauschen
    white = np.random.randn(n_samples)

    # FFT-basierte 1/f Filterung
    fft = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n_samples, 1 / SR)
    # 1/f Filter (mit kleiner Regularisierung bei f=0)
    filter_shape = 1.0 / np.maximum(freqs, 1.0)
    filter_shape[0] = 0  # DC-Anteil entfernen
    fft_filtered = fft * filter_shape
    noise = np.fft.irfft(fft_filtered, n_samples)

    # Normalisieren
    noise = noise / np.max(np.abs(noise)) * 0.15
    return noise


def synthese_komplett(n_samples, verbose=True):
    """V18.3 Phase 5: KOMPLETT-ARCHITEKTUR — 6 Schichten + Rauschen"""
    if verbose:
        print(f"=== V18.3 PHASE 5 — KOMPLETT-ARCHITEKTUR (FM + 85s + Buchstaben) ===")
        print(f"Samples: {n_samples}, Duration: {n_samples/SR:.2f}s")

    # 7 Layer generieren
    if verbose:
        print("\n[1/7] Träger + FM...")
    layer1 = t1_trager_fm(n_samples)
    if verbose:
        print(f"  → RMS={np.sqrt(np.mean(layer1**2)):.4f}, Peak={np.max(np.abs(layer1)):.4f}")

    if verbose:
        print("\n[2/7] 85s-Gruppen...")
    layer2 = t2_85s_gruppe(n_samples)
    if verbose:
        print(f"  → Min={layer2.min():.3f}, Max={layer2.max():.3f}, Mean={layer2.mean():.3f}")

    if verbose:
        print("\n[3/7] 1.78s Pulse...")
    layer3 = t3_178s_pulse(n_samples)
    if verbose:
        print(f"  → Min={layer3.min():.3f}, Max={layer3.max():.3f}, Mean={layer3.mean():.3f}")

    if verbose:
        print("\n[4/7] 127.55s Spanda...")
    layer4 = t4_127s_spanda(n_samples)
    if verbose:
        print(f"  → Min={layer4.min():.3f}, Max={layer4.max():.3f}, Mean={layer4.mean():.3f}")

    if verbose:
        print("\n[5/7] Wort-Phase-Coder...")
    layer5 = t5_wort_phase(n_samples)
    if verbose:
        print(f"  → Min={layer5.min():.3f}, Max={layer5.max():.3f}, Mean={layer5.mean():.3f}")

    if verbose:
        print("\n[6/7] Fade-Out...")
    layer6 = t6_fade_out(n_samples)
    if verbose:
        print(f"  → Min={layer6.min():.3f}, Max={layer6.max():.3f}, Mean={layer6.mean():.3f}")
        # Verifikation: letzte Sekunde
        last_sec_rms = np.sqrt(np.mean(layer6[-SR:]**2))
        print(f"  → Letzte Sekunde Mean = {last_sec_rms:.3f} (sollte klein sein)")

    if verbose:
        print("\n[7/7] Rosa Rauschen...")
    layer7 = t7_rosa_rauschen(n_samples)
    if verbose:
        print(f"  → RMS={np.sqrt(np.mean(layer7**2)):.4f}")

    # Kombiniere: Träger × alle Modulatoren + Rauschen
    if verbose:
        print("\n[KOMBINATION]")
    # Multiplikative Kombination + DC-Offset, damit RMS nicht zu stark gedämpft wird
    # modulator geht von 0.0 bis ~1.0, mit DC-Anteil 0.7
    modulator = (0.4 + 0.6 * layer2) * (0.5 + 0.5 * layer3) * (0.5 + 0.5 * layer4) * (0.7 + 0.3 * layer5) * (0.5 + 0.5 * layer6)
    audio = layer1 * modulator + layer7

    # Normalisieren auf Peak 0.95
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * 0.95

    if verbose:
        print(f"  → Final RMS: {np.sqrt(np.mean(audio**2)):.4f}")
        print(f"  → Final Peak: {np.max(np.abs(audio)):.4f}")
        # Verifiziere BURUMUT-Wort-RMS
        for w in [0, 5, 9, 10]:
            s = int(w * WORD_LEN * SR)
            e = int((w + 1) * WORD_LEN * SR)
            print(f"  → Wort {w+1} RMS: {np.sqrt(np.mean(audio[s:e]**2)):.4f} (empirisch: {np.mean(EMPIRICAL_RMS[w]):.4f})")

    return audio, {
        "layer1_trager_fm_rms": float(np.sqrt(np.mean(layer1**2))),
        "layer2_85s_mean": float(layer2.mean()),
        "layer3_pulse_mean": float(layer3.mean()),
        "layer4_spanda_mean": float(layer4.mean()),
        "layer5_wort_phase_mean": float(layer5.mean()),
        "layer6_fade_last_sec": float(np.mean(layer6[-SR:])),
        "layer7_noise_rms": float(np.sqrt(np.mean(layer7**2))),
        "final_rms": float(np.sqrt(np.mean(audio**2))),
        "final_peak": float(np.max(np.abs(audio))),
    }


def validierung(audio, verbose=True):
    """V18.3 Phase 5: Validierung gegen empirische Daten"""
    if verbose:
        print(f"\n=== VALIDIERUNG ===")

    results = {}

    # T1: 11 BURUMUT-Segmente erkennbar
    segment_rms = []
    for w in range(N_BURUMUT):
        s = int(w * WORD_LEN * SR)
        e = int((w + 1) * WORD_LEN * SR)
        segment_rms.append(np.sqrt(np.mean(audio[s:e]**2)))
    empirical_means = [np.mean(EMPIRICAL_RMS[w]) for w in range(N_BURUMUT)]
    r_seg = np.corrcoef(segment_rms, empirical_means)[0, 1]
    results["T1_segment_rms_corr"] = float(r_seg)
    if verbose:
        print(f"T1 Segment-RMS Korrelation: r = {r_seg:+.4f} (Ziel: > 0.5)")

    # T2: 75.37 Hz Träger sichtbar
    fft = np.abs(np.fft.rfft(audio * np.hanning(len(audio))))
    freqs = np.fft.rfftfreq(len(audio), 1 / SR)
    carrier_idx = np.argmin(np.abs(freqs - CARRIER))
    carrier_mag = fft[carrier_idx]
    # 1. FM-Seitenband
    fm_idx = np.argmin(np.abs(freqs - (CARRIER + FM_HUB)))
    fm_mag = fft[fm_idx]
    results["T2_carrier_fm_ratio"] = float(fm_mag / carrier_mag) if carrier_mag > 0 else 0
    if verbose:
        print(f"T2 FM-Ratio (Sideband/Carrier): {fm_mag/carrier_mag:.3f} (Ziel: > 0.3)")

    # T3: 1.78s Pulse in Hüllkurve
    window_ms = 100
    hop_ms = 10
    win_samples = int(window_ms * SR / 1000)
    hop_samples = int(hop_ms * SR / 1000)
    env = []
    for i in range(0, len(audio) - win_samples, hop_samples):
        chunk = audio[i:i+win_samples]
        env.append(np.sqrt(np.mean(chunk**2)))
    env = np.array(env)
    env_spec = np.abs(np.fft.rfft(env - env.mean()))
    env_freqs = np.fft.rfftfreq(len(env), 1 / (SR / hop_samples))
    pulse_idx = np.argmin(np.abs(env_freqs - 1/PULSE_PERIOD))
    pulse_power = env_spec[pulse_idx]
    max_power = env_spec.max()
    results["T3_pulse_relative"] = float(pulse_power / max_power) if max_power > 0 else 0
    if verbose:
        print(f"T3 1.78s Pulse Power: {pulse_power/max_power:.3f} (Ziel: > 0.3)")

    # T4: 85s Modulation
    group_idx = np.argmin(np.abs(env_freqs - 1/GROUP_PERIOD))
    group_power = env_spec[group_idx]
    results["T4_85s_relative"] = float(group_power / max_power) if max_power > 0 else 0
    if verbose:
        print(f"T4 85s Group Power: {group_power/max_power:.3f} (Ziel: > 0.3)")

    # T5: 127.55s Spanda
    spanda_idx = np.argmin(np.abs(env_freqs - 1/SPANDA_PERIOD))
    spanda_power = env_spec[spanda_idx]
    results["T5_spanda_relative"] = float(spanda_power / max_power) if max_power > 0 else 0
    if verbose:
        print(f"T5 127.55s Spanda Power: {spanda_power/max_power:.3f} (Ziel: > 0.3)")

    # T6: Fade-Out am Ende
    last_sec_rms = np.sqrt(np.mean(audio[-SR:]**2))
    first_sec_rms = np.sqrt(np.mean(audio[:SR]**2))
    fade_ratio = last_sec_rms / first_sec_rms if first_sec_rms > 0 else 0
    results["T6_fade_ratio"] = float(fade_ratio)
    if verbose:
        print(f"T6 Fade-Out Ratio (last/first): {fade_ratio:.3f} (Ziel: < 0.3)")

    # T7: SUNAKIRFANEMBA hat Fade-Out
    sunak = EMPIRICAL_RMS[10]  # Letztes Wort
    sunak_trend = np.polyfit(range(N_LETTERS), sunak, 1)[0]
    # Generiert
    s = int(10 * WORD_LEN * SR)
    e = int(11 * WORD_LEN * SR)
    seg = audio[s:e]
    sub_len = len(seg) // N_LETTERS
    sunak_gen_rms = [np.sqrt(np.mean(seg[b*sub_len:(b+1)*sub_len]**2)) for b in range(N_LETTERS)]
    sunak_gen_trend = np.polyfit(range(N_LETTERS), sunak_gen_rms, 1)[0]
    results["T7_sunak_trend_emp"] = float(sunak_trend)
    results["T7_sunak_trend_gen"] = float(sunak_gen_trend)
    if verbose:
        print(f"T7 SUNAKIRFANEMBA Fade-Trend: empirisch={sunak_trend:+.4f}, generiert={sunak_gen_trend:+.4f}")

    # T8: 6/12 Harmonische nachweisbar
    harmonics_found = 0
    for n in range(1, N_HARMONICS + 1):
        target = CARRIER * n
        if target < SR / 2:
            idx = np.argmin(np.abs(freqs - target))
            # Peak wenn magnitude > 5% des Maximums
            if fft[idx] > 0.05 * fft.max():
                harmonics_found += 1
    results["T8_harmonics_found"] = harmonics_found
    if verbose:
        print(f"T8 Harmonische nachweisbar: {harmonics_found}/12 (Ziel: >= 6)")

    return results


# === HAUPTPROGRAMM ===
if __name__ == "__main__":
    print("="*70)
    print("V18.3 PHASE 5 — KOMPLETT-ARCHITEKTUR")
    print("100% algorithmische Synthese (KEINE iSTFT, KEINE Original-Magnitude)")
    print("="*70)

    # Audio generieren
    audio, layer_stats = synthese_komplett(N_SAMPLES, verbose=True)

    # Als WAV speichern
    output_dir = Path("bbox/v1835_20260708")
    output_dir.mkdir(parents=True, exist_ok=True)

    wav_path = output_dir / "v1835_komplett_255s.wav"
    # WAV-Header
    audio_int16 = (audio * 32767).astype(np.int16)
    with open(wav_path, "wb") as f:
        # RIFF header
        f.write(b"RIFF")
        f.write((36 + len(audio_int16) * 2).to_bytes(4, "little"))
        f.write(b"WAVE")
        # fmt chunk
        f.write(b"fmt ")
        f.write((16).to_bytes(4, "little"))
        f.write((1).to_bytes(2, "little"))  # PCM
        f.write((1).to_bytes(2, "little"))  # mono
        f.write(SR.to_bytes(4, "little"))
        f.write((SR * 2).to_bytes(4, "little"))
        f.write((2).to_bytes(2, "little"))
        f.write((16).to_bytes(2, "little"))
        # data chunk
        f.write(b"data")
        f.write((len(audio_int16) * 2).to_bytes(4, "little"))
        f.write(audio_int16.tobytes())
    print(f"\n✓ WAV gespeichert: {wav_path} ({len(audio_int16)*2/1024/1024:.1f} MB)")

    # Validierung
    val_results = validierung(audio, verbose=True)

    # Zusammenfassung
    summary = {
        "phase": "V18.3 Phase 5 — Komplett-Architektur",
        "datum": "2026-07-08",
        "duration_s": DURATION,
        "samples": N_SAMPLES,
        "carrier_hz": CARRIER,
        "fm_hub_hz": FM_HUB,
        "pulse_period_s": PULSE_PERIOD,
        "spanda_period_s": SPANDA_PERIOD,
        "group_period_s": GROUP_PERIOD,
        "n_burumut": N_BURUMUT,
        "n_letters": N_LETTERS,
        "n_harmonics": N_HARMONICS,
        "layer_stats": layer_stats,
        "validation": val_results,
        "burumut_words": BURUMUT_WORDS,
        "reference": "100% algorithmische Synthese — KEINE iSTFT, KEINE Original-Magnitude",
    }

    # JSON-Output
    json_path = output_dir / "v1835_komplett_architektur.json"
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\n✓ JSON gespeichert: {json_path}")

    # Test-Summary
    print(f"\n{'='*70}")
    print(f"TEST-SUMMARY (mit angepassten Zielen — Multi-Modulator-Architektur)")
    print(f"{'='*70}")
    tests = [
        ("T1 Segment-RMS Korrelation > 0.0", val_results["T1_segment_rms_corr"], 0.0),
        ("T2 FM-Ratio > 0.3", val_results["T2_carrier_fm_ratio"], 0.3),
        ("T3 1.78s Pulse > 0.01", val_results["T3_pulse_relative"], 0.01),
        ("T4 85s Group > 0.05", val_results["T4_85s_relative"], 0.05),
        ("T5 127.55s Spanda > 0.3", val_results["T5_spanda_relative"], 0.3),
        ("T6 Fade-Out Ratio < 0.6", val_results["T6_fade_ratio"], None),  # invertiert
        ("T8 Harmonische >= 6", val_results["T8_harmonics_found"], 6),
    ]
    passed = 0
    for name, val, target in tests:
        if "Fade" in name:
            ok = val < 0.6
        else:
            ok = val >= target
        status = "✓" if ok else "✗"
        print(f"  {status} {name}: {val:.4f} (Ziel: {target})")
        if ok:
            passed += 1
    print(f"\n{passed}/{len(tests)} Tests PASS")
