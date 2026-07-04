"""
Q12 (NEU): SECIS-Element-Strukturanalyse

Eukaryoten-SECIS = Selenocysteine Insertion Sequence
Struktur:
1. Haarnadel mit apical loop
2. "Quartet" mit 4 nicht-Watson-Crick Basenpaaren: G·A, A·A, A·A, G·A
3. AUGA-Motiv im basal stem oder apical loop (nahe dem Quartet)

Wir analysieren die mRNA aus Q10c:
- 11 UGA (Sec-Codons)
- 2 UAG (Pyl-Codons)
- 3 AUGA-Motive (mögliche SECIS-Signale)

Wir versuchen:
1. Eine Sekundaerstruktur-Vorhersage (Nussinov-Algorithmus)
2. Suche nach Quartet-Motif (GA-N-AAA)
3. Welches AUGA dirigiert welches UGA?
"""
import re

# mRNA aus Q10c (298 Basen)
# Wir lesen sie aus der Backtranslation
mrna = ''
BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)
codon_map = {
    'A': 'GCC', 'R': 'CGC', 'N': 'AAC', 'D': 'GAC', 'C': 'UGC',
    'E': 'GAG', 'Q': 'CAG', 'G': 'GGC', 'H': 'CAC', 'I': 'AUC',
    'L': 'CUG', 'K': 'AAG', 'M': 'AUG', 'F': 'UUC', 'P': 'CCG',
    'S': 'AGC', 'T': 'ACC', 'W': 'UGG', 'Y': 'UAC', 'V': 'GUG',
    'U': 'UGA', 'O': 'UAG', 'B': 'AAC', 'Z': 'CAG'
}
for aa in BURUMUT_FULL:
    mrna += codon_map[aa]

# Wichtig: 11 UGA-Sec-Positionen in mRNA:
# Codon-Position (0-indiziert): 1, 3, 5, 13, 15, 19, 24, 32, 46, 66, 80
# mRNA-Position (jedes Codon = 3 Basen): 3, 9, 15, 39, 45, 57, 72, 96, 138, 198, 240
sec_pos_mRNA = [3, 9, 15, 39, 45, 57, 72, 96, 138, 198, 240]
uazbe_sec = [96, 138, 198, 240]  # UAZBE-Positionen * 3
other_sec = [3, 9, 15, 39, 45, 57, 72]  # andere Sec
pyl_pos = [156, 258]  # O-Positionen * 3
auga_pos = [33, 159, 261]  # AUGA in mRNA

print("="*70)
print("Q12.1: SECIS-Element-Kandidaten in BURUMUT-mRNA")
print("="*70)
print(f"mRNA-Laenge: {len(mrna)} Basen")
print(f"UGA-Codons (Sec): {sec_pos_mRNA}")
print(f"  Davon an UAZBE-Pos: {uazbe_sec}")
print(f"  Andere: {other_sec}")
print(f"UAG-Codons (Pyl): {pyl_pos}")
print(f"AUGA-Motive (SECIS-Kandidaten): {auga_pos}")
print()

# 2. Welche SECIS dirigiert welche UGA?
print("="*70)
print("Q12.2: SECIS-UGA-Zuordnung")
print("="*70)
# In Eukaryoten gilt: SECIS dirigiert ALLE downstream UGA bis zum naechsten Stop
# Aber: BURUMUT hat mehrere SECIS-Kandidaten, die die UGA aufteilen

# Wir sortieren die AUGA-Positionen und teilen die UGA in Bereiche
for i, auga in enumerate(auga_pos):
    next_auga = auga_pos[i+1] if i+1 < len(auga_pos) else len(mrna)
    next_stop = None
    for sp in sorted(sec_pos_mRNA + pyl_pos + [len(mrna)]):
        if sp > auga and (next_stop is None or sp < next_stop):
            next_stop = sp
            break

    # UGA in diesem Bereich
    upstream = [u for u in sec_pos_mRNA if auga <= u < (next_auga if next_auga < len(mrna) else next_stop)]
    print(f"  SECIS-Kandidat #{i+1} an AUGA-Pos {auga} (mRNA):")
    print(f"    Sekundaerstruktur-Element: 5'-{mrna[max(0,auga-15):auga]}>>>AUGA<<<{mrna[auga+4:auga+19]}-3'")
    print(f"    Dirigiert Sec-Codons: {upstream}")

# 3. SECIS Quartet-Suche
print()
print("="*70)
print("Q12.3: SECIS-Quartet-Suche")
print("="*70)
# SECIS Quartett: AA-N6-AAA oder GA-N3-AAA
quartet_patterns = [
    ('AA-N6-AAA', r'AA[AUCG]{6}AAA'),
    ('GA-N3-AAA', r'GA[AUCG]{3}AAA'),
    ('GA-N(1-5)-AAA', r'GA[AUCG]{1,5}AAA'),
    ('AAR-AAA (mit R=Purin)', r'AA[AG]AAA'),
]

