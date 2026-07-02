"""
🌌 P67: KVM-ANALYSE AUF TENGRI137 + BURUMUT
=============================================

Wendet das Kanonik-Validierungs-Modul (KVM) auf alle 168 Phasen
von Tengri137 an, plus BURUMUT, BURUMUTREFAMTU, Phase 26 und 161.

Dokumentiert die echten Befunde — NICHT spekulativ, sondern
empirisch reproduzierbar (deterministisch).
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import json
import re
from collections import Counter
from KANONIK_VALIDATOR_MODUL import (
    KanonikValidator, GematriaAnchor, kanonik_run, extract_anchor_from_tengri
)
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import (
    BURUMUT, burumut_to_hebr, HEBR_VALUES, MISSING_OPERATORS
)
from PHASE_MAPPING_TORA import phase_to_torah


def load_tengri137_hebr():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    lat = re.sub(r'[^A-Z]', '', full.upper())
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


def main():
    print("=" * 78)
    print("🌌 P67: KVM-ANALYSE AUF TENGRI137 + BURUMUT")
    print("=" * 78)
    print()
    print("BEFUNDE-ERWARTUNG:")
    print("  - KVM ist Beobachter, modifiziert NICHTS")
    print("  - 37² = 1369 ist die kanonische Brücke")
    print("  - BURUMUT-99 sollte 0 Backtracks haben (Heimat)")
    print("  - Phase 26 (Gen 29) ist der Stress-Test (20 Sec-Operatoren)")
    print("  - Phase 161 (BURUMUTREFAMTU) ist 'Heimat' in Tengri137")
    print()

    tengri_hebr = load_tengri137_hebr()
    n_phases = (len(tengri_hebr) + 98) // 99

    # ============================================================
    # A) BURUMUT + BURUMUTREFAMTU (kanonisch)
    # ============================================================
    print("=" * 78)
    print("🌀 A) BURUMUT + BURUMUTREFAMTU (KANONISCH)")
    print("=" * 78)
    print()

    # BURUMUT-99
    result_burumut = kanonik_run(
        burumut_to_hebr(BURUMUT), phase_size=99, max_steps=200
    )
    print(f"BURUMUT-99:        "
          f"violations={result_burumut['n_violations']}, "
          f"backtracks={result_burumut['n_backtracks']}, "
          f"halt={result_burumut['halt_reason']}")
    print(f"  Soll-Gematria (BURUMUT-99): "
          f"{sum(HEBR_VALUES.get(c, 0) for c in burumut_to_hebr(BURUMUT))}")

    # BURUMUTREFAMTU (14 Zeichen)
    result_refamtu = kanonik_run(
        burumut_to_hebr(BURUMUT[:14]), phase_size=99, max_steps=20
    )
    print(f"BURUMUTREFAMTU:    "
          f"violations={result_refamtu['n_violations']}, "
          f"backtracks={result_refamtu['n_backtracks']}, "
          f"halt={result_refamtu['halt_reason']}")
    print(f"  Soll-Gematria (REFAMTU): "
          f"{sum(HEBR_VALUES.get(c, 0) for c in burumut_to_hebr(BURUMUT[:14]))}")
    print()

    # ============================================================
    # B) PHASE 26 (Genesis 29) — STRESS-TEST
    # ============================================================
    print("=" * 78)
    print("💓 B) PHASE 26 (Genesis 29, 20 Sec-Operatoren) — STRESS-TEST")
    print("=" * 78)
    print()

    phase_26 = tengri_hebr[26*99:27*99]
    n_sec_26 = sum(1 for c in phase_26 if c in MISSING_OPERATORS)
    soll_26 = extract_anchor_from_tengri(tengri_hebr, 26)
    print(f"Phase 26 hat {n_sec_26} Sec-Operatoren")
    print(f"Soll-Gematria (Oraculum): {soll_26}")
    print()

    # Non-strict
    result_26_lax = kanonik_run(phase_26, phase_size=99, max_steps=200)
    print(f"Phase 26 (non-strict):     "
          f"violations={result_26_lax['n_violations']}, "
          f"backtracks={result_26_lax['n_backtracks']}, "
          f"halt={result_26_lax['halt_reason']}")

    # Strict
    result_26_strict = kanonik_run(
        phase_26, phase_size=99, max_steps=200, strict=True
    )
    print(f"Phase 26 (strict):         "
          f"violations={result_26_strict['n_violations']}, "
          f"backtracks={result_26_strict['n_backtracks']}, "
          f"halt={result_26_strict['halt_reason']}")
    print()

    # ============================================================
    # C) PHASE 161 (BURUMUTREFAMTU in Tengri137)
    # ============================================================
    print("=" * 78)
    print("🏠 C) PHASE 161 (BURUMUTREFAMTU an Pos 47) — HEIMAT-TEST")
    print("=" * 78)
    print()

    phase_161 = tengri_hebr[161*99:162*99]
    refamtu_hebr = burumut_to_hebr(BURUMUT[:14])
    pos_in_161 = phase_161.find(refamtu_hebr)
    soll_161 = extract_anchor_from_tengri(tengri_hebr, 161)
    print(f"BURUMUTREFAMTU an Pos {pos_in_161} in Phase 161")
    print(f"Soll-Gematria (Oraculum): {soll_161}")
    result_161 = kanonik_run(phase_161, phase_size=99, max_steps=200)
    print(f"Phase 161:                 "
          f"violations={result_161['n_violations']}, "
          f"backtracks={result_161['n_backtracks']}, "
          f"halt={result_161['halt_reason']}")
    print()

    # ============================================================
    # D) VERGLEICH: 37² vs. andere Brücken
    # ============================================================
    print("=" * 78)
    print("🔢 D) BRÜCKEN-VERGLEICH: 37 vs. 13 vs. 7 vs. 17")
    print("=" * 78)
    print()

    for bridge in [37, 13, 7, 17, 1]:
        result = kanonik_run(
            burumut_to_hebr(BURUMUT), phase_size=99,
            max_steps=200, anchor_bridge=bridge
        )
        print(f"Brücke {bridge:>2}: BURUMUT-99 "
              f"violations={result['n_violations']}, "
              f"backtracks={result['n_backtracks']}")

    print()

    # ============================================================
    # E) ALLE 168 PHASEN — Violations-Verteilung
    # ============================================================
    print("=" * 78)
    print("📊 E) ALLE 168 PHASEN — KVM-VIOLATIONS-VERTEILUNG")
    print("=" * 78)
    print()

    phase_results = []
    for i in range(n_phases):
        start = i * 99
        end = min((i + 1) * 99, len(tengri_hebr))
        phase_tape = tengri_hebr[start:end]
        result = kanonik_run(phase_tape, phase_size=99, max_steps=200)
        book, chap = phase_to_torah(i)
        phase_results.append({
            'phase': i,
            'book': book,
            'chapter': chap,
            'n_snapshots': result['n_snapshots'],
            'n_violations': result['n_violations'],
            'n_backtracks': result['n_backtracks'],
            'halt_reason': result['halt_reason'],
            'soll_gematria': extract_anchor_from_tengri(tengri_hebr, i),
            'n_sec_operators': sum(1 for c in phase_tape if c in MISSING_OPERATORS),
        })

    # Top 10 Phasen mit den meisten Violations
    top_violations = sorted(phase_results, key=lambda x: -x['n_violations'])[:10]
    print("Top 10 Phasen mit den meisten 37²-Violations:")
    for p in top_violations:
        print(f"  Phase {p['phase']:>3} ({p['book'][:3]} {p['chapter']:>2}): "
              f"violations={p['n_violations']:>3}, "
              f"sec={p['n_sec_operators']:>2}, "
              f"gem={p['soll_gematria']:>5}")
    print()

    # Pro Buch
    violations_per_book = Counter()
    for p in phase_results:
        violations_per_book[p['book']] += p['n_violations']

    print("Total Violations pro Tora-Buch:")
    for book in ['Genesis', 'Exodus', 'Leviticus', 'Numeri', 'Deuteronomium']:
        total = violations_per_book.get(book, 0)
        n_phases_book = sum(1 for p in phase_results if p['book'] == book)
        avg = total / n_phases_book if n_phases_book > 0 else 0
        print(f"  {book:<18}: {total:>5} total, {avg:>6.1f} avg/Phase "
              f"({n_phases_book} Phasen)")
    print()

    # ============================================================
    # F) DETERMINISMUS-VERIFIKATION
    # ============================================================
    print("=" * 78)
    print("🎲 F) DETERMINISMUS-VERIFIKATION (5 Läufe, identisch?)")
    print("=" * 78)
    print()

    det_results = []
    for i in range(5):
        result = kanonik_run(
            burumut_to_hebr(BURUMUT), phase_size=99, max_steps=100
        )
        det_results.append((result['n_violations'], result['n_backtracks']))

    unique = set(det_results)
    print(f"5 Läufe BURUMUT-99: {det_results}")
    print(f"Unique Werte: {len(unique)}")
    assert len(unique) == 1, "NICHT deterministisch!"
    print("✓ DETERMINISTISCH")
    print()

    # ============================================================
    # SPEICHERN
    # ============================================================
    output = {
        'method': 'KVM (Kanonik-Validierungs-Modul) P67',
        'principle': 'Beobachter der M4, prüft 37² = 1369 Brücke, '
                     'Self-Backtracking bei Violation, Tape-Invariante',
        'burumut_99': result_burumut,
        'burumutrefamtu': result_refamtu,
        'phase_26_gen_29': {
            'n_sec_operators': n_sec_26,
            'soll_gematria_oraculum': soll_26,
            'non_strict': result_26_lax,
            'strict': result_26_strict,
        },
        'phase_161_refamtu': {
            'refamtu_position_in_phase': pos_in_161,
            'soll_gematria_oraculum': soll_161,
            'result': result_161,
        },
        'all_168_phases': phase_results,
        'top_10_violations': top_violations,
        'violations_per_book': dict(violations_per_book),
        'determinismus_5_runs': det_results,
        'is_deterministic': len(unique) == 1,
    }

    with open('/run/media/julian/ML4/tengri137/sources/kvm_analyse.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("Ergebnisse gespeichert in kvm_analyse.json")
    print()
    print("=" * 78)
    print("🌌 KVM-ANALYSE ABGESCHLOSSEN")
    print("=" * 78)


if __name__ == "__main__":
    main()
