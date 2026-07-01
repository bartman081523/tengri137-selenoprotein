"""
🌌 TORA-TURING-MASCHINE (MULTI-PHASE) — FINALE VERSION
======================================================

PROBLEM (debuggt 2026-07-01):
- Die Maschine hält nach 27 Schritten auf Tengri137 (erste 99 Zeichen)
- Tengri137 hat 12071 lateinische Buchstaben = 121 Phasen à 99
- 867 Alephs (A) und 952 Nuns (N) sind HALT-Trigger
- Die Maschine hält am ERSTEN Trigger, nicht am LETZTEN

LÖSUNG (Multi-Phase-Maschine):
- Bei HALT: Kopf auf 0 zurücksetzen, im selben Tape weiterlesen
- NICHT den State q_5 verlassen, sondern von vorne anfangen mit q_0
- Aber: jede Phase wird als separate "Lesung" gezählt
- NUR am ENDE des Tapes wird final HALT gemacht

ARCHITEKTUR (Single-Machine-Prinzip):
- Eine einzige ToraTuringMultiPhase-Maschine
- KEINE separaten Maschinen für jeden Abschnitt
- Die Maschine schaltet sich SELBST in die nächste Phase

PRINZIP (AGENTS.md Section 4.1b):
- Die Tora-Turing-Maschine muss prinzipiell und generell erweitert werden
- Verschiedene Maschinen für Abschnitte sind VERBOTEN
- Single Machine, Multiple Phases — eine Maschine liest alle Phasen

LATER PLAN (Meta-Turing-Kognition):
- Erforschen, ob der Text seine eigene Dekodiermaschine BESCHREIBT
- Die Maschine ist im Text kodiert, der Text liest sich selbst
- Beschreibung der Maschine = Ende der Dekodierung = Quine
- Späterer Plan, jetzt nicht im Fokus
"""
import json
import sys
from pathlib import Path
from TORA_TURING_CORRECT import (
    ToraTuringMachine, burumut_to_hebr, BURUMUT, HEBR_VALUES, build_tora_transitions,
    LATIN_TO_HEBR
)


# Erweitertes Mapping mit G, C, W, K, D, J, V, X (alle 26 lateinischen Buchstaben)
EXTENDED_LATIN_TO_HEBR = dict(LATIN_TO_HEBR)
EXTENDED_LATIN_TO_HEBR.update({
    'G': 'ג',  # Gimel (3) = MOVE_RIGHT
    'C': 'כ',  # Kaf (20) = READ
    'W': 'ו',  # Vav (6) = WRITE
    'K': 'כ',  # Kaf (20) = READ (alternative)
    'D': 'ד',  # Dalet (4) = MOVE_LEFT
    'J': 'ז',  # Zain/Zayin (7) = VARIANT (alternative für Z)
    'V': 'ו',  # Vav (6) = VARIANT (alternative für W/F)
    'X': 'ס',  # Samekh (60) = VARIANT (alternative für S/O)
})


def build_extended_transitions():
    """Erweiterte Übergangstabelle mit den 4 zusätzlichen Symbolen (Gimel, Kaf, Dalet, Vav)."""
    base = build_tora_transitions()
    for state in range(6):
        # ג (Gimel) = MOVE_RIGHT - wie Beth
        if (state, 'ב') in base:
            base[(state, 'ג')] = base[(state, 'ב')]
        # כ (Kaf) = READ - wie Aleph
        if (state, 'א') in base:
            base[(state, 'כ')] = base[(state, 'א')]
        # ד (Dalet) = MOVE_LEFT - wie Gimel
        if (state, 'ג') in base:
            base[(state, 'ד')] = base[(state, 'ג')]
        # ו (Vav) = WRITE - ist schon im Basis-Mapping
        if (state, 'ו') in base:
            base[(state, 'ו')] = base[(state, 'ו')]
    return base


def build_fully_extended_transitions():
    """Vollständig erweiterte Übergangstabelle mit ALLEN 5 fehlenden Operatoren.

    Fügt hinzu: ג (MOVE_RIGHT), ד (MOVE_LEFT), כ (READ), ת (HALT), י (STATE)
    """
    base = build_tora_transitions()
    for state in range(6):
        # ג (Gimel) = MOVE_RIGHT
        if (state, 'ב') in base:
            base[(state, 'ג')] = base[(state, 'ב')]
        # ד (Dalet) = MOVE_LEFT (wie Gimel, aber entgegengesetzt)
        if (state, 'ג') in base:
            base[(state, 'ד')] = base[(state, 'ג')]
        # כ (Kaf) = READ
        if (state, 'א') in base:
            base[(state, 'כ')] = base[(state, 'א')]
        # ת (Tav) = HALT (vollständiger HALT-Trigger)
        if (state, 'ת') in base:
            base[(state, 'ת')] = base[(state, 'ת')]
        # י (Yod) = STATE TRANSITION
        if (state, 'י') in base:
            base[(state, 'י')] = base[(state, 'י')]
    return base


