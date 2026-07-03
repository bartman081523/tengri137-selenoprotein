"""
🌌 P76: FIRST-FAIL-KARTOGRAPHIE — Die 168 Maschinen-Tode
========================================================

Tests für die systematische Kartographie des ersten M4-Versagens
in allen 168 Phasen von Tengri137.

P70 zeigte: ALLE 168 Phasen scheitern an Step 1.
P76 zeigt: WO genau stirbt die Maschine? An welchem hebr. Buchstaben?

EMPIRISCHE VOR-BEFUNDE:
- Phase 0 → ה (He, 5)
- Phase 1 → כ (Kaf, 20)
- Phase 2 → ק (Kof, 100)
- Phase 3 → נ (Nun, 50)
- Phase 26 → ד (Dalet, 4)
- Phase 122 → ו (Vav, 6)

DETERMINISMUS:
- 3/3 Läufe identisch
"""

import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
from collections import Counter
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import HEBR_VALUES, build_tora_transitions
from KANONIK_VALIDATOR_MODUL import KanonikValidator, GematriaAnchor, Snapshot
from PHASE_MAPPING_TORA import phase_to_torah
from FIRST_FAIL_KARTOGRAPHIE import (
    FirstFailRecord, FirstFailKartographie,
    kartographiere_first_fails, phase_first_fail_lookup,
    verteilung_der_first_fails, top_symbole
)


def load_tengri_hebr():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        text = f.read()
    text_clean = re.sub(r'\s+', '', text.upper())
    lat = re.sub(r'[^A-Z]', '', text_clean)
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


# ============================================================
# TEST 1: FirstFailRecord Dataclass
# ============================================================

class TestFirstFailRecord:
    """FirstFailRecord speichert die Versagens-Daten."""

    def test_first_fail_record_erstellen(self):
        rec = FirstFailRecord(
            phase_idx=0,
            fail_symbol='ה',
            fail_gematria=5,
            fail_state=1,
            fail_gematria_acc=5,
            mod_37=5,
            mod_73=5,
            tora_book='Genesis',
            tora_chapter=1,
        )
        assert rec.phase_idx == 0
        assert rec.fail_symbol == 'ה'
        assert rec.fail_gematria == 5

    def test_first_fail_record_to_dict(self):
        rec = FirstFailRecord(0, 'ה', 5, 1, 5, 5, 5, 'Genesis', 1)
        d = rec.to_dict()
        assert d['phase_idx'] == 0
        assert d['fail_symbol'] == 'ה'
        assert d['tora_book'] == 'Genesis'

    def test_first_fail_record_mit_state(self):
        """State ist 0-5."""
        rec = FirstFailRecord(0, 'ה', 5, 1, 5, 5, 5, 'Genesis', 1)
        assert 0 <= rec.fail_state <= 5


# ============================================================
# TEST 2: Kartographie 168 Phasen
# ============================================================

class TestKartographie168Phasen:
    """Alle 168 Phasen sind dokumentiert."""

    def test_168_phasen_dokumentiert(self):
        result = kartographiere_first_fails()
        assert result['n_phases'] == 168

    def test_records_haben_alle_phase_idx(self):
        """Jede Phase 0-167 ist vertreten."""
        result = kartographiere_first_fails()
        indices = [r.phase_idx for r in result['records']]
        for i in range(168):
            assert i in indices

    def test_jede_phase_hat_fail_symbol(self):
        """Jede Phase hat ein Fail-Symbol dokumentiert."""
        result = kartographiere_first_fails()
        for r in result['records']:
            assert r.fail_symbol is not None
            assert r.fail_gematria > 0

    def test_failure_step_ist_1_fuer_alle(self):
        """Failure-Step ist 1 für alle (empirisch, P70)."""
        result = kartographiere_first_fails()
        for r in result['records']:
            assert r.failure_step == 1


# ============================================================
# TEST 3: Verteilung der Symbole
# ============================================================

class TestVerteilungSymbole:
    """Welcher Buchstabe dominiert als First-Fail?"""

    def test_verteilung_ist_dict(self):
        result = kartographiere_first_fails()
        vert = result['verteilung']
        assert isinstance(vert, dict)
        assert sum(vert.values()) == 168

    def test_top_symbol_existiert(self):
        """Es gibt einen häufigsten First-Fail."""
        result = kartographiere_first_fails()
        top = result['top_5']
        assert len(top) == 5
        # Top-Symbol hat die meisten Vorkommen
        assert top[0][1] >= top[1][1]

    def test_fail_symbole_aus_22_hebr_buchstaben(self):
        """First-Fails sind aus den 22 hebr. Buchstaben."""
        result = kartographiere_first_fails()
        vert = result['verteilung']
        for sym in vert:
            assert sym in HEBR_VALUES

    def test_kein_fail_symbol_ist_multiples_37(self):
        """Symbole mit Gematria = Vielfaches von 37 (74, 111, …) sind selten.
        Bei Step 1 ist acc = gematria. Wenn gematria % 37 == 0, gibt es
        keine Violation. Also: keine First-Fails mit gematria % 37 == 0."""
        result = kartographiere_first_fails()
        for r in result['records']:
            # Wenn fail_gematria % 37 == 0, dann acc = 0 + gematria
            # und das wäre KEINE Violation
            assert r.fail_gematria % 37 != 0


# ============================================================
# TEST 4: First-Fail pro Tag
# ============================================================

