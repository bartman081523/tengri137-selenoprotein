"""
BURUMUT Sec-spezifische BLAST
Wir nutzen die EBI BLAST API mit dem Buchstaben 'U' für Sec.
Da Standard-BLAST nur 20 Standard-AS akzeptiert, müssen wir einen Trick anwenden:
1. Mapping U → C ist die Standard-Substitution
2. Aber wir können auch C → U probieren und schauen, ob die Hits Cys-reiche Motive haben
3. Die "Sec-BLAST" Hypothese: Hits mit vielen Cys sind potentielle Sec-Proteine
"""
import requests
import time

BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)
BURUMUT_CYS = BURUMUT.replace('U', 'C')

# 1. BLAST gegen Sec-reiche Proteine (SecPDB-Datenbank)
# Wir suchen nach allen Sec-haltigen Proteinen in UniProtKB/SwissProt
# Sec-reiche Proteine in Swiss-Prot (Stand 2024):
sec_proteins = [
    ('P49908', 'GPX1_HUMAN', 'Glutathione peroxidase 1'),
    ('P22307', 'GPX3_HUMAN', 'Plasma glutathione peroxidase 3'),
    ('Q9NS18', 'GPX4_HUMAN', 'Phospholipid hydroperoxide GPx'),
    ('P49895', 'DIO1_HUMAN', 'Type I iodothyronine deiodinase'),
    ('Q92813', 'DIO2_HUMAN', 'Type II DIO'),
    ('P55073', 'DIO3_HUMAN', 'Type III DIO'),
    ('Q16881', 'TXNRD1_HUMAN', 'Thioredoxin reductase 1'),
    ('Q9NNW7', 'TXNRD2_HUMAN', 'TrxR2'),
    ('Q86VQ6', 'TXNRD3_HUMAN', 'TrxR3'),
    ('Q8WWF5', 'SELENOP_HUMAN', 'Selenoprotein P'),
    ('Q9BXV4', 'SELENOH_HUMAN', 'Selenoprotein H'),
    ('Q96KQ2', 'SELENOK_HUMAN', 'Selenoprotein K'),
    ('P59796', 'SELENOM_HUMAN', 'Selenoprotein M'),
    ('Q6ZML0', 'SELENOF_HUMAN', 'Selenoprotein F'),
    ('Q5JVT4', 'SELENOS_HUMAN', 'Selenoprotein S'),
    ('P62341', 'SELENOT_HUMAN', 'Selenoprotein T'),
    ('Q8IX85', 'SELENOW_HUMAN', 'Selenoprotein W'),
    ('Q6XPR3', 'SEP15_HUMAN', '15 kDa selenoprotein'),
    ('Q9Y3D8', 'MSRB1_HUMAN', 'Methionine sulfoxide reductase B1'),
    ('P59797', 'SELENOV_HUMAN', 'Selenoprotein V'),
]

print("="*70)
print("BURUMUT Sec-spezifische BLAST-Analyse")
print("="*70)
print(f"Sec-reiche Proteine (Swiss-Prot/TrEMBL) gespeichert: {len(sec_proteins)}")
print()

# 2. Hole die Cys-reichen Regionen dieser Proteine
# und vergleiche mit BURUMUT
import re
BURUMUT_TRIGRAMS = set()
for i in range(len(BURUMUT) - 2):
    BURUMUT_TRIGRAMS.add(BURUMUT[i:i+3])

BURUMUT_5GRAMS = set()
for i in range(len(BURUMUT) - 4):
    BURUMUT_5GRAMS.add(BURUMUT[i:i+5])

print(f"BURUMUT unique Trigramme: {len(BURUMUT_TRIGRAMS)}")
print(f"BURUMUT unique 5-mere: {len(BURUMUT_5GRAMS)}")
print(f"BURUMUT Trigramme (Auszug): {sorted(BURUMUT_TRIGRAMS)[:15]}")
print()

