"""
Q23 (NEU): Vollständige mRNA-Architektur von BURUMUT

Wir rekonstruieren die vollständige mRNA, die BURUMUT kodiert:
1. AUG-Start-Codon (Methionin)
2. 99 Codons für die AS
3. SECIS-Elemente in 3'-UTR
4. Stop-Codon

Wir testen mehrere Szenarien:
A. BURUMUT hat KEINEN M am Anfang → M am Anfang hinzufügen
B. BURUMUT hat KEIN echtes Stop am Ende → UAA/UGA am Ende
C. SECIS-Elemente im 3'-UTR
"""
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# Codon-Tabelle (haeufigste eukaryote Codons)
CODON_MAP = {
    'A': 'GCC', 'R': 'CGC', 'N': 'AAC', 'D': 'GAC', 'C': 'UGC',
    'E': 'GAG', 'Q': 'CAG', 'G': 'GGC', 'H': 'CAC', 'I': 'AUC',
    'L': 'CUG', 'K': 'AAG', 'M': 'AUG', 'F': 'UUC', 'P': 'CCG',
    'S': 'AGC', 'T': 'ACC', 'W': 'UGG', 'Y': 'UAC', 'V': 'GUG',
    'U': 'UGA', 'O': 'UAG', 'B': 'AAC', 'Z': 'CAG'
}

# Szenario A: BURUMUT beginnt mit M (Standard-Protein)
print("="*70)
print("Q23.1: BURUMUT mit kuenstlichem M-Start")
print("="*70)
protein_with_start = 'M' + BURUMUT_FULL
mrna_with_start = 'AUG' + ''.join(CODON_MAP[aa] for aa in BURUMUT_FULL)
print(f"Protein: M + BURUMUT = {len(protein_with_start)} AS")
print(f"mRNA: 297 + 3 = {len(mrna_with_start)} Basen")

# 5'-UTR hinzufuegen
utr_5 = 'GCCAGACAAUUAAG'  # Kozak-Context
mrna_full = utr_5 + mrna_with_start
print(f"5'-UTR: {utr_5} ({len(utr_5)} Basen)")
print(f"mRNA Total: {len(mrna_full)} Basen")

# 3'-UTR mit SECIS-Element
secis = 'AUGAACCGGAAAAAAGCAACGUAAACUUGA'  # SECIS-Konsensus
utr_3 = secis + 'AAAAAAAAA'  # poly-A-Schwanz
mrna_full += utr_3
print(f"3'-UTR-SECIS: {secis} ({len(secis)} Basen)")
print(f"3'-UTR-polyA: AAAAAAAAA (9 Basen)")
print(f"mRNA Total mit UTRs: {len(mrna_full)} Basen")
print()

# 2. Szenario B: BURUMUT koennte eigenstaendiges Protein sein
print("="*70)
print("Q23.2: BURUMUT als Fragment eines groesseren Proteins")
print("="*70)
# Wenn BURUMUT Fragment ist, fehlt der N-Terminus
# Die erste AS waere dann der Sec-Position
print(f"BURUMUT beginnt mit 'B' (Asx = Asn/Asp unscharf)")
print(f"Wenn Fragment: B ist eine interne Position, kein N-Terminus")
print(f"  → Moeglicher N-Terminus: ein Sec-reiches Leader-Peptid")
print(f"  → C-Terminus unklar (BURUMUT endet mit N)")

# 3. SECIS-Element-Analyse
print()
print("="*70)
print("Q23.3: SECIS-Elemente in der 3'-UTR")
print("="*70)
# Suche AUGA in 3'-UTR
import re
auga_in_utr = re.findall('AUGA', utr_3)
print(f"AUGA in SECIS-Konsensus: {len(auga_in_utr)}")

# 4. Strukturelle Konsistenz mit Sec-Insertion
print()
print("="*70)
print("Q23.4: Strukturelle Konsistenz")
print("="*70)
# In Eukaryoten:
# 1. SECIS im 3'-UTR dirigiert ALLE UGA-Stops davor
# 2. SECIS ist 30-700 nt nach dem letzten UGA
# 3. SECIS hat ein AUGA-Motiv

# BURUMUT-mRNA hat 11 UGA (Sec) + 2 UAG (Pyl) = 13 "Stops"
# Ein einziges SECIS wuerde alle 13 dirigieren
# 3 SECIS-Elemente teilen die Last auf

# Wenn 3 SECIS, wo sind sie?
print("3 SECIS-Elemente (basierend auf AUGA-Pattern in mRNA):")
mrna = ''.join(CODON_MAP[aa] for aa in BURUMUT_FULL)
auga_pos = [m.start() for m in re.finditer('AUGA', mrna)]
for i, ap in enumerate(auga_pos):
    # Welcher Bereich wird dirigiert?
    next_auga = auga_pos[i+1] if i+1 < len(auga_pos) else len(mrna)
    in_range = [j for j in range(0, len(mrna) - 2, 3)
                if ap < j < next_auga and mrna[j:j+3] in {'UGA', 'UAG'}]
    print(f"  SECIS #{i+1} an mRNA-Pos {ap}: dirigiert {len(in_range)} Stop-Codons")

# 5. Phylogenetische Marker
print()
print("="*70)
print("Q23.5: Was SECIS-Struktur verraten")
print("="*70)
# SECIS-Sekundaerstruktur in Eukaryoten:
# - Haarnadel mit apical loop
# - "Quartet" mit GA-N-AAA
# - "K-turn" mit G·A, A·A Basenpaaren
#
# In Prokaryoten: KEIN SECIS, Sec-Insertion via SelB direkt
# In Archaea: SECIS-artige Strukturen
# In Eukaryoten: SECIS-Element im 3'-UTR

# Wenn BURUMUT archaeal-ähnlich ist:
# - SECIS-Struktur ist anders
# - Sec-Insertion ist einfacher

# Wenn BURUMUT eukaryotisch ist:
# - SECIS muss im 3'-UTR sein
# - Multi-SECIS-Architektur ist ungewöhnlich

# Wenn BURUMUT prokaryotisch ist:
# - KEIN SECIS
# - SelB-abhängige Insertion
# - mRNA ist polycistronisch möglich

print("BURUMUT hat 11 UGA + 2 UAG in 99 AS = 13 recodierte Stops")
print("Multi-SECIS-Architektur (3 SECIS fuer 13 Stops) ist:")
print("  - Bei Eukaryoten: komplex aber moeglich (z.B. SelenoP hat 10 Sec)")
print("  - Bei Prokaryoten: ungewoehnlich (eukaryoten-ähnlicher Mechanismus)")
print("  - Bei Archaea: sehr selten")
