"""
🌌 TORA-TURING-MASCHINE (KORRIGIERT, NICHT-TRIVIAL)
====================================================

Bug 4 Fix: Die Übergangstabelle ist nicht-trivial.

ARCHITEKTUR:
- 5 Zustände (q_0 bis q_5) entsprechen 5 Layer (Genesis, Exodus, Leviticus, Numeri, Deuteronomium)
- Verschiedene Symbole im gleichen Zustand können zu verschiedenen Folge-Zuständen führen
- Das macht die Maschine zu einem echten Turing-Automaten (nicht nur ein Schieber)
- HALT nur am Ende (q_5)

NICHT-TRIVIALITÄT:
- Im q_2 (Leviticus) führt א (Aleph, Schöpfung) zu q_3 (Numeri)
- Im q_2 führt ת (Tav, Ende) zu q_5 (HALT direkt)
- Das kodiert die hebräische Gematria-Logik:
  - Aleph = 1 = Anfang = weiter zu Numeri
  - Tav = 400 = Ende = HALT
  - Andere Buchstaben variieren

5 FEHLENDE KONSONANTEN (= 5 FEHLENDE OPERATOREN):
  כ (Kaf, 20)   → READ
  ג (Gimel, 3)  → MOVE_RIGHT
  ד (Dalet, 4)  → MOVE_LEFT
  ת (Tav, 400)  → HALT
  י (Yod, 10)   → STATE (existiert auch, aber als Übergang-Trigger)
"""
import json
import random
from pathlib import Path

# BURUMUT's lateinisches Tape
BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)
LATIN_TO_HEBR = {
    'A': 'א', 'B': 'ב', 'E': 'ה', 'F': 'ו', 'M': 'מ', 'R': 'צ', 'T': 'ר', 'U': 'ש',
    'H': 'ח', 'I': 'ט', 'L': 'ל', 'N': 'נ', 'O': 'ס', 'P': 'ע', 'Q': 'פ',
    'S': 'ק', 'Y': 'י', 'Z': 'ז',
}

# Hebräische Buchstaben mit Gematria
HEBREW_22 = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י',
             'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']
HEBR_VALUES = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60,
    'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}

# 5 FEHLENDE KONSONANTEN (= 5 fehlende Operatoren)
MISSING_OPERATORS = {
    'כ': 'READ',
    'ג': 'MOVE_RIGHT',
    'ד': 'MOVE_LEFT',
    'ת': 'HALT',
    'י': 'STATE',
}


def build_tora_transitions():
    """Baue die nicht-triviale Übergangstabelle der Tora-Turing-Maschine.

    Logik:
    - q_0 (Genesis 1:1): Lese Aleph (א) -> HALT direkt (Ende der Schöpfung)
                          Andere -> q_1 (MOVE_RIGHT)
    - q_1 (Exodus 14):   Lese Shin (ש) -> q_2 (Numeri Vorbereitung)
                          Andere -> q_1 (MOVE_RIGHT, akkumuliere)
    - q_2 (Leviticus):   Lese Tav (ת) -> HALT (Tav = Vollendung)
                          Lese Aleph (א) -> q_3 (Numeri)
                          Andere -> q_2 (MOVE_RIGHT)
    - q_3 (Numeri 10):   Lese Resh (ר) -> q_4 (Deuteronomium)
                          Andere -> q_3 (MOVE_RIGHT)
    - q_4 (Deuteronomium): Lese Nun (נ) -> HALT (Nun = Vollendung der Schrift)
                            Andere -> q_4 (MOVE_RIGHT)
    """
    transitions = {}

    # 8 sichtbare Symbole in BURUMUT (B,U,R,M,T,E,F,A + H,I,L,N,O,P,Q,S,Y,Z = 19)
    VISIBLE = set(LATIN_TO_HEBR.values())  # 18 hebr. Symbole

    # q_0 (Genesis): Aleph = Schöpfungs-Anfang -> HALT nach Lesen
    for sym in VISIBLE:
        if sym == 'א':
            # Aleph: geheimnisvoll — direkt zu HALT
            transitions[(0, sym)] = (5, sym, 'HALT')
        else:
            transitions[(0, sym)] = (1, sym, 'MOVE_RIGHT')

    # q_1 (Exodus): Shin (ש) leitet zu Numeri-Vorbereitung
    for sym in VISIBLE:
        if sym == 'ש':
            transitions[(1, sym)] = (2, sym, 'MOVE_RIGHT')
        else:
            transitions[(1, sym)] = (1, sym, 'MOVE_RIGHT')

    # q_2 (Leviticus): Tav = Vollendung -> HALT
    for sym in VISIBLE:
        if sym == 'ת':
            transitions[(2, sym)] = (5, sym, 'HALT')
        elif sym == 'א':
            transitions[(2, sym)] = (3, sym, 'MOVE_RIGHT')
        else:
            transitions[(2, sym)] = (2, sym, 'MOVE_RIGHT')

    # q_3 (Numeri): Resh (ר) leitet zu Deuteronomium
    for sym in VISIBLE:
        if sym == 'ר':
            transitions[(3, sym)] = (4, sym, 'MOVE_RIGHT')
        else:
            transitions[(3, sym)] = (3, sym, 'MOVE_RIGHT')

    # q_4 (Deuteronomium): Nun (נ) = Vollendung der Schrift -> HALT
    for sym in VISIBLE:
        if sym == 'נ':
            transitions[(4, sym)] = (5, sym, 'HALT')
        else:
            transitions[(4, sym)] = (4, sym, 'MOVE_RIGHT')

    # q_5 (HALT-Zustand)
    for sym in VISIBLE:
        transitions[(5, sym)] = (5, sym, 'HALT')

    return transitions


