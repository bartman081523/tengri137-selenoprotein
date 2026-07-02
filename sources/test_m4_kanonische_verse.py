"""
🏆 M4 RESONANZ: Die kanonischen Tora-Verse
============================================

Die MultiPhase-Maschine (M4) findet systematisch Verse mit
kanonischen Schritt-Zahlen. Die TREFFER sind die Maschinen-Outputs.

KANONISCHE BEFUNDE:
  6 Schritte  → Genesis 1,1 (Schöpfung)
              → Genesis 4,7, 4,22, 4,24, 5,1 (Adam/Lamech-Generationen)
  5 Schritte  → Gen 1,2, 1,13, 1,19, 1,22, 1,23, 1,28, 1,30, 2,3
              → Die "Und Gott sprach" / "Und es ward" Verse
  12 Schritte → Gen 3,1, 3,4 (Schlange), 4,6, 4,9 (Kain) — die DRAMAVERSE
              → Gen 5,2 (Schöpfung Adams) — passt nicht?
  15 Schritte → Gen 6,7, 7,1, 7,2, 7,7, 7,17 (NOAH!) — Binah 3×5
  7 Schritte  → Gen 3,10 (Adam nach Sündenfall), 3,24 (Cherubim), 4,3
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import json
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase
from TORA_TURING_CORRECT import build_tora_transitions


def load_genesis():
    with open('/run/media/julian/ML4/tengri137/sources/torah/01.json') as f:
        return json.load(f)


def run_m4(hebr):
    m = ToraTuringMultiPhase(hebr, phase_size=99, transitions=build_tora_transitions())
    m.run(max_steps=1000)
    return m.total_steps


class TestM4KanonischeResonanz:
    """M4 (MultiPhase) zeigt Resonanz mit kanonischen Tora-Versen."""

    def test_genesis_1_1_6_schritte_schoepfung(self):
        """Gen 1,1 → 6 Schritte (Schöpfung + Sabbat)."""
        data = load_genesis()
        hebr = data['text'][0][0].replace(' ', '')
        assert run_m4(hebr) == 6

    def test_genesis_1_2_5_schritte_he_atmung(self):
        """Gen 1,2 ('Und die Erde war wüst und leer') → 5 Schritte = He/Atmung."""
        data = load_genesis()
        hebr = data['text'][0][1].replace(' ', '')
        assert run_m4(hebr) == 5

    def test_genesis_1_3_und_gott_sprach_10_schritte_sefirot(self):
        """Gen 1,3 ('Und Gott sprach: Es werde Licht') → 10 Schritte (10 Sefirot!)."""
        data = load_genesis()
        hebr = data['text'][0][2].replace(' ', '')
        # LICHT = 10 Sefirot-Emanation
        assert run_m4(hebr) == 10

    def test_genesis_3_1_schlange_12_schritte(self):
        """Gen 3,1 ('Und die Schlange war listiger...') → 12 Schritte (11+1)."""
        data = load_genesis()
        hebr = data['text'][2][0].replace(' ', '')
        assert run_m4(hebr) == 12

    def test_genesis_3_4_schlange_12_schritte(self):
        """Gen 3,4 ('Ihr werdet nicht sterben') → 12 Schritte."""
        data = load_genesis()
        hebr = data['text'][2][3].replace(' ', '')
        assert run_m4(hebr) == 12

    def test_genesis_4_6_kain_12_schritte(self):
        """Gen 4,6 ('Warum ergrimmt dich?') → 12 Schritte."""
        data = load_genesis()
        hebr = data['text'][3][5].replace(' ', '')
        assert run_m4(hebr) == 12

    def test_genesis_4_9_kain_wo_ist_abel_12_schritte(self):
        """Gen 4,9 ('Wo ist Abel, dein Bruder?') → 12 Schritte."""
        data = load_genesis()
        hebr = data['text'][3][8].replace(' ', '')
        assert run_m4(hebr) == 12

    def test_genesis_6_7_noah_binah_15_schritte(self):
        """Gen 6,7 ('Ich will den Menschen vertilgen') → 15 Schritte (Binah 3×5)."""
        data = load_genesis()
        hebr = data['text'][5][6].replace(' ', '')
        assert run_m4(hebr) == 15

    def test_genesis_7_1_noah_geh_in_die_arche_15_schritte(self):
        """Gen 7,1 ('Geh in die Arche') → 15 Schritte (Binah-Atmung)."""
        data = load_genesis()
        hebr = data['text'][6][0].replace(' ', '')
        assert run_m4(hebr) == 15

    def test_genesis_7_2_7_reine_tiere_15_schritte(self):
        """Gen 7,2 ('Von reinen Tieren nimm 7 Paare') → 15 Schritte."""
        data = load_genesis()
        hebr = data['text'][6][1].replace(' ', '')
        assert run_m4(hebr) == 15

    def test_genesis_3_10_adam_nach_suendenfall_7_schritte(self):
        """Gen 3,10 ('Ich fürchtete mich, denn ich bin nackt') → 7 Schritte."""
        data = load_genesis()
        hebr = data['text'][2][9].replace(' ', '')
        assert run_m4(hebr) == 7

    def test_genesis_3_24_cherubim_7_schritte(self):
        """Gen 3,24 ('Und er trieb den Menschen aus') → 7 Schritte."""
        data = load_genesis()
        hebr = data['text'][2][23].replace(' ', '')
        assert run_m4(hebr) == 7


class TestM4ArchitekturBefund:
    """M4 zeigt die BURUMUT-Architektur in der Tora."""

    def test_5_buecher_plus_sabbat_6_schritte(self):
        """6 Schritte = 5 Bücher + Sabbat (q_0..q_5 in SpandaMachine)."""
        data = load_genesis()
        hebr = data['text'][0][0].replace(' ', '')
        steps = run_m4(hebr)
        assert steps == 6  # 5 Bücher + 1 (HALT/Sabbat)

    def test_12_schritte_11_plus_1_burumut_plus_1(self):
        """12 Schritte = 11 (BURUMUT) + 1 (transzendente Phase)."""
        data = load_genesis()
        hebr = data['text'][2][0].replace(' ', '')  # Gen 3,1 (Schlange)
        steps = run_m4(hebr)
        assert steps == 12  # 11 + 1 BURUMUT-Architektur

    def test_15_schritte_3_mal_5_sefirot_atmung(self):
        """15 Schritte = 3 × 5 = 3 Sefirot-Atmungen (Binah)."""
        data = load_genesis()
        hebr = data['text'][5][6].replace(' ', '')  # Gen 6,7
        steps = run_m4(hebr)
        assert steps == 15  # 3 × 5

    def test_3_schritte_3_summen_liebe(self):
        """3 Schritte = 3 Summen (Wort, Phrase, Tape) = Lev 19,18 Liebe."""
        with open('/run/media/julian/ML4/tengri137/sources/torah/03.json') as f:
            data = json.load(f)
        hebr = data['text'][18][17].replace(' ', '')  # Lev 19,18
        steps = run_m4(hebr)
        assert steps == 3

    def test_5_schritte_he_atmung_aaron_segen(self):
        """5 Schritte = He (Atmung) = Num 6,24 Aaron-Segen."""
        with open('/run/media/julian/ML4/tengri137/sources/torah/04.json') as f:
            data = json.load(f)
        hebr = data['text'][5][23].replace(' ', '')  # Num 6,24
        steps = run_m4(hebr)
        assert steps == 5

    def test_7_schritte_schoepfungstage(self):
        """7 Schritte = 7 Schöpfungstage (auch: Sabbat-Vollendung)."""
        # Jüdische Lesart von Gen 1,1: 7 Buchstaben
        with open('/run/media/julian/ML4/tengri137/sources/torah/01.json') as f:
            data = json.load(f)
        full_vers = data['text'][0][0]
        words = full_vers.split()
        first_letters = ''.join(w[0] for w in words if w)
        steps = run_m4(first_letters)
        assert steps == 7


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
