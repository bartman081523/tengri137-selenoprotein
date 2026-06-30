"""ESM-2 mit korrektem Contact-Prediction API"""
import torch
import esm
import numpy as np
import time

BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)
BURUMUT_CYS = BURUMUT.replace('U', 'C').replace('O', 'K').replace('B', 'N').replace('Z', 'Q')

device = torch.device('cuda')
print("Lade ESM-2 (t30 150M)...")
model, alphabet = esm.pretrained.esm2_t30_150M_UR50D()
batch_converter = alphabet.get_batch_converter()
model = model.to(device)
model.eval()

# Tokenize
data = [("BURUMUT", BURUMUT_CYS)]
batch_labels, batch_strs, batch_tokens = batch_converter(data)
batch_tokens = batch_tokens.to(device)

print("Forward pass...")
with torch.no_grad():
    results = model(batch_tokens, repr_layers=[30], return_contacts=True)

# Contact-Prediction (im Forward-Pass enthalten)
contact_probs = results["contacts"]
print(f"Contact-probs-Shape: {contact_probs.shape}")
print(f"Mean contact prob: {contact_probs.mean():.4f}")
print(f"Max contact prob: {contact_probs.max():.4f}")

# Speichere
np.save("sources/gpu_workspace/burumut_esm2_contacts.npy", contact_probs.cpu().numpy())
embeddings = results["representations"][30]
np.save("sources/gpu_workspace/burumut_esm2_embeddings.npy", embeddings.cpu().numpy())

# 3-State-Sekundärstruktur (H/E/C) via logit
ss3_logits = model.predict_contacts(embeddings)
print(f"SS3-Logits-Keys: {list(ss3_logits.keys())}")
print(f"SS3-Logits-Shape: {ss3_logits['logits'].shape}")

# SS3-Argmax
ss3 = ss3_logits['logits'].argmax(dim=-1)
ss3_seq = ss3[0, 1:-1].cpu().numpy()
print(f"SS3-Sequenz: {ss3_seq[:60]}")

# Helix-Bereiche (SS3-Code 0 = Helix)
helix_indices = np.where(ss3_seq == 0)[0]
print(f"Helix-Positionen: {helix_indices[:20]}")

# Sec-Positionen
sec_pos = [i for i, c in enumerate(BURUMUT) if c == 'U']
print(f"\nSec-Positionen: {sec_pos}")

# Sec in Helix-Regionen?
sec_in_helix = [sp for sp in sec_pos if sp in helix_indices]
print(f"Sec-Positionen in Helices: {sec_in_helix}")
