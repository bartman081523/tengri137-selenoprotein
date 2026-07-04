"""
🌌 PHASEN-ÜBERGANGS-MAPPING: Tora ↔ Tengri137
=================================================

HYPOTHESE (Weg 2, P30, P45b):
Die 168 Phasen von Tengri137 spiegeln die 187 Kapitel der Tora.
- 187 - 168 = 19 = BURUMUT-Sec (Sec-Positionen)
- 168 × 99 = 16632 (vs 16576 Tengri137, Diff = 56)
- 56 = erste BURUMUTREFAMTU-Länge, die in Tengri137 identisch ist

MAPPING (Verhältnis):
  Genesis (50) → 45 Phasen (0..44)
  Exodus (40) → 36 Phasen (45..80)
  Leviticus (27) → 24 Phasen (81..104)
  Numeri (36) → 32 Phasen (105..136)
  Deuteronomium (34) → 31 Phasen (137..167)
  Total: 168 Phasen

VERIFIKATION:
1. Numerische Brücke zwischen Phasen-Gematria und Tora-Kapitel-Summen
2. Welche Phasen sind "kanonisch resonant" (1, 6, 12, 15, 7, 3, 10, 4)
3. Welche Phasen sind BURUMUTREFAMTU (Phase 121 = "+1")?
4. Welche Phasen entsprechen den 30 Tora-Referenzen?
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import re
import json
from collections import Counter
from maschine.TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from maschine.TORA_TURING_CORRECT import (
    build_tora_transitions, get_layer_name, HEBR_VALUES
)


# Tora-Struktur
TORA_BOOKS = {
    'Genesis':       {'chapters': 50, 'phases_start': 0,  'phases_end': 45},
    'Exodus':        {'chapters': 40, 'phases_start': 45, 'phases_end': 81},
    'Leviticus':     {'chapters': 27, 'phases_start': 81, 'phases_end': 105},
    'Numeri':        {'chapters': 36, 'phases_start': 105, 'phases_end': 137},
    'Deuteronomium': {'chapters': 34, 'phases_start': 137, 'phases_end': 168},
}
TOTAL_CHAPTERS = 187
TOTAL_PHASES = 168


def gematria(hebr_str):
    """Berechne Gematria eines hebr. Strings."""
    return sum(HEBR_VALUES.get(c, 0) for c in hebr_str)


def run_phase(tape, max_steps=200):
    """Eine Phase (≤99 Zeichen) durch M4 laufen lassen."""
    m = ToraTuringMultiPhase(tape, phase_size=99,
                             transitions=build_tora_transitions())
    m.run(max_steps=max_steps)

    states = [h.get('new_state', 0) for h in m.history if 'new_state' in h]
    return {
        'total_steps': m.total_steps,
        'halt_state': m.halt_state,
        'halt_reason': m.halt_reason,
        'unique_states': sorted(set(states)),
        'n_unique_states': len(set(states)),
        'state_transitions': len(states),
    }


def phase_to_torah(phase_idx):
    """Map Phase-Index auf (Buch, Kapitel)."""
    for book, info in TORA_BOOKS.items():
        if info['phases_start'] <= phase_idx < info['phases_end']:
            # Phasen-Index innerhalb des Buches
            phases_in_book = info['phases_end'] - info['phases_start']
            chap_in_book = info['chapters']
            # Verteilung: 1 Kapitel ≈ phases_in_book / chap_in_book Phasen
            phase_offset = phase_idx - info['phases_start']
            chapter = 1 + (phase_offset * chap_in_book) // phases_in_book
            if chapter > chap_in_book:
                chapter = chap_in_book
            return book, chapter
    return None, None


# ============================================================
# HAUPTPROGRAMM
# ============================================================

def main():
    print("=" * 78)
    print("🌌 PHASEN-ÜBERGANGS-MAPPING: Tora ↔ Tengri137")
    print("=" * 78)
    print()
    print("Hypothese: Die 168 Phasen von Tengri137 spiegeln die 187 Kapitel der Tora.")
    print()

    # Tora-Struktur anzeigen
    print("Tora-Struktur:")
    for book, info in TORA_BOOKS.items():
        n_phases = info['phases_end'] - info['phases_start']
        print(f"  {book:18s}: {info['chapters']:3d} Kapitel → {n_phases:3d} Phasen "
              f"({info['phases_start']:3d}..{info['phases_end']-1:3d})")
    print(f"  Total: {TOTAL_CHAPTERS} Kapitel → {TOTAL_PHASES} Phasen")
    print()

    # Tengri137 laden
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    all_letters = re.sub(r'[^A-Z]', '', full.upper())
    tengri_hebr = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in all_letters)
    n_actual_phases = (len(tengri_hebr) + 98) // 99
    print(f"Tengri137: {len(tengri_hebr)} Zeichen, {n_actual_phases} Phasen à 99")
    print()

    # Numerische Brücke
    print("=" * 78)
    print("🔢 NUMERISCHE BRÜCKE")
    print("=" * 78)
    print()
    print(f"  187 (Tora) - 168 (Phasen) = 19 = BURUMUT-Sec")
    print(f"  168 × 99 = {168*99} (vs 16576 Tengri137, Differenz {168*99-16576})")
    print(f"  187 × 99 = {187*99} (Tora komplett, Differenz zu Tengri {187*99-16576})")
    print(f"  Differenz 168 vs 187: 19 = Sec")
    print()

    # Pro Phase: M4-Lauf + Tora-Mapping
    print("=" * 78)
    print("📜 PHASEN-ANALYSE (alle 168 Phasen)")
    print("=" * 78)
    print()
    print(f"{'Phase':>5} | {'Buch':<14} | {'Kap':>3} | {'Steps':>5} | {'Halt':<25} | {'States':<20} | {'Gem':>5}")
    print("-" * 120)

    phases_data = []
    for phase_idx in range(n_actual_phases):
        start = phase_idx * 99
        end = min((phase_idx + 1) * 99, len(tengri_hebr))
        phase_tape = tengri_hebr[start:end]
        phase_gematria = gematria(phase_tape)

        result = run_phase(phase_tape)
        book, chapter = phase_to_torah(phase_idx)

        states_str = ','.join(str(s) for s in result['unique_states'][:6])
        halt_str = result['halt_reason'][:24]

        phases_data.append({
            'phase': phase_idx,
            'book': book,
            'chapter': chapter,
            'total_steps': result['total_steps'],
            'halt_state': result['halt_state'],
            'halt_reason': result['halt_reason'],
            'unique_states': result['unique_states'],
            'gematria': phase_gematria,
        })

        # Drucke alle Phasen
        print(f"{phase_idx:>5} | {book:<14} | {chapter:>3} | "
              f"{result['total_steps']:>5} | {halt_str:<25} | "
              f"{states_str:<20} | {phase_gematria:>5}")

    # Verteilung
    print()
    print("=" * 78)
    print("📊 VERTEILUNGEN")
    print("=" * 78)
    print()

    # Clean vs Pendel
    clean = [p for p in phases_data if p['halt_reason'] == 'ALL_PHASES_COMPLETE']
    pendel = [p for p in phases_data if p['halt_reason'] != 'ALL_PHASES_COMPLETE']
    print(f"Clean (ALL_PHASES_COMPLETE): {len(clean)} / {n_actual_phases}")
    print(f"Pendel (MAX_STEPS_EXCEEDED): {len(pendel)} / {n_actual_phases}")
    print()

    # Schritt-Zahl-Verteilung
    step_counts = Counter(p['total_steps'] for p in clean)
    print("Schritt-Zahlen (clean Phasen):")
    for s, c in sorted(step_counts.items()):
        print(f"  {s:3d} Schritte: {c:2d} Phasen")
    print()

    # Pro Buch
    for book, info in TORA_BOOKS.items():
        book_phases = [p for p in phases_data
                       if info['phases_start'] <= p['phase'] < info['phases_end']]
        book_clean = [p for p in book_phases if p['halt_reason'] == 'ALL_PHASES_COMPLETE']
        book_gematria = sum(p['gematria'] for p in book_phases)
        print(f"{book}:")
        print(f"  {len(book_phases)} Phasen total, {len(book_clean)} clean")
        print(f"  Total-Gematria: {book_gematria}")
        print(f"  Clean-Phasen: {sorted(p['phase'] for p in book_clean)}")
    print()

    # BURUMUT-Sec-Beziehung
    print("=" * 78)
    print("🔑 BURUMUT-SEC-BEZIEHUNG")
    print("=" * 78)
    print()
    print("187 Tora-Kapitel - 168 Tengri137-Phasen = 19 = BURUMUT-Sec")
    print()

    # Kanonische Schritt-Zahlen: 1, 3, 4, 5, 6, 7, 10, 12, 15
    canonical = [1, 3, 4, 5, 6, 7, 10, 12, 15]
    print("Kanonische Resonanz-Phasen:")
    for s in canonical:
        n_with = sum(1 for p in clean if p['total_steps'] == s)
        print(f"  {s:3d} Schritte: {n_with} Phasen")
    print()

    # 11² + 1 = 122 — die BURUMUT-Architektur
    # Phase 121 = das "+1" = BURUMUT
    print("BURUMUT-Architektur (11²+1=122):")
    print(f"  Phase 121: Phase-Idx {121}, Tora-Mapping:")
    if 121 < n_actual_phases:
        p = phases_data[121]
        print(f"    Buch: {p['book']}, Kapitel: {p['chapter']}, Steps: {p['total_steps']}, Gematria: {p['gematria']}")
    print()

    # Speichern
    output = {
        'method': 'Phasen-Übergangs-Mapping Tora ↔ Tengri137',
        'tora_structure': TORA_BOOKS,
        'n_tengri_phases': n_actual_phases,
        'n_tora_chapters': TOTAL_CHAPTERS,
        'differenz': TOTAL_CHAPTERS - n_actual_phases,
        'differenz_meaning': 'BURUMUT-Sec (19)',
        'phases_data': phases_data,
    }
    with open('/run/media/julian/ML4/tengri137/sources/phasen/phase_mapping_tora.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("Ergebnisse gespeichert in phase_mapping_tora.json")

    return phases_data


if __name__ == "__main__":
    main()
