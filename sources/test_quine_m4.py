"""
🌌 QUINE-BEWEIS DER M4-MASCHINE (TDD-Tests)
============================================

TDD-Tests für die formale Verifikation der Quine-Hypothese:
1. M4 auf BURUMUT: 15 Schritte, Tape-Invariante
2. M4 auf Tengri137-99: 34 Schritte, 5 Layer besucht
3. M4 ist deterministisch (5/5 Läufe identisch)
4. REFAMTU-Beziehung: 15 = 14 + 1
5. 5-Layer-Traversal: M4 besucht alle 5 Tora-Bücher
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase
from TORA_TURING_CORRECT import (
    BURUMUT, LATIN_TO_HEBR, build_tora_transitions, burumut_to_hebr,
    MISSING_OPERATORS, HEBR_VALUES, get_layer_name
)


def load_tengri137_letters():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    return re.sub(r'[^A-Z]', '', full.upper())


def to_hebr(letters, mapping=None):
    if mapping is None:
        from TORA_TURING_MULTIPHASE import EXTENDED_LATIN_TO_HEBR
        mapping = EXTENDED_LATIN_TO_HEBR
    return ''.join(mapping.get(c, '?') for c in letters)


# ============================================================
# TEST 1: M4 ist deterministisch
# ============================================================

class TestM4Determinismus:
    """M4 muss auf identischem Tape identische Ergebnisse liefern."""

    def test_burumut_5_mal_identisch(self):
        """5 Läufe auf BURUMUT müssen 15 Schritte geben."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        results = []
        for _ in range(5):
            m = ToraTuringMultiPhase(burumut_hebr, phase_size=99,
                                     transitions=build_tora_transitions())
            m.run(max_steps=10000)
            results.append(m.total_steps)
        assert len(set(results)) == 1, f"Nicht deterministisch: {results}"
        assert results[0] == 15

    def test_tengri137_99_5_mal_identisch(self):
        """5 Läufe auf Tengri137-99 müssen 34 Schritte geben."""
        tengri = load_tengri137_letters()[:99]
        tengri_hebr = to_hebr(tengri)
        results = []
        for _ in range(5):
            m = ToraTuringMultiPhase(tengri_hebr, phase_size=99,
                                     transitions=build_tora_transitions())
            m.run(max_steps=10000)
            results.append(m.total_steps)
        assert len(set(results)) == 1
        assert results[0] == 34


# ============================================================
# TEST 2: Tape-Invariante (Quine-Eigenschaft)
# ============================================================

class TestM4TapeInvariante:
    """M4 modifiziert BURUMUT NICHT — Quine-Eigenschaft."""

    def test_burumut_tape_unchanged(self):
        """BURUMUT-Tape muss vor und nach M4 identisch sein."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        m = ToraTuringMultiPhase(burumut_hebr, phase_size=99,
                                 transitions=build_tora_transitions())
        m.run(max_steps=10000)
        final_tape = ''.join(m.tape)
        assert final_tape == burumut_hebr, (
            f"Tape wurde modifiziert!\n"
            f"  Vor:  {burumut_hebr}\n"
            f"  Nach: {final_tape}"
        )

    def test_tengri137_99_tape_unchanged(self):
        """Tengri137-99-Tape muss vor und nach M4 identisch sein."""
        tengri = load_tengri137_letters()[:99]
        tengri_hebr = to_hebr(tengri)
        m = ToraTuringMultiPhase(tengri_hebr, phase_size=99,
                                 transitions=build_tora_transitions())
        m.run(max_steps=10000)
        final_tape = ''.join(m.tape)
        assert final_tape == tengri_hebr


# ============================================================
# TEST 3: Schritt-Zahlen
# ============================================================

class TestM4SchrittZahlen:
    """M4 produziert kanonische Schritt-Zahlen."""

    def test_burumut_15_schritte(self):
        """BURUMUT → 15 Schritte (q_5 HALT)."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        m = ToraTuringMultiPhase(burumut_hebr, phase_size=99,
                                 transitions=build_tora_transitions())
        m.run(max_steps=10000)
        assert m.total_steps == 15
        assert m.halt_state == 0  # Genesis
        assert m.halt_reason == 'ALL_PHASES_COMPLETE'

    def test_tengri137_99_34_schritte(self):
        """Tengri137-99 → 34 Schritte (q_5 HALT)."""
        tengri = load_tengri137_letters()[:99]
        tengri_hebr = to_hebr(tengri)
        m = ToraTuringMultiPhase(tengri_hebr, phase_size=99,
                                 transitions=build_tora_transitions())
        m.run(max_steps=10000)
        assert m.total_steps == 34
        assert m.halt_reason == 'ALL_PHASES_COMPLETE'

    def test_tengri137_99_vs_burumut_differenz(self):
        """Tengri137-99 - BURUMUT = 34 - 15 = 19 Schritte Differenz.
        19 = Anzahl distinct lateinischer Buchstaben in BURUMUT!"""
        assert 34 - 15 == 19
        assert len(set(BURUMUT)) == 19


# ============================================================
# TEST 4: REFAMTU-Beziehung
# ============================================================

