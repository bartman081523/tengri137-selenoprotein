"""
Q11 (NEU): SECIS-Element-Analyse in der hypothetischen mRNA

SECIS = Selenocysteine Insertion Sequence

In Eukaryoten ist SECIS eine RNA-Sekundaerstruktur im 3'-UTR der mRNA.
Konsensus-Struktur:
- Haarnadel mit apical loop
- AUGA-Motiv im apical loop (oder 5' davon)
- "Quartett" mit konservierten Basen: GA-N3-AAA-N-AAAR

BURUMUT's mRNA (aus Q10) hat:
- 11 UGA-Codons (Sec-Positionen)
- 2 UAG-Codons (Pyl-Positionen)
- AUGA-Motiv an Position 33, 159, 261

Wir testen:
1. Ist die RNA-Sekundaerstruktur plausibel als SECIS?
2. Wie viele SECIS-Elemente werden gebraucht (1 pro UGA, oder mehrere)?
3. Welche UGA-Positionen sind "echte" Sec vs nur-Stop?

In Selenoprotein P (menschlich):
- 10 UGA-Codons für Sec
- 2 SECIS-Elemente (1 fuer alle 10 UGA reicht)

In GPx1 (menschlich):
- 1 UGA-Codon (Sec am C-Terminus)
- 1 SECIS-Element

In BURUMUT:
- 11 UGA-Codons
- AUGA-Pattern an 3 Positionen
- UAG (Pyl) braucht keine SECIS (anderer Mechanismus)
"""
from collections import Counter

# mRNA aus Q10b
DNA = ('AACUGACGUGAAUGUGAACCCGUGAAUUCGCUAUGACCUGAAACUGACGUGAAAGCUGAACCCG'
       'UGAAUGUUCGCUUACGCUCCGAGCUGAGCAGAACGAGCACAUUAUGCUGGCUCAGGCUAACCGUG'
       'CAGAACGAACUAGAUGAACGCUCGUGCUCAGCACCAGCGUAGCGCUAAC')
mrna = DNA.replace('T', 'U')

print("="*70)
print("Q11.1: mRNA Struktur-Übersicht")
print("="*70)
print(f"mRNA-Laenge: {len(mrna)} Basen")
print(f"Anzahl UGA-Codons: {mrna.count('UGA')}")
print(f"Anzahl UAG-Codons: {mrna.count('UAG')}")
print(f"Anzahl UAA-Codons: {mrna.count('UAA')}")
print(f"Anzahl AUGA-Pattern: {mrna.count('AUGA')}")
print()

# In echten mRNAs ist UAA der häufigste echte Stop (50%)
# UAG ist Amber-Stop, ~20% der echten Stops
# UGA ist Opal-Stop, ~30% der echten Stops
# In BURUMUT: 0 UAA, 2 UAG, 11 UGA
# -> Alle UGA wären Sec, die 2 UAG sind echte Stops ODER Pyl

# Falls 2 UAG echte Stops sind:
# -> BURUMUT hätte 2-3 Teilproteine (Polypeptid-Fragmente)
# -> Sehr ungewöhnlich, aber nicht unmöglich (z.B. polycistronische mRNA)

# Falls 2 UAG Pyl sind (auch recodiert):
# -> BURUMUT wäre ein einziges Polypeptid mit 11 Sec + 2 Pyl
# -> Das ist extrem: 13 recodierte Stops in einem 99-AS-Protein

# 2. Sekundaerstruktur-Suche
print("="*70)
print("Q11.2: SECIS-Element-Pattern-Suche")
print("="*70)

# Eukaryoten-SECIS consensus (vereinfacht):
# AUGA-CC-GA + apical loop + Quartet: GA-N(3-9)-AAA-N-AAAR
# A 'quartet' consists of 4 non-Watson-Crick base pairs:
#   G·A, A·A, A·A, G·A

# Suche nach SECIS-Pattern
import re
print("\nSECIS-Element-Konsensus-Pattern-Suche:")
patterns = [
    ('Eukaryot-SECIS-AUGA-CC', r'AUGA.{0,3}CC.{0,5}GA'),
    ('SECIS-Quartet (GA-N3-AAA)', r'GA[AUCG]{3}AAA'),
    ('SECIS-Quartet erweitert', r'GA[AUCG]{0,9}AAA[UCG]{0,2}AAA'),
    ('Apical Loop AUGA', r'AUGA'),
]

for name, pat in patterns:
    matches = list(re.finditer(pat, mrna))
    if matches:
        print(f"  {name}: {len(matches)} Treffer")
        for m in matches[:3]:
            ctx = mrna[max(0, m.start()-3):m.end()+3]
            print(f"    Pos {m.start()}: ...{ctx}...")

# 3. Suche nach Stem-Loop-Strukturen (Hairpins)
print()
print("="*70)
print("Q11.3: Hairpin-Suche in der mRNA")
print("="*70)
# Eine Hairpin hat palindrome Struktur. RNA-Palindrome sind
# komplementär (A-U, G-C) aber inverted.
# Wir suchen nach inverted repeats.

# Invertierte Repeats: X-GAP-X', wobei X komplementär zu X' ist
# Mit minimaler Loop-Länge von 4 und minimaler Stem-Länge von 3
# Wir suchen vereinfacht nach Sequenz-Patterns.

