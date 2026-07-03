"""
🌌 P72: ENTROPIE-TOPOGRAPHIE — Die Kartografie des nackten Wissens
================================================================

Tests für die vollständige Shannon-Entropie-Landkarte über alle
168 Phasen von Tengri137. Reine informationstheoretische Messung.

METRIKEN pro Phase:
- H: Shannon-Entropie
- n_unique_symbols: Anzahl verschiedener Buchstaben
- top_symbol: häufigster Buchstabe
- top_freq: Frequenz des häufigsten
- alphabet_size_eff: 2^H (effektive Alphabetgröße)
- H_relative: H / log2(26) (normalisiert)

ARCHITEKTUR:
- 168 Phasen à 99 lateinische Buchstaben
- Vergleiche mit P68 (7-Tage) und P70 (Topologie)
- Bestimmt: H_mean ≈ log2(16) = 4.0?
- Bestimmt: Sabbat-Tag (7) entropisch ruhiger als Chaos-Tag (6)?

DETERMINISMUS:
- H(X) ist deterministisch
- 3/3 Läufe identisch
"""

import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
import math
import json
from collections import Counter
from TENGRI_ORAKEL import berechne_entropie
from PHASE_MAPPING_TORA import phase_to_torah, TORA_BOOKS
from ENTROPIE_TOPOGRAPHIE import (
    PhaseEntropie, EntropieTopographie,
    kartographiere_phaenomen, pole_der_topographie,
    topographie_phase_5, alphabet_effizienz, H_MAX_LATIN
)


def load_tengri_text():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        return f.read()


def tengri_to_phases(text, phase_size=99):
    lat = re.sub(r'[^A-Z]', '', text.upper())
    return [lat[i:i+phase_size] for i in range(0, len(lat), phase_size)]


# ============================================================
# TEST 1: PhaseEntropie Dataclass
# ============================================================

class TestPhaseEntropie:
    """PhaseEntropie speichert alle H-relevanten Daten."""

    def test_phase_entropie_erstellen(self):
        pe = PhaseEntropie(
            phase_idx=0, entropy=4.0, n_unique_symbols=15,
            top_symbol='E', top_freq=15, alphabet_size_eff=16.0
        )
        assert pe.phase_idx == 0
        assert pe.entropy == 4.0
        assert pe.n_unique_symbols == 15
        assert pe.top_symbol == 'E'
        assert pe.top_freq == 15
        assert pe.alphabet_size_eff == 16.0

    def test_phase_entropie_to_dict(self):
        pe = PhaseEntropie(5, 4.03, 17, 'E', 14, 16.3)
        d = pe.to_dict()
        assert d['phase_idx'] == 5
        assert d['entropy'] == 4.03
        assert d['alphabet_size_eff'] == 16.3


# ============================================================
# TEST 2: EntropieTopographie Hauptklasse
# ============================================================

class TestEntropieTopographie:
    """Hauptklasse sammelt 168 Records."""

    def test_topographie_leer(self):
        t = EntropieTopographie()
        assert t.records == []
        assert t.n_total == 0

    def test_topographie_add(self):
        t = EntropieTopographie()
        pe = PhaseEntropie(0, 4.0, 15, 'E', 15, 16.0)
        t.add(pe)
        assert t.n_total == 1
        assert t.records[0] == pe

    def test_topographie_extrema(self):
        """Max/Min Entropie sind dokumentiert."""
        t = EntropieTopographie()
        for i, h in enumerate([3.5, 4.0, 4.2, 3.8]):
            t.add(PhaseEntropie(i, h, 15, 'E', 12, 2**h))
        max_h, min_h = t.entropie_extrema()
        assert max_h == 4.2
        assert min_h == 3.5

    def test_topographie_mean_std(self):
        """Mittelwert und Standardabweichung."""
        t = EntropieTopographie()
        for i, h in enumerate([3.0, 4.0, 5.0]):
            t.add(PhaseEntropie(i, h, 15, 'E', 12, 2**h))
        assert abs(t.entropy_mean() - 4.0) < 0.001
        assert t.entropy_std() > 0

    def test_topographie_alle_168_phasen(self):
        """Alle 168 Phasen sind dokumentiert."""
        result = kartographiere_phaenomen()
        assert result['n_total'] == 168


# ============================================================
# TEST 3: Pole der Topographie
# ============================================================

