"""
🌌 TDD-TESTS FÜR SPANDA-MASCHINE
=================================

Test-First-Approach: Jede Beobachtung wird ein Test.
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
from pathlib import Path
from SPANDA_MACHINE import (
    BaseTruth, SpandaMachine, HaltInterpreter,
    ExpansionEngine, BacktrackingDebugger,
)
from TORA_TURING_CORRECT import HEBR_VALUES, LATIN_TO_HEBR
from TORA_TURING_MULTIPHASE import EXTENDED_LATIN_TO_HEBR


class TestBaseTruth:
    """Tests für die unveränderliche Basis-Wahrheit."""

    def test_base_truth_loads(self):
        """BaseTruth lädt die Full Notes."""
        base = BaseTruth()
        assert base.size > 40000  # 42246
        assert base.lines == 1167

    def test_base_truth_extracts_letters(self):
        """BaseTruth extrahiert 12071 lateinische A-Z-Buchstaben."""
        base = BaseTruth()
        assert len(base.letters) == 12071
        assert len(base.position_map) == 12071
        # Nur A-Z
        assert all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' for c in base.letters)

    def test_base_truth_hebrew_length(self):
        """Hebräische Konvertierung hat gleiche Länge."""
        base = BaseTruth()
        assert base.hebr_length == 12071
        # Keine unbekannten Zeichen
        assert base.hebr.count('?') == 0

    def test_base_truth_fingerprint_stable(self):
        """SHA-256 Fingerabdruck ist deterministisch."""
        b1 = BaseTruth()
        b2 = BaseTruth()
        assert b1.fingerprint == b2.fingerprint

    def test_halt_to_context_maps_correctly(self):
        """Mappe Maschinen-Position zurück auf Original-Text."""
        base = BaseTruth()
        # BURUMUT-Prefix an Tape-Index 11740 — das ist in der BURUMUT-99-Sektion
        # "B U R U M U T R E F A M T U ..." (mit Spaces)
        ctx = base.halt_to_context(11740)
        assert ctx is not None
        # Im Full Notes-Original hat BURUMUT Spaces zwischen den Buchstaben
        ctx_stripped = re.sub(r'\s+', '', ctx['context'].upper())
        # Entweder direkt "BURUMUT" oder space-stripped "BURUMUT"
        assert 'BURUMUT' in ctx['context'].upper() or 'BURUMUT' in ctx_stripped

    def test_context_at_position_bounds(self):
        """Kontext-Anfrage am Anfang und Ende."""
        base = BaseTruth()
        # Anfang
        ctx0 = base.halt_to_context(0)
        assert ctx0 is not None
        # Ende
        ctx_last = base.halt_to_context(12070)
        assert ctx_last is not None


class TestSpandaMachine:
    """Tests für die Spanda-Maschine."""

    def test_machine_has_132_transitions(self):
        """22 Konsonanten × 6 Zustände = 132 Transitionen."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        assert spanda.n_transitions == 132
        assert spanda.n_states == 6
        assert spanda.n_symbols == 22

    def test_machine_runs_to_end(self):
        """Maschine hält am Tape-Ende (nicht mitten drin)."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        result = spanda.run_full()
        assert result['halt_reason'] == 'TAPE_END'
        assert result['final_head'] == len(base.hebr)

    def test_machine_has_122_phases(self):
        """12071 / 99 = 121.9... → 122 Phasen."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        result = spanda.run_full()
        assert result['n_phases'] == 122

    def test_machine_has_122_halts(self):
        """Genau 122 Halt-Punkte (einer pro Phase)."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        result = spanda.run_full()
        assert len(result['phase_halts']) == 122

    def test_final_state_is_q5(self):
        """Maschine endet in q_5 (HALT)."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        result = spanda.run_full()
        assert result['final_state'] == 5


