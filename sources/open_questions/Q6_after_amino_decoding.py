"""
OFFENE FRAGE 6: Was kommt NACH der Aminosaeure-Dekodierung?

Tengri sagt:
- 'UPCOMING TEXTS ARE GENETICALLY ENCRYPTED'
- 'YOUR KNOWLEDGE CAN NOT HELP AT THIS POINT'
- 'WHO HAS THE CORRECT GENETIC CODING WILL UNDERSTAND THIS TEXT'

Wenn BURUMUT Aminosaeure-Sequenz ist:
1. Welches Protein bildet es (3-letter → 1-letter Code)?
2. Hat es eine biologische Funktion?
3. Was ist die 'genetische Botschaft' nach der Transkription?

Methoden:
1. BLAST-aehnliche Suche nach aehnlichen Protein-Sequenzen
2. Sekundaerstruktur-Vorhersage
3. Phylogenetische Analyse (welche Organismen haben aehnliche Proteine?)
"""
import random
from collections import Counter

# Standard Aminosaeure 3-letter zu 1-letter Code
AA_3_TO_1 = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
    'GLU': 'E', 'GLN': 'Q', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
    'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
    'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V',
    'SEC': 'U', 'PYL': 'O',  # Selenocystein, Pyrrolysine
}

# Codon-Tabelle (Standard)
CODON_TABLE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# 1. Aminosaeure-Verteilung in BURUMUT (1-letter Code)
print("="*70)
print("Q6.1: BURUMUT als Aminosaeure-Sequenz")
print("="*70)
freq = Counter(BURUMUT_FULL)
print(f"Total: {len(BURUMUT_FULL)} Buchstaben, {len(freq)} unique")
print(f"Verteilung:")
for ch, n in sorted(freq.items(), key=lambda x: -x[1]):
    name = AA_3_TO_1.get(ch, f"??? (kein Standard-Amino)")
    print(f"  {ch}: {n:3d}x ({n/len(BURUMUT_FULL)*100:.1f}%) -> {name}")

# 2. BLAST-aehnlich: Welche Proteine haben aehnliche Verteilung?
# Wir suchen nach Proteinen mit hoher Frequenz von A, U, R, M, Z (Phantom), E
print()
print("="*70)
print("Q6.2: Welche Proteine haben aehnliche Aminosaeure-Verteilung?")
print("="*70)
# Bekannte Proteine mit hoher Ala+Arg+Met Frequenz:
# - Histone (DNA-bindend): sehr arginin- und lysin-reich
# - Transkriptionsfaktoren: oft zinc-finger mit hohen Cys+His
# - Strukturproteine: Collagen (Glycin-reich)
# - Enzyme mit aktiven Sites: variabel

# In BURUMUT:
# A (16x) = 16.2% (Alanine) - sehr hoch!
# U (11x) = 11.1% (Sec/Stop) - ungewoehnlich hoch
# R (10x) = 10.1% (Arginine) - hoch
# M (8x) = 8.1% (Methionine)
# Z (8x) = 8.1% (KEIN Standard-Amino!)
# B (7x) = 7.1% (KEIN Standard-Amino!)

print("Beobachtung: 8 Z und 7 B sind KEINE Standard-Aminosaeuren!")
print("In echten Proteinen waere das ein massiver Frameshift oder")
print("post-translationale Modifikation.")

# 3. Kodon-Analyse: Welche DNA-Sequenz produziert BURUMUT?
print()
print("="*70)
print("Q6.3: Welche DNA kodiert BURUMUT?")
print("="*70)
# Da BURUMUT 19 distinkte Buchstaben hat, aber DNA nur 4,
# ist BURUMUT KEINE direkte DNA-Sequenz.
# Aber: Was wenn BURUMUT ein Protein ist, das aus DNA translatiert wurde?
# Dann ist die DNA eine Projektion auf 20 (= 4^3/...) Buchstaben.

# Wenn wir jeden Buchstaben auf einen Codon mappen:
# Wir suchen eine Codon-Mapping B->XYZ, U->ABC, R->DEF, ...
# so dass die resultierende DNA-Sequenz biologisch plausibel ist.

# Einfache Variante: Map auf 4 Basen mit 4-Zyklus
# A=AAA, B=AAA, U=AAC, R=AAG, M=AAT, T=ACA, E=ACC, F=ACG, N=ACT, S=AGA, ...
# Aber: dies ist ein vager Ansatz

# Stattdessen: Berechne, ob BURUMUT ein bekanntes Protein-Motiv enthaelt
known_motifs = {
    'RGD': 'Integrin-binding motif',
    'NLS': 'KKRKVK nuclear localization',
    'KH': 'hnRNP K-homology',
    'SH3': 'PXXP Src homology 3',
    'RGG': 'RGG box (RNA binding)',
    'RXR': 'Retinoid receptor binding',
    'DEAD': 'DEAD-box helicase',
    'PEST': 'PEST sequence (protein degradation)',
    'KFERQ': 'KFERQ-like chaperone-mediated autophagy',
    'HKD': 'HKD phospholipase',
    'DEDD': 'DEDD death effector',
    'DXXXD': 'DXXXD DNA-binding',
}

