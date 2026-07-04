#!/usr/bin/env python3
"""
parse_schmeh_raw.py — Extrahiert Schmeh-2017-Rekonstruktion aus Tengri137_raw_text.txt.

Input:  Tengri137_raw_text.txt
Output: bbox/schmeh_hints_20260704_V4/schmeh_parsed.json
        {
          "p01": {
            "manifesto_lines": [
              "TENGRI IS THE SOURCE OF IMPORTANT WRITINGS. ONLY THE CHOSEN SOULS KNOW THE MEANING...",
              "YOUR FAITH WILL WEAKEN YOU..."
            ],
            "letter_block_lines": [],  # P17-P23 BURUMUT-style Buchstaben-Blöcke
            "symbol_descriptions": [
              {"description": "one Chinese Oracle-script character for 天 (tiān, \"heaven\")", "kind": "chinese_oracle_script_tian"}
            ]
          },
          ...
        }

Algorithmus:
1. Parse Tengri137_raw_text.txt
2. Pro Page: Trenne Manifesto-Lines (uppercase prose) von Letter-Block (einzelne chars)
   und Symbol-Description (in {description} Klammern)
3. Manifesto-Lines: Zeilenumbrüche zusammenfügen (z.B. "ONL\nY" → "ONLY")
4. Letter-Block: nur A-Z chars, einzelne Leerzeichen-getrennt
5. Output: pro Page
"""
import json
import re
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


def parse_schmeh_raw(path: Path) -> dict:
    text = path.read_text()
    # Split by PAGE markers
    pages = re.split(r"#{30,}\s*\n\s*PAGE (\d+)\s*\n\s*#{30,}", text)
    # pages[0] = intro, pages[1] = '1', pages[2] = body1, ...

    result = {}
    for i in range(1, len(pages), 2):
        pid = pages[i].zfill(2)  # '1' → '01'
        body = pages[i + 1] if i + 1 < len(pages) else ""

        # Schritt 1: Trenne nach Paragraph (blank line)
        paragraphs = re.split(r"\n\s*\n", body.strip())

        manifesto_lines = []
        letter_block_lines = []
        numerics_lines = []
        symbol_descriptions = []

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            if "END OF FILE" in para:
                continue
            # Symbol-Description Block-Header (PAGE X — visual elements)
            if "PAGE" in para and "—" in para and "visual elements" in para:
                continue
            # Symbol-Description
            if para.startswith("{") and para.endswith("}"):
                inner = para[1:-1].strip()
                if not inner.startswith("PAGE"):
                    desc = " ".join(inner.split())
                    if len(desc) > 10:
                        symbol_descriptions.append({"description": desc})
                continue
            # Numerics: Prime-Factorization
            if "[" in para and "]" in para and "*" in para:
                numerics_lines.append(para)
                continue

            # Schritt 2: Trenne Paragraph in einzelne Zeilen
            raw_lines = para.split("\n")

            for line in raw_lines:
                line = line.strip()
                if not line:
                    continue
                # Letter-Block-Zeile: einzelne Buchstaben (B U R U M U T) — jedes Char
                # mit Whitespace dazwischen
                if re.match(r"^([A-Z] )+[A-Z]$", line):
                    letter_block_lines.append(line)
                    continue
                # Numerics: Magic-Cube-style "638      24       4      (=666)"
                if re.match(r"^(\s*\d+\s*){3,}", line) and re.search(r"\(=(\d+)\)\s*$", line):
                    numerics_lines.append(line)
                    continue
                # Numerics: Primfaktorzerlegung "2^5 * 13 * 37 * 179 * 471077143"
                if re.match(r"^\s*\d+(\^\d+)?(\s*\*\s*\d+(\^\d+)?)+\s*$", line):
                    numerics_lines.append(line)
                    continue
                # Numerics: Trenn-Linie "----..."
                if re.match(r"^-{10,}$", line.strip()):
                    # Skip Trennlinien (gehören zu vorheriger Numerics)
                    continue
                # Manifesto: Wort-Zeilenumbrüche entfernen (nicht durch Space)
                # Wenn Zeile mitten im Wort endet (z.B. "ONL"), wird sie mit
                # der nächsten zusammengefügt.
                joined = line
                manifesto_lines.append(joined)

        result[pid] = {
            "manifesto_lines": manifesto_lines,
            "letter_block_lines": letter_block_lines,
            "numerics_lines": numerics_lines,
            "symbol_descriptions": symbol_descriptions,
        }
    return result


def main():
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--in", dest="inp", type=Path,
                    default=ROOT / "Tengri137_raw_text.txt")
    ap.add_argument("--out", type=Path,
                    default=ROOT / "bbox" / "schmeh_hints_20260704_V4" / "schmeh_parsed.json")
    args = ap.parse_args()
    parsed = parse_schmeh_raw(args.inp)
    args.out.write_text(json.dumps(parsed, indent=2, ensure_ascii=False))
    print(f"Parsed {len(parsed)} pages → {args.out}")
    for pid, data in parsed.items():
        n_manif = len(data["manifesto_lines"])
        n_letter = len(data["letter_block_lines"])
        n_sym = len(data["symbol_descriptions"])
        print(f"  p{pid}: {n_manif} manifesto, {n_letter} letter-block, {n_sym} symbol-desc")


if __name__ == "__main__":
    main()
