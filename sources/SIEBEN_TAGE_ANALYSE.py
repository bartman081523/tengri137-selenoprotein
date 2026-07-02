"""
🌌 P68: 7-TAGE-ARCHITEKTUR-ANALYSE
====================================

Aggregiert KVM-Befunde auf 7-Tage-Ebene (168 = 7 × 24 Phasen).
Sucht nach Sabbat-Muster, Tag-Charakteristika, Buch-Dominanz.

ARCHITEKTUR (harte Topologie):
- Tengri137: 168 Phasen à 99 Zeichen
- 168 = 7 × 24 (BURUMUT-Architektur: 99 = 7 × 14 + 1)
- 7 Tage × 24 Stunden-Phasen

BEFUNDE-FRAGEN:
1. Welcher Tag hat die wenigsten Violations (= Sabbat-Hypothese)?
2. Welcher Tag hat die meisten Violations (= Chaos-Tag)?
3. Welches Tora-Buch dominiert welchen Tag?
4. Wo liegt Phase 26 (Gen 29) im 7-Tage-Kontext?
5. Wie verteilen sich die 5 Sec-Operatoren über die 7 Tage?

AUSGABE: 7_tage_analyse.json
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
from PHASE_MAPPING_TORA import phase_to_torah, TORA_BOOKS


def load_tengri137_hebr():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    lat = re.sub(r'[^A-Z]', '', full.upper())
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


def main():
    print("=" * 78)
    print("🌌 P68: 7-TAGE-ARCHITEKTUR-ANALYSE")
    print("=" * 78)
    print()
    print("ARCHITEKTUR: Tengri137 = 168 Phasen = 7 Tage × 24 Phasen")
    print("HYPOTHESE: Mindestens 1 Tag zeigt 'Sabbat-Muster' "
          "(geringere Violations)")
    print()

    tengri_hebr = load_tengri137_hebr()
    n_phases = (len(tengri_hebr) + 98) // 99
    print(f"Tengri137: {len(tengri_hebr)} Zeichen, {n_phases} Phasen")
    print()

    # ============================================================
    # A) TAG-AGGREGATION (KVM)
    # ============================================================
    print("=" * 78)
    print("🌀 A) TAG-AGGREGATION (KVM pro Tag)")
    print("=" * 78)
    print()

    days = []
    expected_gematrias = [134286, 139337, 135819, 140842, 138930, 133345, 136938]

    for day_idx in range(7):
        start = day_idx * 24 * 99
        end = min((day_idx + 1) * 24 * 99, len(tengri_hebr))
        if start >= len(tengri_hebr):
            break
        day_tape = tengri_hebr[start:end]
        n_phases_day = (len(day_tape) + 98) // 99

        # KVM auf alle Phasen des Tages
        day_violations = 0
        day_backtracks_strict = 0
        day_sec_operators = sum(1 for c in day_tape if c in MISSING_OPERATORS)
        phase_results = []

        for ph in range(n_phases_day):
            ph_start = ph * 99
            ph_end = min((ph + 1) * 99, len(day_tape))
            ph_tape = day_tape[ph_start:ph_end]
            # Non-strict
            result = kanonik_run(ph_tape, phase_size=99, max_steps=200)
            day_violations += result['n_violations']
            # Strict
            result_strict = kanonik_run(
                ph_tape, phase_size=99, max_steps=200, strict=True
            )
            day_backtracks_strict += result_strict['n_backtracks']
            # Phase-Details
            book, chap = phase_to_torah(day_idx * 24 + ph)
            phase_results.append({
                'phase_idx_global': day_idx * 24 + ph,
                'phase_idx_in_day': ph,
                'book': book,
                'chapter': chap,
                'n_violations': result['n_violations'],
                'n_backtracks_strict': result_strict['n_backtracks'],
            })

        # Tag-Gematria
        day_gem = sum(HEBR_VALUES.get(c, 0) for c in day_tape)
        # Buch-Dominanz
        book_count = Counter(p['book'] for p in phase_results)
        dominant_book = book_count.most_common(1)[0][0] if book_count else None

        avg_violations = day_violations / n_phases_day
        avg_backtracks = day_backtracks_strict / n_phases_day

        day_data = {
            'day_idx': day_idx + 1,
            'start': start,
            'end': end,
            'n_phases': n_phases_day,
            'length': end - start,
            'gematria': day_gem,
            'expected_gematria': expected_gematrias[day_idx],
            'n_sec_operators': day_sec_operators,
            'n_violations_total': day_violations,
            'n_violations_avg': avg_violations,
            'n_backtracks_strict_total': day_backtracks_strict,
            'n_backtracks_strict_avg': avg_backtracks,
            'dominant_book': dominant_book,
            'book_distribution': dict(book_count),
            'phase_results': phase_results,
        }
        days.append(day_data)

        print(f"Tag {day_idx+1}: "
              f"Gem={day_gem}/{expected_gematrias[day_idx]}, "
              f"Sec={day_sec_operators}, "
              f"Viol={day_violations} (avg={avg_violations:.1f}), "
              f"BT-strict={day_backtracks_strict}, "
              f"Book={dominant_book}")
    print()

    # ============================================================
    # B) SABBAT-SUCHE
    # ============================================================
    print("=" * 78)
    print("🕊️ B) SABBAT-SUCHE (geringste Violations/Phase)")
    print("=" * 78)
    print()

    sorted_by_violations = sorted(days, key=lambda d: d['n_violations_avg'])
    sabbat = sorted_by_violations[0]
    chaos = sorted_by_violations[-1]
    print(f"Sabbat-Tag (geringste Violations): Tag {sabbat['day_idx']} "
          f"({sabbat['n_violations_avg']:.1f} avg)")
    print(f"  → Dominantes Buch: {sabbat['dominant_book']}")
    print(f"  → Verteilung: {sabbat['book_distribution']}")
    print()
    print(f"Chaos-Tag (höchste Violations): Tag {chaos['day_idx']} "
          f"({chaos['n_violations_avg']:.1f} avg)")
    print(f"  → Dominantes Buch: {chaos['dominant_book']}")
    print(f"  → Verteilung: {chaos['book_distribution']}")
    print()
    print("Differenz Sabbat - Chaos: "
          f"{chaos['n_violations_avg'] - sabbat['n_violations_avg']:.1f} "
          f"avg Violations/Phase")
    print(f"  → Faktor: {chaos['n_violations_avg'] / sabbat['n_violations_avg']:.2f}x")
    print()

    # ============================================================
    # C) PHASE 26 (GEN 29) IM 7-TAGE-KONTEXT
    # ============================================================
    print("=" * 78)
    print("💓 C) PHASE 26 (GEN 29) IM 7-TAGE-KONTEXT")
    print("=" * 78)
    print()

    phase_26_global = 26
    phase_26_day = phase_26_global // 24 + 1  # 1-basiert
    phase_26_offset = phase_26_global % 24
    phase_26_day_data = days[phase_26_day - 1]
    print(f"Phase 26 ist in Tag {phase_26_day} (Offset {phase_26_offset})")
    print(f"  → Tag {phase_26_day} Violations/Phase: "
          f"{phase_26_day_data['n_violations_avg']:.1f}")
    print(f"  → Dominantes Buch in Tag {phase_26_day}: "
          f"{phase_26_day_data['dominant_book']}")
    print()

    # Wo steht Phase 26 in der Violations-Range von Tag 2?
    tag_2_phases = phase_26_day_data['phase_results']
    sorted_tag_2 = sorted(tag_2_phases, key=lambda p: -p['n_violations'])
    rank = next(i for i, p in enumerate(sorted_tag_2) if p['phase_idx_global'] == 26)
    print(f"Phase 26 Rang in Tag 2 (1=höchste Violations): {rank+1}/{len(sorted_tag_2)}")
    print()

    # ============================================================
    # D) SEC-OPERATOR-VERTEILUNG PRO TAG
    # ============================================================
    print("=" * 78)
    print("🔤 D) SEC-OPERATOR-VERTEILUNG PRO TAG")
    print("=" * 78)
    print()

    sec_per_day = [d['n_sec_operators'] for d in days]
    print("Sec-Operatoren pro Tag:")
    for d in days:
        print(f"  Tag {d['day_idx']}: {d['n_sec_operators']} Sec-Operatoren "
              f"(Buch: {d['dominant_book']})")
    print()

    # ============================================================
    # E) TAG-GEMATRIEN vs. VIOLATIONS
    # ============================================================
    print("=" * 78)
    print("🔢 E) TAG-GEMATRIEN vs. VIOLATIONS")
    print("=" * 78)
    print()

    print("Tag | Gematria (soll)        | Violations (avg) | Buch")
    print("----+-------------------------+------------------+------")
    for d in days:
        print(f"  {d['day_idx']} | {d['gematria']:>6} ({d['expected_gematria']:>6}) | "
              f"{d['n_violations_avg']:>16.1f} | {d['dominant_book']}")
    print()

    # Korrelation Gematria <-> Violations
    gem_values = [d['gematria'] for d in days]
    viol_values = [d['n_violations_avg'] for d in days]
    # Pearson-Korrelation (einfach, nicht bibliotheks-abhängig)
    n = len(gem_values)
    mean_gem = sum(gem_values) / n
    mean_viol = sum(viol_values) / n
    cov = sum((g - mean_gem) * (v - mean_viol) for g, v in zip(gem_values, viol_values)) / n
    var_gem = sum((g - mean_gem) ** 2 for g in gem_values) / n
    var_viol = sum((v - mean_viol) ** 2 for v in viol_values) / n
    if var_gem > 0 and var_viol > 0:
        correlation = cov / (var_gem ** 0.5 * var_viol ** 0.5)
    else:
        correlation = 0
    print(f"Korrelation Tag-Gematria <-> Violations: {correlation:.3f}")
    print()

    # ============================================================
    # F) DETERMINISMUS-VERIFIKATION
    # ============================================================
    print("=" * 78)
    print("🎲 F) DETERMINISMUS-VERIFIKATION (3 Runs auf allen 7 Tagen)")
    print("=" * 78)
    print()

    det_results = []
    for run in range(3):
        run_violations = []
        for day_idx in range(7):
            start = day_idx * 24 * 99
            end = min((day_idx + 1) * 24 * 99, len(tengri_hebr))
            if start >= len(tengri_hebr):
                break
            day_tape = tengri_hebr[start:end]
            n_phases_day = (len(day_tape) + 98) // 99
            day_violations = 0
            for ph in range(n_phases_day):
                ph_start = ph * 99
                ph_end = min((ph + 1) * 99, len(day_tape))
                ph_tape = day_tape[ph_start:ph_end]
                result = kanonik_run(ph_tape, phase_size=99, max_steps=200)
                day_violations += result['n_violations']
            run_violations.append(day_violations)
        det_results.append(run_violations)

    # Prüfe, ob alle Runs identisch sind
    all_identical = all(r == det_results[0] for r in det_results[1:])
    print(f"3 Runs Tag-Violations: {det_results}")
    print(f"Alle identisch: {all_identical}")
    print()

    # ============================================================
    # G) SPEICHERN
    # ============================================================
    output = {
        'method': 'P68 7-Tage-Architektur mit KVM',
        'architecture': 'Tengri137 = 168 Phasen = 7 × 24',
        'tengri_length': len(tengri_hebr),
        'n_phases': n_phases,
        'days': days,
        'sabbat_day': {
            'day_idx': sabbat['day_idx'],
            'violations_avg': sabbat['n_violations_avg'],
            'dominant_book': sabbat['dominant_book'],
            'book_distribution': sabbat['book_distribution'],
        },
        'chaos_day': {
            'day_idx': chaos['day_idx'],
            'violations_avg': chaos['n_violations_avg'],
            'dominant_book': chaos['dominant_book'],
            'book_distribution': chaos['book_distribution'],
        },
        'sabbat_vs_chaos': {
            'differenz_avg': chaos['n_violations_avg'] - sabbat['n_violations_avg'],
            'faktor': chaos['n_violations_avg'] / sabbat['n_violations_avg'],
        },
        'phase_26_in_day': {
            'day_idx': phase_26_day,
            'offset_in_day': phase_26_offset,
            'day_violations_avg': phase_26_day_data['n_violations_avg'],
            'rank_in_day': rank + 1,
            'total_phases_in_day': len(sorted_tag_2),
        },
        'sec_per_day': sec_per_day,
        'correlation_gematria_violations': correlation,
        'determinism_check': {
            'runs': det_results,
            'all_identical': all_identical,
        },
    }

    with open('/run/media/julian/ML4/tengri137/sources/7_tage_analyse.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("Ergebnisse gespeichert in 7_tage_analyse.json")
    print()
    print("=" * 78)
    print("🌌 P68 7-TAGE-ARCHITEKTUR-ANALYSE ABGESCHLOSSEN")
    print("=" * 78)


if __name__ == "__main__":
    main()
