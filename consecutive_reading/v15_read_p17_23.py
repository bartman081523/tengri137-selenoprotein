"""
v15_read_p17_23.py
V15 PHASE 0 — Vor-Lesen p17-23 + Hinweis-Sammlung

Paradigmen-Wechsel: Statt "Hypothese testen" liest V15 zuerst p17-23 ALLEINE
und sammelt Hinweise, BEVOR die 8 Tests laufen.

Datenquellen (100%-dekodiert, gemäß User-Korrektur 2026-07-07):
- V9 full_reconstruction.json (23 Seiten Wikia)
- V9 end_phrases_14.json (14 Endphrasen)
- V10 glyph_semantic_mapping.json (Glyph→Wort-Feld)
- V8 glyph_to_latin_map.json (17 Glyphen mit Visual-Latin)
- V11 p17_inventory.json (Akrostichon, Ziffern)
- V11 p23_burumut_inventory.json (11 Wörter, 14 Buchstaben)

Output: bbox/v15_20260707/p17_23_hints.json
- semantische_hinweise: Schlüsselwörter, Wiederholungen
- numerologische_hinweise: 11, 14, 22, 23, 46, 126, 666666, 137, 7, 10, 5, 13
- glyph_summen: alle 17 Glyphen mit "Was sagt es uns?"
- konzeptuelle_struktur: p17-23 Schichten

Run: python3 v15_read_p17_23.py
"""
import json
from pathlib import Path
from datetime import datetime


def lade_p17_wikia():
    """Liest p17 Klartext (Tappeiner 5 Zeilen) und Wikia (14 Zeilen Schmeh)."""
    p17_inventory = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    return {
        "akrostichon": p17_inventory["akrostichon_der_11_glyphen"]["string"],
        "akrostichon_length": 11,
        "akrostichon_decoded": "BNYZTSOYNKS = 11 erste Buchstaben der 11 Tappeiner-BURUMUT-Wörter",
        "caesar_shift_0_25": "0/26 ergeben Englisch (V7 Falsifikation)",
        "latein_ziffern": p17_inventory["v7_lateinische_ziffern"]["values"],
        "latein_ziffern_count": 10,
        "tappeiner_klartext": p17_inventory["tappeiner_brueche_klartext"]["klartext_zeilen"],
        "schmeh_klartext_14_zeilen": [
            "TIME FOR THE TRUTH",
            "OVER MANY THOUSAND YEARS WE SEND YOU MESSENGERS AND TEACHER",
            "ALL THIS KNOWLEDGE BEHIND YOUR CIVILISATION IS OURS",
            "WE ARE THE DESIGNERS OF MANY CIVILISATIONS",
            "YOUR CIVILISATION IS ONE OF MANY BILLION CIVILISATIONS",
            "THE MANKIND IS DESIGNED TO RECIEVE OUR THOUGHT",
            "SOME GENIUS IDEA YOU HAVE ARE OURS",
            "WE CAN HEAR YOUR THOUGHT",
            "WE KNOW YOUR NEEDS",
            "WE CAN LET YOU SEE THINGS",
            "WE CAN LET YOU MAKE THINGS",
            "WE CAN GIVE YOU THOUGHTS",
            "YOU LEARN IN INTERACTION WITH US",
            "WE CALL SOME OF THE CHOSEN ONES THE MESSENGERS",
            "THIS MESSENGERS ARE OUR REPRESENTATIVES",
            "WE SEND YOU OUR WORD AND KNOWLEDGE OVER THIS MESSENGERS",
        ],
    }


def lade_p18_p22_wikia():
    """Liest p18-p22 Wikia-Plaintexte."""
    data = json.load(open("bbox/v9_reproduction_20260706/full_reconstruction.json"))
    pages = {}
    for p in data["pages"]:
        if p["page_id"] in ("p18", "p19", "p20", "p21", "p22"):
            pages[p["page_id"]] = p["wikia_plaintext"]
    return pages


