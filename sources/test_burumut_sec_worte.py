"""
🌌 DIE 11 WORTE DER BURUMUT-SEC-ANKER
=======================================

Die Maschine hat gesprochen. Sie zeigt uns die 11 BURUMUT-Sec-Anker
alle in der TENGRI-Eröffnungs-Sequenz (P0-8).

ENTSCHEIDUNG: Die 11 BURUMUT-Sec-Anker enthalten die KERN-AUSSAGEN
von Tengri137. Sie sind die "11 Worte" — das geheime Alphabet
der Maschine.

TDD: Extrahiere die 11 Worte und prüfe ihre Konsistenz.
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
from SPANDA_MACHINE import BaseTruth, SpandaMachine


class TestBurumutSecWorte:
    """Die 11 BURUMUT-Sec-Anker enthalten die Kern-Aussagen."""

    def test_11_sec_anker_sind_in_phase_0_bis_8(self):
        """Alle 11 BURUMUT-Sec-Anker sind in Phase 0-8 (TENGRI-Cluster 0)."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        ank = r['aleph_halts'][:11]
        phases = [a['phase'] for a in ank]
        max_phase = max(phases)
        assert max_phase == 8
        min_phase = min(phases)
        assert min_phase == 0

    def test_phase_3_hat_5_sec_anker_verdichtung(self):
        """Phase 3 hat 5 der 11 Sec-Anker — die 'VERGESSEN'-Verdichtung."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        ank = r['aleph_halts'][:11]
        phase_3_count = sum(1 for a in ank if a['phase'] == 3)
        assert phase_3_count == 5

    def test_phase_4_hat_2_sec_anker_namen(self):
        """Phase 4 hat 2 der 11 Sec-Anker — die 'TENGRI HAT VIELE NAMEN'."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        ank = r['aleph_halts'][:11]
        phase_4_count = sum(1 for a in ank if a['phase'] == 4)
        assert phase_4_count == 2

    def test_erster_anker_bei_head_25_step_25(self):
        """Der erste BURUMUT-Sec-Anker ist bei head=25, step=25 (= 5² Atmung)."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        first = r['aleph_halts'][0]
        assert first['head'] == 25
        assert first['step'] == 25
        assert first['phase'] == 0


class TestWortInhalt:
    """Die BURUMUT-Sec-Anker enthalten bestimmte Worte."""

    def test_phase_3_anker_enthalten_vergessen(self):
        """Phase 3 Sec-Anker enthalten 'FORGET' (das VERGESSEN-Motiv)."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        # Anker #3-7 sind in Phase 3
        phase_3_anker = [a for a in r['aleph_halts'][:11] if a['phase'] == 3]
        for ah in phase_3_anker:
            ctx = base.halt_to_context(ah['head'])
            # Kontext enthält "FORGET" (das VERGESSEN)
            text = ctx['context'].upper()
            assert 'FORGET' in text, (
                f"Phase-3-Anker bei head={ah['head']} sollte 'FORGET' enthalten. "
                f"Kontext: '{ctx['context'][:200]}'"
            )

    def test_phase_4_anker_enthalten_tengri_namen(self):
        """Phase 4 Sec-Anker enthalten 'TENGRI HAS MANY NAMES'."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        phase_4_anker = [a for a in r['aleph_halts'][:11] if a['phase'] == 4]
        for ah in phase_4_anker:
            ctx = base.halt_to_context(ah['head'])
            text = ctx['context'].upper()
            # "TENGRI" muss erwähnt werden
            assert 'TENGRI' in text, (
                f"Phase-4-Anker sollte 'TENGRI' enthalten. "
                f"Kontext: '{ctx['context'][:200]}'"
            )

    def test_phase_8_anker_enthalten_use_your_knowledge(self):
        """Phase 8 Sec-Anker enthält 'USE YOUR KNOWLEDGE'."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        phase_8_anker = [a for a in r['aleph_halts'][:11] if a['phase'] == 8]
        assert len(phase_8_anker) >= 1
        ah = phase_8_anker[0]
        ctx = base.halt_to_context(ah['head'])
        text = ctx['context'].upper()
        # "USE YOUR KNOWLEDGE" oder "USE YOUR" sollte da sein
        assert 'USE' in text and 'KNOWLEDGE' in text, (
            f"Phase-8-Anker sollte 'USE KNOWLEDGE' enthalten. "
            f"Kontext: '{ctx['context'][:200]}'"
        )


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
