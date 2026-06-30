"""BURUMUT-AlphaFold2-Ähnliche Analyse mit ESM-2-Embeddings

Da AlphaFold2 eine komplette MSA braucht (Multi-Sequence-Alignment),
verwenden wir eine einfachere Methode:
- ESM-2-Embeddings als "Pseudo-MSA" (eine Sequenz)
- Analyse der Embedding-Ähnlichkeiten zwischen BURUMUT und A0AAV4C3M3
"""
import torch
import esm
import numpy as np
import requests

BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)
BURUMUT_CYS = BURUMUT.replace('U', 'C').replace('O', 'K').replace('B', 'N').replace('Z', 'Q')

# Lade A0AAV4C3M3-Sequenz von BLAST
print("Hole A0AAV4C3M3-Sequenz...")
r = requests.get(
    "https://rest.uniprot.org/uniprotkb/A0AAV4C3M3.fasta",
    timeout=15
)
fam_seq = ""
for line in r.text.split("\n"):
    if not line.startswith(">"):
        fam_seq += line.strip()
print(f"A0AAV4C3M3: {len(fam_seq)} AS")
print(f"A0AAV4C3M3-Sequenz: {fam_seq[:80]}...")

# Hole Embeddings für beide
device = torch.device('cuda')
print("\nLade ESM-2...")
model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
batch_converter = alphabet.get_batch_converter()
model = model.to(device)
model.eval()

data = [("BURUMUT", BURUMUT_CYS), ("A0AAV4C3M3", fam_seq)]
batch_labels, batch_strs, batch_tokens = batch_converter(data)
batch_tokens = batch_tokens.to(device)

with torch.no_grad():
    results = model(batch_tokens, repr_layers=[33], return_contacts=True)
embeddings = results["representations"][33]

burumut_emb = embeddings[0, 1:100, :].cpu().numpy()  # ohne BOS/EOS
fam_emb = embeddings[1, 1:210, :].cpu().numpy()

print(f"BURUMUT-Embeddings: {burumut_emb.shape}")
print(f"A0AAV4C3M3-Embeddings: {fam_emb.shape}")

# Paarweise Ähnlichkeit zwischen BURUMUT-Frames und A0AAV4C3M3-Frames
print("\nBerechne Ähnlichkeits-Matrix BURUMUT vs A0AAV4C3M3...")
sim_matrix = burumut_emb @ fam_emb.T  # (99, 209)
sim_matrix_norm = sim_matrix / (
    np.linalg.norm(burumut_emb, axis=1, keepdims=True) *
    np.linalg.norm(fam_emb, axis=1, keepdims=True).T
)

# Für jedes BURUMUT-Frame: bestes Match in A0AAV4C3M3
best_match = sim_matrix_norm.argmax(axis=1)
best_score = sim_matrix_norm.max(axis=1)
print(f"\nBeste Matches (BURUMUT-Frame -> A0AAV4C3M3-Frame):")
print(f"  Mittlere Similarity: {best_score.mean():.3f}")
print(f"  Max Similarity: {best_score.max():.3f} bei BURUMUT-Pos {best_score.argmax()}")
print(f"  Min Similarity: {best_score.min():.3f} bei BURUMUT-Pos {best_score.argmin()}")

# Sec-Positionen
sec_pos = [i for i, c in enumerate(BURUMUT) if c == 'U']
uazbe_pos = [32, 46, 66, 80]
print(f"\nÄhnlichkeit an Sec-Positionen (BURUMUT):")
for sp in sec_pos:
    if sp < 99:
        match_pos = best_match[sp]
        match_score = best_score[sp]
        is_uazbe = " (UAZBE)" if sp in uazbe_pos else ""
        print(f"  Pos {sp:3d}: beste Match in Fam-a an Pos {match_pos:3d} (Score: {match_score:.3f}){is_uazbe}")

# Korrelation Sec-Ähnlichkeit mit Sec-Originalposition
print()
print("="*70)
print("BEFUND: ESM-2-Embedding-Korrelation BURUMUT vs A0AAV4C3M3")
print("="*70)
print(f"  Mittlere Ähnlichkeit: {best_score.mean():.3f}")
print(f"  Sec-Positionen-Ähnlichkeit (Durchschnitt): {best_score[sec_pos].mean():.3f}")
print(f"  UAZBE-Ähnlichkeit (Durchschnitt): {best_score[uazbe_pos].mean():.3f}")
print()
print("Wenn UAZBE-Positionen auffallend hohe Ähnlichkeit haben:")
print("  -> Sekundärstruktur-Homologie zwischen BURUMUT und Fam-a")
print("  -> 4 Sec-Positionen markieren ähnliche strukturelle Regionen")