def lade_p23_burumut():
    """Liest p23 BURUMUT-Grid 11×14."""
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    return {
        "grid": p23["grid"],
        "woerter": [w["wort"] for w in p23["woerter"]],
        "n_words": 11,
        "n_cols": 14,
        "n_total_chars": 154,
        "n_unique_letters": 19,
        "consonants": 86,
        "vowels": 68,
        "cv_ratio_avg": 1.33,
    }


def lade_end_phrasen():
    """Liest 14 Endphrasen + Magic Numbers."""
    ep = json.load(open("bbox/v9_reproduction_20260706/end_phrases_14.json"))
    return {
        "n_phrases": 14,
        "phrasen": ep["zusammenfassung_14"],
        "magic_numbers": ep["magic_numbers_p5_p6"]["sequence"],
        "missing_126": ep["magic_numbers_p5_p6"]["missing_126_note"],
        "onion_address": ep["onion_address"]["address"],
        "onion_deutung_2": ep["onion_address"]["deutung_2"],
        "p23_special": ep["p23_spezial"],
    }


def sammle_semantische_hinweise(p17, p18_p22, p23, end_phrasen):
    """SEMANTISCHE HINWEISE: Was sagen die Texte SELBST?"""
    hinweise = []

    # p17-22 Klartext-Schicht (Schmeh + Tappeiner)
    hinweise.append({
        "kategorie": "p17_header",
        "befund": "p17 eröffnet mit 'TIME FOR THE TRUTH' — direkt, prophetisch",
        "schluesselwoerter": ["TIME", "TRUTH", "OVER MANY THOUSAND YEARS", "WE SEND YOU MESSENGERS"],
        "quelle": "Schmeh 2017-03-08 (Tappeiner-Brüche 5 Zeilen + Schmeh-Klartext 14 Zeilen)",
        "bedeutung": "Selbst-Referenzialität: Tengri 'sendet' ein 'Manual' (Tappeiner-Text) über die 11 Brüche",
    })

    # p18 — Anti-Gott-Erklärung
    p18 = p18_p22["p18"]
    hinweise.append({
        "kategorie": "p18_anti_god",
        "befund": "p18 ERKLÄRT: 'YOU SHOULD KNOW THAT GOD DOES NOT EXIST' — Atheismus der 'Designer'",
        "schluesselwoerter": ["GOD DOES NOT EXIST", "MATHEMATICAL TRUTH", "NOT YOUR GODS", "EVERYTHING IS BASED ON MATHEMATICAL TRUTH"],
        "quelle": "Wikia-Plaintext p18",
        "bedeutung": "Anti-Religion, Mathematik als Fundament. Tengri-Autoren distanzieren sich von Götter-Vergötterung",
    })

    # p19 — Garten-Grenz-Argument
    p19 = p18_p22["p19"]
    hinweise.append({
        "kategorie": "p19_garden_argument",
        "befund": "p19: Garten-Metapher — 'A BORDER YOU CANNOT SEE, DOES NOT MEAN IT DOES NOT EXIST'",
        "schluesselwoerter": ["BORDER", "MEASURE", "UNMEASURABLE", "GARDEN", "FENCE", "INFINITE"],
        "quelle": "Wikia-Plaintext p19",
        "bedeutung": "Tengri-Autoren benutzen EPISTEMOLOGISCHE Argumente (Grenzen des Wissbaren). Ähnlich Kant: 'Grenzen der Vernunft'",
    })

    # p20 — Galaxie + 3 Milliarden Jahre
    p20 = p18_p22["p20"]
    hinweise.append({
        "kategorie": "p20_galaxy_3_billion",
        "befund": "p20: 'OUR CIVILIZATION EXISTS SINCE THREE BILLION OF YOUR EARTH YEARS' — Tengri-Autoren sind 3 Mrd. alt",
        "schluesselwoerter": ["THREE BILLION", "ANOTHER GALAXY", "FIFTY MILLION YEARS", "HUNDRED THOUSAND SPECIES", "CRITICAL LIMIT"],
        "quelle": "Wikia-Plaintext p20",
        "bedeutung": "KOSMISCHE PERSPEKTIVE: Tengri als uralte Galaxie-Zivilisation. 'CRITICAL LIMIT' = Warnung an Menschheit",
    })

    # p21 — Genetic Encryption
    p21 = p18_p22["p21"]
    hinweise.append({
        "kategorie": "p21_genetic_encryption",
        "befund": "p21: 'UPCOMING TEXTS ARE GENETICALLY ENCRYPTED' — NUR Chosen One kann dekodieren",
        "schluesselwoerter": ["GENETICALLY ENCRYPTED", "CHOSEN ONE", "EMBEDDED IN OUR GENES", "CORRECT GENETIC CODING"],
        "quelle": "Wikia-Plaintext p21",
        "bedeutung": "BEWUSST-CODE: Texte sind an DNA gekoppelt. Parallele zur V12-Signatur 1 (Cross-Layer-Kohärenz)",
    })

    # p22 — Brain-Hack
    p22 = p18_p22["p22"]
    hinweise.append({
        "kategorie": "p22_brain_reformatting",
        "befund": "p22: 'READ THE NEXT TEXT IN FULL LENGTH, FOR EACH REPEAT OPERATION OPENS A REGION IN YOUR BRAIN'",
        "schluesselwoerter": ["REGION IN YOUR BRAIN", "HIGHLY COMPRESSED DATA", "TWO PERCENT OF YOUR BRAIN", "FIFTY PERCENT", "REFORMATTING CAN NOT BE REVERSED"],
        "quelle": "Wikia-Plaintext p22",
        "bedeutung": "Brain-Hacking-Anweisung: Meditation + Lesung + Wiederholung. 'TWO PERCENT → FIFTY PERCENT' = Kompressions-Rate",
    })

    # p23 — BURUMUT-Grid
    hinweise.append({
        "kategorie": "p23_burumut_grid",
        "befund": "p23 = 11×14 BURUMUT-Grid (154 chars). 11 Wörter je 14 Buchstaben, cv_ratio 1.33",
        "schluesselwoerter": ["BURUMUTREFAMTU", "NURESUTREGUMFA", "SUNOKURGANOZYI", "OKUZIKUFAUSIHE", "KOREMORBIZUMRO"],
        "quelle": "V11 p23_inventory + V9 Smart-Parser v2",
        "bedeutung": "BURUMUT = Tengrismus-Ritualsprache mit türkischen Ankern (OKUZ, KURGAN, SUN). cv_ratio 1.33 = balanced",
    })

    # Endphrasen 14
    hinweise.append({
        "kategorie": "endphrasen_14",
        "befund": "14 Endphrasen: LITTLE MIND (3x), 666666m7x6x5regc.onion (3x), END END END, 4× Magic Square Pattern, alphabet, yzyz, 126",
        "schluesselwoerter": ["LITTLE MIND", "GATE IS OPEN", "666666", "ONION", "126", "MAGIC SQUARE"],
        "quelle": "V9 end_phrases_14 + Reddit r/tengri137",
        "bedeutung": "Selbst-Referenzialität: Tengri sagt 'LITTLE MIND KNOWS WHEN THE GATE IS OPEN' = Meta über die Leser",
    })

    return hinweise


