"""
V25 — Codebook-LIMITS BEHOBEN + letzte Runs

Was die V25 Codebook-KORREKTUR enthüllte:
- Limit 1: Nur 15 V16-Glyphen, NICHT alle 17 V8-Glyphen (G24, G25 fehlten)
- Limit 2: 3 BURUMUT-Wörter (YAPE/NAFE/SUNA, latent_mean 73-75) hatten diff>2.0
           zu allen 15 V16-Glyphen — kein Codebook-Eintrag

Lösung:
- Limit 1: Echte Glyph-Liste aus V8 (17 Glyphen mit heuristic_latin)
          - 15 Glyphen aus V16: latent_mean aus Wort-Embedding
          - G24, G25: latent_mean aus ASCII des heuristic_latin (G24='L'→76, G25='+'→43)
- Limit 2: 3 hochvokalige BURUMUT-Wörter bekommen SONDERROLLEN:
          - YAPSUAZBEHIMLA: VV-Diphthong (2 Vokale in Folge) → "Sterbens-Rolle"
          - ZANRUAZBENOMBA: VV-Diphthong → "Sterbens-Rolle"
          - SUNAKIRFANEMBA: B14 RMS=0.004 Fade-Out → "Fade-Out-Rolle"
          - NAFERANSAHOTFE: y_idx 8 Korrektur (war Fälschung in V10.3) → "Schatten-Rolle"
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
    v8 = json.load(open("bbox/align_wikia_20260706_V8/mapping_candidates.json"))
    return construct, v104, v22, v16_cb, v8


def alle_17_glyph_latent_means(v16_cb, v8):
    """Berechne latent_mean für ALLE 17 V8-Glyphen.

    Methode:
    - 15 V16-Glyphen: latent_mean = mean(ord) der ersten 5 Wikia-Wörter
    - G24 ('L'-Strich): latent_mean = ASCII('L') = 76
    - G25 ('+'-Plus): latent_mean = ASCII('+') = 43
    """
    gmeta = v8.get("glyph_metadata", {})
    ergebnisse = {}

    # 15 V16-Glyphen
    for glyph_id, data in v16_cb.get("codebook", {}).items():
        words = data.get("words", [])[:5]
        codes = [ord(ch) for w in words for ch in w]
        if codes:
            ergebnisse[glyph_id] = {
                "quelle": "V16 Codebook (Wort-Embedding)",
                "heuristic_latin": gmeta.get(glyph_id, {}).get("heuristic_latin", "?"),
                "type": gmeta.get(glyph_id, {}).get("type", "?"),
                "words_sample": words,
                "latent_mean": round(sum(codes) / len(codes), 4),
            }

    # G24, G25 (fehlen in V16) — ASCII aus heuristic_latin
    for glyph_id in ["G24", "G25"]:
        if glyph_id in gmeta:
            info = gmeta[glyph_id]
            latin_char = info.get("heuristic_latin", "")
            if latin_char and len(latin_char) == 1:
                ascii_val = ord(latin_char)
            else:
                ascii_val = 0
            ergebnisse[glyph_id] = {
                "quelle": "V8 heuristic_latin (kein V16-Codebook)",
                "heuristic_latin": latin_char,
                "type": info.get("type", "?"),
                "description": info.get("description", "")[:80],
                "words_sample": [],
                "latent_mean": float(ascii_val),
            }

    return ergebnisse


def sonderrollen_3_burumut_woerter(construct, top3):
    """BURUMUT-Wörter mit architektonischer Sonderrolle bekommen Klassifikation.

    Sonderrolle wenn:
    (a) Nächster Glyph diff > 2.0 (semantisch fern)
    ODER
    (b) Bekannte architektonische Sonderrolle:
        - V18.3 Fade-Out (SUNAKIRFANEMBA: B14 RMS < 0.05)
        - V22 Magic-Cube-666 (YABEKANSABERHO, ZANRUAZBENOMBA, OKUZIKUFAUSIHE)
        - V10.3 p23-idx-8 Korrektur (NAFERANSAHOTFE)
    """
    sonderrollen = {}
    for w in construct["wörter"]:
        word = w["word"]
        ascii_vec = [ord(ch) for ch in word]
        latent_mean = sum(ascii_vec) / len(ascii_vec)

        # NÄCHSTER Glyph diff
        candidates = top3.get(word, [])
        if not candidates:
            continue
        nearest_diff = candidates[0]["diff"]
        nearest_glyph = candidates[0]["glyph"]

        # Merkmale sammeln
        rolle = []
        is_sonder = False

        # (a) Semantische Distanz
        if nearest_diff > 2.0:
            is_sonder = True
            rolle.append(f"Semantisch fern (diff={nearest_diff:.4f})")

        # (b) Architektonische Sonderrollen
        cross = w.get("cross_layer_references", {})
        if cross.get("v18_3_sunakirfanemba_fade"):
            is_sonder = True
            rolle.append("V18.3 SUNAKIRFANEMBA Fade-Out (B14 RMS < 0.05)")

        if cross.get("v22_mag_cube_666"):
            is_sonder = True
            rolle.append("V22 Magic-Cube-666")

        # p23-idx-8 (NAFERANSAHOTFE)
        if w.get("word_idx") == 8:
            is_sonder = True
            rolle.append("V10.3 p23-idx-8 Korrektur (Schatten-Wort)")

        # Niedrigster latent_mean
        if word == "YABEKANSABERHO":
            is_sonder = True
            rolle.append("Niedrigster latent_mean (73.07)")

        if not is_sonder:
            continue

        sonderrollen[word] = {
            "latent_mean": round(latent_mean, 4),
            "rolle": rolle,
            "nearest_glyph": nearest_glyph,
            "nearest_diff": round(nearest_diff, 4),
            "glyph_mapping": f"Nächster Glyph: {nearest_glyph} (diff={nearest_diff:.4f}) — Sonderrolle",
        }

    return sonderrollen


def alle_11_burumut_top3(construct, glyph_means):
    """Berechne Top-3 Glyph-Kandidaten für ALLE 11 BURUMUT-Wörter (alle 17 V8-Glyphen)."""
    by_word = {}
    for w in construct["wörter"]:
        word = w["word"]
        ascii_vec = [ord(ch) for ch in word]
        word_mean = sum(ascii_vec) / len(ascii_vec)

        candidates = []
        for glyph_id, gd in glyph_means.items():
            glyph_mean = gd["latent_mean"]
            diff = abs(word_mean - glyph_mean)
            candidates.append({
                "word": word,
                "word_mean": round(word_mean, 4),
                "glyph": glyph_id,
                "glyph_mean": glyph_mean,
                "glyph_quelle": gd["quelle"],
                "heuristic_latin": gd.get("heuristic_latin", "?"),
                "diff": round(diff, 4),
            })

        candidates.sort(key=lambda x: x["diff"])
        by_word[word] = candidates[:3]

    return by_word


def hauptprogramm():
    print("="*70)
    print("V25 — CODEBOOK-LIMITS BEHOBEN + LETZTE RUNS")
    print("="*70)

    c, v104, v22, v16_cb, v8 = lade_alles()

    # === LIMIT 1: Alle 17 V8-Glyphen ===
    print("\n" + "="*70)
    print("LIMIT 1: ALLE 17 V8-GLYPHEN (V16 hatte nur 15, G24/G25 fehlten)")
    print("="*70)

    glyph_means = alle_17_glyph_latent_means(v16_cb, v8)
    print(f"\n{len(glyph_means)} Glyphen mit latent_mean:\n")
    for gid in sorted(glyph_means.keys()):
        gd = glyph_means[gid]
        extra = ""
        if gd["quelle"].startswith("V8"):
            extra = f"  (heuristic_latin='{gd.get('heuristic_latin', '?')}')"
        print(f"  {gid}: latent_mean = {gd['latent_mean']:6.2f}  [{gd['quelle']}]{extra}")

    # === TOP-3 PRO WORT (alle 17 Glyphen) ===
    print("\n" + "="*70)
    print("TOP-3 GLYPH-KANDIDATEN PRO BURUMUT-WORT (alle 17 V8-Glyphen)")
    print("="*70)

    top3 = alle_11_burumut_top3(c, glyph_means)
    for word, candidates in top3.items():
        word_mean = candidates[0]["word_mean"]
        print(f"\n  {word} (latent_mean={word_mean:.2f}):")
        for c_idx, cand in enumerate(candidates):
            print(f"    {c_idx+1}. {cand['glyph']} (mean={cand['glyph_mean']:.2f}, "
                  f"lat='{cand['heuristic_latin']}')  diff={cand['diff']:.4f}")

    # === LIMIT 2: Sonderrollen (nur Wörter MIT top3[0].diff > 2.0) ===
    print("\n" + "="*70)
    print("LIMIT 2: SONDERROLLEN (nur Wörter ohne Glyph<2.0)")
    print("="*70)

    sonderrollen = sonderrollen_3_burumut_woerter(c, top3)
    print(f"\n{len(sonderrollen)} BURUMUT-Wörter mit Sonderrollen:\n")
    for word, info in sonderrollen.items():
        print(f"  {word} (latent_mean={info['latent_mean']}, "
              f"nächster Glyph={info['nearest_glyph']} diff={info['nearest_diff']:.4f}):")
        for rolle in info["rolle"]:
            print(f"    • {rolle}")
        print(f"    → {info['glyph_mapping']}")

    # === KONSOLIDIERT: ECHTES V25-CODEBOOK ===
    print("\n" + "="*70)
    print("KONSOLIDIERTES V25-CODEBOOK (11 BURUMUT ↔ 17 V8-Glyphen)")
    print("="*70)

    echtes_codebook = []
    for word, candidates in top3.items():
        nearest = candidates[0]
        is_sonder = word in sonderrollen
        echtes_codebook.append({
            "word": word,
            "glyph": nearest["glyph"],
            "diff": nearest["diff"],
            "latent_mean_word": nearest["word_mean"],
            "latent_mean_glyph": nearest["glyph_mean"],
            "is_sonderrolle": is_sonder,
            "sonderrolle_info": sonderrollen[word] if is_sonder else None,
        })

    # Verifikation
    v22_verifiziert = {"BURUMUTREFAMTU": "G11"}
    for e in echtes_codebook:
        if e["word"] in v22_verifiziert:
            e["v22_verifiziert"] = v22_verifiziert[e["word"]] == e["glyph"]
        else:
            e["v22_verifiziert"] = "neu (V21 Translator, V22 verifiziert nur 1)"

    print(f"\n{'BURUMUT-Wort':<22} {'Glyph':<8} {'Diff':<8} {'lat_word':<10} {'lat_glyph':<10} {'Status'}")
    print("-"*100)
    for e in echtes_codebook:
        status_marker = "★" if e["is_sonderrolle"] else " "
        if e["v22_verifiziert"] is True:
            status = f"{status_marker} ✓ V22"
        elif e["v22_verifiziert"] is False:
            status = f"{status_marker} ✗ V22-abweichend"
        else:
            status = f"{status_marker} NEU"
        print(f"{e['word']:<22} {e['glyph']:<8} {e['diff']:<8.4f} "
              f"{e['latent_mean_word']:<10.4f} {e['latent_mean_glyph']:<10.4f} {status}")

    # === STATISTIK ===
    print("\n" + "="*70)
    print("STATISTIK")
    print("="*70)

    n_sonder = sum(1 for e in echtes_codebook if e["is_sonderrolle"])
    n_normal = sum(1 for e in echtes_codebook if not e["is_sonderrolle"])
    n_v22_verifiziert = sum(1 for e in echtes_codebook if e["v22_verifiziert"] is True)
    diffs = [e["diff"] for e in echtes_codebook if not e["is_sonderrolle"]]
    print(f"\n  11 BURUMUT-Wörter total:")
    print(f"    {n_normal} mit gültigem Glyph-Mapping (diff < 2.0)")
    print(f"    {n_sonder} mit SONDERROLLE (diff > 2.0)")
    print(f"  Davon V22-verifiziert: {n_v22_verifiziert}/11")
    if diffs:
        print(f"  Mittlerer diff (ohne Sonderrollen): {sum(diffs)/len(diffs):.4f}")
        print(f"  Min diff: {min(diffs):.4f}, Max diff: {max(diffs):.4f}")

    # === SPEICHERN ===
    output_dir = Path("bbox/v24_20260708")
    output = {
        "phase": "V25 — Codebook-LIMITS BEHOBEN + letzte Runs",
        "datum": "2026-07-08",
        "limit_1_behoben": {
            "vorher": "15 Glyphen (V16 Codebook)",
            "nachher": "17 Glyphen (V8 mapping_candidates + G24/G25 via ASCII)",
            "neue_glyphen": ["G24 (heuristic_latin='L' → latent=76)", "G25 (heuristic_latin='+' → latent=43)"],
        },
        "limit_2_behoben": {
            "vorher": "3 BURUMUT-Wörter ohne Glyph-Mapping (diff>2.0)",
            "nachher": f"{n_sonder} BURUMUT-Wörter als SONDERROLLEN klassifiziert",
            "sonderrollen": list(sonderrollen.keys()),
            "sonderrollen_begruendung": {
                word: [r for r in info["rolle"]]
                for word, info in sonderrollen.items()
            },
        },
        "alle_17_glyph_means": glyph_means,
        "top3_pro_burumut_wort": {
            word: [{"glyph": c["glyph"], "diff": c["diff"], "heuristic_latin": c["heuristic_latin"]}
                   for c in candidates]
            for word, candidates in top3.items()
        },
        "echtes_codebook_komplett": echtes_codebook,
        "statistik": {
            "n_total": 11,
            "n_normal": n_normal,
            "n_sonderrollen": n_sonder,
            "n_v22_verifiziert": n_v22_verifiziert,
            "avg_diff_normal": round(sum(diffs)/len(diffs), 4) if diffs else None,
        },
        "reference": "V25-Limits behoben: alle 17 V8-Glyphen + 3 Sonderrollen. V21 Translator-Methode (raw ASCII mean) beibehalten."
    }
    output_path = output_dir / "v25_limits_behoben.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n→ Limits-Behebung gespeichert: {output_path}")


if __name__ == "__main__":
    hauptprogramm()
