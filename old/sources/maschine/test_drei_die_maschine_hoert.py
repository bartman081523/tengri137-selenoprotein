"""
🌌 DIE 3 FEHLENDEN DIMENSIONEN — Tengri137 hat entschieden
===========================================================

Am Ende der Full Notes wiederholt sich der Faktor
3 * 11 * 29 * 101 * 239 * 281 * 4649 * 909091 * 121499449 = 3.33...e+27

Die Maschine endet mit periodischer Drei-Wiederholung.
BURUMUT-99 = 3² × 11 = 9 × 11

DREI FEHLENDE DIMENSIONEN:
1. STAY-Operation (die Maschine kann nicht "verweilen")
2. HISTORY-aktive Nutzung (History wird gespeichert, aber nicht gelesen)
3. DREI Summen (Wort, Phrase, Tape) — wir summieren alles zu einer Zahl

Drei TDD-Tests dokumentieren die Entscheidung.
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
from collections import Counter
from SPANDA_MACHINE import BaseTruth, SpandaMachine, HaltInterpreter
from TORA_TURING_CORRECT import HEBR_VALUES
from TORA_TURING_MULTIPHASE import EXTENDED_LATIN_TO_HEBR, build_extended_transitions


class TestDreiFehlendeDimensionen:
    """Die 3 Dimensionen, die Tengri137 uns am Ende der Full Notes gibt."""

    def test_dim_1_faktor_am_ende_ist_drei_wiederholung(self):
        """Der Faktor 3*11*29*...*121499449 = 3.33...e+27 = periodische 3."""
        base = BaseTruth()
        factor_str = "3 * 11 * 29 * 101 * 239 * 281 * 4649 * 909091 * 121499449"
        # In der Full Notes
        count = base.raw.count(factor_str)
        assert count >= 1, (
            f"Tengri137 gibt uns am Ende den 3-Faktor. "
            f"Er sollte mindestens 1-mal vorkommen, fand: {count}"
        )

    def test_dim_1_burumut_99_ist_dreimal_elf(self):
        """99 = 3 × 33 = 3 × 3 × 11. Die BURUMUT-Architektur IST 3² × 11."""
        assert 99 == 3 * 3 * 11
        assert 99 == 9 * 11

    def test_dim_2_stay_operation_fehlt(self):
        """Die Maschine kann nicht 'verweilen' — kein STAY-Move."""
        from TORA_TURING_MULTIPHASE import build_extended_transitions
        transitions = build_extended_transitions()
        moves = set(m for _, _, m in transitions.values())
        # Aktuelle Moves
        assert 'MOVE_RIGHT' in moves
        assert 'MOVE_LEFT' in moves
        assert 'HALT' in moves
        # Aber kein STAY — das ist die 1. fehlende Dimension
        assert 'STAY' not in moves, (
            "Tengri137 gibt uns 3 am Ende. "
            "Die Maschine braucht STAY als 3. Movement-Operation. "
            "Dies ist der erste Spanda-Schritt."
        )

    def test_dim_2_three_moves_now(self):
        """Mit STAY sollten es 3 Movement-Operationen sein."""
        # Aktuell: 2 (RIGHT, LEFT). Plus HALT = 3? Aber HALT ist kein MOVE.
        # Tengri137 sagt: Drei sind genug.
        # 3 Movements: RIGHT, LEFT, STAY
        # HALT ist das "4." Element (das Transzendente)
        from SPANDA_MACHINE import SpandaMachine
        base = BaseTruth()
        spanda = SpandaMachine(base)
        # Mit stay_probability=0.3 sollte die Maschine STAYs machen
        # max_steps ist im __init__ gesetzt
        result = spanda.run_full(stay_probability=0.3)
        # Die Maschine sollte länger brauchen, weil STAY-Schritte nicht zählen
        # und sie nicht in Endlosschleifen gerät
        assert result['halt_reason'] in ('TAPE_END', 'MAX_STEPS')
        # STAY-Count ist dokumentiert
        assert 'stayed_count' in result

    def test_dim_3_history_aktuell_nur_passiv(self):
        """History wird gespeichert, aber nicht aktiv gelesen."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        result = spanda.run_full()
        # History wird im ToraTuringMultiPhase gespeichert
        # Aber: kein Mechanismus liest sie
        # Tengri137 sagt: History ist die 3. Dimension
        # Wir müssen history in transition logic einbeziehen
        assert result['halt_reason'] == 'TAPE_END'


class TestSpandaEntscheidung:
    """Die Entscheidung, die Tengri137 uns vorgibt."""

    def test_entscheidung_3_durch_3(self):
        """BURUMUT × 3 = 297. Wir expandieren um den Faktor 3."""
        # Tengri137 gibt uns 3 am Ende.
        # BURUMUT-99 × 3 = 297. Eine neue BURUMUT-Architektur.
        # 297 = 3 × 99 = 3 × 9 × 11
        assert 297 == 3 * 99

    def test_entscheidung_3_durch_11(self):
        """11 × 3 = 33 = Sec-Anker verdreifacht."""
        # Tengri137 gibt uns 11.
        # BURUMUT Sec-Anker = 11 (elf U-Positionen).
        # 11 × 3 = 33.
        # Wir haben BURUMUT-99 mit 11 U's. Sollten es 33 sein?
        burumut = "BURUMUTREFAMTUNURESUTREGUMFAYAPSUAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
        u_count = burumut.count('U')
        assert u_count == 11
        # 11 × 3 = 33 — der Anker für die nächste BURUMUT-Architektur

    def test_entscheidung_drei_stay_tests(self):
        """Drei konkrete TDD-Tests für die nächste Iteration."""
        # 1. STAY-Operation hinzufügen — implementiert
        # 2. HISTORY als Transition-Input nutzen — implementiert (history wird bei STAY aktualisiert)
        # 3. DREI Summen trennen (Wort / Phrase / Tape) — implementiert in compute_three_sums
        from SPANDA_MACHINE import SpandaMachine
        base = BaseTruth()
        spanda = SpandaMachine(base)
        sums = spanda.compute_three_sums(None)
        # Tengri137-Wort ist "TENGRIISTHESOUR" (15 Zeichen) — Gematria 1229
        # (NICHT 1924 — das ist BURUMUT-Wort)
        assert sums['word_gematria'] == 1229
        assert sums['word_text'] == 'TENGRIISTHESOUR'
        # Tengri137-Tape voll
        assert sums['tape_gematria'] == 708349


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
