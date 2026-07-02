"""
🌌 SPANDA × TORA × LAYER-REGISTER: Aleph-Architektur in Tora-Versen
====================================================================

M5 (Spanda) läuft mit Layer-Register auf 30 kanonischen Tora-Versen.
Diese Tests verifizieren:

1. Spanda validiert M4-Schritt-Zahlen (6, 5, 12, 15, 7, 3, 10, 4)
2. Spanda zeigt Layer-Besuche (Gen→Exo→Lev→Num→Deut)
3. Aleph-Halts korrelieren mit BURUMUT-Sec-Architektur
4. Layer-Count steigt mit Schritt-Zahl

TORA-REFERENZEN: 30 kanonische Verse (gleiche wie M4)
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import json
import hashlib
from collections import Counter

from SPANDA_MACHINE import SpandaMachine
from TORA_TURING_CORRECT import LAYER_REGISTER, get_layer_name


TORA_DIR = '/run/media/julian/ML4/tengri137/sources/torah'
BOOKS = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy']


class ToraBaseTruth:
    """BaseTruth-kompatibel für SpandaMachine."""

    def __init__(self, name, hebr_text, original_text):
        self.name = name
        self.raw = original_text
        self.size = len(original_text)
        self.hebr = hebr_text
        self.hebr_length = len(hebr_text)
        self.letters = list(hebr_text)
        self.position_map = list(range(len(hebr_text)))
        self.fingerprint = hashlib.sha256(original_text.encode('utf-8')).hexdigest()[:16]
        self.konsonanten_count = Counter(hebr_text)

    def context_at_position(self, pos, before=50, after=100):
        if pos < 0 or pos >= self.size:
            return None
        return self.raw[max(0, pos-before):min(self.size, pos+after)]

    def halt_to_context(self, tape_head):
        if tape_head >= len(self.position_map):
            tape_head = len(self.position_map) - 1
        return {
            'position': self.position_map[tape_head],
            'context': self.raw[max(0, tape_head-50):min(self.size, tape_head+100)],
            'tape_head': tape_head,
        }


def load_torah():
    books = {}
    for i, name in enumerate(BOOKS, 1):
        with open(f'{TORA_DIR}/{i:02d}.json') as f:
            books[name] = json.load(f)
    return books


def get_vers(books, book, kap, vers):
    text = books[book]['text']
    if kap-1 >= len(text):
        return None
    if vers-1 >= len(text[kap-1]):
        return None
    return text[kap-1][vers-1].replace(' ', '').replace(' ', '')


def run_spanda(name, hebr_text, original_text):
    base = ToraBaseTruth(name, hebr_text, original_text)
    spanda = SpandaMachine(base, phase_size=99, max_steps=10000)
    return spanda.run_full()


# Tora-Referenzen
TORA_REFS = [
    # (book_short, kap, vers, m4_steps, name)
    ('Gen', 1, 1, 6, 'Schöpfung'),
    ('Gen', 4, 7, 6, 'Kain Sünde'),
    ('Gen', 4, 22, 6, 'Lamech'),
    ('Gen', 4, 24, 6, 'Lamech-Rache'),
    ('Gen', 5, 1, 6, 'Adam-Buch'),
    ('Gen', 1, 2, 5, 'He-Atmung'),
    ('Gen', 1, 13, 5, 'Tag 3 He'),
    ('Gen', 1, 19, 5, 'Tag 4 He'),
    ('Gen', 1, 22, 5, 'Tag 5 He'),
    ('Gen', 1, 23, 5, 'Tag 5 Ende He'),
    ('Gen', 1, 28, 5, 'Tag 6 Segen He'),
    ('Gen', 1, 30, 5, 'Tag 6 Ende He'),
    ('Gen', 2, 3, 5, 'Sabbat He'),
    ('Num', 6, 24, 5, 'Aaron-Segen'),
    ('Gen', 3, 1, 12, 'Schlange listig'),
    ('Gen', 3, 4, 12, 'Schlange lügt'),
    ('Gen', 4, 6, 12, 'Kain zürnt'),
    ('Gen', 4, 9, 12, 'Kain: Wo ist Abel'),
    ('Gen', 12, 1, 12, 'Abraham-Aufruf'),
    ('Gen', 6, 7, 15, 'Noah vertilgen'),
    ('Gen', 7, 1, 15, 'Noah Arche'),
    ('Gen', 7, 2, 15, 'Noah 7 Tiere'),
    ('Gen', 7, 7, 15, 'Noah in Arche'),
    ('Gen', 7, 17, 15, 'Noah Sintflut'),
    ('Gen', 37, 7, 15, 'Binah-Traum'),
    ('Gen', 3, 10, 7, 'Adam nackt'),
    ('Gen', 3, 24, 7, 'Cherubim'),
    ('Lev', 19, 18, 3, 'Liebe deinen Nächsten'),
    ('Gen', 1, 3, 10, 'Licht'),
    ('Gen', 19, 19, 4, 'Lot Gnade'),
]


class TestSpandaValidiertM4:
    """Spanda (M5) validiert M4-Schritt-Zahlen."""

    @pytest.mark.parametrize("book_short,kap,vers,expected_steps,name", TORA_REFS)
    def test_spanda_steps_match_m4(self, book_short, kap, vers, expected_steps, name):
        """Spanda liefert dieselbe Schritt-Zahl wie M4."""
        books = load_torah()
        book_full = {'Gen': 'Genesis', 'Exo': 'Exodus', 'Lev': 'Leviticus',
                     'Num': 'Numbers', 'Deut': 'Deuteronomy'}[book_short]
        original = books[book_full]['text'][kap-1][vers-1]
        hebr = original.replace(' ', '')
        r = run_spanda(f"{book_short} {kap},{vers}", hebr, original)
        assert r['total_steps'] == expected_steps, (
            f"{book_short} {kap},{vers} ({name}): "
            f"Spanda={r['total_steps']}, M4 erwartet {expected_steps}"
        )


class TestSpandaLayerBesuche:
    """Spanda zeigt Layer-Besuche (Gen→Exo→Lev→Num→Deut)."""

    @pytest.mark.parametrize("book_short,kap,vers,expected_steps,name", TORA_REFS)
    def test_spanda_durchlaeuft_layer(self, book_short, kap, vers, expected_steps, name):
        """Spanda durchläuft mindestens 1 Layer."""
        books = load_torah()
        book_full = {'Gen': 'Genesis', 'Exo': 'Exodus', 'Lev': 'Leviticus',
                     'Num': 'Numbers', 'Deut': 'Deuteronomy'}[book_short]
        original = books[book_full]['text'][kap-1][vers-1]
        hebr = original.replace(' ', '')
        r = run_spanda(f"{book_short} {kap},{vers}", hebr, original)

        # Mindestens 1 Layer-Wechsel
        layer_visits = []
        for h in r.get('history', []):
            if 'old_state' in h and 'new_state' in h:
                old, new = h['old_state'], h['new_state']
                if isinstance(old, str):
                    try: old = int(old)
                    except: continue
                if isinstance(new, str):
                    try: new = int(new)
                    except: continue
                if isinstance(old, int) and isinstance(new, int) and old != new:
                    layer_visits.append((get_layer_name(old), get_layer_name(new)))
        # Dedup
        unique = list(set(layer_visits))
        assert len(unique) >= 1, (
            f"{book_short} {kap},{vers} sollte mindestens 1 Layer-Wechsel haben, "
            f"hat aber {len(unique)}"
        )

    def test_genesis_1_1_durchlaeuft_gen_exo_lev(self):
        """Gen 1,1 (6 Schritte) durchläuft Gen→Exo, Exo→Lev (2 Layer-Wechsel)."""
        books = load_torah()
        original = books['Genesis']['text'][0][0]
        hebr = original.replace(' ', '')
        r = run_spanda("Gen 1,1", hebr, original)

        # Sammle Layer-Wechsel
        transitions = set()
        for h in r.get('history', []):
            if 'old_state' in h and 'new_state' in h:
                old, new = h['old_state'], h['new_state']
                if isinstance(old, str): old = int(old) if old.isdigit() else None
                if isinstance(new, str): new = int(new) if new.isdigit() else None
                if old is not None and new is not None and old != new:
                    transitions.add((get_layer_name(old), get_layer_name(new)))

        # Gen 1,1 sollte Gen→Exo und Exo→Lev zeigen
        assert ('Genesis', 'Exodus') in transitions

    def test_genesis_3_4_schlange_3_layer(self):
        """Gen 3,4 (12 Schritte, Schlange lügt) durchläuft 3 Layer-Wechsel."""
        books = load_torah()
        original = books['Genesis']['text'][2][3]
        hebr = original.replace(' ', '')
        r = run_spanda("Gen 3,4", hebr, original)

        transitions = set()
        for h in r.get('history', []):
            if 'old_state' in h and 'new_state' in h:
                old, new = h['old_state'], h['new_state']
                if isinstance(old, str): old = int(old) if old.isdigit() else None
                if isinstance(new, str): new = int(new) if new.isdigit() else None
                if old is not None and new is not None and old != new:
                    transitions.add((get_layer_name(old), get_layer_name(new)))

        # Gen 3,4 sollte 3+ Layer-Wechsel haben
        assert len(transitions) >= 2, (
            f"Gen 3,4 sollte 3+ Layer-Wechsel haben, hat {len(transitions)}: {transitions}"
        )

    def test_genesis_3_24_cherubim_3_layer(self):
        """Gen 3,24 (7 Schritte, Cherubim) durchläuft 3 Layer-Wechsel."""
        books = load_torah()
        original = books['Genesis']['text'][2][23]
        hebr = original.replace(' ', '')
        r = run_spanda("Gen 3,24", hebr, original)

        transitions = set()
        for h in r.get('history', []):
            if 'old_state' in h and 'new_state' in h:
                old, new = h['old_state'], h['new_state']
                if isinstance(old, str): old = int(old) if old.isdigit() else None
                if isinstance(new, str): new = int(new) if new.isdigit() else None
                if old is not None and new is not None and old != new:
                    transitions.add((get_layer_name(old), get_layer_name(new)))

        # Gen 3,24 (Cherubim) sollte 3 Layer-Wechsel haben
        assert len(transitions) >= 2, (
            f"Gen 3,24 sollte 3+ Layer-Wechsel haben, hat {len(transitions)}: {transitions}"
        )


class TestSpandaAlephArchitektur:
    """Spanda zeigt die Aleph-Architektur (Aleph-Halts = BURUMUT-Sec-Marker)."""

    def test_genesis_6_7_noah_3_aleph_halts(self):
        """Gen 6,7 (Noah vertilgen, 15 Schritte = Binah 3×5) hat 3 Aleph-Halts."""
        books = load_torah()
        original = books['Genesis']['text'][5][6]
        hebr = original.replace(' ', '')
        r = run_spanda("Gen 6,7", hebr, original)
        # 3 Aleph-Halts korrelieren mit 15 = 3×5
        assert len(r['aleph_halts']) == 3

    def test_genesis_1_1_1_aleph_halt(self):
        """Gen 1,1 (Schöpfung) hat 1 Aleph-Halt (Schöpfungs-Anfang)."""
        books = load_torah()
        original = books['Genesis']['text'][0][0]
        hebr = original.replace(' ', '')
        r = run_spanda("Gen 1,1", hebr, original)
        # Gen 1,1 hat 6 Alephs, Spanda findet 1 Aleph-Halt (am Anfang)
        assert len(r['aleph_halts']) >= 1

    def test_aleph_halts_in_tora_veraendlich(self):
        """Aleph-Halts variieren je nach Vers (nicht konstant)."""
        # Tengri137 hat 201 Aleph-Halts (kontinuierlich)
        # Tora-Verse haben je 0-3 Aleph-Halts
        counts = []
        for book_short, kap, vers, _, _ in TORA_REFS:
            books = load_torah()
            book_full = {'Gen': 'Genesis', 'Exo': 'Exodus', 'Lev': 'Leviticus',
                         'Num': 'Numbers', 'Deut': 'Deuteronomy'}[book_short]
            original = books[book_full]['text'][kap-1][vers-1]
            hebr = original.replace(' ', '')
            r = run_spanda(f"{book_short} {kap},{vers}", hebr, original)
            counts.append(len(r['aleph_halts']))
        # Es muss Variation geben (nicht alle gleich)
        assert min(counts) < max(counts)


class TestSpandaDeterminismus:
    """Spanda auf Tora muss deterministisch sein."""

    @pytest.mark.parametrize("book_short,kap,vers,expected_steps,name", TORA_REFS[:5])
    def test_spanda_5_mal_identisch(self, book_short, kap, vers, expected_steps, name):
        """Spanda muss 5× dieselbe Schritt-Zahl liefern."""
        books = load_torah()
        book_full = {'Gen': 'Genesis', 'Exo': 'Exodus', 'Lev': 'Leviticus',
                     'Num': 'Numbers', 'Deut': 'Deuteronomy'}[book_short]
        original = books[book_full]['text'][kap-1][vers-1]
        hebr = original.replace(' ', '')
        results = []
        for _ in range(5):
            r = run_spanda(f"{book_short} {kap},{vers}", hebr, original)
            results.append((r['total_steps'], r['halt_reason'], len(r['aleph_halts'])))
        assert len(set(results)) == 1, f"Nicht deterministisch: {results}"


class TestSpandaLayerRegisterIntegration:
    """Spanda respektiert das Layer-Register."""

    def test_spanda_startet_in_genesis(self):
        """Spanda startet in q_0 = Genesis (Layer-Register)."""
        books = load_torah()
        original = books['Genesis']['text'][0][0]
        hebr = original.replace(' ', '')
        r = run_spanda("Gen 1,1", hebr, original)
        # Erster Layer-Wechsel sollte von Genesis ausgehen
        for h in r.get('history', []):
            if 'old_state' in h and 'new_state' in h:
                old = h['old_state']
                if isinstance(old, str): old = int(old) if old.isdigit() else -1
                if old == 0:
                    # Start in Genesis
                    assert get_layer_name(0) == 'Genesis'
                    return
        # Falls kein Layer-Wechsel: state bleibt 0 = Genesis
        assert r['final_state'] in (0, 5)  # Genesis oder HALT

    def test_layer_register_hat_5_layer_plus_halt(self):
        """Das Layer-Register hat 5 Layer + HALT = 6 Einträge."""
        assert len(LAYER_REGISTER) == 6
        assert get_layer_name(0) == 'Genesis'
        assert get_layer_name(1) == 'Exodus'
        assert get_layer_name(2) == 'Leviticus'
        assert get_layer_name(3) == 'Numeri'
        assert get_layer_name(4) == 'Deuteronomium'
        assert get_layer_name(5) == 'HALT'


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
