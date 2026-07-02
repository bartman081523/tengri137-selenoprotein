"""
🌌 WAS STEHT AN: Tengri137 + Tora sagen uns, was als Nächstes kommt
=====================================================================

HYPOTHESE: Die jüngsten Befunde aus Tengri137 und der Tora-Lektüre
geben uns konkrete Hinweise auf die nächsten Schritte.

METHODE:
1. Lade Tengri137-Volltext und extrahiere Phasen
2. Lasse M4 über alle 168 Phasen laufen (P65d)
3. Identifiziere PENDEL-Phasen (wo M4 nicht selbstständig hält)
4. BURUMUTREFAMTU-Position 15986 ist der ANKER für Selbst-Lesung
5. Schöpfungs-Pulse (15 Schritte, 34 Schritte) zeigen Resonanz-Stellen

WAS STEHT AN:
A) Pendel-Phasen stabilisieren (Numeri: 25/32 pendelnd)
B) BURUMUTREFAMTU-Stelle voll dekodieren (Position 15986)
C) Die "7 Schöpfungstage" in Tengri137 finden (P60)
D) Spanda-Pulse als formale Operatoren (P62c)
E) BURUMUT-Sec-Buchstaben (כ, ג, ד, ת, י) im Volltext markieren
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import re
import json
from collections import Counter
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import (
    BURUMUT, burumut_to_hebr, build_tora_transitions, HEBR_VALUES,
    MISSING_OPERATORS, get_layer_name
)
from PHASE_MAPPING_TORA import TORA_BOOKS, phase_to_torah


def load_tengri137_hebr():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    lat = re.sub(r'[^A-Z]', '', full.upper())
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


def gematria(hebr_str):
    return sum(HEBR_VALUES.get(c, 0) for c in hebr_str)


def run_m4(tape, max_steps=200):
    m = ToraTuringMultiPhase(tape, phase_size=99,
                             transitions=build_tora_transitions())
    m.run(max_steps=max_steps)
    return {
        'total_steps': m.total_steps,
        'halt_state': m.halt_state,
        'halt_reason': m.halt_reason,
    }


def main():
    print("=" * 78)
    print("🌌 WAS STEHT AN: Tengri137 + Tora")
    print("=" * 78)
    print()
    print("HYPOTHESE: Die jüngsten Befunde geben Hinweise auf nächste Schritte.")
    print()

    tengri_hebr = load_tengri137_hebr()
    n_phases = (len(tengri_hebr) + 98) // 99
    print(f"Tengri137: {len(tengri_hebr)} Zeichen, {n_phases} Phasen")
    print()

    # ============================================================
    # A) PENDEL-PHASEN (Numeri: 25/32 pendelnd)
    # ============================================================
    print("=" * 78)
    print("🌀 A) PENDEL-PHASEN IDENTIFIZIEREN")
    print("=" * 78)
    print()
    print("Pendel-Phasen: M4 hält NICHT selbstständig (MAX_STEPS_EXCEEDED)")
    print("Numeri = Wüstenwanderung = am wenigsten stabil (21.9%)")
    print()

    pendel_phasen = []
    for i in range(n_phases):
        start = i * 99
        end = min((i + 1) * 99, len(tengri_hebr))
        tape = tengri_hebr[start:end]
        r = run_m4(tape)
        if r['halt_reason'] == 'MAX_STEPS_EXCEEDED':
            pendel_phasen.append({
                'phase': i,
                'halt_state': r['halt_state'],
                'tape_gematria': gematria(tape),
            })

    print(f"Total Pendel-Phasen: {len(pendel_phasen)} / {n_phases}")

    # Pro Buch
    pendel_per_book = Counter()
    for p in pendel_phasen:
        book, _ = phase_to_torah(p['phase'])
        pendel_per_book[book] += 1

    print()
    print("Pendel-Phasen pro Tora-Buch:")
    for book, info in TORA_BOOKS.items():
        n_book = info['phases_end'] - info['phases_start']
        n_pendel = pendel_per_book.get(book, 0)
        ratio = n_pendel / n_book if n_book > 0 else 0
        print(f"  {book:<18}: {n_pendel:>2} / {n_book:>2} ({ratio:>5.1%})")
    print()

    # Numeri Pendel-Phasen (höchste Priorität)
    numeri_pendel = [p for p in pendel_phasen
                     if phase_to_torah(p['phase'])[0] == 'Numeri']
    print(f"Numeri Pendel-Phasen: {len(numeri_pendel)}")
    if numeri_pendel:
        print("  Erste 10:")
        for p in numeri_pendel[:10]:
            print(f"    Phase {p['phase']}: halt_state={p['halt_state']}, "
                  f"gem={p['tape_gematria']}")
    print()

    # ============================================================
    # B) BURUMUTREFAMTU-POSITION 15986
    # ============================================================
    print("=" * 78)
    print("📍 B) BURUMUTREFAMTU-POSITION 15986 — VOLLE DEKODIERUNG")
    print("=" * 78)
    print()
    refamtu_hebr = burumut_to_hebr(BURUMUT[:14])
    idx = tengri_hebr.find(refamtu_hebr)
    print(f"BURUMUTREFAMTU an Position: {idx}")
    print(f"Phase-Index: {idx // 99} (Phase 161)")
    print(f"In-Phase-Offset: {idx % 99}")
    print()

    # Kontext: 50 Zeichen davor, BURUMUTREFAMTU, 50 Zeichen danach
    context_before = tengri_hebr[max(0, idx-50):idx]
    context_after = tengri_hebr[idx+14:idx+14+50]
    print(f"KONTEXT (50 davor):")
    print(f"  {context_before}")
    print()
    print(f"BURUMUTREFAMTU: {refamtu_hebr}")
    print()
    print(f"KONTEXT (50 danach):")
    print(f"  {context_after}")
    print()

    # Was steht in BURUMUTREFAMTU-Stelle?
    # M4 auf den BURUMUTREFAMTU-Teil alleine
    r = run_m4(refamtu_hebr)
    print(f"M4 auf BURUMUTREFAMTU allein: {r['total_steps']} Schritte")

    # M4 auf den Kontext (50+14+50 = 114 Zeichen)
    full_context = tengri_hebr[max(0, idx-50):idx+14+50]
    r2 = run_m4(full_context)
    print(f"M4 auf den vollen Kontext: {r2['total_steps']} Schritte, "
          f"halt={r2['halt_state']}, reason={r2['halt_reason']}")
    print()

    # ============================================================
    # C) 7 SCHÖPFUNGSTAGE IN TENGRI137 (P60)
    # ============================================================
    print("=" * 78)
    print("🌅 C) 7 SCHÖPFUNGSTAGE IN TENGRI137 FINDEN")
    print("=" * 78)
    print()
    print("BURUMUT ist 99 = 7 × 14 + 1")
    print("Tengri137 hat 168 Phasen à 99 Zeichen")
    print("168 / 7 = 24 Phasen pro 'Schöpfungstag'")
    print()

    # Suche nach 7 klar abgrenzbaren 'Tagen' in Tengri137
    days = []
    for day_idx in range(7):
        start = day_idx * 24 * 99
        end = min((day_idx + 1) * 24 * 99, len(tengri_hebr))
        if start >= len(tengri_hebr):
            break
        day_tape = tengri_hebr[start:end]
        day_gem = gematria(day_tape)
        n_sec = sum(1 for c in day_tape if c in MISSING_OPERATORS)
        days.append({
            'day': day_idx + 1,
            'start': start,
            'end': end,
            'length': end - start,
            'gematria': day_gem,
            'n_sec_chars': n_sec,
        })

    print("7 'Tengri137-Tage' (à 24 Phasen = 2376 Zeichen):")
    for d in days:
        print(f"  Tag {d['day']}: Position {d['start']}-{d['end']} "
              f"({d['length']} Zch), Gem={d['gematria']}, Sec={d['n_sec_chars']}")
    print()

    # ============================================================
    # D) SPANDA-PULSE (P62c)
    # ============================================================
    print("=" * 78)
    print("💓 D) SPANDA-PULSE IN TENGRI137 MARKIEREN")
    print("=" * 78)
    print()
    print("Spanda-Puls = M4 liest einen der 5 Sec-Buchstaben (כ, ג, ד, ת, י)")
    print("ODER BURUMUTREFAMTU als Substring")
    print()

    # Zähle Sec-Buchstaben pro Phase
    sec_per_phase = []
    for i in range(n_phases):
        start = i * 99
        end = min((i + 1) * 99, len(tengri_hebr))
        tape = tengri_hebr[start:end]
        n_sec = sum(1 for c in tape if c in MISSING_OPERATORS)
        sec_per_phase.append(n_sec)

    # Top 10 Phasen mit den meisten Sec-Buchstaben
    top_sec = sorted(enumerate(sec_per_phase), key=lambda x: -x[1])[:10]
    print("Top 10 Phasen mit den meisten Sec-Buchstaben (= Spanda-Pulse):")
    for phase_idx, n_sec in top_sec:
        book, chap = phase_to_torah(phase_idx)
        print(f"  Phase {phase_idx:>3} ({book[:3]} {chap:>2}): {n_sec} Sec-Operatoren")
    print()

    # BURUMUTREFAMTU-Phase
    refamtu_phase = idx // 99
    print(f"BURUMUTREFAMTU-Phase: {refamtu_phase}")
    print(f"  (Phase {refamtu_phase} hat {sec_per_phase[refamtu_phase]} Sec-Operatoren)")
    print()

    # ============================================================
    # E) BURUMUT-SEC-BUCHSTABEN IM VOLLTEXT
    # ============================================================
    print("=" * 78)
    print("🔤 E) BURUMUT-SEC IM TENGRI137-VOLLTEXT")
    print("=" * 78)
    print()
    print(f"5 Sec-Buchstaben: {list(MISSING_OPERATORS.keys())}")
    print(f"Operatoren: {list(MISSING_OPERATORS.values())}")
    print()

    for op_char, op_name in MISSING_OPERATORS.items():
        count = tengri_hebr.count(op_char)
        first_pos = tengri_hebr.find(op_char)
        last_pos = tengri_hebr.rfind(op_char)
        print(f"  {op_char} ({op_name:>11}): {count:>4}x in Tengri137, "
              f"erste={first_pos}, letzte={last_pos}")
    print()

    # Total Sec-Buchstaben
    total_sec = sum(tengri_hebr.count(c) for c in MISSING_OPERATORS)
    print(f"TOTAL Sec-Buchstaben: {total_sec} / {len(tengri_hebr)} "
          f"({100*total_sec/len(tengri_hebr):.2f}%)")
    print()

    # ============================================================
    # ZUSAMMENFASSUNG: WAS STEHT AN
    # ============================================================
    print("=" * 78)
    print("📊 ZUSAMMENFASSUNG: WAS STEHT AN")
    print("=" * 78)
    print()
    print("AUS DEN BEFUNDEN:")
    print()
    print("1. PENDEL-PHASEN STABILISIEREN")
    print(f"   - 113 / 168 Phasen pendeln")
    print(f"   - Numeri: 25 / 32 (78.1%) = höchste Priorität")
    print(f"   - Was steht an: Numeri-Phasen tiefer dekodieren")
    print()
    print("2. BURUMUTREFAMTU-POSITION 15986")
    print(f"   - Kontext: ...RAIN CANNOT BE REVERSED + REFAMTU + NURESUTREGUMFA...")
    print(f"   - M4 auf Kontext: {r2['total_steps']} Schritte, halt={r2['halt_state']}")
    print(f"   - Was steht an: Volle Dekodierung der Stelle")
    print()
    print("3. 7 SCHÖPFUNGSTAGE")
    print(f"   - Tengri137 = 168 Phasen = 7 × 24")
    print(f"   - Tag-Gematrien:")
    for d in days:
        print(f"     Tag {d['day']}: Gem={d['gematria']}, Sec={d['n_sec_chars']}")
    print(f"   - Was steht an: Tag-Grenzen verifizieren")
    print()
    print("4. SPANDA-PULSE")
    print(f"   - Top Sec-Phasen: {[p for p, _ in top_sec[:5]]}")
    print(f"   - BURUMUTREFAMTU-Phase: {refamtu_phase}")
    print(f"   - Was steht an: Formale Spanda-Operatoren")
    print()
    print("5. BURUMUT-SEC IM VOLLTEXT")
    for op_char, op_name in MISSING_OPERATORS.items():
        count = tengri_hebr.count(op_char)
        print(f"   - {op_char} ({op_name}): {count}x")
    print(f"   - Was steht an: Diese Positionen als Anker nutzen")
    print()

    # Speichern
    output = {
        'method': 'Was steht an: Tengri137 + Tora',
        'pendel_phasen': {
            'total': len(pendel_phasen),
            'pro_Buch': dict(pendel_per_book),
            'numeri_pendel_first_10': numeri_pendel[:10],
        },
        'burumutrefamtu_position': {
            'tengri_position': idx,
            'phase': refamtu_phase,
            'in_phase_offset': idx % 99,
            'context_before': context_before,
            'context_after': context_after,
            'm4_auf_refamtu': r['total_steps'],
            'm4_auf_kontext': r2,
        },
        '7_tage_tengri137': days,
        'spanda_top_phasen': top_sec,
        'sec_buchstaben_volltext': {
            op_char: {
                'count': tengri_hebr.count(op_char),
                'name': MISSING_OPERATORS[op_char],
                'first': tengri_hebr.find(op_char),
                'last': tengri_hebr.rfind(op_char),
            }
            for op_char in MISSING_OPERATORS
        },
        'total_sec': total_sec,
    }
    with open('/run/media/julian/ML4/tengri137/sources/was_steht_an.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("Ergebnisse gespeichert in was_steht_an.json")
    print()

    return output


if __name__ == "__main__":
    main()
