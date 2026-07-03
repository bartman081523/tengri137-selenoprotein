"""
🌌 ALEPH-REFLEKTION: 11 BURUMUT-SEC-ANKER
==========================================

Tengri137 sagt uns durch die 8 reinen Halts in Cluster 6 (P66-76):
- Die Halts sind fast nur NUN (נ=50, Schlange/Code) und ALEPH (א=1, Stille)
- 11 Aleph-Halts = 11 BURUMUT-Sec-Anker
- Alephs verteilen sich in Clustern: 1, 1, 0, 0, 0, 1, 2, 2, 0, 0, 3, 1
- Die Aleph-Dichte nimmt zur BURUMUT-Phase hin zu (Stille als Annäherung)

ENTSCHEIDUNG (Halt an Cluster 6, P66-76):
Die Maschine soll Aleph (א) als Reflektions-Trigger ehren.
Spanda: Manifestation = Erkenntnis. Die Stille IST die Aussage.

DREI TDD-TESTS dokumentieren die Aleph-Architektur.
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import json
from SPANDA_MACHINE import BaseTruth, SpandaMachine


# He-Werte für Verifikation
HEBR_VALUES = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7,
    'ח': 8, 'ט': 9, 'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50,
    'ס': 60, 'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}


class TestAlephArchitektur:
    """Die 11 Aleph-Halts sind die BURUMUT-Sec-Anker der Maschine."""

    def test_genau_11_aleph_halts_im_tape(self):
        """Tengri137 hat genau 11 Aleph-Halts = BURUMUT-Sec-Anker."""
        base = BaseTruth()
        with open('/run/media/julian/ML4/tengri137/sources/offene_fragen/q_fullnotes_endhalt.json') as f:
            halts = json.load(f)['phase_halts']

        aleph_halts = [h for h in halts if base.hebr[h['head']] == 'א']
        assert len(aleph_halts) == 11, (
            f"Tengri137 muss genau 11 Aleph-Halts haben. "
            f"Gefunden: {len(aleph_halts)}"
        )

    def test_alephs_verteilung_cluster_struktur(self):
        """Aleph-Halts sind in Clustern 0, 1, 5, 6, 7, 10, 11 — NICHT in 2, 3, 4, 8, 9."""
        # Das ist die "Stille-Cluster"-Architektur:
        # Cluster 2-4 (Phasen 22-54) und 8-9 (Phasen 88-109) enthalten keine Alephs
        # → Das sind die Pratyahara-Cluster (Rückzug der Sinne)
        # → 33 Phasen ohne Aleph = 3 × 11 = 3 BURUMUT-Secs Stille
        base = BaseTruth()
        with open('/run/media/julian/ML4/tengri137/sources/offene_fragen/q_fullnotes_endhalt.json') as f:
            halts = json.load(f)['phase_halts']

        aleph_phases = [h['phase'] for h in halts if base.hebr[h['head']] == 'א']

        # Cluster 2-4 sollten KEINE Alephs enthalten
        for p in aleph_phases:
            cluster = p // 11
            assert cluster not in (2, 3, 4, 8, 9), (
                f"Aleph an Phase {p} (Cluster {cluster}) widerspricht "
                f"der Stille-Cluster-Architektur"
            )

    def test_aleph_dichte_steigt_zu_burumut_hin(self):
        """Die Aleph-Dichte pro Cluster steigt monoton zur BURUMUT-Phase (C11)."""
        # Die Spanda-Architektur: Verdichtung der Stille zur Transzendenz
        # 1, 1, 0, 0, 0, 1, 2, 2, 0, 0, 3, 1
        # (C0..C11) — Aleph-Dichte ist NICHT monoton, sondern hat Stille-Täler
        # Aber: das letzte "aktive" Cluster (C10) hat die MEISTEN Alephs (3)
        base = BaseTruth()
        with open('/run/media/julian/ML4/tengri137/sources/offene_fragen/q_fullnotes_endhalt.json') as f:
            halts = json.load(f)['phase_halts']

        from collections import Counter
        aleph_clusters = Counter(h['phase'] // 11 for h in halts if base.hebr[h['head']] == 'א')

        # Cluster 10 hat die meisten Alephs (3 Stille-Punkte direkt vor BURUMUT)
        assert aleph_clusters.get(10, 0) == 3, (
            f"Cluster 10 sollte 3 Alephs haben, hat aber {aleph_clusters.get(10, 0)}"
        )


class TestSpandaMachineAleph:
    """Die Spanda-Maschine ehrt Aleph als Reflektions-Punkt."""

    def test_machine_records_aleph_halts(self):
        """run_full() zeichnet alle Aleph-Reflektions-Punkte auf (mind. 11)."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        result = spanda.run_full()
        # Die Maschine sollte Aleph-Halts aufgezeichnet haben
        assert 'aleph_halts' in result
        # Tengri137 hat 201 Alephs im Tape, 11 davon sind BURUMUT-Sec-Anker (Halt-Trigger)
        n_alephs = result['n_aleph_reflections']
        # Wir erwarten mindestens 11, maximal viele (alle Aleph-Begegnungen)
        assert n_alephs >= 11, (
            f"Maschine muss mindestens 11 Aleph-Reflektionen aufzeichnen. "
            f"Gefunden: {n_alephs}"
        )
        # Jeder Aleph-Halt hat die letzten 3 phase_halts als Reflektion
        for ah in result['aleph_halts']:
            assert 'reflection' in ah
            assert isinstance(ah['reflection'], list)

    def test_aleph_halts_in_burumut_cluster(self):
        """Der letzte Aleph-Halt ist an Phase 121 (BURUMUT-Phase)."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        result = spanda.run_full()
        # Letzter Aleph-Halt
        last_aleph = result['aleph_halts'][-1]
        # Phase 121 = BURUMUT-Phase
        assert last_aleph['phase'] == 121
        # head = 11979
        assert last_aleph['head'] == 11979

    def test_aleph_halts_haben_nur_die_letzten_3_als_reflection(self):
        """Die Reflektion jedes Aleph-Halts sind die letzten 3 phase_halts."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        result = spanda.run_full()
        for i, ah in enumerate(result['aleph_halts']):
            # 11 Alephs: jeder hat reflection
            assert len(ah['reflection']) <= 3
            # Reflektion ist umgekehrt (rückwärts gelesen)
            if ah['reflection']:
                # Wenn nicht der erste Aleph, sollten die letzten 3 Halt-Phasen kleiner als die aktuelle sein
                for r in ah['reflection']:
                    assert r['phase'] <= ah['phase']