class TestFirstFailProTag:
    """7-Tage-Aggregation."""

    def test_7_tage_dokumentiert(self):
        result = kartographiere_first_fails()
        per_day = result['per_day']
        assert len(per_day) == 7

    def test_jeder_tag_hat_24_phasen(self):
        result = kartographiere_first_fails()
        per_day = result['per_day']
        for d in per_day:
            assert d['n_phases'] == 24

    def test_tag_sabbat_vs_chaos(self):
        """Sabbat-Tag (7) und Chaos-Tag (6) sind dokumentiert."""
        result = kartographiere_first_fails()
        per_day = result['per_day']
        sabbat = next(d for d in per_day if d['day_idx'] == 7)
        chaos = next(d for d in per_day if d['day_idx'] == 6)
        assert sabbat['n_phases'] == 24
        assert chaos['n_phases'] == 24


# ============================================================
# TEST 5: First-Fail pro Tora-Buch
# ============================================================

class TestFirstFailProBuch:
    """Tora-Buch-Aggregation."""

    def test_5_buecher_dokumentiert(self):
        result = kartographiere_first_fails()
        per_book = result['per_book']
        for book in ['Genesis', 'Exodus', 'Leviticus',
                     'Numeri', 'Deuteronomium']:
            assert book in per_book

    def test_jedes_buch_hat_phasen(self):
        result = kartographiere_first_fails()
        per_book = result['per_book']
        for book, count in per_book.items():
            assert count > 0

    def test_total_phasen_pro_buch_ist_168(self):
        result = kartographiere_first_fails()
        per_book = result['per_book']
        assert sum(per_book.values()) == 168


# ============================================================
# TEST 6: Phase Lookup
# ============================================================

class TestPhaseLookup:
    """Gezielte Abfrage für bekannte Phasen."""

    def test_phase_0_fail_ist_he(self):
        """Phase 0: First-Fail = He (ה, 5)."""
        result = kartographiere_first_fails()
        p0 = next(r for r in result['records'] if r.phase_idx == 0)
        assert p0.fail_symbol == 'ה'
        assert p0.fail_gematria == 5

    def test_phase_3_fail_ist_nun(self):
        """Phase 3: First-Fail = Nun (נ, 50)."""
        result = kartographiere_first_fails()
        p3 = next(r for r in result['records'] if r.phase_idx == 3)
        assert p3.fail_symbol == 'נ'
        assert p3.fail_gematria == 50

    def test_phase_122_fail_ist_vav(self):
        """Phase 122: First-Fail = Vav (ו, 6)."""
        result = kartographiere_first_fails()
        p122 = next(r for r in result['records'] if r.phase_idx == 122)
        assert p122.fail_symbol == 'ו'
        assert p122.fail_gematria == 6


# ============================================================
# TEST 7: Mod-37 und Mod-73
# ============================================================

class TestMod37Mod73:
    """Gematria-Resonanz der First-Fails."""

    def test_mod_37_nie_0(self):
        """Wenn fail_gematria % 37 == 0, gäbe es keine Violation.
        Also: mod_37 != 0 für alle First-Fails."""
        result = kartographiere_first_fails()
        for r in result['records']:
            assert r.mod_37 != 0

    def test_mod_37_im_bereich(self):
        """mod_37 ist im Bereich 1-36."""
        result = kartographiere_first_fails()
        for r in result['records']:
            assert 1 <= r.mod_37 <= 36

    def test_mod_73_im_bereich(self):
        """mod_73 ist im Bereich 0-72."""
        result = kartographiere_first_fails()
        for r in result['records']:
            assert 0 <= r.mod_73 <= 72


# ============================================================
# TEST 8: Korrelation mit Entropie
# ============================================================

class TestKorrelationEntropie:
    """H ↔ Fail-Symbol."""

    def test_fail_gematria_korreliert_mit_h(self):
        """Korrelationskoeffizient r zwischen H und fail_gematria."""
        result = kartographiere_first_fails()
        corr = result.get('correlation_h_fail_gem')
        if corr is not None:
            assert -1 <= corr <= 1

    def test_fail_symbol_dict_konsistent(self):
        """Fail-Symbol-Verteilung ist konsistent."""
        result = kartographiere_first_fails()
        vert = result['verteilung']
        # Summe = 168
        assert sum(vert.values()) == 168
        # Mindestens 1 Symbol
        assert len(vert) >= 1


# ============================================================
# TEST 9: Determinismus
# ============================================================

class TestDeterminismus:
    """kartographiere_first_fails ist deterministisch."""

    def test_3_runs_identisch(self):
        r1 = kartographiere_first_fails()
        r2 = kartographiere_first_fails()
        r3 = kartographiere_first_fails()
        # Verteilung identisch
        assert r1['verteilung'] == r2['verteilung']
        assert r2['verteilung'] == r3['verteilung']

    def test_records_identisch(self):
        r1 = kartographiere_first_fails()
        r2 = kartographiere_first_fails()
        # Phase 0, 3, 26, 122 müssen identisch sein
        for idx in [0, 3, 26, 122]:
            p1 = next(r for r in r1['records'] if r.phase_idx == idx)
            p2 = next(r for r in r2['records'] if r.phase_idx == idx)
            assert p1.fail_symbol == p2.fail_symbol
            assert p1.fail_gematria == p2.fail_gematria


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
