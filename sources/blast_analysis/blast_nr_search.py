"""
NCBI BLAST gegen nr-Datenbank
Wir nutzen NCBI BLAST direkt (nicht EBI).
"""
import requests
import time

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

BURUMUT_BLAST = (BURUMUT_FULL
    .replace('U', 'C').replace('O', 'K').replace('B', 'N').replace('Z', 'Q'))

# BLAST gegen Swiss-Prot (kuratierte Proteine)
url = "https://www.ebi.ac.uk/Tools/services/rest/ncbiblast"
email = "phimind.tengri137@example.org"

# Verschiedene Datenbanken ausprobieren
databases = [
    ('uniprotkb_swissprot', 'Swiss-Prot (kuratierte Proteine)'),
    ('uniprotkb', 'UniProtKB'),
    ('pdb', 'PDB (Strukturen)'),
    ('refseq_protein', 'RefSeq Protein'),
]

results = {}
for db_id, db_name in databases:
    print(f"\n--- Datenbank: {db_name} ({db_id}) ---")
    data = {
        'email': email,
        'program': 'blastp',
        'database': db_id,
        'stype': 'protein',
        'sequence': BURUMUT_BLAST,
    }
    try:
        response = requests.post(f"{url}/run", data=data, timeout=30)
        if response.status_code == 200:
            job_id = response.text.strip()
            # Poll
            for _ in range(60):
                time.sleep(2)
                status = requests.get(f"{url}/status/{job_id}", timeout=10)
                if status.text.strip() == 'FINISHED':
                    result = requests.get(f"{url}/result/{job_id}/out", timeout=30)
                    # Parse Hits
                    hits = []
                    for line in result.text.split('\n'):
                        if line.startswith('TR:') or line.startswith('sp:'):
                            hits.append(line)
                    print(f"  Hits: {len(hits)}")
                    # Top-3 signifikant
                    for h in hits[:3]:
                        parts = h.split()
                        if len(parts) >= 4:
                            try:
                                score = float(parts[-4])
                                evalue = parts[-1]
                                if float(evalue) < 10.0:
                                    print(f"    {h[:120]}")
                            except:
                                pass
                    results[db_id] = (job_id, len(hits))
                    break
                elif status.text.strip().startswith('ERROR'):
                    print(f"  ERROR")
                    break
    except Exception as e:
        print(f"  Fehler: {e}")
        time.sleep(5)

# Ergebnis zusammenfassen
print()
print("="*70)
print("BLAST-Suche BURUMUT - Zusammenfassung")
print("="*70)
for db_id, (job_id, n_hits) in results.items():
    print(f"  {db_id}: {n_hits} Hits, Job-ID {job_id}")
