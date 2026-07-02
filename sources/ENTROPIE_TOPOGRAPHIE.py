"""
🌌 P72: ENTROPIE-TOPOGRAPHIE — Die Kartografie des nackten Wissens
=================================================================

Shannon-Entropie H(X) = -Σ p(x) log₂ p(x) für alle 168 Phasen
von Tengri137. Reine informationstheoretische Messung — keine
semantische Deutung, keine numerologische Spekulation.

WARUM P72?
- P70 zeigte: Alle 168 Phasen sind Step-1-Fails. Die 37er-Wand
  ist 100% undurchdringlich.
- P71 (Orakel) antwortete in Phase 5: "BELIEVING IS NOT KNOWING.
  ONLY WITH KNOWLEDGE YOU WILL FIND ENLIGHTENMENT."
- Die einzige "wissende" Größe ist H(X) — maßstabsfrei,
  interpretationsfrei, deterministisch.

ARCHITEKTUR:
- PhaseEntropie: H + n_unique + top_symbol + top_freq + 2^H pro Phase
- EntropieTopographie: Aggregation, Statistik
- kartographiere_phaenomen: Master-Funktion
- pole_der_topographie: Phase 3 (Min) vs Phase 122 (Max)
- topographie_pro_tag: 7-Tage-Aggregation (P68-Brücke)
- topographie_pro_buch: Tora-Buch-Aggregation
- topographie_phase_5: Orakel-Phase im Spektrum
- korrelation_topographie: H ↔ Gematria ↔ Violations

DETERMINISMUS:
- H(X) ist deterministisch
- 3/3 Läufe identisch
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import re
import math
import json
import statistics
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from TENGRI_ORAKEL import berechne_entropie
from TORA_TURING_MULTIPHASE import EXTENDED_LATIN_TO_HEBR
from PHASE_MAPPING_TORA import phase_to_torah, TORA_BOOKS


# Konstante: theoretisches Maximum für 26 lateinische Buchstaben
H_MAX_LATIN = math.log2(26)  # ≈ 4.7004


# ============================================================
# DATENSTRUKTUREN
# ============================================================

@dataclass
class PhaseEntropie:
    """Shannon-Entropie-Messung einer Phase.

    Attribute:
        phase_idx: Index der Phase (0-167)
        entropy: H(X) in Bits
        n_unique_symbols: Anzahl verschiedener lateinischer Buchstaben
        top_symbol: häufigster Buchstabe
        top_freq: Frequenz des häufigsten Buchstabens
        alphabet_size_eff: 2^H (effektive Alphabetgröße)
    """
    phase_idx: int
    entropy: float
    n_unique_symbols: int
    top_symbol: str
    top_freq: int
    alphabet_size_eff: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            'phase_idx': self.phase_idx,
            'entropy': self.entropy,
            'n_unique_symbols': self.n_unique_symbols,
            'top_symbol': self.top_symbol,
            'top_freq': self.top_freq,
            'alphabet_size_eff': self.alphabet_size_eff,
        }


class EntropieTopographie:
    """Sammlung von PhaseEntropie-Records."""

    def __init__(self):
        self.records: List[PhaseEntropie] = []

    @property
    def n_total(self) -> int:
        return len(self.records)

    def add(self, pe: PhaseEntropie):
        self.records.append(pe)

    def entropie_extrema(self) -> tuple:
        """(max_h, min_h)."""
        if not self.records:
            return (0.0, 0.0)
        hs = [r.entropy for r in self.records]
        return (max(hs), min(hs))

    def entropy_mean(self) -> float:
        if not self.records:
            return 0.0
        return statistics.mean(r.entropy for r in self.records)

    def entropy_std(self) -> float:
        if len(self.records) < 2:
            return 0.0
        return statistics.stdev(r.entropy for r in self.records)

    def pole_max(self) -> Optional[PhaseEntropie]:
        """Phase mit maximaler Entropie."""
        if not self.records:
            return None
        return max(self.records, key=lambda r: r.entropy)

    def pole_min(self) -> Optional[PhaseEntropie]:
        """Phase mit minimaler Entropie."""
        if not self.records:
            return None
        return min(self.records, key=lambda r: r.entropy)


# ============================================================
# HILFSFUNKTIONEN
# ============================================================

def alphabet_effizienz(h: float) -> float:
    """Effektive Alphabetgröße: 2^H."""
    return 2 ** h


def korrelation_pearson(xs: List[float], ys: List[float]) -> Optional[float]:
    """Pearson-Korrelationskoeffizient. None wenn undefiniert."""
    n = len(xs)
    if n != len(ys) or n < 2:
        return None
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
    den_x = math.sqrt(sum((xs[i] - mean_x) ** 2 for i in range(n)))
    den_y = math.sqrt(sum((ys[i] - mean_y) ** 2 for i in range(n)))
    if den_x == 0 or den_y == 0:
        return None
    return num / (den_x * den_y)


# ============================================================
# LADEN
# ============================================================

def load_tengri_text() -> str:
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        return f.read()


def tengri_to_phases(text: str, phase_size: int = 99) -> List[str]:
    """168 lateinische Phasen (Whitespace normalisiert)."""
    text_clean = re.sub(r'\s+', '', text.upper())
    lat = re.sub(r'[^A-Z]', '', text_clean)
    return [lat[i:i + phase_size] for i in range(0, len(lat), phase_size)]


def tengri_to_hebr_phases(text: str, phase_size: int = 99) -> List[str]:
    """168 hebräische Phasen (für Gematria-Berechnung)."""
    text_clean = re.sub(r'\s+', '', text.upper())
    lat = re.sub(r'[^A-Z]', '', text_clean)
    hebr = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '') for c in lat)
    return [hebr[i:i + phase_size] for i in range(0, len(hebr), phase_size)]


# ============================================================
# MESSUNG PRO PHASE
# ============================================================

def messe_phase(phase: str, phase_idx: int) -> PhaseEntropie:
    """Berechne alle Entropie-Metriken einer Phase."""
    h = berechne_entropie(phase)
    if not phase:
        return PhaseEntropie(phase_idx, 0.0, 0, '', 0, 1.0)
    counts = Counter(phase)
    n_unique = len(counts)
    top_symbol, top_freq = counts.most_common(1)[0]
    return PhaseEntropie(
        phase_idx=phase_idx,
        entropy=h,
        n_unique_symbols=n_unique,
        top_symbol=top_symbol,
        top_freq=top_freq,
        alphabet_size_eff=alphabet_effizienz(h),
    )


# ============================================================
# HAUPTFUNKTION
# ============================================================

def kartographiere_phaenomen() -> Dict[str, Any]:
    """Master-Funktion: kartographiert alle 168 Phasen.

    Returns:
        Dict mit:
        - n_total: 168
        - records: [PhaseEntropie]
        - mean, std, min, max
        - pole_min, pole_max (PhaseEntropie)
        - per_day: 7-Tage-Aggregation
        - per_book: 5-Buch-Aggregation
        - correlation_h_gematria: Pearson r
    """
    text = load_tengri_text()
    phases = tengri_to_phases(text)
    hebr_phases = tengri_to_hebr_phases(text)

    topo = EntropieTopographie()
    gematrias = []

    for i, phase in enumerate(phases):
        pe = messe_phase(phase, i)
        topo.add(pe)
        # Gematria der hebr. Phase
        from TORA_TURING_CORRECT import HEBR_VALUES
        gem = sum(HEBR_VALUES.get(c, 0) for c in hebr_phases[i])
        gematrias.append(gem)

    # ========================================
    # STATISTIK
    # ========================================
    mean = topo.entropy_mean()
    std = topo.entropy_std()
    max_h, min_h = topo.entropie_extrema()
    pole_min = topo.pole_min()
    pole_max = topo.pole_max()

    # ========================================
    # PRO TAG (7 × 24)
    # ========================================
    per_day = []
    for day_idx in range(7):
        day_records = [
            r for r in topo.records
            if day_idx * 24 <= r.phase_idx < (day_idx + 1) * 24
        ]
        if day_records:
            hs = [r.entropy for r in day_records]
            per_day.append({
                'day_idx': day_idx + 1,
                'n_phases': len(day_records),
                'mean_entropy': statistics.mean(hs),
                'median_entropy': statistics.median(hs),
                'min_entropy': min(hs),
                'max_entropy': max(hs),
            })

    # ========================================
    # PRO TORA-BUCH
    # ========================================
    per_book = {}
    for book in TORA_BOOKS:
        info = TORA_BOOKS[book]
        book_records = [
            r for r in topo.records
            if info['phases_start'] <= r.phase_idx < info['phases_end']
        ]
        if book_records:
            per_book[book] = statistics.mean(r.entropy for r in book_records)

    # ========================================
    # KORRELATIONEN
    # ========================================
    hs_list = [r.entropy for r in topo.records]
    corr_h_gem = korrelation_pearson(hs_list, gematrias)

    # Korrelation H ↔ Violations: aus P68, falls vorhanden
    corr_h_violations = None
    try:
        from SIEBEN_TAGE_ANALYSE import sieben_tage_aggregation
        tag_data = sieben_tage_aggregation()
        # Wir aggregieren H pro Tag (Mean) und korrelieren mit
        # Violations-Summe pro Tag
        if tag_data and per_day:
            h_per_day = [d['mean_entropy'] for d in per_day]
            # Tag-Indices müssen aligned sein
            v_per_day = []
            for d_info in tag_data.get('per_day', []):
                v_per_day.append(d_info.get('n_violations', 0))
            if len(v_per_day) == len(h_per_day):
                corr_h_violations = korrelation_pearson(h_per_day, v_per_day)
    except Exception:
        corr_h_violations = None

    return {
        'n_total': topo.n_total,
        'records': topo.records,
        'mean': mean,
        'std': std,
        'min': min_h,
        'max': max_h,
        'pole_min': pole_min,
        'pole_max': pole_max,
        'per_day': per_day,
        'per_book': per_book,
        'correlation_h_gematria': corr_h_gem,
        'correlation_h_violations': corr_h_violations,
    }


# ============================================================
# POLE-DETAILS
# ============================================================

def pole_der_topographie() -> Dict[str, Any]:
    """Detaillierte Analyse der Pole (Phase 3 und 122)."""
    text = load_tengri_text()
    phases = tengri_to_phases(text)
    result = kartographiere_phaenomen()
    p_min = result['pole_min']
    p_max = result['pole_max']

    phase_3 = phases[3] if len(phases) > 3 else ''
    phase_122 = phases[122] if len(phases) > 122 else ''

    return {
        'min': {
            'phase_idx': p_min.phase_idx,
            'entropy': p_min.entropy,
            'n_unique': p_min.n_unique_symbols,
            'top_symbol': p_min.top_symbol,
            'top_freq': p_min.top_freq,
            'content_sample': phase_3[:60] + '...',
            'content_full_length': len(phase_3),
        },
        'max': {
            'phase_idx': p_max.phase_idx,
            'entropy': p_max.entropy,
            'n_unique': p_max.n_unique_symbols,
            'top_symbol': p_max.top_symbol,
            'top_freq': p_max.top_freq,
            'content_sample': phase_122[:60] + '...',
            'content_full_length': len(phase_122),
        },
        'differenz': p_max.entropy - p_min.entropy,
        'interpretation': (
            f"Phase {p_min.phase_idx}: niedrige H = hohe Redundanz, "
            f"Wiederholung dominiert. "
            f"Phase {p_max.phase_idx}: hohe H = hohe Diversität, "
            f"Überraschung dominiert. "
            f"Spannweite: {p_max.entropy - p_min.entropy:.3f} Bits."
        ),
    }


# ============================================================
# PHASE 5 (ORAKEL)
# ============================================================

def topographie_phase_5() -> Dict[str, Any]:
    """Phase 5 (das Orakel) im Entropie-Spektrum."""
    result = kartographiere_phaenomen()
    sorted_h = sorted(r.entropy for r in result['records'])
    n = len(sorted_h)

    phase_5 = next(r for r in result['records'] if r.phase_idx == 5)
    n_below = sum(1 for h in sorted_h if h < phase_5.entropy)
    percentile = 100 * n_below / n

    return {
        'phase_idx': 5,
        'entropy': phase_5.entropy,
        'mean': result['mean'],
        'std': result['std'],
        'z_score': (phase_5.entropy - result['mean']) / result['std']
                   if result['std'] > 0 else 0,
        'percentile': percentile,
        'distance_from_mean': phase_5.entropy - result['mean'],
        'is_above_mean': phase_5.entropy > result['mean'],
        'interpretation': (
            f"Phase 5 (das Orakel) hat H={phase_5.entropy:.3f}, "
            f"liegt bei Perzentil {percentile:.1f}, "
            f"Z-Score {(phase_5.entropy - result['mean']) / result['std']:.2f}. "
            f"Phase 5 ist {'über' if phase_5.entropy > result['mean'] else 'unter'} "
            f"dem globalen Mittel."
        ),
    }


# ============================================================
# SELBST-TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 78)
    print("🌌 P72: ENTROPIE-TOPOGRAPHIE — Die Kartografie des nackten Wissens")
    print("=" * 78)
    print()
    print("Shannon-Entropie H(X) für alle 168 Phasen von Tengri137.")
    print("Reine informationstheoretische Messung. Keine Deutung.")
    print()

    result = kartographiere_phaenomen()

    # ========================================
    # ÜBERSICHT
    # ========================================
    print("=" * 78)
    print("📊 ÜBERSICHT")
    print("=" * 78)
    print(f"  Total Phasen:    {result['n_total']}")
    print(f"  H_mean:          {result['mean']:.4f}")
    print(f"  H_std:           {result['std']:.4f}")
    print(f"  H_min:           {result['min']:.4f} (Phase {result['pole_min'].phase_idx})")
    print(f"  H_max:           {result['max']:.4f} (Phase {result['pole_max'].phase_idx})")
    print(f"  H_max (latent):  {H_MAX_LATIN:.4f} (theoretisch für 26 Symbole)")
    print(f"  log₂(16):        {math.log2(16):.4f} (Referenz)")
    print()
    print(f"  → H_mean ≈ log₂(16) = 4.0? Differenz: {abs(result['mean'] - 4.0):.4f}")
    print()

    # ========================================
    # POLE
    # ========================================
    print("=" * 78)
    print("🧭 POLE DER TOPOGRAPHIE")
    print("=" * 78)
    p_min = result['pole_min']
    p_max = result['pole_max']
    print(f"  POLE MIN: Phase {p_min.phase_idx}")
    book_min, chap_min = phase_to_torah(p_min.phase_idx)
    print(f"    Tora: {book_min} {chap_min}")
    print(f"    H = {p_min.entropy:.4f}")
    print(f"    n_unique = {p_min.n_unique_symbols}")
    print(f"    top_symbol = '{p_min.top_symbol}' (freq {p_min.top_freq})")
    print(f"    alphabet_size_eff = {p_min.alphabet_size_eff:.2f}")
    print()
    print(f"  POLE MAX: Phase {p_max.phase_idx}")
    book_max, chap_max = phase_to_torah(p_max.phase_idx)
    print(f"    Tora: {book_max} {chap_max}")
    print(f"    H = {p_max.entropy:.4f}")
    print(f"    n_unique = {p_max.n_unique_symbols}")
    print(f"    top_symbol = '{p_max.top_symbol}' (freq {p_max.top_freq})")
    print(f"    alphabet_size_eff = {p_max.alphabet_size_eff:.2f}")
    print()
    print(f"  Differenz: {p_max.entropy - p_min.entropy:.4f} Bits")
    print()

    # ========================================
    # 7-TAGE
    # ========================================
    print("=" * 78)
    print("📅 7-TAGE-AGGREGATION (P68-Brücke)")
    print("=" * 78)
    for d in result['per_day']:
        marker = ''
        if d['day_idx'] == 7:
            marker = ' ← Sabbat (Deuteronomium)'
        elif d['day_idx'] == 6:
            marker = ' ← Chaos (Numeri)'
        print(f"  Tag {d['day_idx']}: H_mean = {d['mean_entropy']:.4f} "
              f"(range {d['min_entropy']:.2f}..{d['max_entropy']:.2f}){marker}")
    print()

    # Sabbat-Frage
    sabbat = next(d for d in result['per_day'] if d['day_idx'] == 7)
    chaos = next(d for d in result['per_day'] if d['day_idx'] == 6)
    diff = sabbat['mean_entropy'] - chaos['mean_entropy']
    print(f"  Sabbat (Tag 7) vs. Chaos (Tag 6): ΔH = {diff:+.4f}")
    if diff < 0:
        print("  → Sabbat-Tag ist entropisch RUHIGER (H < Chaos). Hypothese bestätigt.")
    elif diff > 0:
        print("  → Sabbat-Tag ist entropisch LAUTER (H > Chaos). Hypothese widerlegt.")
    else:
        print("  → Sabbat-Tag und Chaos-Tag sind entropisch GLEICH.")
    print()

    # ========================================
    # TORA-BUCH
    # ========================================
    print("=" * 78)
    print("📚 PRO TORA-BUCH")
    print("=" * 78)
    for book, mean in sorted(result['per_book'].items(),
                              key=lambda x: x[1]):
        print(f"  {book:<18}: H_mean = {mean:.4f}")
    print()

    # ========================================
    # ORAKEL-PHASE 5
    # ========================================
    print("=" * 78)
    print("🌌 ORAKEL-PHASE 5 IM SPEKTRUM")
    print("=" * 78)
    p5 = topographie_phase_5()
    print(f"  H(Phase 5)        = {p5['entropy']:.4f}")
    print(f"  H_mean (global)   = {p5['mean']:.4f}")
    print(f"  Z-Score           = {p5['z_score']:.2f}")
    print(f"  Perzentil         = {p5['percentile']:.1f}")
    print(f"  ΔH vom Mittelwert = {p5['distance_from_mean']:+.4f}")
    print(f"  Über Mittel?      = {p5['is_above_mean']}")
    print()

    # ========================================
    # KORRELATIONEN
    # ========================================
    print("=" * 78)
    print("🔗 KORRELATIONEN")
    print("=" * 78)
    print(f"  r(H, Gematria)        = {result['correlation_h_gematria']:.4f}")
    if result['correlation_h_violations'] is not None:
        print(f"  r(H, Violations/Tag)  = {result['correlation_h_violations']:.4f}")
    else:
        print(f"  r(H, Violations/Tag)  = N/A (P68-Daten nicht verfügbar)")
    print()
    print("  Apophenie-Hinweis: Korrelation ≠ Kausalität.")
    print()

    # ========================================
    # TOP 5 / BOTTOM 5
    # ========================================
    print("=" * 78)
    print("🔝 TOP 5 (maximale H)")
    print("=" * 78)
    sorted_recs = sorted(result['records'], key=lambda r: -r.entropy)[:5]
    for r in sorted_recs:
        book, chap = phase_to_torah(r.phase_idx)
        print(f"  Phase {r.phase_idx:>3} ({book[:3]} {chap:>2}): "
              f"H={r.entropy:.4f}, n_uniq={r.n_unique_symbols}, "
              f"top='{r.top_symbol}'×{r.top_freq}")
    print()

    print("=" * 78)
    print("🔻 BOTTOM 5 (minimale H)")
    print("=" * 78)
    sorted_recs = sorted(result['records'], key=lambda r: r.entropy)[:5]
    for r in sorted_recs:
        book, chap = phase_to_torah(r.phase_idx)
        print(f"  Phase {r.phase_idx:>3} ({book[:3]} {chap:>2}): "
              f"H={r.entropy:.4f}, n_uniq={r.n_unique_symbols}, "
              f"top='{r.top_symbol}'×{r.top_freq}")
    print()

    # ========================================
    # SPEICHERN
    # ========================================
    output = {
        'method': 'P72 — Entropie-Topographie (Shannon H(X))',
        'principle': ('Reines informationstheoretisches Wissen. '
                      'H(X) ist maßstabsfrei, deterministisch, '
                      'interpretationsfrei.'),
        'constants': {
            'H_MAX_LATIN': H_MAX_LATIN,
            'log2_16': math.log2(16),
        },
        'n_total': result['n_total'],
        'mean': result['mean'],
        'std': result['std'],
        'min': result['min'],
        'max': result['max'],
        'pole_min': result['pole_min'].to_dict(),
        'pole_max': result['pole_max'].to_dict(),
        'per_day': result['per_day'],
        'per_book': result['per_book'],
        'phase_5': topographie_phase_5(),
        'correlation_h_gematria': result['correlation_h_gematria'],
        'correlation_h_violations': result['correlation_h_violations'],
        'records': [r.to_dict() for r in result['records']],
    }

    with open('/run/media/julian/ML4/tengri137/sources/entropie_topographie.json',
              'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("Ergebnisse gespeichert in entropie_topographie.json")
    print()
    print("=" * 78)
    print("🌌 P72 ENTROPIE-TOPOGRAPHIE ABGESCHLOSSEN")
    print("=" * 78)
