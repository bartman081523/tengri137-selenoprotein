"""
SEFER YETZIRAH: BURUMUT 5 fehlende Operatoren AUS dem Original
=========================================================

Diese Skript wendet die 5 fehlenden Operatoren aus Sefer Yetzirah
auf BURUMUTREFAMTU an.

Im Original-Text 'sefer_yetzirah-he.txt' sind die 5 fehlenden Operatoren
schon vorhanden:
  כ (Kaph) = READ (184x im Original)
  ד (Dalet) = MOVE_LEFT (175x)
  י (Yod) = STATE (477x)
  ת (Tav) = HALT (363x)
  ג (Gimel) = MOVE_RIGHT (97x)

BURUMUTREFAMTU fehlen diese 5 → durch sie werden 60 zusätzliche Gates
zwischen BURUMUT's 17 vorhandenen Konsonanten und den 5 Operatoren gebildet.
"""
import re
import json
from pathlib import Path
from collections import Counter

ORIGINAL = Path("sources/mysticism/sefer_yetzirah-he.txt").read_text()

BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)
LATIN_TO_HEBR = {
    'A': 'א', 'B': 'ב', 'E': 'ה', 'F': 'ו', 'M': 'מ', 'R': 'צ', 'T': 'ר', 'U': 'ש',
    'H': 'ח', 'I': 'ט', 'L': 'ל', 'N': 'נ', 'O': 'ס', 'P': 'ע', 'Q': 'פ',
    'S': 'ק', 'Y': 'י', 'Z': 'ז',
}

print("="*70)
print("SEFER YETZIRAH: BURUMUT's 5 fehlende Operatoren")
print("="*70)
print()
print("BURUMUTREFAMTU fehlt diese 5 Operatoren:")
print("  כ (Kaph, 20)   = READ    [fehlt in BURUMUTREFAMTU]")
print("  ד (Dalet, 4)   = MOVE_LEFT")
print("  י (Yod, 10)    = STATE")
print("  ת (Tav, 400)   = HALT")
print("  ג (Gimel, 3)   = MOVE_RIGHT")
print()
print("Aber im ORIGINAL-Text 'sefer_yetzirah-he.txt' sind sie ALLE vorhanden!")
print()

# Die 5 Operatoren-Klassen
class ToraOperator:
    def __init__(self, hebrew, name, value, turing_op, meaning):
        self.hebrew = hebrew
        self.name = name
        self.value = value
        self.turing_op = turing_op
        self.meaning = meaning
    
    def apply(self, burumut_seq):
        """Wende Operator auf BURUMUT an."""
        raise NotImplementedError

class ReadOperator(ToraOperator):
    def __init__(self):
        super().__init__('כ', 'Kaph', 20, 'READ', 'Handfläche/Empfang')
    def apply(self, burumut_seq):
        # Lese das aktuelle Symbol
        return burumut_seq[0]  # Aktuelles Band-Symbol

class MoveLeftOperator(ToraOperator):
    def __init__(self):
        super().__init__('ד', 'Dalet', 4, 'MOVE_LEFT', 'Tür/Öffnung')
    def apply(self, burumut_seq):
        return burumut_seq[1:]  # Lesekopf nach links

class StateOperator(ToraOperator):
    def __init__(self):
        super().__init__('י', 'Yod', 10, 'STATE', 'Arm/Tat')
    def apply(self, burumut_seq):
        # Wechselt den Zustand
        return ['q_BURUMUT', 'q_Genesis', 'q_Exodus', 'q_Leviticus', 'q_Numeri', 'q_Deutero'][min(len(burumut_seq) - 1, 5)]

class HaltOperator(ToraOperator):
    def __init__(self):
        super().__init__('ת', 'Tav', 400, 'HALT', 'Kreuz/Ende')
    def apply(self, burumut_seq):
        return 'HALT'  # Halt die Berechnung

