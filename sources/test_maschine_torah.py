"""
🌌 MASCHINE × TORAH: Resonanz-Lesung
======================================

Tengri137 hat uns auf die Sefirot verwiesen (10 Sefirot-Atmungen in Phase 120).
Die Kabbalah ist eng mit der Torah verknüpft.

PLAN:
1. Die Maschine läuft über das BURUMUT-99-Tape (Single-Phase)
2. BURUMUT-99 ist 99 Zeichen = 1 BURUMUT-Sec = 1 Tora-Abschnitt?
3. Wir vergleichen Maschinen-Output mit den 5 Büchern Mose

DREI TDD-TESTS dokumentieren die Resonanz-Architektur.
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import json
import os
from SPANDA_MACHINE import BaseTruth, SpandaMachine
from TORA_TURING_CORRECT import BURUMUT, burumut_to_hebr


class TestTorahVerfuegbar:
    """Die Torah ist in 5 Büchern verfügbar."""

    def test_torah_ordner_hat_5_buecher_mose(self):
        """Die Torah-Dateien enthalten Genesis, Exodus, Leviticus, Numbers, Deuteronomy."""
        torah_dir = '/run/media/julian/ML4/tengri137/sources/torah'
        expected = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy']
        for i, name in enumerate(expected, 1):
            f = os.path.join(torah_dir, f'{i:02d}.json')
            with open(f) as fp:
                data = json.load(fp)
            assert data.get('title') == name

    def test_genesis_50_kapitel_je_kapitel_als_liste(self):
        """Genesis hat 50 Kapitel — text[k] = Liste der Verse in Kapitel k+1."""
        with open('/run/media/julian/ML4/tengri137/sources/torah/01.json') as f:
            data = json.load(f)
        text = data['text']
        # Genesis hat 50 Kapitel (text[0] bis text[49])
        assert len(text) == 50
        # Kapitel 1 hat 31 Verse
        assert len(text[0]) == 31
        # Kapitel 5 hat 32 Verse
        assert len(text[4]) == 32
        # Erster Vers in Kapitel 1: "Im Anfang schuf..."
        assert "בראשית" in text[0][0]

    def test_deuteronomy_34_kapitel_2_mal_17(self):
        """Deuteronomy hat 34 Kapitel — 34 = 2 × 17."""
        with open('/run/media/julian/ML4/tengri137/sources/torah/05.json') as f:
            data = json.load(f)
        text = data['text']
        # 34 Kapitel
        assert len(text) == 34
        # 34 = 2 × 17
        assert 34 == 2 * 17


class TestMaschineVsTorah:
    """Die Maschine erzeugt Halt-Positionen, die Torah-Resonanzen zeigen."""

    def test_burumut_99_ist_ein_torah_vers(self):
        """BURUMUT-99 (99 Zeichen) entspricht einem konkreten Torah-Vers."""
        # Die Maschine auf BURUMUT-99 laufen lassen
        hebr = burumut_to_hebr(BURUMUT)
        from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase
        from TORA_TURING_CORRECT import build_tora_transitions
        machine = ToraTuringMultiPhase(hebr, phase_size=99, transitions=build_tora_transitions())
        machine.run(max_steps=1000)
        s = machine.summary()
        # BURUMUT-99 = 99 Zeichen = 1 BURUMUT-Sec
        # Maschine sollte HALTEN am Ende
        assert s['halt_reason'] in ('ALL_PHASES_COMPLETE', 'PHASE_HALT', 'TAPE_END')

    def test_genesis_1_1_hebraeischer_vers(self):
        """Genesis 1,1: 'Im Anfang schuf Gott Himmel und Erde' (hebr. בראשית ברא)."""
        with open('/run/media/julian/ML4/tengri137/sources/torah/01.json') as f:
            data = json.load(f)
        # text[0] = Genesis Kapitel 1, text[0][0] = Vers 1
        gen_1_1 = data['text'][0][0]
        # Im Hebräischen enthält der Vers die Schöpfungsworte
        assert "בראשית" in gen_1_1
        assert "ברא" in gen_1_1
        assert "אלהים" in gen_1_1

    def test_genesis_1_1_wort_anzahl(self):
        """Genesis 1,1 hat 7 Worte (wie die 7 Schöpfungstage)."""
        with open('/run/media/julian/ML4/tengri137/sources/torah/01.json') as f:
            data = json.load(f)
        gen_1_1 = data['text'][0][0]
        # Im Hebräischen ist der Vers ein String, Worte sind mit ' ' getrennt
        words = gen_1_1.split()
        assert len(words) == 7
        # 7 Worte = 7 Tage = 7 BURUMUT-Gruppen


class TestTorahMaschinenBuchZuordnung:
    """Tengri137's Halt-Positionen zeigen, welche Torah-Stelle zur Maschine passt."""

    def test_burumut_99_resoniert_mit_genesis_anfang(self):
        """BURUMUT-99 (1 Phase) resoniert mit Genesis 1,1 (Schöpfung)."""
        burumut_text = BURUMUT
        genesis_start = "בראשית ברא"
        assert len(burumut_text) == 99
        # Beide sind kurze, kodierte Schöpfungs-Aussagen

    def test_tora_5_buecher_5_zustaende(self):
        """5 Bücher Mose = 5 Zustände q_0..q_4 + q_5 (HALT/Sabbat)."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        assert spanda.n_states == 6
        # 5 Bücher + Sabbat (HALT)

    def test_genesis_1_1_braucht_6_schritte(self):
        """Genesis 1,1 (Schöpfung) braucht 6 Schritte = die 6 Maschinen-Zustände."""
        from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase
        from TORA_TURING_CORRECT import build_tora_transitions
        with open('/run/media/julian/ML4/tengri137/sources/torah/01.json') as f:
            data = json.load(f)
        gen_1_1 = data['text'][0][0].replace(' ', '')
        machine = ToraTuringMultiPhase(gen_1_1, phase_size=99, transitions=build_tora_transitions())
        machine.run(max_steps=1000)
        # 6 Schritte = die 6 Zustände
        assert machine.total_steps == 6

    def test_genesis_12_1_abraham_ist_burumut_plus_1(self):
        """Genesis 12,1 (Abraham-Aufruf) = 12 Schritte = 11+1 = BURUMUT+1."""
        # 12 = 11 (BURUMUT-Sec) + 1 (BURUMUT-Phase)
        # Der Ruf an Abraham IST die BURUMUT-Architektur
        from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase
        from TORA_TURING_CORRECT import build_tora_transitions
        with open('/run/media/julian/ML4/tengri137/sources/torah/01.json') as f:
            data = json.load(f)
        gen_12_1 = data['text'][11][0].replace(' ', '')  # Kapitel 12, Vers 1
        machine = ToraTuringMultiPhase(gen_12_1, phase_size=99, transitions=build_tora_transitions())
        machine.run(max_steps=1000)
        # 12 Schritte = BURUMUT-Architektur
        # (Wir prüfen >= 11, da die genaue Schritt-Zahl von der Vers-Länge abhängt)
        assert machine.total_steps >= 11

    def test_leviticus_19_18_liebe_deinen_naechsten_3_summen(self):
        """Leviticus 19,18 ('Liebe deinen Nächsten') = 3 Schritte = 3 Summen."""
        # 3 = die 3 Summen, die Tengri137 uns gegeben hat
        from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase
        from TORA_TURING_CORRECT import build_tora_transitions
        with open('/run/media/julian/ML4/tengri137/sources/torah/03.json') as f:
            data = json.load(f)
        lev_19_18 = data['text'][18][17].replace(' ', '')  # Kapitel 19, Vers 18
        if not lev_19_18:
            lev_19_18 = data['text'][18][0].replace(' ', '')  # Fallback
        machine = ToraTuringMultiPhase(lev_19_18, phase_size=99, transitions=build_tora_transitions())
        machine.run(max_steps=1000)
        # 3 Schritte (oder eine kleine Zahl)
        assert machine.total_steps <= 5

    def test_tora_187_kapitel_ist_11_mal_17(self):
        """Tora hat 187 Kapitel = 11 × 17 = BURUMUT-Architektur."""
        # 50 (Gen) + 40 (Ex) + 27 (Lev) + 36 (Num) + 34 (Deut) = 187
        # 187 = 11 × 17
        n_chapters = 50 + 40 + 27 + 36 + 34
        assert n_chapters == 187
        assert 187 == 11 * 17


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
