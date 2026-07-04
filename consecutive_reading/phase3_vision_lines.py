#!/usr/bin/env python3
"""
Phase 3 v4 — Zeilenweiser Vision-Quercheck.

Input:  bbox/components_<TS>/p{NN}/p{NN}_lines/line_*.png  (Zeilen-Crops)
        schemas/line_vision.schema.json  (Vision-Schema)
        bbox/schmeh_hints_<TS>/p{NN}_hints.json  (Hinweis-Quelle Schmeh)

Output: bbox/vision_qa_<TS>/p{NN}/p{NN}_line_NN.json  (Vision-Output pro Zeile)
        bbox/vision_qa_<TS>/p{NN}/p{NN}_page.json     (Page-Level-Zusammenfassung)

Algorithmus:
1. Pro Zeile: claude-vision-json mit line_vision.schema.json
2. Vision klassifiziert: pure_glyph_line, pure_latin_line, pure_numeric_line, ...
3. BBox-Match mit Phase-2-Glyphen (IoU > 0.5)
4. Schmeh-Hints als Hinweis-Validierung (NICHT als Wahrheit)
5. 4 Worker parallel für Speed
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")

PROMPT = """Diese Zeile stammt aus einem historischen Manuskript mit unbekannter Schrift.

Identifiziere:
1) Unbekannte geometrische Schriftzeichen (jedes mit eigener bbox in der Zeile)
2) Lateinische Wörter (in Großbuchstaben, mit Position und Text)
3) Zahlen, mathematische Formeln
4) Grafische Elemente (Linien, Bögen, Verzierungen)
5) Zeilen-Typ (line_type)

WICHTIG:
- Die Zeile ist möglicherweise eine Mischung aus unbekannter Schrift und lateinischem Text
- "Unbekannte Schriftzeichen" = nicht-alphanumerische Symbole, Glyphen, Sigille
- Wenn du lateinische Wörter siehst, gib sie EXAKT wieder (Caps-Lock beibehalten)
- BBox-Koordinaten sind RELATIV zur Zeile (0,0 = oben-links der Zeile)

Hinweis (Schmeh 2017 Rekonstruktion, KEINE Wahrheit sondern nur möglicher Inhalt dieser Zeile):
{schmeh_hint}

