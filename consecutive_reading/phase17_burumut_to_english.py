"""
phase17_burumut_to_english.py
V7 Phase 6 — BURUMUT → Englisch Mapping

Schmehs Methode: erste Buchstaben der BURUMUT-Wörter ergeben englische Phrasen.

Test: BURUMUTREFAMTU → erste Buchstaben: B, U, R, U, M, U, T, R, E, F, A, M, T, U
→ "BURUMUTREFAMTU"

Hmm, das ist nicht Englisch. Aber Schmehs Kommentar sagt:
"Exact text of first calculation (first letter of every group): TIME FOR THE TRUTH NPKIAKVGPPPFBIR"

Also: erste Buchstaben ergeben ENGLISCH.
"""
from pathlib import Path
import json

# BURUMUT-Texte (von phase16)
burumut = {
    1: ["IYPKHIMHBCOMPA", "BSANNNPDHLPSNS", "TUCHSCCFACMO?A", "SRNBICRFGRYTIC", "YKREXAATBXSASG", "PTNTCPSBMOSIUH", "BURUMUTREFAMTU"],
    2: ["CCZHNLAACVPRSN", "ETPPBIIEPMNYTI", "GYBSCTG?ECNOCL", "CHPGCTTCRRCWBC", "CCACWSZNTLLREH", "XSSTCCXEWBTCWP", "NURESUTREGUMFA"],
    3: ["GTOHCKMPTPBPFC", "AICHRMNGCPGMTA", "CBNCDABPPRCTTW", "CCABFUTZCORNZP", "KGF?PCSFEMCGAM", "IORWCTTHCRFPBP", "YAPSUAZBEHIMLA"],
    4: ["BHBTCNPTMYICPK", "OCBSTRKXHCMZRC", "BTYGPSPCSWHHPP", "GZZNPAPGSKBRPR", "PRPSAPRNCPPZAT", "CAAHAARACYYAGL", "ZANRUAZBENOMBA"],
    5: ["BGFBNMSTB?BPRD", "PTCNRTAGCBTANB", "NCSCCNNBYBNCTC", "TYAAHFFCZYOEPA", "ZCPNPTBIPYBIHX", "BAHATCWO?HSBFI", "TOBIKOTLUBUMYO"],
    6: ["NFPCPRSLTNEZC?", "SSRMONENHTSRPZ", "NAARRRTGHEHPZC", "REUAXPCELCNMBK", "SUNOKURGANOZYI"],
    7: ["GTOHCKMPTPBPFC", "PCGRPRCCEAKCWA", "AYPBBBGMASGSPG", "SMYPICBIBTICSN", "SCCLKFFEBERNPF", "EHXESNOCPEHKAR", "OKUZIKUFAUSIHE"],
    8: ["DBSTRFMANENSBP", "NCBCCCTSBRCNRT", "GNMFZWRCNBAXPT", "CPHSERPTPFRPAN", "EPCHERRRBHUFRS", "BSNPPBHTPOSPSK", "YABEKANSABERHO"],
    9: ["ECN?TPTMTPNRTBC", "NWCGRCFFCGLBWSP", "MCFKCSPSMZPNRTV", "MPZIMCAATSAOSSM", "ERTPAHCVCAMHHRF", "SMNEMCCLYSVLKPC", "LYBMCRUZO?MCPYG", "NANPSSGNNRCSSSE"],
    10: ["LOTTNIECPWGAHP", "YCTTGNMSPRFRIT", "TRSFZHOARABSVE", "TNSLMBPPNEBPRB", "PCCBRANNSSLAST", "RTRMGCCSCSATGP", "KOREMORBIZUMRO"],
    11: ["BMGBISE?PBSFST", "BGNCOHIAFCBNRT", "KFI?OEUMCNCPGL", "SCTGGYBCRLACHN", "TRPMSCZSFCRTIH", "GECSNESSOPTPEN", "SUNAKIRFANEMBA"],
}

# Methode: Erste Buchstaben der BURUMUT-Texte einer Zeile
print("=" * 80)
print("Methode 1: Erste Buchstaben aller BURUMUT-Texte pro Bruch")
print("=" * 80)

for bnr in sorted(burumut.keys()):
    texts = burumut[bnr]
    initials = ''.join(t[0] if t else '?' for t in texts)
    print(f"Bruch {bnr:2d} ({len(texts)} Texte): {initials}")

# Aber Schmehs Kommentar sagt "TIME FOR THE TRUTH" für die erste Rechnung
# Das sind 19 Buchstaben
# Wenn jede BURUMUT-Periode 14 Buchstaben hat, brauchen wir 19/14 = 1.4 Perioden
# Eher: BURUMUT-Periode 7 = BURUMUTREFAMTU = 14 Buchstaben
# Das ist "BURUMUT-REFAMTU" (Wortgrenzen: BURUMUT | REFAMTU)

# Vielleicht ist die 7. Periode das "Schlüsselwort" BURUMUT
# Und die anderen Perioden enthalten die englische Botschaft

# Versuche: Erste Buchstaben = 14 Zeichen, vielleicht das englische Wort
# BURUMUTREFAMTU = BURUMUT(7) + REFAMTU(7)

# Schaue Periode 7 von allen 11 Bruechen an
print("\n" + "=" * 80)
print("Periode 7 (Schlussperiode) von allen Bruechen")
print("=" * 80)
for bnr in sorted(burumut.keys()):
    texts = burumut[bnr]
    if len(texts) >= 7:
        t = texts[6]  # Index 6 = Periode 7
        print(f"  Bruch {bnr:2d}: {t}")
    else:
        print(f"  Bruch {bnr:2d}: <nur {len(texts)} Perioden>")

# Vielleicht sind die Perioden 1-6 die BURUMUT-Wörter und Periode 7 ist "Schlusswort"
# 6 BURUMUT-Wörter + 1 Schlusswort = 7 Perioden
# Tatsächlich sind die Texte ungleich lang und wir wissen nicht welche Bedeutung sie haben
