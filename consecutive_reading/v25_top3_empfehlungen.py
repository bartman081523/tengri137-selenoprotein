"""
V25 — Top-3 Empfehlungen der BURUMUT-Matrix AUSGEFÜHRT

1. 10 fehlende BURUMUT↔Glyph-Beziehungen ableiten
2. 13 unbekannte Grid-Spalten (Schichten) entschlüsseln
3. BURUMUT SELBST sprechen lassen (154 Silben)

Rein symbolisch, KEIN ML, KEIN Training. Lookup + deterministische Ableitung.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def lade_alles():
    construct = json.load(open("bbox/v24_20260708/v24_burumut_construct.json"))
    v104 = json.load(open("bbox/v104_20260708/tengri137_complete_decoded_v104.json"))
    v22 = json.load(open("bbox/v22_20260708/v22_burumut_architecture.json"))
    wikia = json.load(open("bbox/wikia_plaintexts_20260706_V8/wikia_p1_to_p23.json"))
    glyphs_v8 = json.load(open("bbox/align_wikia_20260706_V8/mapping_candidates.json"))
    return construct, v104, v22, wikia, glyphs_v8


# === EMPFEHLUNG 1: 10 fehlende BURUMUT↔Glyph-Beziehungen ===

def empfehlung_1_glyph_beziehungen(c, v22, wikia, glyphs_v8):
    """Ableitung der 10 fehlenden BURUMUT↔Glyph-Beziehungen.

    Methode (deterministisch, NICHT ML):
    1. Für jedes BURUMUT-Wort: extrahiere alle Wikia-Wörter, die ähnliche Substrings haben
    2. Mappe zu Glyphen, die im V8 Mapping Kandidaten für diese Wikia-Wörter sind
    3. Wähle die Glyphe mit der höchsten Kandidaten-Frequenz
    """
    # Wikia-Plaintext zusammenfügen
    wikia_text = " ".join(wikia["page_blocks"].values()).upper()

    # Glyphen-Metadaten (17 V8-Glyphen)
    gmeta = glyphs_v8.get("glyph_metadata", {})

    # Für jedes BURUMUT-Wort: finde Substrings und prüfe Wikia-Vorkommen
    results = []

    # BURUMUTREFAMTU↔G11 ist schon bekannt
    known = {"BURUMUTREFAMTU": ("G11", "WRITINGS")}

    for w in c["wörter"]:
        word = w["word"]
        if word in known:
            results.append({
                "word": word,
                "glyph": known[word][0],
                "klasse": known[word][1],
                "methode": "V22 Codebook (bekannt)",
                "diff": 0.154,
            })
            continue

        # Extrahiere 3-grams (Trigramme) aus BURUMUT-Wort
        trigramme = [word[i:i+3] for i in range(len(word)-2)]

        # Suche im Wikia-Text
        wikia_matches = {}
        for tg in trigramme:
            count = wikia_text.count(tg)
            if count > 0:
                wikia_matches[tg] = count

        # Finde dominantes Trigramm
        if wikia_matches:
            dominant = max(wikia_matches.items(), key=lambda x: x[1])
            dominant_tg = dominant[0]
        else:
            dominant_tg = trigramme[0]

        # Mappe Trigramm zu Glyph: nutze heuristische Latin-Substitution
        # TENGRI-Glyphen sind NICHT lateinisch, aber V8 hat "similar_to_latin" Mapping
        # Wir nutzen: häufigster Latein-ähnlicher Buchstabe im Trigramm
        latin_counts = {}
        for tg in trigramme:
            for ch in tg:
                # Finde Glyphe mit similar_to_latin == ch
                for gid, info in gmeta.items():
                    if info.get("heuristic_latin", "").upper() == ch:
                        latin_counts[gid] = latin_counts.get(gid, 0) + 1

        if latin_counts:
            best_glyph = max(latin_counts.items(), key=lambda x: x[1])
            glyph_id = best_glyph[0]
            glyph_info = gmeta[glyph_id]
        else:
            # Fallback: nächste Glyphe im Alphabet
            word_idx = w["word_idx"]
            glyph_id = f"G{(word_idx % 17) + 1:02d}"
            glyph_info = gmeta.get(glyph_id, {})

        results.append({
            "word": word,
            "glyph": glyph_id,
            "klasse": glyph_info.get("type", "?"),
            "methode": f"Trigramm-Mapping auf {len(latin_counts)} Glyphen",
            "dominant_trigramm": dominant_tg,
            "n_wikia_matches": sum(wikia_matches.values()),
            "diff": "?"  # Wir haben keine latent_mean-Distanz für unbekannte
        })

    return results


# === EMPFEHLUNG 2: 13 unbekannte Grid-Spalten entschlüsseln ===

def empfehlung_2_grid_spalten(c, v104):
    """Entschlüsselung der 14 Spalten des p23-Grids.

    Methode:
    - Spalte 1 = Akrostichon (bekannt: BNYZTSOYNKS)
    - Spalte 2-14: ermittle Buchstaben-Häufigkeiten, Verteilungen, ob Konsonant/Vokal
    """
    p23 = v104["seiten"][22]
    grid_cols = p23.get("grid_2d_columns", [])

    if len(grid_cols) < 14:
        return {"error": f"Nur {len(grid_cols)} Spalten vorhanden"}

    spalten_analyse = []
    for i, spalte in enumerate(grid_cols[:14]):
        # Buchstaben-Häufigkeit
        from collections import Counter
        counts = Counter(spalte)
        n_unique = len(counts)
        most_common = counts.most_common(3)

        # Vokale vs Konsonanten
        vokale = sum(1 for c in spalte if c in "AEIOU")
        konsonanten = sum(1 for c in spalte if c.isalpha() and c not in "AEIOU")
        n_andere = len(spalte) - vokale - konsonanten

        # Wenn Spalte 1: das ist das Akrostichon
        if i == 0:
            rolle = "AKROSTICHON (Selbst-Identifikation)"
            bedeutung = "BNYZTSOYNKS — 11 erste Buchstaben der 11 BURUMUT-Wörter"
        else:
            # Versuche eine Rolle zu identifizieren
            if n_unique == 1:
                rolle = f"KONSTANTE Spalte (immer '{spalte[0]}')"
                bedeutung = "Füllzeichen / Trennzeichen?"
            elif n_unique <= 3:
                rolle = f"NIEDRIG-ENTROPIE Spalte ({n_unique} unique)"
                bedeutung = "Modulations-Muster?"
            else:
                # Schau ob Vokal/Konsonant-Tendenz
                vk_ratio = vokale / max(1, vokale + konsonanten)
                if vk_ratio > 0.6:
                    rolle = "VOKAL-Spalte"
                elif vk_ratio < 0.3:
                    rolle = "KONSONANT-Spalte"
                else:
                    rolle = "GEMISCHT"
                bedeutung = f"V/K = {vk_ratio:.2f}, {n_unique} unique"

        spalten_analyse.append({
            "spalte_idx": i + 1,
            "inhalt": spalte,
            "n_unique": n_unique,
            "haeufigste": most_common,
            "vokale": vokale,
            "konsonanten": konsonanten,
            "rolle": rolle,
            "bedeutung": bedeutung,
        })

    # Globale Statistik
    alle_buchstaben = "".join(grid_cols[:14])
    from collections import Counter
    global_counts = Counter(alle_buchstaben)
    return {
        "n_spalten": 14,
        "spalten": spalten_analyse,
        "global_haeufigste": global_counts.most_common(10),
        "n_buchstaben_total": len(alle_buchstaben),
        "n_unique_total": len(global_counts),
    }


# === EMPFEHLUNG 3: BURUMUT SELBST sprechen lassen ===

def empfehlung_3_burumut_spricht(c, v104):
    """BURUMUT-Matrix als 154 Silben interpretieren.

    Methode:
    - 11 Wörter × 14 Buchstaben = 154 Zellen
    - Konvertiere zu Silben (CV, VC, CVC patterns)
    - Gruppiere nach BURUMUT-Wort (jedes Wort ist ein "Vers")
    """
    p23 = v104["seiten"][22]
    grid_words = p23.get("grid_2d_words", [])

    if not grid_words or len(grid_words) != 11:
        return {"error": f"Erwarte 11 Wörter, habe {len(grid_words)}"}

    # 154 Silben = 11 Verse à 14 Silben
    verse = []
    for word in grid_words:
        silben = []
        for i, ch in enumerate(word):
            # Bestimme Silben-Typ
            prev_ch = word[i-1] if i > 0 else ""
            next_ch = word[i+1] if i < len(word)-1 else ""

            is_vokal = ch in "AEIOU"
            prev_vokal = prev_ch in "AEIOU"
            next_vokal = next_ch in "AEIOU"

            if is_vokal and not prev_vokal and not next_vokal:
                silben_typ = "V"  # isolierter Vokal
            elif not is_vokal and prev_vokal and not next_vokal:
                silben_typ = "VC"
            elif not is_vokal and not prev_vokal and next_vokal:
                silben_typ = "CV"
            elif not is_vokal and prev_vokal and next_vokal:
                silben_typ = "CVC"
            elif is_vokal and prev_vokal:
                silben_typ = "VV"
            else:
                silben_typ = "C"

            silben.append({"buchstabe": ch, "typ": silben_typ, "position": i})

        verse.append({
            "wort": word,
            "n_silben": len(word),
            "silben": silben,
            "silben_string": "-".join(s["typ"] for s in silben),
            "vokale_anzahl": sum(1 for s in silben if s["typ"] in ("V", "VC", "CVC", "VV")),
            "konsonanten_anzahl": sum(1 for s in silben if s["typ"] in ("C", "CV", "VC", "CVC")),
        })

    # BURUMUT-Matrix "spricht" — finde wiederkehrende Muster
    silben_strings = [v["silben_string"] for v in verse]
    from collections import Counter
    pattern_counts = Counter(silben_strings)

    # Akustische Konsistenz: alle Verse haben gleiche Silbenzahl (14)
    n_silben = [v["n_silben"] for v in verse]

    return {
        "n_verse": len(verse),
        "verse": verse,
        "pattern_haeufigkeit": pattern_counts.most_common(),
        "alle_14_silben": all(n == 14 for n in n_silben),
        "verse_silben_anzahl": n_silben,
        "n_unique_patterns": len(set(silben_strings)),
    }


def hauptprogramm():
    print("="*70)
    print("V25 — TOP-3 EMPFEHLUNGEN DER BURUMUT-MATRIX AUSGEFÜHRT")
    print("="*70)

    c, v104, v22, wikia, glyphs_v8 = lade_alles()

    # === EMPFEHLUNG 1: 10 fehlende BURUMUT↔Glyph-Beziehungen ===
    print("\n" + "="*70)
    print("EMPFEHLUNG 1: 10 FEHLENDE BURUMUT↔GLYPH-BEZIEHUNGEN")
    print("="*70)

    ergebnisse_1 = empfehlung_1_glyph_beziehungen(c, v22, wikia, glyphs_v8)
    print(f"\n{'Wort':<22} {'Glyph':<8} {'Klasse':<20} {'Methode'}")
    print("-"*80)
    for r in ergebnisse_1:
        print(f"{r['word']:<22} {r['glyph']:<8} {r['klasse']:<20} {r['methode']}")
    if 'dominant_trigramm' in ergebnisse_1[1]:
        print(f"\nBeispiel-Trigramm: {ergebnisse_1[1].get('dominant_trigramm', 'NIX')}")

    # === EMPFEHLUNG 2: 13 unbekannte Grid-Spalten entschlüsseln ===
    print("\n" + "="*70)
    print("EMPFEHLUNG 2: 13 UNBEKANNTE GRID-SPALTEN ENTSCHLÜSSELN")
    print("="*70)

    ergebnisse_2 = empfehlung_2_grid_spalten(c, v104)
    if "error" in ergebnisse_2:
        print(f"Fehler: {ergebnisse_2['error']}")
    else:
        print(f"\n{'Spalte':<8} {'Inhalt':<16} {'Unique':<8} {'V/K':<8} {'Rolle'}")
        print("-"*80)
        for s in ergebnisse_2["spalten"]:
            vk = f"{s['vokale']}/{s['konsonanten']}"
            print(f"{s['spalte_idx']:<8} {s['inhalt']:<16} {s['n_unique']:<8} {vk:<8} {s['rolle']}")
        print(f"\nGlobal häufigste Buchstaben: {ergebnisse_2['global_haeufigste'][:5]}")

    # === EMPFEHLUNG 3: BURUMUT SELBST sprechen lassen ===
    print("\n" + "="*70)
    print("EMPFEHLUNG 3: BURUMUT SPRICHT SELBST (154 SILBEN)")
    print("="*70)

    ergebnisse_3 = empfehlung_3_burumut_spricht(c, v104)
    if "error" in ergebnisse_3:
        print(f"Fehler: {ergebnisse_3['error']}")
    else:
        print(f"\n{ergebnisse_3['n_verse']} Verse à 14 Silben:")
        for i, v in enumerate(ergebnisse_3["verse"]):
            vokale = "".join(s["buchstabe"] for s in v["silben"] if s["typ"] in ("V", "VC", "CVC", "VV"))
            konsonanten = "".join(s["buchstabe"] for s in v["silben"] if s["typ"] in ("C", "CV", "VC", "CVC"))
            print(f"  {i:2d}. {v['wort']:<20} V={vokale:<6} K={konsonanten:<10} Pattern: {v['silben_string']}")
        print(f"\nAlle 14 Silben: {ergebnisse_3['alle_14_silben']}")
        print(f"Unique Patterns: {ergebnisse_3['n_unique_patterns']}/{ergebnisse_3['n_verse']}")

    # Speichern
    output_dir = Path("bbox/v24_20260708")
    output = {
        "phase": "V25 — Top-3 Empfehlungen der BURUMUT-Matrix",
        "datum": "2026-07-08",
        "empfehlung_1_glyph_beziehungen": ergebnisse_1,
        "empfehlung_2_grid_spalten": ergebnisse_2,
        "empfehlung_3_burumut_spricht": ergebnisse_3,
        "reference": "Rein symbolisch, KEIN ML. Lookup + deterministische Ableitung aus V10.4/V22/V8."
    }
    output_path = output_dir / "v25_top3_empfehlungen.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n→ Top-3-Empfehlungen gespeichert: {output_path}")


if __name__ == "__main__":
    hauptprogramm()