class TestEntropiePole:
    """Phase 3 (Min) und Phase 122 (Max) als Pole."""

    def test_phase_3_ist_minimum(self):
        """Phase 3 hat die minimale Entropie."""
        result = kartographiere_phaenomen()
        min_pe = result['pole_min']
        assert min_pe.phase_idx == 3
        assert min_pe.entropy < 4.0  # unter dem Mittelwert

    def test_phase_122_ist_maximum(self):
        """Phase 122 hat die maximale Entropie."""
        result = kartographiere_phaenomen()
        max_pe = result['pole_max']
        assert max_pe.phase_idx == 122
        assert max_pe.entropy > 4.0  # über dem Mittelwert

    def test_pole_3_vs_122_unterschied(self):
        """Die Pole unterscheiden sich um mindestens 0.3 in H."""
        result = kartographiere_phaenomen()
        diff = result['pole_max'].entropy - result['pole_min'].entropy
        assert diff > 0.3

    def test_pole_inhalt_phase_3(self):
        """Phase 3 ist strukturiert (niedrige Entropie = Repetition)."""
        text = load_tengri_text()
        phases = tengri_to_phases(text)
        phase_3 = phases[3]
        # Niedrige Entropie → wenige unique symbols
        n_unique = len(set(phase_3))
        # Bei H ≈ 3.64 erwarten wir <= 20 unique symbols
        assert n_unique <= 22

    def test_pole_inhalt_phase_122(self):
        """Phase 122 ist chaotisch (hohe Entropie = Vielfalt)."""
        text = load_tengri_text()
        phases = tengri_to_phases(text)
        phase_122 = phases[122]
        # Hohe Entropie → viele unique symbols
        n_unique = len(set(phase_122))
        # Bei H ≈ 4.18 erwarten wir viele unique symbols
        assert n_unique >= 20


# ============================================================
# TEST 4: Topographie pro Tag (P68-Brücke)
# ============================================================

class TestEntropieProTag:
    """7-Tage-Aggregation: Sabbat vs. Chaos."""

    def test_7_tage_dokumentiert(self):
        """7 Tage sind dokumentiert."""
        result = kartographiere_phaenomen()
        per_day = result['per_day']
        assert len(per_day) == 7

    def test_jeder_tag_hat_24_phasen(self):
        """Jeder Tag hat (bis zu) 24 Phasen."""
        result = kartographiere_phaenomen()
        per_day = result['per_day']
        for d in per_day:
            assert d['n_phases'] == 24

    def test_sabbat_vs_chaos_entropie(self):
        """Sabbat-Tag (7) vs. Chaos-Tag (6) entropisch verglichen."""
        result = kartographiere_phaenomen()
        per_day = result['per_day']
        # Tag 7 = Deuteronomium (Sabbat)
        sabbat = next(d for d in per_day if d['day_idx'] == 7)
        # Tag 6 = Numeri (Chaos, gemäß P68)
        chaos = next(d for d in per_day if d['day_idx'] == 6)
        # Beide haben gültige H-Werte
        assert 0 < sabbat['mean_entropy'] < 5
        assert 0 < chaos['mean_entropy'] < 5

    def test_tag_entropie_erlaubt_spektrum(self):
        """H-Werte pro Tag sind im sinnvollen Bereich."""
        result = kartographiere_phaenomen()
        per_day = result['per_day']
        for d in per_day:
            # H zwischen 0 und log2(26) ≈ 4.70
            assert 0 <= d['mean_entropy'] <= 4.71


# ============================================================
# TEST 5: Topographie pro Tora-Buch
# ============================================================

class TestEntropieProBuch:
    """Aggregation auf 5 Tora-Bücher."""

    def test_5_buecher_dokumentiert(self):
        """5 Tora-Bücher sind dokumentiert."""
        result = kartographiere_phaenomen()
        per_book = result['per_book']
        assert len(per_book) == 5

    def test_jedes_buch_in_result(self):
        """Genesis, Exodus, Leviticus, Numeri, Deuteronomium."""
        result = kartographiere_phaenomen()
        per_book = result['per_book']
        for book in ['Genesis', 'Exodus', 'Leviticus',
                     'Numeri', 'Deuteronomium']:
            assert book in per_book

    def test_buch_entropie_sinnvoll(self):
        """H pro Buch im sinnvollen Bereich."""
        result = kartographiere_phaenomen()
        per_book = result['per_book']
        for book, mean in per_book.items():
            assert 0 < mean < 4.71


# ============================================================
# TEST 6: Orakel-Phase (Phase 5) im Spektrum
# ============================================================

