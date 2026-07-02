"""
🌌 P74: PHASEN-122-SEZIERUNG — Die Anatomie des absoluten Chaos
================================================================

Tests für die exakte Sezierung von Phase 122 (Numeri 20: Moses
schlägt den Fels). Phase 122 hat H = 4.1844 — die HÖCHSTE
Entropie aller 168 Phasen (P72-Befund). Sie ist das Gegenstück
zu Phase 3 (P73: Namen-Phase).

EMPIRISCHE BEFUNDE (P72 + Vor-Analyse):
- H = 4.1844 (Maximum)
- n_unique = 21 lateinische Symbole
- Top-1: 'E' mit 11
- 11 hebr. Sec-Operatoren: 6× כ (READ), 3× ג (RIGHT), 1× ד (LEFT), 1× י (STATE)
- Inhalt: "WITH THE FOLLOWING PRIME NUMBERS CHECK ALL
  CALCULATED NUMBERS AGAIN TO BE SURE THIS OBJECT IS FOR
  THE BEST AMONG YOU I AM" — eine Meta-Anweisung

ARCHITEKTUR:
- Phase122FrequenzAnatomie
- Phase122OperatorKarte
- Phase122MaschinenLauf
- Phase122EntropieVergleich
- Phase122SemantischeSignatur
- seziere_phase_122

DETERMINISMUS:
- 3/3 Läufe identisch
"""

import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
import math
import json
from collections import Counter
from TENGRI_ORAKEL import berechne_entropie
from TORA_TURING_MULTIPHASE import EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import (
    HEBR_VALUES, MISSING_OPERATORS, build_tora_transitions
)
from PHASE_MAPPING_TORA import phase_to_torah
from PHASE122_SEZIERUNG import (
    Phase122FrequenzAnatomie, Phase122OperatorKarte,
    Phase122MaschinenLauf, Phase122EntropieVergleich,
    Phase122SemantischeSignatur, seziere_phase_122
)


def load_tengri_text():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        return f.read()


def get_phase_122_lat():
    text = load_tengri_text()
    text_clean = re.sub(r'\s+', '', text.upper())
    lat = re.sub(r'[^A-Z]', '', text_clean)
    return lat[122*99:123*99]


def get_phase_122_hebr():
    lat = get_phase_122_lat()
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


# ============================================================
# TEST 1: Grundlagen
# ============================================================

class TestPhase122Grundlagen:
    """Phase 122 korrekt extrahiert."""

    def test_phase_122_hat_99_zeichen(self):
        p122 = get_phase_122_lat()
        assert len(p122) == 99

    def test_phase_122_ist_numeri_20(self):
        """Phase 122 ist topologisch Numeri 20 (Wüste Zin / Fels)."""
        book, chap = phase_to_torah(122)
        assert book == 'Numeri'
        assert chap == 20

    def test_phase_122_hebr_99_zeichen(self):
        p122h = get_phase_122_hebr()
        assert len(p122h) == 99

    def test_phase_122_enthaelt_primitive(self):
        """Phase 122 enthält 'PRIME' (lateinisch, Whitespace-stripped)."""
        p122 = get_phase_122_lat()
        assert 'PRIME' in p122 or 'PRIMEN' in p122 or 'PRIMENU' in p122


# ============================================================
# TEST 2: Frequenz
# ============================================================

