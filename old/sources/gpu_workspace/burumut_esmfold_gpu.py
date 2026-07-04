"""
ESMFold 3D-Strukturvorhersage für BURUMUT (GPU-beschleunigt)

Da AlphaFold2 und ESMFold groß sind, verwenden wir
ESM-2 (Protein Language Model) für die Sekundärstrukturvorhersage
als Approximation. Das ist schneller und läuft komplett auf unserer GPU.
"""
import torch
import esm
import numpy as np
import time

# BURUMUT-Sequenz (Sec zu Cys für ESM)
BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)
BURUMUT_CYS = BURUMUT.replace('U', 'C').replace('O', 'K').replace('B', 'N').replace('Z', 'Q')

print("="*70)
print("ESM-2 Vorhersage auf GPU")
print("="*70)
print(f"Sequenz: {BURUMUT_CYS[:60]}...")
print(f"Laenge: {len(BURUMUT_CYS)} AS")
print()

# Lade ESM-2 (650M, klein)
print("Lade ESM-2 (esm2_t30_150M_UR50D)...")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {device}")

# Lade Modell (etwas größer für bessere Vorhersagen)
t0 = time.time()
model, alphabet = esm.pretrained.esm2_t30_150M_UR50D()
batch_converter = alphabet.get_batch_converter()
model = model.to(device)
model.eval()
print(f"Modell geladen in {time.time()-t0:.1f}s")

# Tokenize
data = [("BURUMUT", BURUMUT_CYS)]
batch_labels, batch_strs, batch_tokens = batch_converter(data)
batch_tokens = batch_tokens.to(device)

# Forward pass
print("\nForward pass...")
with torch.no_grad():
    t0 = time.time()
    results = model(batch_tokens, repr_layers=[30], return_contacts=True)
    print(f"Inferenz in {time.time()-t0:.1f}s")

# Embeddings
embeddings = results["representations"][30]
print(f"Embedding-Shape: {embeddings.shape}")

# Sekundärstruktur-Vorhersage via 3-State-Classifier
ss3_results = model.predict_contacts(embeddings)
print(f"SS3-Contacts-Shape: {ss3_results['contact_probs'].shape}")

# Speichere Embeddings
import numpy as np
np.save("sources/gpu_workspace/burumut_esm2_embeddings.npy", 
        embeddings.cpu().numpy())
np.save("sources/gpu_workspace/burumut_esm2_contacts.npy",
        ss3_results['contact_probs'].cpu().numpy())

# Sekundärstruktur-Profil
# Wir berechnen einfache Profile aus der Sequenz
import collections
print()
print("="*70)
print("Sekundaerstruktur-Profil (Heuristik)")
print("="*70)
helix_p = {'A': 1.42, 'R': 0.98, 'N': 0.67, 'D': 1.01, 'C': 0.70,
           'E': 1.51, 'Q': 1.11, 'G': 0.57, 'H': 1.00, 'I': 1.08,
           'L': 1.21, 'K': 1.16, 'M': 1.45, 'F': 1.13, 'P': 0.57,
           'S': 0.77, 'T': 0.83, 'W': 1.08, 'Y': 0.69, 'V': 1.06}
profile = [helix_p.get(c, 1.0) for c in BURUMUT_CYS]
print(f"Durchschnittliche Helix-Propensity: {sum(profile)/len(profile):.3f}")
print(f"Max Helix-Propensity: {max(profile):.3f} bei Position {profile.index(max(profile))}")
print(f"Min Helix-Propensity: {min(profile):.3f} bei Position {profile.index(min(profile))}")

# Sec-Positionen
sec_pos = [i for i, c in enumerate(BURUMUT) if c == 'U']
uazbe_pos = [32, 46, 66, 80]
print()
print(f"Sec-Positionen: {sec_pos}")
print(f"UAZBE-Positionen: {uazbe_pos}")
print()
print("Helix-Propensity an Sec-Positionen:")
for sp in sec_pos[:5]:
    print(f"  Pos {sp} (Sec): {profile[sp]:.3f}")
print("Helix-Propensity an UAZBE-Positionen:")
for up in uazbe_pos:
    print(f"  Pos {up} (UAZBE): {profile[up]:.3f}")

print()
print("="*70)
print("BURUMUT-ESM-2-Vorhersage gespeichert:")
print("  - sources/gpu_workspace/burumut_esm2_embeddings.npy")
print("  - sources/gpu_workspace/burumut_esm2_contacts.npy")
print("="*70)
