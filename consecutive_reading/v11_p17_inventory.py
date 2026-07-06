"""
v11_p17_inventory.py
V11 PHASE 2A — p17 VOLLSTÄNDIGE INVENTUR

Was steht WO auf p17?
- V7: 10 lateinische Ziffern (2^5, 13, 37, 179, 471077143, 23, 53, 2711, 897232321)
- V7: 11 Tengri-Glyphen (Akrostichon BNYZTSOYNKS)
- Schmeh #12: Tappeiner-Brüche (z.B. 0.000023174...)

Output: bbox/v11_p17_20260706/p17_inventory.json

EMPIRISCH (ohne Tora-Turing-Maschine, ohne TCI-Experimente).
"""
import json
import re
from pathlib import Path
from collections import Counter
from datetime import datetime

OUT_DIR = Path("bbox/v11_p17_20260706")
OUT_DIR.mkdir(parents=True, exist_ok=True)


# Schmeh-Artikel 2017-03-08 (#12) — empirisch verifizierte Daten
# Klartext p17 (Tappeiner-Dekodierung):
# "TIME FOR THE TRUTH / OVER MANY THOUSAND YEARS WE SEND YOU MESSENGERS
#  AND TEACHER / ALL THIS KNOWLEDGE BEHIND YOUR CIVILISATION IS OURS"
TAPPEINER_KLARTEXT_P17 = [
    "TIME FOR THE TRUTH",
    "OVER MANY THOUSAND YEARS",
    "WE SEND YOU MESSENGERS AND TEACHER",
    "ALL THIS KNOWLEDGE",
    "BEHIND YOUR CIVILISATION IS OURS",
]

# V7-belegte lateinische Ziffern (Faktor-Zerlegungen)
V7_ZIFFERN_P17 = [2, 5, 13, 37, 179, 471077143, 23, 53, 2711, 897232321]

# V7-belegtes Akrostichon der 11 Tengri-Glyphen
P17_AKROSTICHON = "BNYZTSOYNKS"


def main():
    print("=" * 80)
    print("V11 PHASE 2A: p17 VOLLSTÄNDIGE INVENTUR")
    print("=" * 80)

    inventory = {
        "metadata": {
            "phase": "V11 / Phase 2A",
            "datum": datetime.now().isoformat(),
            "method": "V7-belegte Daten + Schmeh-Artikel #12 (Tappeiner-Empirik)",
            "sources": [
                "old/sources/oeffentliche_dekodierungen/schmeh_2017-03-08_pages_17-22_solved.md",
                "V7 BURUMUT-Analyse",
                "Schmeh 2017-03-08 Kommentar #12 (Tappeiner)",
            ],
        },
        "v7_lateinische_ziffern": {
            "values": V7_ZIFFERN_P17,
            "count": len(V7_ZIFFERN_P17),
            "source": "V7 p17-Befund (visuelle Verifikation der Ziffern 0-9)",
        },
        "akrostichon_der_11_glyphen": {
            "string": P17_AKROSTICHON,
            "length": len(P17_AKROSTICHON),
            "decoded_meaning": "BNYZTSOYNKS = 11 erste Buchstaben der 11 Tappeiner-BURUMUT-Wörter",
            "caesar_shift_0_25": "0/26 ergeben Englisch (V7 Falsifikation)",
        },
        "tappeiner_brueche_klartext": {
            "method": "Periode → Dinome (2-Ziffern) → Element-Symbol (IUPAC) → 1. Buchstabe",
            "klartext_zeilen": TAPPEINER_KLARTEXT_P17,
            "source": "Schmeh 2017-03-08, Kommentar #12 (Klaus Tappeiner)",
        },
        "schicht_struktur": {
            "tengri_glyphen": "11 Glyphen (Akrostichon BNYZTSOYNKS)",
            "latein_ziffern": "10 Ziffern (Faktor-Zerlegungen)",
            "tappeiner_brueche": "Unbekannte Anzahl Brüche (dekodiert zu BURUMUT-Wörtern)",
            "falsifikation_p1_p16": "p17 hat KEINE der 17 V6-Tengri-Glyphen — p17 ist EIGENE Schicht",
        },
    }

    # Speichern
    out_path = OUT_DIR / "p17_inventory.json"
    with open(out_path, "w") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)

    print()
    print(f"✓ p17 Inventur: {out_path}")
    print()
    print("INVENTUR-ÜBERSICHT:")
    print(f"  • {len(V7_ZIFFERN_P17)} lateinische Ziffern: {V7_ZIFFERN_P17}")
    print(f"  • {len(P17_AKROSTICHON)} Tengri-Glyphen: Akrostichon = '{P17_AKROSTICHON}'")
    print(f"  • {len(TAPPEINER_KLARTEXT_P17)} Tappeiner-Klartext-Zeilen")
    print()
    print("Klartext (Tappeiner-Dekodierung, Schmeh #12):")
    for i, line in enumerate(TAPPEINER_KLARTEXT_P17, 1):
        print(f"  F{i}: {line}")
    print()
    print("Apophenia-Ausschluss: p17 ist EIGENE Schicht (NICHT Tengri-Fließtext)")
    print("  → V11 nutzt Tappeiner-Methode direkt, NICHT V6-Glyph-Mapping")


if __name__ == "__main__":
    main()
