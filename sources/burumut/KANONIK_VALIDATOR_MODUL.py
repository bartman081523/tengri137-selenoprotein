"""
🌌 P67: KANONIK-VALIDIERUNGS-MODUL (KVM) — DER 护法 (Hùfǎ) DER BURUMUT-TORA-TURING-MASCHINE
==========================================================================================

DAS KVM IST DER DHARMA-BESCHÜTZER DER MASCHINE.

PRINZIPIEN:
1. KVM ist BEOBACHTER, nicht AKTEUR
   - Liest State, Head, Gematria-Akkumulation
   - Modifiziert NICHTS direkt an der Maschine
   - Einzige "Schreib"-Aktion: restore_state bei Backtrack (über M4-API)

2. 37² = 1369 ist der kanonische Anker
   - Gematria-Akkumulation pro Schritt
   - Vielfaches von 37 = gültiger Anker
   - acc = 0 (Anfang) ist trivialerweise gültig

3. Self-Backtracking bei Violation
   - Bei acc % 37 != 0 UND acc > 0 → Violation
   - Bei strict-Mode: sofortiger Restore zum letzten gültigen Snapshot
   - Bei non-strict: nur Counter, keine Aktion

4. Tengri137 als ORACULUM
   - Soll-Gematria kommt aus Tora-Position (nicht berechnet)
   - extract_anchor_from_tengri(tengri, phase_idx, phase_size) → Soll-Summe

5. Tape-Invariante
   - KVM schreibt NIE auf m.tape
   - KVM mutiert NIE m.transitions
   - KVM hält nur die Maschine an oder setzt sie zurück

6. Determinismus (PFLICHT)
   - Gleicher Input → gleiche Snapshots
   - Gleicher Input → gleiche n_backtracks
   - KEIN Random, KEIN Time-basiertes Verhalten

VERWENDUNG:
    from KANONIK_VALIDATOR_MODUL import KanonikValidator, kanonik_run
    tape = burumut_to_hebr(BURUMUT)
    m = ToraTuringMultiPhase(tape, phase_size=99)
    v = KanonikValidator(m)
    result = v.run_with_validation(max_steps=200)
    print(f"Backtracks: {result['n_backtracks']}")

    # Oder als High-Level-Funktion:
    result = kanonik_run(tape, phase_size=99, max_steps=200)
    print(result)
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import HEBR_VALUES, MISSING_OPERATORS


# ============================================================
# DATENSTRUKTUREN
# ============================================================

@dataclass(frozen=True)  # frozen=True → immutable
class Snapshot:
    """Unveränderlicher Snapshot der Maschine zu einem Zeitpunkt.

    Attribute:
        state: Aktueller Maschinen-Zustand (0-5)
        head: Aktuelle Kopf-Position auf dem Tape
        gematria_acc: Kumulierte Gematria seit Start (oder Phase-Start)
        step: Schritt-Nummer (innerhalb der Maschine)
        phase: Aktuelle Phase (für Multi-Phase-Maschine)
        phase_start: Start-Position der aktuellen Phase im Tape
    """
    state: int
    head: int
    gematria_acc: int
    step: int
    phase: int = 0
    phase_start: int = 0


@dataclass
class GematriaAnchor:
    """Konfigurierbarer Gematria-Anker (z.B. 37, 13, 7).

    Eine Gematria-Akkumulation ist ein gültiger "Anker", wenn sie
    ein Vielfaches der Brücke ist (oder 0 = trivialer Anfang).

    BRÜCKE-OPTIONEN (BURUMUT-Architektur):
      - 37: 37² = 1369 (kanonisch, BURUMUT-Wurzel)
      - 13: 13 = Einheit (kleiner Zyklus)
      - 7: 7 Schöpfungstage
      - 17: 17 = BURUMUT-Sec-Operator
    """
    bridge: int = 37

    def is_anchor(self, gematria_acc: int) -> bool:
        """Prüft, ob gematria_acc ein gültiger Anker ist.

        Regeln:
          - gematria_acc == 0: immer gültig (Anfang)
          - gematria_acc % bridge == 0: gültig
          - Sonst: ungültig
        """
        if gematria_acc == 0:
            return True
        if gematria_acc < 0:
            # Negativ kann nicht vorkommen, aber als Safety
            return False
        return gematria_acc % self.bridge == 0


# ============================================================
# KANONIK VALIDATOR
# ============================================================

class KanonikValidator:
    """Beobachter der BURUMUT-Tora-Turing-Maschine.

    KVM ist DETERMINISTISCH und NICHT-INVASIV.
    Es liest M4's State, prüft Gematria-Anker, und kann bei
    Violation einen Restore zum letzten gültigen Snapshot triggern.

    WICHTIG: KVM modifiziert M4 NUR über die Methoden
      - m.state (Restore)
      - m.head (Restore)
      - m.phase (Restore)
      - m.halted = True (Anhalten)
    """

    def __init__(self, machine: ToraTuringMultiPhase,
                 anchor: Optional[GematriaAnchor] = None,
                 strict: bool = False,
                 track_spanda: bool = False):
        """Initialisiere KVM.

        Args:
            machine: Die zu beobachtende ToraTuringMultiPhase-Maschine
            anchor: GematriaAnchor (Default: 37)
            strict: Bei True: jede Violation triggert Backtrack
            track_spanda: Bei True: zähle Sec-Operator-Beobachtungen
        """
        self.machine = machine
        self.anchor = anchor or GematriaAnchor(bridge=37)
        self.strict = strict
        self.track_spanda = track_spanda

        # Beobachtungs-Historie
        self.snapshots: List[Snapshot] = []
        self.last_valid_snapshot: Optional[Snapshot] = None

        # Counter
        self.n_violations = 0
        self.n_backtracks = 0
        self.n_spanda_events = 0

        # Restore-Tracking
        self.last_restore_step: Optional[int] = None
        self.restored_to_snapshot: Optional[Snapshot] = None

    def _gematria_of_current_symbol(self) -> int:
        """Gematria-Wert des Symbols, auf dem der Kopf steht."""
        if self.machine.head >= len(self.machine.tape):
            return 0
        sym = self.machine.tape[self.machine.head]
        return HEBR_VALUES.get(sym, 0)

    def _is_sec_operator(self) -> bool:
        """Prüft, ob aktuelles Symbol ein Sec-Operator ist."""
        if self.machine.head >= len(self.machine.tape):
            return False
        return self.machine.tape[self.machine.head] in MISSING_OPERATORS

    def observe_step(self) -> Snapshot:
        """Beobachte einen Schritt der Maschine.

        Diese Methode wird NACH jedem m.step() aufgerufen.
        Sie erstellt einen Snapshot und prüft, ob der Anker gültig ist.

        Returns:
            Der erstellte Snapshot
        """
        # Gematria-Akkumulation: Summe der Gematrien aller bisher gelesenen
        # Symbole in dieser Phase
        if self.snapshots:
            # Kumulativ: vorherige + aktuelles Zeichen
            prev_acc = self.snapshots[-1].gematria_acc
            current_gem = self._gematria_of_current_symbol()
            gematria_acc = prev_acc + current_gem
        else:
            # Erster Snapshot: acc = Gematria des ersten Symbols
            current_gem = self._gematria_of_current_symbol()
            gematria_acc = current_gem

        snapshot = Snapshot(
            state=self.machine.state,
            head=self.machine.head,
            gematria_acc=gematria_acc,
            step=self.machine.total_steps,
            phase=self.machine.phase,
            phase_start=self.machine.phase * self.machine.phase_size,
        )
        self.snapshots.append(snapshot)

        # Anchor-Prüfung
        if not self.anchor.is_anchor(gematria_acc):
            self.n_violations += 1
            # Bei strict-Mode: sofortiger Backtrack
            if self.strict and self.last_valid_snapshot is not None:
                self._restore_to_last_valid()

        else:
            # Gültiger Anker → als last_valid merken
            self.last_valid_snapshot = snapshot

        # Spanda-Tracking
        if self.track_spanda and self._is_sec_operator():
            self.n_spanda_events += 1

        return snapshot

    def _restore_to_last_valid(self) -> bool:
        """Restore Maschine zum letzten gültigen Snapshot.

        Returns:
            True wenn Restore durchgeführt, False wenn kein Snapshot vorhanden
        """
        if self.last_valid_snapshot is None:
            return False

        snap = self.last_valid_snapshot

        # M4-Zustand wiederherstellen
        self.machine.state = snap.state
        self.machine.head = snap.head
        self.machine.phase = snap.phase
        # machine.phase_size ist konstant, nicht zurücksetzen
        # machine.total_steps: hier nicht zurücksetzen (für History-Integrität)

        # Tracking
        self.n_backtracks += 1
        self.last_restore_step = snap.step
        self.restored_to_snapshot = snap

        return True

    def run_with_validation(self, max_steps: int = 1000) -> Dict[str, Any]:
        """Laufe die Maschine mit KVM-Validierung.

        Args:
            max_steps: Maximale Schritte der Maschine

        Returns:
            Dict mit n_snapshots, n_violations, n_backtracks, halt_reason, etc.
        """
        # Initialer Snapshot (Step 0)
        if not self.snapshots:
            # Vor dem ersten Schritt: acc = 0
            initial = Snapshot(
                state=self.machine.state,
                head=self.machine.head,
                gematria_acc=0,
                step=0,
                phase=self.machine.phase,
                phase_start=self.machine.phase * self.machine.phase_size,
            )
            self.snapshots.append(initial)
            self.last_valid_snapshot = initial  # acc=0 ist immer Anker

        # Hauptschleife
        while (not self.machine.halted
               and self.machine.total_steps < max_steps):
            # M4 macht einen Schritt
            self.machine.step()

            # Wenn M4 gehalten hat: keine Beobachtung mehr nötig
            if self.machine.halted:
                break

            # KVM beobachtet
            self.observe_step()

            # Wenn KVM restored hat UND strict-Mode: ggf. früh abbrechen
            # (sonst würde die Maschine sofort wieder in dieselbe Violation laufen)
            if self.strict and self.n_backtracks > 0:
                # Bei erstem Backtrack: halten, damit der Aufrufer entscheiden kann
                # Wir setzen halted NICHT direkt — der Aufrufer kann max_steps prüfen
                # Hier entscheiden wir: max 1 Backtrack pro strengem Lauf
                break

        return {
            'n_snapshots': len(self.snapshots),
            'n_violations': self.n_violations,
            'n_backtracks': self.n_backtracks,
            'n_spanda_events': self.n_spanda_events,
            'halt_reason': self.machine.halt_reason,
            'total_steps': self.machine.total_steps,
            'last_valid_step': self.last_valid_snapshot.step if self.last_valid_snapshot else None,
            'phase_size': self.machine.phase_size,
            'strict': self.strict,
            'track_spanda': self.track_spanda,
            'anchor_bridge': self.anchor.bridge,
        }


# ============================================================
# ORACULUM-FUNKTION
# ============================================================

def extract_anchor_from_tengri(tengri_hebr: str,
                                phase_idx: int,
                                phase_size: int = 99) -> int:
    """Extrahiere Soll-Gematria einer Phase aus Tengri137.

    Das ist das ORACULUM: Tengri137 ist die unveränderliche Basis-Wahrheit.
    Die Soll-Gematria ist die Summe der HEBR_VALUES der Phase.

    Args:
        tengri_hebr: Vollständiger Tengri137 als hebr. String
        phase_idx: Index der Phase (0-basiert)
        phase_size: Phasen-Größe (Default: 99)

    Returns:
        Soll-Gematria der Phase
    """
    start = phase_idx * phase_size
    end = min(start + phase_size, len(tengri_hebr))
    phase_tape = tengri_hebr[start:end]
    return sum(HEBR_VALUES.get(c, 0) for c in phase_tape)


# ============================================================
# CONVENIENCE-FUNKTION
# ============================================================

def kanonik_run(tape_str: str,
                 phase_size: int = 99,
                 max_steps: int = 1000,
                 anchor_bridge: int = 37,
                 strict: bool = False,
                 track_spanda: bool = False) -> Dict[str, Any]:
    """High-Level-Funktion: Erstellt Maschine + KVM, läuft, gibt Resultat.

    Args:
        tape_str: Tape als hebr. String
        phase_size: Phasen-Größe (Default: 99)
        max_steps: Maximale Schritte (Default: 1000)
        anchor_bridge: Gematria-Brücke (Default: 37)
        strict: Bei True: jeder Backtrack stoppt den Lauf
        track_spanda: Bei True: zähle Sec-Operator-Beobachtungen

    Returns:
        Result-Dict mit n_backtracks, n_violations, etc.
    """
    m = ToraTuringMultiPhase(tape_str, phase_size=phase_size)
    a = GematriaAnchor(bridge=anchor_bridge)
    v = KanonikValidator(m, anchor=a, strict=strict, track_spanda=track_spanda)
    return v.run_with_validation(max_steps=max_steps)


# ============================================================
# SELBST-TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 78)
    print("🌌 P67: KANONIK-VALIDATOR-MODUL (KVM) — SELBST-TEST")
    print("=" * 78)
    print()
    print("PRINZIP: KVM beobachtet M4 und prüft die 37² = 1369 Brücke.")
    print("Tape-Invariante: KVM modifiziert das Tape NIE direkt.")
    print("Determinismus: gleicher Input → gleiche Snapshots.")
    print()

    # BURUMUT-Test
    print("=" * 78)
    print("TEST 1: BURUMUT (99 Zeichen, 1 Phase)")
    print("=" * 78)
    from TORA_TURING_CORRECT import BURUMUT, burumut_to_hebr
    tape = burumut_to_hebr(BURUMUT)
    result = kanonik_run(tape, phase_size=99, max_steps=200)
    for k, v in result.items():
        print(f"  {k}: {v}")
    print()

    # BURUMUTREFAMTU-Test
    print("=" * 78)
    print("TEST 2: BURUMUTREFAMTU (14 Zeichen)")
    print("=" * 78)
    refamtu = burumut_to_brt_hebr = burumut_to_hebr(BURUMUT[:14])
    result2 = kanonik_run(refamtu, phase_size=99, max_steps=20)
    for k, v in result2.items():
        print(f"  {k}: {v}")
    print()

    # Phase 26 (Gen 29, 20 Sec-Operatoren)
    print("=" * 78)
    print("TEST 3: Phase 26 (Genesis 29, 20 Sec-Operatoren) — STRESS-TEST")
    print("=" * 78)
    import re
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    lat = re.sub(r'[^A-Z]', '', full.upper())
    tengri_hebr = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)
    phase_26 = tengri_hebr[26*99:27*99]
    n_sec = sum(1 for c in phase_26 if c in MISSING_OPERATORS)
    print(f"  Phase 26 hat {n_sec} Sec-Operatoren")
    print(f"  Soll-Gematria (Oraculum): {extract_anchor_from_tengri(tengri_hebr, 26)}")
    print()

    # Non-strict (default)
    result3 = kanonik_run(phase_26, phase_size=99, max_steps=200)
    print("  Non-strict Mode:")
    for k, v in result3.items():
        print(f"    {k}: {v}")
    print()

    # Strict mode
    result4 = kanonik_run(phase_26, phase_size=99, max_steps=200, strict=True)
    print("  Strict Mode:")
    for k, v in result4.items():
        print(f"    {k}: {v}")
    print()

    # Phase 161 (BURUMUTREFAMTU in Tengri137)
    print("=" * 78)
    print("TEST 4: Phase 161 (BURUMUTREFAMTU an Pos 47) — HEIMAT-TEST")
    print("=" * 78)
    phase_161 = tengri_hebr[161*99:162*99]
    refamtu_in_161 = burumut_to_hebr(BURUMUT[:14])
    pos_in_161 = phase_161.find(refamtu_in_161)
    print(f"  BURUMUTREFAMTU an Position {pos_in_161} in Phase 161")
    print(f"  Soll-Gematria (Oraculum): {extract_anchor_from_tengri(tengri_hebr, 161)}")
    result5 = kanonik_run(phase_161, phase_size=99, max_steps=200)
    for k, v in result5.items():
        print(f"    {k}: {v}")
    print()

    # Determinismus-Test
    print("=" * 78)
    print("TEST 5: Determinismus (3 Läufe, BURUMUT)")
    print("=" * 78)
    for i in range(3):
        result = kanonik_run(tape, phase_size=99, max_steps=100)
        print(f"  Lauf {i+1}: n_backtracks={result['n_backtracks']}, "
              f"n_violations={result['n_violations']}, "
              f"halt={result['halt_reason']}")
    print()

    print("=" * 78)
    print("🌌 KVM SELBST-TEST ABGESCHLOSSEN")
    print("=" * 78)