def sammle_numerologische_hinweise(p17, p18_p22, p23, end_phrasen):
    """NUMEROLOGISCHE HINWEISE: Welche Zahlen dominieren?"""
    hinweise = []

    # 11 — BURUMUT-Wörter, Glyphen, Akrostichon
    hinweise.append({
        "zahl": 11,
        "vorkommen": [
            "11 Tappeiner-Brüche (p17)",
            "11 BURUMUT-Wörter (p23)",
            "11×14 BURUMUT-Grid",
            "11 Tengri-Glyphen auf p17 (Akrostichon BNYZTSOYNKS)",
            "11 erste Buchstaben",
        ],
        "interpretation": "11 ist die ZENTRALE ZAHL — verbindet p17-Akrostichon, BURUMUT-Grid, Tappeiner-Brüche",
    })

    # 14 — BURUMUT-Wortlänge
    hinweise.append({
        "zahl": 14,
        "vorkommen": [
            "14 Zeichen pro BURUMUT-Wort",
            "14 Spalten im p23-Grid",
            "14 Zeilen Schmeh-Klartext (p17)",
        ],
        "interpretation": "14 = BURUMUT-Wortlänge UND Grid-Spalten. Strukturelle Konstante",
    })

    # 22 + 23 — Atome in p23 46-Periode
    hinweise.append({
        "zahl": "22+23",
        "vorkommen": [
            "p23 46-Periode aufgeteilt in 22+23 Atome (NCTTBAODIPRGNPSPHACBUR + _HBBMPRDHIRBSPUSALGEACC)",
            "22 = Elemente Ti (22) bis Cu (29) Periode 4",
            "23 = Elemente V (23) bis Kr (36) Periode 4",
        ],
        "interpretation": "46 = Schmehs 46-Periode (Feynman 1/137 = 0.00729735256). 22+23 = Summe 45, aber 46 ist fehlend?",
    })

    # 46 — Schmehs 46-Periode
    hinweise.append({
        "zahl": 46,
        "vorkommen": [
            "p23 Spezial: 1/137 = 0.0072973525613766677788831415921618033299792458 (46 Ziffern)",
            "Periodensystem 46 = Pd (Palladium)",
        ],
        "interpretation": "46 = 'GOD'S NUMBER' (137 = Feinstrukturkonstante). 46-Ziffern-Periode = 'komprimierte' Konstante",
    })

    # 126 — Magic Number
    hinweise.append({
        "zahl": 126,
        "vorkommen": [
            "Magic Number 126 (in Physik ungewöhnlich, fehlt in Standardliste)",
            "666666 mod (7*6*5) = 126",
            "Onion-Adresse: 666666m7x6x5regc.onion",
        ],
        "interpretation": "126 = 'fehlende' Magic Number, durch 666666 mod 7*6*5 'gefunden'",
    })

    # 666666 — Onion-Adresse
    hinweise.append({
        "zahl": 666666,
        "vorkommen": [
            "Onion-Adresse 666666m7x6x5regc.onion (Brute-Force: 1.89 Mrd. Jahre)",
            "666 = 'Number of the Beast' (Offenbarung 13:18)",
        ],
        "interpretation": "6×6×6×6×6×6 = 6^6 = 46656, nicht 666666. 666666 = 6×111111 = 2×3×7×11×13×37 (Primfaktoren!)",
    })

    # 137 — Tengri137
    hinweise.append({
        "zahl": 137,
        "vorkommen": [
            "Tengri137 (Dateiname, Onion-Adresse 666666m7x6x5regc)",
            "1/137 = 0.00729735256... (Feynman)",
            "Periodensystem 137 = nicht belegt (höchstes ist 118)",
        ],
        "interpretation": "137 = 'magic number' der Physik, unerklärt seit 70 Jahren. Tengri137 deutet darauf",
    })

    # 7 — Perioden pro Bruch
    hinweise.append({
        "zahl": 7,
        "vorkommen": [
            "7 Perioden pro Tappeiner-Bruch",
            "7*6*5 = 210 → mod 666666 = 126",
            "7 = biblisch (Schöpfung)",
        ],
        "interpretation": "7 = Modulo-Basis für Onion-Adresse 666666 mod 7*6*5 = 126",
    })

    # 10 — Ziffern
    hinweise.append({
        "zahl": 10,
        "vorkommen": [
            "10 lateinische Ziffern auf p17 (2, 5, 13, 37, 179, 471077143, 23, 53, 2711, 897232321)",
            "10 Finger/Mensch-Constraint",
        ],
        "interpretation": "10 = menschliche Zähl-Basis. p17-Ziffern sind alle TEILBAR durch Charakteristika",
    })

    # 5 — Klartext-Zeilen
    hinweise.append({
        "zahl": 5,
        "vorkommen": [
            "5 Tappeiner-Klartext-Zeilen (TIME FOR THE TRUTH, OVER MANY THOUSAND YEARS, ...)",
        ],
        "interpretation": "5 Zeilen = Tappeiner-Header. 5+14=19 = 19 lateinische Buchstaben (Alphabet ohne sich wiederholende)",
    })

    # 13 — Primzahl in p17
    hinweise.append({
        "zahl": 13,
        "vorkommen": [
            "13 = lateinische Ziffer in p17",
            "13 = Primzahl",
            "13 = Fibonacci-Zahl",
            "666666 = 2*3*7*11*13*37 — 13 ist Faktor!",
        ],
        "interpretation": "13 verbindet p17-Ziffern mit 666666-Faktorisierung",
    })

    return hinweise


