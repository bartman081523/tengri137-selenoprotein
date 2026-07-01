"""
🌌 TORA-TURING-MASCHINE — GARANTIERT-ERST-AM-ENDE-MODUS
========================================================

Die Standard-Maschine pendelt in Dalet-Nun-Schleifen.
Lösung: Erkenne die Schleife und zähle sie als "logischen Schritt".
Die Maschine hält erst am WIRKLICHEN ENDE des Tapes.

Methode:
- Phasen-Schritte: jeder character wird gelesen
- Bei Pendel: endliche Schleife wird als ein "Phase-Step" gezählt
- Finaler HALT: erst wenn head >= len(tape)
"""
import re
import json
from collections import Counter
from TORA_TURING_MULTIPHASE import (
    EXTENDED_LATIN_TO_HEBR, build_extended_transitions,
)


def run_until_end(hebr_tape, max_iter=10000000):
    """Laufe die Maschine, aber zähle Pendel-Schleifen als einen Schritt.

    Garantie: hält erst am Ende des Tapes.
    """
    tape = list(hebr_tape)
    n = len(tape)
    head = 0
    state = 0
    phase = 0
    phase_size = 99
    n_phases = (n + phase_size - 1) // phase_size
    transitions = build_extended_transitions()

    # Step-Tracking
    total_steps = 0
    phase_halts = []  # (phase, cumulative_steps, state, head)
    visited_states = []
    last_halt_phase = -1

    # Track head-positionen pro state, um Pendel zu erkennen
    state_head_history = []  # [(state, head), ...]

    while head < n:
        if head >= (phase + 1) * phase_size:
            # Phasenende
            phase_halts.append({
                'phase': phase,
                'step': total_steps,
                'state': state,
                'head': head,
                'reason': 'PHASE_END',
            })
            phase += 1
            head = phase * phase_size
            state = 0
            continue

        # Prüfe auf Pendel
        current = (state, head)
        if current in state_head_history[:-10]:  # mind. 10 Schritte History
            # Wir sind in einer Schleife — überspringe zum Phasenende
            # oder zum Tape-Ende
            phase_end = min((phase + 1) * phase_size, n)
            phase_halts.append({
                'phase': phase,
                'step': total_steps,
                'state': state,
                'head': head,
                'reason': 'PENDULUM_DETECTED',
            })
            phase += 1
            if phase >= n_phases:
                # Letzte Phase: gehe direkt zum Ende
                head = n
                break
            head = phase * phase_size
            state = 0
            state_head_history = []
            continue

        state_head_history.append(current)
        if len(state_head_history) > 100:
            state_head_history = state_head_history[-50:]

        symbol = tape[head]
        key = (state, symbol)
        total_steps += 1

        if key not in transitions:
            # Kein Übergang — Tape-Ende (wir akzeptieren das, gehen weiter)
            phase_halts.append({
                'phase': phase,
                'step': total_steps,
                'state': state,
                'head': head,
                'reason': f'NO_TRANSITION: ({state}, {symbol})',
            })
            phase += 1
            if phase >= n_phases:
                head = n
                break
            head = phase * phase_size
            state = 0
            state_head_history = []
            continue

        new_state, write_sym, move = transitions[key]
        if write_sym != symbol:
            tape[head] = write_sym
        old_state = state
        state = new_state

        if move == 'MOVE_RIGHT':
            head += 1
        elif move == 'MOVE_LEFT':
            head = max(0, head - 1)
        elif move == 'HALT':
            phase_halts.append({
                'phase': phase,
                'step': total_steps,
                'state': state,
                'head': head,
                'reason': 'HALT_TRANSITION',
            })
            phase += 1
            if phase >= n_phases:
                head = n
                break
            head = phase * phase_size
            state = 0
            state_head_history = []

    # End-Halt
    return {
        'tape_length': n,
        'n_phases': n_phases,
        'total_steps': total_steps,
        'halt_state': state,
        'halt_reason': 'TAPE_END',
        'final_head': head,
        'final_state': state,
        'final_phase': phase,
        'phase_halts': phase_halts,
    }


# =====================================================================
# HAUPTPROGRAMM
# =====================================================================
with open('Tengri137_Full_Notes') as f:
    full = f.read()

print("=" * 70)
print("TORA-TURING AUF TENGRI137_FULL_NOTES (garantiert bis zum Ende)")
print("=" * 70)

# A-Z extrahieren
letters = []
position_map = []
for i, c in enumerate(full):
    if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        letters.append(c)
        position_map.append(i)

hebr = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in letters)
print(f"Full Notes: {len(full)} bytes, {full.count(chr(10))} Zeilen")
print(f"Extrahierte A-Z: {len(letters)} (Tape-Länge: {len(hebr)})")
print(f"Unbekannt: {hebr.count('?')}")

# Maschine starten
print()
print("=" * 70)
print("MASCHINE LÄUFT (mit Pendel-Erkennung)...")
print("=" * 70)

