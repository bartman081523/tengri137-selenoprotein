#!/usr/bin/env python3
"""
phase4b_schmeh_fusion.py — Fusioniert V4-Vision-Daten MIT Schmeh-2017-Rekonstruktion.

Input:
  - bbox/pages_merged_20260704_V4/p{NN}.json  (Phase 4 Output)
  - bbox/schmeh_hints_20260704_V4/schmeh_parsed.json  (Schmeh-Manifesto + Letter-Block + Symbol-Description)
  - bbox/schmeh_hints_20260704_V4/p{NN}_hints.json  (Schmeh-Hint mit n_latin etc.)

Output:
  - bbox/pages_merged_20260704_V4/p{NN}.json  (überschrieben mit Fusion)
  - bbox/schmeh_hints_20260704_V4/schmeh_fusion_log.json  (was woher kam)

Algorithmus:
1. Lade Schmeh-parsed (manifesto_lines, letter_block_lines, symbol_descriptions)
2. Lade Phase-4-Output
3. Für jede Page:
   a) Wenn Vision n_latin < Schmeh n_latin:
      - Ergänze fehlende Latin-Tokens aus Schmeh-Manifesto
      - Markiere source="schmeh_fusion"
   b) Letter-Block (P17-P23 BURUMUT) → neue Region "letter_block" mit den 11-12 Zeilen
   c) Symbol-Description → in "graphics" der entsprechenden Region
4. Schreibe fusionierte Page
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


def fuse_page(page_data: dict, schmeh_parsed: dict, schmeh_hint: dict) -> dict:
    """Fusioniere Schmeh-Daten in eine V4-Page.

    Strategie: Schmeh liefert die VOLLSTÄNDIGEN lateinischen Sätze (ohne Wort-Zeilenumbrüche),
    während Vision nur FRAGMENTE liefert (einzelne Zeilen). Wir markieren die V4-Regionen
    mit `schmeh_complete_text` als Referenz für Leser.
    """
    page_id = page_data.get("page_id", "")
    page_num = page_id.lstrip("p")  # "p01" → "01"
    schmeh_p = schmeh_parsed.get(page_num, schmeh_parsed.get(page_id, {}))
    manifesto_lines = schmeh_p.get("manifesto_lines", [])
    letter_block_lines = schmeh_p.get("letter_block_lines", [])
    symbol_descriptions = schmeh_p.get("symbol_descriptions", [])

    n_latin_v4 = page_data.get("n_latin_tokens", 0)
    n_latin_schmeh = schmeh_hint.get("n_latin", 0)

    log = {
        "page_id": page_id,
        "n_latin_v4": n_latin_v4,
        "n_latin_schmeh": n_latin_schmeh,
        "n_manifesto_parsed": len(manifesto_lines),
        "n_letter_block_parsed": len(letter_block_lines),
        "n_symbol_desc_parsed": len(symbol_descriptions),
        "added_manifesto": 0,
        "added_letter_block_region": False,
        "added_symbol_descriptions": 0,
    }

    # 1) Manifesto-Lines: Wort-Zeilenumbrüche entfernen + als zusammenhängende Sätze
    #    in eine eigene "schmeh_complete" Region
    if manifesto_lines:
        # Zusammenfügen: Manifesto-Lines, die auf gleicher Zeile enden
        # Heuristik: Wenn eine Zeile mitten im Wort endet (z.B. "ONL"),
        # mit nächster Zeile zusammenfügen.
        cleaned_manifesto = []
        i = 0
        while i < len(manifesto_lines):
            current = manifesto_lines[i]
            # Wenn current nicht mit Punkt/Quote/... endet und die nächste Zeile
            # mit einem Uppercase-Buchstaben ohne Punkt beginnt → zusammenfügen
            while (i + 1 < len(manifesto_lines)
                   and not current.rstrip().endswith((".", "?", "!", '"', "'", ":"))
                   and manifesto_lines[i + 1].strip()):
                # Wenn aktuelles Wort nicht zu Ende ist (endet mitten im Wort)
                last_word = current.rstrip().split()[-1]
                next_first_word = manifesto_lines[i + 1].strip().split()[0] if manifesto_lines[i + 1].strip() else ""
                # Wenn last_word ein Wortfragment ist (kürzer als 3 oder endet mit ungewöhnlichem Suffix)
                # ODER next_first_word ist Uppercase ohne Punkt → join
                if (len(last_word) < 3 or
                        (next_first_word and next_first_word[0].isupper()
                         and not next_first_word.endswith("."))):
                    current = current + manifesto_lines[i + 1].lstrip()
                    i += 1
                else:
                    break
            cleaned_manifesto.append(current)
            i += 1
        # Whitespace normalisieren
        cleaned_manifesto = [re.sub(r"\s+", " ", m).strip() for m in cleaned_manifesto]
        # Nur Lines mit ≥ 3 Wörtern
        cleaned_manifesto = [m for m in cleaned_manifesto if len(m.split()) >= 3]

        # Neue "schmeh_complete" Region mit allen Manifesto-Lines
        if cleaned_manifesto:
            # Region-ID muss Schema-Validierung passieren: p{NN}_R{NNN}
            n_existing = len(page_data.get("regions", []))
            page_data["regions"].append({
                "region_id": f"{page_id}_R{n_existing + 1:02d}_SCHMEH",
                "bbox": [0, 0, 0, 0],
                "region_type": "latin_text",
                "description": (f"Schmeh 2017 vollständige lateinische Sätze "
                                f"({len(cleaned_manifesto)} lines, joined)"),
                "lines": [],
                "glyphs": [],
                "latin_tokens": [
                    {"text": m, "bbox": [0, 0, 0, 0], "conf": 0.95,
                     "line_id": idx + 1, "source": "schmeh_complete"}
                    for idx, m in enumerate(cleaned_manifesto)
                ],
                "formulas": [],
                "numerics": [],
                "graphics": [],
                "uncertain": [],
            })
            log["added_manifesto"] = len(cleaned_manifesto)

    # 2) Letter-Block: BURUMUT-Style (P19-P23) als eigene Region
    if letter_block_lines:
        n_existing = len(page_data.get("regions", []))
        page_data["regions"].append({
            "region_id": f"{page_id}_R{n_existing + 1:02d}_LETTERBLOCK",
            "bbox": [0, 0, 0, 0],
            "region_type": "burumut_block",
            "description": f"Schmeh letter-block ({len(letter_block_lines)} Zeilen, BURUMUT-Style)",
            "lines": [],
            "glyphs": [],
            "latin_tokens": [
                {"text": line, "bbox": [0, 0, 0, 0], "conf": 0.95,
                 "line_id": idx + 1, "source": "schmeh_complete"}
                for idx, line in enumerate(letter_block_lines)
            ],
            "formulas": [],
            "numerics": [],
            "graphics": [],
            "uncertain": [],
        })
        log["added_letter_block_region"] = True

    # 3) Symbol-Description als "graphics"-Eintrag in erste Magic-Cube / Glyph-Region
    if symbol_descriptions:
        target_region = None
        for region in page_data.get("regions", []):
            rtype = region.get("region_type", "")
            if rtype in ("magic_cube", "rings_sigil", "graphic_line", "drawing",
                         "glyph_block", "glyph_raster", "header", "footer"):
                target_region = region
                break
        if target_region is None and page_data.get("regions"):
            target_region = page_data["regions"][0]
        if target_region:
            for sd in symbol_descriptions:
                target_region["graphics"].append({
                    "type": "schmeh_symbol",
                    "description": sd["description"],
                    "bbox": [0, 0, 0, 0],
                })
                log["added_symbol_descriptions"] += 1

    # 4) Update n_latin_tokens (jetzt inkl. schmeh_complete)
    n_latin_total = sum(len(r.get("latin_tokens", [])) for r in page_data["regions"])
    page_data["n_latin_tokens"] = n_latin_total

    return log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=Path, required=True,
                    help="bbox/pages_merged_<TS>/")
    ap.add_argument("--schmeh-parsed", type=Path, required=True,
                    help="bbox/schmeh_hints_<TS>/schmeh_parsed.json")
    ap.add_argument("--schmeh-hints", type=Path, required=True,
                    help="bbox/schmeh_hints_<TS>/  (p{NN}_hints.json)")
    ap.add_argument("--log", type=Path, required=True,
                    help="Output log file")
    args = ap.parse_args()

    schmeh_parsed = json.loads(args.schmeh_parsed.read_text())
    log_total = []
    for i in range(1, 24):
        page_id = f"p{i:02d}"
        page_path = args.pages / f"{page_id}.json"
        if not page_path.exists():
            continue
        page_data = json.loads(page_path.read_text())
        schmeh_hint_path = args.schmeh_hints / f"{page_id}_hints.json"
        schmeh_hint = json.loads(schmeh_hint_path.read_text()) if schmeh_hint_path.exists() else {}
        log = fuse_page(page_data, schmeh_parsed, schmeh_hint)
        log_total.append(log)
        # Save
        page_path.write_text(json.dumps(page_data, indent=2, ensure_ascii=False))
        print(f"  {page_id}: V4={log['n_latin_v4']} → final={page_data['n_latin_tokens']}, "
              f"added_manifesto={log['added_manifesto']}, "
              f"letter_block={log['added_letter_block_region']}, "
              f"symbol_desc={log['added_symbol_descriptions']}")
    args.log.write_text(json.dumps(log_total, indent=2, ensure_ascii=False))
    n_added = sum(l["added_manifesto"] for l in log_total)
    n_lb = sum(1 for l in log_total if l["added_letter_block_region"])
    n_sd = sum(l["added_symbol_descriptions"] for l in log_total)
    print(f"\nTotal: {n_added} manifesto-lines added, {n_lb} letter-block regions, {n_sd} symbol-descriptions")


if __name__ == "__main__":
    main()
