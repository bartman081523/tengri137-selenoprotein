"""
V25 SCHRITT 4 — 154 Zellen multidimensional lesen.

Matrix-Emergenz (v25_burumut_emergiert_weiter.py):
  SCHRITT 5 (154 Zellen): Multidimensionale Selbst-Lesung

Jede der 11×14=154 Zellen hat 7 Dimensionen:
  1. Buchstabe (A-Z)
  2. V/K (Vokal/Konsonant)
  3. ASCII-Wert (65-90)
  4. RMS-Amplitude (V18.3)
  5. Glyph-Cluster (welcher Glyph mapped auf dieses Wort?)
  6. Wikia-Klasse (welcher Klasse gehört das Wort an?)
  7. Tappeiner-Stelle (welche Position im Bruch?)

Rein symbolisch, KEIN ML.
"""

import json
from pathlib import Path
from collections import Counter, defaultdict


def lade_construct():
    return json.load(open("bbox/v24_20260708/v24_burumut_construct.json"))


def lade_codebook():
    return json.load(open("bbox/v24_20260708/v25_limits_behoben.json"))


def baue_154_zellen(c, cb):
    """Erzeuge 154 Zellen mit je 7 Dimensionen."""
    # Codebook-Mapping: BURUMUT-Wort → Glyph
    wort_zu_glyph = {}
    for e in cb["echtes_codebook_komplett"]:
        wort_zu_glyph[e["word"]] = {
            "glyph": e["glyph"],
            "diff": e["diff"],
            "is_sonderrolle": e["is_sonderrolle"],
        }

    zellen = []
    for w in c["wörter"]:
        word = w["word"]
        word_idx = w["word_idx"]
        ascii_vec = w["ascii_vec"]
        rms_vec = w["rms_vec_14"]
        cross = w.get("cross_layer_references", {})
        wikia_klasse = w.get("wikia_klasse", "?")

        # Glyph-Beziehung
        glyph_info = wort_zu_glyph.get(word, {})
        glyph_id = glyph_info.get("glyph", "?")
        glyph_diff = glyph_info.get("diff", -1)
        is_sonder = glyph_info.get("is_sonderrolle", False)

        # Tappeiner-Stelle: wir haben tapp_brueche mit 22_atoms_corrected
        # Position = word_idx
        tapp = w.get("tappeiner_brueche", [])
        tapp_info = tapp[0] if tapp else {}
        tapp_22_atoms = tapp_info.get("22_atoms_corrected", "?")

        # Pro Zelle (jeder Buchstabe des BURUMUT-Wortes)
        for pos, buchstabe in enumerate(word):
            ist_vokal = buchstabe in "AEIOU"
            zelle = {
                "zelle_idx": word_idx * 14 + pos,
                "wort_idx": word_idx,
                "wort": word,
                "position": pos,
                "buchstabe": buchstabe,
                "vk": "V" if ist_vokal else "K",
                "ascii": ascii_vec[pos] if pos < len(ascii_vec) else 0,
                "rms": round(rms_vec[pos], 4) if pos < len(rms_vec) else 0,
                "glyph": glyph_id,
                "glyph_diff": glyph_diff,
                "is_sonderrolle": is_sonder,
                "wikia_klasse": wikia_klasse,
                "tapp_22_atoms": tapp_22_atoms,
            }
            zellen.append(zelle)

    return zellen