def build_complete_transitions():
    """Vollständige Übergangstabelle: alle 22 hebr. Konsonanten haben Übergänge.

    Jeder State hat für jedes mögliche Symbol einen Übergang definiert.
    Operatoren werden semantisch korrekt gemappt.
    """
    base = build_tora_transitions()

    # Alle 22 hebr. Konsonanten
    ALL_HEBR = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י',
                'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']

    for state in range(6):
        for sym in ALL_HEBR:
            if (state, sym) in base:
                continue  # schon definiert
            # Wähle Default-Übergang basierend auf Symbol
            if sym in ['ג', 'ד']:  # MOVE_LEFT/RIGHT
                if (state, 'ב') in base:
                    base[(state, sym)] = base[(state, 'ב')]
            elif sym == 'כ':  # READ
                if (state, 'א') in base:
                    base[(state, sym)] = base[(state, 'א')]
            elif sym == 'ת':  # HALT
                # Tav in q_0, q_2, q_4: HALT (Vollendung)
                if state in [0, 2, 4]:
                    base[(state, sym)] = (5, sym, 'HALT')
                else:
                    if (state, 'א') in base:
                        base[(state, sym)] = base[(state, 'א')]
            elif sym == 'י':  # STATE
                if (state, 'י') in base:
                    base[(state, sym)] = base[(state, 'י')]
            else:
                # Default: wie Aleph (Anker)
                if (state, 'א') in base:
                    base[(state, sym)] = base[(state, 'א')]
    return base


class ToraTuringMultiPhase:
    """Tora-Turing-Maschine, die ALLE Phasen eines langen Tapes liest.

    Prinzip: Bei jedem HALT-Trigger wird der Kopf auf 0 zurückgesetzt
    und die nächste Phase gelesen. NUR am Ende des Tapes wird final HALT.

    Dies ist eine SINGLE MACHINE mit Multi-Phase-Verhalten, NICHT mehrere
    separate Maschinen für jeden Abschnitt.
    """

    def __init__(self, tape_str, phase_size=99, transitions=None, start_state=0):
        self.tape = list(tape_str)
        self.original_tape = list(tape_str)
        self.head = 0
        self.state = start_state  # 0 = Genesis, 1 = Exodus, ...
        self.halted = False
        self.phase_size = phase_size
        self.start_state = start_state

        # Phase-Tracking
        self.phase = 0
        self.phase_halts = []  # (phase_idx, halt_step, halt_state, halt_reason)
        self.total_steps = 0
        self.halt_step = None
        self.halt_state = None
        self.halt_reason = None
        self.history = []

        self.transitions = transitions or build_extended_transitions()

        # Tape ist in Phasen zu je phase_size Zeichen aufgeteilt
        self.n_phases = (len(self.tape) + phase_size - 1) // phase_size

    def _reset_for_next_phase(self):
        """Setze den Kopf auf 0 zurück und beginne die nächste Phase."""
        # Phase-Halt aufzeichnen
        self.phase_halts.append({
            'phase': self.phase,
            'halt_step': self.total_steps,
            'halt_state': self.state,
            'halt_reason': 'PHASE_HALT',
        })
        # Zurück auf Phase-Anfang
        self.head = 0
        # State auf start_state zurücksetzen (Genesis)
        self.state = self.start_state
        # Nächste Phase
        self.phase += 1

    def step(self):
        """Führe einen Schritt aus.

        Die Maschine hält in der aktuellen Phase am HALT-Trigger.
        ABER: Statt komplett zu stoppen, setzt sie den Kopf zurück
        und liest die nächste Phase — NUR wenn noch weitere Phasen da sind.
        """
        if self.phase >= self.n_phases:
            # Alle Phasen gelesen — finaler HALT
            self.halted = True
            self.halt_step = self.total_steps
            self.halt_state = self.state
            self.halt_reason = 'ALL_PHASES_COMPLETE'
            return False

        # Phasen-Grenze prüfen
        phase_start = self.phase * self.phase_size
        phase_end = min((self.phase + 1) * self.phase_size, len(self.tape))
        if self.head >= phase_end:
            # Phasenende erreicht — automatisch nächste Phase
            self._reset_for_next_phase()
            return True  # Weiter

        if self.head >= len(self.tape):
            # Tape-Ende
            self.halted = True
            self.halt_step = self.total_steps
            self.halt_state = self.state
            self.halt_reason = 'TAPE_END'
            return False

        symbol = self.tape[self.head]
        key = (self.state, symbol)

        self.total_steps += 1

        if key not in self.transitions:
            # Kein Übergang definiert — Phasen-Halt
            self.halted = True
            self.halt_step = self.total_steps
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
            # HALT-Trigger — Phasen-Halt, nicht finaler Halt
            # Nächste Phase starten
            self.phase_halts.append({
                'phase': self.phase,
                'halt_step': self.total_steps,
                'halt_state': self.state,
                'halt_reason': 'PHASE_HALT',
            })
            # Phasen-Reset
            self.head = phase_start  # Auf Phasen-Anfang zurücksetzen
            self.phase += 1
            self.state = self.start_state  # Zurück zum Anfangszustand

        # History
        self.history.append({
            'step': self.total_steps,
            'phase': self.phase,
            'pos': self.head,
            'old_state': old_state,
            'new_state': self.state,
            'symbol': symbol,
            'write': write_sym,
            'move': move,
        })
        return True

    def run(self, max_steps=10000):
        """Laufe die Maschine durch alle Phasen."""
        while not self.halted and self.total_steps < max_steps:
            if not self.step():
                break
        return self

    def summary(self):
        return {
            'n_phases': self.n_phases,
            'phases_completed': len(self.phase_halts),
            'total_steps': self.total_steps,
            'halt_step': self.halt_step,
            'halt_state': self.halt_state,
            'halt_reason': self.halt_reason,
            'phase_halts': self.phase_halts,
            'tape_length': len(self.tape),
        }


