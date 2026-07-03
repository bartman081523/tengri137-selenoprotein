"""
TORA-TURING-MASCHINE v2 (KORRIGIERT)
====================================

Diese Skript verwendet die HEBRÄISCHEN KONSONANTEN als Symbole,
nicht die lateinischen BURUMUT-Zeichen.

Das ist die korrekte Implementierung:
- Band = hebr. Konsonanten (BURUMUT 1:1 zu hebr. abgebildet)
- 5 Operatoren = die 5 fehlenden hebr. Konsonanten
- 5-Layer-Torah-Fold als Übergangs-Tabelle

BURUMUT's 5 fehlende hebr. Konsonanten = 5 Turing-Operatoren:
  - READ (כ/Kaph, 20)
  - WRITE (ו/Vav, 6) - aber vorhanden in BURUMUT (lat. W)
  - MOVE_LEFT (ד/Dalet, 4)
  - MOVE_RIGHT (ג/Gimel, 3)
  - HALT (ת/Tav, 400)
  - STATE (י/Yod, 10) (Transition)
"""
import json
from collections import Counter

# BURUMUT (lateinisch, 99 Zeichen)
BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# 22 hebräische Konsonanten
HEBREW_22 = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י',
              'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']
HEBR_VALUES = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60,
    'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}

# BURUMUT (lateinisch) zu hebräisch (1:1 A-T, 17 von 22 vorhanden)
LATIN_TO_HEBR = {
    'A': 'א', 'B': 'ב', 'C': None, 'D': None, 'E': 'ה',
    'F': 'ו', 'G': 'ז', 'H': 'ח', 'I': 'ט', 'J': 'י',  # Yod/Jod (state) - J in hebr. is Jod (י)
    'K': 'כ', 'L': 'ל', 'M': 'מ', 'N': 'נ', 'O': 'ס',
    'P': 'ע', 'Q': 'פ', 'R': 'צ', 'S': 'ק', 'T': 'ר',
    'U': 'ש', 'V': 'ת',  # Vav (write) - W = Vav fehlt aber U->Shin
    'W': 'ו',  # W (latein) -> Vav (hebr.)
    'X': None, 'Y': None, 'Z': None,
}

# BURUMUTREFAMTU als hebr. Symbole
burumut_hebr = ''.join(LATIN_TO_HEBR.get(c) or '?' for c in BURUMUT)
print(f"BURUMUT (99 Zeichen) -> hebr. (mit '?' für fehlende):")
print(f"  Latein: {BURUMUT[:60]}...")
print(f"  Hebr.:  {burumut_hebr[:60]}...")
print()

# 5 Turing-Operatoren als Klassen
class TuringOperator:
    def __init__(self, name, hebrew, gematria, meaning):
        self.name = name
        self.hebrew = hebrew
        self.gematria = gematria
        self.meaning = meaning

class ReadOperator(TuringOperator):
    def __init__(self):
        super().__init__('READ', 'כ', 20, 'Handfläche/Öffnung')
    def execute(self, machine):
        if machine.head >= len(machine.tape):
            return ' '
        return machine.tape[machine.head]

class WriteOperator(TuringOperator):
    def __init__(self):
        super().__init__('WRITE', 'ו', 6, 'Haken/Verbindung')
    def execute(self, machine, symbol=None):
        while machine.head >= len(machine.tape):
            machine.tape.append(' ')
        if symbol is not None:
            machine.tape[machine.head] = symbol
        return machine.tape[machine.head]

class MoveLeftOperator(TuringOperator):
    def __init__(self):
        super().__init__('MOVE_LEFT', 'ד', 4, 'Tür/Öffnung')
    def execute(self, machine):
        machine.head = max(0, machine.head - 1)
        return 'LEFT'

class MoveRightOperator(TuringOperator):
    def __init__(self):
        super().__init__('MOVE_RIGHT', 'ג', 3, 'Kamel/Bewegung')
    def execute(self, machine):
        machine.head += 1
        return 'RIGHT'

