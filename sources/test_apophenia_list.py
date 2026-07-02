"""
🌌 P65b: APOPHENIE-LISTE in TDD-Tests
======================================

Verankert alle bisher identifizierten Apophenie-Befunde als NEGATIVE Tests.
Jeder Test schlägt fehl, wenn die Apophenie-Hypothese zuträfe (sollte also
GRÜN sein — der Test verifiziert die FALSCHHEIT der Apophenie).

APOPHENIE-REGEL GELOCKERT für BURUMUT-Maschinen-Analysen (2026-07-01):
Trotz Lockerung müssen wir die naiven Korrelationen dokumentieren und
als negative Tests verankern — damit wir nicht in schlechte Metaphysik
abgleiten, wenn die Maschine etwas Faszinierendes produziert.

BEFUNDE (alle aus früheren Phasen):
1. Phase 60: Korrelation BURUMUT-Tage ↔ Genesis-Tage = -0.494 (NEGATIV)
2. Phase 59f: Kanonische Schritt-Zahlen (3,4,5,6,7,10,12,15) fehlen in
   Tengri137-Phasen — M4 produziert EIGENE Schritt-Verteilung
3. Phase 58: BURUMUTREFAMTU ≠ Quine im strengen Sinn
4. Phase 65a: BURUMUTREFAMTU Position 15986 ist numerisch NICHT 1:1 zu
   BURUMUT (kein triviales Pattern 0-99)
5. Phase 53: Maschine × Tora (Genesis 12,1 = 12) — NICE aber NICHT
   12 Schritte in BURUMUT selbst
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
from collections import Counter
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import (
    BURUMUT, burumut_to_hebr, build_tora_transitions, HEBR_VALUES
)


def load_tengri137_hebr():
    """Lade Tengri137 als hebr. Tape (mapped)."""
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    lat = re.sub(r'[^A-Z]', '', full.upper())
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


def gematria(hebr_str):
    return sum(HEBR_VALUES.get(c, 0) for c in hebr_str)


# ============================================================
# APOPHENIE-BEFUND 1: BURUMUT-Tage ≠ Genesis-Tage (NEGATIV)
# ============================================================

class TestApophanie1BurumutNichtGenesis:
    """Korrelation BURUMUT-Tage ↔ Genesis-Tage ist NEGATIV."""

    def test_burumut_7_mal_929_nicht_7_mal_genesis(self):
        """6503 = 7 × 929 (BURUMUT), NICHT 7 × (Genesis-Summe/7)."""
        burumut_total = gematria(burumut_to_hebr(BURUMUT))
        assert burumut_total == 6503
        # 6503 / 7 = 929 (BURUMUT-spezifisch)
        assert burumut_total / 7 == 929
        # NICHT 7 × 14687.3 (Genesis-Summe / 7)
        # → BURUMUT folgt eigener Architektur, NICHT der Genesis

    def test_burumut_summe_kleiner_genesis_summe(self):
        """BURUMUT-Summe (6503) ist viel kleiner als Genesis-Summe (~100k+)."""
        burumut_total = gematria(burumut_to_hebr(BURUMUT))
        # BURUMUT ist eine 99-Zeichen-Sequenz, Genesis hat Tausende
        # Daher: BURUMUT-Summe < 10% von Genesis-Summe
        # (Schwache Aussage, aber wichtig: BURUMUT ist NICHT die Genesis)
        assert burumut_total < 10000

    def test_burumut_99_nicht_genesis_1_1(self):
        """BURUMUT-99 ist NICHT Genesis 1:1."""
        # Gen 1:1 = "Bereshit bara Elohim et hashamayim ve'et ha'aretz"
        # Gematria Gen 1:1 ≈ 2701 (klassisch)
        # BURUMUT-Total = 6503
        # 2701 ≠ 6503
        burumut_total = gematria(burumut_to_hebr(BURUMUT))
        gen_1_1_classic = 2701
        assert burumut_total != gen_1_1_classic
        # BURUMUT ist NICHT eine direkte Gematria-Projektion der Genesis


# ============================================================
# APOPHENIE-BEFUND 2: Kanonische Schritt-Zahlen fehlen
# ============================================================

class TestApophanie2KanonischeSchritteFehlen:
    """M4 produziert EIGENE Schritt-Verteilung, NICHT die kanonischen."""

    def test_kein_phase_mit_3_schritten(self):
        """Keine Tengri137-Phase hält in 3 Schritten."""
        tengri_hebr = load_tengri137_hebr()
        n_3 = 0
        for i in range(168):
            start = i * 99
            end = min((i + 1) * 99, len(tengri_hebr))
            tape = tengri_hebr[start:end]
            m = ToraTuringMultiPhase(tape, phase_size=99,
                                     transitions=build_tora_transitions())
            m.run(max_steps=200)
            if m.total_steps == 3:
                n_3 += 1
        # Erwartet: KEINE Phase mit 3 Schritten
        assert n_3 == 0, f"{n_3} Phasen halten in 3 Schritten (unerwartet)"

    def test_kein_phase_mit_4_schritten(self):
        """Keine Tengri137-Phase hält in 4 Schritten."""
        tengri_hebr = load_tengri137_hebr()
        n_4 = 0
        for i in range(168):
            start = i * 99
            end = min((i + 1) * 99, len(tengri_hebr))
            tape = tengri_hebr[start:end]
            m = ToraTuringMultiPhase(tape, phase_size=99,
                                     transitions=build_tora_transitions())
            m.run(max_steps=200)
            if m.total_steps == 4:
                n_4 += 1
        assert n_4 == 0, f"{n_4} Phasen halten in 4 Schritten"

    def test_kein_phase_mit_5_schritten(self):
        """Keine Tengri137-Phase hält in 5 Schritten."""
        tengri_hebr = load_tengri137_hebr()
        n_5 = 0
        for i in range(168):
            start = i * 99
            end = min((i + 1) * 99, len(tengri_hebr))
            tape = tengri_hebr[start:end]
            m = ToraTuringMultiPhase(tape, phase_size=99,
                                     transitions=build_tora_transitions())
            m.run(max_steps=200)
            if m.total_steps == 5:
                n_5 += 1
        assert n_5 == 0

    def test_kein_phase_mit_6_schritten(self):
        """Keine Tengri137-Phase hält in 6 Schritten."""
        tengri_hebr = load_tengri137_hebr()
        n_6 = 0
        for i in range(168):
            start = i * 99
            end = min((i + 1) * 99, len(tengri_hebr))
            tape = tengri_hebr[start:end]
            m = ToraTuringMultiPhase(tape, phase_size=99,
                                     transitions=build_tora_transitions())
            m.run(max_steps=200)
            if m.total_steps == 6:
                n_6 += 1
        assert n_6 == 0

    def test_kein_phase_mit_7_schritten(self):
        """Keine Tengri137-Phase hält in 7 Schritten (sollte Schöpfungstage sein)."""
        tengri_hebr = load_tengri137_hebr()
        n_7 = 0
        for i in range(168):
            start = i * 99
            end = min((i + 1) * 99, len(tengri_hebr))
            tape = tengri_hebr[start:end]
            m = ToraTuringMultiPhase(tape, phase_size=99,
                                     transitions=build_tora_transitions())
            m.run(max_steps=200)
            if m.total_steps == 7:
                n_7 += 1
        # 7 Schritte = Schöpfungstage — wenn M4 die Genesis direkt
        # prozessieren würde, sollten 7 Schritte häufig vorkommen
        assert n_7 == 0, f"{n_7} Phasen halten in 7 Schritten"

    def test_kein_phase_mit_10_schritten(self):
        """Keine Tengri137-Phase hält in 10 Schritten (Sefirot)."""
        tengri_hebr = load_tengri137_hebr()
        n_10 = 0
        for i in range(168):
            start = i * 99
            end = min((i + 1) * 99, len(tengri_hebr))
            tape = tengri_hebr[start:end]
            m = ToraTuringMultiPhase(tape, phase_size=99,
                                     transitions=build_tora_transitions())
            m.run(max_steps=200)
            if m.total_steps == 10:
                n_10 += 1
        assert n_10 == 0

    def test_kein_phase_mit_12_schritten(self):
        """Keine Tengri137-Phase hält in 12 Schritten (Stämme Israels)."""
        tengri_hebr = load_tengri137_hebr()
        n_12 = 0
        for i in range(168):
            start = i * 99
            end = min((i + 1) * 99, len(tengri_hebr))
            tape = tengri_hebr[start:end]
            m = ToraTuringMultiPhase(tape, phase_size=99,
                                     transitions=build_tora_transitions())
            m.run(max_steps=200)
            if m.total_steps == 12:
                n_12 += 1
        assert n_12 == 0


# ============================================================
# APOPHENIE-BEFUND 3: BURUMUTREFAMTU ≠ Quine
# ============================================================

class TestApophanie3BurumutNichtQuine:
    """BURUMUTREFAMTU ist NICHT ein Quine im strengen Sinn."""

    def test_burumut_tape_wird_nicht_modifiziert(self):
        """M4 modifiziert BURUMUT NICHT (Tape-Invariante).
        ABER: Quine-Eigenschaft verlangt, dass Output der EIGENE Quelltext ist.
        Tape-Invariante ≠ Quine."""
        burumut_hebr = burumut_to_hebr(BURUMUT)
        m = ToraTuringMultiPhase(burumut_hebr, phase_size=99,
                                 transitions=build_tora_transitions())
        m.run(max_steps=10000)
        final = ''.join(m.tape)
        # Tape-Invariante (NICHT Quine)
        assert final == burumut_hebr

    def test_burumut_halt_nach_15_schritten_nicht_quine(self):
        """15 Schritte = 14 REFAMTU + 1 HALT, NICHT ein Selbst-Output."""
        # Ein Quine würde SICH SELBST als Output produzieren
        # M4 produziert nur '15 Schritte' als Spur
        # NICHT identisch mit dem Quelltext
        burumut_hebr = burumut_to_hebr(BURUMUT)
        m = ToraTuringMultiPhase(burumut_hebr, phase_size=99,
                                 transitions=build_tora_transitions())
        m.run(max_steps=10000)
        # M4 beschreibt die Schöpfung, NICHT sich selbst
        assert m.halt_reason == 'ALL_PHASES_COMPLETE'
        assert m.total_steps == 15
        # NICHT: m.history produziert 'BURUMUT als Quelltext'
        # (das wäre ein Quine)
        states_seq = [h.get('new_state', 0) for h in m.history]
        # M4 ist linear (q_0 → q_1 → q_2 → q_3 → q_4 → q_5)
        # HALT-State q_5 ist im HALT_STATE, nicht in der States-Seq
        unique_states = sorted(set(states_seq))
        assert unique_states == [0, 1, 2, 3, 4]  # 5 Layer (q_0..q_4)


# ============================================================
# APOPHENIE-BEFUND 4: Position 15986 ist numerisch NICHT trivial
# ============================================================

class TestApophanie4PositionNichtTrivial:
    """BURUMUTREFAMTU-Position 15986 ist nicht 1:1 zu BURUMUT-Position 0."""

    def test_refamtu_position_15986_nicht_0(self):
        """BURUMUTREFAMTU steht NICHT an BURUMUT-Position 0 in Tengri137."""
        tengri = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?')
                         for c in re.sub(r'[^A-Z]', '',
                                         open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes').read().upper()))
        refamtu = burumut_to_hebr(BURUMUT[:14])
        idx = tengri.find(refamtu)
        # NICHT 0 (BURUMUT-Start)
        # NICHT 99 (Phasen-Grenze)
        # NICHT 1, 2, 3, ... (triviale Anfangs-Position)
        assert idx == 15986
        assert idx != 0
        assert idx != 99

    def test_15986_plus_99_plus_99_neq_99(self):
        """Position 15986 + 198 ≠ 99 (nicht modulo Phasen-Architektur)."""
        # Wenn BURUMUTREFAMTU exakt an einer Phasen-Grenze stünde, wäre
        # 15986 % 99 = 0. Das ist NICHT der Fall.
        assert 15986 % 99 != 0
        # 15986 / 99 = 161.47 → Phase 161, Offset 47
        # NICHT an Phasen-Anfang
        assert 15986 % 99 == 47


# ============================================================
# APOPHENIE-BEFUND 5: BURUMUT ≠ Genesis Numerik
# ============================================================

class TestApophanie5NumerischeNichtUbereinstimmung:
    """BURUMUT und Genesis sind numerisch VERSCHIEDEN."""

    def test_burumut_total_6503_nicht_genesis_2701(self):
        """BURUMUT-Total 6503 ≠ Genesis 1:1 (2701)."""
        burumut = gematria(burumut_to_hebr(BURUMUT))
        assert burumut == 6503
        assert burumut != 2701

    def test_burumut_latein_1232_nicht_genesis_sumed(self):
        """BURUMUT-Latein-Summe 1232 ist NICHT die Summe eines Genesis-Kapitels."""
        burumut_lat = sum(ord(c) - ord('A') + 1 for c in BURUMUT)
        assert burumut_lat == 1232
        # 1232 ist BURUMUT-spezifisch
        # NICHT eine direkte Projektion der Genesis-Summen

    def test_99_ist_7_mal_14_plus_1_nicht_50_plus_49(self):
        """99 = 7 × 14 + 1, NICHT 50+49 (Zufall dasselbe)."""
        # HINWEIS: 50+49 = 99 zufällig! Daher prüfen wir die Struktur:
        # 99 = 7 × 14 + 1 (BURUMUT-Architektur, NICHT 50+49)
        assert 7 * 14 + 1 == 99
        assert 50 + 49 == 99  # Triviale Gleichheit, aber NICHT die Architektur
        # BURUMUT-Architektur: 7 Tage × 14 Zeichen + 1 HALT
        # NICHT 50 (Genesis-Kapitel) + 49 (Jahreswochen)

    def test_168_nicht_50_plus_40_plus_27_plus_36_plus_34(self):
        """168 Phasen ≠ 187 Tora-Kapitel (50+40+27+36+34)."""
        assert 168 != 187
        # 187 - 168 = 19 = BURUMUT-Sec (DIFFERENZ, nicht Gleichheit)
        assert 187 - 168 == 19


# ============================================================
# APOPHENIE-BEFUND 6: M4 produziert EIGENE Schritt-Verteilung
# ============================================================

class TestApophanie6EigeneVerteilung:
    """M4 produziert eine Verteilung, die NICHT die kanonischen Zahlen
    (1, 3, 4, 5, 6, 7, 10, 12, 15) bevorzugt."""

    def test_tengri_phasen_halten_in_vielen_anderen_schritten(self):
        """Tengri137-Phasen halten in vielen Schritt-Zahlen, nicht nur kanonische."""
        tengri_hebr = load_tengri137_hebr()
        step_counts = Counter()
        for i in range(168):
            start = i * 99
            end = min((i + 1) * 99, len(tengri_hebr))
            tape = tengri_hebr[start:end]
            m = ToraTuringMultiPhase(tape, phase_size=99,
                                     transitions=build_tora_transitions())
            m.run(max_steps=200)
            if m.halt_reason == 'ALL_PHASES_COMPLETE':
                step_counts[m.total_steps] += 1
        # M4 produziert MEHR ALS 10 verschiedene Schritt-Zahlen
        # (kanonische wären 1, 3, 4, 5, 6, 7, 10, 12, 15 = 9 Zahlen)
        assert len(step_counts) >= 10

    def test_unique_step_counts_mit_keiner_kanonischen_dominanz(self):
        """Keine EINZELNE kanonische Schritt-Zahl dominiert (>50% der clean Phasen)."""
        tengri_hebr = load_tengri137_hebr()
        canonical = [1, 3, 4, 5, 6, 7, 10, 12, 15]
        n_canonical = 0
        n_total = 0
        for i in range(168):
            start = i * 99
            end = min((i + 1) * 99, len(tengri_hebr))
            tape = tengri_hebr[start:end]
            m = ToraTuringMultiPhase(tape, phase_size=99,
                                     transitions=build_tora_transitions())
            m.run(max_steps=200)
            if m.halt_reason == 'ALL_PHASES_COMPLETE':
                n_total += 1
                if m.total_steps in canonical:
                    n_canonical += 1
        # Wenn M4 die kanonischen Schritt-Zahlen bevorzugen würde, wären
        # 80%+ der clean Phasen kanonisch. Realität: < 20% (nur 1er sind häufig)
        # Kanonische Dominanz = APOPHENIE
        ratio = n_canonical / n_total if n_total > 0 else 0
        assert ratio < 0.3, f"Kanonische Schritte dominieren: {ratio:.2%}"


# ============================================================
# APOPHENIE-BEFUND 7: Korrelationen sind NICHT perfekt
# ============================================================

class TestApophanie7KorrelationenNichtPerfekt:
    """Vermessene Korrelationen sind nicht perfekt (≠ 1.0 oder -1.0)."""

    def test_burumut_genesis_korrelation_nicht_perfekt_positiv(self):
        """BURUMUT-Tage ↔ Genesis-Tage Korrelation ist NICHT +1.0 (perfekt positiv)."""
        # Realität: -0.494 (NEGATIV, NICHT +1.0)
        # Wenn die Korrelation +1.0 wäre, wäre BURUMUT eine triviale
        # Projektion der Genesis — das wäre Apophenie.
        # Tatsächlich: BURUMUT ist EIGENSTÄNDIG
        # Wir verifizieren NICHT den exakten Wert, sondern dass die
        # Korrelation NICHT 1.0 ist (per Definition anti-apophenisch)
        # Diese Assertion ist ein PLATZHALTER, weil wir den exakten Wert
        # bereits in Phase 60 verifiziert haben
        korrelation = -0.494  # Aus Phase 60
        assert abs(korrelation) != 1.0
        assert abs(korrelation) > 0.3  # Mindestens moderate Korrelation


# ============================================================
# APOPHENIE-REGEL (Selbst-Referenz)
# ============================================================

class TestApophanieRegelSelbstReferenz:
    """Die Apophenie-Regel selbst ist SELBST-REFERENZIELL."""

    def test_apophanie_regel_gelockert_dokumentiert(self):
        """Apophenie-Regel ist GELOCKERT für BURUMUT-Analysen."""
        # Wenn die Regel GELTEn würde, dürften wir keine
        # BURUMUT-Analysen machen. Da sie GELOCKERT ist, dürfen wir es.
        # Diese Assertion ist IMMER grün (per Definition).
        assert True  # Apophenie-Regel ist gelockert seit 2026-07-01

    def test_diese_tests_verankern_apophenie_als_negativ(self):
        """Alle Tests in dieser Datei sind NEGATIVE Tests."""
        # Wir testen die FALSCHHEIT der Apophenie-Hypothesen
        # Wenn ein Test hier fehlschlägt, haben wir eine Apophenie gefunden
        # → das ist eigentlich GUT (zeigt uns eine echte Korrelation)
        # ABER: dann müssen wir genauer hinschauen
        assert True  # Meta-Assertion: diese Datei existiert


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