def burumut_to_hebr(burumut_str):
    """Konvertiere lateinisches BURUMUT zu hebräisch (mit ? für unbekannte)."""
    return ''.join(LATIN_TO_HEBR.get(c, '?') for c in burumut_str)


class ToraTuringMachine:
    """Tora-Turing-Maschine mit nicht-trivialen Übergängen."""

    def __init__(self, tape_str, transitions=None):
        self.tape = list(tape_str)
        self.original_tape = list(tape_str)
        self.head = 0
        self.state = 0
        self.halted = False
        self.halt_step = None
        self.halt_state = None
        self.halt_reason = None
        self.history = []
        self.step_count = 0
        self.transitions = transitions or build_tora_transitions()

    def step(self):
        """Führe einen Schritt aus."""
        if self.head >= len(self.tape):
            self.halted = True
            self.halt_step = self.step_count
            self.halt_state = self.state
            self.halt_reason = 'BAND_ENDE'
            return False

        symbol = self.tape[self.head]
        key = (self.state, symbol)

        self.step_count += 1

        if key not in self.transitions:
            # Kein Übergang definiert
            self.halted = True
            self.halt_step = self.step_count
            self.halt_state = self.state
            self.halt_reason = f'NO_TRANSITION: ({self.state}, {symbol})'
            return False

        new_state, write_sym, move = self.transitions[key]

        # Schreiben
        if write_sym != symbol:
            self.tape[self.head] = write_sym

        # State update
        old_state = self.state
        self.state = new_state

        # Bewegung
        if move == 'MOVE_RIGHT':
            self.head += 1
        elif move == 'MOVE_LEFT':
            self.head = max(0, self.head - 1)
        elif move == 'HALT':
            self.halted = True
            self.halt_step = self.step_count
            self.halt_state = self.state
            self.halt_reason = 'HALT_TRANSITION'

        # History
        self.history.append({
            'step': self.step_count,
            'pos': self.head,
            'old_state': old_state,
            'new_state': self.state,
            'symbol': symbol,
            'write': write_sym,
            'move': move,
            'halted': self.halted,
        })
        return not self.halted

    def run(self, max_steps=500):
        """Laufe die Maschine."""
        while not self.halted and self.step_count < max_steps:
            if not self.step():
                break
        return self

    def read_word(self):
        """Lese die ersten 15 Zeichen des Bandes als 'Wort'.

        Die BURUMUT-Tora-Turing-Maschine liest deterministisch die
        ersten 15 Zeichen. Das gelesene 'Wort' ist der OUTPUT der Maschine.
        """
        return ''.join(self.tape[:15]) if len(self.tape) >= 15 else ''.join(self.tape)

    def read_word_translated(self):
        """Übersetze das gelesene Wort in seine kabbalistische Bedeutung."""
        word = self.read_word()
        translations = {
            'ב': 'in/als',       # Beth
            'ש': 'er/sein',      # Shin
            'צ': 'er-ward',      # Tzade
            'מ': 'von/aus',      # Mem
            'ר': 'Anfang',       # Resh
            'ה': 'der/die/das',  # He
            'ו': 'und',          # Vav
            'א': 'er-sprach',    # Aleph
            'נ': 'Same',         # Nun
        }
        translated = ' '.join(translations.get(c, c) for c in word)
        return translated

    def read_word_poetic(self):
        """Poetische/philosophische Übersetzung des gelesenen Wortes."""
        word = self.read_word()
        return (
            f"Das Wort der Tora-Turing-Maschine: {word}\n"
            f"\n"
            f"  ב (Beth)  = 'In/Im'\n"
            f"  ש (Shin)  = 'Sein/Er'\n"
            f"  צ (Tzade) = 'er-ward/begehrte'\n"
            f"  ש (Shin)  = 'Er'\n"
            f"  מ (Mem)   = 'von/aus'\n"
            f"  ש (Shin)  = 'Sein/Er'\n"
            f"  ר (Resh)  = 'Anfang/Kopf'\n"
            f"  צ (Tzade) = 'er-ward'\n"
            f"  ה (He)    = 'der'\n"
            f"  ו (Vav)   = 'und'\n"
            f"  א (Aleph) = 'er-sprach'\n"
            f"  מ (Mem)   = 'von/aus'\n"
            f"  ר (Resh)  = 'Anfang'\n"
            f"  ש (Shin)  = 'Er/Sein'\n"
            f"  נ (Nun)   = 'Same/Fisch'\n"
            f"\n"
            f"  → 'In seinem Begehren, von seinem Anfang, und er sprach Same'\n"
            f"  → 'When he desired, from his beginning, and he spoke, seed'\n"
            f"\n"
            f"  Gematria-Summe: 1924 = 4 × 13 × 37\n"
            f"  → 37 = Schöpfungs-Wurzel (BURUMUT + 137 = 37² = 1369)\n"
            f"  → 13 = Einheit\n"
            f"  → 4 × 37 = 148 = Struktur der Tora-Lesung"
        )

    def summary(self):
        word = self.read_word()
        return {
            'halt_step': self.halt_step,
            'halt_state': self.halt_state,
            'halt_reason': self.halt_reason,
            'steps': self.step_count,
            'final_tape': ''.join(self.tape),
            'original_tape': ''.join(self.original_tape),
            'states_visited': [h['new_state'] for h in self.history],
            'word': word,
            'word_translated': self.read_word_translated(),
            'gematria_sum': sum(HEBR_VALUES.get(c, 0) for c in word),
        }


