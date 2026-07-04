"""
🌌 P69: SEZIERUNG DER SINGULARITÄT — PHASE 26 (Gen 29) TDD-Tests
==================================================================

Verifiziert drei exakte Fragen an Phase 26 (Genesis 29):

1. POINT OF FAILURE:
   - An welchem exakten Zeichen/Operator reißt die 37² = 1369 Brücke
     im KVM-Strict-Mode?
   - Welcher Buchstabe steht dort, welche Gematria?
   - Welcher Maschinen-Zustand (q_0..q_5)?

2. OPERATOR-SYNTAX:
   - Sind die 20 Sec-Operatoren zufällig verstreut, oder bilden sie
     ein zusammenhängendes Instruktions-Set?
   - Welche Verteilung? (MOVE_LEFT, READ, MOVE_RIGHT, STATE, HALT)
   - Welche Positionen? (Offset 0-98 in Phase)

3. RESONANZ-ECHO:
   - Wenn KVM das Backtracking erzwingt, auf welchen Zustand
     fällt die Maschine zurück?
   - Welcher letzte gültige Snapshot wurde gefunden?
   - Welche letzte gültige Gematria-Akkumulation?

ARCHITEKTUR:
- Phase 26 = Tengri137 Position 2574-2672 (hebr.)
- 99 Zeichen, 20 Sec-Operatoren (Maximum in Tengri137)
- Genesis 29: Jakob, Lea, Rahel (Täuschung, irdische Konflikte)
- In unserer Maschine: Punkt maximaler Operator-Dichte

KVM-STRICT-MODE:
- Bei erster Violation → sofortiger Backtrack
- Phase 26 bricht nach 1 Schritt zusammen (lt. KVM_ANALYSE)
- Das ist die "Wand im Informationsfeld"
"""

import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
from collections import Counter
from KANONIK_VALIDATOR_MODUL import (
    KanonikValidator, GematriaAnchor, kanonik_run, extract_anchor_from_tengri
)
from PHASE26_SEZIERUNG import (
    Phase26OperatorMap, PointOfFailure, ResonanzEcho, seziere_phase_26
)
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import (
    BURUMUT, burumut_to_hebr, HEBR_VALUES, MISSING_OPERATORS, build_tora_transitions
)
from PHASE_MAPPING_TORA import phase_to_torah


def load_tengri137_hebr():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    lat = re.sub(r'[^A-Z]', '', full.upper())
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


PHASE_26 = None  # Lazy init


def get_phase_26():
    global PHASE_26
    if PHASE_26 is None:
        tengri_hebr = load_tengri137_hebr()
        PHASE_26 = tengri_hebr[26*99:27*99]
    return PHASE_26


# ============================================================
# TEST 1: Phase 26 Grundlagen
# ============================================================

class TestPhase26Grundlagen:
    """Phase 26 = Gen 29, 99 Zeichen."""

    def test_phase_26_ist_genesis_29(self):
        """Phase 26 ist Genesis, Kapitel 29."""
        book, chap = phase_to_torah(26)
        assert book == 'Genesis'
        assert chap == 29

    def test_phase_26_hat_99_zeichen(self):
        """Phase 26 hat 99 Zeichen."""
        phase_26 = get_phase_26()
        assert len(phase_26) == 99

    def test_phase_26_hat_20_sec_operatoren(self):
        """Phase 26 hat 20 Sec-Operatoren (Maximum in Tengri137)."""
        phase_26 = get_phase_26()
        n_sec = sum(1 for c in phase_26 if c in MISSING_OPERATORS)
        assert n_sec == 20

    def test_phase_26_gematria(self):
        """Phase 26 Soll-Gematria = 4481."""
        tengri_hebr = load_tengri137_hebr()
        gem = extract_anchor_from_tengri(tengri_hebr, 26, 99)
        assert gem == 4481


# ============================================================
# TEST 2: Phase26OperatorMap — Operator-Syntax
# ============================================================

