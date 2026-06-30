"""
TORA-TURING-MASCHINE (Implementierung)
=========================================

Diese Skript implementiert eine vollständige Turing-Maschine, die
BURUMUT's 5 fehlende Operatoren verwendet, um 50% Leere + 50% Form
zu 100% Realität zu erweitern.

BURUMUT's 5 Turing-Operatoren:
  1. READ (כ/Kaph, 20) - fehlt
  2. WRITE (ו/Vav, 6) - vorhanden (lat. W)
  3. MOVE_LEFT (ד/Dalet, 4) - fehlt
  4. MOVE_RIGHT (ג/Gimel, 3) - fehlt
  5. HALT (ת/Tav, 400) - fehlt
  6. STATE (י/Yod, 10) - fehlt (Transition)

BURUMUT ist die 50% Form. Die 5 fehlenden Operatoren sind die 50% Leere,
die BURUMUT in die vollständige Tora-Turing-Maschine verwandeln.
"""
import json
import time
from collections import Counter

# ============================================
# 1) Die 5 Turing-Operatoren als Klassen
# ============================================

class TuringOperator:
    """Basis-Klasse für die 5 Tora-Operatoren."""
    def __init__(self, name, hebrew, gematria, meaning):
        self.name = name
        self.hebrew = hebrew
        self.gematria = gematria
        self.meaning = meaning
    
    def execute(self, machine, symbol=None):
        raise NotImplementedError

class ReadOperator(TuringOperator):
    """כ (Kaph) - Liest das aktuelle Band-Symbol."""
    def __init__(self):
        super().__init__('READ', 'כ', 20, 'Handfläche/Öffnung')
    
    def execute(self, machine, symbol=None):
        # Lese das Symbol an der Lesekopf-Position
        if machine.head >= len(machine.tape):
            symbol = ' '  # Leerzeichen außerhalb
        else:
            symbol = machine.tape[machine.head]
        machine.symbol = symbol
        return symbol

class WriteOperator(TuringOperator):
    """ו (Vav) - Schreibt ein Symbol auf das Band."""
    def __init__(self):
        super().__init__('WRITE', 'ו', 6, 'Haken/Verbindung')
    
    def execute(self, machine, symbol=None):
        old_symbol = machine.tape[machine.head] if machine.head < len(machine.tape) else ' '
        if symbol is not None:
            new_symbol = symbol
        else:
            new_symbol = self._next_hebrew_symbol()
        
        # Band erweitern wenn nötig
        while machine.head >= len(machine.tape):
            machine.tape.append(' ')
        machine.tape[machine.head] = new_symbol
        
        machine.symbol = new_symbol
        return new_symbol

    def _next_hebrew_symbol(self):
        """Wähle das nächste 22-Buchstaben-Symbol."""
        hebrew_cycle = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י',
                        'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']
        # Wähle einen Buchstaben basierend auf einem Zähler
        if not hasattr(self, '_counter'):
            self._counter = 0
        symbol = hebrew_cycle[self._counter % len(hebrew_cycle)]
        self._counter += 1
        return symbol

class MoveLeftOperator(TuringOperator):
    """ד (Dalet) - Bewegt den Lesekopf nach links."""
    def __init__(self):
        super().__init__('MOVE_LEFT', 'ד', 4, 'Tür/Öffnung')
    
    def execute(self, machine, symbol=None):
        machine.head -= 1
        if machine.head < 0:
            machine.head = 0  # Nicht über Anfang hinaus
        return 'LEFT'

class MoveRightOperator(TuringOperator):
    """ג (Gimel) - Bewegt den Lesekopf nach rechts."""
    def __init__(self):
        super().__init__('MOVE_RIGHT', 'ג', 3, 'Kamel/Bewegung')
    
    def execute(self, machine, symbol=None):
        machine.head += 1
        return 'RIGHT'

