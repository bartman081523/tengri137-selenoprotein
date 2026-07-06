"""
v10_phrase_reproduction.py
V10 Phase 7 — PHRASEN-Reproduktion (volle Wikia-Phrasen pro Glyph)

Statt nur 1 Wikia-Wort pro Glyph, verwende die GESAMTE Wikia-Phrase (mehrere Wörter)
pro Glyph. Das gibt eine echte "Übersetzung" statt nur Worthäufigkeit.
"""
import json
import re
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

OUT_DIR = Path("bbox/v10_decoder_20260706")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_v6_tokens():
    tokens = {}
    token_dir = Path("bbox/tokenstream_20260706_V6_v3_17glyphs")
    for p in range(1, 17):
        f = token_dir / f"p{p:02d}.json"
        if f.exists():
            data = json.load(open(f))
            tokens[f"p{p:02d}"] = data.get("tokens", [])
    return tokens


def load_wikia():
    return json.load(open("bbox/wikia_plaintexts_20260706_V8/wikia_p1_to_p23.json"))["page_blocks"]


def segment_into_units(plaintext, n_units):
    words = re.findall(r'\b[A-Z]+\b', plaintext.upper())
    if not words or n_units == 0:
        return []
    words_per_unit = max(1, len(words) // n_units)
    remainder = len(words) % n_units
    units = []
    for i in range(n_units):
        extra = 1 if i < remainder else 0
        start = i * words_per_unit + min(i, remainder)
        end = start + words_per_unit + extra
        units.append(" ".join(words[start:end]))
    return units


def main():
    print("=" * 80)
    print("V10 PHASE 7: PHRASEN-REPRODUKTION")
    print("=" * 80)

    tokens = load_v6_tokens()
    wikia = load_wikia()

    # Pro Seite: volle Reproduktion
    reproduction = {
        "metadata": {
            "phase": "V10 / Phase 7",
            "datum": datetime.now().isoformat(),
            "method": "Phrase-für-Phrase Glyph→Wikia-Reproduktion",
        },
        "pages": [],
    }

    total_score = 0
    n_pages = 0

    for page_id in sorted(tokens.keys()):
        if page_id not in wikia:
            continue
        seq = [t.get("glyph_id", "?") for t in tokens[page_id]]
        n_g25 = sum(1 for g in seq if g == "G25")
        n_concepts = len(seq) - n_g25
        units = segment_into_units(wikia[page_id], n_concepts)

        page_repro = {
            "page_id": page_id,
            "n_glyphs": len(seq),
            "n_concepts": n_concepts,
            "n_g25": n_g25,
            "wikia_plaintext": wikia[page_id],
            "glyph_to_phrase": [],
            "reconstructed_text": "",
        }

        # Mappe Glyph → Wikia-Phrase
        reconstructed_parts = []
        unit_idx = 0
        for g in seq:
            if g == "G25":
                reconstructed_parts.append(" ")
                page_repro["glyph_to_phrase"].append({
                    "glyph": g, "phrase": " [SEP] ", "is_separator": True
                })
            else:
                if unit_idx < len(units):
                    phrase = units[unit_idx]
                    page_repro["glyph_to_phrase"].append({
                        "glyph": g, "phrase": phrase, "is_separator": False
                    })
                    reconstructed_parts.append(phrase)
                    unit_idx += 1
                else:
                    page_repro["glyph_to_phrase"].append({
                        "glyph": g, "phrase": "[MISSING]", "is_separator": False
                    })
                    reconstructed_parts.append("[?]")

        page_repro["reconstructed_text"] = "".join(reconstructed_parts)

        # Berechne Match-Score
        recon_words = set(re.findall(r'\b[A-Z]+\b', page_repro["reconstructed_text"]))
        wikia_words = set(re.findall(r'\b[A-Z]+\b', wikia[page_id]))
        if recon_words:
            score = len(recon_words & wikia_words) / len(recon_words)
            page_repro["match_score"] = score
            page_repro["n_matched"] = len(recon_words & wikia_words)
            page_repro["n_decoded_unique"] = len(recon_words)
            total_score += score
            n_pages += 1

        reproduction["pages"].append(page_repro)

    # Speichere
    out_path = OUT_DIR / "phrase_reproduction.json"
    with open(out_path, "w") as f:
        json.dump(reproduction, f, indent=2, ensure_ascii=False)

    # Statistik
    print(f"\n✓ Gespeichert: {out_path}")
    print(f"\n{'='*80}")
    print("PHRASEN-REPRODUKTION — ÜBERSICHT")
    print("=" * 80)
    for p in reproduction["pages"]:
        score = p.get("match_score", 0)
        print(f"  {p['page_id']}: {p['n_concepts']} concepts / {p['n_glyphs']} glyphs / "
              f"{p['n_matched']}/{p['n_decoded_unique']} matched (score={score:.2%})")

    avg_score = total_score / n_pages if n_pages else 0
    print(f"\n  DURCHSCHNITT: {avg_score:.2%} Match")

    # Beispiel: p10 komplett
    print(f"\n{'='*80}")
    print("P10 REPRODUKTION (komplett, 1/137 + AMRAM, LEVI, ISHMAEL)")
    print("=" * 80)
    p10 = [p for p in reproduction["pages"] if p["page_id"] == "p10"][0]

    print(f"\n  REKONSTRUIERTER TEXT (Phrase-für-Phrase):")
    print(f"  {p10['reconstructed_text'][:1500]}")
    print(f"\n  WIKIA-ORIGINAL:")
    print(f"  {p10['wikia_plaintext'][:1500]}")

    # Glyph-für-Glyph Mapping p10
    print(f"\n  GLYPH→PHRASE MAPPING (erste 30):")
    for i, m in enumerate(p10["glyph_to_phrase"][:30]):
        if not m["is_separator"]:
            print(f"    [{i:>2}] {m['glyph']:>4} → {m['phrase'][:80]}")
        else:
            print(f"    [{i:>2}] {m['glyph']:>4} → [SEP]")


if __name__ == "__main__":
    main()
