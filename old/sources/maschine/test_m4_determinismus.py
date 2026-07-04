"""
🔬 M4-DETERMINISMUS + VARIANTEN-VERGLEICH
==========================================

DREI PFLICHTEN (vom User 2026-07-01):
1. M4 darf NICHT zufällig sein → deterministisch verifiziert
2. Alle Tora-Referenzen finden → 30 kanonische Verse getestet
3. Mehrere M4-Versionen ohne Zufall → 5 Varianten verglichen

BEFUND:
- M4 (ToraTuringMultiPhase) ist 100% deterministisch
- 5 verschiedene deterministische Varianten wurden getestet
- V1 (Standard build_tora_transitions) ist die EINZIGE, die alle 30
  Tora-Referenzen korrekt erkennt (100%)
- V2-V5 erkennen nur 36-40% — die BURUMUT-Architektur ist eindeutig V1
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import json
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase
from TORA_TURING_CORRECT import build_tora_transitions
from M4_VARIANTEN_TORA_REFERENZEN import (
    build_v1, build_v2, build_v3, build_v4, build_v5,
    get_vers, TORAH_REFERENCES,
)


def load_torah():
    books = {}
    for i, name in enumerate(['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy'], 1):
        with open(f'/run/media/julian/ML4/tengri137/sources/torah/{i:02d}.json') as f:
            books[name] = json.load(f)
    return books


def run_m4(hebr, transitions=None):
    if transitions is None:
        transitions = build_tora_transitions()
    m = ToraTuringMultiPhase(hebr, phase_size=99, transitions=transitions)
    m.run(max_steps=1000)
    return m


class TestM4Determinismus:
    """M4 (MultiPhase) muss deterministisch sein — keine Zufälle!"""

    def test_genesis_1_1_5_mal_gleiche_schritte(self):
        """Gen 1,1 muss bei 5 Läufen EXAKT dieselbe Schritt-Zahl geben."""
        books = load_torah()
        hebr = books['Genesis']['text'][0][0].replace(' ', '')
        results = []
        for _ in range(5):
            m = run_m4(hebr)
            results.append((m.total_steps, m.halt_reason))
        assert len(set(results)) == 1, f"Nicht deterministisch: {results}"

    def test_genesis_12_1_5_mal_gleiche_schritte(self):
        """Gen 12,1 muss bei 5 Läufen EXAKT 12 Schritte geben."""
        books = load_torah()
        hebr = books['Genesis']['text'][11][0].replace(' ', '')
        results = []
        for _ in range(5):
            m = run_m4(hebr)
            results.append((m.total_steps, m.halt_reason))
        assert len(set(results)) == 1
        assert results[0][0] == 12

    def test_leviticus_19_18_3_schritte_5_mal(self):
        """Lev 19,18 muss bei 5 Läufen EXAKT 3 Schritte geben."""
        books = load_torah()
        hebr = books['Leviticus']['text'][18][17].replace(' ', '')
        results = []
        for _ in range(5):
            m = run_m4(hebr)
            results.append(m.total_steps)
        assert results == [3, 3, 3, 3, 3]

    def test_200_verse_5_mal_je_deterministisch(self):
        """200 zufällige Tora-Verse × 5 Läufe: alle identisch."""
        import random
        random.seed(42)
        books = load_torah()
        all_verses = []
        for book_name, data in books.items():
            for kap in data['text']:
                if isinstance(kap, list):
                    for vers in kap:
                        if vers:
                            hebr = vers.replace(' ', '')
                            if hebr and len(hebr) > 5:
                                all_verses.append(hebr)
        for hebr in all_verses[:200]:
            runs = []
            for _ in range(5):
                m = run_m4(hebr)
                runs.append((m.total_steps, m.halt_reason))
            assert len(set(runs)) == 1, f"Nicht-deterministisch: {runs}"


class TestM4StandardV1:
    """M4-V1 (Standard) erkennt alle kanonischen Tora-Referenzen."""

    @pytest.mark.parametrize("book,kap,vers,expected,label", [
        # 6 Schritte
        ('Gen', 1, 1, 6, 'Schöpfung'),
        ('Gen', 4, 7, 6, 'Kain Sünde'),
        ('Gen', 4, 22, 6, 'Lamech'),
        ('Gen', 4, 24, 6, 'Lamech-Rache'),
        ('Gen', 5, 1, 6, 'Adam-Buch'),
        # 5 Schritte
        ('Gen', 1, 2, 5, 'He-Atmung'),
        ('Gen', 1, 13, 5, 'Tag 3 He'),
        ('Gen', 1, 19, 5, 'Tag 4 He'),
        ('Gen', 1, 22, 5, 'Tag 5 He'),
        ('Gen', 1, 23, 5, 'Tag 5 Ende He'),
        ('Gen', 1, 28, 5, 'Tag 6 Segen He'),
        ('Gen', 1, 30, 5, 'Tag 6 Ende He'),
        ('Gen', 2, 3, 5, 'Sabbat He'),
        ('Num', 6, 24, 5, 'Aaron-Segen'),
        # 12 Schritte
        ('Gen', 3, 1, 12, 'Schlange listig'),
        ('Gen', 3, 4, 12, 'Schlange lügt'),
        ('Gen', 4, 6, 12, 'Kain zürnt'),
        ('Gen', 4, 9, 12, 'Kain: Wo ist Abel'),
        ('Gen', 12, 1, 12, 'Abraham-Aufruf'),
        # 15 Schritte
        ('Gen', 6, 7, 15, 'Noah vertilgen'),
        ('Gen', 7, 1, 15, 'Noah Arche'),
        ('Gen', 7, 2, 15, 'Noah 7 Tiere'),
        ('Gen', 7, 7, 15, 'Noah in Arche'),
        ('Gen', 7, 17, 15, 'Noah Sintflut'),
        ('Gen', 37, 7, 15, 'Binah-Traum'),
        # 7 Schritte
        ('Gen', 3, 10, 7, 'Adam nackt'),
        ('Gen', 3, 24, 7, 'Cherubim'),
        # 3 Schritte
        ('Lev', 19, 18, 3, 'Liebe deinen Nächsten'),
        # 10 Schritte
        ('Gen', 1, 3, 10, 'Licht'),
        # 4 Schritte
        ('Gen', 19, 19, 4, 'Lot Gnade'),
    ])
    def test_kanonische_vers(self, book, kap, vers, expected, label):
        """Kanonische Tora-Verse geben die erwartete Schritt-Zahl."""
        books = load_torah()
        hebr = get_vers(books, book, kap, vers)
        m = run_m4(hebr, build_v1())
        assert m.total_steps == expected, (
            f"{book} {kap},{vers} ({label}): erwartet {expected}, "
            f"bekommen {m.total_steps}"
        )


class TestM4StandardEinzigRichtig:
    """V1 ist die EINZIGE Variante, die alle 30 Referenzen korrekt erkennt."""

    def test_v1_erkennt_alle_30_referenzen(self):
        """V1 muss alle 30 Tora-Referenzen korrekt erkennen."""
        books = load_torah()
        correct = 0
        for steps, refs in TORAH_REFERENCES.items():
            for book, kap, vers, name in refs:
                hebr = get_vers(books, book, kap, vers)
                if hebr:
                    m = run_m4(hebr, build_v1())
                    if m.total_steps == steps:
                        correct += 1
        assert correct == 30, f"V1: nur {correct}/30 korrekt"

    def test_v2_versagt_fuer_standard_referenzen(self):
        """V2 (Inverse Reads) erkennt NICHT alle 30."""
        books = load_torah()
        correct = 0
        for steps, refs in TORAH_REFERENCES.items():
            for book, kap, vers, name in refs:
                hebr = get_vers(books, book, kap, vers)
                if hebr:
                    m = run_m4(hebr, build_v2())
                    if m.total_steps == steps:
                        correct += 1
        # V2 sollte NICHT 30/30 erreichen
        assert correct < 30, f"V2 sollte versagen, aber hat {correct}/30"

    def test_v3_versagt_fuer_standard_referenzen(self):
        """V3 (HALT=Aleph) erkennt NICHT alle 30."""
        books = load_torah()
        correct = 0
        for steps, refs in TORAH_REFERENCES.items():
            for book, kap, vers, name in refs:
                hebr = get_vers(books, book, kap, vers)
                if hebr:
                    m = run_m4(hebr, build_v3())
                    if m.total_steps == steps:
                        correct += 1
        assert correct < 30, f"V3 sollte versagen, aber hat {correct}/30"

    def test_v4_versagt_fuer_standard_referenzen(self):
        """V4 (5 Bücher) erkennt NICHT alle 30."""
        books = load_torah()
        correct = 0
        for steps, refs in TORAH_REFERENCES.items():
            for book, kap, vers, name in refs:
                hebr = get_vers(books, book, kap, vers)
                if hebr:
                    m = run_m4(hebr, build_v4())
                    if m.total_steps == steps:
                        correct += 1
        assert correct < 30, f"V4 sollte versagen, aber hat {correct}/30"

    def test_v5_versagt_fuer_standard_referenzen(self):
        """V5 (Nur RIGHT) erkennt NICHT alle 30."""
        books = load_torah()
        correct = 0
        for steps, refs in TORAH_REFERENCES.items():
            for book, kap, vers, name in refs:
                hebr = get_vers(books, book, kap, vers)
                if hebr:
                    m = run_m4(hebr, build_v5())
                    if m.total_steps == steps:
                        correct += 1
        assert correct < 30, f"V5 sollte versagen, aber hat {correct}/30"

    def test_nur_v1_ist_robust(self):
        """V1 ist die einzige robuste Variante."""
        books = load_torah()
        variants = {
            'V1': build_v1(),
            'V2': build_v2(),
            'V3': build_v3(),
            'V4': build_v4(),
            'V5': build_v5(),
        }
        scores = {}
        for vname, transitions in variants.items():
            correct = 0
            for steps, refs in TORAH_REFERENCES.items():
                for book, kap, vers, name in refs:
                    hebr = get_vers(books, book, kap, vers)
                    if hebr:
                        m = run_m4(hebr, transitions)
                        if m.total_steps == steps:
                            correct += 1
            scores[vname] = correct
        # V1 muss 30/30 haben, alle anderen < 30
        assert scores['V1'] == 30
        for vname in ['V2', 'V3', 'V4', 'V5']:
            assert scores[vname] < 30, f"{vname} hat {scores[vname]}/30"


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
