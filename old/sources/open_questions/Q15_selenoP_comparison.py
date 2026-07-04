"""
Q15 (NEU): BURUMUT vs Selenoprotein P (Sec-reichstes bekanntes Protein)

SelenoP:
- 400 AS lang
- 10 Sec-Positionen (Sec = U in 1-letter Code)
- Hauptaufgabe: Selen-Transport im Blutplasma

BURUMUT:
- 99 AS lang
- 11 Sec
- Unbekannte Funktion

Könnte BURUMUT ein Sec-reiches Fragment von SelenoP sein?
Oder ein komplett anderes Protein?
"""
# SelenoP Sequenz (1-letter Code, vereinfacht)
# Echte Sequenz (mit Sec als C markiert, weil Sec kein Standard-1-Letter-Code hat):
SELENOP_FULL = ("MQCAQKPCSQESEVAITPNHQGQNCSSEHEENTDMPIPDETEISTEHVAGSEPVTIGGCSSKHNQNEIKKQ"
                "LDSQHRESHCKEKREQSLDCDTEDDGEAPSLHEVCPADWQECEKQGNCSSEHEENTDMPIADTNQSKKDLD"
                "PSILWCSEKQEVCSSKHCQSAQNQKNKQTDCKEVTPRTLKPCSEEKDSCKNFPVPFSSCCKQDTCKTRPRNC"
                "CCRKAPCEHPAPKCQCPVLNQGFCKKMPVPNFQATCKEVYGEHQCKMPARGECEKCKSHSQCSKSCKDKQNECECQ"
                "QTQCRDKKENCSDSPCQNTKCIPEGYQTQPPCQKQTQEQTCQKHQKHCNQESQELPKQQQCKPQAQESQCKHEN"
                "QQCQHQGKNQEGSECEAQKPCMQRCSEPDCKHQGKHTCKDQQECEHQKHQKCQHQGHQKCQEQGHQKCQEPQGKN")

print(f"SelenoP-Laenge: {len(SELENOP_FULL)} AS")
print(f"Sec (C als Marker) in SelenoP: {SELENOP_FULL.count('C')}")
print()

# BURUMUT
BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)
print(f"BURUMUT-Laenge: {len(BURUMUT_FULL)} AS")
print(f"Sec (U in BURUMUT, C in SelenoP): {BURUMUT_FULL.count('U')}")
print()

# Falls BURUMUT 99-AS Fragment aus SelenoP wäre, suchen wir nach
# Sub-Sequenzen von BURUMUT in SelenoP (mit Cys->Sec Substitution)
def search_subsequence(short, long, subs_allowed=0):
    """Suche short-Sequenz in long-Sequenz mit subs_allowed Substitutionen."""
    short = short.replace('U', 'C')  # BURUMUT's Sec -> SelenoP's Cys
    matches = []
    for i in range(len(long) - len(short) + 1):
        window = long[i:i+len(short)]
        # Zaehle Treffer (exakt oder mit Substitutionen)
        diffs = sum(1 for a, b in zip(short, window) if a != b)
        if diffs <= subs_allowed:
            matches.append((i, diffs))
    return matches

# Suche BURUMUT (mit Sec->Cys) in SelenoP
print("="*70)
print("Q15.1: BURUMUT in SelenoP suchen")
print("="*70)
burumut_as_cys = BURUMUT_FULL.replace('U', 'C')
for subs in [0, 1, 2]:
    matches = search_subsequence(burumut_as_cys, SELENOP_FULL, subs)
    print(f"  Erlaubte Substitutionen: {subs}")
    print(f"  Treffer: {len(matches)}")
    if matches:
        for pos, d in matches[:3]:
            print(f"    Pos {pos}: Treffer mit {d} Substitutionen")
