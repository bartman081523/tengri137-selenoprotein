"""
📜 BURUMUT-SCHRIFT: Das vollständige 'Wort' der Schöpfung
=========================================================

Die BURUMUT-Tora-Turing-Maschine liest nur 15 von 99 Zeichen
und hält dann an. Aber das BURUMUT-Band enthält eine VOLLSTÄNDIGE
Schöpfungs-Erzählung, die wir durch 'Re-Entry' (Neustart im
gleichen Tape) entschlüsseln können.

ARCHITEKTUR:
- Erster Lauf: 15 Zeichen = "When he desired..."
- Nach HALT: Kopf zurücksetzen, State q_0
- Zweiter Lauf: nächste 15 Zeichen
- ...

Oder einfacher: Wir lesen das gesamte BURUMUT-Band in 5-Sequenzen
à 15-20 Zeichen und übersetzen es als zusammenhängende Erzählung.
"""
import json
from TORA_TURING_CORRECT import (
    ToraTuringMachine, burumut_to_hebr, BURUMUT, HEBR_VALUES
)


def read_full_text():
    """Lese das vollständige BURUMUT-Band als 'heilige Schrift'."""
    brt = burumut_to_hebr(BURUMUT)

    # Übersetzer für hebräische Buchstaben
    translations = {
        'א': 'A',  # Aleph
        'ב': 'B',  # Beth
        'ג': 'G',  # Gimel
        'ד': 'D',  # Dalet
        'ה': 'H',  # He
        'ו': 'V',  # Vav
        'ז': 'Z',  # Zayin
        'ח': 'Ch', # Chet
        'ט': 'T',  # Tet
        'י': 'Y',  # Yod
        'כ': 'K',  # Kaf
        'ל': 'L',  # Lamed
        'מ': 'M',  # Mem
        'נ': 'N',  # Nun
        'ס': 'S',  # Samekh
        'ע': 'O',  # Ayin
        'פ': 'P',  # Pe
        'צ': 'Tz', # Tzade
        'ק': 'Q',  # Qof
        'ר': 'R',  # Resh
        'ש': 'Sh', # Shin
        'ת': 'Th', # Tav
    }

    # Vollständige Übersetzung des BURUMUT-Bandes
    full_text = brt
    # Versuche, das Band in "Wörter" zu segmentieren
    # Heuristik: Vav (ו) und He (ה) sind oft Wortverbindungen

    # Erste Interpretation: rohe Sequenz
    return full_text, brt


def read_segments():
    """Lese das BURUMUT-Band in Segmenten.

    Wir teilen das 99-Zeichen-Band in 5-7 logische Segmente auf.
    """
    brt = burumut_to_hebr(BURUMUT)

    # Wort-für-Wort Lesung
    # Die BURUMUT-Sequenz ist ein PALINDROM-ähnliches Muster:
    # BURUMUTREFAMTU + NURESUTREGUMFAYAPS + UAZBEHIMLAZANR +
    # UAZBENOMBAMZHQRSANLR + UAZBEHIMLAZANR + UAZBENOMBARAZHQRSAN

    lateinisch = (
        'BURUMUTREFAMTU'   # 14 - "When he desired, from his beginning, and he spoke, seed"
        'NURESUTREGUMFAYAPS'  # 16 - Modul-Variante
        'UAZBEHIMLAZANR'  # 14 - "und er wanderte durch die Schrift"
        'UAZBENOMBAMZHQRSANLR'  # 19 - "und Same, Fisch-Anfang"
        'UAZBEHIMLAZANR'  # 14 - wiederholt
        'UAZBENOMBARAZHQRSAN'  # 18 - "und Same, Anfang"
    )
    # Total: 14+16+14+19+14+18 = 95, aber BURUMUT hat 99

    return lateinisch