def analysiere_154_zellen(zellen):
    """Suche Muster über die 154 Zellen."""
    ergebnisse = {}

    # === MUSTER 1: Buchstaben-Häufigkeit ===
    buchstaben_count = Counter(z["buchstabe"] for z in zellen)
    ergebnisse["buchstaben_haeufigkeit"] = dict(buchstaben_count.most_common())

    # === MUSTER 2: V/K-Verteilung pro Position ===
    vk_pro_pos = defaultdict(lambda: {"V": 0, "K": 0})
    for z in zellen:
        vk_pro_pos[z["position"]][z["vk"]] += 1
    vk_ergebnis = {}
    for pos in range(14):
        v = vk_pro_pos[pos]["V"]
        k = vk_pro_pos[pos]["K"]
        vk_ergebnis[pos] = {
            "V": v,
            "K": k,
            "V/K": round(v / max(1, v + k), 3),
        }
    ergebnisse["vk_pro_position"] = vk_ergebnis

    # === MUSTER 3: ASCII-Mittelwert pro Position ===
    ascii_pro_pos = defaultdict(list)
    for z in zellen:
        ascii_pro_pos[z["position"]].append(z["ascii"])
    ascii_ergebnis = {}
    for pos in range(14):
        vals = ascii_pro_pos[pos]
        if vals:
            ascii_ergebnis[pos] = {
                "mean": round(sum(vals) / len(vals), 2),
                "min": min(vals),
                "max": max(vals),
                "range": max(vals) - min(vals),
            }
    ergebnisse["ascii_pro_position"] = ascii_ergebnis

    # === MUSTER 4: RMS-Mittelwert pro Position ===
    rms_pro_pos = defaultdict(list)
    for z in zellen:
        rms_pro_pos[z["position"]].append(z["rms"])
    rms_ergebnis = {}
    for pos in range(14):
        vals = rms_pro_pos[pos]
        if vals:
            rms_ergebnis[pos] = {
                "mean": round(sum(vals) / len(vals), 4),
                "min": round(min(vals), 4),
                "max": round(max(vals), 4),
            }
    ergebnisse["rms_pro_position"] = rms_ergebnis

    # === MUSTER 5: V/K-Binärcode-Pro Wort ===
    vk_codes = {}
    for word_idx in range(11):
        wort_zellen = [z for z in zellen if z["wort_idx"] == word_idx]
        wort_zellen.sort(key=lambda z: z["position"])
        bits = "".join("1" if z["vk"] == "V" else "0" for z in wort_zellen)
        vk_codes[wort_zellen[0]["wort"]] = bits
    ergebnisse["vk_codes_pro_wort"] = vk_codes

    # === MUSTER 6: Korrelation V/K ↔ RMS ===
    vk_rms = defaultdict(list)
    for z in zellen:
        vk_rms[z["vk"]].append(z["rms"])
    ergebnisse["rms_nach_vk"] = {
        "V_mean": round(sum(vk_rms["V"]) / len(vk_rms["V"]), 4),
        "K_mean": round(sum(vk_rms["K"]) / len(vk_rms["K"]), 4),
        "V_count": len(vk_rms["V"]),
        "K_count": len(vk_rms["K"]),
    }

    # === MUSTER 7: Korrelation V/K ↔ ASCII ===
    vk_ascii = defaultdict(list)
    for z in zellen:
        vk_ascii[z["vk"]].append(z["ascii"])
    ergebnisse["ascii_nach_vk"] = {
        "V_mean": round(sum(vk_ascii["V"]) / len(vk_ascii["V"]), 2),
        "K_mean": round(sum(vk_ascii["K"]) / len(vk_ascii["K"]), 2),
    }

    # === MUSTER 8: Glyph-Cluster ===
    glyph_pro_wort = {}
    for z in zellen:
        if z["wort"] not in glyph_pro_wort:
            glyph_pro_wort[z["wort"]] = {
                "glyph": z["glyph"],
                "is_sonderrolle": z["is_sonderrolle"],
                "diff": z["glyph_diff"],
            }
    ergebnisse["glyph_pro_wort"] = glyph_pro_wort

    # === MUSTER 9: Position der Vokale ===
    vokal_pos_pro_wort = {}
    for word_idx in range(11):
        wort_zellen = [z for z in zellen if z["wort_idx"] == word_idx]
        wort_zellen.sort(key=lambda z: z["position"])
        wort = wort_zellen[0]["wort"]
        vokal_pos = [z["position"] for z in wort_zellen if z["vk"] == "V"]
        vokal_pos_pro_wort[wort] = vokal_pos
    ergebnisse["vokal_pos_pro_wort"] = vokal_pos_pro_wort

    return ergebnisse