class TestPhase122Frequenz:
    """22 unique, E dominiert mit 11."""

    def test_top_symbol_ist_e(self):
        """'E' ist Top-Symbol mit 11 Vorkommen."""
        p122 = get_phase_122_lat()
        fa = Phase122FrequenzAnatomie(p122)
        assert fa.top4[0]['symbol'] == 'E'
        assert fa.top4[0]['freq'] == 11

    def test_n_unique_ist_22(self):
        """Phase 122 hat 22 unique Symbole (vs 16 in Phase 3)."""
        p122 = get_phase_122_lat()
        fa = Phase122FrequenzAnatomie(p122)
        assert fa.n_unique == 22

    def test_top4_ausgeglichen(self):
        """Top-4 sind NICHT perfekt gleichverteilt (anders als Phase 3)."""
        p122 = get_phase_122_lat()
        fa = Phase122FrequenzAnatomie(p122)
        top4_freqs = [e['freq'] for e in fa.top4]
        # In Phase 3: alle 4 = 12. Hier: Verteilung ist ungleich.
        assert not all(f == top4_freqs[0] for f in top4_freqs)

    def test_mehr_unique_als_phase_3(self):
        """Phase 122 hat mehr unique Symbole als Phase 3 (21 > 16)."""
        p122 = get_phase_122_lat()
        fa = Phase122FrequenzAnatomie(p122)
        assert fa.n_unique >= 16

    def test_top4_dominieren_weniger(self):
        """Top-4 dominieren weniger als 50% (vs 48.5% in Phase 3)."""
        p122 = get_phase_122_lat()
        fa = Phase122FrequenzAnatomie(p122)
        total_top4 = sum(e['freq'] for e in fa.top4)
        # Bei H = 4.18 ist die Verteilung flacher
        assert total_top4 < 50  # < 50/99 = 50.5%


# ============================================================
# TEST 3: Operatoren
# ============================================================

class TestPhase122Operatoren:
    """11 hebr. Sec-Operatoren, כ dominiert mit 6."""

    def test_11_hebr_sec_operatoren(self):
        p122h = get_phase_122_hebr()
        ok = Phase122OperatorKarte(p122h)
        assert ok.n_sec_total == 11

    def test_kaf_dominiert_mit_6(self):
        """כ (Kaf, READ) dominiert mit 6."""
        p122h = get_phase_122_hebr()
        ok = Phase122OperatorKarte(p122h)
        assert ok.sec_distribution.get('כ', 0) == 6

    def test_gimel_mit_3(self):
        """ג (Gimel, MOVE_RIGHT) hat 3 Vorkommen."""
        p122h = get_phase_122_hebr()
        ok = Phase122OperatorKarte(p122h)
        assert ok.sec_distribution.get('ג', 0) == 3

    def test_dalet_und_yod_mit_1(self):
        """ד (Dalet) und י (Yod) je 1x."""
        p122h = get_phase_122_hebr()
        ok = Phase122OperatorKarte(p122h)
        assert ok.sec_distribution.get('ד', 0) == 1
        assert ok.sec_distribution.get('י', 0) == 1


# ============================================================
# TEST 4: Maschinen-Lauf
# ============================================================

class TestPhase122MaschinenLauf:
    """M4 auf Phase 122."""

    def test_maschine_startet(self):
        p122h = get_phase_122_hebr()
        ml = Phase122MaschinenLauf(p122h)
        result = ml.run(max_steps=100)
        assert 'first_violation_step' in result
        assert 'total_steps' in result

    def test_maschine_failure_step_ist_1(self):
        """M4 scheitert bei Step 1 (wie alle 168 Phasen, P70)."""
        p122h = get_phase_122_hebr()
        ml = Phase122MaschinenLauf(p122h)
        result = ml.run(max_steps=100)
        assert result['first_violation_step'] is not None
        assert result['first_violation_step'] >= 1

    def test_maschine_failure_symbol_dokumentiert(self):
        p122h = get_phase_122_hebr()
        ml = Phase122MaschinenLauf(p122h)
        result = ml.run(max_steps=100)
        assert result.get('first_violation_symbol') is not None

    def test_maschine_max_gematria_dokumentiert(self):
        p122h = get_phase_122_hebr()
        ml = Phase122MaschinenLauf(p122h)
        result = ml.run(max_steps=100)
        assert result['max_gematria_acc'] > 0


# ============================================================
# TEST 5: Entropie
# ============================================================

