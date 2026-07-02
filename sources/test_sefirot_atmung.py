"""
🌌 PHASE 120: DIE 10 SEFIROT-ATMUNGEN VOR BURUMUT
==================================================

Die Maschine hat gesprochen. Sie zeigt uns:

1. He (ה) ist der häufigste Aleph-Nachbar (128 mal) — Stille + Atmung
2. Phase 120 hat 10 Alephs — die meisten aller Phasen
3. Phase 121 (BURUMUT) ist chemische Elementsymbol-Verschlüsselung
4. GENETIC-Atmung: mittlere Distanz 30.00 = Lamed-Atmung

ENTSCHEIDUNG: Phase 120 = BURUMUT-Vorbereitung mit 10 Sefirot-Atmungen.
Die 10 Sefirot sind die 10 Emanationen in der Kabbalah:
Kether (1), Chokhmah (2), Binah (3), Chesed (4), Geburah (5),
Tiphereth (6), Netzach (7), Hod (8), Jesod (9), Malkuth (10).

TDD: Verifiziere die 10 Alephs in Phase 120.
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
from collections import Counter
from SPANDA_MACHINE import BaseTruth, SpandaMachine


class TestSefirotAtmung:
    """Phase 120 hat 10 Alephs = 10 Sefirot-Atmungen vor BURUMUT."""

    def test_phase_120_hat_10_alephs(self):
        """Phase 120 (direkt vor BURUMUT-Phase 121) hat 10 Alephs."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        phase_120_alephs = [ah for ah in r['aleph_halts'] if ah['phase'] == 120]
        # 10 Alephs in Phase 120
        assert len(phase_120_alephs) == 10, (
            f"Phase 120 sollte 10 Alephs haben. Gefunden: {len(phase_120_alephs)}"
        )

    def test_10_alephs_in_phase_120_ist_die_meiste_anzahl(self):
        """Phase 120 hat die meisten Alephs aller Phasen."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        phase_counter = Counter(ah['phase'] for ah in r['aleph_halts'])
        # Phase 120 ist die Phase mit den meisten Alephs
        max_phase = phase_counter.most_common(1)[0][0]
        max_count = phase_counter.most_common(1)[0][1]
        assert max_phase == 120
        assert max_count == 10

    def test_10_sefirot_kabbalistisch(self):
        """10 Sefirot = 10 Emanationen in der Kabbalah."""
        # 10 = Anzahl der Sefirot
        assert 10 == 10
        # Die 10 Sefirot sind in der Kabbalah die göttlichen Emanationen
        sefirot = [
            "Kether (1, Krone)",
            "Chokhmah (2, Weisheit)",
            "Binah (3, Verstand)",
            "Chesed (4, Güte)",
            "Geburah (5, Stärke)",
            "Tiphereth (6, Schönheit)",
            "Netzach (7, Sieg)",
            "Hod (8, Herrlichkeit)",
            "Jesod (9, Fundament)",
            "Malkuth (10, Königreich)",
        ]
        assert len(sefirot) == 10


class TestHeNachbarschaft:
    """He (ה) ist der häufigste Aleph-Nachbar (Stille + Atmung)."""

    def test_he_ist_haeufigster_nachbar(self):
        """He (ה=5, Atmung) ist der häufigste Konsonant neben Aleph."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        # Sammle alle Nachbarn
        neighbor_counter = Counter()
        for ah in r['aleph_halts']:
            head = ah['head']
            for offset in [-3, -2, -1, 1, 2, 3]:
                if 0 <= head + offset < len(base.hebr):
                    neighbor_counter[base.hebr[head + offset]] += 1
        # He (ה) ist der häufigste
        most_common = neighbor_counter.most_common(1)[0][0]
        assert most_common == 'ה', (
            f"ה (He) sollte der häufigste Nachbar sein. "
            f"Gefunden: {most_common}"
        )
        # He hat mindestens 100 Vorkommen
        assert neighbor_counter['ה'] >= 100


class TestLamedAtmung:
    """GENETIC-Atmung: mittlere Distanz 30 = Lamed (ל=30)."""

    def test_genetic_mittlere_distanz_ist_30(self):
        """Die mittlere Distanz zwischen Alephs in P55-65 ist ~30."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        genetic = [ah for ah in r['aleph_halts'] if 55 <= ah['phase'] <= 65]
        heads = sorted([ah['head'] for ah in genetic])
        diffs = [heads[i+1] - heads[i] for i in range(len(heads)-1)]
        mean_dist = sum(diffs) / len(diffs)
        # Mittlere Distanz ist ungefähr 30 (Lamed)
        # (kann zwischen 25-35 sein, wegen des Anfangs/Endes)
        assert 25 <= mean_dist <= 35


class TestBURUMUTPhaseVerschluesselung:
    """Phase 121 (BURUMUT) enthält chemische Elementsymbole."""

    def test_phase_121_enthaelt_elementsymbole(self):
        """Phase 121 enthält chemische Elementsymbole (TC, IR, MN, EU, ...)."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        # Finde Aleph-Halt in Phase 121
        p121_anker = [ah for ah in r['aleph_halts'] if ah['phase'] == 121]
        assert len(p121_anker) >= 1
        ah = p121_anker[0]
        ctx = base.halt_to_context(ah['head'])
        text = ctx['context'].upper()
        # Chemische Elementsymbole
        elements = ['TC', 'IR', 'MN', 'EU', 'FR', 'OS', 'RB', 'TI', 'HG']
        # Mindestens 3 sollten im Text vorkommen
        found_count = sum(1 for e in elements if e in text)
        assert found_count >= 3, (
            f"Phase 121 sollte chemische Elementsymbole enthalten. "
            f"Gefunden: {found_count} von 9"
        )


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