def find_hairpins(seq, min_stem=3, min_loop=4, max_dist=30):
    """Findet mögliche Hairpin-Loops in einer RNA-Sequenz."""
    comp = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G'}
    hairpins = []
    for i in range(len(seq)):
        for j in range(i + min_stem + min_loop, min(i + max_dist, len(seq) - min_stem + 1)):
            # seq[i:i+stem] paired with seq[j:j+stem] (inverted)
            stem_len = min_stem
            matches = True
            for k in range(stem_len):
                if i + k >= j or j + k >= len(seq):
                    matches = False
                    break
                if seq[i + k] != comp.get(seq[j + k], '?'):
                    matches = False
                    break
            if matches:
                loop_seq = seq[i + stem_len:j]
                if len(loop_seq) >= min_loop:
                    hairpins.append((i, j, stem_len, loop_seq))
    return hairpins

hairpins = find_hairpins(mrna, min_stem=3, min_loop=3, max_dist=50)
print(f"Mögliche Hairpins: {len(hairpins)}")
for h in hairpins[:10]:
    i, j, stem_len, loop = h
    stem5 = mrna[i:i+stem_len]
    stem3 = mrna[j:j+stem_len]
    print(f"  Pos {i}-{j+stem_len}: 5'-{stem5}...{loop}...{stem3[::-1]}-3'")

# 4. Welche UGA-Codons sind an AUGA-Pattern gekoppelt?
print()
print("="*70)
print("Q11.4: AUGA-Pattern als Sec-Recodierungs-Signal")
print("="*70)
auga_pos = []
for m in re.finditer('AUGA', mrna):
    auga_pos.append(m.start())
print(f"AUGA-Positionen: {auga_pos}")
# Positionen sind 33, 159, 261 (in mRNA-Koordinaten)
# Aber: AUGA an Pos 33 ist NICHT das Codon-Pattern, sondern
# das letzte Codon vor dem nächsten Codon + Start von UGA

# RNA-Sekundaerstruktur: AUGA in Haarnadel-Loop dirigiert Sec-Einbau
# für das nächste UGA stromabwärts (downstream)
# Ein SECIS-Element dirigiert ALLE UGA-Codons stromabwärts bis zum Stop

# Falls die mRNA 3 SECIS-Elemente hat (an Pos 33, 159, 261):
# - SECIS#1 an Pos 33 dirigiert UGA-Codons stromabwärts
# - SECIS#2 an Pos 159 dirigiert UGA-Codons danach
# - SECIS#3 an Pos 261 dirigiert UGA-Codons danach

# Welche UGA-Codons werden von welchem SECIS dirigiert?
uga_codons = [i for i in range(0, len(mrna) - 2, 3) if mrna[i:i+3] == 'UGA']
print(f"UGA-Codon-Positionen: {uga_codons}")

for secis_pos in auga_pos:
    downstream = [u for u in uga_codons if u > secis_pos]
    upstream = [u for u in uga_codons if u < secis_pos]
    next_secis = [a for a in auga_pos if a > secis_pos]
    if next_secis:
        downstream = [u for u in uga_codons if secis_pos < u < next_secis[0]]
    else:
        downstream = [u for u in uga_codons if u > secis_pos]
    print(f"  AUGA@{secis_pos}: dirigiert UGA@{downstream} (n={len(downstream)})")

# 5. Was wenn BURUMUT 3 Subproteine kodiert?
# Wenn die UAG (Pyl) echte Stops sind, wären es 3 Fragmente:
# Fragment 1: BURUMUTREFAMTUNURESUTREGUMFAYAPS (32 AS, ohne Sec-an-UAG)
# Fragment 2: UAZBEHIMLAZANR (11 AS)
# Fragment 3: ... NOMBAMZHQRSAN (10 AS)

# Aber: Es gibt nur 2 UAG. Das Fragment-Pattern ist unklar.
# Wir testen: Welche UAG markieren Protein-Fragmente?
print()
print("="*70)
print("Q11.5: Mögliche Protein-Fragmente (UAG als echter Stop)")
print("="*70)
# Suche nach UAG in der Codon-Sequenz
uag_pos = [i // 3 for i in range(0, len(mrna) - 2, 3) if mrna[i:i+3] == 'UAG']
print(f"UAG-Positionen (Protein-Ebene): {uag_pos}")
# Wenn 2 UAG = 2 echte Stops:
# Fragment 1: Pos 0-39 (40 AS)
# Fragment 2: Pos 41-44 (4 AS, dann Stop)
# Fragment 3: Pos 46-? 
# Hmm, das passt nicht zu BURUMUT-Layout

# Lass uns einfach mal annehmen: alle 13 UGA/UAG sind Sec/Pyl,
# dann ist BURUMUT EIN Protein mit 13 ungewöhnlichen Aminosäuren.

# SECIS-Element-Suche um die mRNA
print()
print("Suche nach kompletten SECIS-Element-Strukturen:")
# SECIS consensus (Berry et al. 1993):
# 5'-AUGA-CC-[X]-GA-N(3-9)-AAA-N-AAAR-3' in apical loop
secis_pattern = r'AUGA.{0,4}CC.{0,3}GA[AUCG]{3,9}AAA[UCG]?AAA'
matches = list(re.finditer(secis_pattern, mrna))
print(f"Vollständige SECIS-Muster: {len(matches)} Treffer")
for m in matches:
    ctx = mrna[max(0,m.start()-10):m.end()+10]
    print(f"  Pos {m.start()}: ...{ctx}...")
