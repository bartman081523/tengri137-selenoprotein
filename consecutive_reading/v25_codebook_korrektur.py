"""
V25 — Codebook-KORREKTUR wie die BURUMUT-Matrix es sagt.

Die Matrix hat enthüllt (v25_top3_ausgefuehrt.py Schritt 3):
- Heuristik war FALSCH: BURUMUTREFAMTU wurde auf G10 gemappt
- V22 verifiziert: BURUMUTREFAMTU=78.29 ↔ G11=78.44, diff=0.154
- Echte latent_mean = MITTELWERT DER ASCII-BUCHSTABEN (raw, 65-90)
- Falsche Formel war: (ord-65)/25 * 100 — die hat BURUMUTREFAMTU auf 53.14 abgebildet

KORREKTUR:
1. Für alle 11 BURUMUT-Wörter: latent_mean = sum(ASCII)/14 (V21 Translator-Methode)
2. Für alle 15 V16-Codebook-Glyphen: latent_mean = mittleres Wort-Embedding
3. Berechne L2-Distanz für alle 11×15=165 Paare
4. Verifiziere: BURUMUTREFAMTU↔G11 (diff < 0.01 als sanity)
5. Top-3 Kandidaten pro BURUMUT-Wort mit echten Distanzen
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def lade_alles():
    construct = json.load(open("bbox/v24_20260708/v24_burumut_construct.json"))
    v104 = json.load(open("bbox/v104_20260708/tengri137_complete_decoded_v104.json"))
    v22 = json.load(open("bbox/v22_20260708/v22_burumut_architecture.json"))
    v16_cb = json.load(open("bbox/v16_20260707/codebook_lookup.json"))
    v22_wikia = json.load(open("bbox/v22_20260708/v22_wikia_semantics.json"))
    return construct, v104, v22, v16_cb, v22_wikia


def schritt_1_burumut_latent_means(c):
    """KORREKTE latent_mean für alle 11 BURUMUT-Wörter.

    Methode (V21 Translator-Pattern):
    - latent = M[i, :] = 14-dim ASCII-Vektor des BURUMUT-Wortes
    - latent_mean = mean(latent) = sum(ord(c))/14
    - Für BURUMUTREFAMTU: (66+85+82+85+77+85+84+82+69+70+65+77+84+85)/14 = 78.29
    """
    ergebnisse = []
    for w in c["wörter"]:
        word = w["word"]
        # KORREKT: raw ASCII mean, nicht normalisiert
        ascii_vec = [ord(ch) for ch in word]
        latent_mean = sum(ascii_vec) / len(ascii_vec)
        ergebnisse.append({
            "word": word,
            "ascii_vec": ascii_vec,
            "latent_mean": round(latent_mean, 4),
        })
    return ergebnisse


def schritt_2_glyph_latent_means(v16_cb):
    """KORREKTE latent_mean für alle 15 V16-Codebook-Glyphen.

    Methode (V21 Translator):
    - Für jedes Glyph: mittlerer ASCII-Wert der ersten 5 Wörter
    """
    ergebnisse = {}
    codebook = v16_cb.get("codebook", {})
    for glyph_id, data in codebook.items():
        words = data.get("words", [])[:5]
        codes = []
        for w in words:
            codes.extend([ord(ch) for ch in w])
        if codes:
            ergebnisse[glyph_id] = {
                "words_sample": words,
                "latent_mean": round(sum(codes) / len(codes), 4),
                "n_words_used": len(words),
            }
    return ergebnisse


def schritt_3_distanz_matrix(burumut_means, glyph_means):
    """Berechne L2-Distanz für alle 11×15=165 BURUMUT↔Glyph-Paare."""
    ergebnisse = []
    for bm in burumut_means:
        word = bm["word"]
        word_mean = bm["latent_mean"]
        for glyph_id, gd in glyph_means.items():
            glyph_mean = gd["latent_mean"]
            diff = abs(word_mean - glyph_mean)
            ergebnisse.append({
                "word": word,
                "word_mean": word_mean,
                "glyph": glyph_id,
                "glyph_mean": glyph_mean,
                "diff": round(diff, 4),
            })
    return ergebnisse


def schritt_4_top3_pro_wort(distanzen, burumut_means):
    """Pro BURUMUT-Wort: Top-3 nächste Glyphen."""
    by_word = {}
    for d in distanzen:
        w = d["word"]
        if w not in by_word:
            by_word[w] = []
        by_word[w].append(d)

    top3 = {}
    for word, dists in by_word.items():
        dists_sorted = sorted(dists, key=lambda x: x["diff"])
        top3[word] = dists_sorted[:3]
    return top3


def schritt_5_verifikation(c, burumut_means, top3):
    """Verifiziere: BURUMUTREFAMTU↔G11 (V22 verifiziert, diff=0.154)."""
    brf = next((b for b in burumut_means if b["word"] == "BURUMUTREFAMTU"), None)
    if not brf:
        return {"error": "BURUMUTREFAMTU nicht gefunden"}

    top3_brf = top3.get("BURUMUTREFAMTU", [])
    if not top3_brf:
        return {"error": "Top3 für BURUMUTREFAMTU leer"}

    nearest = top3_brf[0]
    nearest_glyph = nearest["glyph"]
    nearest_diff = nearest["diff"]

    # V22 sagt: BURUMUTREFAMTU↔G11, diff=0.154
    v22_diff = 0.154
    v22_glyph = "G11"

    korrekt = (nearest_glyph == v22_glyph) and (abs(nearest_diff - v22_diff) < 0.01)

    return {
        "v22_erwartet": {
            "glyph": v22_glyph,
            "diff": v22_diff,
        },
        "v25_berechnet": {
            "glyph": nearest_glyph,
            "diff": nearest_diff,
            "latent_mean_brf": brf["latent_mean"],
        },
        "verifiziert": korrekt,
        "top3_brf": top3_brf,
    }


def hauptprogramm():
    print("="*70)
    print("V25 — CODEBOOK-KORREKTUR (V21 Translator-Methode)")
    print("="*70)

    c, v104, v22, v16_cb, v22_wikia = lade_alles()

    # === SCHRITT 1: BURUMUT latent_means ===
    print("\n" + "="*70)
    print("SCHRITT 1: BURUMUT LATENT_MEANS (V21 Translator, raw ASCII mean)")
    print("="*70)

    burumut_means = schritt_1_burumut_latent_means(c)
    print(f"\n{len(burumut_means)} BURUMUT-Wörter:\n")
    for b in burumut_means:
        print(f"  {b['word']:<20} latent_mean = {b['latent_mean']:.4f}")

    # === SCHRITT 2: Glyph latent_means ===
    print("\n" + "="*70)
    print("SCHRITT 2: GLYPH LATENT_MEANS (V16 Codebook + V21 Translator)")
    print("="*70)

    glyph_means = schritt_2_glyph_latent_means(v16_cb)
    print(f"\n{len(glyph_means)} Glyphen aus V16 Codebook:\n")
    for gid, gd in sorted(glyph_means.items()):
        print(f"  {gid}: latent_mean = {gd['latent_mean']:.4f}  (Wörter: {gd['words_sample'][:3]})")

    # === SCHRITT 3: Distanz-Matrix ===
    print("\n" + "="*70)
    print("SCHRITT 3: DISTANZ-MATRIX (11×15 = 165 Paare)")
    print("="*70)

    distanzen = schritt_3_distanz_matrix(burumut_means, glyph_means)
    print(f"\n{len(distanzen)} Distanzen berechnet\n")

    # === SCHRITT 4: Top-3 pro BURUMUT-Wort ===
    print("="*70)
    print("SCHRITT 4: TOP-3 NÄCHSTE GLYPHEN PRO BURUMUT-WORT")
    print("="*70)

    top3 = schritt_4_top3_pro_wort(distanzen, burumut_means)
    for word, candidates in top3.items():
        print(f"\n  {word} (latent_mean = {next(b['latent_mean'] for b in burumut_means if b['word'] == word):.2f}):")
        for c_idx, cand in enumerate(candidates):
            marker = " ← V22 verifiziert" if (word == "BURUMUTREFAMTU" and cand["glyph"] == "G11") else ""
            print(f"    {c_idx+1}. {cand['glyph']} (mean={cand['glyph_mean']:.2f})  diff={cand['diff']:.4f}{marker}")

    # === SCHRITT 5: Verifikation ===
    print("\n" + "="*70)
    print("SCHRITT 5: VERIFIKATION BURUMUTREFAMTU↔G11 (V22-Sanity-Check)")
    print("="*70)

    verif = schritt_5_verifikation(c, burumut_means, top3)
    print(f"\nV22 Erwartung:  BURUMUTREFAMTU↔{verif['v22_erwartet']['glyph']}, diff={verif['v22_erwartet']['diff']:.4f}")
    print(f"V25 Berechnet:  BURUMUTREFAMTU↔{verif['v25_berechnet']['glyph']}, diff={verif['v25_berechnet']['diff']:.4f}")
    print(f"latent_mean BURUMUTREFAMTU = {verif['v25_berechnet']['latent_mean_brf']:.4f}")
    print(f"\nVERIFIKATION: {'✓ BESTÄTIGT' if verif['verifiziert'] else '✗ ABWEICHUNG'}")

    # === KONSOLIDIERUNG: Echtes Codebook ===
    print("\n" + "="*70)
    print("ECHTES CODEBOOK (V21 Translator + V16 Codebook)")
    print("="*70)

    echtes_codebook = []
    for word, candidates in top3.items():
        nearest = candidates[0]
        echtes_codebook.append({
            "word": word,
            "glyph": nearest["glyph"],
            "diff": nearest["diff"],
            "latent_mean_word": nearest["word_mean"],
            "latent_mean_glyph": nearest["glyph_mean"],
        })

    # Vergleich: V22 verifiziert nur BURUMUTREFAMTU↔G11
    # Die anderen 10 sind NEU aus V21 Translator abgeleitet
    v22_verifiziert = {"BURUMUTREFAMTU": "G11"}
    for e in echtes_codebook:
        if e["word"] in v22_verifiziert:
            e["v22_verifiziert"] = v22_verifiziert[e["word"]] == e["glyph"]
        else:
            e["v22_verifiziert"] = "neu (V21 Translator, nicht in V22)"

    print(f"\n{'BURUMUT-Wort':<22} {'Glyph':<8} {'Diff':<10} {'latent_word':<14} {'V22-Status'}")
    print("-"*80)
    for e in echtes_codebook:
        status = f"✓ verifiziert" if e["v22_verifiziert"] is True else (
                 f"✗ abweichend" if e["v22_verifiziert"] is False else
                 e["v22_verifiziert"])
        print(f"{e['word']:<22} {e['glyph']:<8} {e['diff']:<10.4f} {e['latent_mean_word']:<14.4f} {status}")

    # Speichern
    output_dir = Path("bbox/v24_20260708")
    output = {
        "phase": "V25 — Codebook-KORREKTUR (V21 Translator-Methode)",
        "datum": "2026-07-08",
        "korrektur": "V25 Schritt 3 verriet: ASCII-normalisiert (0-100) ist FALSCH. Raw ASCII mean (65-90) ist RICHTIG.",
        "v21_translator_methode": "latent_mean = sum(ord(c) for c in word) / 14 (semi-orthogonale Matrix-Zeile)",
        "schritt_1_burumut_means": burumut_means,
        "schritt_2_glyph_means": glyph_means,
        "schritt_4_top3_pro_wort": top3,
        "schritt_5_verifikation": verif,
        "echtes_codebook": echtes_codebook,
        "n_10_neu_abgeleitet": sum(1 for e in echtes_codebook if e["v22_verifiziert"] != True and e["v22_verifiziert"] != False),
        "reference": "V21 Translator-Pattern (M[i, :].mean()) statt ASCII-Normalisierung. V16 Codebook (15 Glyphen) als Vergleich."
    }
    output_path = output_dir / "v25_codebook_korrektur.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n→ Korrektur gespeichert: {output_path}")


if __name__ == "__main__":
    hauptprogramm()