class TestHaltInterpreter:
    """Tests für den Halt-Interpreter."""

    def test_interpreter_finds_key_phrases(self):
        """Mindestens 100 der 122 Halts matchen Key-Phrasen."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        result = spanda.run_full()
        interpreter = HaltInterpreter()
        interps = interpreter.interpret_all(base, result)
        with_matches = [i for i in interps if i['key_matches']]
        assert len(with_matches) >= 100

    def test_interpreter_finds_time_for_truth(self):
        """Der 'TIME FOR THE TRUTH'-Halt wird gefunden."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        result = spanda.run_full()
        interpreter = HaltInterpreter()
        interps = interpreter.interpret_all(base, result)
        truth_halts = [
            i for i in interps
            if any('TIME FOR THE TRUTH' in m[0] for m in i['key_matches'])
        ]
        assert len(truth_halts) >= 1

    def test_interpreter_finds_burumut(self):
        """Der BURUMUT-Halt wird gefunden (Quine-Effekt)."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        result = spanda.run_full()
        interpreter = HaltInterpreter()
        interps = interpreter.interpret_all(base, result)
        burumut_halts = [
            i for i in interps
            if any('BURUMUT' in m[0] for m in i['key_matches'])
        ]
        assert len(burumut_halts) >= 1

    def test_interpreter_finds_genetic(self):
        """Der 'GENETICALLY ENCRYPTED'-Halt wird gefunden."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        result = spanda.run_full()
        interpreter = HaltInterpreter()
        interps = interpreter.interpret_all(base, result)
        gen_halts = [
            i for i in interps
            if any('GENETIC' in m[0] for m in i['key_matches'])
        ]
        assert len(gen_halts) >= 1

    def test_interpreter_finds_137(self):
        """Der 'ONE THREE SEVEN'-Halt wird gefunden."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        result = spanda.run_full()
        interpreter = HaltInterpreter()
        interps = interpreter.interpret_all(base, result)
        h137 = [
            i for i in interps
            if any('ONE THREE SEVEN' in m[0] for m in i['key_matches'])
        ]
        assert len(h137) >= 1


class TestExpansionEngine:
    """Tests für die Expansions-Engine."""

    def test_gematria_calculation(self):
        """Gematria einer bekannten Sequenz."""
        expander = ExpansionEngine(BaseTruth())
        # ב = 2, ש = 300, ר = 200, ה = 5 → 507
        assert expander.gematria('בשרה') == 507

    def test_gematria_latin_input(self):
        """Gematria akzeptiert lateinischen Input."""
        expander = ExpansionEngine(BaseTruth())
        # BUR → ב(2) + ש(300) + צ(90) = 392
        assert expander.gematria('BUR') == 392

    def test_expansion_proposed_letters_length(self):
        """Expansions-Vorschlag hat 14 lateinische Buchstaben."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        result = spanda.run_full()
        interpreter = HaltInterpreter()
        interps = interpreter.interpret_all(base, result)

        expander = ExpansionEngine(base)
        for interp in interps[:5]:
            if interp['key_matches']:
                exp = expander.propose_expansion(interp)
                if exp:
                    assert len(exp['proposed_letters']) <= 14
                    assert exp['proposed_gematria'] > 0


class TestBacktrackingDebugger:
    """Tests für den Backtracking-Debugger."""

    def test_checkpoint_creation(self):
        """Checkpoint kann erstellt und wiederhergestellt werden."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        spanda.step()  # initialisiere
        dbg = BacktrackingDebugger(spanda, base)
        dbg.save_checkpoint(label='test1')
        assert len(dbg.checkpoints) == 1
        assert dbg.checkpoints[0]['label'] == 'test1'

    def test_restore_changes_state(self):
        """Restore setzt Maschine auf Checkpoint zurück."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        spanda.step()
        spanda.step()
        spanda.step()
        dbg = BacktrackingDebugger(spanda, base)
        dbg.save_checkpoint(label='after_3_steps')

        original_head = spanda.machine.head
        original_state = spanda.machine.state

        spanda.step()
        spanda.step()

        dbg.restore_checkpoint()
        assert spanda.machine.head == original_head
        assert spanda.machine.state == original_state


class TestPhilosophicalArchitecture:
    """Tests für die philosophische Architektur-Konsistenz."""

    def test_vier_sprach_stadien_present(self):
        """Vāc 4-Stadien sind in der Architektur verkörpert."""
        # vaikharī = lateinisch (B, U, R...)
        # madhyamā = hebräisch (ב, ש, צ...)
        # paśyantī = gematria (1924, 6503...)
        # parā = 5 fehlende Operatoren + Halt-Punkt
        base = BaseTruth()
        # 1: vaikharī
        assert len(base.letters) > 0
        # 2: madhyamā
        assert len(base.hebr) > 0
        # 3: paśyantī
        assert sum(HEBR_VALUES.get(c, 0) for c in base.hebr) > 0
        # 4: parā (5 Operatoren — 4 in EXTENDED_LATIN_TO_HEBR, Tav via Kontext-Regel)
        ops = ['כ', 'ג', 'ד', 'י']  # 4 in EXTENDED direkt
        for op in ops:
            assert op in EXTENDED_LATIN_TO_HEBR.values(), (
                f"Operator {op} fehlt in EXTENDED_LATIN_TO_HEBR"
            )
        # Tav (ת) wird über TAV_CONTEXT-Regel aufgelöst, nicht im direkten Mapping
        # (siehe SPANDA-Maschinen-Architektur: T ist mehrdeutig Resh/Tav)

    def test_five_states_equals_torah(self):
        """5 Bücher Mose = 5 Zustände (q_0..q_4) + q_5 (Sabbat/HALT)."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        # 5+1 = 6 Zustände
        assert spanda.n_states == 6

    def test_kanonizitaet_erhalten(self):
        """Die Base-Truth bleibt unverändert."""
        b1 = BaseTruth()
        original = b1.raw
        # Versuche zu mutieren
        try:
            b1.raw = 'mutated'
        except Exception:
            pass
        # Lade neu
        b2 = BaseTruth()
        assert b2.raw == original


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