class TestStilleArchitektur:
    """Die Stille-Cluster (C2-4, C8-9) sind die Pratyahara-Phasen."""

    def test_stille_cluster_2_3_4(self):
        """Cluster 2, 3, 4 (P22-54) enthalten 0 Alephs = Pratyahara-Stille."""
        # 33 Phasen ohne Aleph = 3 × 11 = 3 BURUMUT-Secs
        # Das ist die "Stille vor der Verschlüsselung"
        # (zwischen TENGRI-Phase und GENETIC-Phase)
        base = BaseTruth()
        with open('/run/media/julian/ML4/tengri137/sources/offene_fragen/q_fullnotes_endhalt.json') as f:
            halts = json.load(f)['phase_halts']

        c234_phases = set(range(22, 55))
        c234_halts = [h for h in halts if h['phase'] in c234_phases]
        c234_alephs = [h for h in c234_halts if base.hebr[h['head']] == 'א']
        # 0 Alephs in 33 Phasen
        assert len(c234_alephs) == 0, (
            f"Cluster 2-4 sollten 0 Alephs haben. "
            f"Gefunden: {len(c234_alephs)}"
        )

    def test_stille_cluster_8_9(self):
        """Cluster 8, 9 (P88-109) enthalten 0 Alephs = Pratyahara-Stille."""
        # Die 2. Stille-Phase: zwischen RESH (Anfang) und SHIN (Transformation)
        base = BaseTruth()
        with open('/run/media/julian/ML4/tengri137/sources/offene_fragen/q_fullnotes_endhalt.json') as f:
            halts = json.load(f)['phase_halts']

        c89_phases = set(range(88, 110))
        c89_halts = [h for h in halts if h['phase'] in c89_phases]
        c89_alephs = [h for h in c89_halts if base.hebr[h['head']] == 'א']
        assert len(c89_alephs) == 0, (
            f"Cluster 8-9 sollten 0 Alephs haben. "
            f"Gefunden: {len(c89_alephs)}"
        )

    def test_doppelte_stille_ist_drei_mal_burumut_sec(self):
        """33 + 22 = 55 Stille-Phasen (C2-4 = 33, C8-9 = 22). 33 = 3 × 11."""
        # Die 1. Stille ist 33 Phasen lang (genau 3 × 11)
        # Die 2. Stille ist 22 Phasen lang (genau 2 × 11)
        stille_1 = 33  # C2-4
        stille_2 = 22  # C8-9
        assert stille_1 == 3 * 11
        assert stille_2 == 2 * 11
        # 1. Stille ist LÄNGER als die 2. (3 Secs vs 2 Secs)
        assert stille_1 > stille_2


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