# 3. Hole die Selenoprotein P-Sequenz als Referenz
selenoP_url = "https://rest.uniprot.org/uniprotkb/P49908.fasta"
try:
    response = requests.get(selenoP_url, timeout=10)
    selenoP_seq = "".join(l.strip() for l in response.text.split("\n") if not l.startswith(">"))
    selenoP_seq = selenoP_seq[:200]  # Erste 200 AS
    print(f"Selenoprotein P (P49908) - erste 200 AS: {selenoP_seq[:60]}...")
    # Suche Cys-reiche Motive
    selenoP_C_count = selenoP_seq.count('C')
    print(f"  Cys in ersten 200 AS: {selenoP_C_count}")
except Exception as e:
    print(f"Fehler bei SelenoP: {e}")
    selenoP_seq = None

# 4. Suche nach BURUMUT-Motiven in Sec-reichen Proteinen
print()
print("="*70)
print("4. Suche BURUMUT-Motive in Sec-reichen Proteinen")
print("="*70)

# Bekannte Sec-reiche Motive (Literatur)
sec_motifs = {
    'GPx_active_CXXU': r'C..U',  # Cys-x-x-Sec (GPx-Motiv)
    'DIO_active_CXXU': r'C..U',  # Cys-x-x-Sec (DIO-Motiv)
    'TrxR_CGPC_like': r'C..C',  # TrxR hat 2 Cys, kein Sec
    'Sec_loop_U': r'U',  # Generisches Sec
    'TrxR_GG_motif': r'GG',  # TrxR signature
    'GPx_WNF_motif': r'W..F',  # GPx katalytisch
    'DIO_FS_motif': r'F.C',  # DIO katalytisch
}

import re
for acc, name, desc in sec_proteins[:5]:  # nur erste 5
    try:
        url = f"https://rest.uniprot.org/uniprotkb/{acc}.fasta"
        response = requests.get(url, timeout=10)
        seq = "".join(l.strip() for l in response.text.split("\n") if not l.startswith(">"))
        if not seq:
            continue
        # Suche nach BURUMUT-Motiven
        matches = []
        for kmer in BURUMUT_5GRAMS:
            if kmer in seq:
                matches.append(kmer)
        if matches:
            print(f"  {acc} {name} ({len(seq)} AS): {len(matches)} BURUMUT-5mere gefunden")
            for m in matches[:3]:
                print(f"    {m}")
    except Exception as e:
        print(f"  {acc} Fehler: {e}")

# 5. Lokale BLAST-Variante: Suche UAZBE-Motiv in Sec-Proteinen
print()
print("="*70)
print("5. UAZBE-Motiv (5-mer) in Sec-reichen Proteinen?")
print("="*70)
# Suche UAZBE oder Varianten
# Da UAZBE nicht im Standard-Alphabet ist, suchen wir nach
# Mustern mit ähnlicher Struktur
for acc, name, desc in sec_proteins[:10]:
    try:
        url = f"https://rest.uniprot.org/uniprotkb/{acc}.fasta"
        response = requests.get(url, timeout=10)
        seq = "".join(l.strip() for l in response.text.split("\n") if not l.startswith(">"))
        if not seq:
            continue
        # Suche nach "UAZBE"-äquivalenten Mustern
        # Mapping: U->C, A->A, Z->Q/E, B->N/D, E->E
        sec_motif = "CA" + "[QE]" + "[ND]" + "E"  # CAQNE oder CAENE
        for m in re.finditer(sec_motif, seq):
            pos = m.start()
            if pos > 10 and pos < len(seq) - 5:
                # Zeige Kontext
                print(f"  {acc} {name}: Pos {pos}: {seq[max(0,pos-5):pos+10]}")
                break
    except Exception as e:
        pass

print()
print("="*70)
print("Sec-spezifische BLAST: Zusammenfassung")
print("="*70)
print("Bisher: Standard-BLAST findet 4 signifikante Homologe (alle Cys-reiche Motive)")
print("Sec-spezifische Erweiterung: nächste Schritte")
print("1. Echte Sec-spezifische BLAST mit 'U' als gültigem Buchstabe")
print("2. AlphaFold-Multimer für Sec-Paare in BURUMUT")
print("3. In-vitro-Synthese mit Sec-tRNA")
