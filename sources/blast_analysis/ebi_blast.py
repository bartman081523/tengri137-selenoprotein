"""
EBI BLAST REST API - korrekte Verwendung
"""
import requests
import time

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# Mapping fuer BLAST: Sec->C, Pyl->K, Asx->N, Glx->Q
BURUMUT_BLAST = (BURUMUT_FULL
    .replace('U', 'C')  # Sec
    .replace('O', 'K')  # Pyl
    .replace('B', 'N')  # Asx
    .replace('Z', 'Q'))  # Glx

print("="*70)
print("EBI BLAST SUCHE - BURUMUT vs UniProtKB")
print("="*70)
print(f"Query: {BURUMUT_BLAST}")
print(f"Laenge: {len(BURUMUT_BLAST)} AS")
print()

# EBI BLAST REST
url = "https://www.ebi.ac.uk/Tools/services/rest/ncbiblast"
email = "phimind.tengri137@example.org"  # Gültiges E-Mail-Format

try:
    data = {
        'email': email,
        'program': 'blastp',
        'database': 'uniprotkb',
        'stype': 'protein',
        'sequence': BURUMUT_BLAST,
    }
    print(f"Submitting to EBI BLAST...")
    response = requests.post(f"{url}/run", data=data, timeout=30)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        job_id = response.text.strip()
        print(f"Job-ID: {job_id}")
        # Poll fuer Status
        for attempt in range(20):
            time.sleep(3)
            status = requests.get(f"{url}/status/{job_id}", timeout=10)
            current_status = status.text.strip()
            print(f"  Status check {attempt+1}: {current_status}")
            if current_status == 'FINISHED':
                # Ergebnis abrufen
                result = requests.get(f"{url}/result/{job_id}/xml", timeout=30)
                print(f"Result: {len(result.text)} Zeichen XML")
                with open("sources/blast_analysis/ebi_blast_result.xml", "w") as f:
                    f.write(result.text)
                # Parse Ergebnisse
                import xml.etree.ElementTree as ET
                root = ET.fromstring(result.text)
                hits = root.findall('.//{*}Hit')
                print(f"\nAnzahl Hits: {len(hits)}")
                for i, hit in enumerate(hits[:10]):
                    acc = hit.find('.//{*}Hit_accession')
                    desc = hit.find('.//{*}Hit_def')
                    evalue = hit.find('.//{*}Hsp_evalue')
                    score = hit.find('.//{*}Hsp_score')
                    if acc is not None and desc is not None:
                        print(f"  {i+1}. {acc.text}: {desc.text[:60]}... e={evalue.text if evalue is not None else '?'}")
                break
            elif current_status.startswith('ERROR'):
                print(f"  ERROR")
                break
    else:
        print(f"Response: {response.text[:300]}")
except Exception as e:
    print(f"Exception: {e}")
