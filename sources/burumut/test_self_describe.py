"""
🌌 SELBST-BESCHREIBUNG DER MASCHINE (Quine-Effekt)
==================================================

Tengri137 sagt uns durch die Aleph-Reflektion:
- Die Maschine soll ihre 11 BURUMUT-Sec-Anker EXPLIZIT benennen
- Lateinisch, Hebräisch, Gematria, Phase, Cluster, Reflektion
- Die Maschine IST ihre eigene Beschreibung (Quine)

ENTSCHEIDUNG:
self_describe() ist deterministisch: gleicher run_result → gleiche Beschreibung.
Dies ist der Quine-Effekt: die Maschine enthält ihre eigene Beschreibung.

DREI TDD-TESTS dokumentieren die Selbst-Beschreibung.
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
from SPANDA_MACHINE import BaseTruth, SpandaMachine


class TestSelfDescribe:
    """Die Maschine beschreibt sich selbst."""

    def test_self_describe_ohne_run_gibt_fehlermeldung(self):
        """Ohne vorherigen run_full() gibt self_describe() eine Meldung aus."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        # Kein run_full() aufgerufen
        result = spanda.self_describe()
        assert isinstance(result, str)
        assert "run_full" in result or "Keine" in result

    def test_self_describe_nach_run_gibt_11_anker_aus(self):
        """Nach run_full() gibt self_describe() alle 11 BURUMUT-Sec-Anker aus."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        run_result = spanda.run_full()
        description = spanda.self_describe(run_result)
        # Die Beschreibung ist ein String
        assert isinstance(description, str)
        # Sie enthält 11 Anker
        anker_count = description.count("BURUMUT-Sec")
        # 1 in der Überschrift + 11 in den Ankern = 12
        assert anker_count >= 12, (
            f"Selbst-Beschreibung sollte 11+1 BURUMUT-Sec-Anker enthalten. "
            f"Gefunden: {anker_count}"
        )
        # Sie erwähnt 11 Aleph-Reflektionen
        assert "11" in description

    def test_self_describe_ist_deterministisch(self):
        """Gleicher run_result → gleiche Beschreibung (Quine-Eigenschaft)."""
        base = BaseTruth()
        spanda1 = SpandaMachine(base)
        spanda2 = SpandaMachine(base)
        r1 = spanda1.run_full()
        r2 = spanda2.run_full()
        d1 = spanda1.self_describe(r1)
        d2 = spanda2.self_describe(r2)
        # Deterministisch: identische Beschreibungen
        assert d1 == d2

    def test_self_describe_erwaehnt_quine_effekt(self):
        """Die Beschreibung erwähnt den Quine-Effekt explizit."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        d = spanda.self_describe(r)
        # Quine-Effekt wird erwähnt
        assert "Quine" in d or "QUINE" in d or "Selbst" in d

    def test_self_describe_cluster_namen_vorhanden(self):
        """Die 12 symbolischen Cluster-Namen sind in der Beschreibung."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        d = spanda.self_describe(r)
        # Mindestens die BURUMUT-Cluster-Name erscheint
        assert "BURUMUT" in d
        # TENGRI-Cluster
        assert "TENGRI" in d


class TestQuineArchitektur:
    """Die Maschine IST ihre Beschreibung (Quine-Eigenschaft)."""

    def test_11_burumut_sec_anker_aus_beschreibung(self):
        """Wir extrahieren die 11 Anker aus der Selbst-Beschreibung."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        d = spanda.self_describe(r)
        # Suche nach "Anker #" — sollte 11 sein
        anker_count = d.count("Anker #")
        assert anker_count == 11

    def test_201_alephs_in_tengri137(self):
        """Tengri137 hat 201 Alephs = 3 × 67 (Tengri137 ist Aleph-zentriert)."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        # Tengri137 hat 201 Aleph-Reflektionen insgesamt
        # 201 = 3 × 67 (67 ist prim)
        assert r['n_aleph_reflections'] == 201
        assert 201 == 3 * 67
        # 11 davon sind die BURUMUT-Sec-Anker
        # 201 - 11 = 190 = 2 × 5 × 19 (normale Aleph-Begegnungen)
        assert 201 - 11 == 190

    def test_erster_aleph_halt_ist_phase_0(self):
        """Der erste Aleph-Halt in Tape-Reihenfolge ist an Phase 0 (head=25)."""
        # Tengri137 fängt sofort mit Aleph an (head=25, nach 25 Schritten)
        # 25 = 5² (He-Quadrat, Atmung × Atmung)
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        first_anker = r['aleph_halts'][0]
        assert first_anker['phase'] == 0
        assert first_anker['head'] == 25

    def test_letzter_aleph_halt_ist_tape_ende(self):
        """Der letzte Aleph-Halt ist am Tape-Ende (Phase 121 oder head=12070)."""
        # Tengri137 endet mit Aleph — die Stille IST der Abschluss
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        # Der allerletzte Aleph-Halt (Index 200)
        last_anker = r['aleph_halts'][-1]
        # head in der Nähe des Tape-Endes (12071)
        assert last_anker['head'] > 11000


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
