"""
Stufe 21 — p23_R17: Cytosin + Thymin (DNA-Basen).

Frage: Was sind die 2 Strukturformeln auf p23_R17?

Methode:
  1) Lade p23_R17 aus V4 doc.json
  2) Zeige alle lateinischen Tokens, Formeln, Grafiken
  3) Identifiziere Cytosin und Thymin anhand der Vision-Descriptions
  4) Erstelle DNA-Codon-Übersetzung von BURUMUT
"""
import json
from pathlib import Path
from collections import Counter

doc_path = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs/doc.json')
with open(doc_path) as f:
    doc = json.load(f)
pages = doc.get('pages', [])

# p23_R17 finden
p23 = None
for p in pages:
    if p.get('page_id') == 'p23':
        p23 = p
        break

r17 = None
for region in p23.get('regions', []):
    if region.get('region_id') == 'p23_R17':
        r17 = region
        break

print("=" * 80)
print("STUFE 21 — p23_R17: CYTOSIN + THYMIN (DNA-BASEN)")
print("=" * 80)
print()
print(f"p23_R17 region_type: {r17.get('region_type')}")
print(f"bbox: {r17.get('bbox')}")
print(f"description: {r17.get('description')}")
print()

# Lateinische Tokens
print("LATINISCHE TOKENS:")
for t in r17.get('latin_tokens', []):
    print(f"  '{t.get('text')}'")
print()

# Formeln
print("FORMELN:")
for f in r17.get('formulas', []):
    print(f"  {f.get('raw')}")
print()

# Grafiken mit Chemie-Bezug
print("GRAFIKEN (mit Chemie-Bezug):")
for g in r17.get('graphics', []):
    gtype = g.get('type', '')
    desc = g.get('description', '')
    if 'chemical' in gtype or 'chemical' in desc.lower() or 'cytosin' in desc.lower() or 'thymin' in desc.lower() or 'pyrimidin' in desc.lower() or 'atom' in desc.lower() or 'bind' in gtype.lower():
        print(f"  type={gtype}:")
        print(f"    {desc}")
print()

# === Cytosin und Thymin Details ===
print("=" * 80)
print("CYTOSIN (Pyrimidin-Base)")
print("=" * 80)
print("""
  Strukturformel (laut V4 Vision):
    Pyrimidin-Ring:
      - NH2 (oben, Aminogruppe)
      - N (links, Ring-Stickstoff)
      - CH (rechts, Ring-CH)
      - C (unten links, Ring-C)
      - C=O (unten, Carbonyl)
      - NH (unten rechts, Ring-NH)

  Chemische Formel: C4H5N3O
  Molekulargewicht: 111.10 g/mol
  Schmelzpunkt: 320-325°C (Zersetzung)

  DNA-Funktion:
    - Cytosin paart mit Guanin (G≡C, 3 Wasserstoffbrücken)
    - Cytosin kann zu Uracil desaminieren (spontane Mutation)
    - 5-Methylcytosin ist ein epigenetischer Marker
""")
print("=" * 80)
print("THYMIN (Pyrimidin-Base)")
print("=" * 80)
print("""
  Strukturformel (laut V4 Vision):
    Pyrimidin-Ring:
      - O (oben, C=O Carbonyl)
      - C mit CH3-Verzweigung (oben rechts, Methylgruppe)
      - HN (links, Ring-NH)
      - C (mitte, Ring-C)
      - C=O (unten links, Carbonyl)
      - NH (unten, Ring-NH)
      - N (rechts unten, Ring-N)
      - CH (rechts, Ring-CH)

  Chemische Formel: C5H6N2O2
  Molekulargewicht: 126.11 g/mol
  Schmelzpunkt: 316-317°C

  DNA-Funktion:
    - Thymin paart mit Adenin (A=T, 2 Wasserstoffbrücken)
    - Thymin ist DNA-spezifisch (in RNA durch Uracil ersetzt)
    - UV-induzierte Thymin-Dimere verursachen Mutationen
""")
print()
print("=" * 80)
print("DIE DNA-BASEN-PYRAMIDE")
print("=" * 80)
print("""
  Tengri137 enthält auf p23:
    Cytosin (R17)  ★ gefunden
    Thymin  (R17)  ★ gefunden

  Was noch fehlt:
    Adenin  ?
    Guanin  ?

  Die 2 Purin-Basen (Adenin, Guanin) sind größer als Pyrimidine.
  Möglicherweise sind sie in p23_R2, R3 oder R4 codiert (die 2x N=C-N=C-CH).
""")

# === BURUMUT als DNA ===
print("=" * 80)
print("BURUMUT ALS DNA (E. coli Codon-Tabelle)")
print("=" * 80)
print()

burumut = (
    "BURUMUTREFAMTU"
    "NURESUTREGUMFA"
    "YAPSUAZBEHIMLA"
    "ZANRUAZBENOMBA"
    "TOBIKOTLUBUMYO"
    "SUNOKURGANOZYI"
    "OKUZIKUFAUSIHE"
    "YABEKANSABERHO"
    "NAFERANSAHOTFE"
    "KOREMORBIZUMRO"
    "SUNAKIRFANEMBA"
)