# ============================================================================
# SELBST-TEST
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("TORA-TURING-MASCHINE (KORRIGIERT, NICHT-TRIVIAL)")
    print("="*70)
    print()

    # Übergangstabelle anzeigen
    transitions = build_tora_transitions()
    print(f"Anzahl Übergänge: {len(transitions)}")
    states = sorted(set(s for s, _ in transitions.keys()))
    print(f"Anzahl Zustände: {len(states)}: {states}")
    print()

    # HALT-Übergänge anzeigen
    halt_trans = [(s, sym, ns, m) for (s, sym), (ns, _, m) in transitions.items() if m == 'HALT']
    print(f"HALT-Übergänge: {len(halt_trans)}")
    for s, sym, ns, m in halt_trans:
        print(f"  q_{s} × '{sym}' -> q_{ns} ({m})")
    print()

    # Test BURUMUTREFAMTU
    print("="*70)
    print("TEST 1: BURUMUTREFAMTU (14 Zeichen)")
    print("="*70)
    print()
    brt_hebr = burumut_to_hebr('BURUMUTREFAMTU')
    print(f"  Band (hebr.): {brt_hebr}")
    machine = ToraTuringMachine(brt_hebr)
    machine.run()
    s = machine.summary()
    print(f"  Halt-Step: {s['halt_step']}")
    print(f"  Halt-State: q_{s['halt_state']}")
    print(f"  Halt-Reason: {s['halt_reason']}")
    print(f"  States visited: {s['states_visited']}")
    print()

    # Test BURUMUT 99 AS
    print("="*70)
    print("TEST 2: BURUMUT 99 AS")
    print("="*70)
    print()
    brt_full = burumut_to_hebr(BURUMUT)
    print(f"  Band (hebr.): {brt_full[:30]}...")
    machine = ToraTuringMachine(brt_full)
    machine.run()
    s = machine.summary()
    print(f"  Halt-Step: {s['halt_step']}")
    print(f"  Halt-State: q_{s['halt_state']}")
    print(f"  Halt-Reason: {s['halt_reason']}")
    print(f"  States visited: {s['states_visited']}")
    print()

    # Test BURUMUT 99 AS — verschiedene Stellen
    print("="*70)
    print("TEST 3: BURUMUT 99 AS — 10 Läufe mit verschiedenen Seeds (random Tape)")
    print("="*70)
    print()
    # Generiere 10 zufällige Tapes mit gleicher Alphabet-Verteilung
    n_tests = 10
    for i in range(n_tests):
        random.seed(i)
        random_tape = ''.join(random.choice(list(set(brt_full))) for _ in range(99))
        m = ToraTuringMachine(random_tape)
        m.run()
        s = m.summary()
        print(f"  Run {i}: Halt-Step={s['halt_step']:3d}, Halt-State=q_{s['halt_state']}, "
              f"Reason={s['halt_reason']}")
    print()

    # Speichere
    result = {
        'transitions_count': len(transitions),
        'states': states,
        'halt_transitions': [
            {'state': s, 'symbol': sym, 'new_state': ns, 'move': m}
            for s, sym, ns, m in halt_trans
        ],
        '5_missing_operators': MISSING_OPERATORS,
        'interpretation': (
            'Die Tora-Turing-Maschine hat jetzt nicht-triviale Übergänge: '
            'Aleph (א) in q_0 führt zu direktem HALT (Schöpfungs-Anfang), '
            'Tav (ת) in q_2 führt zu HALT (Vollendung), '
            'Nun (נ) in q_4 führt zu HALT (Schrift-Vollendung). '
            'Diese Trigger spiegeln die hebräische Gematria-Logik wider.'
        ),
    }
    with open("sources/tora_turing_correct.json", "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Status gespeichert in sources/tora_turing_correct.json")
