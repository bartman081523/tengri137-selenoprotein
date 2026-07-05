#!/usr/bin/env python3
"""
build_gemini_questions2_repo.py — Erstelle Gemini-Fragen2-repo.txt (kompakt)

Nur V5-JSONs. Phase 0 wird aggregiert pro Page (kein voller Component-Output).
"""
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")
OUT = ROOT / "Gemini-Fragen2-repo.txt"

BEGIN = "=" * 80
END = "=" * 80


def emit(f, label, path, content):
    f.write(f"\n{BEGIN}\n")
    f.write(f"# FILE: {label}\n")
    f.write(f"# PATH: {path}\n")
    f.write(f"# BEGIN CONTENT\n")
    f.write(content)
    if not content.endswith("\n"):
        f.write("\n")
    f.write(f"# END CONTENT\n")
    f.write(f"{END}\n\n")


def read_text(path: Path) -> str:
    if not path.exists():
        return f"[FILE NOT FOUND: {path}]"
    return path.read_text(encoding="utf-8")


def aggregate_substrat(path: Path) -> str:
    """Substrat aggregieren: nur Statistik, nicht alle Components."""
    import json
    d = json.loads(path.read_text())
    # Components zusammenfassen: bbox nur als bounding-union + counts
    if d.get("components"):
        xs = [c["bbox"][0] for c in d["components"]]
        ys = [c["bbox"][1] for c in d["components"]]
        rights = [c["bbox"][0] + c["bbox"][2] for c in d["components"]]
        bottoms = [c["bbox"][1] + c["bbox"][3] for c in d["components"]]
        size_px_total = sum(c["size_px"] for c in d["components"])
        bbox_union = [min(xs), min(ys), max(rights) - min(xs), max(bottoms) - min(ys)]
        # size_px-Verteilung pro Level
        levels = {}
        for c in d["components"]:
            lvl = c.get("level", "unknown")
            levels.setdefault(lvl, {"count": 0, "size_px_total": 0})
            levels[lvl]["count"] += 1
            levels[lvl]["size_px_total"] += c["size_px"]
    else:
        bbox_union = [0, 0, 0, 0]
        size_px_total = 0
        levels = {}

    compact = {
        "page_id": d.get("page_id"),
        "image_size": d.get("image_size"),
        "ink_threshold": d.get("ink_threshold"),
        "n_components": d.get("n_components"),
        "n_micro": d.get("n_micro"),
        "n_meso": d.get("n_meso"),
        "n_macro": d.get("n_macro"),
        "size_px_total": size_px_total,
        "bbox_union": bbox_union,
        "levels": levels,
    }
    return json.dumps(compact, indent=2, ensure_ascii=False)