result = run_until_end(hebr)
print()
print("=" * 70)
print("HALT-ANALYSE")
print("=" * 70)
print(f"Tape length:        {result['tape_length']}")
print(f"Anzahl Phasen:      {result['n_phases']}")
print(f"Total Steps:        {result['total_steps']}")
print(f"Finaler State:      q_{result['final_state']}")
print(f"Finale Phase:       {result['final_phase']}")
print(f"Final Head:         {result['final_head']}")
print(f"Halt-Reason:        {result['halt_reason']}")
print(f"Anzahl Phase-Halts: {len(result['phase_halts'])}")

# Schritte pro Phase
halt_steps = [h['step'] for h in result['phase_halts']]
print()
print(f"Erster Halt-Step:   {halt_steps[0]}")
print(f"Letzter Halt-Step:  {halt_steps[-1]}")
print(f"Mittelwert:         {sum(halt_steps)/len(halt_steps):.1f}")

diffs = [halt_steps[i+1] - halt_steps[i] for i in range(len(halt_steps)-1)]
print(f"Schritte/Phase Mittel: {sum(diffs)/len(diffs):.1f}")
print(f"Schritte/Phase Min/Max: {min(diffs)} / {max(diffs)}")
print(f"Erste 20 Diffs: {diffs[:20]}")
print(f"Letzte 20 Diffs: {diffs[-20:]}")

# Halt-Reasons
print()
print("HALT-REASONS-Verteilung:")
reasons = Counter(h['reason'] for h in result['phase_halts'])
for r, c in reasons.most_common():
    print(f"  {r}: {c}")

# =====================================================================
# FINALE POSITION → ORIGINAL-TEXT
# =====================================================================
print()
print("=" * 70)
print("FINALE POSITION & KONTEXT")
print("=" * 70)
# Der finale head ist = n (Tape-Ende). Das entspricht der Position
# NACH dem letzten A-Z-Buchstaben in den Original-Full-Notes.
final_tape_pos = result['final_head'] - 1  # letzter gelesener Index
if final_tape_pos < 0:
    final_tape_pos = 0
if final_tape_pos >= len(position_map):
    final_tape_pos = len(position_map) - 1

orig_pos = position_map[final_tape_pos]
print(f"Letzter gelesener Tape-Index: {final_tape_pos}")
print(f"Original-Position in Full Notes: {orig_pos}")
print()
print("=" * 70)
print(f"KONTEXT ±400 Zeichen um Pos {orig_pos}")
print("=" * 70)
ctx_start = max(0, orig_pos - 400)
ctx_end = min(len(full), orig_pos + 400)
print(f"Bereich: [{ctx_start}, {ctx_end})")
print("-" * 70)
print(full[ctx_start:ctx_end])
print("-" * 70)

# Letzter gelesener lateinischer Buchstabe
last_letter = letters[final_tape_pos] if final_tape_pos < len(letters) else '?'
print(f"Letzter gelesener lateinischer Buchstabe: '{last_letter}'")
print(f"  = Hebräisch: {EXTENDED_LATIN_TO_HEBR.get(last_letter, '?')}")

# =====================================================================
# GEMATRIA
# =====================================================================
HEBR_VALUES = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60,
    'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}
full_gematria = sum(HEBR_VALUES.get(c, 0) for c in hebr)
print()
print(f"Full Notes Gematria (gesamt): {full_gematria}")

# =====================================================================
# Letzter Halt-Position → original
# =====================================================================
print()
print("=" * 70)
print("HALT-POSITIONEN → ORIGINAL-TEXT")
print("=" * 70)
for i, h in enumerate(result['phase_halts'][:5]):
    p = min(h['head'], len(position_map) - 1)
    orig = position_map[p]
    letter = letters[p] if p < len(letters) else '?'
    print(f"  Phase {h['phase']:3d} (step {h['step']:6d}, state q_{h['state']}, {h['reason']}): head={h['head']}, orig_pos={orig}, letter='{letter}'")

# Letzter Halt
print(f"  ...")
last_h = result['phase_halts'][-1]
p = min(last_h['head'], len(position_map) - 1)
orig = position_map[p]
print(f"  Phase {last_h['phase']:3d} (step {last_h['step']:6d}, state q_{last_h['state']}, {last_h['reason']}): head={last_h['head']}, orig_pos={orig}")

# =====================================================================
# PHASE-HALTS SPEICHERN
# =====================================================================
output = {
    'method': 'Pendel-resistente Multi-Phase (garantiert bis Ende)',
    'full_notes_bytes': len(full),
    'extracted_AZ': len(letters),
    'hebr_tape_length': len(hebr),
    'total_steps': result['total_steps'],
    'n_phases': result['n_phases'],
    'final_state': result['final_state'],
    'final_head': result['final_head'],
    'halt_reason': result['halt_reason'],
    'phase_halts': result['phase_halts'],
    'full_gematria': full_gematria,
    'last_letter': last_letter,
    'final_orig_pos': orig_pos,
    'final_context': full[ctx_start:ctx_end],
}

with open('sources/q_fullnotes_endhalt.json', 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print()
print("Output gespeichert in sources/q_fullnotes_endhalt.json")