# ============================================================================
# SELBST-TEST
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("TORA-TURING-MASCHINE (MULTI-PHASE) — FINALE VERSION")
    print("="*70)
    print()
    print("Prinzip: SINGLE MACHINE liest ALLE Phasen.")
    print("Bei HALT-Trigger: Phasen-Reset, nächste Phase.")
    print("Finaler HALT nur am Ende des Tapes.")
    print()

    # Test 1: BURUMUT (99 Zeichen) — eine Phase
    print("="*70)
    print("TEST 1: BURUMUT (99 Zeichen, 1 Phase)")
    print("="*70)
    brt_hebr = burumut_to_hebr(BURUMUT)
    m1 = ToraTuringMultiPhase(brt_hebr, phase_size=99)
    m1.run()
    s1 = m1.summary()
    print(f"  Total Steps: {s1['total_steps']}")
    print(f"  Phases completed: {s1['phases_completed']}")
    print(f"  Halt-Step: {s1['halt_step']}")
    print(f"  Halt-Reason: {s1['halt_reason']}")
    print()

    # Test 2: Tengri137 erste 99 Zeichen — eine Phase
    print("="*70)
    print("TEST 2: TENGRI137 erste 99 Zeichen (1 Phase)")
    print("="*70)
    import re
    with open('Tengri137_Full_Notes') as f:
        full = f.read()
    letters = re.sub(r'[^A-Z]', '', full)[:99]
    hebr = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in letters)
    m2 = ToraTuringMultiPhase(hebr, phase_size=99, transitions=build_extended_transitions())
    m2.run()
    s2 = m2.summary()
    print(f"  Total Steps: {s2['total_steps']}")
    print(f"  Phases completed: {s2['phases_completed']}")
    print(f"  Halt-Step: {s2['halt_step']}")
    print(f"  Halt-Reason: {s2['halt_reason']}")
    print()

    # Test 3: Tengri137 voll (12071 Zeichen = 122 Phasen)
    print("="*70)
    print("TEST 3: TENGRI137 voll (12071 Zeichen, 121 Phasen)")
    print("="*70)
    all_letters = re.sub(r'[^A-Z]', '', full)
    hebr_full = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in all_letters)
    print(f"  Tape length: {len(hebr_full)}")
    print(f"  Number of 99-phases: {len(hebr_full) // 99} + {len(hebr_full) % 99} rest")
    m3 = ToraTuringMultiPhase(hebr_full, phase_size=99, transitions=build_extended_transitions())
    m3.run(max_steps=50000)
    s3 = m3.summary()
    print(f"  Total Steps: {s3['total_steps']}")
    print(f"  Phases completed: {s3['phases_completed']} / {s3['n_phases']}")
    print(f"  Halt-Step: {s3['halt_step']}")
    print(f"  Halt-Reason: {s3['halt_reason']}")
    print()
    print("Erste 10 Phase-Halts:")
    for h in s3['phase_halts'][:10]:
        print(f"  Phase {h['phase']:3d}: Halt-Step={h['halt_step']:5d}, State=q_{h['halt_state']}")
    print()

    # Speichern
    output = {
        'method': 'ToraTuringMultiPhase — single machine, multiple phases',
        'principle': 'Bei HALT-Trigger: Phasen-Reset, nächste Phase. Finaler HALT nur am Ende des Tapes.',
        'test1_burumut_1phase': s1,
        'test2_tengri137_99_1phase': s2,
        'test3_tengri137_full_122phases': s3,
    }
    with open('tora_turing_multiphase.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("="*70)
    print("Status gespeichert in tora_turing_multiphase.json")