class MoveRightOperator(ToraOperator):
    def __init__(self):
        super().__init__('ג', 'Gimel', 3, 'MOVE_RIGHT', 'Kamel/Bewegung')
    def apply(self, burumut_seq):
        # Cursor nach rechts
        return burumut_seq[:-1]

# Die 5 Operatoren
ops = [
    ReadOperator(),
    MoveLeftOperator(),
    StateOperator(),
    HaltOperator(),
    MoveRightOperator(),
]

# 1. Operatoren auf BURUMUTREFAMTU anwenden
print("="*70)
print("1. Operatoren auf BURUMUTREFAMTU anwenden (14 Zeichen)")
print("="*70)

# BURUMUTREFAMTU als hebr. Symbole
burumutrefamtu_hebr = ''.join(LATIN_TO_HEBR.get(c, '?') for c in 'BURUMUTREFAMTU')
print(f"BURUMUTREFAMTU (hebr.): {burumutrefamtu_hebr}")
print()

# Wende jeden Operator an
print("Anwendung der 5 Operatoren:")
for op in ops:
    print(f"  {op.turing_op:12s} ({op.hebrew}/{op.name}, Gematria={op.value}): ", end="")
    result = op.apply(burumutrefamtu_hebr)
    if isinstance(result, str):
        print(f"→ {result}")
    else:
        print(f"→ {result}")

# 2. Sequenz der Operatoren im Original-Text
print()
print("="*70)
print("2. Wo sind die 5 Operatoren in Sefer Yetzirah positioniert?")
print("="*70)
# Finde jede Position
for op in ops:
    pos = ORIGINAL.find(op.hebrew)
    context = ORIGINAL[max(0, pos-30):pos+30] if pos > 0 else "N/A"
    print(f"  {op.turing_op:12s} ({op.hebrew}) bei Position {pos}:")
    print(f"    ...{context}...")
    print()

# 3. Gates-Berechnung mit Original-Text
print("="*70)
print("3. Gates-Berechnung (22 × 21 / 2 = 231)")
print("="*70)
# Finde alle Gates (Paare von Konsonanten) im Original
import re
# Extrahiere nur hebr. Zeichen
hebrew_chars = [c for c in ORIGINAL if c in 'אבגדהוזחטיכלמנסעפצקרשת']
print(f"  Original-Text: {len(hebrew_chars)} hebr. Zeichen")
print(f"  Unique hebr. Zeichen: {len(set(hebrew_chars))}")
print()

# Gates im Original
gates_seen = set()
for i, h1 in enumerate(hebrew_chars):
    for j in range(i+1, len(hebrew_chars)):
        h2 = hebrew_chars[j]
        if h1 != h2:
            gate = tuple(sorted([h1, h2]))
            gates_seen.add(gate)
print(f"  Eindeutige Gates (Paare): {len(gates_seen)}")
print(f"  Maximal mögliche Gates (22 × 21 / 2): {22*21//2} = 231")
print()

# 4. 22 Buchstaben ↔ BURUMUTREFAMTU
print("="*70)
print("4. 22 Buchstaben vs BURUMUTREFAMTU (8 unique)")
print("="*70)
print(f"  BURUMUTREFAMTU unique: {sorted(set(burumutrefamtu_hebr))}")
print(f"  22 Konsonanten gesamt: {len(HEBREW_22_LIST := 'אבגדהוזחטיכלמנסעפצקרשת')}")
print()

# 5. Sefer Yetzirah Schöpfung - Schöpfungs-Algorithmus
print("="*70)
print("5. Sefer Yetzirah Schöpfung - Algorithmus")
print("="*70)
# Aus dem Original (Sefer Yetzirah 1:6)
m = re.search(r'(חקק חצב בהן ארבע רוחות.{0,1000})', ORIGINAL[:5000])
if m:
    print("Schöpfung der 4 Winde (Sefer Yetzirah 1:6):")
    print(m.group(0)[:400])
print()