class TestPhase26OperatorMap:
    """Operator-Map: wo sind die 20 Sec-Operatoren?"""

    def test_operator_map_zaehlt_20_sec(self):
        """OperatorMap zählt 20 Sec-Operatoren."""
        phase_26 = get_phase_26()
        m = Phase26OperatorMap(phase_26)
        assert m.n_sec_total == 20

    def test_operator_map_positionen(self):
        """OperatorMap gibt alle 20 Positionen zurück."""
        phase_26 = get_phase_26()
        m = Phase26OperatorMap(phase_26)
        positions = m.sec_positions
        assert len(positions) == 20
        # Alle Positionen sind < 99
        assert all(0 <= p < 99 for p in positions)

    def test_operator_map_buchstaben(self):
        """OperatorMap gibt alle 20 Sec-Buchstaben zurück."""
        phase_26 = get_phase_26()
        m = Phase26OperatorMap(phase_26)
        letters = m.sec_letters
        assert len(letters) == 20
        # Alle sind in MISSING_OPERATORS
        assert all(l in MISSING_OPERATORS for l in letters)

    def test_operator_map_verteilung(self):
        """OperatorMap zählt Verteilung der 5 Sec-Typen."""
        phase_26 = get_phase_26()
        m = Phase26OperatorMap(phase_26)
        distribution = m.sec_distribution
        # Mindestens 1 Operator pro Sec-Typ ODER eine dokumentierte Verteilung
        # Wir prüfen: Summe = 20
        assert sum(distribution.values()) == 20

    def test_operator_map_ist_zufaellig_oder_strukturiert(self):
        """OperatorMap: sind die Positionen zufällig oder strukturiert?"""
        phase_26 = get_phase_26()
        m = Phase26OperatorMap(phase_26)
        # Berechne durchschnittliche Distanz zwischen Sec-Operatoren
        positions = sorted(m.sec_positions)
        if len(positions) >= 2:
            gaps = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
            avg_gap = sum(gaps) / len(gaps)
            # Mittlerer Abstand im 99er-Tape: 99/20 ≈ 4.95
            assert 1.0 <= avg_gap <= 50.0  # Sanity-Check

    def test_operator_map_analyse(self):
        """OperatorMap: vollständige Analyse als Dict."""
        phase_26 = get_phase_26()
        m = Phase26OperatorMap(phase_26)
        result = m.analyse()
        assert 'n_sec_total' in result
        assert 'sec_positions' in result
        assert 'sec_letters' in result
        assert 'sec_distribution' in result
        assert 'sec_gaps' in result
        assert 'avg_gap' in result
        assert result['n_sec_total'] == 20


# ============================================================
# TEST 3: PointOfFailure — wo reißt 37²?
# ============================================================

class TestPointOfFailure:
    """Point of Failure: wo reißt 37² im strict-Mode?"""

    def test_point_of_failure_strict_mode(self):
        """Im strict-Mode: Phase 26 bricht nach wenigen Schritten."""
        phase_26 = get_phase_26()
        pof = PointOfFailure(phase_26, strict=True)
        pof.run()
        # Phase 26 bricht sehr schnell zusammen
        assert pof.failure_step is not None
        assert pof.failure_step < 50  # Sollte schnell sein

    def test_point_of_failure_position(self):
        """Point of Failure: Position im Tape."""
        phase_26 = get_phase_26()
        pof = PointOfFailure(phase_26, strict=True)
        pof.run()
        # Position 0-98
        assert 0 <= pof.failure_position < 99

    def test_point_of_failure_symbol(self):
        """Point of Failure: das auslösende Symbol."""
        phase_26 = get_phase_26()
        pof = PointOfFailure(phase_26, strict=True)
        pof.run()
        # Symbol ist ein hebr. Buchstabe
        assert pof.failure_symbol in HEBR_VALUES

    def test_point_of_failure_gematria(self):
        """Point of Failure: Gematria des auslösenden Symbols."""
        phase_26 = get_phase_26()
        pof = PointOfFailure(phase_26, strict=True)
        pof.run()
        # Gematria ist nachschlagbar
        assert pof.failure_gematria == HEBR_VALUES.get(pof.failure_symbol, 0)

    def test_point_of_failure_state(self):
        """Point of Failure: Maschinen-Zustand q_0..q_5."""
        phase_26 = get_phase_26()
        pof = PointOfFailure(phase_26, strict=True)
        pof.run()
        # 6 Zustände (0-5)
        assert 0 <= pof.failure_state <= 5

    def test_point_of_failure_gematria_acc(self):
        """Point of Failure: die Gematria-Akkumulation am Failure-Punkt."""
        phase_26 = get_phase_26()
        pof = PointOfFailure(phase_26, strict=True)
        pof.run()
        # Die acc ist NICHT durch 37 teilbar
        assert pof.failure_gematria_acc % 37 != 0
        assert pof.failure_gematria_acc > 0

    def test_point_of_failure_analyse_dict(self):
        """Point of Failure: vollständige Analyse als Dict."""
        phase_26 = get_phase_26()
        pof = PointOfFailure(phase_26, strict=True)
        pof.run()
        result = pof.analyse()
        assert 'failure_step' in result
        assert 'failure_position' in result
        assert 'failure_symbol' in result
        assert 'failure_gematria' in result
        assert 'failure_state' in result
        assert 'failure_gematria_acc' in result
        assert 'last_valid_state' in result
        assert 'last_valid_position' in result
        assert 'last_valid_gematria_acc' in result