Gib strukturierte JSON-Antwort."""


def shrink(src: Path, dst: Path, max_side: int = 1024, quality: int = 85):
    """Resize image to max_side using magick."""
    subprocess.run(
        ["magick", str(src), "-resize", f"{max_side}x{max_side}>",
         "-quality", str(quality), str(dst)],
        check=True,
    )


def _strip_json_wrapper(text: str) -> str:
    """Entferne ```json ... ``` Wrapper und ähnliches."""
    t = text.strip()
    # ```json ... ``` oder ``` ... ```
    if t.startswith("```"):
        # Finde erste Zeile nach ```
        nl = t.find("\n")
        if nl > 0:
            t = t[nl + 1:]
        if t.endswith("```"):
            t = t[:-3]
        t = t.strip()
    return t


def _find_json_object(text: str) -> str:
    """Finde das erste vollständige JSON-Objekt in text."""
    # Suche erstes {
    start = text.find("{")
    if start < 0:
        return text
    # Suche passendes }
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        c = text[i]
        if escape:
            escape = False
            continue
        if c == "\\":
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return text[start:]


def run_vision(image_path: Path, schema_path: Path, prompt: str,
               max_retries: int = 4, timeout: int = 240) -> dict:
    """Run claude-vision-json with retry, JSON-wrapper-strip, schema-leak detection."""
    last_error = None
    for attempt in range(max_retries):
        try:
            cmd = [
                "claude-vision-json", str(image_path),
                "--schema", str(schema_path),
                "--prompt", prompt,
            ]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout,
            )
            if result.returncode != 0:
                last_error = f"rc={result.returncode}: {result.stderr[:200]}"
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(last_error)
            # Versuche zuerst direkt, dann mit Wrapper-Strip
            raw = result.stdout
            stripped = _strip_json_wrapper(raw)
            try:
                d = json.loads(stripped)
            except json.JSONDecodeError:
                # Versuche JSON-Objekt aus dem Output zu extrahieren
                extracted = _find_json_object(stripped)
                d = json.loads(extracted)
            # V4: Schema-Leak-Detection
            if isinstance(d, dict) and "$schema" in d and "type" in d and "properties" in d:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise ValueError("vision returned schema definition (after retries)")
            if isinstance(d, dict) and "$ref" in d and "definitions" in d:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise ValueError("vision returned schema $ref")
            return d
        except (subprocess.TimeoutExpired, json.JSONDecodeError, RuntimeError, ValueError) as e:
            last_error = str(e)
            if attempt == max_retries - 1:
                return {"error": last_error, "_failed_after_retries": True,
                        "_raw_excerpt": raw[:500] if 'raw' in dir() else ""}
            time.sleep(2 ** attempt)
    return {"error": f"max retries: {last_error}"}


def process_line(page_id: str, line_id: int, line_data: dict,
                 page_components_dir: Path, schmeh_hints: dict, schema_path: Path,
                 vision_dir: Path) -> dict:
    """Verarbeitet eine einzelne Zeile."""
    crop_path_rel = line_data.get("line_crop_path")
    if not crop_path_rel:
        return {"page": page_id, "line_id": line_id, "error": "no crop path"}
    crop_path = ROOT / crop_path_rel
    if not crop_path.exists():
        return {"page": page_id, "line_id": line_id, "error": f"crop not found: {crop_path}"}

    # Schmeh-Hinweis
    schmeh_hint = "(no schmeh hint available)"
    if schmeh_hints:
        # Suche ähnlichste Zeile in Schmeh-Hinweisen (y-Position relativ)
        # Hier vereinfacht: alle Zeilen zusammen als Hint-Liste
        lines = schmeh_hints.get("lines", [])
        if lines and line_id - 1 < len(lines):
            hint_line = lines[line_id - 1]
            schmeh_hint = f"Line {line_id}: {hint_line['type']} -> {hint_line.get('text', '')[:200]}"
        else:
            schmeh_hint = f"Schmeh has {len(lines)} lines for this page"

    prompt = PROMPT.format(schmeh_hint=schmeh_hint)

    # Shrink + Vision
    with tempfile.TemporaryDirectory() as tmp:
        small = Path(tmp) / f"{page_id}_line{line_id:02d}.jpg"
        try:
            # V4: Kleinere Resize für sehr leere Zeilen (512 statt 1024) —
            # sonst gibt Vision manchmal das Schema statt Antwort zurück
            from PIL import Image
            src_img = Image.open(crop_path)
            w, h = src_img.size
            # Wenn das Bild sehr klein/leer ist, weniger resize
            if max(w, h) < 200:
                shrink(crop_path, small, max_side=512)
            else:
                shrink(crop_path, small, max_side=1024)
        except Exception as e:
            return {"page": page_id, "line_id": line_id, "error": f"shrink failed: {e}"}
        vision_result = run_vision(small, schema_path, prompt)
        if "error" in vision_result:
            return {"page": page_id, "line_id": line_id, "error": vision_result["error"]}

    # BBox-Match mit Phase-2-Glyph-Indexen
    page_glyphs_data = json.loads((page_components_dir / f"{page_id}_glyphs.json").read_text())
    page_glyphs = page_glyphs_data["glyphs"]
    line_glyph_ids = line_data.get("glyph_ids", [])

    # BBox-Match: Vision gibt BBox in Zeilen-Relativ-Koordinaten;
    # wir konvertieren zu globalen Koordinaten und matchen mit Page-Glyph-Liste
    line_bbox_global = line_data["bbox"]  # [x0, y0, w, h] (in Page-Koordinaten)
    line_x0, line_y0 = line_bbox_global[0], line_bbox_global[1]

    # Für jedes Vision-Glyph: finde den nächsten Page-Glyph (IoU)
    matched_glyphs = []
    unmatched_vision = []
    for vg in vision_result.get("glyphs", []):
        v_bbox = vg.get("bbox", [])
        if len(v_bbox) != 4:
            unmatched_vision.append(vg)
            continue
        # Globale Koordinaten
        vg_global = [
            line_x0 + v_bbox[0],
            line_y0 + v_bbox[1],
            v_bbox[2],
            v_bbox[3],
        ]
        # Finde best match (IoU ODER Containment)
        best_iou = 0.0
        best_glyph = None
        for g in page_glyphs:
            if g["glyph_index"] not in line_glyph_ids:
                continue
            gb = g["bbox"]
            # IoU
            x0 = max(vg_global[0], gb[0])
            y0 = max(vg_global[1], gb[1])
            x1 = min(vg_global[0] + vg_global[2], gb[0] + gb[2])
            y1 = min(vg_global[1] + vg_global[3], gb[1] + gb[3])
            if x1 > x0 and y1 > y0:
                inter = (x1 - x0) * (y1 - y0)
                union = vg_global[2] * vg_global[3] + gb[2] * gb[3] - inter
                iou = inter / max(1, union)
                # Containment: Vision-BBox ist innerhalb Page-Glyph
                containment = inter / max(1, vg_global[2] * vg_global[3])
                # Akzeptiere wenn IoU > 0.05 ODER Containment > 0.3
                score = max(iou, 0.5 * containment)
                if score > best_iou:
                    best_iou = score
                    best_glyph = g
        if best_iou > 0.05 and best_glyph is not None:
            matched_glyphs.append({
                "vision_glyph": vg,
                "matched_glyph_index": best_glyph["glyph_index"],
                "iou": round(best_iou, 3),
                "page_glyph_bbox": best_glyph["bbox"],
            })
        else:
            unmatched_vision.append(vg)

    out = {
        "page": page_id,
        "line_id": line_id,
        "line_bbox": line_data["bbox"],
        "line_type": vision_result.get("line_type", "unknown"),
        "line_description": vision_result.get("line_description", ""),
        "n_glyphs_vision": len(vision_result.get("glyphs", [])),
        "n_latin_tokens": len(vision_result.get("latin_tokens", [])),
        "n_numerics": len(vision_result.get("numerics", [])),
        "n_formulas": len(vision_result.get("formulas", [])),
        "n_graphics": len(vision_result.get("graphics", [])),
        "n_matched_glyphs": len(matched_glyphs),
        "n_unmatched_vision_glyphs": len(unmatched_vision),
        "matched_glyphs": matched_glyphs,
        "unmatched_vision_glyphs": unmatched_vision,
        "latin_tokens": vision_result.get("latin_tokens", []),
        "numerics": vision_result.get("numerics", []),
        "formulas": vision_result.get("formulas", []),
        "graphics": vision_result.get("graphics", []),
        "schmeh_hint": schmeh_hint,
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--components", type=Path, required=True,
                    help="bbox/components_<TS>/")
    ap.add_argument("--schmeh-hints", type=Path, default=None,
                    help="bbox/schmeh_hints_<TS>/ (optional, nur Hinweise)")
    ap.add_argument("--schema", type=Path,
                    default=ROOT / "schemas" / "line_vision.schema.json")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--only-page", type=int, default=None,
                    help="Nur diese eine Seite verarbeiten (Debug)")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    pages = list(range(args.only_page, args.only_page + 1) if args.only_page
                 else range(1, 24))

    all_lines = []
    for i in pages:
        page_id = f"p{i:02d}"
        page_dir = args.components / page_id
        if not (page_dir / f"{page_id}_lines.json").exists():
            print(f"  {page_id}: SKIP (no lines.json)")
            continue
        lines_data = json.loads((page_dir / f"{page_id}_lines.json").read_text())
        schmeh_hints = None
        if args.schmeh_hints and (args.schmeh_hints / f"{page_id}_hints.json").exists():
            schmeh_hints = json.loads(
                (args.schmeh_hints / f"{page_id}_hints.json").read_text())
        page_vision_dir = args.out / page_id
        page_vision_dir.mkdir(parents=True, exist_ok=True)

        # Sammle Tasks
        tasks = []
        for line in lines_data["lines"]:
            tasks.append((page_id, line["line_id"], line, page_dir,
                          schmeh_hints, args.schema, page_vision_dir))
        # Parallel ausführen
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futs = {pool.submit(process_line, *t): t for t in tasks}
            for fut in as_completed(futs):
                t = futs[fut]
                try:
                    result = fut.result()
                    line_id = result.get("line_id")
                    if "error" in result and "n_glyphs_vision" not in result:
                        print(f"  {t[0]} line {line_id}: ERROR {result['error']}")
                        continue
                    out_path = t[6] / f"{t[0]}_line{line_id:02d}.json"
                    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
                    all_lines.append(result)
                    line_type = result.get("line_type", "?")
                    n_matched = result.get("n_matched_glyphs", 0)
                    n_latin = result.get("n_latin_tokens", 0)
                    print(f"  {t[0]} line {line_id:>2}: type={line_type:<22} "
                          f"matched={n_matched} latin={n_latin}")
                except Exception as e:
                    print(f"  {t[0]} line {t[1]}: EXC {e}")

        # Page-Level Summary
        page_summary = {
            "page": page_id,
            "n_lines": len(lines_data["lines"]),
            "n_lines_vision_ok": sum(1 for l in all_lines if l.get("page") == page_id
                                      and "error" not in l),
            "n_total_vision_glyphs": sum(l.get("n_glyphs_vision", 0)
                                          for l in all_lines if l.get("page") == page_id),
            "n_total_matched": sum(l.get("n_matched_glyphs", 0)
                                    for l in all_lines if l.get("page") == page_id),
            "n_total_latin_tokens": sum(l.get("n_latin_tokens", 0)
                                          for l in all_lines if l.get("page") == page_id),
            "line_types": [l.get("line_type", "?") for l in all_lines
                            if l.get("page") == page_id],
        }
        (page_vision_dir / f"{page_id}_page.json").write_text(
            json.dumps(page_summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
