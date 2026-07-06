"""
v9_phase2_reconstruct.py
V9 Phase 2 — Vollständige Reproduktion der 23 Seiten

Da 1:1 Glyph→Latin unmöglich ist (V8 Beweis), verwenden wir die
Drei-Schichten-Architektur:
1. Tengri-Glyphen (V6 ML) — semantische Codes
2. Lateinischer Text (Wikia Plaintext) — Schmehs Übersetzung
3. Formeln/Berechnungen (Magic Cubes, Brüche) — entschlüsselt

Output: Parallele Dokumentation pro Seite mit:
- V6-Glyph-Sequenz
- Wikia-Plaintext (Schmehs Übersetzung)
- Annotierte Erklärungen
- Magic-Cube/Bruch-Decodes (wo zutreffend)
"""
import json
from pathlib import Path
from datetime import datetime
from collections import Counter

V8_WIKIA = Path("bbox/wikia_plaintexts_20260706_V8/wikia_p1_to_p23.json")
V9_KNOWLEDGE = Path("/run/media/julian/ML4/tengri137/original_sources/wikia/wikia_complete_knowledge.json")
V6_TOKENS = Path("bbox/tokenstream_20260706_V6_v3_17glyphs")
V8_GLYPH_MAP = Path("bbox/glyph_refs_20260706_V6_consolidated/glyphs_final.json")
V7_BURUMUT = Path("bbox/burumut_20260707_V7/burumut_texts.json")
V7_FRACTIONS = Path("bbox/burumut_20260707_V7/burumut_candidates.json")
OUT_DIR = Path("bbox/v9_reproduction_20260706")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("=" * 80)
    print("V9 PHASE 2: VOLLSTÄNDIGE REPRODUKTION — 23 SEITEN")
    print("=" * 80)

    # Load all sources
    wikia_v8 = json.load(open(V8_WIKIA))["page_blocks"]
    knowledge = json.load(open(V9_KNOWLEDGE))
    glyph_catalog = json.load(open(V8_GLYPH_MAP))
    burumut_texts = json.load(open(V7_BURUMUT))

    # Build page_id map
    page_id_map = {
        "p01": "001", "p02": "002", "p03": "003", "p04": "004",
        "p05_p06": "005-006", "p07": "007", "p08": "008", "p09": "009", "p10": "010",
        "p11": "011", "p12": "012", "p13": "013", "p14": "014", "p15": "015",
        "p16": "016", "p17_fractions": "017", "p17_to_p22_english": "017-022",
        "p18": "018", "p19": "019", "p20": "020", "p21": "021", "p22": "022", "p23": "023",
    }

    # Reconstruct each page
    reconstruction = {
        "metadata": {
            "phase": "V9 / Phase 2",
            "datum": datetime.now().isoformat(),
            "method": "Drei-Schichten-Architektur: V6-Glyphen + Wikia-Plaintext + Formel-Decodes",
            "n_pages": len(wikia_v8),
        },
        "pages": [],
    }

    for page_id, plaintext in wikia_v8.items():
        page_data = {
            "page_id": page_id,
            "n_chars": len(plaintext),
            "n_words": len(plaintext.split()),
            "wikia_plaintext": plaintext,
            "glyph_sequence": [],
            "n_glyphs": 0,
            "glyph_frequency": {},
            "annotations": [],
            "formulas": [],
            "burumut_words": [],
            "magic_cube_refs": [],
        }

        # Load V6 tokens
        if page_id == "p05_p06":
            token_paths = [V6_TOKENS / "p05.json", V6_TOKENS / "p06.json"]
        elif page_id in ("p17_fractions", "p17_to_p22_english"):
            token_paths = [V6_TOKENS / "p17.json"]
        else:
            token_paths = [V6_TOKENS / f"{page_id}.json"]

        all_tokens = []
        for tp in token_paths:
            if tp.exists():
                tdata = json.load(open(tp))
                all_tokens.extend(tdata.get("tokens", []))

        if all_tokens:
            all_tokens = sorted(all_tokens, key=lambda t: (t.get('y', 0), t.get('x', 0)))
            page_data["glyph_sequence"] = [t.get('glyph_id', '?') for t in all_tokens]
            page_data["n_glyphs"] = len(all_tokens)
            page_data["glyph_frequency"] = dict(Counter(page_data["glyph_sequence"]))

        # Add annotations from V9 knowledge
        wk_key = page_id_map.get(page_id)
        if wk_key and wk_key in knowledge:
            wk_page = knowledge[wk_key]
            page_data["annotations"] = wk_page.get("annotations", [])

        # Extract formulas (magic cube refs, fractions)
        for ann in page_data["annotations"]:
            header = ann.get("header", "")
            text = ann.get("text", "")
            if "magic cube" in text.lower() or "cube" in text.lower():
                # Extract bible refs like "JOB 15:2"
                import re
                refs = re.findall(r'\b(JOB|JOHN|EXODUS|GEN|REVELATION|2 CHRONICLES|1 KINGS|EZRA)\s*(\d+):(\d+)\b', text)
                for ref in refs:
                    page_data["magic_cube_refs"].append({"book": ref[0], "chapter": int(ref[1]), "verse": int(ref[2]), "context": text[:200]})

        # Add BURUMUT words for p17-p22
        if page_id in ("p17_to_p22_english",):
            for fraction_id, words in burumut_texts.get("burumut_texts", {}).items():
                page_data["burumut_words"].append({
                    "fraction": int(fraction_id),
                    "words": words,
                })

        reconstruction["pages"].append(page_data)

    # Save
    out_path = OUT_DIR / "full_reconstruction.json"
    with open(out_path, "w") as f:
        json.dump(reconstruction, f, indent=2, ensure_ascii=False)

    # Summary
    print(f"\n✓ Gespeichert: {out_path}")
    print(f"\n{'='*80}")
    print("REPRODUKTION — ÜBERSICHT")
    print("=" * 80)
    print(f"  Total pages: {len(reconstruction['pages'])}")
    for p in reconstruction["pages"]:
        n_g = p["n_glyphs"]
        n_a = len(p["annotations"])
        n_b = len(p["burumut_words"])
        n_mc = len(p["magic_cube_refs"])
        wikia_len = p["n_chars"]
        print(f"  {p['page_id']:<20} {n_g:>4} glyphs | {wikia_len:>5}c plaintext | {n_a:>2} ann | {n_mc:>2} cube | {n_b:>2} burumut")

    # Print p10 fully as example
    print(f"\n{'='*80}")
    print("BEISPIEL p10 — Tengri + Latein + 1/137 Berechnung")
    print("=" * 80)
    p10 = [p for p in reconstruction["pages"] if p["page_id"] == "p10"][0]
    print(f"\nWIKIA PLAINTEXT (Schmeh-Übersetzung):")
    print(p10["wikia_plaintext"][:1000])
    print(f"\n\nV6 GLYPHS ({p10['n_glyphs']} tokens, top 10):")
    for gid, cnt in sorted(p10["glyph_frequency"].items(), key=lambda x: -x[1])[:10]:
        print(f"  {gid}: {cnt}x")
    print(f"\nANNOTATIONEN ({len(p10['annotations'])}):")
    for ann in p10["annotations"]:
        print(f"  [{ann['header']}]: {ann['text'][:300]}")


if __name__ == "__main__":
    main()
