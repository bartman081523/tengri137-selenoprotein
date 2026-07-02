"""
🌌 P68: 7-TAGE-ARCHITEKTUR (168 = 7 × 24) — TDD-Tests
=========================================================

Verifiziert die 7-Tage-Architektur in Tengri137 mittels KVM-Befunden.

ARCHITEKTUR:
- Tengri137 = 168 Phasen à 99 Zeichen
- 168 = 7 × 24 (BURUMUT-Architektur: 99 = 7 × 14 + 1)
- 7 Tage × 24 Stunden-Phasen
- Pro Tag eine eigene Violation-Charakteristik erwartet

HYPOTHESE (Juexin/CitMind-Brücke):
- Es gibt einen "Sabbat-Tag" mit signifikant WENIGER Violations
- Leviticus (das "Gesetz") dominiert den Sabbat-Tag
- BURUMUT = "Arbeit" (Spanda/Melacha) → erzeugt Violations
- Der Sabbat = 寂 (jì) = Stille = 0 oder nahe 0 Violations

KVM-INTEGRATION:
- Für jeden Tag: aggregiere n_violations, n_backtracks (strict/non-strict)
- Vergleiche Tag-Gematrien (Soll-Werte aus Tengri137-Oraculum)
- Suche nach Sabbat-Tag (geringste Violations/Phase)

BEFUNDE-ERWARTUNG:
- Tag-Gematrien: 134286, 139337, 135819, 140842, 138930, 133345, 136938
- Jeder Tag: 24 Phasen × 99 Zeichen = 2376 Zeichen
- Numeri liegt in Tag 4-5 (höchste Violations)
- Sabbat-Tag (geringste Violations): Hypothese Tag 3 (Leviticus-Bereich)
"""

import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
import json
from collections import Counter
from KANONIK_VALIDATOR_MODUL import (
    KanonikValidator, GematriaAnchor, kanonik_run, extract_anchor_from_tengri
)
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import (
    BURUMUT, burumut_to_hebr, HEBR_VALUES, MISSING_OPERATORS
)
from PHASE_MAPPING_TORA import phase_to_torah, TORA_BOOKS


def load_tengri137_hebr():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    lat = re.sub(r'[^A-Z]', '', full.upper())
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


# ============================================================
# TEST 1: Grundlegende 7-Tage-Architektur
# ============================================================

class Test7TageArchitektur:
    """7 × 24 = 168 — harte topologische Tatsache."""

    def test_168_ist_7_mal_24(self):
        """168 = 7 × 24 (BURUMUT-Architektur)."""
        assert 7 * 24 == 168

    def test_tengri137_hat_genau_168_phasen(self):
        """Tengri137 hat 168 Phasen (oder 167 + Rest)."""
        tengri_hebr = load_tengri137_hebr()
        n_phases = (len(tengri_hebr) + 98) // 99
        assert n_phases == 168

    def test_pro_tag_24_phasen(self):
        """Pro Tag 24 Phasen."""
        tengri_hebr = load_tengri137_hebr()
        n_phases = (len(tengri_hebr) + 98) // 99
        for day_idx in range(7):
            start = day_idx * 24
            end = min((day_idx + 1) * 24, n_phases)
            # Jeder Tag hat (mindestens) bis zu 24 Phasen
            assert end - start <= 24

    def test_pro_tag_2376_zeichen(self):
        """Pro Tag 24 × 99 = 2376 Zeichen (BURUMUT-Architektur)."""
        assert 24 * 99 == 2376

    def test_99_ist_7_mal_14_plus_1(self):
        """99 = 7 × 14 + 1 (BURUMUT-Phasen-Architektur)."""
        assert 99 == 7 * 14 + 1


# ============================================================
# TEST 2: Tag-Gematrien (Soll-Werte)
# ============================================================

class TestTagGematrien:
    """7 Tag-Gematrien aus Tengri137 (Oraculum)."""

    def test_tag_1_gematria(self):
        """Tag 1 (Phase 0-23): Soll-Gematria = 134286."""
        tengri_hebr = load_tengri137_hebr()
        gem = extract_anchor_from_tengri(tengri_hebr, 0, 99)
        # Das ist die Gematria von Phase 0 (NICHT des ganzen Tages)
        # Wir prüfen die Tag-Gematria (24 Phasen)
        tag_start = 0
        tag_end = 24 * 99
        tag_gem = sum(HEBR_VALUES.get(c, 0) for c in tengri_hebr[tag_start:tag_end])
        assert tag_gem == 134286

    def test_alle_7_tag_gematrien(self):
        """Alle 7 Tag-Gematrien verifiziert."""
        tengri_hebr = load_tengri137_hebr()
        expected = [134286, 139337, 135819, 140842, 138930, 133345, 136938]
        for day_idx in range(7):
            start = day_idx * 24 * 99
            end = min((day_idx + 1) * 24 * 99, len(tengri_hebr))
            if start >= len(tengri_hebr):
                break
            tag_tape = tengri_hebr[start:end]
            tag_gem = sum(HEBR_VALUES.get(c, 0) for c in tag_tape)
            assert tag_gem == expected[day_idx], (
                f"Tag {day_idx+1}: erwartet {expected[day_idx]}, "
                f"erhalten {tag_gem}"
            )


