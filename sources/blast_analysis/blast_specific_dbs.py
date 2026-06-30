"""
BLAST gegen spezifische Datenbanken:
- Selenocysteine-spezifische Proteine
- Adhesion-GPCR Familie
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

# BLAST gegen Swiss-Prot (kuratierte, höhere Spezifitaet)
print("="*70)
print("BLAST gegen Swiss-Prot (kuratierte Datenbank)")
print("="*70)

url = "https://www.ebi.ac.uk/Tools/services/rest/ncbiblast"
data = {
    'email': 'phimind.tengri137@example.org',
    'program': 'blastp',
    'database': 'uniprotkb_swissprot',
    'stype': 'protein',
    'sequence': BURUMUT_BLAST,
}

response = requests.post(f"{url}/run", data=data, timeout=30)
if response.status_code == 200:
    job_id = response.text.strip()
    print(f"Job-ID: {job_id}")
    for _ in range(60):
        time.sleep(2)
        status = requests.get(f"{url}/status/{job_id}", timeout=10)
        if status.text.strip() == 'FINISHED':
            result = requests.get(f"{url}/result/{job_id}/out", timeout=30)
            with open("sources/blast_analysis/ebi_swissprot_out.txt", "w") as f:
                f.write(result.text)
            # Parse
            for line in result.text.split('\n'):
                if line.startswith('sp:') or line.startswith('tr:'):
                    print(f"  {line[:130]}")
            break
        elif status.text.strip().startswith('ERROR'):
            print("ERROR")
            break