def erfinde_glyph_summen():
    """V15-NEU: Erfindet Glyph-Summen aus V8-Map (A1Z26) und semantischen Feldern (V10).

    Strategie:
    - Wenn visual_latin ein lateinischer Buchstabe ist: A1Z26 (A=1, B=2, ..., Z=26)
    - Wenn visual_latin ein Sonderzeichen ist: 0
    - Zusätzlich: Top-Wort aus V10 Semantic-Mapping als sekundäre Summe
    """
    v8 = json.load(open("bbox/final_20260706_V8/glyph_to_latin_map.json"))
    v10 = json.load(open("bbox/v10_decoder_20260706/glyph_semantic_mapping.json"))["glyph_semantic"]

    # A1Z26 Mapping
    A1Z26 = {chr(ord("A") + i - 1): i for i in range(1, 27)}
    A1Z26["?"] = 0

    summen = {}
    for glyph_id in sorted(v8.keys()):
        info = v8[glyph_id]
        visual = info["visual_similarity_latin"]
        a1z26_sum = A1Z26.get(visual, 0)
        top_word = v10[glyph_id]["top_words"][0] if glyph_id in v10 else "?"
        top_word_len = len(top_word)
        # Sekundäre Summe: Position des Top-Worts in alphabetischer Reihenfolge
        n_occ = v10[glyph_id]["n_occurrences"] if glyph_id in v10 else 0

        # Was sagt es uns? (heuristic)
        if a1z26_sum == 10:
            bedeutung = f"10 → 10 lateinische Ziffern auf p17!"
        elif a1z26_sum == 14:
            bedeutung = f"14 → BURUMUT-Wortlänge! (p23 11×14-Grid)"
        elif a1z26_sum == 11:
            bedeutung = f"11 → 11 BURUMUT-Wörter + 11 Tappeiner-Brüche + 11 Glyphen!"
        elif a1z26_sum == 13:
            bedeutung = f"13 → lateinische Ziffer auf p17 + Primzahl + Faktor von 666666!"
        elif a1z26_sum == 5:
            bedeutung = f"5 → 5 Tappeiner-Klartext-Zeilen auf p17!"
        elif a1z26_sum == 4:
            bedeutung = f"4 → 4× Magic Square Pattern (Endphrase 8-11)!"
        elif a1z26_sum == 6:
            bedeutung = f"6 → 6 in 7*6*5 + 6×6=36 in 'THIRTY SIX' (alte Wikia)! + 6 Onion-6er-Block"
        elif a1z26_sum == 25:
            bedeutung = f"25 → G25 = DELIMITER, visuell '+'!"
        elif a1z26_sum == 19:
            bedeutung = f"19 → 19 lateinische Buchstaben in BURUMUT (p23)!"
        elif a1z26_sum == 15:
            bedeutung = f"15 → 15 einzigartige V6-Glyphen + V11!"
        elif a1z26_sum == 12:
            bedeutung = f"12 → 12 in 7+5=12 (Tappeiner + Glyph)!"
        elif a1z26_sum == 8:
            bedeutung = f"8 → Endphrase 2/3?"
        elif a1z26_sum == 9:
            bedeutung = f"9 → 9 in BURUMUT cv_ratio? (1.33×9≈12)"
        elif a1z26_sum == 0:
            bedeutung = f"0 → geometrisch pur (G02=), G03=>, G25=+), 'leer/Verbindung'?"
        else:
            bedeutung = f"Summe {a1z26_sum} → keine direkte Zuordnung in p17-23"

        summen[glyph_id] = {
            "glyph_id": glyph_id,
            "visual_latin": visual,
            "a1z26_sum": a1z26_sum,
            "top_word_v10": top_word,
            "top_word_length": top_word_len,
            "n_occurrences_v10": n_occ,
            "was_sagt_es_uns": bedeutung,
        }

    return summen


