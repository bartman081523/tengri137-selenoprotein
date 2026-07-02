"""
🌌 P70: TOPOLOGIE-PROFIL DES SCHEITERNS
========================================

Kartografiert die Failure-Step-Verteilung über alle 168 Phasen
von Tengri137. Bestimmt:

1. ABGRÜNDE: Phasen mit Failure-Step 1 (sofort verriegelt)
2. KORRIDORE: Phasen mit tiefem Eindringen (failure_step > 10)
3. HEIMAT: Phase 161 (BURUMUTREFAMTU) als Kontrast

ARCHITEKTUR:
- Pro Phase: M4 + KVM (beobachtend, strict=False)
- Bei erster Violation: dokumentiere exakten Zustand
- Statistik: Median, Mean, Verteilung, Top-5

METRIKEN:
- failure_step: Schritt-Nummer der ersten Violation
- failure_position: Position auf Tape
- failure_symbol: das auslösende Zeichen
- failure_state: q_0..q_5
- failure_gematria_acc: Gematria-Akkumulation am Failure-Punkt
- n_unique_states: Anzahl verschiedener Zustände vor Failure

DETERMINISMUS:
- Gleicher Input → gleiche Resultate
- 3/3 Läufe identisch verifiziert
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import re
import json
import statistics
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from KANONIK_VALIDATOR_MODUL import (
    KanonikValidator, GematriaAnchor, Snapshot
)
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import (
    BURUMUT, burumut_to_hebr, HEBR_VALUES, MISSING_OPERATORS,
    build_tora_transitions
)
from PHASE_MAPPING_TORA import phase_to_torah


def load_tengri137_hebr():
    """Lade Tengri137 als hebr. String."""
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    lat = re.sub(r'[^A-Z]', '', full.upper())
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


# ============================================================
# DATENSTRUKTUREN
# ============================================================

@dataclass
class FailureRecord:
    """Failure-Record für eine Phase.

    Attribute:
        phase_idx: Index der Phase (0-basiert)
        failure_step: Schritt-Nummer der ersten Violation
        failure_position: Position auf dem Tape (0-basiert)
        failure_symbol: das auslösende Zeichen (hebr.)
        failure_state: Maschinen-Zustand (0-5)
        failure_gematria_acc: Gematria-Akkumulation am Failure-Punkt
        n_unique_states: Anzahl verschiedener Zustände vor Failure
        max_gematria_acc: maximale Gematria-Akkumulation vor Failure
    """
    phase_idx: int
    failure_step: int
    failure_position: int
    failure_symbol: Optional[str]
    failure_state: int
    failure_gematria_acc: int
    n_unique_states: int
    max_gematria_acc: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            'phase_idx': self.phase_idx,
            'failure_step': self.failure_step,
            'failure_position': self.failure_position,
            'failure_symbol': self.failure_symbol,
            'failure_state': self.failure_state,
            'failure_gematria_acc': self.failure_gematria_acc,
            'n_unique_states': self.n_unique_states,
            'max_gematria_acc': self.max_gematria_acc,
        }


class TopologieProfil:
    """Sammlung von Failure-Records mit Statistik-Methoden."""

    def __init__(self):
        self.records: List[FailureRecord] = []

    @property
    def n_total(self) -> int:
        return len(self.records)

    def add(self, rec: FailureRecord):
        self.records.append(rec)

    def failure_step_distribution(self) -> Dict[int, int]:
        """Verteilung der Failure-Steps."""
        return dict(Counter(r.failure_step for r in self.records))

    def median_failure_step(self) -> float:
        """Median der Failure-Steps."""
        steps = [r.failure_step for r in self.records]
        return statistics.median(steps) if steps else 0

    def mean_failure_step(self) -> float:
        """Mean der Failure-Steps."""
        steps = [r.failure_step for r in self.records]
        return statistics.mean(steps) if steps else 0

    def mean_per_book(self) -> Dict[str, float]:
        """Mean Failure-Step pro Tora-Buch."""
        per_book = {}
        for r in self.records:
            book, _ = phase_to_torah(r.phase_idx)
            per_book.setdefault(book, []).append(r.failure_step)
        return {book: statistics.mean(steps) for book, steps in per_book.items()}

    def mean_per_day(self) -> List[Dict[str, Any]]:
        """Mean Failure-Step pro Tag (7 × 24)."""
        per_day = []
        for day_idx in range(7):
            day_records = [
                r for r in self.records
                if day_idx * 24 <= r.phase_idx < (day_idx + 1) * 24
            ]
            if day_records:
                steps = [r.failure_step for r in day_records]
                per_day.append({
                    'day_idx': day_idx + 1,
                    'n_phases': len(day_records),
                    'mean_failure_step': statistics.mean(steps),
                    'median_failure_step': statistics.median(steps),
                    'min_failure_step': min(steps),
                    'max_failure_step': max(steps),
                })
        return per_day

    def top_5_deepest(self) -> List[Dict[str, Any]]:
        """Top 5 Phasen mit höchstem failure_step (tiefstes Eindringen)."""
        sorted_recs = sorted(self.records, key=lambda r: -r.failure_step)[:5]
        return [r.to_dict() for r in sorted_recs]

    def top_5_shallowest(self) -> List[Dict[str, Any]]:
        """Top 5 Phasen mit niedrigstem failure_step (flachstes Eindringen)."""
        sorted_recs = sorted(self.records, key=lambda r: r.failure_step)[:5]
        return [r.to_dict() for r in sorted_recs]

    def abgruende(self, step_threshold: int = 1) -> List[Dict[str, Any]]:
        """Phasen mit failure_step <= step_threshold (Abgründe)."""
        abgrund_recs = [r for r in self.records if r.failure_step <= step_threshold]
        return [r.to_dict() for r in abgrund_recs]

    def korridore(self, step_threshold: int = 10) -> List[Dict[str, Any]]:
        """Phasen mit failure_step > step_threshold (Korridore)."""
        korridor_recs = [r for r in self.records if r.failure_step > step_threshold]
        return [r.to_dict() for r in korridor_recs]


# ============================================================
# KARTIERUNG
# ============================================================

def kartografiere_phase(tape: str, phase_idx: int) -> FailureRecord:
    """Kartografiere eine einzelne Phase.

    Erstellt M4 + KVM (beobachtend, strict=False) und findet den
    ersten Failure-Punkt (erste 37²-Violation).

    Args:
        tape: Phase als hebr. String
        phase_idx: Globaler Index der Phase

    Returns:
        FailureRecord mit allen Failure-Informationen
    """
    m = ToraTuringMultiPhase(
        tape, phase_size=99, transitions=build_tora_transitions()
    )
    anchor = GematriaAnchor(bridge=37)
    validator = KanonikValidator(m, anchor=anchor, strict=False)

    # Tracking
    failure_step = None
    failure_position = None
    failure_symbol = None
    failure_state = None
    failure_gematria_acc = None
    max_gematria_acc = 0
    states_visited = set()

    # Initialer Snapshot
    initial = Snapshot(
        state=m.state,
        head=m.head,
        gematria_acc=0,
        step=0,
        phase=m.phase,
        phase_start=m.phase * m.phase_size,
    )
    validator.snapshots.append(initial)
    states_visited.add(m.state)

    # Laufe bis Failure oder max_steps
    max_steps = 200
    while (not m.halted
           and m.total_steps < max_steps
           and failure_step is None):
        m.step()
        if m.halted:
            break
        states_visited.add(m.state)

        # Gematria-Akkumulation
        if validator.snapshots:
            prev_acc = validator.snapshots[-1].gematria_acc
        else:
            prev_acc = 0

        if m.head < len(m.tape):
            current_gem = HEBR_VALUES.get(m.tape[m.head], 0)
        else:
            current_gem = 0

        gematria_acc = prev_acc + current_gem
        max_gematria_acc = max(max_gematria_acc, gematria_acc)

        snap = Snapshot(
            state=m.state,
            head=m.head,
            gematria_acc=gematria_acc,
            step=m.total_steps,
            phase=m.phase,
            phase_start=m.phase * m.phase_size,
        )
        validator.snapshots.append(snap)

        # Anchor-Prüfung
        if not anchor.is_anchor(gematria_acc):
            failure_step = m.total_steps
            failure_position = m.head
            failure_symbol = m.tape[m.head] if m.head < len(m.tape) else None
            failure_state = m.state
            failure_gematria_acc = gematria_acc

    # Falls kein Failure gefunden wurde (sehr seltener Fall)
    if failure_step is None:
        # Default: 99 (ganzes Tape durchlaufen)
        failure_step = 99
        failure_position = min(98, len(tape) - 1)
        failure_symbol = tape[failure_position] if failure_position < len(tape) else None
        failure_state = m.state
        failure_gematria_acc = max_gematria_acc

    return FailureRecord(
        phase_idx=phase_idx,
        failure_step=failure_step,
        failure_position=failure_position,
        failure_symbol=failure_symbol,
        failure_state=failure_state,
        failure_gematria_acc=failure_gematria_acc,
        n_unique_states=len(states_visited),
        max_gematria_acc=max_gematria_acc,
    )


def kartografiere_phaenomen() -> Dict[str, Any]:
    """Kartografiere alle 168 Phasen von Tengri137.

    Returns:
        Vollständiges Dict mit allen Statistiken
    """
    tengri_hebr = load_tengri137_hebr()
    n_phases = (len(tengri_hebr) + 98) // 99

    profil = TopologieProfil()

    for i in range(n_phases):
        start = i * 99
        end = min((i + 1) * 99, len(tengri_hebr))
        phase_tape = tengri_hebr[start:end]
        rec = kartografiere_phase(phase_tape, i)
        profil.add(rec)

    # Statistiken
    result = {
        'n_phases': n_phases,
        'n_total': profil.n_total,
        'records': [r.to_dict() for r in profil.records],
        'median_failure_step': profil.median_failure_step(),
        'mean_failure_step': profil.mean_failure_step(),
        'failure_step_distribution': profil.failure_step_distribution(),
        'mean_per_book': profil.mean_per_book(),
        'mean_per_day': profil.mean_per_day(),
        'top_5_deepest': profil.top_5_deepest(),
        'top_5_shallowest': profil.top_5_shallowest(),
        'abgruende_step_1': profil.abgruende(step_threshold=1),
        'korridore_deep': profil.korridore(step_threshold=10),
    }

    return result


# ============================================================
# SELBST-TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 78)
    print("🌌 P70: TOPOLOGIE-PROFIL DES SCHEITERNS")
    print("=" * 78)
    print()
    print("KARTIOGRAFIERUNG aller 168 Phasen von Tengri137.")
    print("Bestimmt Failure-Step-Verteilung, Abgründe, Korridore, Heimat.")
    print()

    result = kartografiere_phaenomen()

    # ============================================================
    # ÜBERSICHT
    # ============================================================
    print("=" * 78)
    print("📊 ÜBERSICHT")
    print("=" * 78)
    print(f"  Total Phasen: {result['n_total']}")
    print(f"  Median Failure-Step: {result['median_failure_step']:.1f}")
    print(f"  Mean Failure-Step: {result['mean_failure_step']:.2f}")
    print()

    # ============================================================
    # ABGRÜNDE (Step 1)
    # ============================================================
    print("=" * 78)
    print("🕳️ ABGRÜNDE (Failure-Step == 1)")
    print("=" * 78)
    abgruende = result['abgruende_step_1']
    print(f"  Anzahl: {len(abgruende)} / {result['n_total']} "
          f"({100 * len(abgruende) / result['n_total']:.1f}%)")
    print()
    print("  Erste 10:")
    for r in abgruende[:10]:
        book, chap = phase_to_torah(r['phase_idx'])
        print(f"    Phase {r['phase_idx']:>3} ({book[:3]} {chap:>2}): "
              f"symbol={r['failure_symbol']}, "
              f"state=q_{r['failure_state']}, "
              f"acc={r['failure_gematria_acc']}")
    print()

    # ============================================================
    # KORRIDORE (Deep Fails)
    # ============================================================
    print("=" * 78)
    print("🚪 KORRIDORE (Failure-Step > 10)")
    print("=" * 78)
    korridore = result['korridore_deep']
    print(f"  Anzahl: {len(korridore)} / {result['n_total']} "
          f"({100 * len(korridore) / result['n_total']:.1f}%)")
    print()

    # ============================================================
    # TOP 5 TIEFSTE PHASEN
    # ============================================================
    print("=" * 78)
    print("🌊 TOP 5 TIEFSTE PHASEN (längstes Eindringen)")
    print("=" * 78)
    for r in result['top_5_deepest']:
        book, chap = phase_to_torah(r['phase_idx'])
        print(f"  Phase {r['phase_idx']:>3} ({book[:3]} {chap:>2}): "
              f"step={r['failure_step']}, "
              f"symbol={r['failure_symbol']}, "
              f"max_acc={r['max_gematria_acc']}, "
              f"states={r['n_unique_states']}")
    print()

    # ============================================================
    # TOP 5 FLACHSTE PHASEN (Abgrund-Könige)
    # ============================================================
    print("=" * 78)
    print("⛰️ TOP 5 FLACHSTE PHASEN (kürzestes Eindringen)")
    print("=" * 78)
    for r in result['top_5_shallowest']:
        book, chap = phase_to_torah(r['phase_idx'])
        print(f"  Phase {r['phase_idx']:>3} ({book[:3]} {chap:>2}): "
              f"step={r['failure_step']}, "
              f"symbol={r['failure_symbol']}, "
              f"acc={r['failure_gematria_acc']}")
    print()

    # ============================================================
    # PRO TORA-BUCH
    # ============================================================
    print("=" * 78)
    print("📚 PRO TORA-BUCH (Mean Failure-Step)")
    print("=" * 78)
    for book, mean in sorted(result['mean_per_book'].items(), key=lambda x: -x[1]):
        print(f"  {book:<18}: {mean:>6.2f}")
    print()

    # ============================================================
    # PRO TAG (7 × 24)
    # ============================================================
    print("=" * 78)
    print("📅 PRO TAG (Mean Failure-Step)")
    print("=" * 78)
    for d in result['mean_per_day']:
        print(f"  Tag {d['day_idx']}: mean={d['mean_failure_step']:.2f}, "
              f"median={d['median_failure_step']:.1f}, "
              f"range=[{d['min_failure_step']}, {d['max_failure_step']}]")
    print()

    # ============================================================
    # PHASE 26 vs PHASE 161 (Heimat-Kontrast)
    # ============================================================
    print("=" * 78)
    print("🏠 HEIMAT-KONTRAST: Phase 26 vs Phase 161")
    print("=" * 78)
    p26 = next(r for r in result['records'] if r['phase_idx'] == 26)
    p161 = next(r for r in result['records'] if r['phase_idx'] == 161)
    print(f"  Phase 26 (Gen 29):  failure_step={p26['failure_step']}, "
          f"max_acc={p26['max_gematria_acc']}, "
          f"states={p26['n_unique_states']}")
    print(f"  Phase 161 (Refamtu): failure_step={p161['failure_step']}, "
          f"max_acc={p161['max_gematria_acc']}, "
          f"states={p161['n_unique_states']}")
    print()
    differenz = p161['failure_step'] - p26['failure_step']
    print(f"  Differenz: {differenz:+d} Schritte")
    if differenz > 0:
        print(f"  → Phase 161 dringt {differenz} Schritte TIEFER ein als Phase 26")
    elif differenz < 0:
        print(f"  → Phase 161 verriegelt {-differenz} Schritte FRÜHER als Phase 26")
    else:
        print(f"  → Beide gleich (Heimat-Hypothese nicht bestätigt)")
    print()

    # ============================================================
    # VERTEILUNG DER FAILURE-STEPS
    # ============================================================
    print("=" * 78)
    print("📈 FAILURE-STEP-VERTEILUNG (Top 15 häufigste Werte)")
    print("=" * 78)
    sorted_dist = sorted(
        result['failure_step_distribution'].items(),
        key=lambda x: -x[1]
    )[:15]
    for step, count in sorted_dist:
        bar = '█' * min(50, count)
        print(f"  Step {step:>3}: {count:>3} {bar}")
    print()

    # Speichern
    with open('/run/media/julian/ML4/tengri137/sources/topologie_profil.json', 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("Ergebnisse gespeichert in topologie_profil.json")
    print()
    print("=" * 78)
    print("🌌 P70 TOPOLOGIE-PROFIL ABGESCHLOSSEN")
    print("=" * 78)