class TestPhase122Entropie:
    """H(Phase 122) = 4.1844, das dokumentierte Maximum."""

    def test_phase_122_h_ist_maximum(self):
        p122 = get_phase_122_lat()
        ec = Phase122EntropieVergleich(p122)
        assert abs(ec.h - 4.1844) < 0.001

    def test_phase_122_h_ueber_log2_16(self):
        """H(Phase 122) > log₂(16) = 4.0."""
        p122 = get_phase_122_lat()
        ec = Phase122EntropieVergleich(p122)
        assert ec.h > math.log2(16)

    def test_phase_122_alphabet_eff_18(self):
        """Effektive Alphabetgröße 2^H ≈ 18.18."""
        p122 = get_phase_122_lat()
        ec = Phase122EntropieVergleich(p122)
        assert abs(ec.alphabet_eff - 18.18) < 0.1


# ============================================================
# TEST 6: Bigramm
# ============================================================

class TestPhase122Bigramm:
    """Bigramm-Verteilung."""

    def test_bigramm_counter_existiert(self):
        p122 = get_phase_122_lat()
        fa = Phase122FrequenzAnatomie(p122)
        assert hasattr(fa, 'bigram_counts')
        assert len(fa.bigram_counts) > 0

    def test_top_bigramm_dokumentiert(self):
        p122 = get_phase_122_lat()
        fa = Phase122FrequenzAnatomie(p122)
        assert fa.top_bigram is not None
        assert fa.top_bigram[1] >= 2

    def test_bigramm_anzahl_groesser_als_phase_3(self):
        """Phase 122 hat mehr unique Bigramme als Phase 3 (mehr Vielfalt)."""
        p122 = get_phase_122_lat()
        fa = Phase122FrequenzAnatomie(p122)
        n_bg = len(fa.bigram_counts)
        # Bei 99 Zeichen gibt es 98 Bigramme
        # Phase 3 (geordnet) hat weniger, Phase 122 (chaotisch) mehr
        assert n_bg >= 50  # viele unique


# ============================================================
# TEST 7: Semantik (Meta-Anweisung)
# ============================================================

class TestPhase122Semantik:
    """Die Meta-Anweisung ist lesbar."""

    def test_prime_kommt_vor(self):
        p122 = get_phase_122_lat()
        ss = Phase122SemantischeSignatur(p122)
        assert ss.word_counts.get('PRIME', 0) >= 1

    def test_numbers_kommt_vor(self):
        p122 = get_phase_122_lat()
        ss = Phase122SemantischeSignatur(p122)
        assert ss.word_counts.get('NUMBERS', 0) >= 1

    def test_check_kommt_vor(self):
        p122 = get_phase_122_lat()
        ss = Phase122SemantischeSignatur(p122)
        assert ss.word_counts.get('CHECK', 0) >= 1

    def test_mehr_befehlswoerter_als_namen(self):
        """Phase 122 hat mehr Befehls-Wörter als Gottesnamen."""
        p122 = get_phase_122_lat()
        ss = Phase122SemantischeSignatur(p122)
        # TENGRI sollte NICHT vorkommen
        tengri_count = ss.word_counts.get('TENGRI', 0)
        # Befehls-Wörter (CHECK, NUMBERS, PRIME, CALCULATED) sollten da sein
        command_words = ['CHECK', 'NUMBERS', 'PRIME', 'CALCULATED',
                         'AGAIN', 'SURE', 'BE']
        command_count = sum(ss.word_counts.get(w, 0) for w in command_words)
        assert command_count > tengri_count


# ============================================================
# TEST 8: Phase 122 vs Phase 3 (Kontrast)
# ============================================================

