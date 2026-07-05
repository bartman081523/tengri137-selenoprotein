#!/usr/bin/env python3
"""
phase4c_decode_test.py — V6 Phase 4c: Decode-Test mit hypothetischem Mapping.

Wenn das hypothetische Mapping (G28=E, G25=O, G16=T, ...) korrekt ist, müsste
die dekodierte Tengri-Sequenz von p01 SCHMEHS Klartext ergeben (oder sehr ähnlich).

Test:
1. Lade Token-Stream p01
2. Wende hypothetisches Mapping an: G28→E, G25→O, G16→T, ...
3. Vergleiche mit Schmehs manifesto_lines für p01
4. Bewertung: Welche % der Buchstaben matchen?
"""
import argparse
import json
from collections import Counter
from pathlib import Path


# Mapping aus Phase 4b: Rang-basiert
RANK_MAPPING = {
    "G28": "E", "G25": "O", "G16": "T", "G18": "N", "G19": "I",
    "G29": "A", "G05": "S", "G26": "R", "G03": "H", "G13": "U",
    "G10": "L", "G07": "C", "G23": "D", "G09": "W", "G06": "Y",
    "G11": "M", "G17": "F", "G12": "G", "G08": "B", "G21": "K",
    "G24": "P", "G01": "V", "G30": "X", "G14": "J", "G02": "Q",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokenstream", type=Path, required=True)
    ap.add_argument("--schmeh-parsed", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--pages", type=str, default="01,02,03,04")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    schmeh = json.loads(args.schmeh_parsed.read_text())
    pages = args.pages.split(",")

    results = {}
    for pid in pages:
        ts_path = args.tokenstream / f"p{int(pid):02d}.json"
        if not ts_path.exists():
            continue
        ts = json.loads(ts_path.read_text())
        tengri_tokens = [t["glyph_id"] for t in ts["tokens"]]

        # Dekodiere
        decoded = "".join(RANK_MAPPING.get(t, "?") for t in tengri_tokens)
        n_unk = decoded.count("?")
        n_total = len(decoded)

        # Hole Schmeh-Klartext
        klartext = ""
        if pid in schmeh:
            for line in schmeh[pid]["manifesto_lines"]:
                klartext += line + " "
        klartext = klartext.upper()
        klartext_clean = "".join(c for c in klartext if c.isalpha())

        # Letter-frequency-Vergleich (statt string-exact, weil Wortgrenzen verschieden)
        tengri_counts = Counter(decoded.replace("?", ""))
        schmeh_counts = Counter(klartext_clean)

        # Z-Score-Test pro Buchstabe
        print(f"\n=== p{pid} ===")
        print(f"  Tengri Tokens: {n_total} ({n_unk} unknown)")
        print(f"  Schmeh Klartext: {len(klartext_clean)} Buchstaben")
        print(f"  Dekodiert (Top-50): {decoded[:200]}")
        print(f"  Klartext (Top-50):  {klartext_clean[:200]}")

        # Wenn Mapping korrekt, müsste die häufigste Glyph in Tengri dem häufigsten Buchstaben in Klartext entsprechen
        # Hier: wir testen Buchstabe-für-Buchstabe
        print(f"\n  Top-5 dekodiert:  {tengri_counts.most_common(5)}")
        print(f"  Top-5 Schmeh:     {schmeh_counts.most_common(5)}")

        results[pid] = {
            "n_tengri_tokens": n_total,
            "n_unknown": n_unk,
            "n_schmeh_letters": len(klartext_clean),
            "decoded_sample": decoded[:500],
            "schmeh_sample": klartext_clean[:500],
            "decoded_top5": tengri_counts.most_common(5),
            "schmeh_top5": schmeh_counts.most_common(5),
        }

    out_path = args.out / "decode_test.json"
    out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
