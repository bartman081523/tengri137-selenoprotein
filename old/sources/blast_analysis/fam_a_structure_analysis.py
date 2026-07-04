"""Detaillierte Analyse der A0AAV4C3M3 3D-Struktur"""
import requests

# PDB-URL
pdb_url = "https://alphafold.ebi.ac.uk/files/AF-A0AAV4C3M3-F1-model_v6.pdb"
response = requests.get(pdb_url, timeout=60)
pdb_text = response.text

# Parse
pdb_lines = pdb_text.split('\n')

# Sekundärstruktur
helix_count = sum(1 for l in pdb_lines if l.startswith('HELIX'))
sheet_count = sum(1 for l in pdb_lines if l.startswith('SHEET'))
print(f"Sekundärstruktur-Einträge in A0AAV4C3M3:")
print(f"  Helices: {helix_count}")
print(f"  Sheets: {sheet_count}")

# pLDDT
residues = {}
for line in pdb_lines:
    if line.startswith('ATOM'):
        try:
            resi = int(line[22:26].strip())
            bfactor = float(line[60:66].strip())
            if resi not in residues:
                residues[resi] = bfactor
        except:
            pass

# Region-spezifisches pLDDT
print()
print("pLDDT-Score pro Region:")
for region_name, start, end in [
    ('BURUMUTREFAMTU (1-14)', 1, 14),
    ('MRC-Repeat 1 (15-25)', 15, 25),
    ('MRC-Repeat 2 (26-37)', 26, 37),
    ('MRC-Repeat 3 (38-49)', 38, 49),
    ('C-terminal (50-99)', 50, 99),
    ('TRANSMEM (117-150)', 117, 150),
    ('C-term (199-209)', 199, 209),
]:
    region_plddt = [bf for ri, bf in residues.items() if start <= ri <= end]
    if region_plddt:
        avg = sum(region_plddt) / len(region_plddt)
        print(f"  {region_name} (Pos {start}-{end}): pLDDT = {avg:.2f} (n={len(region_plddt)})")

# Sekundärstruktur
print()
print("Sekundärstruktur-Details (Helices):")
helices = [l for l in pdb_lines if l.startswith('HELIX')][:10]
for h in helices:
    # Format: HELIX    1  H1 ALA A    1  ALA A    9  1                                  9
    parts = h.split()
    if len(parts) >= 8:
        helix_id = parts[1]
        start_res = parts[5] if len(parts) > 5 else '?'
        end_res = parts[8] if len(parts) > 8 else '?'
        print(f"  {helix_id}: {start_res} -> {end_res}")

# Sekundärstruktur in den ersten 50 AS
print()
print("Sekundärstruktur-Annotationen in den ersten 50 AS:")
helix_in_first_50 = [l for l in pdb_lines if l.startswith('HELIX') and int(l[21:25].strip()) <= 50]
for h in helix_in_first_50[:5]:
    print(f"  {h[:80]}")

# Welche AS sind in der Struktur?
seq_in_structure = ''
last_resi = 0
for line in pdb_lines:
    if line.startswith('ATOM'):
        try:
            resi = int(line[22:26].strip())
            if resi != last_resi:
                resname = line[17:20].strip()
                aa3_to_1 = {
                    'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F',
                    'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L',
                    'MET': 'M', 'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R',
                    'SER': 'S', 'THR': 'T', 'VAL': 'V', 'TRP': 'W', 'TYR': 'Y',
                }
                if resname in aa3_to_1:
                    seq_in_structure += aa3_to_1[resname]
                    last_resi = resi
        except:
            pass

print()
print(f"A0AAV4C3M3-Sequenz in PDB: {seq_in_structure}")
print(f"Laenge: {len(seq_in_structure)} AS")

# BURUMUT-Mapping
BURUMUT_MAPPED = 'NCRCMCTREFAMTCNCRESCTREGCMFAYAPSCAQNEHIMLAQANRCAQNENKMNAMQHQRSANLRCAQNEHIMLAQANRCAQNENKMNARAQHQRSAN'
print(f"BURUMUT (gemappt): {BURUMUT_MAPPED}")
print()

# Suche BURUMUT-ähnliche Subsequenzen
match_14 = 0
for i in range(min(14, len(seq_in_structure))):
    if i < len(BURUMUT_MAPPED) and seq_in_structure[i] == BURUMUT_MAPPED[i]:
        match_14 += 1
print(f"Identitaet (erste 14 AS): {match_14}/14 = {match_14/14*100:.1f}%")

# Position 32 = UAZBE-Position in BURUMUT
# Suche nach UAZBE in A0AAV4C3M3-Sequenz
fam_seq = seq_in_structure
if 'MRCPEDKH' in fam_seq:
    print(f"  A0AAV4C3M3 enthaelt 'MRCPEDKH' (BURUMUT-Vorspann-Pattern)")
    # Finde alle Vorkommen
    for i in range(len(fam_seq) - 7):
        if fam_seq[i:i+8] == 'MRCPEDKH':
            print(f"    Vorkommen bei Position {i+1}")

# Speichere die PDB-Datei
with open("sources/blast_analysis/A0AAV4C3M3_alphafold.pdb", "w") as f:
    f.write(pdb_text)
print()
print(f"PDB gespeichert in A0AAV4C3M3_alphafold.pdb ({len(pdb_text)} Zeichen)")