# ============================================================================
# HAUPTPROGRAMM
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("📜 BURUMUT-SCHRIFT: Das vollständige 'Wort' der Schöpfung")
    print("="*70)
    print()

    brt = burumut_to_hebr(BURUMUT)

    # Übersetzer
    hebr_to_lat = {
        'א': 'A', 'ב': 'B', 'ג': 'G', 'ד': 'D', 'ה': 'H', 'ו': 'V',
        'ז': 'Z', 'ח': 'Ch', 'ט': 'T', 'י': 'Y', 'כ': 'K', 'ל': 'L',
        'מ': 'M', 'נ': 'N', 'ס': 'S', 'ע': 'O', 'פ': 'P', 'צ': 'Tz',
        'ק': 'Q', 'ר': 'R', 'ש': 'Sh', 'ת': 'Th',
    }

    hebr_meaning = {
        'א': 'Anfang',  'ב': 'Haus/Trennung', 'ג': 'Kamel/Wanderung',
        'ד': 'Tür',     'ה': 'Atem/Offenbarung', 'ו': 'Haken/und',
        'ז': 'Waffe',   'ח': 'Leben',  'ט': 'Gut',
        'י': 'Hand',    'כ': 'Handfläche', 'ל': 'Stab/Lernen',
        'מ': 'Wasser',  'נ': 'Same/Fisch', 'ס': 'Stütze',
        'ע': 'Auge',    'פ': 'Mund',  'צ': 'Jäger/Gerechtigkeit',
        'ק': 'Heilig',  'ר': 'Anfang/Kopf', 'ש': 'Flamme/Zahn',
        'ת': 'Vollendung/Ende',
    }

    print("DAS VOLLSTÄNDIGE BURUMUT-BAND IN 7 ABSCHNITTEN:")
    print("="*70)
    print()

    # Erste Aufteilung
    sections = [
        (0, 14, "BURUMUTREFAMTU", "Modul 1: Schöpfungs-Akt"),
        (14, 28, "NURESUTREGUMF", "Modul 2: Same-Vervielfachung"),
        (28, 42, "AYAPSUAZBEHIML", "Modul 3: Wanderung"),
        (42, 56, "AZANRUAZBENOMB", "Modul 4: Schrift-Vollendung"),
        (56, 70, "AMZHQRSANLRUAZ", "Modul 5: Heilige Struktur"),
        (70, 84, "BEHIMLAZANRUAZ", "Modul 6: Wiederholung"),
        (84, 99, "BENOMBARAZHQRSAN", "Modul 7: Vollendung"),
    ]

    for i, (start, end, latein, bedeutung) in enumerate(sections, 1):
        segment = brt[start:end]
        segment_latein = latein[:end-start]
        print(f"ABSCHNITT {i} (Position {start}-{end-1}, {end-start} Zeichen):")
        print(f"  Hebräisch: {segment}")
        print(f"  Lateinisch: {segment_latein}")
        print(f"  Bedeutung: {bedeutung}")
        # Wort-für-Wort-Übersetzung
        words = []
        for c in segment:
            if c in hebr_meaning:
                words.append(f"{c}={hebr_meaning[c]}")
        print(f"  Wörter: {', '.join(words[:8])}")
        # Gematria des Abschnitts
        gematria = sum(HEBR_VALUES.get(c, 0) for c in segment)
        print(f"  Gematria: {gematria}")
        print()

    # Gesamte Gematria
    total_gematria = sum(HEBR_VALUES.get(c, 0) for c in brt)
    print("="*70)
    print(f"GESAMT-GEMATRIA des BURUMUT-99-Bandes: {total_gematria}")
    print()

    # Vergleiche mit anderen wichtigen Zahlen
    print("ZAHLEN-BRÜCKEN:")
    print(f"  BURUMUT (lateinisch) = 1232")
    print(f"  BURUMUT + 137 = 1369 = 37² = Genesis 1:7")
    print(f"  BURUMUT (hebräisch, 99 AS) = {total_gematria}")
    print(f"  99 + 117 = 216 (Numeri-Boustrophedon)")
    print(f"  1924 = 4 × 13 × 37 (Wort der 15 Schritte)")
    print()

    # Speichere
    output = {
        'burumut_full_text': brt,
        'sections': [
            {
                'position': (start, end),
                'latein': latein[:end-start],
                'hebraisch': brt[start:end],
                'bedeutung': bedeutung,
                'gematria': sum(HEBR_VALUES.get(c, 0) for c in brt[start:end]),
            }
            for start, end, latein, bedeutung in sections
        ],
        'total_gematria': total_gematria,
    }
    with open("sources/burumut_full_text.json", "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("Status gespeichert in sources/burumut_full_text.json")
