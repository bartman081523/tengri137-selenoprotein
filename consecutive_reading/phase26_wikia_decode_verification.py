"""
phase26_wikia_decode_verification.py
V7 Phase 26 — WIKIA-METHODE VERIFIKATION: 11 Tappeiner-BURUMUT-Schlusswörter

KRITISCHE KORREKTUR (2026-07-05):
Schmehs Wikia-Translation enthüllt die ECHTE Dekodier-Methode:
- Periode (28 Ziffern) → 14 Dinome
- Dinom → Atom-Nummer
- Atom-Nummer → Element-SYMBOL (z.B. 56→Ba, 92→U)
- ERSTER BUCHSTABE des Symbols = Buchstabe (Ba→B, U→U)

Tool: http://www.dcode.fr/atomic-number-substitution

Quelle: Tengri 137 Wikia (Fandom), lokal: Tengri 137 Translation _ Tengri 137 Wikia _ FANDOM powered by Wikia.html
Wikia-Beispiel: (2^5 * 13 * 37 * 179 * 471077143) / (23 * 53 * 2711 * 897232321) → 0.43 77 25 63 87 76 37 22 80 63 43 37 92 22 ... → "TIME FOR THE TRUTH"

VERIFIKATION: Alle 11 Tappeiner-BURUMUT-Schlusswörter (Periode 7 jedes Bruchs)
sind PERFEKT mit der Wikia-Methode reproduzierbar.
"""
import json
from pathlib import Path

OUT = Path("bbox/wikia_method_20260707_V7")
OUT.mkdir(parents=True, exist_ok=True)

PERIODIC = {
    1:'H', 2:'He', 3:'Li', 4:'Be', 5:'B', 6:'C', 7:'N', 8:'O', 9:'F', 10:'Ne',
    11:'Na', 12:'Mg', 13:'Al', 14:'Si', 15:'P', 16:'S', 17:'Cl', 18:'Ar', 19:'K', 20:'Ca',
    21:'Sc', 22:'Ti', 23:'V', 24:'Cr', 25:'Mn', 26:'Fe', 27:'Co', 28:'Ni', 29:'Cu', 30:'Zn',
    31:'Ga', 32:'Ge', 33:'As', 34:'Se', 35:'Br', 36:'Kr', 37:'Rb', 38:'Sr', 39:'Y', 40:'Zr',
    41:'Nb', 42:'Mo', 43:'Tc', 44:'Ru', 45:'Rh', 46:'Pd', 47:'Ag', 48:'Cd', 49:'In', 50:'Sn',
    51:'Sb', 52:'Te', 53:'I', 54:'Xe', 55:'Cs', 56:'Ba', 57:'La', 58:'Ce', 59:'Pr', 60:'Nd',
    61:'Pm', 62:'Sm', 63:'Eu', 64:'Gd', 65:'Tb', 66:'Dy', 67:'Ho', 68:'Er', 69:'Tm', 70:'Yb',
    71:'Lu', 72:'Hf', 73:'Ta', 74:'W', 75:'Re', 76:'Os', 77:'Ir', 78:'Pt', 79:'Au', 80:'Hg',
    81:'Tl', 82:'Pb', 83:'Bi', 84:'Po', 85:'At', 86:'Rn', 87:'Fr', 88:'Ra', 89:'Ac', 90:'Th',
    91:'Pa', 92:'U', 93:'Np', 94:'Pu', 95:'Am', 96:'Cm', 97:'Bk', 98:'Cf', 99:'Es', 100:'Fm',
    101:'Md', 102:'No', 103:'Lr', 104:'Rf', 105:'Db', 106:'Sg', 107:'Bh', 108:'Hs',
    109:'Mt', 110:'Ds', 111:'Rg', 112:'Cn', 113:'Nh', 114:'Fl', 115:'Mc', 116:'Lv',
    117:'Ts', 118:'Og',
}

# Periode 7 jedes Bruchs (Tappeiner-Methode)
PERIODS_7 = {
    1: "5692379212922245638713122292",
    2: "1192456316922245633192128713",
    3: "3913461492133083638077255713",
    4: "3013113792133083631176125613",
    5: "2276837736762257925692123976",
    6: "1492117619923731131176307077",
    7: "7619924077199287139216778063",
    8: "3913836336131114138363457276",
    9: "111311463451311141372762211463",  # 30 Ziffern = 15 Dinome
    10: "1976456325763783773092123776",
    11: "1492111319774587139363255613"
}

# Erwartete BURUMUT-Wörter
EXPECTED = {
    1: 'BURUMUTREFAMTU', 2: 'NURESUTREGUMFA', 3: 'YAPSUAZBEHIMLA',
    4: 'ZANRUAZBENOMBA', 5: 'TOBIKOTLUBUMYO', 6: 'SUNOKURGANOZYI',
    7: 'OKUZIKUFAUSIHE', 8: 'YABEKANSABERHO', 9: 'NANPSSGNNRCSSSE',
    10: 'KOREMORBIZUMRO', 11: 'SUNAKIRFANEMBA'
}

