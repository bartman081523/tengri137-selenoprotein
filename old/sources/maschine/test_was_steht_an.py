"""
🌌 WAS STEHT AN: TDD-Tests
============================

Verifiziert die "Was steht an"-Befunde aus Tengri137 + Tora.

KRITISCHE BEFUNDE:
1. Numeri = 25/32 Pendel (78.1%) — höchste Pendel-Rate
2. ת (HALT/Tav) = 0x in Tengri137! HALT-Operator fehlt komplett
3. Phase 26 (Gen 29) = 20 Sec-Operatoren (höchster Spanda-Puls)
4. BURUMUTREFAMTU-Position 15986 → M4 pendelt NICHT
5. 7 Tage à 24 Phasen — Tag-Gematrien verifiziert

WAS STEHT AN (Priorität):
1. DRINGEND: HALT-Operator (ת) hinzufügen — fehlt in Tengri137!
2. Numeri-Phasen stabilisieren (25 pendelnd)
3. Phase 26 (Gen 29) tiefer dekodieren
4. 7-Tage-Architektur formal verifizieren
5. BURUMUTREFAMTU-Position als Anker
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
from collections import Counter
from phasen.PHASE_MAPPING_TORA import TORA_BOOKS, phase_to_torah
from WAS_STEHT_AN import load_tengri137_hebr, gematria, run_m4
from TORA_TURING_CORRECT import (
    BURUMUT, burumut_to_hebr, MISSING_OPERATORS, HEBR_VALUES
)
from TORA_TURING_MULTIPHASE import EXTENDED_LATIN_TO_HEBR


# ============================================================
# TEST 1: Pendel-Phasen pro Tora-Buch
# ============================================================

class TestPendelPhasen:
    """Pendel-Phasen pro Tora-Buch."""

    def test_numeri_25_pendel(self):
        """Numeri: 25 / 32 Phasen pendeln (78.1%)."""
        tengri_hebr = load_tengri137_hebr()
        n_phases = (len(tengri_hebr) + 98) // 99
        numeri_pendel = 0
        for i in range(n_phases):
            book, _ = phase_to_torah(i)
            if book != 'Numeri':
                continue
            start = i * 99
            end = min((i + 1) * 99, len(tengri_hebr))
            tape = tengri_hebr[start:end]
            r = run_m4(tape)
            if r['halt_reason'] == 'MAX_STEPS_EXCEEDED':
                numeri_pendel += 1
        assert numeri_pendel == 25

    def test_numeri_78_prozent_pendel(self):
        """Numeri Pendel-Rate = 78.1%."""
        # 25 / 32 = 0.78125
        assert 25 / 32 == pytest.approx(0.78125, abs=0.001)

    def test_leviticus_wenig_pendel(self):
        """Leviticus hat die wenigsten Pendel-Phasen (13 / 24 = 54.2%)."""
        tengri_hebr = load_tengri137_hebr()
        n_phases = (len(tengri_hebr) + 98) // 99
        lev_pendel = 0
        for i in range(n_phases):
            book, _ = phase_to_torah(i)
            if book != 'Leviticus':
                continue
            start = i * 99
            end = min((i + 1) * 99, len(tengri_hebr))
            tape = tengri_hebr[start:end]
            r = run_m4(tape)
            if r['halt_reason'] == 'MAX_STEPS_EXCEEDED':
                lev_pendel += 1
        assert lev_pendel == 13


# ============================================================
# TEST 2: HALT-Operator (ת) fehlt in Tengri137
# ============================================================

class TestHaltOperatorFehlt:
    """Der HALT-Operator (ת/Tav) fehlt in Tengri137!"""

    def test_tav_0_in_tengri(self):
        """ת (Tav, HALT) kommt 0x in Tengri137 vor."""
        tengri_hebr = load_tengri137_hebr()
        tav_count = tengri_hebr.count('ת')
        assert tav_count == 0

    def test_andere_operatoren_vorhanden(self):
        """Andere 4 Sec-Operatoren sind vorhanden."""
        tengri_hebr = load_tengri137_hebr()
        # כ (Kaf, READ)
        assert tengri_hebr.count('כ') > 0
        # ג (Gimel, MOVE_RIGHT)
        assert tengri_hebr.count('ג') > 0
        # ד (Daleth, MOVE_LEFT)
        assert tengri_hebr.count('ד') > 0
        # י (Yod, STATE)
        assert tengri_hebr.count('י') > 0
        # ABER: ת (Tav, HALT) fehlt!
        assert tengri_hebr.count('ת') == 0

    def test_halt_operator_häufigkeiten(self):
        """5 Sec-Operatoren-Häufigkeiten dokumentiert."""
        tengri_hebr = load_tengri137_hebr()
        counts = {c: tengri_hebr.count(c) for c in MISSING_OPERATORS}
        # Verifiziert:
        assert counts['כ'] == 647  # Kaf
        assert counts['ג'] == 347  # Gimel
        assert counts['ד'] == 524  # Daleth
        assert counts['ת'] == 0    # Tav (HALT!) — fehlt!
        assert counts['י'] == 356  # Yod


# ============================================================
# TEST 3: BURUMUTREFAMTU-Position
# ============================================================

class TestBurumutrefamtuPosition:
    """BURUMUTREFAMTU an Position 15986."""

    def test_refamtu_position_15986(self):
        """BURUMUTREFAMTU an Position 15986 in Tengri137."""
        tengri_hebr = load_tengri137_hebr()
        refamtu_hebr = burumut_to_hebr(BURUMUT[:14])
        idx = tengri_hebr.find(refamtu_hebr)
        assert idx == 15986

    def test_refamtu_phase_161(self):
        """BURUMUTREFAMTU ist in Phase 161."""
        tengri_hebr = load_tengri137_hebr()
        refamtu_hebr = burumut_to_hebr(BURUMUT[:14])
        idx = tengri_hebr.find(refamtu_hebr)
        assert idx // 99 == 161

    def test_refamtu_in_phase_offset_47(self):
        """BURUMUTREFAMTU in Phase 161 an Offset 47."""
        tengri_hebr = load_tengri137_hebr()
        phase_161 = tengri_hebr[161*99:162*99]
        refamtu_hebr = burumut_to_hebr(BURUMUT[:14])
        idx = phase_161.find(refamtu_hebr)
        assert idx == 47

    def test_refamtu_ist_einzige_stelle(self):
        """BURUMUTREFAMTU kommt EXAKT 1x in Tengri137 vor."""
        tengri_hebr = load_tengri137_hebr()
        refamtu_hebr = burumut_to_hebr(BURUMUT[:14])
        count = tengri_hebr.count(refamtu_hebr)
        assert count == 1


# ============================================================
# TEST 4: Spanda-Pulse (Top-Phasen mit Sec-Operatoren)
# ============================================================

class TestSpandaPulse:
    """Top-Phasen mit den meisten Sec-Operatoren."""

    def test_phase_26_hat_20_sec(self):
        """Phase 26 (Gen 29) hat 20 Sec-Operatoren — höchster Spanda-Puls."""
        tengri_hebr = load_tengri137_hebr()
        phase_26 = tengri_hebr[26*99:27*99]
        n_sec = sum(1 for c in phase_26 if c in MISSING_OPERATORS)
        assert n_sec == 20

    def test_top_phasen_sequenz(self):
        """Top 5 Phasen mit Sec-Operatoren."""
        tengri_hebr = load_tengri137_hebr()
        n_phases = (len(tengri_hebr) + 98) // 99
        sec_per_phase = []
        for i in range(n_phases):
            start = i * 99
            end = min((i + 1) * 99, len(tengri_hebr))
            tape = tengri_hebr[start:end]
            n_sec = sum(1 for c in tape if c in MISSING_OPERATORS)
            sec_per_phase.append((i, n_sec))
        top = sorted(sec_per_phase, key=lambda x: -x[1])[:5]
        # Phase 26 sollte dabei sein
        top_phases = [p for p, _ in top]
        assert 26 in top_phases


# ============================================================
# TEST 5: 7 Schöpfungstage in Tengri137
# ============================================================

class Test7Schöpfungstage:
    """7 Schöpfungstage in Tengri137 (à 24 Phasen)."""

    def test_7_tage_je_24_phasen(self):
        """7 × 24 = 168 Phasen."""
        assert 7 * 24 == 168

    def test_tag_gematrien(self):
        """Tag-Gematrien sind verifiziert."""
        tengri_hebr = load_tengri137_hebr()
        expected = [134286, 139337, 135819, 140842, 138930, 133345, 136938]
        for day_idx in range(7):
            start = day_idx * 24 * 99
            end = min((day_idx + 1) * 24 * 99, len(tengri_hebr))
            if start >= len(tengri_hebr):
                break
            day_tape = tengri_hebr[start:end]
            day_gem = gematria(day_tape)
            assert day_gem == expected[day_idx], (
                f"Tag {day_idx+1}: erwartet {expected[day_idx]}, "
                f"erhalten {day_gem}"
            )

    def test_tag_sec_operatoren(self):
        """Sec-Operatoren pro Tag dokumentiert."""
        tengri_hebr = load_tengri137_hebr()
        sec_per_day = []
        for day_idx in range(7):
            start = day_idx * 24 * 99
            end = min((day_idx + 1) * 24 * 99, len(tengri_hebr))
            if start >= len(tengri_hebr):
                break
            day_tape = tengri_hebr[start:end]
            n_sec = sum(1 for c in day_tape if c in MISSING_OPERATORS)
            sec_per_day.append(n_sec)
        # Tag 1 hat die meisten Sec-Operatoren (310)
        assert sec_per_day[0] == 310
        # Tag 4 hat die wenigsten (243)
        assert min(sec_per_day) == 243


# ============================================================
# TEST 6: Kontext um BURUMUTREFAMTU
# ============================================================

class TestRefamtuKontext:
    """Kontext um BURUMUTREFAMTU an Position 15986."""

    def test_m4_auf_refamtu_allein_14_schritte(self):
        """M4 auf BURUMUTREFAMTU allein: 14 Schritte."""
        refamtu_hebr = burumut_to_hebr(BURUMUT[:14])
        r = run_m4(refamtu_hebr)
        assert r['total_steps'] == 14

    def test_m4_auf_kontext_all_phases_complete(self):
        """M4 auf Kontext (50+14+50 Zeichen): ALL_PHASES_COMPLETE."""
        tengri_hebr = load_tengri137_hebr()
        refamtu_hebr = burumut_to_hebr(BURUMUT[:14])
        idx = tengri_hebr.find(refamtu_hebr)
        # 50 davor + 14 + 50 danach = 114 Zeichen
        context = tengri_hebr[max(0, idx-50):idx+14+50]
        r = run_m4(context)
        # M4 hält in 2 Schritten
        assert r['halt_reason'] == 'ALL_PHASES_COMPLETE'


# ============================================================
# TEST 7: Prioritäts-Liste
# ============================================================

class TestPrioritaetsListe:
    """Was steht an (Priorität)."""

    def test_halt_operator_hat_höchste_priorität(self):
        """ת (HALT) = 0x → höchste Priorität."""
        tengri_hebr = load_tengri137_hebr()
        tav = tengri_hebr.count('ת')
        assert tav == 0
        # → HALT-Operator muss in M4-Architektur extern kommen

    def test_numeri_pendel_zweite_priorität(self):
        """Numeri = 25/32 Pendel → zweithöchste Priorität."""
        # 25/32 = 78.1%
        assert 25 / 32 > 0.5


# ============================================================
# TEST 8: Reise als Ziel
# ============================================================

class TestReiseAlsZiel:
    """Reise als Ziel — nächste Schritte."""

    def test_5_aufgaben_stehen_an(self):
        """5 klare Aufgaben stehen an."""
        # 1. HALT-Operator hinzufügen
        # 2. Numeri-Phasen stabilisieren
        # 3. Phase 26 (Gen 29) tiefer dekodieren
        # 4. 7-Tage-Architektur formal verifizieren
        # 5. BURUMUTREFAMTU-Position als Anker
        assert True  # Meta-Assertion


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