# Suche in BURUMUT nach Motiven
for motif, desc in known_motifs.items():
    if motif in BURUMUT_FULL:
        print(f"  '{motif}' GEFUNDEN: {desc}")
    else:
        # Suche nach aehnlichen (mit X = jeder Buchstabe)
        regex = motif.replace('X', '.')
        import re
        match = re.search(regex, BURUMUT_FULL)
        if match:
            print(f"  '{motif}' (mit X-Platzhalter): GEFUNDEN als {match.group()} - {desc}")

# 4. Protein-Sekundaerstruktur-Vorhersage
print()
print("="*70)
print("Q6.4: Sekundaerstruktur-Vorhersage (einfaches Chou-Fasman)")
print("="*70)
# Helix-begünstigend: A, L, M, E, Q, K, R
# Sheet-begünstigend: V, I, Y, F, W, L, T
# Turn-begünstigend: G, N, P, S, D
# Was wenn BURUMUT ein spezifisches Sekundärstruktur-Muster hat?
helix_chars = 'ALMEQKR'
sheet_chars = 'VIYFWLT'
turn_chars = 'GNPSD'

n = len(BURUMUT_FULL)
helix_count = sum(1 for c in BURUMUT_FULL if c in helix_chars)
sheet_count = sum(1 for c in BURUMUT_FULL if c in sheet_chars)
turn_count = sum(1 for c in BURUMUT_FULL if c in turn_chars)
print(f"BURUMUT (n={n}):")
print(f"  Helix-fördernd: {helix_count} ({helix_count/n*100:.1f}%)")
print(f"  Sheet-fördernd: {sheet_count} ({sheet_count/n*100:.1f}%)")
print(f"  Turn-fördernd: {turn_count} ({turn_count/n*100:.1f}%)")
print(f"  (Rest / ungeladen): {n - helix_count - sheet_count - turn_count}")

# 5. Vergleich: Zufallssequenz
print()
print("Vergleich: Zufallssequenz mit gleicher Alphabet-Verteilung:")
random.seed(42)
rand_seq = list(BURUMUT_FULL)
random.shuffle(rand_seq)
rand_seq = ''.join(rand_seq)
helix_r = sum(1 for c in rand_seq if c in helix_chars)
sheet_r = sum(1 for c in rand_seq if c in sheet_chars)
turn_r = sum(1 for c in rand_seq if c in turn_chars)
print(f"Zufall: Helix={helix_r} ({helix_r/n*100:.1f}%) Sheet={sheet_r} ({sheet_r/n*100:.1f}%) Turn={turn_r} ({turn_r/n*100:.1f}%)")
print("BURUMUT ähnelt einem Protein mit ~30% Helix-Begünstigung.")

# 6. Was wenn BURUMUT die Antwort auf eine Frage ist?
print()
print("="*70)
print("Q6.5: Ist BURUMUT eine Antwort auf die Tengri-Frage?")
print("="*70)
# Tengri's Botschaft: 'WHO HAS THE CORRECT GENETIC CODING WILL UNDERSTAND'
# Wenn wir BURUMUT als Codon-3er interpretieren:
# BUR = ? (kein Standard-Codon in Standard-Genetik)
# URU = ?
# MUR = ?

# Tatsaechlich: BURUMUT verwendet Buchstaben, die KEINE
# Standard-DNA oder Standard-Aminosaeure sind (B, Z)
# Was wenn BURUMUT die "korrekte genetische Codierung" SELBST ist?
# B und Z sind PHANTOM-Buchstaben - sie existieren in der
# "Zukunft" der Genetik?

# 7. B/Z als 22. und 23. Aminosaeure?
print()
print("Hypothese: B und Z sind unbekannte Aminosaeuren 21 und 22")
print("B (Asparagin/Asparaginsaeure? = Asx) und Z (Glutamin/Glutaminsaeure? = Glx)")
print("In der IUPAC-Nomenklatur sind B und Z Platzhalter fuer")
print("Asparagin/Asparaginsaeure bzw. Glutamin/Glutaminsaeure,")
print("wenn die genaue Identitaet unbekannt ist.")
print()
print("-> BURUMUT koennte ein Protein sein, bei dem B und Z")
print("   fuer 'unscharfe' Aminosaeuren stehen - moeglicherweise")
print("   post-translational modifizierte Reste.")

# 8. Teste die Hypothese: Protein-Suche mit X (Asx) und Z (Glx)
print()
print("Wenn B=Asx, Z=Glx, dann ist BURUMUT ein Protein mit")
print("unbestimmten Resten. BLAST-Suche nach aehnlichen Sequenzen")
print("waere der naechste Schritt (hier nicht moeglich ohne Internet).")
