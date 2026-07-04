"""
BURUMUT vs ENPP1 - Detailanalyse
ENPP1 ist ein menschliches Enzym, das Signalmoleküle hydroisiert.
"""
import requests
import re

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)
BURUMUT_BLAST = (BURUMUT_FULL
    .replace('U', 'C').replace('O', 'K').replace('B', 'N').replace('Z', 'Q'))

# ENPP1 Position 107-156 aus dem Alignment
ENPP1_ALIGN_REGION = "SCKGRCFERTFGNCRCDAACVELGNCCLDYQETCIEPEHIWTCNKFRCGE"
BURUMUT_QUERY = "NCRCMCTREFAMTCNCRESCTREG-CMFAYAPSCAQNEHIMLAQANRCAQ"

print("="*70)
print("BURUMUT vs ENPP1 Detail-Vergleich")
print("="*70)
print(f"BURUMUT (99 AS, mit Sec/Cys substituiert):")
print(f"  {BURUMUT_BLAST}")
print()
print(f"ENPP1 Match-Region (Position 107-156):")
print(f"  {ENPP1_ALIGN_REGION}")
print()
print(f"Alignment (Mitte: BURUMUT 0-48, ENPP1 107-156):")
print(f"  BURUMUT: {BURUMUT_QUERY}")
print(f"  ENPP1:   {ENPP1_ALIGN_REGION}")
print()
# Position-fuer-Position Match (Substitution-Matrix-ähnlich)
print("Position-fuer-Position-Match:")
matches = 0
for a, b in zip(BURUMUT_QUERY, ENPP1_ALIGN_REGION):
    same = '*' if a == b else ('+' if a in 'CSA' and b in 'CSA' else ' ')
    print(f"  {a} {same} {b}")
    if a == b:
        matches += 1
print(f"\nExakte Matches: {matches}/{len(BURUMUT_QUERY)} = {matches/len(BURUMUT_QUERY)*100:.1f}%")

# Vergleich der BURUMUT-Vorspann-Sequenz (Sec-Markierungen)
print()
print("="*70)
print("Sec-Markierungen im Alignment")
print("="*70)
# Im Original (vor Substitution)
print("Original BURUMUT (erste 50 AS):")
print(f"  {BURUMUT_FULL[:50]}")
print(f"Positionen mit U (Sec): {[i for i, c in enumerate(BURUMUT_FULL[:50]) if c == 'U']}")
print()
print("ENPP1 Match-Region:")
print(f"  {ENPP1_ALIGN_REGION}")
print(f"Positionen mit C: {[i for i, c in enumerate(ENPP1_ALIGN_REGION) if c == 'C']}")
print()
print("Wenn ENPP1 'C' = 'Sec' substituiert, dann hätten wir Sec-Markierungen")
print("an ENPP1-Positionen 1, 6, 9, 11, 16, 20, 27, 33, 36, 42, 46, 49 (12 Cys in 50 AS)")