class HaltOperator(TuringOperator):
    def __init__(self):
        super().__init__('HALT', 'ת', 400, 'Kreuz/Ende/Halt')
    def execute(self, machine):
        machine.halted = True
        return 'HALT'

class StateOperator(TuringOperator):
    def __init__(self):
        super().__init__('STATE', 'י', 10, 'Arm/State-Transition')
    def execute(self, machine):
        machine.state += 1
        return f'q{machine.state}'

# Die Tora-Turing-Maschine
class ToraTuringMachine:
    def __init__(self, burumut):
        # Konvertiere BURUMUT zu hebr. Symbolen (mit '?' für fehlende)
        self.tape = list(LATIN_TO_HEBR.get(c) or '?' for c in burumut)
        self.head = 0
        self.state = 0  # q_0
        self.halted = False
        self.ops = 0
        self.symbol = None
        
        # 5-Operator-Implementation
        self.ops_dict = {
            'READ': ReadOperator(),
            'WRITE': WriteOperator(),
            'MOVE_LEFT': MoveLeftOperator(),
            'MOVE_RIGHT': MoveRightOperator(),
            'HALT': HaltOperator(),
            'STATE': StateOperator(),
        }
        
        # Übergangs-Tabelle: 5-Layer-Torah-Fold (hebr.)
        # Zustand | Symbol | → | n. Symbol | move
        self.transitions = {
            # BURUMUTREFAMTU durchläuft 5 Schichten
            (0, 'ב'): (1, 'ב', 'MOVE_RIGHT'),
            (0, 'ו'): (1, 'ו', 'MOVE_RIGHT'),
            (0, 'ר'): (1, 'ר', 'MOVE_RIGHT'),
            (0, 'א'): (1, 'א', 'MOVE_RIGHT'),
            (0, 'מ'): (1, 'מ', 'MOVE_RIGHT'),
            (0, 'ט'): (1, 'ט', 'MOVE_RIGHT'),
            (1, 'ה'): (2, 'ה', 'MOVE_RIGHT'),
            (1, 'נ'): (2, 'נ', 'MOVE_RIGHT'),
            (1, 'ש'): (2, 'ש', 'MOVE_RIGHT'),
            (1, 'ר'): (2, 'ר', 'MOVE_RIGHT'),
            (1, 'א'): (2, 'א', 'MOVE_RIGHT'),
            (2, 'י'): (3, 'י', 'MOVE_RIGHT'),
            (2, 'ל'): (3, 'ל', 'MOVE_RIGHT'),
            (2, 'מ'): (3, 'מ', 'MOVE_RIGHT'),
            (2, 'א'): (3, 'א', 'MOVE_RIGHT'),
            (2, 'נ'): (3, 'נ', 'MOVE_RIGHT'),
            (2, 'ע'): (3, 'ע', 'MOVE_RIGHT'),
            (3, 'פ'): (4, 'פ', 'MOVE_RIGHT'),
            (3, 'צ'): (4, 'צ', 'MOVE_RIGHT'),
            (3, 'ק'): (4, 'ק', 'MOVE_RIGHT'),
            (3, 'י'): (4, 'י', 'MOVE_RIGHT'),
            (3, 'ע'): (4, 'ע', 'MOVE_RIGHT'),
            (3, 'ר'): (4, 'ר', 'MOVE_RIGHT'),
            (4, 'ס'): (5, 'ס', 'MOVE_RIGHT'),
            (4, 'ע'): (5, 'ע', 'MOVE_RIGHT'),
            (4, 'י'): (5, 'י', 'MOVE_RIGHT'),
            (4, 'נ'): (5, 'נ', 'MOVE_RIGHT'),
            (4, 'ע'): (5, 'ע', 'MOVE_RIGHT'),
            (4, 'ר'): (5, 'ר', 'MOVE_RIGHT'),
            (5, 'א'): (6, 'א', 'HALT'),
            (5, 'כ'): (6, 'כ', 'HALT'),
            (5, 'ל'): (6, 'ל', 'HALT'),
            (5, 'ס'): (6, 'ס', 'HALT'),
            (5, 'ע'): (6, 'ע', 'HALT'),
        }
    
    def run(self, max_steps=500):
        print(f"="*70)
        print(f"TORA-TURING-MASCHINE v2 (hebr. Symbole)")
        print(f"="*70)
        print(f"Initial Band (hebr.): {''.join(self.tape)}")
        print(f"Initial Zustand: q_{self.state}")
        print(f"Initial Lesekopf: {self.head}")
        print()
        
        while not self.halted and self.ops < max_steps:
            # 1. READ
            self.symbol = self.ops_dict['READ'].execute(self)
            # 2. Übergangs-Tabelle
            key = (self.state, self.symbol)
            if key in self.transitions:
                new_state, write_symbol, move = self.transitions[key]
                # 3. WRITE (wenn anders)
                if write_symbol != self.symbol:
                    self.ops_dict['WRITE'].execute(self, write_symbol)
                # 4. STATE
                self.state = new_state
                # 5. MOVE
                if move == 'MOVE_LEFT':
                    self.ops_dict['MOVE_LEFT'].execute(self)
                elif move == 'MOVE_RIGHT':
                    self.ops_dict['MOVE_RIGHT'].execute(self)
                elif move == 'HALT':
                    self.ops_dict['HALT'].execute(self)
            else:
                # Halt wenn keine Übergang
                self.ops_dict['HALT'].execute(self)
                if self.ops < 5:
                    print(f"  HALT bei q_{self.state} Symbol='{self.symbol}' (keine Übergang)")
            
            self.ops += 1
            if self.ops <= 30 or self.halted:
                if self.ops <= 10 or self.halted:
                    print(f"  Step {self.ops:3d}: q_{self.state:1d} '{self.symbol}' Pos={self.head:2d}")
            if self.halted:
                break
        
        print()
        print(f"="*70)
        print(f"END")
        print(f"="*70)
        print(f"Final Tape: {''.join(self.tape)}")
        print(f"Final State: q_{self.state}")
        print(f"Final Head: {self.head}")
        print(f"Operations: {self.ops}")
        print(f"Halted: {self.halted}")
        
        return {
            'final_tape': ''.join(self.tape),
            'final_state': self.state,
            'final_head': self.head,
            'ops': self.ops,
            'halted': self.halted,
        }