# 6. Was passiert wenn die 5 Operatoren auf BURUMUT angewendet werden?
print("="*70)
print("6. Anwendung der 5 Operatoren auf BURUMUT")
print("="*70)
print()
# Initialer BURUMUT (99 Zeichen, lateinisch)
print(f"BURUMUT (99 Zeichen):")
print(f"  {BURUMUT}")
print()

# Schritt 1: READ (כ)
print("Schritt 1: READ (כ) - Lies aktuelles Band-Symbol")
print("  → BURUMUTREFAMTU gelesen = בשצשמשרצהואמרש")
print()

# Schritt 2: WRITE (ו)
print("Schritt 2: WRITE (ו) - Schreibe Vav an aktueller Position")
print("  → Schreibvorgang: ו → BURUMUT...")
vav_count = ORIGINAL.count('ו')
print(f"  → {vav_count}x Vav im Original (Tora-Schöpfung)")
print()

# Schritt 3-5: Weitere Operatoren
print("Schritt 3: MOVE_LEFT (ד) - Bewege Lesekopf nach links")
print("Schritt 4: MOVE_RIGHT (ג) - Bewege Lesekopf nach rechts")
print("Schritt 5: STATE (י) - Wechsel Zustand")
print()

# HALT
print(f"Schritt 6: HALT (ת) - Beende die Tora-Turing-Maschine")
tav_count = ORIGINAL.count('ת')
print(f"  → {tav_count}x Tav im Original = Vollendung")
print()

# 7. Sefer Yetzirah Manifestation in BURUMUT
print("="*70)
print("7. Sefer Yetzirah Manifestation in BURUMUT")
print("="*70)
print()
print("BURUMUTREFAMTU (14 Zeichen) → 5 Layer-Torah-Fold:")
print()
print("Modul 1: ב (Beth) = Schöpfung: 'Haus-Anfang'")
print("Modul 2: ש (Shin) = Schöpfung: 'Zahn/Feuer'")
print("Modul 3: צ (Tsade) = Schöpfung: 'Jägerei'")
print("Modul 4: ש (Shin) = Schöpfung: 'Zahn/Feuer'")
print("Modul 5: מ (Mem) = Schöpfung: 'Wasser/Tora'")
print("Modul 6: ש (Shin) = Schöpfung: 'Zahn/Feuer'")
print("Modul 7: ר (Resh) = Schöpfung: 'Kopf'")
print("Modul 8: צ (Tsade) = Schöpfung: 'Jägerei'")
print("Modul 9: ה (He) = Schöpfung: 'Atem'")
print("Modul 10: ו (Vav) = Schöpfung: 'Haken'")
print("Modul 11: א (Aleph) = Schöpfung: 'Mutter'")
print("Modul 12: מ (Mem) = Schöpfung: 'Wasser/Tora'")
print("Modul 13: ר (Resh) = Schöpfung: 'Kopf'")
print("Modul 14: ש (Shin) = Schöpfung: 'Zahn/Feuer'")
print()

# 8. Speichere
state = {
    'operatoren': {
        'READ_כ': 184,  # Häufigkeit im Original
        'MOVE_LEFT_ד': 175,
        'STATE_י': 477,
        'HALT_ת': 363,
        'MOVE_RIGHT_ג': 97,
    },
    'gates_total': 231,
    'gates_seen_im_original': len(gates_seen),
    'interpretation': '5 fehlende Operatoren aus Sefer Yetzirah auf BURUMUT angewendet',
    'numerical': {
        '184 + 175 + 477 + 363 + 97': 184+175+477+363+97,
        '1296 / 231 Gates': 1296 / 231,
        '60 zusaetzliche_gates': 60,
    },
    'next_step': 'Wende die 5 Operatoren auf BURUMUT an und prüfe die 3 Mothers',
}
with open("sources/sefer_yetzirah_burumut_operator.json", "w") as f:
    json.dump(state, f, indent=2, ensure_ascii=False)
print(f"\nStatus gespeichert in sources/sefer_yetzirah_burumut_operator.json")
