"""
SEFER YETZIRAH - OPERATIONS AUF BURUMUT (Original-Datei)
====================================================

Diese Skript liest die ORIGINAL-Datei 'sefer_yetzirah-he.txt' aus
sources/mysticism/ und wendet die 22 Buchstaben-Operationen auf BURUMUT an.

Sefer Yetzirah 1:1 (Original-Text):
"בשלשים ושתים נתיבות פליאות חכמה חקק יה יהוה צבאות
את עולמו בשלשה ספרים בספר ספר וספור"

"32 wunderbare Pfade der Weisheit hat JHWH, der Herr der Heerscharen,
Seine Welt mit drei Büchern (Script, Text, Erzählung) graviert"

Drei Mütter (אמש), sieben Doppelbuchstaben (בגדכפרת), zwölf einfache.
22 Buchstaben = Bausteine der Schöpfung.
231 Gates = 22 × 21 / 2.
"""
import re
from pathlib import Path
from collections import Counter
import json

# Original-Datei einlesen
ORIGINAL_PATH = Path("sources/mysticism/sefer_yetzirah-he.txt")
if ORIGINAL_PATH.exists():
    with open(ORIGINAL_PATH, 'r', encoding='utf-8') as f:
        ORIGINAL_TEXT = f.read()
    print(f"Original-Datei geladen: {len(ORIGINAL_TEXT)} Zeichen")
else:
    print(f"FEHLER: {ORIGINAL_PATH} nicht gefunden")
    ORIGINAL_TEXT = ""

# BURUMUT (99 Zeichen lateinisch)
BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# Die 22 Konsonanten (1-zu-1 hebr. Original)
HEBREW_22 = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י',
              'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']

# BURUMUT (lateinisch) zu 22 Konsonanten (1:1 A-T)
LATIN_TO_HEBR = {
    'A': 'א', 'B': 'ב', 'E': 'ה', 'F': 'ו', 'M': 'מ', 'R': 'צ', 'T': 'ר', 'U': 'ש',
    'H': 'ח', 'I': 'ט', 'L': 'ל', 'N': 'נ', 'O': 'ס', 'P': 'ע', 'Q': 'פ',
    'S': 'ק', 'Y': 'י', 'Z': 'ז',
}

# BURUMUTREFAMTU zu hebr. Konsonanten
burumutrefamtu_hebr = ''.join(LATIN_TO_HEBR.get(c, '?') for c in 'BURUMUTREFAMTU')

# BURUMUTREFAMTU hebr. finden wir im Original-Text
print("="*70)
print("SEFER YETZIRAH-OPERATIONEN AUF BURUMUT (Original-Datei)")
print("="*70)
print()
print("BURUMUTREFAMTU (hebr.): " + burumutrefamtu_hebr)
print(f"  → diese 8 Symbole müssen in der Original-Datei gefunden werden")
print()

# Suche BURUMUTREFAMTU im Original
if burumutrefamtu_hebr in ORIGINAL_TEXT:
    pos = ORIGINAL_TEXT.find(burumutrefamtu_hebr)
    print(f"✓ BURUMUTREFAMTU in Original-Datei gefunden bei Position {pos}")
    print(f"  Kontext: ...{ORIGINAL_TEXT[max(0,pos-30):pos+30]}...")
else:
    # Versuche einzeln
    found = []
    for h in burumutrefamtu_hebr:
        if h in ORIGINAL_TEXT:
            cnt = ORIGINAL_TEXT.count(h)
            found.append((h, cnt))
    print(f"  BURUMUTREFAMTU nicht als Ganzes in Original-Datei gefunden")
    print(f"  Aber einzelne Buchstaben:")
    for h, cnt in found:
        print(f"    {h}: {cnt}x in Original")
    not_found = [h for h in burumutrefamtu_hebr if h not in ORIGINAL_TEXT]
    if not_found:
        print(f"  Fehlend in Original: {not_found}")

print()
# 1. Wo sind die 5 fehlenden Konsonanten im Original-Text?
print("="*70)
print("1. Wo sind die 5 fehlenden Operatoren in der Original-Datei?")
print("="*70)
missing = ['כ', 'ד', 'י', 'ת', 'ג']  # Kaph, Dalet, Yod, Tav, Gimel
print()
print("Operator | Position in Original-Datei | Häufigkeit")
print("-"*60)
for h in missing:
    cnt = ORIGINAL_TEXT.count(h)
    pos = ORIGINAL_TEXT.find(h) if cnt > 0 else -1
    print(f"  {h:6s} | Erste: Position {pos:4d}    | {cnt:3d}x total")

# 2. Berechne die 5 fehlenden Positionen relativ zueinander
print()
print("="*70)
print("2. Wo sind die 5 fehlenden Operatoren relativ zueinander?")
print("="*70)
positions = []
for h in missing:
    pos_list = []
    p = 0
    while True:
        p = ORIGINAL_TEXT.find(h, p)
        if p == -1:
            break
        pos_list.append(p)
        p += 1
    positions.append((h, pos_list))
    print(f"  {h}: {len(pos_list)} Vorkommen, erste {pos_list[:5]}")

