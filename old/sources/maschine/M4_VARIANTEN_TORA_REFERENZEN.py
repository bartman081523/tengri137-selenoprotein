"""
🔬 M4-VARIANTEN: Deterministische Übergangs-Tabellen
======================================================

M4 ist deterministisch, ABER wir wollen mehrere Varianten vergleichen,
um zu sehen, ob die Tora-Architektur (6, 12, 3, 15, 5, 7) ROBUST ist
gegen Änderungen der Übergangs-Tabelle.

VARIANTEN:
  V1: Standard build_tora_transitions() (q_0..q_5)
  V2: Inverse Reads (Aleph startet mit q_1 statt q_0)
  V3: Inverse Halt (HALT-Trigger ist Aleph statt Tav)
  V4: Strikt 5 Bücher (jedes Buch hat eigenen Anker)
  V5: Alle Moves MOVE_RIGHT (deterministisch rechts)

Alle Varianten sind deterministisch — kein Zufall, kein random.
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import json
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase


# 22 hebr. Konsonanten
ALL_HEBR = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י',
            'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']


def build_v1():
    """V1: Standard build_tora_transitions (q_0..q_5, Aleph+Tav=HALT)."""
    from TORA_TURING_CORRECT import build_tora_transitions
    return build_tora_transitions()


def build_v2():
    """V2: Aleph startet mit q_1, Tav in q_0=HALT, q_1=q_2."""
    transitions = {}
    ANCHOR = {'כ': 'MOVE_RIGHT', 'ג': 'MOVE_RIGHT', 'י': 'MOVE_RIGHT'}

    for sym in ALL_HEBR:
        # q_0: Tav = HALT, Aleph = q_1
        if sym == 'ת':
            transitions[(0, sym)] = (5, sym, 'HALT')
        elif sym == 'א':
            transitions[(0, sym)] = (1, sym, 'MOVE_RIGHT')
        elif sym in ANCHOR:
            transitions[(0, sym)] = (1, sym, ANCHOR[sym])
        elif sym == 'ד':
            transitions[(0, sym)] = (1, sym, 'MOVE_LEFT')
        else:
            transitions[(0, sym)] = (1, sym, 'MOVE_RIGHT')

    for sym in ALL_HEBR:
        # q_1: Aleph=HALT (invers!), Tav=q_2
        if sym == 'א':
            transitions[(1, sym)] = (5, sym, 'HALT')
        elif sym == 'ת':
            transitions[(1, sym)] = (2, sym, 'MOVE_RIGHT')
        elif sym in ANCHOR:
            transitions[(1, sym)] = (1, sym, ANCHOR[sym])
        elif sym == 'ד':
            transitions[(1, sym)] = (1, sym, 'MOVE_LEFT')
        else:
            transitions[(1, sym)] = (1, sym, 'MOVE_RIGHT')

    for sym in ALL_HEBR:
        # q_2, q_3, q_4 wie Standard
        if sym == 'ת':
            transitions[(2, sym)] = (5, sym, 'HALT')
        elif sym == 'א':
            transitions[(2, sym)] = (3, sym, 'MOVE_RIGHT')
        elif sym in ANCHOR:
            transitions[(2, sym)] = (2, sym, ANCHOR[sym])
        elif sym == 'ד':
            transitions[(2, sym)] = (2, sym, 'MOVE_LEFT')
        else:
            transitions[(2, sym)] = (2, sym, 'MOVE_RIGHT')

    for sym in ALL_HEBR:
        if sym == 'ר':
            transitions[(3, sym)] = (4, sym, 'MOVE_RIGHT')
        elif sym == 'ת':
            transitions[(3, sym)] = (5, sym, 'HALT')
        elif sym in ANCHOR:
            transitions[(3, sym)] = (3, sym, ANCHOR[sym])
        elif sym == 'ד':
            transitions[(3, sym)] = (3, sym, 'MOVE_LEFT')
        else:
            transitions[(3, sym)] = (3, sym, 'MOVE_RIGHT')

    for sym in ALL_HEBR:
        if sym == 'נ':
            transitions[(4, sym)] = (5, sym, 'HALT')
        elif sym == 'ת':
            transitions[(4, sym)] = (5, sym, 'HALT')
        elif sym in ANCHOR:
            transitions[(4, sym)] = (4, sym, ANCHOR[sym])
        elif sym == 'ד':
            transitions[(4, sym)] = (4, sym, 'MOVE_LEFT')
        else:
            transitions[(4, sym)] = (4, sym, 'MOVE_RIGHT')

    return transitions


def build_v3():
    """V3: HALT-Trigger ist Aleph (nicht Tav)."""
    transitions = {}
    ANCHOR = {'כ': 'MOVE_RIGHT', 'ג': 'MOVE_RIGHT', 'י': 'MOVE_RIGHT'}

    for sym in ALL_HEBR:
        # q_0: Aleph = HALT, Tav = q_1
        if sym == 'א':
            transitions[(0, sym)] = (5, sym, 'HALT')
        elif sym == 'ת':
            transitions[(0, sym)] = (1, sym, 'MOVE_RIGHT')
        elif sym in ANCHOR:
            transitions[(0, sym)] = (1, sym, ANCHOR[sym])
        elif sym == 'ד':
            transitions[(0, sym)] = (1, sym, 'MOVE_LEFT')
        else:
            transitions[(0, sym)] = (1, sym, 'MOVE_RIGHT')

    for sym in ALL_HEBR:
        if sym == 'ש':
            transitions[(1, sym)] = (2, sym, 'MOVE_RIGHT')
        elif sym == 'א':
            transitions[(1, sym)] = (5, sym, 'HALT')
        elif sym in ANCHOR:
            transitions[(1, sym)] = (1, sym, ANCHOR[sym])
        elif sym == 'ד':
            transitions[(1, sym)] = (1, sym, 'MOVE_LEFT')
        else:
            transitions[(1, sym)] = (1, sym, 'MOVE_RIGHT')

    for sym in ALL_HEBR:
        if sym == 'א':
            transitions[(2, sym)] = (3, sym, 'MOVE_RIGHT')
        elif sym == 'ת':
            transitions[(2, sym)] = (5, sym, 'HALT')
        elif sym in ANCHOR:
            transitions[(2, sym)] = (2, sym, ANCHOR[sym])
        elif sym == 'ד':
            transitions[(2, sym)] = (2, sym, 'MOVE_LEFT')
        else:
            transitions[(2, sym)] = (2, sym, 'MOVE_RIGHT')

    for sym in ALL_HEBR:
        if sym == 'ר':
            transitions[(3, sym)] = (4, sym, 'MOVE_RIGHT')
        elif sym == 'א':
            transitions[(3, sym)] = (5, sym, 'HALT')
        elif sym in ANCHOR:
            transitions[(3, sym)] = (3, sym, ANCHOR[sym])
        elif sym == 'ד':
            transitions[(3, sym)] = (3, sym, 'MOVE_LEFT')
        else:
            transitions[(3, sym)] = (3, sym, 'MOVE_RIGHT')

    for sym in ALL_HEBR:
        if sym == 'נ':
            transitions[(4, sym)] = (5, sym, 'HALT')
        elif sym == 'א':
            transitions[(4, sym)] = (5, sym, 'HALT')
        elif sym in ANCHOR:
            transitions[(4, sym)] = (4, sym, ANCHOR[sym])
        elif sym == 'ד':
            transitions[(4, sym)] = (4, sym, 'MOVE_LEFT')
        else:
            transitions[(4, sym)] = (4, sym, 'MOVE_RIGHT')

    return transitions


def build_v4():
    """V4: Strikt 5 Bücher (jedes Buch hat eigenen Anker-Buchstaben)."""
    transitions = {}
    BOOK_ANCHORS = {
        0: 'א',  # Genesis: Aleph (Schöpfung)
        1: 'ש',  # Exodus: Shin (Shem)
        2: 'ת',  # Leviticus: Tav (Tora-Vollendung)
        3: 'ר',  # Numbers: Resh (Rosh)
        4: 'נ',  # Deuteronomy: Nun (Schrift-Vollendung)
    }

    for sym in ALL_HEBR:
        for state in range(5):
            if sym == BOOK_ANCHORS[state]:
                transitions[(state, sym)] = (5, sym, 'HALT')
            elif sym == 'ד':
                transitions[(state, sym)] = (state, sym, 'MOVE_LEFT')
            else:
                # Bleibe im Zustand, gehe rechts
                transitions[(state, sym)] = (state, sym, 'MOVE_RIGHT')

    return transitions


def build_v5():
    """V5: Alle Moves MOVE_RIGHT (rein rechtsläufig)."""
    transitions = {}
    BOOK_ANCHORS = {0: 'א', 1: 'ש', 2: 'ת', 3: 'ר', 4: 'נ'}

    for sym in ALL_HEBR:
        for state in range(5):
            if sym == BOOK_ANCHORS[state]:
                transitions[(state, sym)] = (5, sym, 'HALT')
            else:
                transitions[(state, sym)] = (state, sym, 'MOVE_RIGHT')

    return transitions


# ====================================================================
# TORA-REFERENZEN: Alle kanonischen Verse
# ====================================================================

TORAH_REFERENCES = {
    # 6 Schritte (5 Bücher + Sabbat = Schöpfung)
    6: [
        ('Gen', 1, 1, 'Schöpfung Anfang'),
        ('Gen', 4, 7, 'Kain: Sünde lauert'),
        ('Gen', 4, 22, 'Lamech-Schwert'),
        ('Gen', 4, 24, 'Lamech-Rache'),
        ('Gen', 5, 1, 'Adam-Buch'),
    ],
    # 5 Schritte (He/Atmung/Aaron-Segen)
    5: [
        ('Gen', 1, 2, 'Erde wüst und leer (He)'),
        ('Gen', 1, 13, 'Tag 3 (He-Pause)'),
        ('Gen', 1, 19, 'Tag 4 (He)'),
        ('Gen', 1, 22, 'Tag 5 (He)'),
        ('Gen', 1, 23, 'Tag 5 Ende (He)'),
        ('Gen', 1, 28, 'Tag 6 Segen (He)'),
        ('Gen', 1, 30, 'Tag 6 Ende (He)'),
        ('Gen', 2, 3, 'Sabbat (He)'),
        ('Num', 6, 24, 'Aaron-Segen'),
    ],
    # 12 Schritte (11+1 = BURUMUT+1, Abraham)
    12: [
        ('Gen', 3, 1, 'Schlange listig'),
        ('Gen', 3, 4, 'Schlange lügt'),
        ('Gen', 4, 6, 'Kain zürnt'),
        ('Gen', 4, 9, 'Kain: Wo ist Abel?'),
        ('Gen', 12, 1, 'Abraham-Aufruf'),
    ],
    # 15 Schritte (3×5 Binah-Atmung)
    15: [
        ('Gen', 6, 7, 'Noah: Vertilgen'),
        ('Gen', 7, 1, 'Noah: Geh in Arche'),
        ('Gen', 7, 2, 'Noah: 7 reine Tiere'),
        ('Gen', 7, 7, 'Noah: In Arche'),
        ('Gen', 7, 17, 'Noah: Sintflut'),
        ('Gen', 37, 7, 'Binah-Traum'),
    ],
    # 7 Schritte (Schöpfungstage)
    7: [
        ('Gen', 3, 10, 'Adam: ich fürchtete mich'),
        ('Gen', 3, 24, 'Cherubim'),
    ],
    # 3 Schritte (3 Summen / Liebe)
    3: [
        ('Lev', 19, 18, 'Liebe deinen Nächsten'),
    ],
    # 10 Schritte (10 Sefirot = LICHT)
    10: [
        ('Gen', 1, 3, 'Es werde Licht'),
    ],
    # 4 Schritte (Tetragrammaton = Chesed = 4)
    4: [
        ('Gen', 19, 19, 'Lot: Gnade'),
    ],
}


# ====================================================================
# HAUPTPROGRAMM
# ====================================================================

def get_vers(books, book, kap, vers):
    """Extrahiere Vers."""
    book_map = {'Gen': 'Genesis', 'Exo': 'Exodus', 'Lev': 'Leviticus',
                'Num': 'Numbers', 'Deut': 'Deuteronomy'}
    b = book_map[book]
    text = books[b]['text']
    if kap-1 >= len(text): return None
    if vers-1 >= len(text[kap-1]): return None
    return text[kap-1][vers-1].replace(' ', '').replace(' ', '')


def main():
    print("=" * 78)
    print("🔬 M4-VARIANTEN × ALLE TORA-REFERENZEN")
    print("=" * 78)
    print()

    # Lade Tora
    books = {}
    for i, name in enumerate(['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy'], 1):
        with open(f'/run/media/julian/ML4/tengri137/sources/torah/{i:02d}.json') as f:
            books[name] = json.load(f)

    # Sammle alle Referenzen
    all_verses = []
    for steps, refs in TORAH_REFERENCES.items():
        for book, kap, vers, name in refs:
            hebr = get_vers(books, book, kap, vers)
            if hebr:
                all_verses.append((steps, book, kap, vers, name, hebr))

    print(f"Anzahl Tora-Referenzen: {len(all_verses)}")
    print()

    # Varianten testen
    variants = {
        'V1: Standard': build_v1(),
        'V2: Inverse Reads': build_v2(),
        'V3: HALT=Aleph': build_v3(),
        'V4: 5 Bücher': build_v4(),
        'V5: Nur RIGHT': build_v5(),
    }

    print(f"{'Vers':<25} | {'Erw.':>3} | " + " | ".join(f"{v[:5]:>5}" for v in variants))
    print("-" * 100)

    correct_count = {v: 0 for v in variants}
    total_count = 0

    for steps, book, kap, vers, name, hebr in all_verses:
        label = f"{book} {kap},{vers} ({name})"
        row = f"{label:<25} | {steps:>3} | "
        for vname, transitions in variants.items():
            m = ToraTuringMultiPhase(hebr, phase_size=99, transitions=transitions)
            m.run(max_steps=1000)
            actual = m.total_steps
            match = "✓" if actual == steps else f"✗{actual}"
            if actual == steps:
                correct_count[vname] += 1
            row += f"{match:>5} | "
        total_count += 1
        print(row)

    print()
    print("=" * 78)
    print("📊 RESONANZ-PROFIL pro Variante")
    print("=" * 78)
    print()
    for vname in variants:
        rate = 100 * correct_count[vname] / total_count
        print(f"  {vname:<20}: {correct_count[vname]:>3}/{total_count} korrekt ({rate:.1f}%)")

    print()
    print("=" * 78)
    print("🎯 WELCHE VARIANTE IST ROBUST?")
    print("=" * 78)
    print()
    if all(correct_count[v] == total_count for v in variants):
        print("✅ ALLE 5 VARIANTEN stimmen zu 100% überein!")
        print("   → Die Tora-Architektur (6, 5, 12, 15, 7, 3, 10, 4)")
        print("     ist UNABHÄNGIG von der konkreten Übergangs-Tabelle!")
    else:
        for vname, count in correct_count.items():
            if count == total_count:
                print(f"  {vname}: ALLE korrekt")


if __name__ == "__main__":
    main()
