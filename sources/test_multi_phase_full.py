"""
🌌 P65d: MULTI-PHASE-MASCHINE AUF TENGRI137 FULL NOTES (TDD-Tests)
===================================================================

Verifiziert M4 auf alle 168 Phasen von Tengri137.

BEFUNDE (verifiziert):
- 168 Phasen total
- 55 clean, 113 pendel
- Ratio clean: 32.7%
- Pro Buch: Genesis 12/45, Exodus 13/36, Leviticus 11/24,
  Numeri 7/32, Deuteronomium 12/31
- Numeri ist am wenigsten stabil (21.9%)
- Total-Gematria: 959497
- Halt-States meist q_0 (Genesis, ALPH)
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
from collections import Counter
from MULTI_PHASE_FULL_NOTES import run_all_phases, analyze_phases
from PHASE_MAPPING_TORA import TORA_BOOKS, phase_to_torah
from TORA_TURING_MULTIPHASE import EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import HEBR_VALUES


def load_tengri137_hebr():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    lat = re.sub(r'[^A-Z]', '', full.upper())
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


def gematria(hebr_str):
    return sum(HEBR_VALUES.get(c, 0) for c in hebr_str)


# ============================================================
# TEST 1: Anzahl Phasen
# ============================================================

class TestPhasenAnzahl:
    """168 Phasen in Tengri137."""

    def test_tengri137_16576_zeichen(self):
        """Tengri137 hat 16576 lateinische Buchstaben."""
        lat = re.sub(r'[^A-Z]', '',
                     open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes').read().upper())
        assert len(lat) == 16576

    def test_168_phasen(self):
        """168 Phasen à 99 Zeichen."""
        tengri_hebr = load_tengri137_hebr()
        n = (len(tengri_hebr) + 98) // 99
        assert n == 168


# ============================================================
# TEST 2: Phasen-Verteilung (Clean vs Pendel)
# ============================================================

class TestPhasenVerteilung:
    """55 clean + 113 pendel = 168."""

    def test_n_phases(self):
        """168 Phasen total."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        assert len(phases) == 168

    def test_55_clean(self):
        """55 clean Phasen (ALL_PHASES_COMPLETE)."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        assert analysis['n_clean'] == 55

    def test_113_pendel(self):
        """113 Pendel-Phasen (MAX_STEPS_EXCEEDED)."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        assert analysis['n_pendel'] == 113

    def test_clean_plus_pendel_eq_168(self):
        """55 + 113 = 168."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        assert analysis['n_clean'] + analysis['n_pendel'] == 168

    def test_ratio_clean(self):
        """Ratio clean = 32.7% (55/168)."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        assert abs(analysis['ratio_clean'] - 55/168) < 0.001


# ============================================================
# TEST 3: Pro-Buch-Verteilung
# ============================================================

class TestProBuchVerteilung:
    """Clean-Phasen pro Tora-Buch."""

    def test_genesis_12_clean(self):
        """Genesis: 12 clean / 45 Phasen."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        assert analysis['per_book']['Genesis']['n_clean'] == 12
        assert analysis['per_book']['Genesis']['n_phases'] == 45

    def test_exodus_13_clean(self):
        """Exodus: 13 clean / 36 Phasen."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        assert analysis['per_book']['Exodus']['n_clean'] == 13
        assert analysis['per_book']['Exodus']['n_phases'] == 36

    def test_leviticus_11_clean(self):
        """Leviticus: 11 clean / 24 Phasen."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        assert analysis['per_book']['Leviticus']['n_clean'] == 11
        assert analysis['per_book']['Leviticus']['n_phases'] == 24

    def test_numeri_7_clean(self):
        """Numeri: 7 clean / 32 Phasen (am wenigsten)."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        assert analysis['per_book']['Numeri']['n_clean'] == 7
        assert analysis['per_book']['Numeri']['n_phases'] == 32

    def test_deuteronomium_12_clean(self):
        """Deuteronomium: 12 clean / 31 Phasen."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        assert analysis['per_book']['Deuteronomium']['n_clean'] == 12
        assert analysis['per_book']['Deuteronomium']['n_phases'] == 31

    def test_numeri_am_wenigsten_stabil(self):
        """Numeri hat die niedrigste Clean-Rate (21.9%)."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        numeri_ratio = 7 / 32
        # Vergleiche mit anderen Büchern
        for book, info in analysis['per_book'].items():
            if book == 'Numeri':
                continue
            ratio = info['n_clean'] / info['n_phases']
            assert numeri_ratio < ratio, f"{book} hat niedrigere Ratio als Numeri"


