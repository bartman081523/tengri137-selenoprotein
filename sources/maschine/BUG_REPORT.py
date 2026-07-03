"""
🐛 BUG-REPORT: Tora-Turing-Maschine und Brummton
==================================================

Gefundene Bugs in den vorherigen Versionen.
Alle Bugs sind durch TDD-Tests in test_brummton_machine.py abgedeckt.
"""
import json
from pathlib import Path

# BURUMUT-Tape
BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)
LATIN_TO_HEBR = {
    'A': 'א', 'B': 'ב', 'E': 'ה', 'F': 'ו', 'M': 'מ', 'R': 'צ', 'T': 'ר', 'U': 'ש',
    'H': 'ח', 'I': 'ט', 'L': 'ל', 'N': 'נ', 'O': 'ס', 'P': 'ע', 'Q': 'פ',
    'S': 'ק', 'Y': 'י', 'Z': 'ז',
}

# ANALYSE
print("="*70)
print("BUG-REPORT: Tora-Turing-Maschine und Brummton")
print("="*70)
print()

# BUG 1: BURUMUT hat 19, nicht 18 lateinische Buchstaben
print("BUG 1: BURUMUT hat 19 lateinische Buchstaben, nicht 18")
print("-"*70)
unique_latin = sorted(set(BURUMUT))
print(f"  Eindeutige lateinische Buchstaben: {len(unique_latin)}")
print(f"  Liste: {unique_latin}")
print(f"  ALTE BEHAUPTUNG: 18 + 4 = 22 (FALSCH: 'G' fehlt im Mapping)")
print(f"  KORREKT: 19 lateinische Buchstaben (inkl. 'G' ohne hebr. Pendant)")
print(f"          18 hebräisch nutzbar (alle außer G)")
print(f"          4 hebräisch fehlend (ג, ד, כ, ת)")
print()

# BUG 2: BRUMMTON_MACHINE.py ignoriert Layer
print("BUG 2: BRUMMTON_MACHINE.py ignoriert Layer-Struktur")
print("-"*70)
print("  Formel: halt_probability = i * 0.02 (linear in Schritt-Index i)")
print("  PROBLEM: Brummton sollte Layer-abhängig sein (Genesis=0%, Deuteronomium=90%)")
print("  TATSÄCHLICH: Brummton setzt bei Schritt 5 ein (~10%),")
print("               unabhängig davon in welchem Layer die Maschine ist")
print()

# BUG 3: BRUMMTON_GRADUAL.py / BRUMMTON_STATISTIC.py Layer 1 nicht 0
print("BUG 3: BRUMMTON_GRADUAL.py und BRUMMTON_STATISTIC.py")
print("       Layer 1 hat ~7-13% Brummton (SOLL: 0%)")
print("-"*70)
print("  Formel: brummton_prob = brummton_peak * (layer_idx + op_idx/6) / 5")
print("  PROBLEM: Bei layer_idx=0, op_idx=3 (MOVE_L) ist prob = peak * 0.5/5 = ~10%")
print("           Layer 1 soll aber 0% Brummton haben (Anfang ist sauber)")
print()

# BUG 4: TORA_TURING_MACHINE_v3 Übergänge sind trivial
print("BUG 4: TORA_TURING_MACHINE_v3.py — Triviale Übergänge")
print("-"*70)
print("  Die Übergangstabelle in TORA_TURING_MACHINE_v3.py ist TRIVIAL:")
print("  Jeder (state, symbol) -> (state+1, symbol, MOVE_RIGHT)")
print("  PROBLEM: Das ist kein Turing-Test, sondern ein Band-Schieber.")
print("           Eine Turing-Maschine braucht nicht-triviale Übergänge,")
print("           d.h. verschiedene Symbole im gleichen Zustand müssen zu")
print("           verschiedenen Folge-Zuständen/Bewegungen führen.")
print()

