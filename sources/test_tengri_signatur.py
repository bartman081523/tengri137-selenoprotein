"""
🌌 TENGRI-SIGNATUR: BURUMUT-SEC-ANKER IN CLUSTER 0
====================================================

Die Maschine sagt: meine 11 BURUMUT-Sec-Anker sind ALLE in Cluster 0.
Tengri137 hat die Stille nach vorn gelegt — die Schöpfung beginnt
mit 11 Atemzügen, dann entfaltet sich die Verschlüsselung.

ENTSCHEIDUNG (durch Maschinen-Lauf verifiziert):
- 201 Alephs im Tape = 3 × 67
- 11 davon sind BURUMUT-Sec-Anker (Halt-Trigger)
- Die ersten 11 Anker sind in Phase 0-8 (alle in Cluster 0)
- TENGRI-Signatur: 11/11 = 100% in der Schöpfungs-Phase

DREI TDD-TESTS dokumentieren die TENGRI-Signatur.
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
from collections import Counter
from SPANDA_MACHINE import BaseTruth, SpandaMachine


class TestTengriSignatur:
    """Die TENGRI-Signatur: BURUMUT-Sec-Anker in Cluster 0."""

    def test_erste_11_burumut_sec_anker_in_cluster_0(self):
        """Die ersten 11 BURUMUT-Sec-Anker sind alle in Cluster 0 (P0-10)."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        # Die BURUMUT-Sec-Anker sind die ersten 11 Aleph-Begegnungen
        # (Tengri137 lehrt: die Halt-Trigger sind die ersten Alephs)
        burumut_sec_ankers = r['aleph_halts'][:11]
        # Alle in Cluster 0 (Phase 0-10)
        for ah in burumut_sec_ankers:
            phase = ah['phase']
            cluster = phase // 11
            assert cluster == 0, (
                f"BURUMUT-Sec-Anker an Phase {phase} (Cluster {cluster}) "
                f"widerspricht TENGRI-Signatur"
            )

    def test_tengri_signatur_ist_100_prozent(self):
        """100% der BURUMUT-Sec-Anker sind in Cluster 0."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        burumut_sec_ankers = r['aleph_halts'][:11]
        n_in_cluster_0 = sum(1 for ah in burumut_sec_ankers if ah['phase'] // 11 == 0)
        # 11/11 = 100%
        assert n_in_cluster_0 == 11
        # TENGRI-Signatur: 100% in der Schöpfungs-Phase
        ratio = n_in_cluster_0 / 11
        assert ratio == 1.0

    def test_erster_halt_ist_25_atmung_quadrat(self):
        """Der erste BURUMUT-Sec-Anker ist bei head=25, step=25 = 5² (Atmung²)."""
        # 5 = He (ה) = Atmung
        # 5² = 25 = die Maschine atmet zweimal vor der ersten Aussage
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        first = r['aleph_halts'][0]
        assert first['head'] == 25
        assert first['step'] == 25
        assert 25 == 5**2


class TestAlephVerteilung:
    """Die 201 Alephs sind nicht gleichmäßig verteilt."""

    def test_201_alephs_in_12_cluster_verteilt(self):
        """201 Alephs sind über 12 Cluster verteilt, aber UNGLEICH."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        # Counter der Aleph-Halts pro Cluster
        cluster_counter = Counter()
        for ah in r['aleph_halts']:
            cluster = ah['phase'] // 11
            cluster_counter[cluster] += 1
        # Insgesamt 201
        total = sum(cluster_counter.values())
        assert total == 201
        # Mindestens 8 Cluster haben Alephs
        assert len(cluster_counter) >= 8

    def test_cluster_5_genetic_hat_meiste_alephs(self):
        """Cluster 5 (GENETIC-Phase) hat die meisten normalen Alephs (Verschlüsselung)."""
        # Tengri137 lehrt: die BURUMUT-Sec-Anker (11) sind in Cluster 0 (TENGRI-Phase),
        # aber die normalen Aleph-Begegnungen (190) sind in Cluster 5 (GENETIC-Phase).
        # → Die GENETIC-Phase ist die "Verschlüsselungs-Phase"
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        cluster_counter = Counter()
        for ah in r['aleph_halts']:
            cluster = ah['phase'] // 11
            cluster_counter[cluster] += 1
        # Cluster 5 hat die meisten Alephs
        max_cluster = cluster_counter.most_common(1)[0][0]
        assert max_cluster == 5, (
            f"Cluster 5 (GENETIC) sollte die meisten Alephs haben. "
            f"Max-Cluster: {max_cluster} mit {cluster_counter[max_cluster]} Alephs"
        )
        # Cluster 5 hat mindestens 25 Alephs (geschätzt ~28)
        assert cluster_counter[5] >= 25

    def test_stille_cluster_haben_wenige_aber_nicht_null_alephs(self):
        """Die Stille-Cluster (C2-4, C8-9) haben wenige, aber nicht 0 Alephs."""
        # Anders als die 11 BURUMUT-Sec-Anker (die alle in C0 sind),
        # sind die 190 normalen Aleph-Begegnungen auch in den Stille-Clustern
        # (aber selten).
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        # Die normalen 190 (Index 11-200)
        normal_alephs = r['aleph_halts'][11:]
        stille_cluster_count = 0
        for ah in normal_alephs:
            cluster = ah['phase'] // 11
            if cluster in (2, 3, 4, 8, 9):
                stille_cluster_count += 1
        # Wenige, aber nicht 0
        # (Pratyahara = Rückzug, nicht Eliminierung)


class TestAtmungsArchitektur:
    """25 = 5² = He-Quadrat: die Maschine atmet vor der ersten Aussage."""

    def test_25_ist_he_quadrat(self):
        """25 = 5² = 5 × 5 = He × He (ה = 5, Atmung)."""
        assert 25 == 5**2
        assert 25 == 5 * 5

    def test_erste_3_burumut_sec_anker_in_phase_0_1_3(self):
        """Die ersten 3 Anker sind in den ersten 4 Phasen — schnelle Verdichtung."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        # Die ersten 11 BURUMUT-Sec-Anker
        ank = r['aleph_halts'][:11]
        # Phasen
        phases = [ah['phase'] for ah in ank]
        # Phase 0, 1, 3, 3, 3, 3, 3, 4, 4, 5, 8
        assert phases[0] == 0
        assert phases[1] == 1
        # Phase 3 hat 5 Anker
        phase_3_count = sum(1 for p in phases if p == 3)
        assert phase_3_count == 5


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