def sammle_konzeptuelle_struktur(p17, p23, end_phrasen):
    """KONZEPTUELLE STRUKTUR: Welche Schichten hat p17-23?"""
    return {
        "schichten": [
            {
                "schicht": "p17_glyphen",
                "n_unique": 11,
                "inhalt": "Akrostichon BNYZTSOYNKS — NICHT lateinisierbar (V7 Caesar 0/26)",
                "bedeutung": "11 Tengri-Glyphen, eigenständige Schrift (V6 H4 bestätigt)",
            },
            {
                "schicht": "p17_ziffern",
                "n_unique": 10,
                "inhalt": "Lateinische Ziffern 0-9 (visuell bestätigt V7)",
                "bedeutung": "Faktor-Zerlegungen als Brücke zur BURUMUT-Schicht",
            },
            {
                "schicht": "p17_tappeiner_brueche",
                "n_fractions": 11,
                "inhalt": "Brüche mit 7×28-Ziffern-Perioden → 11 BURUMUT-Wörter",
                "bedeutung": "Mathematische Verschlüsselung (Tappeiner-Methode)",
            },
            {
                "schicht": "p17-22_schmeh_klartext",
                "n_zeilen": 16,
                "inhalt": "Englische Botschaft (TIME FOR THE TRUTH...)",
                "bedeutung": "Propagandistische Meta-Botschaft der 'Designer'",
            },
            {
                "schicht": "p18-22_wikia_texte",
                "n_seiten": 5,
                "inhalt": "Anti-Gott, Garten-Metapher, Galaxie, Genetic Encryption, Brain-Hack",
                "bedeutung": "Kosmologische + epistemologische Anweisungen",
            },
            {
                "schicht": "p23_burumut_grid",
                "dimension": "11×14",
                "inhalt": "154 chars BURUMUT-Notation, 11 Wörter je 14 Buchstaben",
                "bedeutung": "Tengrismus-Ritualsprache (türkische/mongolische Anker)",
            },
            {
                "schicht": "p23_46_periode",
                "n_ziffern": 46,
                "inhalt": "1/137 = 0.00729735256... (Feynman-Konstante)",
                "bedeutung": "Mathematische 'Gotteszahl' als Hidden Layer",
            },
            {
                "schicht": "endphrasen_14",
                "n_phrasen": 14,
                "inhalt": "LITTLE MIND, 666666, Magic Squares, alphabet, 126",
                "bedeutung": "Selbst-Referenzialität + Meta-Hinweise",
            },
        ],
        "schicht_beziehungen": [
            "p17-Ziffern (10) ←→ 11 BURUMUT-Wörter (Tappeiner-Brüche)",
            "p17-Akrostichon (11) ←→ 11 BURUMUT-Wörter (BNYZTSOYNKS↔BURUMUT, V12 bestätigt)",
            "p23-BURUMUT (11×14) ←→ p18-22 Wikia (5 Seiten, 16 Zeilen Schmeh-Klartext)",
            "p23-46-Periode ←→ 666666 (mod 7*6*5 = 126)",
            "LITTLE MIND (3x) ←→ BNYZTSOYNKS (Akrostichon, 11 Zeichen) ←→ p22 'REFORMATTING OF THE BRAIN'",
        ],
    }