# Verifikation
print("=" * 80)
print("PHASE 26: WIKIA-METHODE VERIFIKATION")
print("=" * 80)
print(f"\nMethode: Periode 28 Ziffern → 14 Dinome → Element-Symbol → 1. Buchstabe")
print(f"Tool: http://www.dcode.fr/atomic-number-substitution")
print(f"Quelle: Tengri 137 Wikia (Fandom)\n")

results = {
    "metadata": {
        "phase": "V7 / Phase 26",
        "datum": "2026-07-05",
        "methode": "Wikia-Methode: Periode → Dinome → Element-Symbol → 1. Buchstabe",
        "tool": "dcode.fr/atomic-number-substitution",
        "quelle": "Tengri 137 Wikia (Fandom, lokal gespeichert)",
        "beispiel_wikia": "(2^5 * 13 * 37 * 179 * 471077143) / (23 * 53 * 2711 * 897232321) → TIME FOR THE TRUTH",
    },
    "verifikationen": []
}

all_match = True
for bnr, p in PERIODS_7.items():
    pairs = [int(p[j:j+2]) for j in range(0, len(p)-1, 2) if j+2 <= len(p)]
    # Erster Buchstabe des SYMBOLS
    text = ''.join(PERIODIC[pair][0] for pair in pairs)
    expected = EXPECTED[bnr]
    match = text == expected

    # Detaillierte Aufschlüsselung
    details = []
    for pair in pairs:
        sym = PERIODIC[pair]
        details.append({
            "dinom": pair,
            "element": sym,
            "erster_buchstabe": sym[0]
        })

    results["verifikationen"].append({
        "bruch_nr": bnr,
        "periode_7": p,
        "n_digits": len(p),
        "n_dinome": len(pairs),
        "decoded": text,
        "expected": expected,
        "match": match,
        "details": details
    })

    status = "✓" if match else "✗"
    print(f"  Bruch {bnr:2}: {text:20} {status}")
    if not match:
        all_match = False
        print(f"    Erwartet: {expected}")

results["alle_match"] = all_match
results["anzahl_bruche"] = len(PERIODS_7)
results["n_match"] = sum(1 for v in results["verifikationen"] if v["match"])

# Speichere
with open(OUT / "phase26_verification.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n{'ALLE 11 BURUMUT-WÖRTER PERFEKT MIT WIKIA-METHODE DEKODIERT' if all_match else 'FEHLER'}")
print(f"Match-Rate: {results['n_match']}/{results['anzahl_bruche']} = {100*results['n_match']/results['anzahl_bruche']:.1f}%")
print(f"\n✓ Gespeichert: {OUT}/phase26_verification.json")

# Zusätzlich: Erklärung der Methode
print("\n" + "=" * 80)
print("METHODE-ERKLÄRUNG")
print("=" * 80)
print("""
Die p17-Seite enthält 11 Brüche (Schmehs Full_Notes bestätigt).
Jeder Bruch hat eine PERIODE (= die sich wiederholenden Nachkommastellen).

WIKIA-METHODE (dcode.fr atomic-number-substitution):
1. Berechne die Periode des Bruchs (oft tausende Ziffern lang)
2. Nimm die ersten 28 Ziffern (für einen 14-Buchstaben-Klartext)
3. Teile in 14 Zwei-Ziffern-Gruppen (Dinome) auf
4. Jedes Dinom ist eine ATOM-NUMMER
5. Ordne die Atom-Nummer dem ELEMENT-SYMBOL zu (z.B. 56→Ba, 92→U)
6. Der ERSTE BUCHSTABE des Symbols ist der Klartext-Buchstabe

Beispiel Tappeiner Bruch 1 Periode 7:
- Periode: 5692379212922245638713122292
- Dinome:  56, 92, 37, 92, 12, 92, 22, 45, 63, 87, 13, 12, 22, 92
- Symbole: Ba, U, Rb, U, Mg, U, Ti, Rh, Eu, Fr, Al, Mg, Ti, U
- Klartext: B, U, R, U, M, U, T, R, E, F, A, M, T, U = "BURUMUTREFAMTU"

KRITISCHE KORREKTUR (vorher → nachher):
- Vorher: BURUMUT ist eine Tengrismus-Ritualsprache, Schmehs Englisch ist die Übersetzung
- Nachher: BURUMUT IST der Klartext der Brüche (Tappeiner hat 11 verschiedene Brüche gefunden)
- Schmehs Wikia-Beispiel zeigt einen ANDEREN Bruch, der "TIME FOR THE TRUTH" ergibt
- BEIDE nutzen die GLEICHE Methode, aber ANDERE Brüche → ANDERE Klartexte
""")