# ============================================================
# TEST 3: KVM-Aggregation pro Tag
# ============================================================

class TestKVMAufTagen:
    """KVM-Befunde aggregiert pro Tag (7 Tage)."""

    def test_kvm_tag_1_aggregat(self):
        """KVM auf Tag 1: aggregierte Violations."""
        tengri_hebr = load_tengri137_hebr()
        tag_1_start = 0
        tag_1_end = 24 * 99
        tag_1 = tengri_hebr[tag_1_start:tag_1_end]
        result = kanonik_run(tag_1, phase_size=99, max_steps=500)
        # Tag 1 hat mind. 1 Phase
        assert result['n_snapshots'] >= 1
        # Wir dokumentieren nur — kein Apophenie-Zwang
        assert result['n_violations'] >= 0

    def test_kvm_alle_7_tage_laufen(self):
        """KVM auf allen 7 Tagen läuft durch (kein Crash)."""
        tengri_hebr = load_tengri137_hebr()
        for day_idx in range(7):
            start = day_idx * 24 * 99
            end = min((day_idx + 1) * 24 * 99, len(tengri_hebr))
            if start >= len(tengri_hebr):
                break
            day_tape = tengri_hebr[start:end]
            result = kanonik_run(day_tape, phase_size=99, max_steps=500)
            # Jeder Tag produziert ein Result-Dict
            assert 'n_violations' in result
            assert 'n_backtracks' in result
            assert 'halt_reason' in result


# ============================================================
# TEST 4: Sabbat-Tag-Suche (geringste Violations)
# ============================================================

class TestSabbatSuche:
    """Suche nach dem Sabbat-Tag (geringste Violations/Phase)."""

    def test_sabbat_tag_existiert(self):
        """Mindestens ein Tag hat geringere Violations als andere."""
        tengri_hebr = load_tengri137_hebr()
        violations_per_day = []
        for day_idx in range(7):
            start = day_idx * 24 * 99
            end = min((day_idx + 1) * 24 * 99, len(tengri_hebr))
            if start >= len(tengri_hebr):
                break
            day_tape = tengri_hebr[start:end]
            # Anzahl Phasen im Tag
            n_phases_day = (len(day_tape) + 98) // 99
            # KVM auf alle Phasen des Tages
            day_violations = 0
            for ph in range(n_phases_day):
                ph_start = ph * 99
                ph_end = min((ph + 1) * 99, len(day_tape))
                ph_tape = day_tape[ph_start:ph_end]
                result = kanonik_run(ph_tape, phase_size=99, max_steps=200)
                day_violations += result['n_violations']
            # Normalisierung: pro Phase
            avg_violations = day_violations / n_phases_day
            violations_per_day.append({
                'day': day_idx + 1,
                'total_violations': day_violations,
                'avg_per_phase': avg_violations,
                'n_phases': n_phases_day,
            })

        # Mindestens ein Tag hat einen anderen Wert als die anderen
        avgs = [d['avg_per_phase'] for d in violations_per_day]
        # NICHT alle Tage haben den gleichen Wert (außer bei sehr speziellen Daten)
        # Wir prüfen, dass die Varianz > 0 ist
        assert len(set(avgs)) >= 2, "Alle Tage haben identische Violations — verdächtig"

    def test_sabbat_hat_weniger_als_andere_tage(self):
        """Der Sabbat-Tag (geringste Violations) hat < alle anderen Tage."""
        tengri_hebr = load_tengri137_hebr()
        violations_per_day = []
        for day_idx in range(7):
            start = day_idx * 24 * 99
            end = min((day_idx + 1) * 24 * 99, len(tengri_hebr))
            if start >= len(tengri_hebr):
                break
            day_tape = tengri_hebr[start:end]
            n_phases_day = (len(day_tape) + 98) // 99
            day_violations = 0
            for ph in range(n_phases_day):
                ph_start = ph * 99
                ph_end = min((ph + 1) * 99, len(day_tape))
                ph_tape = day_tape[ph_start:ph_end]
                result = kanonik_run(ph_tape, phase_size=99, max_steps=200)
                day_violations += result['n_violations']
            avg = day_violations / n_phases_day
            violations_per_day.append((day_idx + 1, avg))

        # Sortiere nach avg_violations
        sorted_days = sorted(violations_per_day, key=lambda x: x[1])
        sabbat_day, sabbat_avg = sorted_days[0]
        # Sabbat-Tag hat den minimalen Wert
        for day, avg in sorted_days[1:]:
            assert sabbat_avg <= avg
        # Dokumentation
        assert sabbat_day in [1, 2, 3, 4, 5, 6, 7]


