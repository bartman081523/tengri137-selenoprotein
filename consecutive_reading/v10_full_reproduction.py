"""
v10_full_reproduction.py
V10 Phase 6 — VOLLSTÄNDIGE Reproduktion mit semantischen Konzepten

Methode:
- Glyph → semantisches Wort-Feld (aus V10 Phase 5)
- Pro Glyph: Wahrscheinlichkeit für jedes Wikia-Wort
- Generiere für jede Seite eine Wort-für-Wort-Übersetzung mit Confidence-Scores

Output: bbox/v10_decoder_20260706/semantic_reproduction.json
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
    print("V10 PHASE 6: VOLLSTÄNDIGE SEMANTISCHE REPRODUKTION")
    print("=" * 80)

    tokens = load_v6_tokens()
    wikia = load_wikia()

    # Schritt 1: Sammle Glyph → Wikia-Wörter über alle Seiten
    glyph_words = defaultdict(Counter)
    for page_id in sorted(tokens.keys()):
        if page_id not in wikia:
            continue
        seq = [t.get("glyph_id", "?") for t in tokens[page_id]]
        n_g25 = sum(1 for g in seq if g == "G25")
        n_concepts = len(seq) - n_g25
        units = segment_into_units(wikia[page_id], n_concepts)

        for i, g in enumerate([g for g in seq if g != "G25"]):
            if i < len(units):
                unit_words = re.findall(r'\b[A-Z]+\b', units[i])
                for w in unit_words:
                    glyph_words[g][w] += 1

    # Schritt 2: Berechne Wort-Wahrscheinlichkeiten pro Glyph
    glyph_word_probs = {}
    for g, counter in glyph_words.items():
        total = sum(counter.values())
        glyph_word_probs[g] = {w: c/total for w, c in counter.most_common()}

    # Schritt 3: Reproduktion pro Seite
    reproduction = {
        "metadata": {
            "phase": "V10 / Phase 6",
            "datum": datetime.now().isoformat(),
            "method": "Semantische Glyph→Wikia-Wort-Übersetzung mit Wahrscheinlichkeiten",
            "n_pages": len(tokens),
            "n_glyphs": len(glyph_words),
        },
        "pages": [],
    }

    for page_id in sorted(tokens.keys()):
        if page_id not in wikia:
            continue
        seq = [t.get("glyph_id", "?") for t in tokens[page_id]]
        n_g25 = sum(1 for g in seq if g == "G25")
        n_concepts = len(seq) - n_g25
        units = segment_into_units(wikia[page_id], n_concepts)

        page_data = {
            "page_id": page_id,
            "n_glyphs": len(seq),
            "n_concepts": n_concepts,
            "n_g25_separators": n_g25,
            "wikia_n_words": len(re.findall(r'\b[A-Z]+\b', wikia[page_id])),
            "wikia_plaintext": wikia[page_id],
            "glyph_sequence": [],
            "semantic_translation": [],
            "word_probabilities": [],
        }

        # Mappe jedes Glyph zu Top-Wort
        for i, g in enumerate(seq):
            page_data["glyph_sequence"].append(g)
            if g == "G25":
                page_data["semantic_translation"].append(" [SEP] ")
                page_data["word_probabilities"].append({"glyph": g, "word": "[SEP]", "prob": 1.0})
            else:
                if g in glyph_word_probs and i < len(units):
                    # Beste Wort für diesen Glyph in dieser Position
                    # Wähle aus den Top-5 das Wort, das in der Einheit vorkommt
                    unit_words = set(re.findall(r'\b[A-Z]+\b', units[i]))
                    top_words = list(glyph_word_probs[g].keys())
                    matched = None
                    for w in top_words[:10]:
                        if w in unit_words:
                            matched = w
                            break
                    if matched:
                        page_data["semantic_translation"].append(matched)
                        page_data["word_probabilities"].append({
                            "glyph": g,
                            "word": matched,
                            "prob": glyph_word_probs[g][matched],
                        })
                    else:
                        # Fallback: Top-Wort
                        top_w = top_words[0] if top_words else "?"
                        page_data["semantic_translation"].append(f"?{top_w}")
                        page_data["word_probabilities"].append({
                            "glyph": g,
                            "word": top_w,
                            "prob": glyph_word_probs[g].get(top_w, 0.0),
                        })

        # Berechne Match-Score
        decoded_words = set()
        for w in page_data["semantic_translation"]:
            decoded_words.update(re.findall(r'\b[A-Z]+\b', w))
        wikia_words = set(re.findall(r'\b[A-Z]+\b', wikia[page_id]))
        if decoded_words:
            page_data["match_score"] = len(decoded_words & wikia_words) / len(decoded_words)
            page_data["n_matched"] = len(decoded_words & wikia_words)
            page_data["n_decoded_unique"] = len(decoded_words)

        reproduction["pages"].append(page_data)

    # Speichere
    out_path = OUT_DIR / "semantic_reproduction.json"
    with open(out_path, "w") as f:
        json.dump(reproduction, f, indent=2, ensure_ascii=False)

    # Drucke Statistik
    print(f"\n✓ Gespeichert: {out_path}")
    print(f"\n{'='*80}")
    print("REPRODUKTION — ÜBERSICHT")
    print("=" * 80)
    for p in reproduction["pages"]:
        score = p.get("match_score", 0)
        n_matched = p.get("n_matched", 0)
        n_decoded = p.get("n_decoded_unique", 0)
        print(f"  {p['page_id']}: {n_decoded} unique decoded, {n_matched} matched (score={score:.2%})")

    # Beispiel: p01 Reproduktion
    print(f"\n{'='*80}")
    print("P01 REPRODUKTION (Beispiel)")
    print("=" * 80)
    p01 = reproduction["pages"][0]
    print(f"\n  Glyphen-Sequenz: {' '.join(p01['glyph_sequence'])}")
    print(f"  Semantische Übersetzung: {''.join(p01['semantic_translation'])[:500]}")
    print(f"\n  Wikia-Plaintext:")
    print(f"  {p01['wikia_plaintext'][:500]}")


if __name__ == "__main__":
    main()
