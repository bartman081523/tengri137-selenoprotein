#!/usr/bin/env python3
"""
phase1g_consolidate_glyphs.py — V6 Phase 1g: 30→17 Glyphen-Mapping erstellen.

Basierend auf dem pixel_similarity_report.json:
- Map alle Glyphen-IDs auf ihren kanonischen Vertreter
- Erstelle eine neue, saubere Referenz-Sammlung von 17 unique Glyphen
- Speichere das Mapping für nachfolgende Phasen

Output: bbox/glyph_refs_20260706_V6_consolidated/
        {
          "metadata": {...},
          "mapping": {"G13": "G03", "G16": "G03", ...},
          "canonical": ["G01", "G02", "G03", "G04", "G05", "G06", "G07", "G08", "G09", "G10", "G11", "G14", "G17", "G18", "G19", "G25", "G29"],
          "n_unique": 17
        }
"""
import argparse
import json
import shutil
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sim-report", type=Path, required=True,
                    help="models/symbols_20260706_V6/pixel_similarity_report.json")
    ap.add_argument("--refs", type=Path, required=True,
                    help="bbox/glyph_refs_20260706_V6/refs/")
    ap.add_argument("--glyphs-final", type=Path, required=True,
                    help="bbox/glyph_refs_20260706_V6/glyphs_final.json")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/glyph_refs_20260706_V6_consolidated/")
    args = ap.parse_args()

    sim = json.loads(args.sim_report.read_text())
    final = json.loads(args.glyphs_final.read_text())
    all_glyphs = {g["glyph_id"] for g in final["glyphs"]}

    # 1. Mapping erstellen
    mapping = {}  # duplicate_id -> canonical_id
    canonical = set()
    # Pro Gruppe: ersten Member als kanonisch wählen
    for group in sim["duplicate_groups"]:
        members = sorted(group["members"])  # Sortiert, damit Auswahl deterministisch
        root = members[0]  # Niedrigste GID als kanonischer Vertreter
        canonical.add(root)
        for member in members[1:]:
            mapping[member] = root
    # Singleton-Gruppen sind selber kanonisch
    in_groups = set()
    for g in sim["duplicate_groups"]:
        in_groups.update(g["members"])
    for g in all_glyphs:
        if g not in in_groups:
            canonical.add(g)

    canonical = sorted(canonical)
    n_unique = len(canonical)
    print(f"Kanonische Glyphen ({n_unique}): {canonical}")
    print(f"Mapping (duplicate -> canonical):")
    for k, v in sorted(mapping.items()):
        print(f"  {k} -> {v}")

    # 2. Neue Referenz-Sammlung erstellen
    args.out.mkdir(parents=True, exist_ok=True)
    refs_out = args.out / "refs"
    refs_out.mkdir(exist_ok=True)

    # Kopiere die kanonischen Crops
    for gid in canonical:
        src = args.refs / f"{gid}.png"
        if src.exists():
            shutil.copy(src, refs_out / f"{gid}.png")
        else:
            print(f"  WARNUNG: {src} fehlt!")

    # 3. Konsolidierte glyphs_final.json
    # Hole die Original-Glyph-Daten — auch für kanonische Vertreter,
    # die NICHT in final["glyphs"] sind (z.B. G04 fehlt im Original,
    # aber G24 ist kanonisch via Mapping G04->G24)
    final_by_id = {g["glyph_id"]: g for g in final["glyphs"]}
    # Für G04 (nicht in Original) und G24 (kanonisch): G24 nehmen
    consolidated_glyphs = []
    for gid in canonical:
        if gid in final_by_id:
            new_g = dict(final_by_id[gid])
            new_g["canonical_id"] = gid
            new_g["template_path"] = f"refs/{gid}.png"
            consolidated_glyphs.append(new_g)
        else:
            # Suche ein Mitglied aus der gleichen Gruppe, das im Original ist
            for group in sim["duplicate_groups"]:
                if gid in group["members"]:
                    for m in group["members"]:
                        if m in final_by_id:
                            new_g = dict(final_by_id[m])
                            new_g["canonical_id"] = gid
                            new_g["template_path"] = f"refs/{gid}.png"
                            new_g["_note"] = f"Original-ID war {m}, mapped zu kanonischem {gid}"
                            consolidated_glyphs.append(new_g)
                            break
                    break

    out_data = {
        "metadata": {
            "n_original": len(final["glyphs"]),
            "n_unique": n_unique,
            "n_duplicates_removed": len(final["glyphs"]) - n_unique,
            "method": "Pixel-Cosine + SSIM Duplikat-Detection aus Phase 1f",
            "source": str(args.sim_report),
        },
        "mapping": mapping,  # "G13" -> "G03" (Duplikat -> Kanonisch)
        "canonical": canonical,  # 17 unique IDs
        "glyphs": consolidated_glyphs,
    }
    (args.out / "glyphs_final.json").write_text(
        json.dumps(out_data, indent=2, ensure_ascii=False)
    )

    # 4. Mapping-JSON (für Token-Stream-Remap)
    mapping_full = dict(mapping)
    for g in all_glyphs:
        if g not in mapping_full:
            mapping_full[g] = g
    (args.out / "id_mapping.json").write_text(
        json.dumps(mapping_full, indent=2, ensure_ascii=False)
    )

    print(f"\nWrote {args.out}/")
    print(f"  refs/ ({n_unique} unique PNGs)")
    print(f"  glyphs_final.json (konsolidiert)")
    print(f"  id_mapping.json (30 IDs -> 17 unique)")


if __name__ == "__main__":
    main()