# BURUMUT (99 Zeichen) als BURUMUTREFAMTU (14 Zeichen) starten
print("="*70)
print("TORA-TURING-MASCHINE v2 - 5 Layer-Übergänge")
print("="*70)
print(f"BURUMUTREFAMTU: {BURUMUT[:14]}")
print(f"BURUMUTREFAMTU (hebr.): {burumut_hebr[:14]}")
print()

# Erste 14 Zeichen = BURUMUTREFAMTU
# 5 Layer-Torah-Fold durchläuft BURUMUTREFAMTU
machine = ToraTuringMachine(BURUMUT[:14])
result = machine.run(max_steps=200)

# Speichere
with open('tora_turing_v2_run.json', "w") as f:
    json.dump({
        'input_burumutrefamtu': BURUMUT[:14],
        'input_hebr': burumut_hebr[:14],
        'result': result,
        'transitions_used': len(machine.transitions),
        '5_operatoren': {
            'READ': 'כ (Kaph, 20)',
            'WRITE': 'ו (Vav, 6)',
            'MOVE_LEFT': 'ד (Dalet, 4)',
            'MOVE_RIGHT': 'ג (Gimel, 3)',
            'HALT': 'ת (Tav, 400)',
            'STATE': 'י (Yod, 10)',
        },
    }, f, indent=2, ensure_ascii=False)
print()
print(f"Ergebnis gespeichert in sources/tora_turing_v2_run.json")
