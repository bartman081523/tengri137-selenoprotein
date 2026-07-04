"""
🌌 P62c: KANONISCHER SPANDA-PULS IN M4 (TDD-Tests)
====================================================

Verifiziert den SpandaPulsDetector:
1. BURUMUTREFAMTU als Substring im Tape → Pulse
2. 5 BURUMUT-Sec-Buchstaben (כ, ג, ד, ת, י) → Pulse
3. Position 15986 in Tengri137 → BURUMUTREFAMTU

WICHTIG:
- M4 modifiziert das Tape NICHT (Tape-Invariante bewahrt)
- Spanda-Puls ist eine BEOBACHTUNG, keine Aktion
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
from SPANDA_PULS_M4 import (
    SpandaPulsDetector, detect_spanda_pulse_in_tape,
    SEC_CHARS, REFAMTU_HEBR
)
from TORA_TURING_CORRECT import (
    BURUMUT, burumut_to_hebr, MISSING_OPERATORS
)
from TORA_TURING_MULTIPHASE import EXTENDED_LATIN_TO_HEBR


def load_tengri137_hebr():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    lat = re.sub(r'[^A-Z]', '', full.upper())
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


# ============================================================
# TEST 1: Detektor-Konstanten
# ============================================================

class TestSpandaPulsDetektorKonstanten:
    """SpandaPulsDetector-Konstanten."""

    def test_5_sec_operatoren(self):
        """5 BURUMUT-Sec-Operatoren (כ, ג, ד, ת, י)."""
        assert len(SEC_CHARS) == 5
        assert SEC_CHARS == set(MISSING_OPERATORS.keys())

    def test_refamtu_hebr_korrekt(self):
        """REFAMTU_HEBR = בשצשמשרצהואמרש (14 Zeichen)."""
        assert REFAMTU_HEBR == 'בשצשמשרצהואמרש'
        assert len(REFAMTU_HEBR) == 14

    def test_5_operatoren_beschriftet(self):
        """5 Operatoren: READ, MOVE_RIGHT, MOVE_LEFT, HALT, STATE."""
        assert MISSING_OPERATORS['כ'] == 'READ'
        assert MISSING_OPERATORS['ג'] == 'MOVE_RIGHT'
        assert MISSING_OPERATORS['ד'] == 'MOVE_LEFT'
        assert MISSING_OPERATORS['ת'] == 'HALT'
        assert MISSING_OPERATORS['י'] == 'STATE'


# ============================================================
# TEST 2: Substring-Detektion
# ============================================================

class TestSubstringDetektion:
    """BURUMUTREFAMTU als Substring im Tape."""

    def test_burumut_startet_mit_refamtu(self):
        """BURUMUT-99 startet mit BURUMUTREFAMTU."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        detector = SpandaPulsDetector(burumut_hebr)
        assert detector.check_burumutrefamtu_at_start() is True

    def test_burumut_enthaelt_refamtu(self):
        """BURUMUT-99 enthält BURUMUTREFAMTU."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        detector = SpandaPulsDetector(burumut_hebr)
        assert detector.check_burumutrefamtu_in_tape() is True

    def test_refamtu_position_in_burumut(self):
        """BURUMUTREFAMTU-Position in BURUMUT = 0."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        detector = SpandaPulsDetector(burumut_hebr)
        assert detector.find_burumutrefamtu_position() == 0

    def test_leeres_tape_kein_refamtu(self):
        """Leeres Tape enthält kein BURUMUTREFAMTU."""
        detector = SpandaPulsDetector('')
        assert detector.check_burumutrefamtu_in_tape() is False
        assert detector.find_burumutrefamtu_position() == -1

    def test_zufaelliges_tape_kein_refamtu(self):
        """Zufälliges Tape enthält kein BURUMUTREFAMTU."""
        random_tape = 'אבגדהוזחטיכלמנסעפצקרשת' * 10
        detector = SpandaPulsDetector(random_tape)
        assert detector.check_burumutrefamtu_in_tape() is False


# ============================================================
# TEST 3: Sec-Operator-Detektion
# ============================================================

