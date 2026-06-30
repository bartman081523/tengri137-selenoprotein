"""
Q26 (NEU): Welcher Sec-Insertion-Mechanismus passt zu BURUMUT?

BURUMUT hat 11 UGA + 2 UAG in einer 99-AS-Sequenz.
In echten Sec-Proteinen gibt es:
- Eukaryoten: 1 SECIS-Element pro mRNA, dirigiert ALLE Sec
- Archaeen: SECIS-ähnliche Strukturen, aber andere Konsensus
- Prokaryoten: KEIN SECIS, sondern SelB-Protein + spezifische mRNA-Haarnadel

BURUMUTs mRNA hat 3 AUGA-Motive als SECIS-Kandidaten.
Wir testen: Welcher Insertions-Mechanismus passt am besten?
"""
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# mRNA zurückübersetzen
codon_map = {
    'A': 'GCC', 'R': 'CGC', 'N': 'AAC', 'D': 'GAC', 'C': 'UGC',
    'E': 'GAG', 'Q': 'CAG', 'G': 'GGC', 'H': 'CAC', 'I': 'AUC',
    'L': 'CUG', 'K': 'AAG', 'M': 'AUG', 'F': 'UUC', 'P': 'CCG',
    'S': 'AGC', 'T': 'ACC', 'W': 'UGG', 'Y': 'UAC', 'V': 'GUG',
    'U': 'UGA', 'O': 'UAG', 'B': 'AAC', 'Z': 'CAG'
}
mrna = ''.join(codon_map[aa] for aa in BURUMUT_FULL)

# Sec-UGA-Positionen
sec_uga = []
pyl_uag = []
for i in range(0, len(mrna) - 2, 3):
    if mrna[i:i+3] == 'UGA':
        sec_uga.append(i)
    elif mrna[i:i+3] == 'UAG':
        pyl_uag.append(i)

print("="*70)
print("Q26.1: Sec-Insertion-Mechanismus - Übersicht")
print("="*70)
print(f"BURUMUT mRNA-Laenge: {len(mrna)} Basen")
print(f"Sec-UGA-Positionen ({len(sec_uga)}): {sec_uga}")
print(f"Pyl-UAG-Positionen ({len(pyl_uag)}): {pyl_uag}")
print()

# In Eukaryoten: SECIS-Element dirigiert ALLE UGA
# Ein einzelnes SECIS-Element reicht
print("="*70)
print("Q26.2: Eukaryot-Modell (1 SECIS dirigiert alle UGA)")
print("="*70)
print("In Eukaryoten: 1 SECIS im 3'-UTR dirigiert ALLE UGA-Codons.")
print("BURUMUT's 3 AUGA-Motive -> 3 SECIS-Elemente -> MOEGLICH aber unueblich")
print("Vergleich: SelenoP hat 2 SECIS fuer 10 UGA")
print(f"  BURUMUT: 3 SECIS fuer 13 UGA+UAG ({13/3:.2f} pro SECIS)")
print(f"  SelenoP: 2 SECIS fuer 10 UGA ({10/2:.2f} pro SECIS)")
print()

# In Archaeen: SECIS-ähnlich, aber anderer Konsensus
# Archaeen-Methanococcus jannaschii hat SECIS-Box (CCUGGA-Loop)
print("="*70)
print("Q26.3: Archaeen-Modell")
print("="*70)
# In M. jannaschii: SECIS-ähnliche Strukturen
# Aber Archaeen haben oft Pyl statt Sec
# BURUMUT hat 2 Pyl (UAG) -> passt zu Archaeen-Hypothese
import re
# Suche nach CCUGGA-Motiv (Archaeen-SECIS)
secis_archaeal = re.findall(r'CC[UC]GGA', mrna)
print(f"Archaeen-SECIS 'CCUGGA' in mRNA: {secis_archaeal}")
print(f"BURUMUT hat 2 Pyl (O) -> Archaeen-Indikator")
print(f"  -> Archaeen-Pyl-Insertion benoetigt PylRS + tRNA-Pyl")
print(f"  -> Sec in Archaeen: meistens E. coli-ähnlich, kein SECIS")
print()

# In Prokaryoten (E. coli): SelB erkennt mRNA-Haarnadel am UGA
# Spezifische Sekundärstruktur
print("="*70)
print("Q26.4: Prokaryoten-Modell (E. coli SelB)")
print("="*70)
# In E. coli: SelB bindet an mRNA-Haarnadel nahe UGA
# Konsensus: mRNA-Schleife am UGA mit bestimmten Basen
# Wenn BURUMUT prokaryotisch wäre: keine SECIS-Elemente nötig
# Aber: BURUMUT hat 3 AUGA-Motive, die zufällig sein könnten

# 5. Welcher Mechanismus passt numerisch?
print("="*70)
print("Q26.5: Numerische Anpassung")
print("="*70)
# In Prokaryoten (E. coli): 1 Sec pro Protein
# BURUMUT hat 11 Sec - in E. coli koexistieren verschiedene Sec-Proteine,
# aber jede einzeln hat nur 1 Sec (außer SelP mit 10)
# → E. coli passt kaum

# In Eukaryoten: Multi-Sec-Proteine (SelP 10 Sec) sind möglich
# BURUMUT mit 11 Sec passt zu Multi-Sec-Proteinen
# → Eukaryot wahrscheinlich

# In Archaeen: Sec seltener, Pyl häufiger (Methanosarcina)
# BURUMUT hat BEIDES (11 Sec, 2 Pyl) - sehr Archaeen-ähnlich
# → Archaeen-Misch-Mechanismus möglich
