"""
ECHTE NCBI-BLAST-SUCHE

BURUMUT (99 AS, 11.1% Sec) gegen:
1. NCBI nr (non-redundant protein database)
2. UniProtKB / Swiss-Prot

Da BLAST ueber WebFetch zu langsam ist, nutzen wir:
- EBI Proteins API fuer Protein-Listen
- NCBI Entrez API fuer Sequenz-Abfragen
"""
import requests
import json
import time

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# In IUPAC-Standard-Code umwandeln
# BURUMUT enthaelt Sec (U), Pyl (O), Asx (B), Glx (Z)
# Standard-BLAST akzeptiert diese nicht direkt
# Wir nutzen C statt U, K statt O fuer BLAST-Suche
BURUMUT_BLAST = BURUMUT_FULL.replace('U', 'C').replace('O', 'K').replace('B', 'N').replace('Z', 'Q')
# C=Sec, K=Pyl, N=Asn (Asx), Q=Gln (Glx)

print("="*70)
print("NCBI BLAST - ECHTE INTERNET-SUCHE")
print("="*70)
print(f"BURUMUT (original): {BURUMUT_FULL}")
print(f"BURUMUT (fuer BLAST): {BURUMUT_BLAST}")
print(f"Laenge: {len(BURUMUT_BLAST)} AS")
print()

# 1. NCBI BLAST URL-Submission
# Format: BLAST FASTA-like ueber URL
query_fasta = f">BURUMUT\n{BURUMUT_BLAST}"
print("1. NCBI BLAST-Webserver (URL-Format):")
print(f"  URL-Format: 'https://blast.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-...'")
print(f"  Query: {query_fasta[:60]}...")

# 2. EBI BLAST REST API
print()
print("2. EBI BLAST REST API:")
try:
    # EBI BLAST URL
    ebi_url = "https://www.ebi.ac.uk/Tools/services/rest/ncbiblast"
    # Submit job
    fasta_seq = f">BURUMUT_hypothetical\n{BURUMUT_BLAST}"
    data = {
        'email': 'phi.mind@tengri137.local',
        'program': 'blastp',
        'database': 'uniprotkb',
        'stype': 'protein',
        'sequence': BURUMUT_BLAST,
    }
    response = requests.post(ebi_url + '/run', data=data, timeout=30)
    if response.status_code == 200:
        job_id = response.text.strip()
        print(f"  Job-ID: {job_id}")
        # Poll fuer Status
        for _ in range(5):
            time.sleep(2)
            status = requests.get(f"{ebi_url}/status/{job_id}", timeout=10)
            if status.text.strip() == 'FINISHED':
                # Ergebnis abrufen
                result = requests.get(f"{ebi_url}/result/{job_id}/xml", timeout=30)
                print(f"  Result XML: {len(result.text)} Zeichen")
                # Speichere Ergebnis
                with open("sources/blast_analysis/ncbi_result.xml", "w") as f:
                    f.write(result.text)
                print(f"  Ergebnis gespeichert in ncbi_result.xml")
                break
            else:
                print(f"  Status: {status.text.strip()}")
    else:
        print(f"  Fehler: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
except Exception as e:
    print(f"  Fehler: {e}")
