"""
Q22 (NEU): Was bedeutet NOMBA in BURUMUT?

NOMBA hat eine 2x-Wiederholung in BURUMUT (Pos 51-55 und 86-90).
Sequenz: N-O-M-B-A = Asn-Pyl-Asx-Ala

In einem Sec-reichen Protein:
- N = Asn (Asparagin)
- O = Pyl (Pyrrolysine, 22. Aminosaeure!)
- M = Met (Methionin)
- B = Asx (Asn/Asp unscharf)
- A = Ala (Alanine)

Hypothese: NOMBA ist ein 'Pyl-Anker' - Pyrrolysine tritt
normalerweise in Archaeen-Methyltransferasen auf.

Wir testen: Was wenn NOMBA ein zweiter Sec-Insertion-Marker ist
(wie UAZBE)?
"""
import random
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# 1. NOMBA-Positionen
print("="*70)
print("Q22.1: NOMBA-Vorkommen in BURUMUT")
print("="*70)
for i in range(len(BURUMUT_FULL) - 4):
    if BURUMUT_FULL[i:i+5] == 'NOMBA':
        ctx = BURUMUT_FULL[max(0,i-5):i+10]
        print(f"  NOMBA an Pos {i}: ...{ctx}...")

# 2. NOMBA als Sec-Insertion-Signal?
# In echten Prokaryoten: SECIS fehlt
# Sec wird über SelB-tRNASec direkt erkannt
# In Eukaryoten: SECIS-Element im 3'-UTR
# In Archaeen: Pyl-Insertion via PylRS

# Wenn BURUMUT archaeal-like ist:
# - NOMBA könnte Pyl-Insertion markieren
# - UAZBE könnte Sec-Insertion markieren

# 3. Vergleich: NOMBA vs UAZBE
print()
print("="*70)
print("Q22.2: NOMBA und UAZBE als Doppel-Anker")
print("="*70)
# UAZBE an Pos 32, 46, 66, 80
# NOMBA an Pos 51, 86
# Differenzen NOMBA-UAZBE: 51-46=5, 86-80=6
# Pattern: NOMBA folgt kurz nach UAZBE (5-6 Zeichen)

uazbe_pos = [32, 46, 66, 80]
nombas_pos = []
for i in range(len(BURUMUT_FULL) - 4):
    if BURUMUT_FULL[i:i+5] == 'NOMBA':
        nombas_pos.append(i)
print(f"UAZBE-Positionen: {uazbe_pos}")
print(f"NOMBA-Positionen: {nombas_pos}")

# 4. Welche Sequenz-Struktur hat BURUMUT zwischen UAZBE und NOMBA?
print()
print("="*70)
print("Q22.3: BURUMUT-Sequenz zwischen Ankern")
print("="*70)
print("Volle BURUMUT-Struktur mit Markierungen:")
marked = BURUMUT_FULL.replace('UAZBE', '|UAZBE|').replace('NOMBA', '|NOMBA|').replace('HIMLAZANR', '|HIMLAZANR|')
print(f"  {marked}")
print()
print("Modulare Struktur:")
print("  Vorspann (BURUMUTREFAMTU...): 32 Zeichen")
print("  UAZBE (Anker #1)")
print("  HIMLAZANR (Modul A)")
print("  UAZBE (Anker #2)")
print("  NOMBA... (Modul B)")
print("  UAZBE (Anker #3)")
print("  HIMLAZANR (Modul A wiederholt)")
print("  UAZBE (Anker #4)")
print("  NOMBA... (Modul B wiederholt, modifiziert)")

# 5. Was wenn die Module Sec-relevante Funktionen haben?
print()
print("="*70)
print("Q22.4: Modulare Hypothese")
print("="*70)
print("HIMLAZANR (Modul A) - 9 AS = Sec-reiches Modul mit Glx-Asx-Glu")
print("NOMBA... (Modul B) - variabel, mit Pyl-Insertion (O)")
print("UAZBE (Anker) - Sec-Insertion-Signal")
print()
print("BURUMUT-Architektur (hypothetisch):")
print("  [UAZBE] [Modul A] [UAZBE] [Modul B] [UAZBE] [Modul A] [UAZBE] [Modul B]")
print("  = 4 Sec-Anker, 2 Modul-A-Wiederholungen, 2 Modul-B-Wiederholungen")
print("  = 99 AS, davon ~11 Sec, 2 Pyl, 0 Cys")