# ============================================================
# TEST 4: ResonanzEcho — wohin fällt die Maschine?
# ============================================================

class TestResonanzEcho:
    """Resonanz-Echo: Restore-Ziel bei Backtrack."""

    def test_resonanz_echo_erstellt(self):
        """ResonanzEcho wird erstellt und läuft."""
        phase_26 = get_phase_26()
        echo = ResonanzEcho(phase_26)
        echo.run()
        # Sollte einen Restore dokumentieren
        assert echo.n_restores >= 1

    def test_resonanz_echo_restore_state(self):
        """ResonanzEcho: Maschinen-Zustand nach Restore."""
        phase_26 = get_phase_26()
        echo = ResonanzEcho(phase_26)
        echo.run()
        # Nach Restore: state ist 0-5
        assert 0 <= echo.last_restore_state <= 5

    def test_resonanz_echo_restore_position(self):
        """ResonanzEcho: Kopf-Position nach Restore."""
        phase_26 = get_phase_26()
        echo = ResonanzEcho(phase_26)
        echo.run()
        # Restore-Position ist 0-98
        assert 0 <= echo.last_restore_position < 99

    def test_resonanz_echo_deterministisch(self):
        """ResonanzEcho: deterministisch (3 Läufe identisch)."""
        phase_26 = get_phase_26()
        results = []
        for _ in range(3):
            echo = ResonanzEcho(phase_26)
            echo.run()
            results.append((
                echo.n_restores,
                echo.last_restore_state,
                echo.last_restore_position,
                echo.last_restore_gematria_acc,
            ))
        assert len(set(results)) == 1

    def test_resonanz_echo_analyse_dict(self):
        """ResonanzEcho: vollständige Analyse als Dict."""
        phase_26 = get_phase_26()
        echo = ResonanzEcho(phase_26)
        echo.run()
        result = echo.analyse()
        assert 'n_restores' in result
        assert 'last_restore_state' in result
        assert 'last_restore_position' in result
        assert 'last_restore_gematria_acc' in result
        assert 'restore_to_step' in result


# ============================================================
# TEST 5: seziere_phase_26 — Master-Funktion
# ============================================================

class TestSezierePhase26:
    """seziere_phase_26: kombiniert alle drei Analysen."""

    def test_seziere_phase_26_liefert_dict(self):
        """seziere_phase_26 liefert vollständiges Dict."""
        result = seziere_phase_26()
        assert 'operator_map' in result
        assert 'point_of_failure' in result
        assert 'resonanz_echo' in result
        assert 'phase_26_meta' in result

    def test_seziere_phase_26_meta(self):
        """seziere_phase_26: Meta-Informationen."""
        result = seziere_phase_26()
        meta = result['phase_26_meta']
        assert meta['book'] == 'Genesis'
        assert meta['chapter'] == 29
        assert meta['length'] == 99
        assert meta['n_sec_operators'] == 20

    def test_seziere_phase_26_deterministisch(self):
        """seziere_phase_26: 3 Läufe identisch."""
        results = []
        for _ in range(3):
            r = seziere_phase_26()
            results.append(r)
        # Operator-Map sollte identisch sein
        for r in results[1:]:
            assert r['operator_map'] == results[0]['operator_map']
            assert r['point_of_failure']['failure_position'] == \
                   results[0]['point_of_failure']['failure_position']
            assert r['resonanz_echo']['last_restore_position'] == \
                   results[0]['resonanz_echo']['last_restore_position']


# ============================================================
# TEST 6: BURUMUTREFAMTU als Kontrast
# ============================================================

class TestBurumutKontrast:
    """BURUMUTREFAMTU als Kontrast zu Phase 26."""

    def test_refamtu_hat_weniger_sec_als_phase_26(self):
        """BURUMUTREFAMTU hat SEC-Operator(en), aber weniger als Phase 26."""
        refamtu = burumut_to_hebr(BURUMUT[:14])
        n_sec_refamtu = sum(1 for c in refamtu if c in MISSING_OPERATORS)
        n_sec_p26 = sum(1 for c in get_phase_26() if c in MISSING_OPERATORS)
        assert n_sec_refamtu < n_sec_p26

    def test_refamtu_14_schritte_kanonisch(self):
        """BURUMUTREFAMTU: 14 Schritte, ALL_PHASES_COMPLETE."""
        refamtu = burumut_to_hebr(BURUMUT[:14])
        m = ToraTuringMultiPhase(refamtu, phase_size=99)
        m.run(max_steps=20)
        assert m.total_steps == 14
        assert m.halt_reason == 'ALL_PHASES_COMPLETE'


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
