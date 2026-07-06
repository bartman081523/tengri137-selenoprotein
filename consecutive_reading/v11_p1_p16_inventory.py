"""
v11_p1_p16_inventory.py
V11 PHASE 1 — Glyph-Wort-Inventur für p1-p16

Methode: Pro Glyph-Position aggregiere Wörter über ALLE Seiten.
Dann: Optimale Phrase-Segmentierung (Wikia-Wörter besser zu Glyphen zuordnen).

Output: bbox/v11_p1_p16_20260706/glyph_word_inventory.json
"""
import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

OUT_DIR = Path("bbox/v11_p1_p16_20260706")
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


def main():
    print("=" * 80)
    print("V11 PHASE 1: GLYPH-WORT-INVENTUR")
    print("=" * 80)

    tokens = load_v6_tokens()
    wikia = load_wikia()

    # Sammle pro Glyph: Welche Wikia-Wörter kommen an welcher Position vor?
    inventory = {
        "metadata": {
            "phase": "V11 / Phase 1",
            "datum": datetime.now().isoformat(),
            "method": "Position-aware Glyph → Word mapping über alle p1-p16",
        },
        "per_glyph_words": {},
        "per_glyph_positions": {},
    }

    for page_id in sorted(tokens.keys()):
        if page_id not in wikia:
            continue
        seq = [t.get("glyph_id", "?") for t in tokens[page_id]]
        n_g25 = sum(1 for g in seq if g == "G25")
        n_concepts = len(seq) - n_g25

        # Wikia-Wörter extrahieren
        wikia_words = re.findall(r'\b[A-Z]+\b', wikia[page_id].upper())

        # Mappe Glyph-Position → Wikia-Wort
        if n_concepts == 0 or not wikia_words:
            continue

        # BESSERE Segmentierung: Gleitende Wort-Allokation
        # Jeder Glyph bekommt 1.6 Wörter im Durchschnitt
        # Total Glyphen = n_concepts
        # Total Wörter = len(wikia_words)
        # words_per_glyph = len(wikia_words) / n_concepts

        words_per_glyph = len(wikia_words) / n_concepts
        print(f"  {page_id}: {n_concepts} Glyphen, {len(wikia_words)} Wörter = {words_per_glyph:.2f} Wörter/Glyph")

        # Pro Glyph: Welche Wörter?
        concept_idx = 0
        for i, g in enumerate(seq):
            if g == "G25":
                continue

            # Position-basiertes Wort-Mapping
            start_word = int(concept_idx * words_per_glyph)
            end_word = int((concept_idx + 1) * words_per_glyph)
            if end_word > len(wikia_words):
                end_word = len(wikia_words)
            if start_word >= len(wikia_words):
                start_word = len(wikia_words) - 1

            phrase_words = wikia_words[start_word:end_word]
            if not phrase_words:
                concept_idx += 1
                continue

            # Inventur pro Glyph
            if g not in inventory["per_glyph_words"]:
                inventory["per_glyph_words"][g] = Counter()
                inventory["per_glyph_positions"][g] = defaultdict(list)

            for w in phrase_words:
                inventory["per_glyph_words"][g][w] += 1
                inventory["per_glyph_positions"][g][concept_idx].append((page_id, w))

            concept_idx += 1

    # Output: Top-Wörter pro Glyph
    print()
    print("=" * 80)
    print("TOP-WÖRTER PRO GLYPH (über alle p1-p16)")
    print("=" * 80)
    for g in sorted(inventory["per_glyph_words"].keys(),
                    key=lambda x: -sum(inventory["per_glyph_words"][x].values())):
        counter = inventory["per_glyph_words"][g]
        top = counter.most_common(15)
        total = sum(counter.values())
        n_unique = len(counter)
        print(f"\n  {g} ({total} total, {n_unique} unique):")
        for word, cnt in top:
            print(f"    {word}: {cnt}")

    # Speichere
    out_data = {
        "metadata": inventory["metadata"],
        "per_glyph_words": {
            g: dict(counter.most_common(50))
            for g, counter in inventory["per_glyph_words"].items()
        },
        "per_glyph_unique_count": {
            g: len(counter)
            for g, counter in inventory["per_glyph_words"].items()
        },
        "per_glyph_total": {
            g: sum(counter.values())
            for g, counter in inventory["per_glyph_words"].items()
        },
    }

    out_path = OUT_DIR / "glyph_word_inventory.json"
    with open(out_path, "w") as f:
        json.dump(out_data, f, indent=2, ensure_ascii=False)

    print()
    print(f"✓ Inventur: {out_path}")
    print(f"   {len(inventory['per_glyph_words'])} Glyphen inventarisiert")


if __name__ == "__main__":
    main()
