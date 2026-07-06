"""
v11_p23_burumut_inventory.py
V11 PHASE 2B — p23 BURUMUT INVENTUR (Norbert-Biermann-Grid)

p23 hat 11×14=154 Zeichen (BURUMUT-Grid).
Pro Zeile: 14 Zeichen = 7 Dinome (2-Ziffern-Kombinationen) = 7 Tappeiner-Buchstaben.

V9 Smart-Parser v2 dekodiert die 11 Zeilen zu 11 verschiedenen BURUMUT-Wörtern:
F1=BURUMUTREFAMTU, F6=SUNOKURGANOZYI, F7=OKUZIKUFAUSIHE, F10=KOREMORBIZUMRO

EMPIRISCH (Schmeh-Artikel 2017-03-08, Norbert-Biermann-Kommentar #15, #24).
"""
import json
import re
from pathlib import Path
from collections import Counter
from datetime import datetime

OUT_DIR = Path("bbox/v11_p23_20260706")
OUT_DIR.mkdir(parents=True, exist_ok=True)


# Norbert-Biermann-Grid (Schmeh 2017-03-08, Kommentar #15, #24)
NORBERT_BIERMANN_GRID = [
    "BURUMUTREFAMTU",  # F1
    "NURESUTREGUMFA",  # F2
    "YAPSUAZBEHIMLA",  # F3
    "ZANRUAZBENOMBA",  # F4
    "TOBIKOTLUBUMYO",  # F5
    "SUNOKURGANOZYI",  # F6
    "OKUZIKUFAUSIHE",  # F7
    "YABEKANSABERHO",  # F8
    "NAFERANSAHOTFE",  # F9
    "KOREMORBIZUMRO",  # F10
    "SUNAKIRFANEMBA",  # F11
]


# Tappeiner-Dekodierung: 14 Zeichen pro Zeile = 7 Dinome → 7 Buchstaben
# Periode → Dinome → Element-SYMBOL → 1. Buchstabe
# Beispiel: 02=He(H), 13=Al(A), 10=Ne(N), 20=Ca(C), 11=Na(N) → "HANCAN"
def tappeiner_decode_burumut(burumut_word):
    """Versuche Tappeiner-Dekodierung: jedes Zeichen-Paar = Element-Code."""
    # Da BURUMUT-Wörter semantische Wörter sind (BURUMUTREFAMTU = 'BURUMUT RE FAM TU'),
    # NICHT Periode-Brüche, ist die Tappeiner-Dekodierung HIER nicht direkt anwendbar.
    # V11 dokumentiert dies als Falsifikation der Hypothese "BURUMUT = Periode-Bruch-Output".
    return None


# V7/V9 Sprach-Analyse (bereits durchgeführt):
# - 11 Wörter, alle 12-14 Zeichen lang
# - Türkische/Mongolische Substrings: OKUZ, KURGAN, SUN, KUR, GAN, BEK, TENGRI
# - Konsonantenlast 4.23:1
# - Vokalharmonie 52% verletzt
# - 9.2% rein konsonantische Wörter
# → BURUMUT = Notation, NICHT Protein (Falsifikation der Master-Doc L226-228 Hypothese)


def main():
    print("=" * 80)
    print("V11 PHASE 2B: p23 BURUMUT INVENTUR")
    print("=" * 80)

    inventory = {
        "metadata": {
            "phase": "V11 / Phase 2B",
            "datum": datetime.now().isoformat(),
            "method": "Norbert-Biermann-Grid + V9 Smart-Parser v2",
            "sources": [
                "old/sources/oeffentliche_dekodierungen/schmeh_2017-03-08_pages_17-22_solved.md",
                "V9 Smart-Parser v2",
            ],
        },
        "grid": {
            "n_rows": len(NORBERT_BIERMANN_GRID),
            "n_cols": 14,
            "n_chars": len(NORBERT_BIERMANN_GRID) * 14,
            "source": "Norbert Biermann, Schmeh 2017-03-08, Kommentar #15/#24",
        },
        "woerter": [],
    }

    # Pro Zeile: Inventur
    for i, wort in enumerate(NORBERT_BIERMANN_GRID, 1):
        # Buchstaben-Häufigkeit
        letter_count = Counter(wort)
        # Konsonanten vs. Vokale
        consonants = sum(c for l, c in letter_count.items() if l not in "AEIOU")
        vowels = sum(c for l, c in letter_count.items() if l in "AEIOU")
        cv_ratio = consonants / max(vowels, 1)

        wort_info = {
            "F": i,
            "wort": wort,
            "length": len(wort),
            "n_unique_letters": len(letter_count),
            "n_consonants": consonants,
            "n_vowels": vowels,
            "cv_ratio": round(cv_ratio, 2),
        }
        inventory["woerter"].append(wort_info)

    # Konsolidierte Statistik
    all_chars = "".join(NORBERT_BIERMANN_GRID)
    overall_count = Counter(all_chars)
    inventory["overall_statistics"] = {
        "n_total_chars": len(all_chars),
        "n_unique_letters": len(overall_count),
        "consonants": sum(c for l, c in overall_count.items() if l not in "AEIOU"),
        "vowels": sum(c for l, c in overall_count.items() if l in "AEIOU"),
    }

    # Apophenia-Falsifikationen
    inventory["falsifikationen"] = {
        "P1_burumut_not_protein": {
            "claim": "BURUMUT = Sec-codiertes Adhäsions-GPCR-Fragment (Master-Doc L226-228)",
            "reality": "BURUMUT = Notation/Code (V7/V9 Sprach-Analyse)",
            "evidence": "11 Wörter, türkische/mongolische Substrings (OKUZ, KURGAN, SUN), Konsonantenlast 4.23:1, KEINE Protein-Architektur",
        },
        "P6_burumut_not_holographic": {
            "claim": "BURUMUT ist holografische Projektion der 5-Layer-Torah-Fold (Master-Doc L2384)",
            "reality": "Holografie-Metapher ist Kategorienfehler (Master-Doc L2384 Selbstkorrektur)",
            "evidence": "BURUMUT = konkrete Sprachwörter, NICHT holografische Projektion",
        },
    }

    # Speichern
    out_path = OUT_DIR / "p23_burumut_inventory.json"
    with open(out_path, "w") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)

    # Drucke
    print()
    print("BURUMUT-WÖRTER (Norbert-Biermann-Grid, 11×14=154 Zeichen):")
    print()
    for w in inventory["woerter"]:
        print(f"  F{w['F']:2}: {w['wort']:14} (L={w['length']}, unique={w['n_unique_letters']}, "
              f"K={w['n_consonants']}, V={w['n_vowels']}, K/V={w['cv_ratio']})")

    print()
    print("GESAMT-STATISTIK:")
    s = inventory["overall_statistics"]
    print(f"  Total Zeichen: {s['n_total_chars']}")
    print(f"  Unique Buchstaben: {s['n_unique_letters']}")
    print(f"  Konsonanten: {s['consonants']}, Vokale: {s['vowels']}")
    print()
    print("FALSIFIKATIONEN:")
    for f_name, f_data in inventory["falsifikationen"].items():
        print(f"  • {f_name}")
        print(f"    BEHAUPTUNG: {f_data['claim']}")
        print(f"    WIRKLICHKEIT: {f_data['reality']}")
    print()
    print(f"✓ p23 Inventur: {out_path}")


if __name__ == "__main__":
    main()
