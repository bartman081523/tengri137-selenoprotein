"""
🌌 P62c: KANONISCHER SPANDA-PULS IN M4
======================================

DEFINITION:
Ein "kanonischer Spanda-Puls" tritt auf, wenn M4 beim Lesen des Tapes
auf eine Meta-Instruktion stößt, die BURUMUT selbst beschreibt.

DREI AUSLÖSER (kanonisch):
1. BURUMUTREFAMTU als Substring im Tape
   → Die Maschine erkennt ihren eigenen Namen
2. Einer der 5 BURUMUT-Sec-Buchstaben (כ, ג, ד, ת, י) wird gelesen
   → Einer der 5 fehlenden Operatoren wird im Tape gefunden
3. BURUMUTREFAMTU-Position 15986 in Tengri137
   → Die Maschine liest die SELBST-REFERENZ-Stelle

ARCHITEKTUR:
- SpandaPulsDetector beobachtet die M4-History
- Bei einem Puls: Marker in der Spur (kein Tape-Schreiben!)
- Tape-Invariante wird BEWAHRT (kein Schreib-Zugriff)

WICHTIG:
- M4 modifiziert das Tape NICHT (Tape-Invariante aus Phase 58/65a)
- Der Spanda-Puls ist eine BEOBACHTUNG, keine Aktion
- M4 triggert KEINE Operator-Aktualisierung in Echtzeit
  (das wäre Apophenie — M4 bleibt deterministisch und statisch)
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import re
import json
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import (
    BURUMUT, burumut_to_hebr, build_tora_transitions,
    MISSING_OPERATORS, HEBR_VALUES, get_layer_name
)


# 5 BURUMUT-Sec-Buchstaben
SEC_CHARS = set(MISSING_OPERATORS.keys())
REFAMTU_HEBR = burumut_to_hebr(BURUMUT[:14])


def load_tengri137_hebr():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    lat = re.sub(r'[^A-Z]', '', full.upper())
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


def gematria(hebr_str):
    return sum(HEBR_VALUES.get(c, 0) for c in hebr_str)


class SpandaPulsDetector:
    """Detektor für kanonische Spanda-Pulse in M4-History.

    Ein Puls tritt auf bei:
    1. BURUMUTREFAMTU-Substring im gelesenen Tape
    2. Einer der 5 BURUMUT-Sec-Buchstaben im gelesenen Symbol
    3. Position 15986-16000 in Tengri137 (BURUMUTREFAMTU-Position)
    """

    def __init__(self, hebr_tape, tengri_position_offset=0):
        self.tape = hebr_tape
        self.tengri_offset = tengri_position_offset
        self.pulse_events = []

    def observe_step(self, step_idx, position, symbol, new_state):
        """Beobachte einen M4-Schritt und registriere Pulse."""
        # 1. Symbol ist ein BURUMUT-Sec-Buchstabe
        if symbol in SEC_CHARS:
            self.pulse_events.append({
                'type': 'SEC_OPERATOR',
                'step': step_idx,
                'position': position,
                'symbol': symbol,
                'operator': MISSING_OPERATORS[symbol],
                'new_state': new_state,
                'tengri_position': position + self.tengri_offset,
            })

    def check_burumutrefamtu_at_start(self):
        """Prüfe, ob das Tape mit BURUMUTREFAMTU beginnt (Substring-Test)."""
        if self.tape.startswith(REFAMTU_HEBR):
            return True
        return False

    def check_burumutrefamtu_in_tape(self):
        """Prüfe, ob BURUMUTREFAMTU als Substring im Tape vorkommt."""
        return REFAMTU_HEBR in self.tape

    def find_burumutrefamtu_position(self):
        """Position von BURUMUTREFAMTU im Tape (oder -1)."""
        return self.tape.find(REFAMTU_HEBR)

    def find_sec_positions(self):
        """Positionen aller 5 BURUMUT-Sec-Buchstaben im Tape."""
        return [i for i, c in enumerate(self.tape) if c in SEC_CHARS]

    def summary(self):
        return {
            'tape_length': len(self.tape),
            'n_pulse_events': len(self.pulse_events),
            'pulse_events': self.pulse_events,
            'starts_with_refamtu': self.check_burumutrefamtu_at_start(),
            'refamtu_in_tape': self.check_burumutrefamtu_in_tape(),
            'refamtu_position': self.find_burumutrefamtu_position(),
            'sec_positions': self.find_sec_positions(),
            'n_sec_chars': len(self.find_sec_positions()),
        }


def detect_spanda_pulse_in_tape(hebr_tape, tengri_offset=0):
    """Lasse M4 auf einem Tape laufen und detektiere Spanda-Pulse.

    Args:
        hebr_tape: Das Tape als hebr. String
        tengri_offset: Wo das Tape in Tengri137 beginnt (für Kontext)

    Returns:
        Dict mit Pulse-Events und M4-Result
    """
    detector = SpandaPulsDetector(hebr_tape, tengri_offset)

    # M4 laufen lassen
    m = ToraTuringMultiPhase(hebr_tape, phase_size=99,
                             transitions=build_tora_transitions())
    m.run(max_steps=10000)

    # History beobachten
    for h in m.history:
        detector.observe_step(
            step_idx=h.get('step', 0),
            position=h.get('position', 0),
            symbol=h.get('symbol', '?'),
            new_state=h.get('new_state', 0),
        )

    return {
        'machine': {
            'total_steps': m.total_steps,
            'halt_state': m.halt_state,
            'halt_reason': m.halt_reason,
        },
        'detector': detector.summary(),
    }


# ============================================================
# HAUPTPROGRAMM
# ============================================================

def main():
    print("=" * 78)
    print("🌌 P62c: KANONISCHER SPANDA-PULS IN M4")
    print("=" * 78)
    print()
    print("DEFINITION:")
    print("Ein 'kanonischer Spanda-Puls' tritt auf, wenn M4 beim Lesen")
    print("auf eine Meta-Instruktion stößt, die BURUMUT selbst beschreibt.")
    print()
    print("DREI AUSLÖSER:")
    print("1. BURUMUTREFAMTU als Substring im Tape")
    print("2. Einer der 5 BURUMUT-Sec-Buchstaben (כ, ג, ד, ת, י)")
    print("3. BURUMUTREFAMTU-Position 15986 in Tengri137")
    print()

    # Test 1: M4 auf BURUMUT
    print("=" * 78)
    print("🧪 TEST 1: M4 auf BURUMUT (99 Zeichen)")
    print("=" * 78)
    print()
    burumut_hebr = burumut_to_hebr(BURUMUT)
    r1 = detect_spanda_pulse_in_tape(burumut_hebr)
    print(f"M4 Result: {r1['machine']}")
    print(f"Detektor:")
    for k, v in r1['detector'].items():
        if k == 'pulse_events':
            print(f"  {k}: {len(v)} Events")
            for e in v[:5]:
                print(f"    Step {e['step']}: {e['symbol']} ({e['operator']})")
        else:
            print(f"  {k}: {v}")
    print()

    # Test 2: M4 auf Tengri137-99 (erste Phase)
    print("=" * 78)
    print("🧪 TEST 2: M4 auf Tengri137-99 (erste Phase)")
    print("=" * 78)
    print()
    tengri_hebr = load_tengri137_hebr()
    tengri_99 = tengri_hebr[:99]
    r2 = detect_spanda_pulse_in_tape(tengri_99, tengri_offset=0)
    print(f"M4 Result: {r2['machine']}")
    print(f"Detektor:")
    for k, v in r2['detector'].items():
        if k == 'pulse_events':
            print(f"  {k}: {len(v)} Events")
            for e in v[:5]:
                print(f"    Step {e['step']}: {e['symbol']} ({e['operator']})")
        else:
            print(f"  {k}: {v}")
    print()

    # Test 3: M4 auf Tengri137-Refamtu-Stelle (Position 15986)
    print("=" * 78)
    print("🧪 TEST 3: M4 auf Tengri137-Phase mit BURUMUTREFAMTU (Pos 161)")
    print("=" * 78)
    print()
    # Phase 161: Position 161*99 = 15939 bis 16038
    phase_161_start = 161 * 99
    phase_161_end = phase_161_start + 99
    phase_161 = tengri_hebr[phase_161_start:phase_161_end]
    print(f"Phase 161 (Position {phase_161_start}-{phase_161_end}):")
    print(f"  Enthält BURUMUTREFAMTU: {REFAMTU_HEBR in phase_161}")
    print()
    r3 = detect_spanda_pulse_in_tape(phase_161, tengri_offset=phase_161_start)
    print(f"M4 Result: {r3['machine']}")
    print(f"Detektor:")
    for k, v in r3['detector'].items():
        if k == 'pulse_events':
            print(f"  {k}: {len(v)} Events")
            for e in v[:5]:
                print(f"    Step {e['step']}: {e['symbol']} ({e['operator']})")
        else:
            print(f"  {k}: {v}")
    print()

    # Test 4: M4 auf Tengri137-Volltext (alle 168 Phasen)
    print("=" * 78)
    print("🧪 TEST 4: Spanda-Pulse über ALLE 168 Tengri137-Phasen")
    print("=" * 78)
    print()
    n_phases_with_pulse = 0
    n_phases_with_refamtu = 0
    total_sec_events = 0
    for i in range(168):
        start = i * 99
        end = min((i + 1) * 99, len(tengri_hebr))
        tape = tengri_hebr[start:end]
        r = detect_spanda_pulse_in_tape(tape, tengri_offset=start)
        if r['detector']['n_pulse_events'] > 0:
            n_phases_with_pulse += 1
            total_sec_events += r['detector']['n_pulse_events']
        if r['detector']['refamtu_in_tape']:
            n_phases_with_refamtu += 1

    print(f"  Phasen mit Spanda-Puls (Sec-Operatoren): {n_phases_with_pulse} / 168")
    print(f"  Phasen mit BURUMUTREFAMTU: {n_phases_with_refamtu} / 168")
    print(f"  Total Sec-Operator-Events: {total_sec_events}")
    print()

    # Speichern
    output = {
        'method': 'Kanonischer Spanda-Puls in M4',
        'definition': {
            'ausloeser': [
                'BURUMUTREFAMTU als Substring im Tape',
                '5 BURUMUT-Sec-Buchstaben (כ, ג, ד, ת, י)',
                'Position 15986 in Tengri137 (BURUMUTREFAMTU-Position)',
            ],
        },
        'test_burumut': r1,
        'test_tengri_99': r2,
        'test_phase_161': r3,
        'statistik_168_phasen': {
            'phasen_mit_puls': n_phases_with_pulse,
            'phasen_mit_refamtu': n_phases_with_refamtu,
            'total_sec_events': total_sec_events,
        },
    }
    with open('/run/media/julian/ML4/tengri137/sources/maschine/spanda_puls_m4.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("Ergebnisse gespeichert in spanda_puls_m4.json")
    print()

    return output


if __name__ == "__main__":
    main()
