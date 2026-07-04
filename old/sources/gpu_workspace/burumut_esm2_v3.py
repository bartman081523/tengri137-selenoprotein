"""ESM-2 Embeddings + Contact-Prediction (korrekte API)"""
import torch
import esm
import numpy as np

BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)
BURUMUT_CYS = BURUMUT.replace('U', 'C').replace('O', 'K').replace('B', 'N').replace('Z', 'Q')

device = torch.device('cuda')
model, alphabet = esm.pretrained.esm2_t30_150M_UR50D()
batch_converter = alphabet.get_batch_converter()
model = model.to(device)
model.eval()

data = [("BURUMUT", BURUMUT_CYS)]
batch_labels, batch_strs, batch_tokens = batch_converter(data)
batch_tokens = batch_tokens.to(device)

print("Forward pass (mit return_contacts=True)...")
with torch.no_grad():
    results = model(batch_tokens, repr_layers=[30], return_contacts=True)

# Alles aus results extrahieren
print("Keys in results:", list(results.keys()))
contact_probs = results.get("contacts")
embeddings = results.get("representations", {}).get(30)
logits = results.get("logits")

if contact_probs is not None:
    print(f"Contacts-Shape: {contact_probs.shape}")
    print(f"Contact mean: {contact_probs.mean():.4f}, max: {contact_probs.max():.4f}")
    np.save("sources/gpu_workspace/burumut_esm2_contacts.npy", contact_probs.cpu().numpy())

if embeddings is not None:
    print(f"Embeddings-Shape: {embeddings.shape}")
    np.save("sources/gpu_workspace/burumut_esm2_embeddings.npy", embeddings.cpu().numpy())

if logits is not None:
    print(f"Logits-Shape: {logits.shape}")
    # SS3-Vorhersage (Sekundärstruktur)
    ss3 = logits.argmax(dim=-1)
    print(f"SS3-Prediction-Shape: {ss3.shape}")
    # Per-Residue
    print(f"SS3-Codes (erste 20): {ss3[0, :20].cpu().tolist()}")
    # 0=Helix, 1=Strand, 2=Coil (oder je nach Alphabet)
    
# Helix-Positionen
ss3_seq = ss3[0, 1:-1].cpu().numpy()  # ohne BOS/EOS
print(f"\nBURUMUT Sekundärstruktur (Length {len(ss3_seq)}):")
print(f"  Helices (Code 0): {np.sum(ss3_seq == 0)} AS")
print(f"  Sheets (Code 1): {np.sum(ss3_seq == 1)} AS")
print(f"  Coils (Code 2): {np.sum(ss3_seq == 2)} AS")

# Sec-Positionen
sec_pos = [i for i, c in enumerate(BURUMUT) if c == 'U']
uazbe_pos = [32, 46, 66, 80]

print(f"\nSec-Positionen: {sec_pos}")
print(f"UAZBE-Positionen: {uazbe_pos}")
print()

# Cross-Correlation: Sec in Helices?
print("Sec-Positionen in ESM-2-Sekundärstruktur:")
for i, sp in enumerate(sec_pos):
    if sp < len(ss3_seq):
        code = ss3_seq[sp]
        ss_name = ['Helix', 'Sheet', 'Coil'][code] if code < 3 else 'Unkn.'
        is_uazbe = " (UAZBE)" if sp in uazbe_pos else ""
        print(f"  Pos {sp:3d}: {ss_name}{is_uazbe}")

# Heißt das was?
print()
print("="*70)
print("BEFUND: Sec-Positionen in ESM-2-Sekundärstruktur")
print("="*70)
sec_in_helix = [sp for sp in sec_pos if sp < len(ss3_seq) and ss3_seq[sp] == 0]
sec_uazbe_in_helix = [sp for sp in sec_in_helix if sp in uazbe_pos]
print(f"Sec-Positionen in Helix: {sec_in_helix}")
print(f"Sec-UAZBE-Positionen in Helix: {sec_uazbe_in_helix}")
print()
if sec_uazbe_in_helix:
    print("→ 4 markierte UAZBE-Sec-Positionen sind in Helices positioniert")
    print("  -> Sekundärstruktur-Konsistenz mit funktionalen Sec-Regionen")
else:
    print("→ 4 markierte UAZBE-Sec-Positionen sind NICHT alle in Helices")
    print("  -> Wahrscheinlich in Loop-/Coil-Regionen für SECIS-Funktion")