def hauptprogramm():
    print("="*70)
    print("V25 SCHRITT 4 — 154 ZELLEN MULTIDIMENSIONAL LESEN")
    print("="*70)

    c = lade_construct()
    cb = lade_codebook()

    print(f"\nConstruct: {len(c['wörter'])} BURUMUT-Wörter")
    print(f"Codebook: {len(cb['echtes_codebook_komplett'])} BURUMUT↔Glyph-Einträge")

    # === 154 ZELLEN BAUEN ===
    print("\n" + "="*70)
    print("BAUE 154 ZELLEN (11 Wörter × 14 Buchstaben)")
    print("="*70)

    zellen = baue_154_zellen(c, cb)
    print(f"\n{len(zellen)} Zellen erzeugt.")

    # Beispiel-Zelle (BURUMUTREFAMTU, Position 0 = 'B')
    print("\nBeispiel-Zelle [0]: BURUMUTREFAMTU, Position 0")
    beispiel = zellen[0]
    for k, v in beispiel.items():
        print(f"  {k}: {v}")

    # === ANALYSE ===
    print("\n" + "="*70)
    print("MUSTER 1: BUCHSTABEN-HÄUFIGKEIT (über 154 Zellen)")
    print("="*70)

    analyse = analysiere_154_zellen(zellen)

    for buchstabe, count in list(analyse["buchstaben_haeufigkeit"].items())[:15]:
        print(f"  {buchstabe}: {count}×")

    # === MUSTER 2: V/K pro Position ===
    print("\n" + "="*70)
    print("MUSTER 2: V/K-VERTEILUNG PRO POSITION (0-13)")
    print("="*70)

    for pos in range(14):
        vkp = analyse["vk_pro_position"][pos]
        bar_v = "V" * vkp["V"]
        bar_k = "K" * vkp["K"]
        print(f"  Position {pos:2d}: V={vkp['V']:2d} K={vkp['K']:2d}  V/K={vkp['V/K']:.2f}  "
              f"{bar_v}{bar_k}")

    # === MUSTER 3: ASCII pro Position ===
    print("\n" + "="*70)
    print("MUSTER 3: ASCII-MITTELWERT PRO POSITION")
    print("="*70)

    for pos in range(14):
        a = analyse["ascii_pro_position"][pos]
        bar = "*" * int(a["mean"] - 60)
        print(f"  Position {pos:2d}: mean={a['mean']:.2f}  range=[{a['min']},{a['max']}]  "
              f"diff={a['range']}  {bar}")

    # === MUSTER 4: RMS pro Position ===
    print("\n" + "="*70)
    print("MUSTER 4: RMS-MITTELWERT PRO POSITION")
    print("="*70)

    for pos in range(14):
        r = analyse["rms_pro_position"][pos]
        bar = "*" * int(r["mean"] * 100)
        print(f"  Position {pos:2d}: mean={r['mean']:.4f}  range=[{r['min']:.3f},{r['max']:.3f}]  {bar}")

    # === MUSTER 5: V/K-Binärcode pro Wort ===
    print("\n" + "="*70)
    print("MUSTER 5: V/K-BINÄRCODE PRO WORT (V=1, K=0)")
    print("="*70)

    for wort, code in analyse["vk_codes_pro_wort"].items():
        n_value = int(code, 2)
        print(f"  {wort:<20} {code}  (={n_value:5d})")

    # === MUSTER 6+7: V/K ↔ RMS/ASCII ===
    print("\n" + "="*70)
    print("MUSTER 6+7: V/K ↔ RMS/ASCII KORRELATION")
    print("="*70)

    rms_vk = analyse["rms_nach_vk"]
    ascii_vk = analyse["ascii_nach_vk"]
    print(f"  V-Zellen: {rms_vk['V_count']}, mean RMS={rms_vk['V_mean']:.4f}, mean ASCII={ascii_vk['V_mean']:.2f}")
    print(f"  K-Zellen: {rms_vk['K_count']}, mean RMS={rms_vk['K_mean']:.4f}, mean ASCII={ascii_vk['K_mean']:.2f}")
    print(f"  → V-Zellen sind {abs(ascii_vk['V_mean']-ascii_vk['K_mean']):.1f} ASCII-Punkte "
          f"{'höher' if ascii_vk['V_mean'] > ascii_vk['K_mean'] else 'niedriger'} als K-Zellen")

    # === MUSTER 9: Vokal-Positionen pro Wort ===
    print("\n" + "="*70)
    print("MUSTER 9: VOKAL-POSITIONEN PRO WORT")
    print("="*70)

    for wort, positions in analyse["vokal_pos_pro_wort"].items():
        # Visualisiere: 14 Zeichen, V an Vokal-Position
        line = ["."] * 14
        for p in positions:
            line[p] = "V"
        print(f"  {wort:<20} {''.join(line)}  V@{positions}")

    # === ZUSAMMENFASSUNG ===
    print("\n" + "="*70)
    print("ZUSAMMENFASSUNG — 154 ZELLEN GELESEN")
    print("="*70)

    # Interessante Befunde
    n_v_zellen = sum(1 for z in zellen if z["vk"] == "V")
    n_k_zellen = sum(1 for z in zellen if z["vk"] == "K")
    print(f"\n  Total Zellen: 154")
    print(f"  V-Zellen: {n_v_zellen} ({n_v_zellen/154*100:.1f}%)")
    print(f"  K-Zellen: {n_k_zellen} ({n_k_zellen/154*100:.1f}%)")
    print(f"  Konsonant/Vokal-Ratio: {n_k_zellen/max(1,n_v_zellen):.2f}")

    # Unique V/K-Codes
    codes = list(analyse["vk_codes_pro_wort"].values())
    n_unique_codes = len(set(codes))
    print(f"  Unique V/K-Codes: {n_unique_codes} (von max 11)")

    # Speichern
    output_dir = Path("bbox/v24_20260708")
    output = {
        "phase": "V25 Schritt 4 — 154 Zellen multidimensional",
        "datum": "2026-07-08",
        "n_zellen": len(zellen),
        "beispiel_zelle_0": zellen[0],
        "analyse": {
            "buchstaben_haeufigkeit": analyse["buchstaben_haeufigkeit"],
            "vk_pro_position": {str(k): v for k, v in analyse["vk_pro_position"].items()},
            "ascii_pro_position": {str(k): v for k, v in analyse["ascii_pro_position"].items()},
            "rms_pro_position": {str(k): v for k, v in analyse["rms_pro_position"].items()},
            "vk_codes_pro_wort": analyse["vk_codes_pro_wort"],
            "rms_nach_vk": analyse["rms_nach_vk"],
            "ascii_nach_vk": analyse["ascii_nach_vk"],
            "vokal_pos_pro_wort": analyse["vokal_pos_pro_wort"],
        },
        "zusammenfassung": {
            "n_v_zellen": n_v_zellen,
            "n_k_zellen": n_k_zellen,
            "kons_vok_ratio": round(n_k_zellen / max(1, n_v_zellen), 2),
            "n_unique_vk_codes": n_unique_codes,
        },
        "reference": "154 Zellen = 11 Wörter × 14 Buchstaben. Rein symbolisch, KEIN ML.",
    }
    output_path = output_dir / "v25_154_zellen.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n→ 154-Zellen-Analyse gespeichert: {output_path}")


if __name__ == "__main__":
    hauptprogramm()