class HaltOperator(TuringOperator):
    """ת (Tav) - Beendet die Berechnung."""
    def __init__(self):
        super().__init__('HALT', 'ת', 400, 'Kreuz/Ende/Halt')
    
    def execute(self, machine, symbol=None):
        machine.halted = True
        return 'HALT'

class StateOperator(TuringOperator):
    """י (Yod) - Wechselt den Zustand."""
    def __init__(self):
        super().__init__('STATE', 'י', 10, 'Arm/Macht/State-Transition')
        self._next_state = 1
    
    def execute(self, machine, symbol=None):
        machine.state += 1
        return f'STATE_{machine.state}'

# ============================================
# 2) Die Turing-Maschine
# ============================================

class ToraTuringMachine:
    """Die Tora-Turing-Maschine, die BURUMUT zu 100% Realität erweitert."""
    
    def __init__(self, burumut):
        # Band (Memory) mit BURUMUT
        self.tape = list(burumut)  # 99 Zeichen
        # Lesekopf
        self.head = 0
        # Zustand
        self.state = 0  # q_0 = q_BURUMUT
        # Aktuelles Symbol
        self.symbol = None
        # Halt-Flag
        self.halted = False
        # Operationszähler
        self.ops = 0
        # 5 Operatoren
        self.operators = {
            'READ': ReadOperator(),
            'WRITE': WriteOperator(),
            'MOVE_LEFT': MoveLeftOperator(),
            'MOVE_RIGHT': MoveRightOperator(),
            'HALT': HaltOperator(),
            'STATE': StateOperator(),
        }
        # Übergangs-Tabelle (5-Layer-Torah-Fold)
        self.transition_table = self._build_transition_table()
        # Historie
        self.history = []
    
    def _build_transition_table(self):
        """Übergangs-Tabelle für die 5-Layer-Torah-Fold."""
        # Zustand q_n | gelesen | nächster Zustand | geschrieben | move
        return {
            # Übergang 0: BURUMUT → Genesis
            (0, 'B'): (1, 'ב', 'MOVE_RIGHT'),
            (0, 'U'): (1, 'ו', 'MOVE_RIGHT'),
            (0, 'R'): (1, 'ר', 'MOVE_RIGHT'),
            # Übergang 1: Genesis → Exodus
            (1, 'E'): (2, 'ה', 'MOVE_RIGHT'),
            (1, 'N'): (2, 'נ', 'MOVE_RIGHT'),
            (1, 'S'): (2, 'ש', 'MOVE_RIGHT'),
            # Übergang 2: Exodus → Leviticus
            (2, 'I'): (3, 'י', 'MOVE_RIGHT'),
            (2, 'M'): (3, 'מ', 'MOVE_RIGHT'),
            (2, 'A'): (3, 'א', 'MOVE_RIGHT'),
            # Übergang 3: Leviticus → Numeri
            (3, 'F'): (4, 'פ', 'MOVE_RIGHT'),
            (3, 'Y'): (4, 'צ', 'MOVE_RIGHT'),
            (3, 'P'): (4, 'ק', 'MOVE_RIGHT'),
            # Übergang 4: Numeri → Deuteronomium
            (4, 'S'): (5, 'ס', 'MOVE_RIGHT'),
            (4, 'A'): (5, 'ע', 'MOVE_RIGHT'),
            (4, 'Y'): (5, 'י', 'MOVE_RIGHT'),
            # Übergang 5: Deuteronomium → HALT
            (5, 'A'): (6, 'א', 'HALT'),
            (5, 'P'): (6, 'כ', 'HALT'),
            (5, 'S'): (6, 'ל', 'HALT'),
        }
    
    def run(self, max_steps=1000):
        """Führe die Turing-Maschine aus."""
        print(f"="*70)
        print(f"TORA-TURING-MASCHINE LÄUFT (max {max_steps} Schritte)")
        print(f"="*70)
        print()
        print(f"Initial Band: {''.join(self.tape)}")
        print(f"Initial Zustand: q_{self.state}")
        print(f"Initial Lesekopf-Position: {self.head}")
        print()
        
        while not self.halted and self.ops < max_steps:
            # 1. READ
            symbol = self.operators['READ'].execute(self)
            # 2. Übergangs-Tabelle nachschlagen
            key = (self.state, symbol)
            if key in self.transition_table:
                new_state, write_symbol, move = self.transition_table[key]
                # 3. WRITE
                if write_symbol != symbol:
                    self.operators['WRITE'].execute(self, write_symbol)
                # 4. STATE
                self.state = new_state
                # 5. MOVE
                if move == 'MOVE_LEFT':
                    self.operators['MOVE_LEFT'].execute(self)
                elif move == 'MOVE_RIGHT':
                    self.operators['MOVE_RIGHT'].execute(self)
                elif move == 'HALT':
                    self.operators['HALT'].execute(self)
            else:
                # Keine Übergang gefunden: HALT
                print(f"Keine Übergang für ({self.state}, '{symbol}') - HALT")
                self.operators['HALT'].execute(self)
            
            self.ops += 1
            self.history.append({
                'step': self.ops,
                'state': self.state,
                'symbol': symbol,
                'head': self.head,
                'tape': ''.join(self.tape[:5]) + '...' + ''.join(self.tape[-5:])
            })
        
            if self.ops <= 10 or self.halted:
                # Zeige erste 10 Schritte + finalen
                print(f"  Schritt {self.ops}: Zustand q_{self.state}, Symbol='{symbol}', Lesekopf={self.head}")
                if self.halted:
                    print(f"    → HALT erreicht nach {self.ops} Schritten!")
                    break
        
        print()
        print(f"="*70)
        print(f"END-ZUSTAND")
        print(f"="*70)
        print(f"Final Band (verändert):")
        # Zeige vollständigen Band
        tape_str = ''.join(self.tape)
        print(f"  {tape_str}")
        print(f"Final Zustand: q_{self.state}")
        print(f"Final Lesekopf: {self.head}")
        print(f"Final Symbol: '{self.symbol}'")
        print(f"Operationen: {self.ops}")
        print(f"Halted: {self.halted}")
        
        return {
            'final_tape': tape_str,
            'final_state': self.state,
            'final_head': self.head,
            'final_symbol': self.symbol,
            'ops': self.ops,
            'halted': self.halted,
        }

