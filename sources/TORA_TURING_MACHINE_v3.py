"""
TORA-TURING-MASCHINE v3 - Vollständige 5-Layer-Übergänge
=================================================

BURUMUTREFAMTU → 5-Layer-Torah-Fold:
  Layer 0: BURUMUT (Genesis 1:1) - Schöpfungs-Impuls
  Layer 1: UAZBE (Exodus 14) - Shem HaMephorash
  Layer 2: HIMLAZANR (Numeri 10) - Mirror-Shem
  Layer 3: UAZBE (Leviticus) - Zentrales Orakel
  Layer 4: NOMBA (Deuteronomium) - Vollendung
  Layer 5: HALT - Tav (Ende)

BURUMUT's 5 fehlende hebr. Konsonanten = 5 Turing-Operatoren
"""
import json
from collections import Counter

BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# BURUMUTREFAMTU (Vorspann, 14 Zeichen)
BURUMUTREFAMTU = BURUMUT[:14]  # 'BURUMUTREFAMTU'

# 22 hebr. Konsonanten mit Gematria
HEBREW_22 = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י',
              'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']
HEBR_VALUES = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60,
    'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}

# Mapping BURUMUTREFAMTU zu hebr. Konsonanten
# A=1(א), B=2(ב), E=5(ה), F=6(ו), M=40(מ), R=200(ר), T=400(ת), U=300(ש)
# BURUMUTREFAMTU hebr. Mapping:
# B=ב, U=ש, R=צ, U=ש, M=מ, U=ש, T=ר, R=צ, E=ה, F=ו, A=א, M=מ, T=ר, U=ש
mapping = {
    'A': 'א', 'B': 'ב', 'E': 'ה', 'F': 'ו', 'M': 'מ', 'R': 'צ', 'T': 'ר', 'U': 'ש',
}

# BURUMUTREFAMTU hebr.
burumutrefamtu_hebr = ''.join(mapping.get(c, '?') for c in BURUMUTREFAMTU)
print(f"BURUMUTREFAMTU (hebr.): {burumutrefamtu_hebr}")

# 5 Layer-Übergänge (KORRIGIERT, vollständig)
# Jeder Schritt liest 1 Zeichen, schreibt 1 Zeichen, bewegt 1 Schritt
TRANSITIONS = {
    # BURUMUTREFAMTU durchläuft die 5 Layer
    # Layer 0 (Genesis): Lesen 'B' -> Schreiben 'ב' -> Wechsel zu q_1 -> MOVE_RIGHT
    (0, 'ב'): (1, 'ב', 'MOVE_RIGHT'),  # q_0, B(ב) -> q_1, B(ב), →
    (0, 'ש'): (1, 'ש', 'MOVE_RIGHT'),  # q_0, U(ש) -> q_1, U(ש), →
    (0, 'צ'): (1, 'צ', 'MOVE_RIGHT'),  # q_0, R(צ) -> q_1, R(צ), →
    (0, 'מ'): (1, 'מ', 'MOVE_RIGHT'),  # q_0, M(מ) -> q_1, M(מ), →
    (0, 'ר'): (1, 'ר', 'MOVE_RIGHT'),  # q_0, T(ר) -> q_1, T(ר), →
    (0, 'ה'): (1, 'ה', 'MOVE_RIGHT'),  # q_0, E(ה) -> q_1, E(ה), →
    (0, 'ו'): (1, 'ו', 'MOVE_RIGHT'),  # q_0, F(ו) -> q_1, F(ו), →
    (0, 'א'): (1, 'א', 'MOVE_RIGHT'),  # q_0, A(א) -> q_1, A(א), →

    # Layer 1 (Exodus): Lesen 'U' -> Schreiben 'ו' -> q_2 -> MOVE_RIGHT
    (1, 'ב'): (2, 'ב', 'MOVE_RIGHT'),
    (1, 'ש'): (2, 'ש', 'MOVE_RIGHT'),
    (1, 'צ'): (2, 'צ', 'MOVE_RIGHT'),
    (1, 'מ'): (2, 'מ', 'MOVE_RIGHT'),
    (1, 'ר'): (2, 'ר', 'MOVE_RIGHT'),
    (1, 'ה'): (2, 'ה', 'MOVE_RIGHT'),
    (1, 'ו'): (2, 'ו', 'MOVE_RIGHT'),
    (1, 'א'): (2, 'א', 'MOVE_RIGHT'),

    # Layer 2 (Numeri 10 / Leviticus): Lesen -> Wechsel zu q_3
    (2, 'ב'): (3, 'ב', 'MOVE_RIGHT'),
    (2, 'ש'): (3, 'ש', 'MOVE_RIGHT'),
    (2, 'צ'): (3, 'צ', 'MOVE_RIGHT'),
    (2, 'מ'): (3, 'מ', 'MOVE_RIGHT'),
    (2, 'ר'): (3, 'ר', 'MOVE_RIGHT'),
    (2, 'ה'): (3, 'ה', 'MOVE_RIGHT'),
    (2, 'ו'): (3, 'ו', 'MOVE_RIGHT'),
    (2, 'א'): (3, 'א', 'MOVE_RIGHT'),

    # Layer 3: q_4
    (3, 'ב'): (4, 'ב', 'MOVE_RIGHT'),
    (3, 'ש'): (4, 'ש', 'MOVE_RIGHT'),
    (3, 'צ'): (4, 'צ', 'MOVE_RIGHT'),
    (3, 'מ'): (4, 'מ', 'MOVE_RIGHT'),
    (3, 'ר'): (4, 'ר', 'MOVE_RIGHT'),
    (3, 'ה'): (4, 'ה', 'MOVE_RIGHT'),
    (3, 'ו'): (4, 'ו', 'MOVE_RIGHT'),
    (3, 'א'): (4, 'א', 'MOVE_RIGHT'),

    # Layer 4: q_5
    (4, 'ב'): (5, 'ב', 'MOVE_RIGHT'),
    (4, 'ש'): (5, 'ש', 'MOVE_RIGHT'),
    (4, 'צ'): (5, 'צ', 'MOVE_RIGHT'),
    (4, 'מ'): (5, 'מ', 'MOVE_RIGHT'),
    (4, 'ר'): (5, 'ר', 'MOVE_RIGHT'),
    (4, 'ה'): (5, 'ה', 'MOVE_RIGHT'),
    (4, 'ו'): (5, 'ו', 'MOVE_RIGHT'),
    (4, 'א'): (5, 'א', 'MOVE_RIGHT'),

    # Layer 5: HALT-Zustand bei q_5
    (5, 'ב'): (6, 'ב', 'HALT'),
    (5, 'ש'): (6, 'ש', 'HALT'),
    (5, 'צ'): (6, 'צ', 'HALT'),
    (5, 'מ'): (6, 'מ', 'HALT'),
    (5, 'ר'): (6, 'ר', 'HALT'),
    (5, 'ה'): (6, 'ה', 'HALT'),
    (5, 'ו'): (6, 'ו', 'HALT'),
    (5, 'א'): (6, 'א', 'HALT'),
}