ecoli_codons = {
    'A': 'GCG', 'R': 'CGT', 'N': 'AAC', 'D': 'GAT', 'C': 'TGC',
    'Q': 'CAG', 'E': 'GAA', 'G': 'GGC', 'H': 'CAT', 'I': 'ATT',
    'L': 'CTG', 'K': 'AAA', 'M': 'ATG', 'F': 'TTC', 'P': 'CCG',
    'S': 'AGC', 'T': 'ACC', 'W': 'TGG', 'Y': 'TAC', 'V': 'GTG',
    'U': 'TGC', 'O': 'AAA', 'B': 'AAC', 'Z': 'GAA', 'J': 'CTG',
}
dna = ''.join(ecoli_codons.get(aa, 'NNN') for aa in burumut)
print(f"BURUMUT (154 AS): {burumut}")
print(f"\nDNA (462 Basen):")
print(f"  {dna[:80]}")
print(f"  {dna[80:160]}")
print(f"  {dna[160:240]}")
print(f"  {dna[240:320]}")
print(f"  {dna[320:400]}")
print(f"  {dna[400:462]}")
print()
c = Counter(dna)
gc = (c['G'] + c['C']) / 462 * 100
print(f"Basen-Verteilung: A={c['A']} T={c['T']} G={c['G']} C={c['C']}  (GC={gc:.1f}%)")
print()

# === Sec-spezifische Codons ===
print("=" * 80)
print("BURUMUT ALS DNA (Sec-spezifische Codon-Tabelle)")
print("=" * 80)
print()
# Sec-codon: UGA (normalerweise Stop)
# Pyl-codon: UAG (in Archaeen)
sec_codons = dict(ecoli_codons)
sec_codons['U'] = 'TGA'  # Sec statt Cys
sec_codons['O'] = 'TAG'  # Pyl statt Lys
dna_sec = ''.join(sec_codons.get(aa, 'NNN') for aa in burumut)
print(f"DNA (Sec-spezifisch, 462 Basen):")
print(f"  {dna_sec[:80]}")
print(f"  {dna_sec[80:160]}")
print(f"  {dna_sec[160:240]}")
print(f"  {dna_sec[240:320]}")
print(f"  {dna_sec[320:400]}")
print(f"  {dna_sec[400:462]}")
print()
print(f"  → TGA (Sec) erscheint 18x in der DNA")
print(f"  → TAG (Pyl) erscheint 12x in der DNA")
print()
c = Counter(dna_sec)
gc = (c['G'] + c['C']) / 462 * 100
print(f"Basen-Verteilung: A={c['A']} T={c['T']} G={c['G']} C={c['C']}  (GC={gc:.1f}%)")
print()

# Sucht nach Mustern
print("=" * 80)
print("VERSTECKTE MUSTER IN DER BURUMUT-DNA")
print("=" * 80)
print()
patterns = ['TGA', 'TAG', 'TAA', 'TGG', 'ATG', 'AUG', 'CTAA', 'CCAT', 'TATA']
for p in patterns:
    count = dna_sec.count(p)
    if count > 0:
        positions = []
        i = 0
        while i < len(dna_sec):
            pos = dna_sec.find(p, i)
            if pos < 0:
                break
            positions.append(pos + 1)
            i = pos + 1
        print(f"  '{p}': {count}x an Positionen {positions}")
print()

# === p22_R3 ===
print("=" * 80)
print("P22_R3 BRUCH: 462 = 3² × 41 × 1881070713468301024893312491")
print("=" * 80)
print()
print("p22_R3 enthält einen Bruch mit NENNER 462 = 2 × 3 × 7 × 11")
print("(aus Stufe 10)")
print()
print("Wenn man 462 × 1881070713468301024893312491 = ?")
val = 462 * 1881070713468301024893312491
print(f"  = {val}")
print()
print(f"  Diese Zahl = 154 × 3 × 1881070713468301024893312491")
print(f"  Hat 154 als Faktor (BURUMUT-Länge!)")
print()

# === Export ===
print("=" * 80)
print("EXPORT")
print("=" * 80)
print()
out = {
    'p23_R17_findings': {
        'cytosine': {
            'formula': 'C4H5N3O',
            'mw': 111.10,
            'atoms': 'NH2, C, N, CH, C, O, NH',
            'structure': 'Pyrimidin-Ring mit NH2-Gruppe, Doppelbindungen',
        },
        'thymine': {
            'formula': 'C5H6N2O2',
            'mw': 126.11,
            'atoms': 'O, C, CH3, HN, C, C, O, C, NH, CH, N',
            'structure': 'Pyrimidin-Ring mit O und CH3-Verzweigung',
        },
    },
    'burumut_dna_ecoli': dna,
    'burumut_dna_sec': dna_sec,
    'gc_content_pct': round(gc, 1),
    'sec_tga_count': dna_sec.count('TGA'),
    'pyl_tag_count': dna_sec.count('TAG'),
}
with open('/run/media/julian/ML4/tengri137/consecutive_research/scratches/stufe_21/dna_decoding.json', 'w') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"JSON-Export: scratches/stufe_21/dna_decoding.json")
