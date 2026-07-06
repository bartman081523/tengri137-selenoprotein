"""
v9_phase0_compile_wikia.py
V9 Phase 0 — Kompiliere vollständige Wikia-Wissensbasis

Konsolidiert die verbesserte Wikia-Extraktion:
- 23 Seiten-Plaintexte
- 13 Annotationen (Important information, Warning, etc.)
- 16 p17-Paare, 16 p18-Paare, ..., 16 p23-Paare (Faktorzerlegungen)

Input: /run/media/julian/ML4/tengri137/original_sources/wikia/wikia_complete_knowledge.json
Output: bbox/v9_reproduction_20260706/wikia_v9_knowledge.json
"""
import json
from pathlib import Path
from datetime import datetime

INPUT = Path("/run/media/julian/ML4/tengri137/original_sources/wikia/wikia_complete_knowledge.json")
OUT_DIR = Path("bbox/v9_reproduction_20260706")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("=" * 80)
    print("V9 PHASE 0: WIKIA-WISSEN KOMPILIEREN")
    print("=" * 80)

    knowledge = json.load(open(INPUT))

    # Reorganize into a clean structure
    v9 = {
        "metadata": {
            "phase": "V9 / Phase 0",
            "datum": datetime.now().isoformat(),
            "source": "Wikia 'Tengri 137 Translation' (Wayback 2017)",
            "n_pages": len(knowledge),
        },
        "pages": [],
        "fractions": {},  # p17-p23 fractions extracted
    }

    # Map page keys to standard format
    page_key_map = {
        "001": "p01", "002": "p02", "003": "p03", "004": "p04",
        "005": "p05", "007": "p07", "008": "p08", "009": "p09", "010": "p10",
        "011": "p11", "012": "p12", "013": "p13", "014": "p14", "015": "p15",
        "016": "p16", "017": "p17", "018": "p18", "019": "p19",
        "020": "p20", "021": "p21", "022": "p22", "023": "p23",
    }

    # Process each page
    for k, p in knowledge.items():
        page_id = page_key_map.get(k, k)
        v9["pages"].append({
            "page": page_id,
            "headers": p.get("headers", []),
            "plaintext": p.get("plaintext", ""),
            "annotations": p.get("annotations", []),
            "n_chars": len(p.get("plaintext", "")),
            "n_annotations": len(p.get("annotations", []))
        })

        # Extract fractions for p17-p23
        if k in ("017", "018", "019", "020", "021", "022", "023"):
            fractions = extract_fractions(p.get("plaintext", ""))
            v9["fractions"][page_id] = fractions

    # Save
    out_path = OUT_DIR / "wikia_v9_knowledge.json"
    with open(out_path, "w") as f:
        json.dump(v9, f, indent=2, ensure_ascii=False)

    # Summary
    print(f"\n✓ Gespeichert: {out_path}")
    print(f"\n{'='*80}")
    print("PHASE 0 SUMMARY")
    print("=" * 80)
    print(f"  Pages: {len(v9['pages'])}")
    print(f"  Fractions (p17-p23):")
    for pg, fr in v9["fractions"].items():
        print(f"    {pg}: {len(fr)} pairs")

    return v9


def extract_fractions(text):
    """Extract factor pairs from p17-p23 plaintext.
    Each block (between -------) may contain 1 or 2 fractions (num/den pairs).
    """
    import re
    blocks = re.split(r'-{20,}', text)
    pairs = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        # Each block has 1 or 2 fractions separated by 2+ newlines OR just blank lines
        # Try splitting on double-newline or single newlines
        # In our raw text, blocks have 1-2 lines per fraction
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        # If 2 lines: 1 fraction
        # If 3 lines: 2 fractions
        # If 4 lines: 2 fractions
        if len(lines) == 2:
            pairs.append({"num": lines[0], "den": lines[1]})
        elif len(lines) == 3:
            # Could be 1 fraction (num spans 2 lines) or 2 fractions
            # Try: lines[0]+lines[1] / lines[2] vs lines[0] / lines[1], lines[2] / ?
            # Pattern: short num, long num, short den, long den usually
            # But "307 * 1481 * ..." looks like a NEW numerator, so 2 fractions
            # Distinguish: if lines[1] and lines[2] are similar in pattern, it's 2 fractions
            pairs.append({"num": lines[0], "den": lines[1]})
            pairs.append({"num": lines[2], "den": None})  # Single value (no den)
        elif len(lines) == 4:
            pairs.append({"num": lines[0], "den": lines[1]})
            pairs.append({"num": lines[2], "den": lines[3]})
        elif len(lines) == 1:
            pairs.append({"num": lines[0], "den": None})
        else:
            # Try to group as (num, den) pairs
            for i in range(0, len(lines) - 1, 2):
                pairs.append({"num": lines[i], "den": lines[i+1]})
            if len(lines) % 2 == 1:
                pairs.append({"num": lines[-1], "den": None})
    return pairs


if __name__ == "__main__":
    main()