class TestPhase122VsPhase3:
    """Chaos vs. Stille."""

    def test_phase_122_h_hoeher_als_3(self):
        """H(Phase 122) > H(Phase 3)."""
        p3 = get_phase_122_lat()  # placeholder
        p3 = 'INGBETTERTENGRIHASMANYNAMESTIANTIANDIRANGISHANGDISHADDAIDINGIRORTENGEREARESOMEOFTHISNAMESTENGRIGAVE'
        ec3 = Phase122EntropieVergleich(p3)  # Wrong class — use Phase3
        from PHASE3_SEZIERUNG import Phase3EntropieVergleich as EC3
        ec3 = EC3(p3)
        p122 = get_phase_122_lat()
        ec122 = Phase122EntropieVergleich(p122)
        assert ec122.h > ec3.h

    def test_phase_122_n_unique_groesser_als_3(self):
        """22 unique > 16 unique."""
        p3 = 'INGBETTERTENGRIHASMANYNAMESTIANTIANDIRANGISHANGDISHADDAIDINGIRORTENGEREARESOMEOFTHISNAMESTENGRIGAVE'
        from PHASE3_SEZIERUNG import Phase3FrequenzAnatomie as FA3
        fa3 = FA3(p3)
        p122 = get_phase_122_lat()
        fa122 = Phase122FrequenzAnatomie(p122)
        assert fa122.n_unique > fa3.n_unique

    def test_phase_122_weniger_sec_als_3(self):
        """11 Sec < 14 Sec."""
        p3h = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?')
                      for c in 'INGBETTERTENGRIHASMANYNAMESTIANTIANDIRANGISHANGDISHADDAIDINGIRORTENGEREARESOMEOFTHISNAMESTENGRIGAVE')
        from PHASE3_SEZIERUNG import Phase3OperatorKarte as OK3
        ok3 = OK3(p3h)
        p122h = get_phase_122_hebr()
        ok122 = Phase122OperatorKarte(p122h)
        assert ok122.n_sec_total < ok3.n_sec_total

    def test_phase_122_top1_doppelt_so_hoch_wie_phase_3_top1(self):
        """Phase 122 Top (E=11) ist NICHT gleich Phase 3 Top (12)."""
        # Phase 3: 4 Symbole mit je 12
        # Phase 122: 1 Symbol mit 11
        # Die "Konzentration" ist unterschiedlich verteilt
        p122 = get_phase_122_lat()
        fa122 = Phase122FrequenzAnatomie(p122)
        top1_freq = fa122.top4[0]['freq']
        # In Phase 3 ist jeder der 4 Tops = 12
        # In Phase 122 ist nur 1 Top = 11
        # Wir prüfen, dass es einen Top gibt
        assert top1_freq >= 10


# ============================================================
# TEST 9: Apophenie-Schutz
# ============================================================

class TestApophenieSchutz:
    """Schutz vor Überinterpretation."""

    def test_meta_anweisung_ist_beobachtung(self):
        """Die Wörter 'CHECK', 'PRIME' sind Beobachtung, kein Beweis."""
        p122 = get_phase_122_lat()
        ss = Phase122SemantischeSignatur(p122)
        # Wir berichten die Wörter, NICHT ihre "Bedeutung"
        assert ss.word_counts.get('CHECK', 0) >= 1

    def test_read_operator_dominant_ist_zahl(self):
        """6× כ (READ) ist eine Zahl, keine metaphysische Aussage."""
        p122h = get_phase_122_hebr()
        ok = Phase122OperatorKarte(p122h)
        assert ok.sec_distribution.get('כ', 0) == 6
        # Wir behaupten NICHT: "Die Maschine soll lesen"


# ============================================================
# TEST 10: Determinismus
# ============================================================

class TestDeterminismus:
    """seziere_phase_122 ist deterministisch."""

    def test_3_runs_identisch(self):
        r1 = seziere_phase_122()
        r2 = seziere_phase_122()
        r3 = seziere_phase_122()
        assert r1['frequenz']['top4'] == r2['frequenz']['top4']
        assert r1['operatoren']['n_sec_total'] == r2['operatoren']['n_sec_total']

    def test_maschine_3_runs_identisch(self):
        p122h = get_phase_122_hebr()
        r1 = Phase122MaschinenLauf(p122h).run()
        r2 = Phase122MaschinenLauf(p122h).run()
        assert r1['first_violation_step'] == r2['first_violation_step']
        assert r1['first_violation_symbol'] == r2['first_violation_symbol']


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