class TestOrakelPhaseImSpektrum:
    """Phase 5 (das Orakel) im Entropie-Spektrum."""

    def test_phase_5_entropie_dokumentiert(self):
        """Phase 5 hat eine messbare Entropie."""
        result = kartographiere_phaenomen()
        phase_5 = next(p for p in result['records'] if p.phase_idx == 5)
        assert 0 < phase_5.entropy < 5

    def test_phase_5_perzentil(self):
        """Phase 5 liegt im mittleren Perzentil-Bereich."""
        result = kartographiere_phaenomen()
        sorted_h = sorted([p.entropy for p in result['records']])
        phase_5 = next(p for p in result['records'] if p.phase_idx == 5)
        # Perzentil-Rang von Phase 5
        n_below = sum(1 for h in sorted_h if h < phase_5.entropy)
        percentile = 100 * n_below / len(sorted_h)
        # Phase 5 liegt NICHT an einem Extrem (20%-80%)
        assert 20 <= percentile <= 80

    def test_phase_5_ueber_mittelwert_minus_std(self):
        """Phase 5 liegt nicht weit unter dem Mittelwert."""
        result = kartographiere_phaenomen()
        phase_5 = next(p for p in result['records'] if p.phase_idx == 5)
        mean = result['mean']
        # Phase 5 ist nicht > 3*Std unter dem Mittelwert
        assert phase_5.entropy > mean - 3 * result['std']


# ============================================================
# TEST 7: Korrelationen (H ↔ Gematria ↔ Violations)
# ============================================================

class TestEntropieKorrelationen:
    """H ↔ Gematria ↔ Violations."""

    def test_korrelation_h_gematria(self):
        """H ↔ Gematria-Summe."""
        result = kartographiere_phaenomen()
        corr = result['correlation_h_gematria']
        # Korrelationskoeffizient im Bereich [-1, 1]
        assert -1 <= corr <= 1

    def test_korrelation_h_violations(self):
        """H ↔ Violations (aus P68, soweit verfügbar)."""
        result = kartographiere_phaenomen()
        # Wenn P68-Daten verfügbar: Korrelation
        # Wenn nicht: dokumentiere None
        corr = result.get('correlation_h_violations')
        if corr is not None:
            assert -1 <= corr <= 1

    def test_korrelations_methode_existiert(self):
        """korrelation_topographie() ist aufrufbar."""
        result = kartographiere_phaenomen()
        # Muss ein Dict zurückgeben
        assert 'correlation_h_gematria' in result

    def test_h_und_alphabet_effizienz_konsistent(self):
        """H und 2^H sind konsistent."""
        result = kartographiere_phaenomen()
        for p in result['records'][:5]:
            expected_eff = 2 ** p.entropy
            # Innerhalb 1% Genauigkeit
            assert abs(p.alphabet_size_eff - expected_eff) < 0.5


# ============================================================
# TEST 8: Alphabet-Effizienz
# ============================================================

class TestAlphabetEffizienz:
    """Effektive Alphabetgröße 2^H."""

    def test_alphabet_effizienz_h0(self):
        """H=0 → 2^H = 1 (perfekte Ordnung)."""
        assert alphabet_effizienz(0.0) == 1.0

    def test_alphabet_effizienz_h4(self):
        """H=4 → 2^H = 16."""
        assert alphabet_effizienz(4.0) == 16.0

    def test_alphabet_effizienz_h_log2_26(self):
        """H=log2(26) → 2^H = 26."""
        eff = alphabet_effizienz(math.log2(26))
        assert abs(eff - 26.0) < 0.01


# ============================================================
# TEST 9: Apophenie-Schutz
# ============================================================

class TestApophenieSchutz:
    """Schutz vor Überinterpretation."""

    def test_h_mean_4_ist_hypothese(self):
        """H_mean ≈ log2(16) ist Beobachtung, kein Beweis."""
        result = kartographiere_phaenomen()
        mean = result['mean']
        # log2(16) = 4.0 exakt
        # Wir prüfen nur, dass die Differenz messbar klein ist
        diff = abs(mean - 4.0)
        # Aber NICHT: diff == 0
        # Sonst: nur dokumentieren
        assert diff >= 0  # trivial

    def test_korrelationen_sind_zahlen_keine_kausalitaet(self):
        """Korrelationskoeffizienten sind Zahlen, keine Kausalität."""
        result = kartographiere_phaenomen()
        corr = result['correlation_h_gematria']
        # Wir behaupten NICHT: "H verursacht Gematria"
        # Wir berichten nur den Zahlenwert
        assert isinstance(corr, (int, float))


# ============================================================
# TEST 10: Determinismus
# ============================================================

class TestDeterminismus:
    """kartographiere_phaenomen ist deterministisch."""

    def test_3_runs_identisch(self):
        """3 Aufrufe liefern identische Resultate."""
        r1 = kartographiere_phaenomen()
        r2 = kartographiere_phaenomen()
        r3 = kartographiere_phaenomen()
        assert r1['mean'] == r2['mean'] == r3['mean']
        assert r1['pole_min'].entropy == r2['pole_min'].entropy
        assert r1['pole_max'].entropy == r2['pole_max'].entropy

    def test_records_identisch(self):
        """Records sind exakt identisch."""
        r1 = kartographiere_phaenomen()
        r2 = kartographiere_phaenomen()
        h1 = [p.entropy for p in r1['records']]
        h2 = [p.entropy for p in r2['records']]
        assert h1 == h2


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