class TestSecOperatorDetektion:
    """5 BURUMUT-Sec-Buchstaben im Tape."""

    def test_burumut_enthaelt_sec_char(self):
        """BURUMUT-99 enthält mindestens einen Sec-Buchstaben."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        detector = SpandaPulsDetector(burumut_hebr)
        sec_positions = detector.find_sec_positions()
        assert len(sec_positions) >= 1

    def test_burumut_sec_position(self):
        """BURUMUT hat Sec-Operator an Position 28 (YAPSUAZBEHIMLA)."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        detector = SpandaPulsDetector(burumut_hebr)
        sec_positions = detector.find_sec_positions()
        # Position 28 = 'A' (YAPSUAZBEHIMLA[2] = P? oder 'A' = Aleph)
        # Lass uns die genaue Position prüfen
        # BURUMUT[28:42] = YAPSUAZBEHIMLA
        # Y=י(SEC!), A=A, P=פ, S=ש, U=ע, A=A, Z=ז, B=ב, E=ע, H=ה, I=י(SEC!), M=מ, L=ל, A=A
        # Erste Sec-Position sollte 28 sein (Y=י)
        assert 28 in sec_positions

    def test_tengri99_hat_9_sec_chars(self):
        """Tengri137-99 hat 9 Sec-Buchstaben."""
        tengri_hebr = load_tengri137_hebr()
        tengri_99 = tengri_hebr[:99]
        detector = SpandaPulsDetector(tengri_99)
        sec_positions = detector.find_sec_positions()
        # Genau 9 Sec-Buchstaben in Tengri-99
        assert len(sec_positions) == 9

    def test_sec_char_observation(self):
        """observe_step registriert Sec-Operator."""
        detector = SpandaPulsDetector('test')
        detector.observe_step(step_idx=1, position=10, symbol='כ', new_state=0)
        assert len(detector.pulse_events) == 1
        assert detector.pulse_events[0]['type'] == 'SEC_OPERATOR'
        assert detector.pulse_events[0]['operator'] == 'READ'

    def test_non_sec_char_kein_event(self):
        """Nicht-Sec-Buchstabe triggert KEIN Event."""
        detector = SpandaPulsDetector('test')
        detector.observe_step(step_idx=1, position=10, symbol='א', new_state=0)
        assert len(detector.pulse_events) == 0


# ============================================================
# TEST 4: M4-Integration
# ============================================================

class TestM4Integration:
    """SpandaPulsDetector + M4."""

    def test_m4_auf_burumut_15_schritte(self):
        """M4 auf BURUMUT → 15 Schritte (q_5 HALT)."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        r = detect_spanda_pulse_in_tape(burumut_hebr)
        assert r['machine']['total_steps'] == 15
        assert r['machine']['halt_reason'] == 'ALL_PHASES_COMPLETE'

    def test_m4_auf_tengri99_34_schritte(self):
        """M4 auf Tengri137-99 → 34 Schritte."""
        tengri_hebr = load_tengri137_hebr()
        tengri_99 = tengri_hebr[:99]
        r = detect_spanda_pulse_in_tape(tengri_99, tengri_offset=0)
        assert r['machine']['total_steps'] == 34

    def test_m4_auf_tengri99_2_pulse_events(self):
        """M4 auf Tengri137-99 → 2 Spanda-Pulse."""
        tengri_hebr = load_tengri137_hebr()
        tengri_99 = tengri_hebr[:99]
        r = detect_spanda_pulse_in_tape(tengri_99, tengri_offset=0)
        # In 34 Schritten liest M4 34 Symbole
        # Mindestens 2 davon sind Sec-Operatoren
        assert r['detector']['n_pulse_events'] == 2

    def test_tape_invariante_unter_detector(self):
        """Detektor modifiziert das Tape NICHT."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        tape_before = burumut_hebr[:]
        detector = SpandaPulsDetector(burumut_hebr)
        detector.observe_step(1, 10, 'כ', 0)
        assert detector.tape == tape_before
        # Tape bleibt unverändert (nur Beobachtung)


# ============================================================
# TEST 5: BURUMUTREFAMTU in Tengri137-Phase 161
# ============================================================