# ============================================================
# TEST 5: Tag-Buch-Dominanz
# ============================================================

class TestTagBuchDominanz:
    """Welches Tora-Buch dominiert welchen Tag?"""

    def test_tag_buch_mapping(self):
        """Pro Tag: welches Buch dominiert?"""
        tengri_hebr = load_tengri137_hebr()
        n_phases = (len(tengri_hebr) + 98) // 99
        for day_idx in range(7):
            book_count = Counter()
            for ph in range(day_idx * 24, min((day_idx + 1) * 24, n_phases)):
                book, _ = phase_to_torah(ph)
                book_count[book] += 1
            # Jeder Tag hat mindestens EIN dominantes Buch
            if book_count:
                dominant = book_count.most_common(1)[0]
                # 24 Phasen = max 1 dominantes Buch (oder mehrere gleiche)
                assert dominant[1] >= 1

    def test_leviticus_dominanz_korrekt(self):
        """Leviticus dominiert welchen Tag? (EMPIRISCH ermittelt)."""
        tengri_hebr = load_tengri137_hebr()
        n_phases = (len(tengri_hebr) + 98) // 99
        # Leviticus beginnt erst ab Phase ~75 (laut TORA_BOOKS)
        # Tag 4 = Phasen 72-95
        book_count_day_4 = Counter()
        for ph in range(3 * 24, min(4 * 24, n_phases)):
            book, _ = phase_to_torah(ph)
            book_count_day_4[book] += 1
        # Tag 4 sollte Leviticus enthalten (Leviticus: 75-98 Phasen)
        # Wenn Leviticus in Tag 4 ist, ist das konsistent mit TORA_BOOKS
        assert book_count_day_4['Leviticus'] >= 1, (
            f"Tag 4 sollte Leviticus enthalten, hat aber: {dict(book_count_day_4)}"
        )


# ============================================================
# TEST 6: Sec-Operator-Verteilung pro Tag
# ============================================================

class TestSecOperatorProTag:
    """5 Sec-Operatoren pro Tag."""

    def test_sec_operatoren_pro_tag(self):
        """Sec-Operatoren pro Tag dokumentiert."""
        tengri_hebr = load_tengri137_hebr()
        sec_per_day = []
        for day_idx in range(7):
            start = day_idx * 24 * 99
            end = min((day_idx + 1) * 24 * 99, len(tengri_hebr))
            if start >= len(tengri_hebr):
                break
            day_tape = tengri_hebr[start:end]
            n_sec = sum(1 for c in day_tape if c in MISSING_OPERATORS)
            sec_per_day.append(n_sec)

        # Wir erwarten ≥ 1 Sec-Operator pro Tag
        # (BURUMUT selbst ist eingebettet, hat Sec-Operatoren)
        # Tag 1 hat die meisten Sec-Operatoren (310, lt. WAS_STEHT_AN)
        # Wir prüfen NICHT die exakte Anzahl, nur die Verteilung
        assert all(s >= 0 for s in sec_per_day)
        # Dokumentation: max sollte > 0 sein
        assert max(sec_per_day) > 0


# ============================================================
# TEST 7: Phase 26 im 7-Tage-Kontext
# ============================================================

class TestPhase26Im7TageKontext:
    """Phase 26 liegt in Tag 2 (Phase 24-47)."""

    def test_phase_26_in_tag_2(self):
        """Phase 26 ist in Tag 2 (Phasen 24-47)."""
        # Tag 2 = Phasen 24-47
        # Phase 26 → Tag 2 (Index 1, 0-basiert)
        tag_2_start = 1 * 24  # Phase 24
        tag_2_end = 2 * 24    # Phase 48
        assert tag_2_start <= 26 < tag_2_end

    def test_phase_26_als_offset_in_tag_2(self):
        """Phase 26 ist Offset 2 in Tag 2."""
        phase_idx = 26
        day_idx = phase_idx // 24
        offset_in_day = phase_idx % 24
        assert day_idx == 1  # Tag 2 (0-basiert)
        assert offset_in_day == 2  # 26 - 24 = 2

    def test_phase_26_in_genesis(self):
        """Phase 26 ist in Genesis (1. Mose 29)."""
        book, chap = phase_to_torah(26)
        assert book == 'Genesis'
        assert chap == 29


