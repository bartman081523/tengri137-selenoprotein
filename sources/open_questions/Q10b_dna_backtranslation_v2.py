"""
Q10 v2: BURUMUT -> DNA Rückübersetzung mit korrekter Codon-Behandlung

Sec (U) wird über UGA recodiert. Aber UGA ist eigentlich der Opal-Stop.
In Sec-reichen mRNAs wird UGA NICHT als Stop gelesen, sondern als Sec.

Pyl (O) wird über UAG recodiert. Aber UAG ist eigentlich der Amber-Stop.

BURUMUT hat 11 U (Sec) und 2 O (Pyl).
Im Protein-Kontext sind das 13 "recodierte Stop-Codons".
Die DNA enthält 11 UGA + 2 UAG = 13 Stellen, wo ein normaler Reader
Stop erwarten würde.

Das ist biologisch AUSSERGEWÖHNLICH - normalerweise hat ein Protein
nur 1 Stop-Codon am Ende.
"""
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# Korrigiert: Sec = UGA (immer), Pyl = UAG (immer)
def backtranslate_sec(seq):
    dna = ''
    for aa in seq:
        if aa == 'A': dna += 'GCU'
        elif aa == 'R': dna += 'CGU'
        elif aa == 'N': dna += 'AAC'
        elif aa == 'D': dna += 'GAC'
        elif aa == 'C': dna += 'UGC'
        elif aa == 'E': dna += 'GAA'
        elif aa == 'Q': dna += 'CAG'
        elif aa == 'G': dna += 'GGC'
        elif aa == 'H': dna += 'CAC'
        elif aa == 'I': dna += 'AUU'
        elif aa == 'L': dna += 'CUG'
        elif aa == 'K': dna += 'AAG'
        elif aa == 'M': dna += 'AUG'
        elif aa == 'F': dna += 'UUC'
        elif aa == 'P': dna += 'CCG'
        elif aa == 'S': dna += 'AGC'
        elif aa == 'T': dna += 'ACC'
        elif aa == 'W': dna += 'UGG'
        elif aa == 'Y': dna += 'UAC'
        elif aa == 'V': dna += 'GUG'
        elif aa == 'U': dna += 'UGA'  # Sec!
        elif aa == 'O': dna += 'UAG'  # Pyl!
        elif aa == 'B': dna += 'AAC'  # Asn (default)
        elif aa == 'Z': dna += 'CAG'  # Gln (default)
        else: dna += 'NNN'
    return dna

dna = backtranslate_sec(BURUMUT_FULL)

print("="*70)
print("Q10b.1: BURUMUT -> DNA (korrekte Sec/Pyl-Behandlung)")
print("="*70)
print(f"DNA-Laenge: {len(dna)} Basen (99 Codons)")
print(f"DNA-Sequenz:")
for i in range(0, len(dna), 60):
    codons = [dna[j:j+3] for j in range(i, min(i+60, len(dna)), 3)]
    print(f"  Pos {i:3d}-{i+len(codons)*3-3:3d}: {' '.join(codons)}")

# Stop-Codon-Suche
print()
print("="*70)
print("Q10b.2: Stop-Codons in der rueckuebersetzten DNA")
print("="*70)
stops = {'TAA': '*', 'TAG': '*', 'TGA': 'Sec (U)'}
for i in range(0, len(dna) - 2, 3):
    codon = dna[i:i+3]
    if codon in stops:
        aa_in_burumut = BURUMUT_FULL[i // 3]
        print(f"  Pos {i//3:2d} ({i:3d}-{i+2}): {codon} -> {stops[codon]} (BURUMUT: {aa_in_burumut})")

# Was wenn BURUMUT KEIN vollständiges Protein ist, sondern nur eine Domäne?
# Dann fehlt das Stop-Codon am Ende, und die Sec-Codons sind die einzigen "Stops".
print()
print(f"Anzahl Sec-relevanter Stops: 11 UGA + 2 UAG = 13")
print(f"  (= Anzahl Sec + Pyl in BURUMUT)")

# Wir testen: Wenn man nur Sec (UGA) als "Stop" liest,
# hat die mRNA 11 Sec-Positionen. Diese brauchen SECIS-Elemente
# in der 3'-UTR, um als Sec recodiert zu werden.

# RNA-Sekundaerstruktur um UGA
print()
print("="*70)
print("Q10b.3: SECIS-Element-Suche in der hypothetischen 3'-UTR")
print("="*70)
# Wir koennen die mRNA-Sequenz direkt anschauen:
mrna = dna.replace('T', 'U')  # DNA -> RNA
print(f"mRNA-Laenge: {len(mrna)} Basen")

# SECIS consensus: AUGA-CC-GA-N3-AA-N2-AAARAA (in Loop-Region)
# Wir suchen nach AUGA in der mRNA
import re
secis_hits = []
for m in re.finditer('AUGA', mrna):
    secis_hits.append(m.start())
print(f"AUGA-Positionen in mRNA (Sec-Recodierungs-Signal): {secis_hits}")
# Aber: AUGA enthält UGA, was Sec-codon ist. Das ist nicht das SECIS-Pattern.

# Echtes SECIS hat AUGA in einer Haarnadel-Struktur.
# Aber: wir haben keine Sekundaerstrukturvorhersage hier.

# Suche nach dem SECIS-Konservierten "Quartett":
# AA-N6-AAA-N2-AAAR (vereinfacht)
# Eukaryoten-SECIS: G-N2-A-N3-AAR-AAA-N2-GA-N-AAARAA
print()
print("Suche nach SECIS-Element-Muster (vereinfacht):")
patterns = ['AAA.{6,12}AAA', 'AUGA.{0,4}CC', 'AAA.{10}AAA.{10}AAA']
for pat in patterns:
    matches = list(re.finditer(pat, mrna))
    if matches:
        print(f"  Pattern '{pat}': {len(matches)} Treffer")
        for m in matches[:3]:
            print(f"    Pos {m.start()}: {mrna[max(0,m.start()-5):m.end()+5]}")

# Letzter Abschnitt der mRNA (nach dem letzten Codon)
last_50 = mrna[-50:]
print(f"\nLetzte 50 Basen der mRNA (3'-UTR-Region):")
print(f"  {last_50}")

# Wenn das ein echtes Protein-Fragment ist, sollte hier ein SECIS sein
# Eukaryoten: SECIS ist 60-90 nt nach dem letzten UGA
# In Prokaryoten: keine SECIS, sondern SelB-abhängig
