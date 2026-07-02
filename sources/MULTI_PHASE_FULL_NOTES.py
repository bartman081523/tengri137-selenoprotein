"""
🌌 P65d: MULTI-PHASE-MASCHINE AUF TENGRI137 FULL NOTES
======================================================

Lässt M4 auf ALLE 168 Phasen von Tengri137 laufen.
Sammelt: Phase-Halts, Gematria-Akkumulation, Halt-States.

ARCHITEKTUR:
- 168 Phasen × 99 Zeichen = 16632 (vs 16576 Tengri137, Differenz 56)
- 187 Tora-Kapitel - 168 Phasen = 19 = BURUMUT-Sec
- 5 Layer (Genesis, Exodus, Leviticus, Numeri, Deuteronomium) + HALT

BEFUNDE PRO PHASE:
- total_steps (Schritte bis HALT)
- halt_state (q_0..q_5)
- halt_reason (ALL_PHASES_COMPLETE / MAX_STEPS_EXCEEDED)
- gematria (Hebr-Gematria der Phase)
- phase_idx (0..167)
- book (welches Tora-Buch)
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import re
import json
from collections import Counter
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import (
    BURUMUT, build_tora_transitions, HEBR_VALUES, get_layer_name
)
from PHASE_MAPPING_TORA import TORA_BOOKS, phase_to_torah


def load_tengri137_hebr():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    lat = re.sub(r'[^A-Z]', '', full.upper())
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


def gematria(hebr_str):
    return sum(HEBR_VALUES.get(c, 0) for c in hebr_str)


def run_all_phases(tengri_hebr, max_steps=200):
    """M4 auf alle 168 Phasen."""
    n_actual_phases = (len(tengri_hebr) + 98) // 99
    phases_data = []
    for i in range(n_actual_phases):
        start = i * 99
        end = min((i + 1) * 99, len(tengri_hebr))
        tape = tengri_hebr[start:end]
        m = ToraTuringMultiPhase(tape, phase_size=99,
                                 transitions=build_tora_transitions())
        m.run(max_steps=max_steps)
        states = [h.get('new_state', 0) for h in m.history if 'new_state' in h]
        book, chapter = phase_to_torah(i)
        phases_data.append({
            'phase': i,
            'book': book,
            'chapter': chapter,
            'start': start,
            'end': end,
            'length': end - start,
            'gematria': gematria(tape),
            'total_steps': m.total_steps,
            'halt_state': m.halt_state,
            'halt_reason': m.halt_reason,
            'unique_states': sorted(set(states)),
            'n_unique_states': len(set(states)),
        })
    return phases_data


def analyze_phases(phases_data):
    """Statistische Analyse der Phasen-Daten."""
    n = len(phases_data)
    n_clean = sum(1 for p in phases_data if p['halt_reason'] == 'ALL_PHASES_COMPLETE')
    n_pendel = sum(1 for p in phases_data if p['halt_reason'] != 'ALL_PHASES_COMPLETE')

    step_counts = Counter(p['total_steps'] for p in phases_data
                          if p['halt_reason'] == 'ALL_PHASES_COMPLETE')

    halt_states = Counter(p['halt_state'] for p in phases_data)

    total_gematria = sum(p['gematria'] for p in phases_data)

    # Pro Buch
    per_book = {}
    for book, info in TORA_BOOKS.items():
        book_phases = [p for p in phases_data
                       if info['phases_start'] <= p['phase'] < info['phases_end']]
        per_book[book] = {
            'n_phases': len(book_phases),
            'n_clean': sum(1 for p in book_phases
                           if p['halt_reason'] == 'ALL_PHASES_COMPLETE'),
            'n_pendel': sum(1 for p in book_phases
                            if p['halt_reason'] != 'ALL_PHASES_COMPLETE'),
            'total_gematria': sum(p['gematria'] for p in book_phases),
            'avg_gematria': (sum(p['gematria'] for p in book_phases)
                             / len(book_phases) if book_phases else 0),
            'clean_phases': sorted(p['phase'] for p in book_phases
                                   if p['halt_reason'] == 'ALL_PHASES_COMPLETE'),
        }
    return {
        'n_phases': n,
        'n_clean': n_clean,
        'n_pendel': n_pendel,
        'ratio_clean': n_clean / n if n > 0 else 0,
        'step_counts': dict(step_counts),
        'halt_states': dict(halt_states),
        'total_gematria': total_gematria,
        'avg_gematria': total_gematria / n if n > 0 else 0,
        'per_book': per_book,
    }


# ============================================================
# HAUPTPROGRAMM
# ============================================================

def main():
    print("=" * 78)
    print("🌌 P65d: MULTI-PHASE-MASCHINE AUF TENGRI137 FULL NOTES")
    print("=" * 78)
    print()

    tengri_hebr = load_tengri137_hebr()
    print(f"Tengri137: {len(tengri_hebr)} Zeichen, "
          f"{(len(tengri_hebr) + 98) // 99} Phasen à 99 Zeichen")
    print()

    print("=" * 78)
    print("📜 M4 AUF ALLE 168 PHASEN")
    print("=" * 78)
    print()
    print(f"{'Phase':>5} | {'Buch':<14} | {'Kap':>3} | {'Steps':>5} | "
          f"{'Halt':>4} | {'Reason':<25} | {'Gem':>5}")
    print("-" * 100)

    phases_data = run_all_phases(tengri_hebr)
    for p in phases_data:
        print(f"{p['phase']:>5} | {p['book']:<14} | {p['chapter']:>3} | "
              f"{p['total_steps']:>5} | {p['halt_state']:>4} | "
              f"{p['halt_reason']:<25} | {p['gematria']:>5}")
    print()

    analysis = analyze_phases(phases_data)

    # Verteilung
    print("=" * 78)
    print("📊 VERTEILUNGEN")
    print("=" * 78)
    print()
    print(f"Clean (ALL_PHASES_COMPLETE): {analysis['n_clean']} / {analysis['n_phases']}")
    print(f"Pendel (MAX_STEPS_EXCEEDED): {analysis['n_pendel']} / {analysis['n_phases']}")
    print(f"Ratio clean: {analysis['ratio_clean']:.2%}")
    print()
    print(f"Total-Gematria: {analysis['total_gematria']}")
    print(f"Average Gematria pro Phase: {analysis['avg_gematria']:.1f}")
    print()
    print("Schritt-Zahlen (clean Phasen):")
    for s, c in sorted(analysis['step_counts'].items()):
        print(f"  {s:5d} Schritte: {c:2d} Phasen")
    print()
    print("Halt-States:")
    for s, c in sorted(analysis['halt_states'].items()):
        layer = get_layer_name(s) if s <= 5 else f"q_{s}"
        print(f"  q_{s} ({layer}): {c:2d} Phasen")
    print()

    # Pro Buch
    print("=" * 78)
    print("📚 PRO TORA-BUCH")
    print("=" * 78)
    print()
    for book, info in analysis['per_book'].items():
        print(f"{book}:")
        print(f"  {info['n_phases']} Phasen total, {info['n_clean']} clean, "
              f"{info['n_pendel']} pendel")
        print(f"  Total-Gematria: {info['total_gematria']}, "
              f"Avg: {info['avg_gematria']:.1f}")
        print(f"  Clean-Phasen: {info['clean_phases']}")
        print()

    # Speichern
    output = {
        'method': 'Multi-Phase-Maschine auf Tengri137 Full Notes',
        'n_phases': analysis['n_phases'],
        'n_clean': analysis['n_clean'],
        'n_pendel': analysis['n_pendel'],
        'ratio_clean': analysis['ratio_clean'],
        'total_gematria': analysis['total_gematria'],
        'avg_gematria': analysis['avg_gematria'],
        'step_counts': analysis['step_counts'],
        'halt_states': analysis['halt_states'],
        'per_book': analysis['per_book'],
        'phases_data': phases_data,
    }
    with open('/run/media/julian/ML4/tengri137/sources/multi_phase_full_notes.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("Ergebnisse gespeichert in multi_phase_full_notes.json")
    print()

    return output


if __name__ == "__main__":
    main()