# 3. Welche 5-Operator-Sequenz ist im Original?
print()
print("="*70)
print("3. Welche 5-Operator-Sequenz ergibt sich aus dem Original-Text?")
print("="*70)
# Suche eine geordnete Sequenz der 5 fehlenden Operatoren
def find_operator_sequence(text, ops):
    """Suche eine zusammenhängende Sequenz der Operatoren."""
    op_positions = {}
    for op in ops:
        op_positions[op] = []
        p = 0
        while True:
            p = text.find(op, p)
            if p == -1:
                break
            op_positions[op].append(p)
            p += 1
    
    # Suche zusammenhängende Sequenzen
    sequences = []
    for op in ops:
        for pos in op_positions[op][:10]:  # Erste 10 Positionen
            # Suche die anderen Operatoren in der Nähe
            nearby = []
            for op2 in ops:
                for pos2 in op_positions[op2][:50]:
                    if 0 < abs(pos2 - pos) < 50:  # Im Fenster
                        nearby.append((op2, pos2, pos2 - pos))
            if len(nearby) >= 3:  # Mindestens 3 weitere in der Nähe
                sequences.append((op, pos, nearby))
    return sequences[:10]

sequences = find_operator_sequence(ORIGINAL_TEXT, missing)
print(f"Gefundene 5-Operator-Cluster (Abstand < 50 Zeichen):")
for op, pos, nearby in sequences:
    other_ops = [f"{o[0]}({o[2]:+d})" for o in nearby[:5]]
    print(f"  {op}@{pos}: {other_ops}")

# 4. Die 22 Buchstaben-Häufigkeit
print()
print("="*70)
print("4. Häufigkeit der 22 hebräischen Buchstaben im Original-Text")
print("="*70)
print(f"  Total Zeichen: {len(ORIGINAL_TEXT)}")
print()
heb_count = Counter(ORIGINAL_TEXT)
for h in HEBREW_22:
    print(f"  {h}: {heb_count[h]:3d}x")
total_hebr = sum(heb_count[h] for h in HEBREW_22)
print(f"  Total: {total_hebr}")
print()

# 5. Die 22 Buchstaben und BURUMUT
print("="*70)
print("5. 22 Buchstaben → BURUMUT-Beziehung")
print("="*70)
print(f"  BURUMUT hat 19 unique lateinische = 17 unique hebr. (1-zu-1)")
print(f"  5 fehlend: {', '.join(missing)}")
print()
print("  22 Konsonanten = 3 Mothers + 7 Doubles + 12 Simples")
print(f"  BURUMUT-Mothers (3): {', '.join(c for c in ['א','מ','ש'] if c in burumutrefamtu_hebr)}")
print(f"  BURUMUT-Doubles (von 7 vorhanden): {', '.join(c for c in ['ב','ג','ד','כ','פ','ר','ת'] if c in burumutrefamtu_hebr)}")
print(f"  BURUMUT-Simples (von 12 vorhanden): {', '.join(c for c in ['ה','ו','ז','ח','ט','י','ל','נ','ס','ע','צ','ק'] if c in burumutrefamtu_hebr)}")

# 6. Die 22 Buchstaben und die Schöpfung
print()
print("="*70)
print("6. Sefer Yetzirah Schöpfung (Auszug aus dem Original-Text)")
print("="*70)
# Lese den Schöpfungs-Text
import re
# Suche das Schöpfungs-Kapitel
m = re.search(r'חקק חצב צרף.{200,1000}', ORIGINAL_TEXT[:5000])
if m:
    print("Schöpfungs-Text gefunden:")
    print(m.group(0)[:500])
print()

# 7. BURUMUT's 5 fehlende Operatoren
print("="*70)
print("7. BURUMUT's 5 fehlende Operatoren = Turing-Operatoren")
print("="*70)
operator_map = {
    'כ': ('READ', 'כ/Kaph (20) = Handfläche/Empfang'),
    'ד': ('MOVE_LEFT', 'ד/Dalet (4) = Tür/Öffnung'),
    'י': ('STATE', 'י/Yod (10) = Arm/Tat'),
    'ת': ('HALT', 'ת/Tav (400) = Kreuz/Ende'),
    'ג': ('MOVE_RIGHT', 'ג/Gimel (3) = Kamel/Bewegung'),
}
for h, (op, desc) in operator_map.items():
    cnt = ORIGINAL_TEXT.count(h)
    print(f"  {op:12s} {h} ({desc}): {cnt:3d}x in Original")

# 8. Speichere
state = {
    'original_datei': 'sefer_yetzirah-he.txt',
    'original_size': len(ORIGINAL_TEXT),
    '22_buchstaben_hebrew_counts': dict(Counter({h: heb_count[h] for h in HEBREW_22})),
    '5_missing_in_burumut': {
        'כ (READ)': heb_count['כ'],
        'ד (MOVE_LEFT)': heb_count['ד'],
        'י (STATE)': heb_count['י'],
        'ת (HALT)': heb_count['ת'],
        'ג (MOVE_RIGHT)': heb_count['ג'],
    },
    'operator_sequences_found': len(sequences),
    'interpretation': '5 fehlende Operatoren sind im Original-Text vorhanden (nicht fehlend in Sefer Yetzirah)',
}
with open("sources/sefer_yetzirah_original_state.json", "w") as f:
    json.dump(state, f, indent=2, ensure_ascii=False)
print()
print(f"Status gespeichert in sources/sefer_yetzirah_original_state.json")