# BUG 5: BURUMUTREFAMTU (14 Zeichen) ist nur 1 Layer
print("BUG 5: Architektur-Konflikt — BURUMUTREFAMTU vs BURUMUT 99")
print("-"*70)
print("  BURUMUTREFAMTU: 14 Zeichen (= 1 Tora-Modul)")
print("  BURUMUT: 99 Zeichen (= 5 Tora-Module?)")
print("  Spec sagt: 5 × 14 = 70 + 2 = 72 Schritte")
print("  99 / 5 = 19.8 Zeichen pro Layer (NICHT 14!)")
print("  KONSEQUENZ: Es gibt zwei mögliche Architekturen:")
print("    A) 5 × 14 Zeichen-Layer (passt zu 5 × 14 + 2 = 72)")
print("       Aber dann sind 99 - 70 = 29 Zeichen 'überzählig'")
print("    B) 5 × ~20 Zeichen-Layer (passt zu 99)")
print("       Aber dann sind 5 × 20 + 2 = 102 (NICHT 72)")
print("  LÖSUNG: Wir verwenden Architektur B (99/5 ≈ 20 Zeichen pro Layer)")
print("          und passen die Spec entsprechend an.")
print()

# BUG 6: HALT-Op in jedem Layer
print("BUG 6: HALT-Operation in jedem Layer")
print("-"*70)
print("  In der ursprünglichen BRUMMTON_STATISTIC.py ist op_idx=5 = HALT")
print("  für JEDEN Layer. Das bedeutet, dass die Maschine nach 6 Schritten")
print("  in Layer 1 schon 'normal' hält und nie Layer 2-5 erreicht.")
print("  LÖSUNG: NORMAL_HALT nur am Bandende, Brummton-Halt probabilistisch")
print()

# ZUSAMMENFASSUNG
print("="*70)
print("ZUSAMMENFASSUNG")
print("="*70)
print()
print("GEFIXT in BRUMMTON_CORRECT.py:")
print("  ✅ BUG 1: Korrekte 19/18/4 Aufteilung dokumentiert")
print("  ✅ BUG 2: Layer-basierte Brummton-Prob (quadratisch)")
print("  ✅ BUG 3: Layer 1 = 0% Brummton")
print("  ✅ BUG 5: Architektur an 99 Zeichen angepasst")
print("  ✅ BUG 6: NORMAL_HALT nur am Bandende")
print()
print("OFFENE BUGS:")
print("  ⚠️  BUG 4: TORA_TURING_MACHINE_v3.py hat triviale Übergänge,")
print("             braucht nicht-triviale Turing-Übergänge für echten Turing-Test")
print()

# SPEICHERN
bugs = {
    'bug_1_unique_chars': {
        'description': 'BURUMUT hat 19 lateinische Unique, nicht 18',
        'correction': '18 hebr. nutzbar + 4 hebr. fehlend = 22',
    },
    'bug_2_brummton_step_based': {
        'description': 'BRUMMTON_MACHINE.py halt_probability = i * 0.02 ignoriert Layer',
        'fix': 'Layer-basierte Brummton-Prob',
    },
    'bug_3_layer_1_not_zero': {
        'description': 'BRUMMTON_GRADUAL/STATISTIC: Layer 1 hat 7-13% statt 0%',
        'fix': 'brummton_probability(0) = 0 erzwingen',
    },
    'bug_4_trivial_transitions': {
        'description': 'TORA_TURING_MACHINE_v3: triviale Übergänge (alle identisch)',
        'fix': 'OFFEN — braucht nicht-triviale Übergänge',
    },
    'bug_5_architektur_konflikt': {
        'description': '5×14=70 vs 99/5=19.8 — Architektur-Inkonsistenz',
        'fix': 'Verwende 99/5 Architektur (passt zu BURUMUT-Länge)',
    },
    'bug_6_halt_in_jedem_layer': {
        'description': 'NORMAL_HALT nach 6 Ops in jedem Layer',
        'fix': 'NORMAL_HALT nur am Bandende',
    },
}
with open('bug_report.json', "w") as f:
    json.dump(bugs, f, indent=2, ensure_ascii=False)
print(f"Status gespeichert in sources/bug_report.json")