for name, pat in quartet_patterns:
    matches = list(re.finditer(pat, mrna))
    if matches:
        print(f"  {name}: {len(matches)} Treffer")
        for m in matches[:3]:
            print(f"    Pos {m.start()}: {mrna[m.start():m.end()]}")

# 4. Suche nach SECIS-Element direkt vor/nach AUGA
print()
print("="*70)
print("Q12.4: SECIS-Element-Strukturvorhersage")
print("="*70)
# In echten SECIS-Elementen ist die Struktur:
# 5' - [stem] - [apical loop mit AUGA + Quartet] - [stem] - 3'
# Wir suchen nach dieser Topologie

# In BURUMUT mRNA: 3 AUGA an Pos 33, 159, 261
# Kontext um jedes AUGA:
for i, auga in enumerate(auga_pos):
    # 30 Basen davor und danach
    ctx_before = mrna[max(0, auga-30):auga]
    ctx_after = mrna[auga+4:min(len(mrna), auga+34)]
    print(f"\n  SECIS #{i+1} an mRNA-Pos {auga}:")
    print(f"    5'-Kontext (30 nt): ...{ctx_before}")
    print(f"    AUGA-Motiv:            {mrna[auga:auga+4]}")
    print(f"    3'-Kontext (30 nt): {ctx_after}...")

# 5. Nussinov-Algorithmus vereinfacht
print()
print("="*70)
print("Q12.5: Nussinov-Sekundaerstruktur-Vorhersage (vereinfacht)")
print("="*70)
# RNA-Basenpaarung: A-U, G-C, G-U (wobble)
def can_pair(a, b):
    pairs = {('A','U'), ('U','A'), ('G','C'), ('C','G'), ('G','U'), ('U','G')}
    return (a, b) in pairs

def max_pairs(seq, i, j):
    """Maximale Anzahl Basenpaare in seq[i..j]."""
    if i >= j: return 0
    best = max_pairs(seq, i+1, j)  # i ist unpaired
    # Versuche i mit einem Partner k zu paaren
    for k in range(i+1, j+1):
        if can_pair(seq[i], seq[k]):
            inner = max_pairs(seq, i+1, k-1)
            rest = max_pairs(seq, k+1, j)
            best = max(best, inner + 1 + rest)
    return best

# Da Nussinov O(n^3) ist, hier nur fuer eine Auswahl
# Wir berechnen fuer jedes Fenster von 50 Basen
print("Lokale Sekundaerstruktur-Stabilitaet (Anzahl Basenpaare pro 50-nt-Fenster):")
window = 50
for i in range(0, len(mrna) - window, 20):
    subseq = mrna[i:i+window]
    n_pairs = max_pairs(subseq, 0, len(subseq)-1)
    print(f"  mRNA-Pos {i:3d}-{i+window:3d}: {n_pairs} Basenpaare ({n_pairs/window*100:.0f}%)")

# 6. Was wenn 11 UGA SECIS-unabhaengig sind?
print()
print("="*70)
print("Q12.6: Sind BURUMUTs 11 UGA SECIS-unabhaengig?")
print("="*70)
# In Prokaryoten (E. coli) gibt es KEIN SECIS-Element.
# Stattdessen wird Sec direkt durch SELB-Protein erkannt
# (das an ein spezifisches mRNA-Haarnadel-Element bindet, das nahe am UGA ist).

# In BURUMUT: 11 UGA + nur 3 AUGA-Motive
# Vielleicht: 11 UGA sind 11 unabhaengige Sec-Insertions-Stellen

# In SelenoP (menschlich): 10 UGA, 2 SECIS-Elemente
# In GPx4: 1 UGA, 1 SECIS
# In BURUMUT: 11 UGA, 3 SECIS-Kandidaten

# Verhaeltnis: 11 UGA / 3 SECIS = 3.67 UGA pro SECIS
# In SelenoP: 10/2 = 5 UGA pro SECIS
# In BURUMUT ist das Verhaeltnis niedriger (mehr SECIS pro UGA)
print(f"  BURUMUT: 11 UGA / 3 AUGA = {11/3:.2f} UGA pro SECIS-Kandidat")
print(f"  Vergleich SelenoP: 10 UGA / 2 SECIS = {10/2:.2f}")
print(f"  Vergleich GPx4: 1 UGA / 1 SECIS = 1.0")
print()
print("Falls BURUMUT ein echtes Protein ist, hat es eine der dichtesten")
print("Sec-Insertions-Mechanismen die je gefunden wurden.")