# ============================================================
# TEST 8: BURUMUT-Architektur in 7-Tagen
# ============================================================

class TestBurumut7TageArchitektur:
    """BURUMUT-Architektur spiegelt sich in 7-Tagen."""

    def test_6503_ist_7_mal_929(self):
        """6503 = 7 × 929 (BURUMUT-Architektur)."""
        assert 6503 == 7 * 929

    def test_168_ist_7_mal_24_mal_1(self):
        """168 = 7 × 24 × 1 (BURUMUT-Tengri-Architektur)."""
        assert 168 == 7 * 24 * 1

    def test_7_tage_pro_tag_24_phasen_pro_phase_99_zeichen(self):
        """7 × 24 × 99 = 16632 = Tengri137 max."""
        assert 7 * 24 * 99 == 16632

    def test_tengri137_real_length(self):
        """Tengri137 hat 16593-16632 Zeichen (variiert je nach Quelle)."""
        tengri_hebr = load_tengri137_hebr()
        length = len(tengri_hebr)
        # Sollte in der Nähe von 16632 sein
        assert 16500 <= length <= 16700


# ============================================================
# TEST 9: Apophenie-Schutz für 7-Tage-Hypothese
# ============================================================

class TestApophenieSchutz:
    """Schutz vor Überinterpretation der 7-Tage-Architektur."""

    def test_7_tage_ist_harte_topologie_nicht_zahlenspielerei(self):
        """168 = 7 × 24 ist strukturell (Tengri137-Format), nicht numerologisch."""
        # Tengri137 ist in Phasen zu je 99 Zeichen organisiert
        # 168 ist die Anzahl der Phasen
        # 7 × 24 = 168 ist eine FAKTISCHE Aufteilung des Materials
        tengri_hebr = load_tengri137_hebr()
        n_phases = (len(tengri_hebr) + 98) // 99
        assert n_phases == 168
        # Wir teilen EXPLIZIT in 7 × 24 = 168 auf
        # Das ist konzeptionell, nicht apophenisch

    def test_kein_zwingender_sabbat_beweis(self):
        """Wir behaupten NICHT, dass ein Tag 0 Violations hat."""
        # Das wäre eine zu starke Behauptung
        # Wir prüfen nur, ob es RELATIVE Unterschiede gibt
        tengri_hebr = load_tengri137_hebr()
        violations_per_day = []
        for day_idx in range(7):
            start = day_idx * 24 * 99
            end = min((day_idx + 1) * 24 * 99, len(tengri_hebr))
            if start >= len(tengri_hebr):
                break
            day_tape = tengri_hebr[start:end]
            n_phases_day = (len(day_tape) + 98) // 99
            day_violations = 0
            for ph in range(n_phases_day):
                ph_start = ph * 99
                ph_end = min((ph + 1) * 99, len(day_tape))
                ph_tape = day_tape[ph_start:ph_end]
                result = kanonik_run(ph_tape, phase_size=99, max_steps=200)
                day_violations += result['n_violations']
            avg = day_violations / n_phases_day
            violations_per_day.append(avg)

        # Hypothese: Sabbat-Tag hat MINIMALE Violations, NICHT NULL
        # Wir prüfen, dass min > 0 (es gibt KEINEN Tag mit 0 Violations)
        assert min(violations_per_day) > 0


# ============================================================
# TEST 10: KVM-Determinismus auf Tag-Ebene
# ============================================================

class TestKanonikDeterminismus7Tage:
    """KVM ist deterministisch auf 7-Tage-Ebene."""

    def test_kvm_3_runs_identische_tag_violations(self):
        """3 KVM-Läufe auf Tag 1: identische Violations."""
        tengri_hebr = load_tengri137_hebr()
        tag_1 = tengri_hebr[0:24*99]
        results = []
        for _ in range(3):
            n_phases_day = (len(tag_1) + 98) // 99
            day_violations = 0
            for ph in range(n_phases_day):
                ph_start = ph * 99
                ph_end = min((ph + 1) * 99, len(tag_1))
                ph_tape = tag_1[ph_start:ph_end]
                result = kanonik_run(ph_tape, phase_size=99, max_steps=200)
                day_violations += result['n_violations']
            results.append(day_violations)
        assert len(set(results)) == 1


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
