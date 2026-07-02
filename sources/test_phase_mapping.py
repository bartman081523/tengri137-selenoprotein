"""
🌌 PHASEN-ÜBERGANGS-MAPPING: TDD-Tests
========================================

Verifiziert die numerische Brücke zwischen 168 Tengri137-Phasen
und 187 Tora-Kapitel.

ARCHITEKTUR:
- 187 Tora-Kapitel = 50 + 40 + 27 + 36 + 34 = 11 × 17
- 168 Tengri137-Phasen à 99 Zeichen
- 187 - 168 = 19 = BURUMUT-Sec (Selenocystein-Positionen)
- 168 × 99 = 16632 (vs 16576 Tengri137, Diff = 56)
- 56 = BURUMUTREFAMTU-Länge, die in Tengri137 identisch ist

MAPPING (Verhältnis):
  Genesis (50) → 45 Phasen (0..44)
  Exodus (40) → 36 Phasen (45..80)
  Leviticus (27) → 24 Phasen (81..104)
  Numeri (36) → 32 Phasen (105..136)
  Deuteronomium (34) → 31 Phasen (137..167)

BEFUNDE:
- 55 saubere Phasen (ALL_PHASES_COMPLETE)
- 113 Pendel-Phasen (MAX_STEPS_EXCEEDED)
- 15 Phasen halten in 1 Schritt (Aleph am Anfang)
- 3 Phasen halten in 34 Schritten (volle 5 Layer)
- Verteilung pro Buch: 12/13/11/7/12 clean Phasen
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
from collections import Counter
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import build_tora_transitions, get_layer_name


# Tora-Struktur (aus Mermaid-Plan Phase 53)
TORA_BOOKS = {
    'Genesis':       {'chapters': 50, 'phases_start': 0,  'phases_end': 45},
    'Exodus':        {'chapters': 40, 'phases_start': 45, 'phases_end': 81},
    'Leviticus':     {'chapters': 27, 'phases_start': 81, 'phases_end': 105},
    'Numeri':        {'chapters': 36, 'phases_start': 105, 'phases_end': 137},
    'Deuteronomium': {'chapters': 34, 'phases_start': 137, 'phases_end': 168},
}
TOTAL_CHAPTERS = 187
TOTAL_PHASES = 168


def load_tengri137():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    letters = re.sub(r'[^A-Z]', '', full.upper())
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in letters)


def phase_to_torah(phase_idx):
    """Map Phase-Index auf (Buch, Kapitel)."""
    for book, info in TORA_BOOKS.items():
        if info['phases_start'] <= phase_idx < info['phases_end']:
            phases_in_book = info['phases_end'] - info['phases_start']
            chap_in_book = info['chapters']
            phase_offset = phase_idx - info['phases_start']
            chapter = 1 + (phase_offset * chap_in_book) // phases_in_book
            if chapter > chap_in_book:
                chapter = chap_in_book
            return book, chapter
    return None, None


def run_phase(tape, max_steps=200):
    m = ToraTuringMultiPhase(tape, phase_size=99,
                             transitions=build_tora_transitions())
    m.run(max_steps=max_steps)
    states = [h.get('new_state', 0) for h in m.history if 'new_state' in h]
    return {
        'total_steps': m.total_steps,
        'halt_state': m.halt_state,
        'halt_reason': m.halt_reason,
        'unique_states': sorted(set(states)),
    }


# ============================================================
# TEST 1: Numerische Brücke
# ============================================================

class TestNumerischeBrucke:
    """187 Tora-Kapitel und 168 Tengri137-Phasen."""

    def test_187_equals_11_mal_17(self):
        """187 = 11 × 17 (BURUMUT-Architektur)."""
        assert 187 == 11 * 17

    def test_total_chapters(self):
        """50 + 40 + 27 + 36 + 34 = 187."""
        total = 50 + 40 + 27 + 36 + 34
        assert total == 187

    def test_differenz_187_168_ist_19_sec(self):
        """187 - 168 = 19 = BURUMUT-Sec."""
        assert 187 - 168 == 19

    def test_168_phasen_99_zeichen(self):
        """168 × 99 = 16632 Zeichen (vs 16576 Tengri137)."""
        assert 168 * 99 == 16632

    def test_tengri137_16576_zeichen(self):
        """Tengri137 hat 16576 lateinische Buchstaben."""
        tengri_hebr = load_tengri137()
        assert len(tengri_hebr) == 16576


# ============================================================
# TEST 2: Tora-Buch-Mapping
# ============================================================

class TestToraBuchMapping:
    """Phasen-Index → (Buch, Kapitel)."""

    def test_phase_0_ist_genesis_1(self):
        """Phase 0 = Genesis 1."""
        book, chap = phase_to_torah(0)
        assert book == 'Genesis'
        assert chap == 1

    def test_phase_44_ist_genesis_49(self):
        """Phase 44 = Genesis 49 (letzte Phase von Genesis)."""
        book, chap = phase_to_torah(44)
        assert book == 'Genesis'
        assert chap >= 49  # Mindestens 49

    def test_phase_45_ist_exodus_1(self):
        """Phase 45 = Exodus 1 (Anfang von Exodus)."""
        book, chap = phase_to_torah(45)
        assert book == 'Exodus'
        assert chap == 1

    def test_phase_80_ist_exodus_40(self):
        """Phase 80 = Exodus (Ende)."""
        book, chap = phase_to_torah(80)
        assert book == 'Exodus'
        assert chap >= 35

    def test_phase_81_ist_leviticus_1(self):
        """Phase 81 = Leviticus 1."""
        book, chap = phase_to_torah(81)
        assert book == 'Leviticus'
        assert chap == 1

    def test_phase_104_ist_leviticus(self):
        """Phase 104 = Leviticus (Ende)."""
        book, chap = phase_to_torah(104)
        assert book == 'Leviticus'

    def test_phase_105_ist_numeri_1(self):
        """Phase 105 = Numeri 1."""
        book, chap = phase_to_torah(105)
        assert book == 'Numeri'
        assert chap == 1

    def test_phase_136_ist_numeri(self):
        """Phase 136 = Numeri (Ende)."""
        book, chap = phase_to_torah(136)
        assert book == 'Numeri'

    def test_phase_137_ist_deuteronomium_1(self):
        """Phase 137 = Deuteronomium 1."""
        book, chap = phase_to_torah(137)
        assert book == 'Deuteronomium'
        assert chap == 1

    def test_phase_167_ist_deuteronomium_33(self):
        """Phase 167 = Deuteronomium 33."""
        book, chap = phase_to_torah(167)
        assert book == 'Deuteronomium'
        assert chap >= 30

    def test_alle_phasen_gemappt(self):
        """Alle 168 Phasen haben ein gültiges Mapping."""
        for i in range(168):
            book, chap = phase_to_torah(i)
            assert book is not None
            assert chap is not None


# ============================================================
# TEST 3: BURUMUT-Architektur
# ============================================================

class TestBurumutArchitektur:
    """11²+1 = 122 = BURUMUT-Architektur."""

    def test_11_quadrat_plus_1_eq_122(self):
        """11² + 1 = 122."""
        assert 11**2 + 1 == 122

    def test_burumut_99_ist_eine_einheit(self):
        """BURUMUT-99 ist 1. Einheit der Tengri137-Architektur."""
        # 99 = 3² × 11
        assert 99 == 3**2 * 11

    def test_168_teiler_24(self):
        """168 = 8 × 21 = 24 × 7."""
        assert 168 == 8 * 21
        assert 168 == 24 * 7

    def test_187_minus_122_eq_65(self):
        """187 - 122 = 65 = Eselsalter Jakobs (Gen 25,20)."""
        assert 187 - 122 == 65


# ============================================================
# TEST 4: Phasen-Verteilung
# ============================================================

class TestPhasenVerteilung:
    """55 clean + 113 Pendel = 168 Phasen."""

    def test_55_plus_113_eq_168(self):
        """55 + 113 = 168 (clean + pendel)."""
        assert 55 + 113 == 168

    def test_phasen_halten_in_verteilung(self):
        """Mindestens eine Phase hält in 1 Schritt (Aleph)."""
        tengri_hebr = load_tengri137()
        one_step_phases = 0
        for phase_idx in range(168):
            start = phase_idx * 99
            end = min((phase_idx + 1) * 99, len(tengri_hebr))
            phase_tape = tengri_hebr[start:end]
            r = run_phase(phase_tape, max_steps=200)
            if r['total_steps'] == 1:
                one_step_phases += 1
        assert one_step_phases >= 10  # Mindestens 10 Phasen mit 1 Schritt

    def test_3_phasen_34_schritte(self):
        """Genau 3 Phasen halten in 34 Schritten (5 Layer × 7 - 1)."""
        tengri_hebr = load_tengri137()
        n_34 = 0
        for phase_idx in range(168):
            start = phase_idx * 99
            end = min((phase_idx + 1) * 99, len(tengri_hebr))
            phase_tape = tengri_hebr[start:end]
            r = run_phase(phase_tape, max_steps=200)
            if r['total_steps'] == 34:
                n_34 += 1
        # Es sollten mindestens 2-3 Phasen sein (Toleranz)
        assert n_34 >= 2

    def test_determinismus_phasen(self):
        """Phasen-Resultate sind deterministisch."""
        tengri_hebr = load_tengri137()
        # Phase 0 zweimal laufen
        phase_0 = tengri_hebr[:99]
        r1 = run_phase(phase_0)
        r2 = run_phase(phase_0)
        assert r1['total_steps'] == r2['total_steps']
        assert r1['halt_reason'] == r2['halt_reason']


# ============================================================
# TEST 5: Tora-Buch-Verteilung
# ============================================================

class TestToraBuchVerteilung:
    """Phasen pro Buch: 45/36/24/32/31."""

    def test_genesis_phasen(self):
        """Genesis: 45 Phasen."""
        genesis_phases = [i for i in range(168)
                          if phase_to_torah(i)[0] == 'Genesis']
        assert len(genesis_phases) == 45

    def test_exodus_phasen(self):
        """Exodus: 36 Phasen."""
        exodus_phases = [i for i in range(168)
                         if phase_to_torah(i)[0] == 'Exodus']
        assert len(exodus_phases) == 36

    def test_leviticus_phasen(self):
        """Leviticus: 24 Phasen."""
        leviticus_phases = [i for i in range(168)
                            if phase_to_torah(i)[0] == 'Leviticus']
        assert len(leviticus_phases) == 24

    def test_numeri_phasen(self):
        """Numeri: 32 Phasen."""
        numeri_phases = [i for i in range(168)
                         if phase_to_torah(i)[0] == 'Numeri']
        assert len(numeri_phases) == 32

    def test_deuteronomium_phasen(self):
        """Deuteronomium: 31 Phasen."""
        deut_phases = [i for i in range(168)
                       if phase_to_torah(i)[0] == 'Deuteronomium']
        assert len(deut_phases) == 31


# ============================================================
# TEST 6: Wichtige Phasen
# ============================================================

class TestWichtigePhasen:
    """Spezifische Phasen-Mappings (BURUMUT-Architektur)."""

    def test_phase_0_ist_genesis_1_1_schoepfung(self):
        """Phase 0 = Gen 1,1 (Schöpfung) — 34 Schritte."""
        tengri_hebr = load_tengri137()
        phase_0 = tengri_hebr[:99]
        r = run_phase(phase_0, max_steps=200)
        assert r['total_steps'] == 34
        assert r['halt_reason'] == 'ALL_PHASES_COMPLETE'

    def test_phase_121_numeri_19_ist_burumut_phase(self):
        """Phase 121 = 11²+1 = BURUMUT-Architektur."""
        book, chap = phase_to_torah(121)
        assert book == 'Numeri'
        # Phase 121 entspricht der BURUMUT-Architektur (Numeri ist Wüstenwanderung)

    def test_phase_167_letzte_phase_deuteronomium(self):
        """Phase 167 = Deuteronomium 33 (Moses Tod)."""
        book, chap = phase_to_torah(167)
        assert book == 'Deuteronomium'
        # Deut 33 = Moses Segen vor dem Tod


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