# 5 Operatoren
class TuringMachine:
    def __init__(self, band, transitions):
        self.tape = list(band)
        self.head = 0
        self.state = 0
        self.halted = False
        self.ops = 0
        self.transitions = transitions
        self.symbol = None
        self.history = []

    def run(self, max_steps=200):
        print(f"="*70)
        print(f"TORA-TURING-MASCHINE v3")
        print(f"="*70)
        print(f"Initial Band: {''.join(self.tape)}")
        print(f"Initial Zustand: q_{self.state}")
        print(f"Initial Lesekopf: {self.head}")
        print()

        while not self.halted and self.ops < max_steps:
            # READ
            if self.head >= len(self.tape):
                symbol = ' '
            else:
                symbol = self.tape[self.head]
            self.symbol = symbol

            # Übergangstabelle
            key = (self.state, symbol)
            if key in self.transitions:
                new_state, write_symbol, move = self.transitions[key]
                if write_symbol != symbol and self.head < len(self.tape):
                    self.tape[self.head] = write_symbol
                self.state = new_state
                if move == 'MOVE_RIGHT':
                    self.head += 1
                elif move == 'MOVE_LEFT':
                    self.head = max(0, self.head - 1)
                elif move == 'HALT':
                    self.halted = True
            else:
                self.halted = True
                if self.ops < 5:
                    print(f"  HALT bei q_{self.state} Symbol='{symbol}' (keine Übergang)")

            self.ops += 1
            self.history.append({
                'step': self.ops,
                'state': self.state,
                'symbol': symbol,
                'head': self.head,
                'tape': ''.join(self.tape)
            })
            if self.ops <= 5 or self.halted:
                print(f"  Step {self.ops:3d}: q_{self.state:1d} '{symbol}' Pos={self.head:2d} Tape={''.join(self.tape[:8])}")
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
        return self.tape, self.state, self.head, self.ops, self.halted

# Test
print("="*70)
print("TORA-TURING-MASCHINE v3 - 5-Layer-Übergänge")
print("="*70)
print(f"BURUMUTREFAMTU (latein): {BURUMUTREFAMTU}")
print(f"BURUMUTREFAMTU (hebr.):  {burumutrefamtu_hebr}")
print()

machine = TuringMachine(burumutrefamtu_hebr, TRANSITIONS)
result = machine.run(max_steps=200)

# Speichere
with open("sources/tora_turing_v3_run.json", "w") as f:
    json.dump({
        'input': BURUMUTREFAMTU,
        'input_hebr': burumutrefamtu_hebr,
        'result': {
            'tape': ''.join(result[0]),
            'state': result[1],
            'head': result[2],
            'ops': result[3],
            'halted': result[4],
        },
        'transitions': len(TRANSITIONS),
        '5_operatoren': {
            'READ': 'כ (fehlt)',
            'WRITE': 'ו (vorhanden)',
            'MOVE_LEFT': 'ד (fehlt)',
            'MOVE_RIGHT': 'ג (fehlt)',
            'HALT': 'ת (fehlt)',
            'STATE': 'י (fehlt)',
        },
    }, f, indent=2, ensure_ascii=False)
print()
print(f"Ergebnis gespeichert in sources/tora_turing_v3_run.json")
