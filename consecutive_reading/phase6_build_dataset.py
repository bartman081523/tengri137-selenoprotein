"""
phase6_build_dataset.py
V8 Phase 6 — Trainings-Datensatz-Builder

Erstelle Trainings-Paare (V6-Token-Sequenz, Wikia-Plaintext) für p1-p10.
Diese Paare können für zukünftiges Sequence-Alignment / Seq2Seq-Modeling
verwendet werden, auch wenn 1:1-Linear-Mapping empirisch nicht funktioniert.

Input:
- bbox/tokenstream_20260706_V6_v3_17glyphs/p{NN}.json (V6 Tokens)
- bbox/wikia_plaintexts_20260706_V8/wikia_p1_to_p23.json (Wikia Plaintexte)

Output:
- bbox/model_v8_20260706_V8/training_pairs.json
- bbox/model_v8_20260706_V8/n_training_pages.json
- bbox/model_v8_20260706_V8/phase6_summary.json
"""
import json
import re
import os
from pathlib import Path
from datetime import datetime

V6_TOKEN_DIR = Path("bbox/tokenstream_20260706_V6_v3_17glyphs")
WIKIA_JSON = Path("bbox/wikia_plaintexts_20260706_V8/wikia_p1_to_p23.json")
OUT_DIR = Path("bbox/model_v8_20260706_V8")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("=" * 80)
    print("V8 PHASE 6: TRAININGS-DATENSATZ-BUILDER")
    print("=" * 80)

    with open(WIKIA_JSON) as f:
        wikia = json.load(f)['page_blocks']

    training_pairs = []
    pair_stats = []

    print("\n[1/2] Erstelle Trainings-Paare (p1-p10)...")
    for pgnum in range(1, 11):
        page_id = f"p{pgnum:02d}"
        v6_path = V6_TOKEN_DIR / f"{page_id}.json"
        if not v6_path.exists():
            continue
        with open(v6_path) as f:
            v6_tokens = json.load(f).get('tokens', [])

        # Sort by reading order
        v6_tokens = sorted(v6_tokens, key=lambda t: (t.get('y', 0), t.get('x', 0)))
        token_seq = [t.get('glyph_id', '?') for t in v6_tokens]

        # Wikia-Text
        if page_id == "p05_p06" or page_id == "p05" or page_id == "p06":
            continue
        text = wikia.get(page_id, '')

        pair = {
            "page_id": page_id,
            "n_glyphs": len(token_seq),
            "glyph_sequence": token_seq,
            "glyph_positions": [
                {"glyph_id": t.get('glyph_id'),
                 "x": t.get('x'), "y": t.get('y'),
                 "w": t.get('w'), "h": t.get('h')}
                for t in v6_tokens
            ],
            "wikia_text": text,
            "wikia_text_no_whitespace": re.sub(r'\s+', '', text),
            "n_latin_chars": sum(1 for c in text if c.isascii() and c.isalpha()),
            "ratio_glyphs_to_latin": len(token_seq) / max(1, sum(1 for c in text if c.isascii() and c.isalpha())),
        }
        training_pairs.append(pair)
        pair_stats.append({
            "page_id": page_id,
            "n_glyphs": len(token_seq),
            "n_latin": sum(1 for c in text if c.isascii() and c.isalpha()),
            "ratio": pair['ratio_glyphs_to_latin'],
        })
        print(f"  {page_id}: {len(token_seq):3} Glyphen ↔ {pair['n_latin_chars']:4} lateinische Zeichen "
              f"(ratio={pair['ratio_glyphs_to_latin']:.3f})")

    with open(OUT_DIR / "training_pairs.json", 'w') as f:
        json.dump(training_pairs, f, indent=2, ensure_ascii=False)
    with open(OUT_DIR / "n_training_pages.json", 'w') as f:
        json.dump(pair_stats, f, indent=2, ensure_ascii=False)

    # Summary
    summary = {
        "metadata": {
            "phase": "V8 / Phase 6",
            "datum": datetime.now().isoformat(),
            "n_training_pairs": len(training_pairs),
        },
        "pair_stats": pair_stats,
        "interpretation": (
            "Trainings-Paare (Glyph-Sequenz, Wikia-Text) sind für zukünftiges "
            "Sequence-Alignment bereitgestellt. Da 1:1-Linear-Mapping empirisch "
            "FALSIFIZIERT ist (Phase 2-4), ist unklar, ob klassische Seq2Seq-Modelle "
            "funktionieren. Empfohlen: Sequence-Alignment mit DTW, dann manuelle "
            "Mapping-Inspektion."
        ),
    }
    with open(OUT_DIR / "phase6_summary.json", 'w') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 80}")
    print(f"PHASE 6 ABGESCHLOSSEN")
    print(f"{'=' * 80}")
    print(f"  Trainings-Paare: {len(training_pairs)}")
    print(f"  Output: bbox/model_v8_20260706_V8/")


if __name__ == "__main__":
    main()
