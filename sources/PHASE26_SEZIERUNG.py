"""
🌌 P69: SEZIERUNG DER SINGULARITÄT — PHASE 26 (Gen 29)
========================================================

Drei exakte Analysen an Phase 26 (Genesis 29, 99 Zeichen, 20 Sec-Operatoren):

1. Phase26OperatorMap: Wo sind die 20 Sec-Operatoren? Welche Typen?
2. PointOfFailure: Wo reißt 37² im strict-Mode?
3. ResonanzEcho: Wohin fällt die Maschine bei Backtrack?

ARCHITEKTUR:
- Phase 26 = Tengri137 Position 2574-2672 (hebr.)
- 99 Zeichen, 20 Sec-Operatoren (Maximum in Tengri137)
- In unserer Maschine: Punkt maximaler Operator-Dichte
- KVM-Strict-Mode: bei erster Violation → Backtrack

PRINZIPIEN:
- Vollständig deterministisch
- Modifiziert das Tape NICHT
- Beobachtet nur M4
- Reproduziert exakte Befunde
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import re
from typing import List, Dict, Any
from collections import Counter
from KANONIK_VALIDATOR_MODUL import (
    KanonikValidator, GematriaAnchor
)
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import (
    BURUMUT, burumut_to_hebr, HEBR_VALUES, MISSING_OPERATORS, build_tora_transitions
)
from PHASE_MAPPING_TORA import phase_to_torah


def load_tengri137_hebr():
    """Lade Tengri137 als hebr. String."""
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    lat = re.sub(r'[^A-Z]', '', full.upper())
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


def get_phase_26():
    """Extrahiere Phase 26 (Gen 29) aus Tengri137."""
    tengri_hebr = load_tengri137_hebr()
    return tengri_hebr[26*99:27*99]


# ============================================================
# 1) Phase26OperatorMap
# ============================================================

class Phase26OperatorMap:
    """Karte der 20 Sec-Operatoren in Phase 26.

    Findet:
    - sec_positions: Liste der Positionen (0-98)
    - sec_letters: Liste der hebr. Buchstaben
    - sec_distribution: Verteilung der 5 Sec-Typen
    - sec_gaps: Abstände zwischen aufeinanderfolgenden Sec-Operatoren
    - avg_gap: durchschnittlicher Abstand
    """

    def __init__(self, phase_26: str):
        self.phase_26 = phase_26
        self._compute()

    def _compute(self):
        """Berechne alle Operator-Informationen."""
        positions = []
        letters = []
        for i, c in enumerate(self.phase_26):
            if c in MISSING_OPERATORS:
                positions.append(i)
                letters.append(c)

        self.n_sec_total = len(positions)
        self.sec_positions = positions
        self.sec_letters = letters
        self.sec_distribution = Counter(letters)

        # Abstände
        if len(positions) >= 2:
            gaps = [positions[i+1] - positions[i]
                    for i in range(len(positions) - 1)]
        else:
            gaps = []
        self.sec_gaps = gaps
        self.avg_gap = sum(gaps) / len(gaps) if gaps else 0

    def analyse(self) -> Dict[str, Any]:
        """Vollständige Analyse als Dict."""
        return {
            'n_sec_total': self.n_sec_total,
            'sec_positions': self.sec_positions,
            'sec_letters': self.sec_letters,
            'sec_distribution': dict(self.sec_distribution),
            'sec_gaps': self.sec_gaps,
            'avg_gap': self.avg_gap,
            'positions_by_type': {
                op: [i for i, c in enumerate(self.phase_26) if c == op]
                for op in MISSING_OPERATORS
            },
        }


# ============================================================
# 2) PointOfFailure
# ============================================================

class PointOfFailure:
    """Findet den exakten Punkt, an dem 37² im strict-Mode reißt.

    Methode:
    - Erstelle M4 auf Phase 26
    - Erstelle KVM im strict-Mode
    - Laufe schrittweise
    - Bei erster Violation: dokumentiere exakten Zustand
    - WICHTIG: Wir beobachten nur, brechen NICHT ab
      (sonst würden wir die späteren Schritte nicht sehen)
    """

    def __init__(self, phase_26: str, strict: bool = True):
        self.phase_26 = phase_26
        self.strict = strict
        self.machine = ToraTuringMultiPhase(
            phase_26, phase_size=99, transitions=build_tora_transitions()
        )
        self.anchor = GematriaAnchor(bridge=37)
        self.validator = KanonikValidator(
            self.machine, anchor=self.anchor, strict=False
        )  # Wir machen das Backtracking MANUELL für Observation

        # Failure-Info
        self.failure_step = None
        self.failure_position = None
        self.failure_symbol = None
        self.failure_gematria = None
        self.failure_state = None
        self.failure_gematria_acc = None

        # Last valid
        self.last_valid_state = None
        self.last_valid_position = None
        self.last_valid_gematria_acc = None

    def run(self, max_steps: int = 200):
        """Laufe und finde den ersten Failure-Punkt."""
        # Initialer Snapshot (Step 0, acc=0)
        from KANONIK_VALIDATOR_MODUL import Snapshot
        initial = Snapshot(
            state=self.machine.state,
            head=self.machine.head,
            gematria_acc=0,
            step=0,
            phase=self.machine.phase,
            phase_start=self.machine.phase * self.machine.phase_size,
        )
        self.validator.snapshots.append(initial)
        self.validator.last_valid_snapshot = initial
        self.last_valid_state = 0
        self.last_valid_position = 0
        self.last_valid_gematria_acc = 0

        # Hauptschleife
        while (not self.machine.halted
               and self.machine.total_steps < max_steps
               and self.failure_step is None):
            # M4 macht einen Schritt
            self.machine.step()
            if self.machine.halted:
                break

            # KVM beobachtet (manuell, OHNE auto-Backtrack)
            self._observe_step_manually()

    def _observe_step_manually(self):
        """Beobachte einen Schritt OHNE auto-Backtrack (zur Beobachtung)."""
        from KANONIK_VALIDATOR_MODUL import Snapshot

        # Gematria-Akkumulation
        if self.validator.snapshots:
            prev_acc = self.validator.snapshots[-1].gematria_acc
        else:
            prev_acc = 0

        if self.machine.head < len(self.machine.tape):
            current_gem = HEBR_VALUES.get(
                self.machine.tape[self.machine.head], 0
            )
        else:
            current_gem = 0

        gematria_acc = prev_acc + current_gem

        snapshot = Snapshot(
            state=self.machine.state,
            head=self.machine.head,
            gematria_acc=gematria_acc,
            step=self.machine.total_steps,
            phase=self.machine.phase,
            phase_start=self.machine.phase * self.machine.phase_size,
        )
        self.validator.snapshots.append(snapshot)

        # Anchor-Prüfung
        if not self.anchor.is_anchor(gematria_acc):
            # VIOLATION! Dies ist der Failure-Punkt
            if self.failure_step is None:
                # Dokumentiere Failure
                self.failure_step = self.machine.total_steps
                self.failure_position = self.machine.head
                if self.machine.head < len(self.machine.tape):
                    self.failure_symbol = self.machine.tape[self.machine.head]
                else:
                    self.failure_symbol = None
                self.failure_gematria = current_gem
                self.failure_state = self.machine.state
                self.failure_gematria_acc = gematria_acc

                # Letzter gültiger Snapshot (VOR diesem)
                if len(self.validator.snapshots) >= 2:
                    last_valid = self.validator.snapshots[-2]
                    self.last_valid_state = last_valid.state
                    self.last_valid_position = last_valid.head
                    self.last_valid_gematria_acc = last_valid.gematria_acc
        else:
            # Gültig → update last_valid (nur wenn NICHT strict)
            if not self.strict:
                self.validator.last_valid_snapshot = snapshot

    def analyse(self) -> Dict[str, Any]:
        """Vollständige Analyse als Dict."""
        return {
            'failure_step': self.failure_step,
            'failure_position': self.failure_position,
            'failure_symbol': self.failure_symbol,
            'failure_gematria': self.failure_gematria,
            'failure_state': self.failure_state,
            'failure_gematria_acc': self.failure_gematria_acc,
            'last_valid_state': self.last_valid_state,
            'last_valid_position': self.last_valid_position,
            'last_valid_gematria_acc': self.last_valid_gematria_acc,
            'phase_26_length': len(self.phase_26),
            'total_steps_executed': self.machine.total_steps,
        }


# ============================================================
# 3) ResonanzEcho
# ============================================================

class ResonanzEcho:
    """Wohin fällt die Maschine bei KVM-Backtracking?

    Methode:
    - Erstelle M4 auf Phase 26
    - Erstelle KVM im strict-Mode
    - Laufe schrittweise
    - Bei Violation: KVM restored automatisch
    - Dokumentiere: wohin wurde restored?
    - Laufe weiter bis zur nächsten Violation
    - Wiederhole, bis Maschine gehalten oder max Restores erreicht
    """

    def __init__(self, phase_26: str, max_restores: int = 10):
        self.phase_26 = phase_26
        self.max_restores = max_restores
        self.machine = ToraTuringMultiPhase(
            phase_26, phase_size=99, transitions=build_tora_transitions()
        )
        self.validator = KanonikValidator(
            self.machine, anchor=GematriaAnchor(bridge=37), strict=True
        )

        # Restore-Tracking
        self.n_restores = 0
        self.last_restore_state = None
        self.last_restore_position = None
        self.last_restore_gematria_acc = None
        self.restore_history = []

    def run(self, max_steps: int = 500):
        """Laufe mit KVM-Strict-Mode, dokumentiere Restores."""
        # Initialer Snapshot
        from KANONIK_VALIDATOR_MODUL import Snapshot
        initial = Snapshot(
            state=self.machine.state,
            head=self.machine.head,
            gematria_acc=0,
            step=0,
            phase=self.machine.phase,
            phase_start=self.machine.phase * self.machine.phase_size,
        )
        self.validator.snapshots.append(initial)
        self.validator.last_valid_snapshot = initial

        # Hauptschleife
        while (not self.machine.halted
               and self.machine.total_steps < max_steps
               and self.n_restores < self.max_restores):
            self.machine.step()
            if self.machine.halted:
                break
            self.validator.observe_step()

            # Prüfe, ob ein Backtrack stattgefunden hat
            if (self.validator.n_backtracks > self.n_restores):
                # Neuer Backtrack!
                self.n_restores = self.validator.n_backtracks
                if self.validator.restored_to_snapshot:
                    snap = self.validator.restored_to_snapshot
                    self.last_restore_state = snap.state
                    self.last_restore_position = snap.head
                    self.last_restore_gematria_acc = snap.gematria_acc
                    self.restore_history.append({
                        'restore_n': self.n_restores,
                        'state': snap.state,
                        'position': snap.head,
                        'gematria_acc': snap.gematria_acc,
                        'step': snap.step,
                    })

    def analyse(self) -> Dict[str, Any]:
        """Vollständige Analyse als Dict."""
        return {
            'n_restores': self.n_restores,
            'last_restore_state': self.last_restore_state,
            'last_restore_position': self.last_restore_position,
            'last_restore_gematria_acc': self.last_restore_gematria_acc,
            'restore_to_step': (
                self.restore_history[-1]['step'] if self.restore_history else None
            ),
            'restore_history': self.restore_history,
            'total_steps_executed': self.machine.total_steps,
            'halt_reason': self.machine.halt_reason,
        }


# ============================================================
# 4) seziere_phase_26 — Master-Funktion
# ============================================================

def seziere_phase_26() -> Dict[str, Any]:
    """Kombinierte Sezierung: alle drei Analysen.

    Returns:
        Dict mit operator_map, point_of_failure, resonanz_echo, phase_26_meta
    """
    phase_26 = get_phase_26()

    # 1) Operator-Map
    op_map = Phase26OperatorMap(phase_26)
    op_map_result = op_map.analyse()

    # 2) Point of Failure
    pof = PointOfFailure(phase_26, strict=True)
    pof.run()
    pof_result = pof.analyse()

    # 3) Resonanz-Echo
    echo = ResonanzEcho(phase_26, max_restores=10)
    echo.run()
    echo_result = echo.analyse()

    # 4) Meta
    book, chap = phase_to_torah(26)
    meta = {
        'book': book,
        'chapter': chap,
        'phase_idx': 26,
        'length': len(phase_26),
        'n_sec_operators': sum(1 for c in phase_26 if c in MISSING_OPERATORS),
        'gematria': sum(HEBR_VALUES.get(c, 0) for c in phase_26),
    }

    return {
        'operator_map': op_map_result,
        'point_of_failure': pof_result,
        'resonanz_echo': echo_result,
        'phase_26_meta': meta,
    }


# ============================================================
# SELBST-TEST
# ============================================================

if __name__ == "__main__":
    import json
    print("=" * 78)
    print("🌌 P69: SEZIERUNG DER SINGULARITÄT — PHASE 26")
    print("=" * 78)
    print()
    print("Drei Analysen an Phase 26 (Gen 29, 99 Zch, 20 Sec-Operatoren):")
    print("  1. Phase26OperatorMap: Wo sind die 20 Sec?")
    print("  2. PointOfFailure: Wo reißt 37² im strict-Mode?")
    print("  3. ResonanzEcho: Wohin fällt die Maschine bei Backtrack?")
    print()

    result = seziere_phase_26()

    # Meta
    meta = result['phase_26_meta']
    print("=" * 78)
    print("📍 META")
    print("=" * 78)
    print(f"  Buch: {meta['book']} {meta['chapter']}")
    print(f"  Phase: {meta['phase_idx']}")
    print(f"  Länge: {meta['length']}")
    print(f"  Sec-Operatoren: {meta['n_sec_operators']}")
    print(f"  Gematria: {meta['gematria']}")
    print()

    # Operator-Map
    op = result['operator_map']
    print("=" * 78)
    print("🔤 OPERATOR-MAP")
    print("=" * 78)
    print(f"  Total Sec: {op['n_sec_total']}")
    print(f"  Positionen: {op['sec_positions']}")
    print(f"  Verteilung: {op['sec_distribution']}")
    print(f"  Mittlerer Abstand: {op['avg_gap']:.2f}")
    print()
    print("  Per-Operator Positionen:")
    for op_type, positions in op['positions_by_type'].items():
        if positions:
            print(f"    {op_type} ({MISSING_OPERATORS[op_type]}): {positions}")
    print()

    # Point of Failure
    pof = result['point_of_failure']
    print("=" * 78)
    print("💥 POINT OF FAILURE")
    print("=" * 78)
    if pof['failure_step'] is not None:
        print(f"  Failure-Step: {pof['failure_step']}")
        print(f"  Failure-Position: {pof['failure_position']}")
        print(f"  Failure-Symbol: {pof['failure_symbol']}")
        print(f"  Failure-Gematria: {pof['failure_gematria']}")
        print(f"  Failure-State: q_{pof['failure_state']}")
        print(f"  Failure-Gematria-Acc: {pof['failure_gematria_acc']} "
              f"(NICHT durch 37 teilbar: {pof['failure_gematria_acc'] % 37})")
        print()
        print("  Letzter gültiger Snapshot (vor Failure):")
        print(f"    State: q_{pof['last_valid_state']}")
        print(f"    Position: {pof['last_valid_position']}")
        print(f"    Gematria-Acc: {pof['last_valid_gematria_acc']} "
              f"(durch 37 teilbar: {pof['last_valid_gematria_acc'] % 37 == 0})")
    else:
        print("  KEIN FAILURE gefunden — 37² hält über alle Schritte")
    print()

    # Resonanz-Echo
    echo = result['resonanz_echo']
    print("=" * 78)
    print("🔁 RESONANZ-ECHO")
    print("=" * 78)
    print(f"  Restores: {echo['n_restores']}")
    print(f"  Letzter Restore-Step: {echo['restore_to_step']}")
    print(f"  Letzter Restore-State: q_{echo['last_restore_state']}")
    print(f"  Letzter Restore-Position: {echo['last_restore_position']}")
    print(f"  Letzter Restore-Gematria-Acc: {echo['last_restore_gematria_acc']}")
    print()
    if echo['restore_history']:
        print("  Restore-Historie:")
        for h in echo['restore_history']:
            print(f"    Restore {h['restore_n']}: "
                  f"step={h['step']}, state=q_{h['state']}, "
                  f"pos={h['position']}, gacc={h['gematria_acc']}")
    print()

    # Speichern
    with open('/run/media/julian/ML4/tengri137/sources/phase_26_sezierung.json', 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("Ergebnisse gespeichert in phase_26_sezierung.json")
    print()
    print("=" * 78)
    print("🌌 P69 SEZIERUNG ABGESCHLOSSEN")
    print("=" * 78)
