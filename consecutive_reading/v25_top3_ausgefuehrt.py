"""
V25 Top-3 nächste Schritte AUSGEFÜHRT

1. V/K-Binärcode aus 14 Spalten
2. BURUMUT-Substrings in p1-p22
3. Echtes Codebook (BURUMUT↔Glyph mit latent_mean)
"""

import json
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))


def lade_alles():
    construct = json.load(open("bbox/v24_20260708/v24_burumut_construct.json"))
    v104 = json.load(open("bbox/v104_20260708/tengri137_complete_decoded_v104.json"))
    v22 = json.load(open("bbox/v22_20260708/v22_burumut_architecture.json"))
    wikia = json.load(open("bbox/wikia_plaintexts_20260706_V8/wikia_p1_to_p23.json"))
    return construct, v104, v22, wikia


# === SCHRITT 1: V/K-Binärcode aus 14 Spalten ===

def schritt_1_vk_binärcode(c, v104):
    """Berechne 14-bit V/K-Code für jedes BURUMUT-Wort."""
    grid_words = v104["seiten"][22].get("grid_2d_words", [])

    ergebnisse = []
    for i, word in enumerate(grid_words):
        bits = []
        for ch in word:
            if ch in "AEIOU":
                bits.append("1")
            else:
                bits.append("0")
        bit_code = "".join(bits)
        # Berechne den numerischen Wert
        n_value = int(bit_code, 2)
        ergebnisse.append({
            "word": word,
            "position": i,
            "vk_code": bit_code,
            "vk_value": n_value,
            "n_vokale": sum(1 for b in bits if b == "1"),
            "n_konsonanten": sum(1 for b in bits if b == "0"),
        })

    # Suche nach Mustern
    n_values = [e["vk_value"] for e in ergebnisse]
    n_unique = len(set(n_values))

    # Welche Wörter sind unique im Binärcode?
    seen = {}
    for e in ergebnisse:
        v = e["vk_value"]
        if v not in seen:
            seen[v] = []
        seen[v].append(e["word"])

    duplicates = {v: ws for v, ws in seen.items() if len(ws) > 1}

    return {
        "n_woerter": len(ergebnisse),
        "n_unique_codes": n_unique,
        "codes": ergebnisse,
        "duplicates": duplicates,
    }


# === SCHRITT 2: BURUMUT-Substrings in p1-p22 ===

def schritt_2_substrings_in_p1_p22(c, v104, wikia):
    """Suche nach 4-7-Buchstaben-Substrings der BURUMUT-Wörter in p1-p22."""
    grid_words = v104["seiten"][22].get("grid_2d_words", [])

    # Sammle alle p1-p22 Wikia-Texte (ohne p23)
    page_blocks = wikia.get("page_blocks", {})
    p1_p22_text = ""
    for page_id in sorted(page_blocks.keys()):
        if page_id != "p23":
            p1_p22_text += " " + page_blocks[page_id]

    p1_p22_upper = p1_p22_text.upper()

    # Suche für jedes BURUMUT-Wort alle Substrings der Länge 4-7
    ergebnisse = []
    for word in grid_words:
        substrings = []
        for length in [4, 5, 6, 7]:
            for start in range(len(word) - length + 1):
                substr = word[start:start+length]
                count = p1_p22_upper.count(substr)
                if count > 0:
                    substrings.append({
                        "substr": substr,
                        "length": length,
                        "position": start,
                        "count": count,
                    })
        # Sortiere nach Häufigkeit
        substrings.sort(key=lambda x: -x["count"])
        ergebnisse.append({
            "word": word,
            "n_substrings_found": len(substrings),
            "top_5_substrings": substrings[:5],
        })

    # Welche BURUMUT-Wörter sind in p1-p22 präsent?
    n_present = sum(1 for e in ergebnisse if e["n_substrings_found"] > 0)
    return {
        "n_woerter": len(ergebnisse),
        "n_woerter_in_p1_p22": n_present,
        "ergebnisse": ergebnisse,
    }


# === SCHRITT 3: Echtes Codebook ===

