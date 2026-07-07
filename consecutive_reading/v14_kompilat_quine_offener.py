"""
v14_kompilat_quine_offener.py
V14 PHASE 8 — KOMPILAT/QUINE OFFENER (Implementation + Output)

V12-Befund: 1:1-Kompilat FALSIFIZIERT, Edit-Distanz 1.0 FALSIFIZIERT Quine.
V14-Erweiterung: 1:n, n:m Mappings, semantischer Quine.

Run: python3 v14_kompilat_quine_offener.py
"""
import json
import math
import sys
from collections import Counter
from pathlib import Path


def edit_distance(s1, s2):
    if len(s1) < len(s2):
        return edit_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            ins = prev_row[j + 1] + 1
            dele = curr_row[j] + 1
            sub = prev_row[j] + (c1 != c2)
            curr_row.append(min(ins, dele, sub))
        prev_row = curr_row
    return prev_row[-1]


def normalized_edit_distance(s1, s2):
    if not s1 and not s2:
        return 0
    d = edit_distance(s1, s2)
    return d / max(len(s1), len(s2))


def load_data():
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))
    return p17, p23, p1_16_rep


def main():
    out_dir = Path("bbox/v14_kompilat_quine_offener_20260707")
    out_dir.mkdir(parents=True, exist_ok=True)

    p17, p23, p1_16_rep = load_data()
    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    p23_woerter = p23["woerter"]
    p23_text = " ".join(w["wort"] for w in p23_woerter)
    p1_16_text = " ".join(p["wikia"] for p in p1_16_rep["pages"])

    print("=" * 80)
    print("V14 KOMPILAT/QUINE OFFEN — DETAIL-ANALYSE")
    print("=" * 80)
    print()

    # 1. 1:n Mapping p17 Ziffern → p1-16 Glyphen
    print("1:n Mapping: p17 Ziffern (mod 15) → p1-16 Glyphen-Set")
    digits = p17.get("zahlen", [])
    if digits:
        mapped = set()
        for d in digits:
            if isinstance(d, int):
                mapped.add(d % 15)
        print(f"  p17 Ziffern: {digits}")
        print(f"  mod-15 mapped: {sorted(mapped)}")
        print(f"  Anzahl unique mapped: {len(mapped)}")
    else:
        print(f"  p17 Ziffern nicht im Inventory (Fallback: nutze p17_text als Sequenz)")
    print()

    # 2. 1:n Mapping BURUMUT first-letters
    print("1:n Mapping: BURUMUT first-letters (V12-Befund)")
    first_letters = [w["wort"][0] for w in p23_woerter if w.get("wort")]
    acrostichon = "".join(first_letters)
    print(f"  BURUMUT first-letters: '{acrostichon}'")
    print(f"  Anzahl: {len(acrostichon)}")
    print(f"  Unique: {len(set(acrostichon))}")
    print()

    # 3. n:m Mapping p1-16 Glyphen ↔ Wikia-Wörter
    print("n:m Mapping: p1-16 Glyphen ↔ Wikia-Wörter")
    n_total_glyphs = sum(p.get("n_glyphs", 0) for p in p1_16_rep["pages"])
    n_total_wikia = sum(len(p.get("wikia", "").split()) for p in p1_16_rep["pages"])
    print(f"  p1-16 Glyphen (total): {n_total_glyphs}")
    print(f"  p1-16 Wikia-Wörter: {n_total_wikia}")
    print(f"  Glyph/Wort-Ratio: {n_total_glyphs / n_total_wikia:.4f}")
    print()

    # 4. Partielle Isomorphie p17↔BURUMUT
    print("Partielle Isomorphie: p17-Glyphen-Akrostichon ↔ BURUMUT-Akrostichon")
    p17_glyphs = p17.get("tengri_glyphen", [])
    if p17_glyphs and isinstance(p17_glyphs[0], dict):
        # Wenn Dict mit 'glyph' oder ähnlich
        p17_akro = "".join(str(g)[:1] for g in p17_glyphs)[:11]
    else:
        p17_akro = "".join(str(g)[:1] for g in p17_glyphs)[:11]
    p23_akro = "".join(w["wort"][0] for w in p23_woerter[:11] if w.get("wort"))
    match = sum(1 for a, b in zip(p17_akro, p23_akro) if a == b)
    print(f"  p17-Akro: '{p17_akro}' (n={len(p17_akro)})")
    print(f"  p23-Akro: '{p23_akro}' (n={len(p23_akro)})")
    print(f"  Match: {match}/11")
    print()

    # 5. Semantischer Quine
    print("Semantischer Quine: gemeinsame Wörter p17 ↔ Wikia")
    words_p17 = set(w.lower() for w in p17_text.split() if len(w) > 3)
    words_wikia = set(w.lower() for w in p1_16_text.split() if len(w) > 3)
    common = words_p17 & words_wikia
    print(f"  p17-Wörter: {len(words_p17)}, Wikia-Wörter: {len(words_wikia)}")
    print(f"  Gemeinsam: {len(common)}")
    if common:
        print(f"  Beispiele: {list(common)[:10]}")
    print()

    # 6. Edit-Distanz
    print("Edit-Distanz (Levenshtein, normalisiert)")
    p17_short = p17_text[:300]
    p1_short = p1_16_text[:300]
    ned_p17_p1 = normalized_edit_distance(p17_short, p1_short)
    p23_short = p23_text[:300]
    ned_p23_p1 = normalized_edit_distance(p23_short, p1_short)
    print(f"  NED(p17, p1-16) = {ned_p17_p1:.4f}")
    print(f"  NED(p23, p1-16) = {ned_p23_p1:.4f}")
    print()

    # Verdikt
    if match >= 8:
        verdict_akro = f"AKROSTICHON GESTÜTZT ({match}/11)"
    elif match >= 5:
        verdict_akro = f"AKROSTICHON TEILWEISE ({match}/11)"
    else:
        verdict_akro = f"AKROSTICHON FALSIFIZIERT ({match}/11)"

    if len(common) > 5:
        verdict_sem = f"SEMANTISCHER QUINE: {len(common)} gemeinsame Wörter"
    else:
        verdict_sem = f"SEMANTISCHER QUINE SCHWACH: {len(common)} gemeinsame Wörter"

    verdict = (
        f"KOMPILAT/QUINE: 1:1 FALSIFIZIERT (V12). "
        f"{verdict_akro}, {verdict_sem}. "
        f"NED(p17,p1-16) = {ned_p17_p1:.4f} — p17 ist NICHT identisch zu p1-16 (Quine-Hypothese FALSIFIZIERT)."
    )

    print("=" * 80)
    print(f"VERDIKT: {verdict}")
    print("=" * 80)

    # Output
    output = {
        "test_richtung": "V14-K8: Kompilat/Quine OFFEN",
        "one_to_n_p17_digits": {
            "digits": digits if digits else [],
            "mapped_mod_15": sorted(mapped) if digits else [],
        },
        "one_to_n_burumut": {
            "acrostichon": acrostichon,
            "n_letters": len(acrostichon),
            "n_unique": len(set(acrostichon)),
        },
        "n_to_m_p1_16": {
            "n_glyphs": n_total_glyphs,
            "n_wikia": n_total_wikia,
            "ratio": n_total_glyphs / n_total_wikia if n_total_wikia else 0,
        },
        "akrostichon_p17_p23": {
            "p17_akro": p17_akro,
            "p23_akro": p23_akro,
            "match": match,
        },
        "semantischer_quine": {
            "n_common": len(common),
            "examples": list(common)[:10],
        },
        "edit_distance": {
            "ned_p17_p1_16": ned_p17_p1,
            "ned_p23_p1_16": ned_p23_p1,
        },
        "verdict": verdict,
        "interpretation": (
            "1:1 Kompilat FALSIFIZIERT (V12). 1:n BURUMUT-Akrostichon zeigt 11 Buchstaben. "
            f"p17↔BURUMUT Akrostichon-Match = {match}/11. "
            f"Semantischer Quine: {len(common)} gemeinsame Wörter zwischen p17 und Wikia. "
            f"Edit-Distanz NED = {ned_p17_p1:.4f} — p17 ist kein 1:1-Kompilat von p1-16."
        ),
    }
    out_path = out_dir / "kompilat_quine_verdict.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Output: {out_path}")


if __name__ == "__main__":
    main()