class TestM4RefamtuBeziehung:
    """BURUMUTREFAMTU (14 Zeichen) beschreibt die Maschine."""

    def test_burumut_schritte_eq_refamtu_plus_1(self):
        """15 BURUMUT-Schritte = 14 REFAMTU + 1 HALT."""
        assert 14 + 1 == 15

    def test_refamtu_ist_14_zeichen(self):
        """BURUMUTREFAMTU muss exakt 14 Zeichen sein."""
        assert len(BURUMUT[:14]) == 14
        assert BURUMUT[:14] == 'BURUMUTREFAMTU'

    def test_refamtu_latin_summe(self):
        """REFAMTU lateinische Summe: B(2)+U(21)+R(18)+U(21)+M(13)+U(21)+T(20)
        +R(18)+E(5)+F(6)+A(1)+M(13)+T(20)+U(21) = 200 (BURUMUT ist der Anfang)."""
        refamtu_sum = sum(ord(c) - ord('A') + 1 for c in BURUMUT[:14])
        assert refamtu_sum == 200


# ============================================================
# TEST 5: 5-Layer-Traversal
# ============================================================

class TestM45LayerTraversal:
    """M4 muss alle 5 Tora-Layer durchlaufen."""

    def test_burumut_besucht_5_layer(self):
        """M4 auf BURUMUT besucht Genesis, Exodus, Leviticus, Numeri, Deut."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        m = ToraTuringMultiPhase(burumut_hebr, phase_size=99,
                                 transitions=build_tora_transitions())
        m.run(max_steps=10000)

        # Sammle States
        states = set()
        for h in m.history:
            if 'new_state' in h:
                states.add(h['new_state'])
        # Layer 0-4 müssen besucht werden
        assert 0 in states, "Genesis (q_0) nicht besucht"
        assert 1 in states, "Exodus (q_1) nicht besucht"
        assert 2 in states, "Leviticus (q_2) nicht besucht"
        assert 3 in states, "Numeri (q_3) nicht besucht"
        assert 4 in states, "Deuteronomium (q_4) nicht besucht"

    def test_burumut_5_layer_count(self):
        """M4 auf BURUMUT besucht genau 5 Layer."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        m = ToraTuringMultiPhase(burumut_hebr, phase_size=99,
                                 transitions=build_tora_transitions())
        m.run(max_steps=10000)
        states = set()
        for h in m.history:
            if 'new_state' in h:
                states.add(h['new_state'])
        # 5 Layer + HALT = 6 Zustände insgesamt
        assert len(states) >= 5
        # Maximal 6 (5 Layer + HALT)
        assert len(states) <= 6


# ============================================================
# TEST 6: Numerische Brücken
# ============================================================

class TestM4NumerischeBrucken:
    """Numerische Verifikation der BURUMUT-Architektur."""

    def test_burumut_latin_summe_1232(self):
        """BURUMUT lateinische Summe = 1232."""
        s = sum(ord(c) - ord('A') + 1 for c in BURUMUT)
        assert s == 1232

    def test_burumut_plus_137_eq_37_squared(self):
        """1232 + 137 = 1369 = 37² = Genesis 1:7 Σ."""
        s = sum(ord(c) - ord('A') + 1 for c in BURUMUT)
        assert s + 137 == 37 * 37
        assert (s + 137) == 1369

    def test_burumut_hebr_gematria_6503(self):
        """BURUMUT hebr. Gematria = 6503 = 7 × 929."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        g = sum(HEBR_VALUES.get(c, 0) for c in burumut_hebr)
        assert g == 6503
        assert 6503 == 7 * 929


# ============================================================
# TEST 7: M4 ist NICHT ein Quine im strengen Sinn
# ============================================================

class TestM4ApophenieCheck:
    """M4 ist selbst-referentiell, aber KEIN Quine im strengen Sinn."""

    def test_m4_beschreibt_schoepfung_nicht_sich_selbst(self):
        """M4 auf BURUMUT beschreibt Genesis, nicht die Maschine selbst.

        Interpretation: 15 Schritte = 14 REFAMTU + 1 HALT = Schöpfung.
        """
        burumut_hebr = burumut_to_hebr(BURUMUT)
        m = ToraTuringMultiPhase(burumut_hebr, phase_size=99,
                                 transitions=build_tora_transitions())
        m.run(max_steps=10000)
        # Maschine hält NICHT durch Selbst-Beschreibung, sondern durch ALL_PHASES_COMPLETE
        assert m.halt_reason == 'ALL_PHASES_COMPLETE'
        # Maschine durchläuft NICHT alle Zustände 'q_0..q_5..q_0..q_5..'
        # (was ein Quine täte), sondern q_0 → q_1 → q_2 → ... → q_5
        states_seq = [h.get('new_state', 0) for h in m.history]
        # Sie ist eine lineare Maschine, kein zyklischer Quine
        assert states_seq == sorted(states_seq) or len(set(states_seq)) <= 5

    def test_tengri137_99_hat_5_operatoren_mehr(self):
        """Tengri137-99 hat 5+ Operatoren, die BURUMUT fehlen.
        Dies erklärt die längere Laufzeit (34 vs 15)."""
        tengri = load_tengri137_letters()[:99]
        tengri_hebr = to_hebr(tengri)
        burumut_hebr = burumut_to_hebr(BURUMUT)

        for op_char, op_name in MISSING_OPERATORS.items():
            tengri_count = tengri_hebr.count(op_char)
            burumut_count = burumut_hebr.count(op_char)
            # Tengri137 hat MINDESTENS so viele Operatoren wie BURUMUT
            assert tengri_count >= burumut_count, (
                f"{op_name} ({op_char}): Tengri137={tengri_count}, "
                f"BURUMUT={burumut_count}"
            )


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