def main():
    out = OUT.open("w", encoding="utf-8")

    out.write("# Gemini-Fragen2-repo.txt\n")
    out.write("# V5-JSON-Outputs (kompakt), mit Pfad-Markern getrennt.\n")
    out.write("# Phase 0 aggregiert pro Page (volle Component-Listen weggelassen — 3.4 MB → ~30 KB).\n")
    out.write("# Kein V4/V3/Schmeh-Hints. PDF übersprungen.\n")
    out.write("# Generiert: 2026-07-05\n\n")

    # 1. V5 doc.json
    out.write("# " + "=" * 76 + "\n")
    out.write("# ABSCHNITT 1: V5 TOP-LEVEL doc.json\n")
    out.write("# " + "=" * 76 + "\n")
    p = ROOT / "Tengri137_detailed_20260705_V5/doc.json"
    emit(out, "V5 top-level document", str(p.relative_to(ROOT)), read_text(p))

    # 2. V5 Phase 0: Substrat (aggregiert)
    out.write("# " + "=" * 76 + "\n")
    out.write("# ABSCHNITT 2: V5 PHASE 0 — Inken-Substrat (aggregiert, 23 p{NN}.json)\n")
    out.write("# " + "=" * 76 + "\n")
    substrat_dir = ROOT / "bbox/substrat_20260705_V5"
    for i in range(1, 24):
        pid = f"p{i:02d}"
        p = substrat_dir / f"{pid}.json"
        emit(out, f"V5 Phase 0 Substrat {pid} (aggregiert)",
             str(p.relative_to(ROOT)), aggregate_substrat(p))

    # 3. V5 Phase 1: Cryptanalysis
    out.write("# " + "=" * 76 + "\n")
    out.write("# ABSCHNITT 3: V5 PHASE 1 — Cryptanalysis Report\n")
    out.write("# " + "=" * 76 + "\n")
    p = ROOT / "bbox/cryptanalysis_20260705_V5/crypto_report.json"
    emit(out, "V5 Phase 1 Cryptanalysis", str(p.relative_to(ROOT)), read_text(p))

    # 4. V5 Phase 2: Alphabet
    out.write("# " + "=" * 76 + "\n")
    out.write("# ABSCHNITT 4: V5 PHASE 2 — Glyph-Alphabet (K=34)\n")
    out.write("# " + "=" * 76 + "\n")
    p = ROOT / "bbox/alphabet_20260705_V5/alphabet.json"
    emit(out, "V5 Phase 2 Alphabet", str(p.relative_to(ROOT)), read_text(p))

    # 5. V5 Phase 3: Layout
    out.write("# " + "=" * 76 + "\n")
    out.write("# ABSCHNITT 5: V5 PHASE 3 — Multi-Layout (23 p{NN}.json)\n")
    out.write("# " + "=" * 76 + "\n")
    layout_dir = ROOT / "bbox/layout_20260705_V5"
    for i in range(1, 24):
        pid = f"p{i:02d}"
        p = layout_dir / f"{pid}.json"
        emit(out, f"V5 Phase 3 Layout {pid}", str(p.relative_to(ROOT)), read_text(p))

    # 6. V5 Phase 4: OCR
    out.write("# " + "=" * 76 + "\n")
    out.write("# ABSCHNITT 6: V5 PHASE 4 — Selektive OCR (23 p{NN}.json)\n")
    out.write("# " + "=" * 76 + "\n")
    ocr_dir = ROOT / "bbox/ocr_20260705_V5"
    for i in range(1, 24):
        pid = f"p{i:02d}"
        p = ocr_dir / f"{pid}.json"
        emit(out, f"V5 Phase 4 OCR {pid}", str(p.relative_to(ROOT)), read_text(p))

    # 7. V5 Phase 5: Decoded
    out.write("# " + "=" * 76 + "\n")
    out.write("# ABSCHNITT 7: V5 PHASE 5 — Decode Report (F1-Falsifikation)\n")
    out.write("# " + "=" * 76 + "\n")
    p = ROOT / "bbox/decoded_20260705_V5/decode_report.json"
    emit(out, "V5 Phase 5 Decode Report", str(p.relative_to(ROOT)), read_text(p))

    # 8. V5 Schema
    out.write("# " + "=" * 76 + "\n")
    out.write("# ABSCHNITT 8: V5 SCHEMA\n")
    out.write("# " + "=" * 76 + "\n")
    p = ROOT / "schemas/tengri137_document_v5.schema.json"
    emit(out, "V5 Schema", str(p.relative_to(ROOT)), read_text(p))

    # 9. Schmeh External Check
    out.write("# " + "=" * 76 + "\n")
    out.write("# ABSCHNITT 9: V5 SCHMEH-EXTERNAL-CHECK\n")
    out.write("# " + "=" * 76 + "\n")
    p = ROOT / "bbox/schmeh_external_check/schmeh_check.json"
    emit(out, "V5 Schmeh External Check", str(p.relative_to(ROOT)), read_text(p))

    out.close()
    size_kb = OUT.stat().st_size / 1024
    print(f"Wrote {OUT} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
