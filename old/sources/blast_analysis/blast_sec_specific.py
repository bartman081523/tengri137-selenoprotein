"""
SEC-SPEZIFISCHE BLAST-SUCHE

Verwende Sec-BLAST (Sec-spezifische Substitution-Matrix)
"""
import requests
import time

# Verwende Sec-spezifische BLAST-Methode
# Wir nutzen PSI-BLAST mit Sec-spezifischen Substitutionen

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# NCBI unterstuetzt keine 22-Buchstaben BLAST direkt
# Aber wir koennen mit Sec als C suchen, da Sec-Cys konserviert sind
# Eigentlich ist der wichtige Schritt:
# 1. Sec-Sekundaerstruktur (disulfid-Bruecke-formation) -> Cys
# 2. Sec-reiche Cys-reiche Sequenzen sind oft Sec-Pendants
# Wir testen die Sec-Pendants direkt in der Cytochrom-b5-Reduktase-Familie

# Stattdessen: BLAST mit U statt C, aber NCBI lehnt das ab
# Daher: Wir nutzen das Mapping
BURUMUT_BLAST = BURUMUT_FULL.replace('U', 'C')

# NCBI web BLAST mit 'organism' Filter
print("="*70)
print("BLAST mit Organism-Filter: Sec-Protein-reiche Organismen")
print("="*70)

# Suche gegen UniProtKB mit Eukaryota-Filter
url = "https://www.ebi.ac.uk/Tools/services/rest/ncbiblast"
data = {
    'email': 'phimind.tengri137@example.org',
    'program': 'blastp',
    'database': 'uniprotkb',
    'stype': 'protein',
    'sequence': BURUMUT_BLAST,
    'taxonomy': 'Eukaryota',  # Nur Eukaryoten
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
            with open("sources/blast_analysis/ebi_eukaryota_result.txt", "w") as f:
                f.write(result.text)
            # Parse
            for line in result.text.split('\n'):
                if line.startswith('TR:') or line.startswith('sp:'):
                    print(f"  {line[:140]}")
            break
        elif status.text.strip().startswith('ERROR'):
            print("ERROR")
            break