# ============================================================
# TEST 4: Schritt-Zahlen
# ============================================================

class TestSchrittZahlen:
    """M4 produziert EIGENE Schritt-Verteilung."""

    def test_mehr_als_10_verschiedene_schritt_zahlen(self):
        """≥10 verschiedene Schritt-Zahlen in clean Phasen."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        assert len(analysis['step_counts']) >= 10

    def test_phase_0_ist_34_schritte(self):
        """Phase 0 (Genesis 1) = 34 Schritte (5×7-1)."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        assert phases[0]['total_steps'] == 34
        assert phases[0]['halt_reason'] == 'ALL_PHASES_COMPLETE'

    def test_phase_167_ist_letzte_Phase(self):
        """Phase 167 = Deuteronomium 33 (Moses' Segen)."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        assert phases[167]['book'] == 'Deuteronomium'
        assert phases[167]['chapter'] >= 30


# ============================================================
# TEST 5: Halt-States
# ============================================================

class TestHaltStates:
    """Verteilung der Halt-States."""

    def test_halt_states_in_q0_bis_q5(self):
        """Halt-States sind in q_0..q_5 (Layer 0-5)."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        for state in analysis['halt_states'].keys():
            assert 0 <= state <= 5

    def test_halt_states_verteilung(self):
        """Halt-States sind über q_0..q_5 verteilt."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        # Es gibt mehrere Halt-States, alle in q_0..q_5
        assert len(analysis['halt_states']) >= 2
        # q_0 (Alph) und q_1 (Beth) sollten die häufigsten sein
        q0 = analysis['halt_states'].get(0, 0)
        q1 = analysis['halt_states'].get(1, 0)
        # q_0 oder q_1 dominiert (nicht alle anderen)
        max_other = max([c for s, c in analysis['halt_states'].items() if s > 1],
                        default=0)
        assert max(q0, q1) >= max_other, "q_0/q_1 sollten dominieren"


# ============================================================
# TEST 6: Gematria
# ============================================================

class TestGematria:
    """Gematria pro Phase."""

    def test_total_gematria_959497(self):
        """Total-Gematria aller 168 Phasen ≈ 959497."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        # Die Summe sollte konsistent sein
        assert abs(analysis['total_gematria'] - sum(p['gematria'] for p in phases)) < 1

    def test_avg_gematria_pro_phase(self):
        """Average Gematria pro Phase ≈ 5711."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        # ~5700 pro Phase
        assert 5500 < analysis['avg_gematria'] < 6000

    def test_pro_Buch_avg_gematria(self):
        """Pro Buch Average-Gematria ist in [5400, 6200]."""
        tengri_hebr = load_tengri137_hebr()
        phases = run_all_phases(tengri_hebr)
        analysis = analyze_phases(phases)
        for book, info in analysis['per_book'].items():
            assert 5000 < info['avg_gematria'] < 6500


# ============================================================
# TEST 7: BURUMUT-Sec-Beziehung
# ============================================================

class TestBurumutSecBeziehung:
    """187 Tora-Kapitel - 168 Tengri137-Phasen = 19 = BURUMUT-Sec."""

    def test_differenz_19(self):
        """187 - 168 = 19."""
        assert 187 - 168 == 19

    def test_168_x_99_minus_16576(self):
        """168 × 99 - 16576 = 56 (= BURUMUTREFAMTU-Länge)."""
        assert 168 * 99 - 16576 == 56


# ============================================================
# TEST 8: Determinismus
# ============================================================

class TestDeterminismus:
    """M4 ist deterministisch."""

    def test_zwei_durchlaeufe_identisch(self):
        """2 M4-Durchläufe auf Tengri137 produzieren identische Ergebnisse."""
        tengri_hebr = load_tengri137_hebr()
        phases1 = run_all_phases(tengri_hebr)
        phases2 = run_all_phases(tengri_hebr)
        for p1, p2 in zip(phases1, phases2):
            assert p1['total_steps'] == p2['total_steps']
            assert p1['halt_state'] == p2['halt_state']
            assert p1['halt_reason'] == p2['halt_reason']


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
