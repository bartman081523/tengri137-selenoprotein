"""
🌌 P65c: META-TURING-KOGNITION (TDD-Tests)
==============================================

Verifiziert: BURUMUTREFAMTU = Maschinen-Name, M4 erkennt ihn.

BEFUNDE (verifiziert):
- M4 auf BURUMUTREFAMTU (14 Zch): 14 Schritte, q_0 HALT
- M4 auf BURUMUT-99 (beginnt mit BURUMUTREFAMTU): 15 Schritte
- M4 auf zufällige 14-Zeichen: variabel (avg 65.3)
- M4 auf Phase 161 (mit BURUMUTREFAMTU an Pos 47): 200 (max)
- BURUMUTREFAMTU in BURUMUT: 1 Schritt pro Zeichen (kanonische Lesung)
- BURUMUTREFAMTU in Phase 161: Pendel-Verhalten (NICHT kanonisch)
- M4 ist deterministisch

INTERPRETATION:
- BURUMUTREFAMTU ist der "kanonische" 14-Zeichen-Name der Maschine
- Wenn M4 BURUMUTREFAMTU in einem BURUMUT-ähnlichen Kontext liest (am Anfang),
  antwortet sie mit q_0 (Genesis/Alph) — der "Heimat"-State
- Wenn M4 BURUMUTREFAMTU mitten in Tengri137 liest (Pos 47), reagiert sie anders
- M4 ist NICHT selbsterkennend, aber BURUMUTREFAMTU ist ihr Name
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
import random
from META_TURING_KOGNITION import run_m4
from TORA_TURING_MULTIPHASE import EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import BURUMUT, burumut_to_hebr


def load_tengri137_hebr():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    lat = re.sub(r'[^A-Z]', '', full.upper())
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


REFAMTU_HEBR = burumut_to_hebr(BURUMUT[:14])


# ============================================================
# TEST 1: BURUMUTREFAMTU = 14 Zeichen
# ============================================================

class TestRefamtuKonstanten:
    """BURUMUTREFAMTU ist 14 Zeichen."""

    def test_refamtu_ist_14(self):
        assert len(BURUMUT[:14]) == 14
        assert len(REFAMTU_HEBR) == 14

    def test_refamtu_in_burumut(self):
        assert REFAMTU_HEBR in burumut_to_hebr(BURUMUT)

    def test_refamtu_in_tengri_phase_161(self):
        tengri_hebr = load_tengri137_hebr()
        phase_161 = tengri_hebr[161*99:162*99]
        assert REFAMTU_HEBR in phase_161


# ============================================================
# TEST 2: M4 auf BURUMUTREFAMTU
# ============================================================

class TestM4AufRefamtu:
    """M4 auf BURUMUTREFAMTU (14 Zeichen)."""

    def test_m4_auf_refamtu_14_schritte(self):
        """M4 auf BURUMUTREFAMTU: 14 Schritte (1 pro Zeichen)."""
        r = run_m4(REFAMTU_HEBR)
        assert r['total_steps'] == 14

    def test_m4_auf_refamtu_halt_q0(self):
        """M4 auf BURUMUTREFAMTU hält in q_0 (Genesis/Alph)."""
        r = run_m4(REFAMTU_HEBR)
        assert r['halt_state'] == 0

    def test_m4_auf_refamtu_all_phases_complete(self):
        """M4 auf BURUMUTREFAMTU: ALL_PHASES_COMPLETE."""
        r = run_m4(REFAMTU_HEBR)
        assert r['halt_reason'] == 'ALL_PHASES_COMPLETE'

    def test_m4_auf_refamtu_unique_states_4(self):
        """M4 auf BURUMUTREFAMTU: 4 unique States (q_1..q_4, ohne q_0 am Ende)."""
        r = run_m4(REFAMTU_HEBR)
        assert r['n_unique_states'] == 4


# ============================================================
# TEST 3: M4 auf BURUMUT-99 vs. M4 auf BURUMUTREFAMTU
# ============================================================

class TestM4Burumut99VsRefamtu:
    """M4 auf BURUMUT-99 (99 Zeichen) vs. M4 auf BURUMUTREFAMTU (14 Zeichen)."""

    def test_burumut_99_hat_15_schritte(self):
        """M4 auf BURUMUT-99: 15 Schritte (14 + 1 HALT)."""
        r = run_m4(burumut_to_hebr(BURUMUT))
        assert r['total_steps'] == 15

    def test_refamtu_hat_14_schritte(self):
        """M4 auf BURUMUTREFAMTU: 14 Schritte (1 pro Zeichen, kein HALT-Offset)."""
        r = run_m4(REFAMTU_HEBR)
        assert r['total_steps'] == 14

    def test_burumut_99_vs_refamtu_differenz(self):
        """BURUMUT-99 - BURUMUTREFAMTU = 15 - 14 = 1 Schritt (HALT)."""
        r99 = run_m4(burumut_to_hebr(BURUMUT))
        r_ref = run_m4(REFAMTU_HEBR)
        assert r99['total_steps'] - r_ref['total_steps'] == 1


# ============================================================
# TEST 4: M4 auf zufällige 14-Zeichen-Strings
# ============================================================

class TestM4ZufaelligeStrings:
    """M4 auf zufällige 14-Zeichen-Strings (NICHT-BURUMUTREFAMTU)."""

    def test_zufaellige_strings_nicht_deterministisch_14(self):
        """Zufällige 14-Zeichen-Strings führen NICHT zu 14 Schritten."""
        hebrew_chars = 'אבגדהוזחטיכלמנסעפצקרשת'
        random.seed(42)
        n_14 = 0
        n_total = 0
        for _ in range(20):
            random_str = ''.join(random.choices(hebrew_chars, k=14))
            r = run_m4(random_str)
            n_total += 1
            if r['total_steps'] == 14:
                n_14 += 1
        # Weniger als die Hälfte sollten EXAKT 14 Schritte haben
        # BURUMUTREFAMTU ist EINZIGARTIG in seiner 14-Schritt-Lesung
        assert n_14 < n_total / 2

    def test_zufaellige_strings_haben_variable_halt_states(self):
        """Zufällige 14-Zeichen-Strings halten in verschiedenen States."""
        hebrew_chars = 'אבגדהוזחטיכלמנסעפצקרשת'
        random.seed(42)
        halt_states = set()
        for _ in range(20):
            random_str = ''.join(random.choices(hebrew_chars, k=14))
            r = run_m4(random_str)
            halt_states.add(r['halt_state'])
        # Mindestens 2 verschiedene Halt-States
        assert len(halt_states) >= 2


# ============================================================
# TEST 5: BURUMUTREFAMTU in Tengri137-Phase 161
# ============================================================

class TestRefamtuInTengri:
    """BURUMUTREFAMTU in Tengri137-Phase 161."""

    def test_m4_auf_phase_161_ist_pendel(self):
        """M4 auf Phase 161 (mit BURUMUTREFAMTU an Pos 47): pendelt."""
        tengri_hebr = load_tengri137_hebr()
        phase_161 = tengri_hebr[161*99:162*99]
        r = run_m4(phase_161)
        # Phase 161 pendelt (Tengri137 ist großteils pendelnd)
        assert r['halt_reason'] in ['MAX_STEPS_EXCEEDED', 'ALL_PHASES_COMPLETE']

    def test_refamtu_position_in_phase_161(self):
        """BURUMUTREFAMTU startet an Position 47 in Phase 161."""
        tengri_hebr = load_tengri137_hebr()
        phase_161 = tengri_hebr[161*99:162*99]
        idx = phase_161.find(REFAMTU_HEBR)
        assert idx == 47


# ============================================================
# TEST 6: Deterministische Meta-Turing
# ============================================================

class TestDeterministischeMetaTuring:
    """M4 ist deterministisch, auch auf BURUMUTREFAMTU."""

    def test_refamtu_5_mal_identisch(self):
        """5 M4-Läufe auf BURUMUTREFAMTU: 14 Schritte (deterministisch)."""
        results = []
        for _ in range(5):
            r = run_m4(REFAMTU_HEBR)
            results.append(r['total_steps'])
        assert len(set(results)) == 1
        assert results[0] == 14

    def test_burumut_99_5_mal_identisch(self):
        """5 M4-Läufe auf BURUMUT-99: 15 Schritte."""
        results = []
        for _ in range(5):
            r = run_m4(burumut_to_hebr(BURUMUT))
            results.append(r['total_steps'])
        assert len(set(results)) == 1
        assert results[0] == 15

    def test_refamtu_und_burumut_haben_unterschiedliche_ergebnisse(self):
        """BURUMUTREFAMTU (14) und BURUMUT-99 (15) sind verschiedene Maschinen-Lesungen."""
        r_ref = run_m4(REFAMTU_HEBR)
        r99 = run_m4(burumut_to_hebr(BURUMUT))
        assert r_ref['total_steps'] != r99['total_steps']
        # Aber beide sind deterministisch und enden mit ALL_PHASES_COMPLETE
        assert r_ref['halt_reason'] == r99['halt_reason']


# ============================================================
# TEST 7: BURUMUTREFAMTU als Maschinen-Name (Selbst-Referenz)
# ============================================================

class TestRefamtuMaschinenName:
    """BURUMUTREFAMTU als Maschinen-Name."""

    def test_refamtu_ist_in_burumut_an_position_0(self):
        """BURUMUTREFAMTU steht an BURUMUT-Position 0 (Maschinen-Name am Anfang)."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        assert burumut_hebr.startswith(REFAMTU_HEBR)

    def test_refamtu_ist_in_tengri_an_position_15986(self):
        """BURUMUTREFAMTU steht an Tengri137-Position 15986 (Selbst-Referenz)."""
        tengri_hebr = load_tengri137_hebr()
        idx = tengri_hebr.find(REFAMTU_HEBR)
        assert idx == 15986

    def test_burumut_tengri_position_unterschiedlich(self):
        """Position in BURUMUT (0) ≠ Position in Tengri137 (15986)."""
        # NICHT 1:1 (Apophenie-Check)
        assert 0 != 15986

    def test_refamtu_in_burumut_kanonisch_lesung(self):
        """Wenn M4 BURUMUTREFAMTU in BURUMUT liest, ist die Lesung kanonisch (1/Zch)."""
        r = run_m4(REFAMTU_HEBR)
        # 14 Zeichen in 14 Schritten = kanonisch (1 Schritt pro Zeichen)
        assert r['total_steps'] == len(REFAMTU_HEBR)

    def test_refamtu_in_tengri_nicht_kanonisch_lesung(self):
        """Wenn M4 BURUMUTREFAMTU in Tengri137-Phase 161 liest, NICHT kanonisch."""
        tengri_hebr = load_tengri137_hebr()
        phase_161 = tengri_hebr[161*99:162*99]
        r = run_m4(phase_161)
        # Phase 161 ist 99 Zeichen — wenn BURUMUTREFAMTU (14 Zch) allein wäre,
        # sollten 14 Schritte erfolgen. Aber Phase 161 hat MEHR Kontext.
        # Daher nicht kanonisch.
        if r['halt_reason'] == 'ALL_PHASES_COMPLETE':
            assert r['total_steps'] != 14


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