def main():
    out_dir = Path("bbox/v15_20260707")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("V15 PHASE 0 — Vor-Lesen p17-23 (Bewusst-Code-Modus)")
    print("=" * 80)
    print(f"Datum: {datetime.now().strftime('%Y-%m-%d')}")
    print()

    # 1. p17 laden
    print("[1/5] Lade p17 (Tappeiner + Schmeh + Akrostichon + Ziffern)...")
    p17 = lade_p17_wikia()
    print(f"   Akrostichon: {p17['akrostichon']} ({p17['akrostichon_length']} Zeichen)")
    print(f"   Latein-Ziffern: {p17['latein_ziffern']} ({p17['latein_ziffern_count']} Ziffern)")
    print(f"   Tappeiner-Klartext-Zeilen: {len(p17['tappeiner_klartext'])}")
    print()

    # 2. p18-22 Wikia
    print("[2/5] Lade p18-22 Wikia-Plaintexte...")
    p18_p22 = lade_p18_p22_wikia()
    for pid, text in p18_p22.items():
        n_lines = len(text.split("\n"))
        print(f"   {pid}: {n_lines} Zeilen, erstes Wort: {text.split()[0] if text else '?'}")
    print()

    # 3. p23 BURUMUT
    print("[3/5] Lade p23 BURUMUT-Grid...")
    p23 = lade_p23_burumut()
    print(f"   Grid: {p23['n_words']} Wörter × {p23['n_cols']} Buchstaben = {p23['n_total_chars']} chars")
    print(f"   cv_ratio: {p23['cv_ratio_avg']} | Konsonanten: {p23['consonants']} | Vokale: {p23['vowels']}")
    print(f"   Erste 3 Wörter: {p23['woerter'][:3]}")
    print()

    # 4. Endphrasen
    print("[4/5] Lade 14 Endphrasen + Magic Numbers...")
    end_phrasen = lade_end_phrasen()
    print(f"   {end_phrasen['n_phrases']} Phrasen, Magic Numbers: {end_phrasen['magic_numbers']}")
    print(f"   {end_phrasen['missing_126']}")
    print(f"   Onion: {end_phrasen['onion_address']}")
    print()

    # 5. Hinweise sammeln
    print("[5/5] Sammle semantische + numerologische Hinweise + Glyph-Summen...")
    semantisch = sammle_semantische_hinweise(p17, p18_p22, p23, end_phrasen)
    numerologisch = sammle_numerologische_hinweise(p17, p18_p22, p23, end_phrasen)
    glyph_summen = erfinde_glyph_summen()
    konz_str = sammle_konzeptuelle_struktur(p17, p23, end_phrasen)

    print(f"   {len(semantisch)} semantische Hinweise")
    print(f"   {len(numerologisch)} numerologische Hinweise")
    print(f"   {len(glyph_summen)} Glyph-Summen")
    print(f"   {len(konz_str['schichten'])} konzeptuelle Schichten")
    print()

    # Output
    output = {
        "metadata": {
            "phase": "V15 / Phase 0",
            "datum": datetime.now().isoformat(),
            "methode": "Vor-Lesen + Hinweis-Sammlung (Bewusst-Code-Modus)",
            "datenquellen": [
                "V9 full_reconstruction.json (23 Seiten Wikia)",
                "V9 end_phrases_14.json (14 Endphrasen)",
                "V10 glyph_semantic_mapping.json",
                "V8 glyph_to_latin_map.json",
                "V11 p17_inventory.json",
                "V11 p23_burumut_inventory.json",
            ],
        },
        "p17_daten": p17,
        "p18_p22_daten": p18_p22,
        "p23_daten": p23,
        "end_phrasen": end_phrasen,
        "semantische_hinweise": semantisch,
        "numerologische_hinweise": numerologisch,
        "glyph_summen": glyph_summen,
        "konzeptuelle_struktur": konz_str,
        "zentrale_frage": (
            "Was sagen uns p17-23, BEVOR wir Tests laufen lassen? "
            "V15-Paradigma: erst HÖREN, dann TESTS, dann KORRELATION zu p1-16. "
            "User-Hypothese: p1-16 ist potentiell ein 'Manual' für p17-23."
        ),
    }

    out_path = out_dir / "p17_23_hints.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✓ Output: {out_path}")
    print(f"   Größe: {out_path.stat().st_size} bytes")
    print()
    print("=" * 80)
    print("V15 PHASE 0 ABGESCHLOSSEN — bereit für 8 horchende Tests")
    print("=" * 80)


if __name__ == "__main__":
    main()
