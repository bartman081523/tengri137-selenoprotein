"""
BLAST Top-Hits Detailanalyse

Wir holen die vollstaendigen Sequenzen der Top-2 Hits und vergleichen
sie mit BURUMUT.
"""
import requests
import re

# Top-2 Hits: A0A1I3K752 (Treponema) und A0ACC2F027 (Dallia)
# UniProt IDs

def fetch_uniprot_sequence(accession):
    """Holt Protein-Sequenz von UniProt."""
    try:
        # EBI Proteins API
        url = f"https://www.ebi.ac.uk/proteins/api/proteins/{accession}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            seq = data.get('sequence', {}).get('version', '')
            if not seq:
                seq = data.get('sequence', {}).get('sequence', '')
            return data.get('protein', {}).get('submittedName', [{}])[0].get('fullName', {}).get('value', 'unknown'), seq
    except Exception as e:
        print(f"  Fehler: {e}")
    return None, None

# NCBI Entrez fuer Sequenz
def fetch_ncbi_sequence(accession):
    """Holt Sequenz via NCBI Entrez API."""
    try:
        # Versuche EBI
        url = f"https://www.ebi.ac.uk/proteins/api/proteins/{accession}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            seq = data.get('sequence', {}).get('sequence', '')
            name = data.get('protein', {}).get('recommendedName', {}).get('fullName', {}).get('value', '?')
            if not name:
                name = data.get('protein', {}).get('submittedName', [{}])[0].get('fullName', {}).get('value', '?')
            return name, seq
    except Exception as e:
        print(f"  Fehler: {e}")
    return None, None

print("="*70)
print("BLAST TOP-HITS: Echte Sequenzen von UniProt/EBI")
print("="*70)

# Top-2 Hits holen
top_hits = ['A0A1I3K752', 'A0ACC2F027']
for acc in top_hits:
    print(f"\n--- {acc} ---")
    name, seq = fetch_ncbi_sequence(acc)
    if name:
        print(f"Name: {name}")
    if seq:
        print(f"Laenge: {len(seq)} AS")
        print(f"Erste 60 AS: {seq[:60]}")
        # Suche nach Sec-Motiv
        if 'C' in seq[:30] or 'U' in seq[:30]:
            print("  -> Enthaelt Cys in den ersten 30 AS (Sec-Hinweis!)")
    else:
        print("  Sequenz nicht verfuegbar")

# Vergleich BURUMUT vs Top-Hits
BURUMUT_BLAST = ("BURUMUTREFAMTUNURESUTREGUMFAYAPSUAZBEHIMLAZANRUAZBENOMBA"
                 "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN")
BURUMUT_BLAST = BURUMUT_BLAST.replace('U', 'C').replace('O', 'K').replace('B', 'N').replace('Z', 'Q')

print()
print("="*70)
print("BLAST Top-Hit Alignment (BURUMUT vs A0A1I3K752)")
print("="*70)
print(f"BURUMUT: {BURUMUT_BLAST}")
print(f"        (99 AS, 11 Sec)")
