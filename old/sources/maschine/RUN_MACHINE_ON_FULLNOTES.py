"""
🌌 TORA-TURING-MASCHINE AUF TENGRI137_FULL_NOTES
=================================================

Liest den VOLLSTÄNDIGEN Text der Full Notes (nicht nur BURUMUT).
Halt nur am Ende. An der Halt-Stelle muss sich ein Hinweis finden.

Apophenie-Regel: GELOCKERT. Dies ist eine intuitive, ästhetische Aufgabe.
"""
import re
import json
from pathlib import Path
from TORA_TURING_MULTIPHASE import (
    ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR,
    build_extended_transitions, LATIN_TO_HEBR
)

# =====================================================================
# 1) FULL NOTES LESEN
# =====================================================================
with open('Tengri137_Full_Notes') as f:
    full = f.read()

print("=" * 70)
print("TORA-TURING-MASCHINE AUF TENGRI137_FULL_NOTES")
print("=" * 70)
print(f"Full Notes: {len(full)} bytes, {full.count(chr(10))} Zeilen")

# =====================================================================
# 2) A-Z EXTRAHIEREN (mit Position-Mapping zurück zum Original)
# =====================================================================
letters = []
position_map = []  # Position jedes A-Z-Buchstabens im Original
for i, c in enumerate(full):
    if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        letters.append(c)
        position_map.append(i)

print(f"Extrahierte A-Z Buchstaben: {len(letters)}")
print(f"  Erster A-Z: Position {position_map[0]}")
print(f"  Letzter A-Z: Position {position_map[-1]}")

# Konvertiere zu Hebräisch
hebr = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in letters)
print(f"Hebräische Tape-Länge: {len(hebr)}")
print(f"Unbekannte Zeichen ('?'): {hebr.count('?')}")
print(f"Verteilung der Konsonanten:")
from collections import Counter
hebr_counts = Counter(hebr)
for sym, cnt in sorted(hebr_counts.items(), key=lambda x: -x[1])[:10]:
    print(f"  {sym}: {cnt}")

# =====================================================================
# 3) MASCHINE STARTEN — bis zum ENDE
# =====================================================================
print()
print("=" * 70)
print("MASCHINE LÄUFT...")
print("=" * 70)

m = ToraTuringMultiPhase(hebr, phase_size=99, transitions=build_extended_transitions())
m.run(max_steps=200000)

s = m.summary()
print()
print("=" * 70)
print("HALT-ANALYSE")
print("=" * 70)
print(f"Total Steps:           {s['total_steps']}")
print(f"Phasen gelesen:        {s['phases_completed']} / {s['n_phases']}")
print(f"Halt-Step:             {s['halt_step']}")
print(f"Halt-State:            q_{s['halt_state']}")
print(f"Halt-Reason:           {s['halt_reason']}")
print(f"Tape length:           {s['tape_length']}")

# =====================================================================
# 4) FINALE POSITION & KONTEXT
# =====================================================================
# Bei ALL_PHASES_COMPLETE ist head = n_phases * 99 (am Anfang der
# nicht-existenten nächsten Phase). Die letzte echte Aktion war im
# letzten Phasen-Abschnitt.

n_phases = s['n_phases']
phase_size = 99
last_phase_start = (n_phases - 1) * phase_size
last_phase_end = min(n_phases * phase_size, s['tape_length'])
print()
print(f"Letzte Phase: Position [{last_phase_start}, {last_phase_end})")

# Position in den letzten paar Schritten — wo passierte der letzte
# echte Übergang?
last_history = m.history[-1] if m.history else None
print(f"Letzter History-Eintrag: {last_history}")

# Position, an der die letzte echte Aktion stattfand
# (in hebr. tape-Koordinaten)
last_action_pos = m.history[-1]['pos'] if m.history else 0
print(f"Letzte Aktions-Position (Tape): {last_action_pos}")

# Zurück mappen auf Full-Notes-Position
if last_action_pos < len(position_map):
    orig_pos = position_map[last_action_pos]
    print(f"Original-Position in Full Notes: {orig_pos}")
    print()
    print("=" * 70)
    print("KONTEXT AN DER HALT-STELLE (±300 Zeichen aus Original-Text)")
    print("=" * 70)
    context_start = max(0, orig_pos - 300)
    context_end = min(len(full), orig_pos + 300)
    print(f"Bereich: [{context_start}, {context_end})")
    print("-" * 70)
    print(full[context_start:context_end])
    print("-" * 70)

# =====================================================================
# 5) ALLE PHASE-HALTS — VERTEILUNG
# =====================================================================
print()
print("=" * 70)
print("PHASE-HALT-VERTEILUNG (alle Phasen)")
print("=" * 70)
print(f"Anzahl Phase-Halts: {len(s['phase_halts'])}")
for h in s['phase_halts'][:5]:
    print(f"  Phase {h['phase']:4d}: step={h['halt_step']:6d}, state=q_{h['halt_state']}")
