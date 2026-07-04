"""
Q13b (KORRIGIERT): BURUMUT hat KEIN Cystein, KEIN Glycin, aber 11 Sec
"""
import re

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# Charakter-Alphabet
chars = sorted(set(BURUMUT_FULL))
print(f"BURUMUT-Alphabet ({len(chars)} chars):")
print(f"  {chars}")

# Cys-Check
print(f"\nCys (C) in BURUMUT: {BURUMUT_FULL.count('C')} (fehlt vollstaendig)")
print(f"Gly (G) in BURUMUT: {BURUMUT_FULL.count('G')} (nur 1x)")
print(f"Sec (U) in BURUMUT: {BURUMUT_FULL.count('U')} (11x = 11.1%)")
print(f"Asx (B) in BURUMUT: {BURUMUT_FULL.count('B')} (7x = 7.1%, unscharf fuer Asn/Asp)")
print(f"Glx (Z) in BURUMUT: {BURUMUT_FULL.count('Z')} (8x = 8.1%, unscharf fuer Gln/Glu)")

# BURUMUT fehlen: C, D, F (1x), G (1x), I (2x), J (0), K (0)
# und enthalten: U (Sec), O (Pyl), B (Asx), Z (Glx) - die unscharfen Seltenen!
print()
print(f"BURUMUT enthaelt Sec (U), Pyl (O), Asx (B), Glx (Z)")
print(f"Diese 4 Buchstaben sind die 'unscharfen' / seltenen AS-Codes.")
print(f"Sie machen {(11+2+7+8)/99*100:.1f}% von BURUMUT aus.")

# Konsequenz: BURUMUT-Protein hat spezifische Anforderungen
# - Kein Cys, kein Gly in ausreichender Menge
# - Viele Sec, viele unscharfe (Asx/Glx) Positionen
# Hypothese: BURUMUT könnte ein Sec-only-Protein sein, das OHNE
# Cys-Substitution arbeitet. Solche Proteine sind extrem selten.
