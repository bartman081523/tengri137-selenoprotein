#!/usr/bin/env python3
"""
load_schmeh_hints.py — parst Tengri137_raw_text.txt (Schmeh 2017) als HINWEIS-Quelle.

WICHTIG: Schmehs Rekonstruktion ist NICHT Wahrheit, sondern mögliche Hinweise
zur Entschlüsselung. Wenn V4-Widersprüche findet, ist die V4-Analyse richtig
und die Schmeh-Rekonstruktion falsch (oder umgekehrt) — der V4-Plan erfordert
explizite Reproduzierbarkeit, damit alte Kodierungsfehler aufgedeckt werden können.

Pro Page (P01-P23) liefert der Loader:
  - lines[]: Liste von Zeilen mit type ∈ {latin, glyph, formula, numeric, unknown, manifest}
            und Hinweis-Text (vermuteter Inhalt der Zeile)
  - descriptions[]: Liste von {description}-Blöcken (z.B. "Chinese Oracle script for tian")
  - has_glyphs: bool (mindestens 1 Glyph-Block)
  - has_magic_cube: bool (P5-P8 haben 3x3 Cubes mit 666)
  - has_rings: bool (P9-P11)
  - has_burumut_block: bool (P23 hat 12x10 Buchstaben-Block)
  - expected_total_lines: int
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


# Heuristik-Marker aus Schmehs Rekonstruktion
LATIN_MARKERS = re.compile(r"^[A-Z][A-Z\s\.\,\-\:\;\(\)\?\!\d'\"&/]+$")
GLYPH_BLOCK = re.compile(r"^\{.*\}$")
MAGIC_CUBE_MARKER = re.compile(r"\(=666\)")
RING_MARKER = re.compile(r"\{\d+ RINGS? - 666\}|Odin's triple horn")
FORMULA_MARKER = re.compile(r"π7|π\^7|2\^9|3\^-1|5\^9|×|197|5563|41681|prime", re.IGNORECASE)
NUMERIC_LINE = re.compile(r"^[\d\s\^\*\-\+\.\(\)\=xX×\/]+$")


def classify_line(text: str) -> str:
    """Klassifiziert eine Zeile aus Schmehs Rekonstruktion."""
    t = text.strip()
    if not t:
        return "empty"
    if GLYPH_BLOCK.match(t):
        # {symbol, ...} oder {in the background -> ...} oder {image}
        return "glyph_description"
    if RING_MARKER.search(t):
        return "ring_marker"
    if MAGIC_CUBE_MARKER.search(t):
        return "magic_cube_line"
    if NUMERIC_LINE.match(t) and any(c.isdigit() for c in t):
        return "numeric"
    if FORMULA_MARKER.search(t):
        return "formula"
    if LATIN_MARKERS.match(t):
        return "latin"
    return "unknown"


def parse_raw_text(path: Path) -> dict:
    """Parst Tengri137_raw_text.txt und liefert pro Page strukturierte Daten."""
    text = path.read_text(encoding="utf-8")
    # Split auf Page-Marker
    page_pattern = re.compile(r"^PAGE (\d+)$", re.MULTILINE)
    matches = list(page_pattern.finditer(text))
    pages = {}
    for i, m in enumerate(matches):
        pn = int(m.group(1))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        pages[pn] = parse_page_block(pn, block)
    return pages


def parse_page_block(pn: int, block: str) -> dict:
    """Parst einen einzelnen Page-Block aus Schmehs Rekonstruktion."""
    lines = []
    descriptions = []
    for raw_line in block.split("\n"):
        line = raw_line.strip()
        if not line or line.startswith("===") or line.startswith("###"):
            continue
        if line.startswith("{-") or line.startswith("{ "):
            # {PAGE N — visual elements} oder { - ... }
            descriptions.append(line)
            continue
        cls = classify_line(line)
        if cls == "empty":
            continue
        entry = {"text": line, "type": cls}
        lines.append(entry)
    # Page-Features
    has_glyphs = any(l["type"] == "glyph_description" for l in lines)
    has_magic_cube = any(l["type"] == "magic_cube_line" for l in lines)
    has_rings = any(l["type"] == "ring_marker" for l in lines)
    has_burumut_block = pn == 23  # P23 hat 12x10 Buchstaben-Block am Ende
    return {
        "page": f"p{pn:02d}",
        "n_lines": len(lines),
        "n_latin": sum(1 for l in lines if l["type"] == "latin"),
        "n_glyphs": sum(1 for l in lines if l["type"] == "glyph_description"),
        "n_numeric": sum(1 for l in lines if l["type"] == "numeric"),
        "n_formula": sum(1 for l in lines if l["type"] == "formula"),
        "n_unknown": sum(1 for l in lines if l["type"] == "unknown"),
        "has_glyphs": has_glyphs,
        "has_magic_cube": has_magic_cube,
        "has_rings": has_rings,
        "has_burumut_block": has_burumut_block,
        "lines": lines,
        "descriptions": descriptions,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-text", type=Path,
                    default=ROOT / "Tengri137_raw_text.txt")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    pages = parse_raw_text(args.raw_text)
    out = {
        "source": str(args.raw_text),
        "extraction_note": (
            "Schmeh 2017 Acrobat-PDFMaker rekonstruktion. "
            "NICHT Wahrheit, sondern HINWEIS-Quelle für V4-Validierung. "
            "Widersprüche zwischen V4-Pixel-Analyse und Schmeh-Rekonstruktion "
            "müssen in V4-Output explizit markiert werden."
        ),
        "n_pages": len(pages),
        "page_features": {pn: {k: v for k, v in p.items() if k != "lines" and k != "descriptions"}
                          for pn, p in pages.items()},
    }
    # Single hint file with per-page lines
    for pn, p in pages.items():
        (args.out / f"p{pn:02d}_hints.json").write_text(
            json.dumps(p, indent=2, ensure_ascii=False))
    (args.out / "all_hints.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))

    # Summary
    print(f"Schmeh-Hints extrahiert für {len(pages)} Pages:")
    for pn in sorted(pages):
        p = pages[pn]
        flags = []
        if p["has_glyphs"]:
            flags.append("GLYPH")
        if p["has_magic_cube"]:
            flags.append("CUBE")
        if p["has_rings"]:
            flags.append("RINGS")
        if p["has_burumut_block"]:
            flags.append("BURUMUT")
        flag_str = " ".join(flags) if flags else ""
        print(f"  p{pn:02d}: {p['n_latin']:>3} latin, {p['n_glyphs']:>2} glyph, "
              f"{p['n_numeric']:>3} numeric, {p['n_formula']:>2} formula "
              f"-> {flag_str}")


if __name__ == "__main__":
    main()