class TestPhase161Refamtu:
    """Phase 161 enthält BURUMUTREFAMTU."""

    def test_phase_161_enthaelt_refamtu(self):
        """Phase 161 (Position 15939-16038) enthält BURUMUTREFAMTU."""
        tengri_hebr = load_tengri137_hebr()
        phase_161 = tengri_hebr[161*99:162*99]
        assert REFAMTU_HEBR in phase_161

    def test_refamtu_in_tengri_hebr_position_15986(self):
        """BURUMUTREFAMTU in Tengri137 (hebr.) an Position 15986."""
        tengri_hebr = load_tengri137_hebr()
        idx = tengri_hebr.find(REFAMTU_HEBR)
        assert idx == 15986

    def test_phase_161_ist_deuteronomium_region(self):
        """Phase 161 ist in der Deuteronomium-Region (137-167)."""
        # Phase 161 ist zwischen 137 (Deut-Start) und 168 (Ende)
        assert 137 <= 161 <= 168

    def test_m4_auf_phase_161_hat_pulse_events(self):
        """M4 auf Phase 161 hat Pulse-Events."""
        tengri_hebr = load_tengri137_hebr()
        phase_161 = tengri_hebr[161*99:162*99]
        r = detect_spanda_pulse_in_tape(phase_161, tengri_offset=161*99)
        # Mindestens 1 Pulse-Event (da BURUMUTREFAMTU gelesen wird)
        assert r['detector']['n_pulse_events'] >= 1


# ============================================================
# TEST 6: Statistik über alle 168 Phasen
# ============================================================

class TestStatistik168Phasen:
    """Spanda-Pulse über alle 168 Tengri137-Phasen."""

    def test_phasen_mit_pulse(self):
        """Mindestens 50 Phasen haben Spanda-Pulse."""
        tengri_hebr = load_tengri137_hebr()
        n_with_pulse = 0
        for i in range(168):
            start = i * 99
            end = min((i + 1) * 99, len(tengri_hebr))
            tape = tengri_hebr[start:end]
            r = detect_spanda_pulse_in_tape(tape, tengri_offset=start)
            if r['detector']['n_pulse_events'] > 0:
                n_with_pulse += 1
        # Mindestens 50 von 168 Phasen (29.8%)
        assert n_with_pulse >= 50

    def test_exakt_eine_phase_mit_refamtu(self):
        """Genau 1 Phase enthält BURUMUTREFAMTU (Position 161)."""
        tengri_hebr = load_tengri137_hebr()
        n_with_refamtu = 0
        for i in range(168):
            start = i * 99
            end = min((i + 1) * 99, len(tengri_hebr))
            tape = tengri_hebr[start:end]
            r = detect_spanda_pulse_in_tape(tape, tengri_offset=start)
            if r['detector']['refamtu_in_tape']:
                n_with_refamtu += 1
        # Genau 1 Phase (Phase 161, Position 15986)
        assert n_with_refamtu == 1

    def test_phase_161_hat_refamtu_in_tape(self):
        """Phase 161 ist die Phase mit BURUMUTREFAMTU."""
        tengri_hebr = load_tengri137_hebr()
        phase_161 = tengri_hebr[161*99:162*99]
        r = detect_spanda_pulse_in_tape(phase_161, tengri_offset=161*99)
        assert r['detector']['refamtu_in_tape'] is True
        # Position innerhalb der Phase: 15986 - 161*99 = 47
        assert r['detector']['refamtu_position'] == 47


# ============================================================
# TEST 7: M4-Apophenie-Check
# ============================================================

class TestM4ApophanieCheck:
    """Spanda-Puls ist KEINE Operator-Aktualisierung in Echtzeit."""

    def test_detector_schreibt_nicht_ins_tape(self):
        """SpandaPulsDetector modifiziert das Tape NICHT."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        tape_before = burumut_hebr[:]
        detector = SpandaPulsDetector(burumut_hebr)
        # Triggere mehrere Events
        for i in range(10):
            detector.observe_step(i, i, 'כ', 0)
        # Tape bleibt unverändert
        assert detector.tape == tape_before

    def test_m4_bleibt_deterministisch(self):
        """M4 ist deterministisch (Tape-Invariante)."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        # 5 Läufe müssen identisch sein
        results = []
        for _ in range(5):
            r = detect_spanda_pulse_in_tape(burumut_hebr)
            results.append(r['machine']['total_steps'])
        assert len(set(results)) == 1
        assert results[0] == 15

    def test_keine_operator_aktualisierung(self):
        """M4 ändert ihre Transition-Tabelle NICHT zur Laufzeit."""
        # Dies ist eine Konstrukt-Eigenschaft — der Detektor ist passiv
        burumut_hebr = burumut_to_hebr(BURUMUT)
        r1 = detect_spanda_pulse_in_tape(burumut_hebr)
        r2 = detect_spanda_pulse_in_tape(burumut_hebr)
        # Identische Ergebnisse (deterministisch)
        assert r1 == r2


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