def schritt_3_codebook(c, v22, v104):
    """Berechne latent_mean für alle 11 BURUMUT-Wörter und mappe zu Glyphen.

    Methode:
    - BURUMUT latent_mean = Mittelwert der normalisierten 14-dim ASCII-Vektoren
    - Glyphen latent_mean aus V22 (nur G11 verfügbar: 78.44)
    - Für andere Glyphen: wir nutzen die ASCII-Buchstaben-Mittelwerte
    """
    grid_words = v104["seiten"][22].get("grid_2d_words", [])
    v22_codebook = v22.get("codebook", {})

    # Lade Glyphen-Metadaten
    glyphs_v8 = json.load(open("bbox/align_wikia_20260706_V8/mapping_candidates.json"))
    gmeta = glyphs_v8.get("glyph_metadata", {})

    # Berechne BURUMUT latent_mean
    # Nutze 14-dim ASCII-Vektor, normalisiert auf [0,1] (A=65, Z=90, a=97, z=122)
    # Mittelwert = (Buchstabe - 65) / 25 für A-Z, also [0,1]
    burumut_means = {}
    for w in c["wörter"]:
        word = w["word"]
        # Normalisierte ASCII-Werte
        norm_values = [(ord(ch) - 65) / 25.0 for ch in word if ch.isalpha() and ch.isupper()]
        if norm_values:
            latent_mean = sum(norm_values) / len(norm_values) * 100  # Skaliere auf 0-100
        else:
            latent_mean = 0
        burumut_means[word] = latent_mean

    # V22 bekannter Codebook
    g11_latent = v22_codebook.get("g11_latent_mean", 78.44)
    burumutrefamtu_known = v22_codebook.get("burumutrefamtu_latent_mean", 78.29)

    # Berechne für jedes BURUMUT-Wort die Glyph-Distanz
    # Glyphen ohne bekannte latent_mean: nutze heuristic_latin-Mapping
    # Mappe BURUMUT-Buchstaben auf Glyphen mit similar_to_latin
    ergebnisse = []
    for w in c["wörter"]:
        word = w["word"]
        burumut_mean = burumut_means[word]

        # Finde nächsten Glyph
        # Glyphen haben kein numerisches latent_mean im V22
        # Wir mappen über: wie viele Buchstaben im BURUMUT-Wort matchen die heuristic_latin der Glyphe?
        glyph_scores = []
        for glyph_id, ginfo in gmeta.items():
            score = 0
            for ch in word:
                if ch == ginfo.get("heuristic_latin", "").upper():
                    score += 1
            glyph_scores.append((glyph_id, score, ginfo))

        if glyph_scores:
            glyph_scores.sort(key=lambda x: -x[1])
            best = glyph_scores[0]
            best_glyph = best[0]
            best_score = best[1]
        else:
            best_glyph = "G11"  # Fallback
            best_score = 0

        # Vergleich mit V22-Bekanntem
        if word == "BURUMUTREFAMTU":
            known_diff = abs(burumut_mean - burumutrefamtu_known)
        else:
            known_diff = None

        ergebnisse.append({
            "word": word,
            "burumut_latent_mean": round(burumut_mean, 4),
            "best_glyph": best_glyph,
            "best_score": best_score,
            "vs_known_brf": round(known_diff, 4) if known_diff is not None else None,
        })

    return {
        "n_woerter": len(ergebnisse),
        "n_glyphs_considered": len(gmeta),
        "burumutrefamtu_v22_mean": burumutrefamtu_known,
        "burumutrefamtu_computed": burumut_means.get("BURUMUTREFAMTU"),
        "g11_latent_v22": g11_latent,
        "codebook": ergebnisse,
    }


# === HAUPTPROGRAMM ===

def hauptprogramm():
    print("="*70)
    print("V25 — TOP-3 NÄCHSTE SCHRITTE AUSGEFÜHRT")
    print("="*70)

    c, v104, v22, wikia = lade_alles()

    # === SCHRITT 1: V/K-Binärcode ===
    print("\n" + "="*70)
    print("SCHRITT 1: V/K-BINÄRCODE AUS 14 SPALTEN")
    print("="*70)

    s1 = schritt_1_vk_binärcode(c, v104)
    print(f"\n{len(s1['codes'])} BURUMUT-Wörter, {s1['n_unique_codes']} unique V/K-Codes:\n")
    for e in s1["codes"]:
        print(f"  {e['position']:2d}. {e['word']:<20} V={e['n_vokale']:2d} K={e['n_konsonanten']:2d}  Code: {e['vk_code']}  Wert: {e['vk_value']:>5d}")
    if s1["duplicates"]:
        print(f"\nDuplikate im V/K-Code: {s1['duplicates']}")
    else:
        print("\nKeine Duplikate — jedes BURUMUT-Wort hat einen UNIQUE V/K-Code.")

    # === SCHRITT 2: BURUMUT-Substrings in p1-p22 ===
    print("\n" + "="*70)
    print("SCHRITT 2: BURUMUT-SUBSTRINGS IN p1-p22")
    print("="*70)

    s2 = schritt_2_substrings_in_p1_p22(c, v104, wikia)
    print(f"\n{s2['n_woerter_in_p1_p22']}/{s2['n_woerter']} BURUMUT-Wörter haben Substrings in p1-p22\n")
    for e in s2["ergebnisse"]:
        if e["n_substrings_found"] > 0:
            print(f"  {e['word']:<20} {e['n_substrings_found']} Substrings gefunden")
            for sub in e["top_5_substrings"][:3]:
                print(f"    - '{sub['substr']}' (Länge {sub['length']}, Position {sub['position']}, {sub['count']}× in p1-p22)")
        else:
            print(f"  {e['word']:<20} KEINE Substrings (nur in p23)")

    # === SCHRITT 3: Echtes Codebook ===
    print("\n" + "="*70)
    print("SCHRITT 3: ECHTES CODEBOOK (BURUMUT↔GLYPH)")
    print("="*70)

    s3 = schritt_3_codebook(c, v22, v104)
    print(f"\nBURUMUTREFAMTU Vergleich:")
    print(f"  V22 latent_mean: {s3['burumutrefamtu_v22_mean']}")
    print(f"  Berechnet:        {s3['burumutrefamtu_computed']:.4f}")
    print(f"  G11 latent_mean: {s3['g11_latent_v22']}")
    print(f"\n{len(s3['codebook'])} BURUMUT-Wörter mit berechneten latent_mean-Werten:\n")
    for e in s3["codebook"]:
        known = f"vs_V22: {e['vs_known_brf']}" if e['vs_known_brf'] is not None else "neu"
        print(f"  {e['word']:<20} latent_mean={e['burumut_latent_mean']:6.2f}  →  {e['best_glyph']} (score {e['best_score']})")

    # Speichern
    output_dir = Path("bbox/v24_20260708")
    output = {
        "phase": "V25 — Top-3 nächste Schritte AUSGEFÜHRT",
        "datum": "2026-07-08",
        "schritt_1_vk_code": s1,
        "schritt_2_substrings": s2,
        "schritt_3_codebook": s3,
        "reference": "Rein symbolisch, KEIN ML. Lookup + deterministische Berechnung."
    }
    output_path = output_dir / "v25_top3_ausgefuehrt.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n→ Ergebnisse gespeichert: {output_path}")


if __name__ == "__main__":
    hauptprogramm()