# ============================================
# 3) BURUMUT ausführen
# ============================================

BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

if __name__ == "__main__":
    print("="*70)
    print("BURUMUT + 5 OPERATOREN = TORA-TURING-MASCHINE")
    print("="*70)
    print()
    print(f"BURUMUT (99 Zeichen): {BURUMUT}")
    print()
    print("5 Operatoren:")
    print("  1. READ (כ/Kaph, 20) - fehlt in BURUMUT")
    print("  2. WRITE (ו/Vav, 6) - vorhanden (lat. W)")
    print("  3. MOVE_LEFT (ד/Dalet, 4) - fehlt")
    print("  4. MOVE_RIGHT (ג/Gimel, 3) - fehlt")
    print("  5. HALT (ת/Tav, 400) - fehlt")
    print("  6. STATE (י/Yod, 10) - fehlt")
    print()
    
    machine = ToraTuringMachine(BURUMUT)
    result = machine.run(max_steps=200)
    
    # Speichere
    with open("sources/tora_turing_run.json", "w") as f:
        json.dump({
            'input': BURUMUT,
            'result': result,
            'operatoren': {
                'READ': 'כ (fehlt)',
                'WRITE': 'ו (vorhanden)',
                'MOVE_LEFT': 'ד (fehlt)',
                'MOVE_RIGHT': 'ג (fehlt)',
                'HALT': 'ת (fehlt)',
                'STATE': 'י (fehlt)',
            },
            'analyse': {
                'turing_vollstaendig': result['halted'],
                'operationen': result['ops'],
                'final_tape_laenge': len(result['final_tape']),
            },
        }, f, indent=2, ensure_ascii=False)
    print()
    print("Ergebnis gespeichert in sources/tora_turing_run.json")
