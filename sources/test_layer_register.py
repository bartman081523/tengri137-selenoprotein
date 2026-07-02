"""
🌟 5-LAYER-REGISTER IN DER TORA-TURING-MASCHINE
================================================

FRAGE (User 2026-07-01):
> "hatten wir eigentlich die 5 Layer der Torah als Register in der
> ToraTorusTuringMaschine?"

ANTWORT: NEIN — die 5 Layer sind nur als q_0..q_4 (Zustandszahlen)
hardcoded. Es gibt keine zentrale Register-Datenstruktur mit Namen.

DIESER TEST:
1. Verifiziert, dass die 5 Layer als REGISTER existieren
2. Jeder Zustand q_i hat einen Namen (Genesis, Exodus, ...)
3. Das Register kann abgefragt werden
4. Die Übergangs-Tabelle respektiert die Register-Namen

Die 5 Layer:
  q_0 = Genesis (Schöpfung)
  q_1 = Exodus (Befreiung)
  q_2 = Leviticus (Ordnung)
  q_3 = Numeri (Wüstenwanderung)
  q_4 = Deuteronomium (Vollendung)
  q_5 = HALT (Sabbat / Vollendung der Schrift)

BURUMUT-Architektur:
  5 Layer = 5 Bücher Mose
  + 1 HALT-Layer = Sabbat
  = 6 Zustände insgesamt
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
from TORA_TURING_CORRECT import (
    build_tora_transitions, ToraTuringMachine, BURUMUT, burumut_to_hebr
)
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase


# =====================================================================
# ERWARTETE 5-LAYER-REGISTER
# =====================================================================

EXPECTED_LAYERS = [
    # (state, name, hebrew_anchor, symbol, book, content)
    (0, 'Genesis',       'א', Aleph := 1, 'Genesis',       'Schöpfung'),
    (1, 'Exodus',        'ש', 21,         'Exodus',        'Befreiung (Shem)'),
    (2, 'Leviticus',     'ת', 400,        'Leviticus',     'Ordnung (Tav)'),
    (3, 'Numeri',        'ר', 200,        'Numbers',       'Wüstenwanderung (Rosh)'),
    (4, 'Deuteronomium', 'נ', 50,         'Deuteronomy',   'Vollendung (Nun)'),
    (5, 'HALT',          'ת', 400,        None,            'Sabbat / Vollendung'),
]


class TestLayerRegisterExistenz:
    """Prüfe, ob die 5 Layer als REGISTER existieren."""

    def test_layer_register_konstante_vorhanden(self):
        """Es MUSS eine LAYER_REGISTER-Konstante geben."""
        from TORA_TURING_CORRECT import LAYER_REGISTER
        assert LAYER_REGISTER is not None
        assert len(LAYER_REGISTER) == 6  # 5 Layer + HALT

    def test_layer_register_hat_5_layer_plus_halt(self):
        """LAYER_REGISTER hat 5 Layer + HALT = 6 Einträge."""
        from TORA_TURING_CORRECT import LAYER_REGISTER
        assert len(LAYER_REGISTER) == 6

    def test_layer_q0_ist_genesis(self):
        """q_0 = Genesis (Schöpfung)."""
        from TORA_TURING_CORRECT import LAYER_REGISTER
        layer = LAYER_REGISTER[0]
        assert layer['name'] == 'Genesis'
        assert layer['book'] == 'Genesis'

    def test_layer_q1_ist_exodus(self):
        """q_1 = Exodus (Befreiung)."""
        from TORA_TURING_CORRECT import LAYER_REGISTER
        layer = LAYER_REGISTER[1]
        assert layer['name'] == 'Exodus'

    def test_layer_q2_ist_leviticus(self):
        """q_2 = Leviticus (Ordnung)."""
        from TORA_TURING_CORRECT import LAYER_REGISTER
        layer = LAYER_REGISTER[2]
        assert layer['name'] == 'Leviticus'

    def test_layer_q3_ist_numeri(self):
        """q_3 = Numeri (Wüstenwanderung)."""
        from TORA_TURING_CORRECT import LAYER_REGISTER
        layer = LAYER_REGISTER[3]
        assert layer['name'] == 'Numeri'

    def test_layer_q4_ist_deuteronomium(self):
        """q_4 = Deuteronomium (Vollendung)."""
        from TORA_TURING_CORRECT import LAYER_REGISTER
        layer = LAYER_REGISTER[4]
        assert layer['name'] == 'Deuteronomium'

    def test_layer_q5_ist_halt(self):
        """q_5 = HALT (Sabbat/Vollendung)."""
        from TORA_TURING_CORRECT import LAYER_REGISTER
        layer = LAYER_REGISTER[5]
        assert layer['name'] == 'HALT'
        assert layer['book'] is None  # Kein Buch, sondern HALT-Zustand

    def test_jeder_layer_hat_hebr_anker(self):
        """Jeder Layer hat einen hebräischen Anker-Konsonanten."""
        from TORA_TURING_CORRECT import LAYER_REGISTER
        for layer in LAYER_REGISTER:
            assert 'hebrew_anchor' in layer, f"{layer['name']} fehlt hebrew_anchor"
            assert layer['hebrew_anchor'] in 'אבגדהוזחטיכלמנסעפצקרשת'

    def test_jeder_layer_hat_gematria(self):
        """Jeder Layer hat eine Gematria für den Anker."""
        from TORA_TURING_CORRECT import LAYER_REGISTER
        for layer in LAYER_REGISTER:
            assert 'gematria' in layer
            assert layer['gematria'] > 0

    def test_register_5_layer_struktur(self):
        """Die 5 Layer folgen der 5-Bücher-Struktur der Tora."""
        from TORA_TURING_CORRECT import LAYER_REGISTER
        assert LAYER_REGISTER[0]['book'] == 'Genesis'
        assert LAYER_REGISTER[1]['book'] == 'Exodus'
        assert LAYER_REGISTER[2]['book'] == 'Leviticus'
        assert LAYER_REGISTER[3]['book'] == 'Numbers'
        assert LAYER_REGISTER[4]['book'] == 'Deuteronomy'


class TestLayerRegisterMitMaschine:
    """Das Register muss mit der Maschine funktionieren."""

    def test_maschine_hat_layer_register(self):
        """ToraTuringMachine hat ein LAYER_REGISTER."""
        from TORA_TURING_CORRECT import ToraTuringMachine
        hebr = burumut_to_hebr(BURUMUT)
        m = ToraTuringMachine(hebr)
        assert hasattr(m, 'layer_register')
        assert len(m.layer_register) == 6

    def test_maschine_genesis_anfang(self):
        """Maschine startet in q_0 = Genesis (initial state)."""
        from TORA_TURING_CORRECT import ToraTuringMachine
        hebr = burumut_to_hebr(BURUMUT)
        m = ToraTuringMachine(hebr)
        # Vor dem Lauf: state == 0 = Genesis
        assert m.state == 0
        assert m.state_to_layer() == 'Genesis'
        assert m.current_layer()['name'] == 'Genesis'
        # Nach dem Lauf: state kann HALT (5) sein, wenn BURUMUT Aleph enthält
        m.run(max_steps=100)
        # Aber das Layer-Register bleibt 6 Einträge
        assert len(m.layer_register) == 6

    def test_maschine_state_zu_layer_name(self):
        """state_to_layer() konvertiert state zu Layer-Name."""
        from TORA_TURING_CORRECT import ToraTuringMachine
        hebr = burumut_to_hebr(BURUMUT)
        m = ToraTuringMachine(hebr)
        # m.state_to_layer() muss existieren
        assert hasattr(m, 'state_to_layer')
        assert m.state_to_layer(0) == 'Genesis'
        assert m.state_to_layer(1) == 'Exodus'
        assert m.state_to_layer(2) == 'Leviticus'
        assert m.state_to_layer(3) == 'Numeri'
        assert m.state_to_layer(4) == 'Deuteronomium'
        assert m.state_to_layer(5) == 'HALT'

    def test_multiphase_hat_layer_register(self):
        """ToraTuringMultiPhase hat LAYER_REGISTER."""
        from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase
        m = ToraTuringMultiPhase(burumut_to_hebr(BURUMUT), phase_size=99)
        assert hasattr(m, 'layer_register')
        assert len(m.layer_register) == 6


class TestLayerUebergaenge:
    """Die Übergänge folgen der 5-Layer-Architektur."""

    def test_q0_zu_q1_ist_genesis_zu_exodus(self):
        """Übergang q_0 → q_1 ist Genesis → Exodus."""
        transitions = build_tora_transitions()
        # Finde einen Übergang q_0 → q_1
        for (state, sym), (new_state, _, _) in transitions.items():
            if state == 0 and new_state == 1:
                # Symbol das Genesis zu Exodus macht
                assert sym in 'בגדהוזחטיכלמנסעפצקרשת'
                break

    def test_q2_zu_q3_ist_leviticus_zu_numeri(self):
        """Übergang q_2 → q_3 ist Leviticus → Numeri (Aleph)."""
        transitions = build_tora_transitions()
        # Aleph in q_2 muss zu q_3 führen
        assert transitions[(2, 'א')] == (3, 'א', 'MOVE_RIGHT')

    def test_q3_zu_q4_ist_numeri_zu_deuteronomium(self):
        """Übergang q_3 → q_4 ist Numeri → Deuteronomium (Resh)."""
        transitions = build_tora_transitions()
        # Resh in q_3 muss zu q_4 führen
        assert transitions[(3, 'ר')] == (4, 'ר', 'MOVE_RIGHT')

    def test_q4_zu_q5_ist_deuteronomium_zu_halt(self):
        """Übergang q_4 → q_5 ist Deuteronomium → HALT (Nun)."""
        transitions = build_tora_transitions()
        # Nun in q_4 muss zu q_5 (HALT) führen
        assert transitions[(4, 'נ')] == (5, 'נ', 'HALT')


class TestLayerArchitektur:
    """5-Layer-Architektur als BURUMUT-Spiegelung."""

    def test_5_layer_5_buecher_mose(self):
        """5 Layer = 5 Bücher Mose."""
        from TORA_TURING_CORRECT import LAYER_REGISTER
        books = [l['book'] for l in LAYER_REGISTER if l['book']]
        assert books == ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy']

    def test_5_layer_plus_halt_6_zustaende(self):
        """5 Layer + HALT = 6 Maschinen-Zustände (q_0..q_5)."""
        from TORA_TURING_CORRECT import LAYER_REGISTER
        assert len(LAYER_REGISTER) == 6

    def test_187_kapitel_5_layer_architektur(self):
        """187 = 11 × 17 — 5-Layer-Architektur."""
        # 50+40+27+36+34 = 187
        total = 50 + 40 + 27 + 36 + 34
        assert total == 187
        # 187 = 11 × 17
        assert 187 == 11 * 17

    def test_layer_5_buecher_kapitelanzahl(self):
        """Jedes Layer-Buch hat seine kanonische Kapitel-Anzahl."""
        from TORA_TURING_CORRECT import LAYER_REGISTER
        expected = {
            'Genesis': 50,
            'Exodus': 40,
            'Leviticus': 27,
            'Numbers': 36,
            'Deuteronomy': 34,
        }
        for layer in LAYER_REGISTER:
            if layer['book']:
                assert layer['chapters'] == expected[layer['book']]


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