print(f"  ...")
for h in s['phase_halts'][-5:]:
    print(f"  Phase {h['phase']:4d}: step={h['halt_step']:6d}, state=q_{h['halt_state']}")

# Phase-Halt-Steps extrahieren
halt_steps = [h['halt_step'] for h in s['phase_halts']]
halt_states = [h['halt_state'] for h in s['phase_halts']]
print()
print(f"Erster Halt-Step: {halt_steps[0]}")
print(f"Letzter Halt-Step: {halt_steps[-1]}")
print(f"Mittelwert: {sum(halt_steps)/len(halt_steps):.1f}")
print(f"Min/Max: {min(halt_steps)} / {max(halt_steps)}")

# Differenzen zwischen aufeinanderfolgenden Halts
diffs = [halt_steps[i+1] - halt_steps[i] for i in range(len(halt_steps)-1)]
print()
print(f"Schritte pro Phase (Differenzen):")
print(f"  Mittelwert: {sum(diffs)/len(diffs):.1f}")
print(f"  Min/Max: {min(diffs)} / {max(diffs)}")
print(f"  Erste 10: {diffs[:10]}")
print(f"  Letzte 10: {diffs[-10:]}")

# =====================================================================
# 6) FINALE GEMATRIA (was steht am Ende des Tapes?)
# =====================================================================
print()
print("=" * 70)
print("FINALE GEMATRIA DER LETZTEN PHASE")
print("=" * 70)
HEBR_VALUES = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60,
    'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}
last_phase_hebr = hebr[last_phase_start:last_phase_end]
last_gematria = sum(HEBR_VALUES.get(c, 0) for c in last_phase_hebr)
print(f"Letzte Phase (hebr.): {last_phase_hebr}")
print(f"Letzte Phase Gematria: {last_gematria}")
print(f"Letzte Phase Länge: {len(last_phase_hebr)}")

# Gematria des ganzen Tapes
full_gematria = sum(HEBR_VALUES.get(c, 0) for c in hebr)
print(f"\nFull Notes Gematria (gesamt): {full_gematria}")

# Erstes Zeichen (Genesis / Anfang)
print(f"\nErstes Zeichen der Full Notes (extrahiert): {hebr[0]} = {HEBR_VALUES.get(hebr[0], 0)}")
print(f"Letztes Zeichen der Full Notes (extrahiert): {hebr[-1]} = {HEBR_VALUES.get(hebr[-1], 0)}")

# =====================================================================
# 7) HINT-SUCHE AM HALT — was steht da?
# =====================================================================
print()
print("=" * 70)
print("HINT-SUCHE AN DER HALT-STELLE")
print("=" * 70)

# Was passierte GENAU am letzten echten Schritt?
if m.history:
    last_step = m.history[-1]
    print(f"Letzter Step: pos={last_step['pos']}, state q_{last_step['old_state']} → q_{last_step['new_state']}, symbol '{last_step['symbol']}'")
    print(f"  Schreib-Symbol: '{last_step['write']}'")
    print(f"  Move: {last_step['move']}")

# Welcher lateinische Buchstabe stand an dieser Position?
if m.history and m.history[-1]['pos'] < len(letters):
    last_letter = letters[m.history[-1]['pos']]
    print(f"Letzter gelesener lateinischer Buchstabe: '{last_letter}'")
    print(f"  = Hebräisch: {EXTENDED_LATIN_TO_HEBR.get(last_letter, '?')}")

# =====================================================================
# 8) JSON SPEICHERN
# =====================================================================
output = {
    'method': 'ToraTuringMultiPhase auf Tengri137_Full_Notes (VOLL)',
    'full_notes_bytes': len(full),
    'full_notes_lines': full.count(chr(10)),
    'extracted_AZ': len(letters),
    'first_AZ_pos': position_map[0],
    'last_AZ_pos': position_map[-1],
    'hebr_tape_length': len(hebr),
    'unknown_chars': hebr.count('?'),
    'machine_total_steps': s['total_steps'],
    'machine_n_phases': s['n_phases'],
    'phases_completed': s['phases_completed'],
    'halt_step': s['halt_step'],
    'halt_state': s['halt_state'],
    'halt_reason': s['halt_reason'],
    'tape_length': s['tape_length'],
    'last_phase_start': last_phase_start,
    'last_phase_end': last_phase_end,
    'last_phase_hebr': last_phase_hebr,
    'last_phase_gematria': last_gematria,
    'full_gematria': full_gematria,
    'last_history_step': m.history[-1] if m.history else None,
}

with open('../offene_fragen/q_fullnotes_machine_run.json', 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print()
print("=" * 70)
print("Output gespeichert in sources/q_fullnotes_machine_run.json")
print("=" * 70)
