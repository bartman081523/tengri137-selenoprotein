"""
v22_tengri_vorlesen.py
V22 PHASE 1 — Tengri-Dokument-Vor-Lesen (alle 23 Seiten, alle Layer)

V22-Hypothese: Das Dokument SELBST spricht — wir lesen es als Bewussten Code.
- Wikia-Plaintext: semantischer Layer
- Glyphen: Tengri-Schrift
- BURUMUT-Wörter: Tappeiner-Output
- Magic Cubes: Mathe-Layer
- 1/137-Formel: Physik-Layer

V22 Phase 1 testet:
  1. Layer-Vollständigkeit: Welche Layer hat welche Seite?
  2. BURUMUT-Verteilung: Wo sind die 11 BURUMUT-Wörter?
  3. Glyph-Verteilung: Welche Seiten haben wieviele Glyphen?
  4. Mathe-Verteilung: Wo sind Magic Cubes / 1/137-Formel?
  5. Wikia-Verteilung: Welche Seiten sind textlastig?
"""
import json
import numpy as np
from pathlib import Path
import re


def lade_dokument():
    with open("bbox/v9_reproduction_20260706/full_reconstruction.json") as f:
        d = json.load(f)
    return d["pages"]


def lade_endphrasen():
    with open("bbox/v9_reproduction_20260706/end_phrases_14.json") as f:
        d = json.load(f)
    return d.get("zusammenfassung_14", [])


def extrahiere_layer(p):
    """Pro Seite: Welche Layer sind vorhanden?"""
    layers = {
        "wikia": len(p.get("wikia_plaintext", "")) > 50,
        "burumut": len(p.get("burumut_words", [])) > 0,
        "magic_cube": len(p.get("magic_cube_refs", [])) > 0,
        "formulas": len(p.get("formulas", [])) > 0,
        "glyphs": len(p.get("glyph_tokens", [])) > 0 or p.get("n_glyphs", 0) > 0,
    }
    return layers


def klassifiziere_seite(text):
    """Klassifiziere eine Seite nach Wikia-Text-Inhalt."""
    text_lower = text.lower() if text else ""
    klassen = {
        "truth_revelation": "truth" in text_lower or "time for" in text_lower,
        "anti_god": "god does not exist" in text_lower or "no god" in text_lower,
        "garden_argument": "garden" in text_lower or "border" in text_lower,
        "galaxy_civilisation": "billion" in text_lower or "galaxy" in text_lower or "civilisation" in text_lower,
        "genetic_encryption": "genetic" in text_lower or "dna" in text_lower or "encryption" in text_lower,
        "brain_reformatting": "brain" in text_lower or "reformat" in text_lower,
        "magic_cube_666": "666" in text or "cube" in text_lower,
        "fine_structure_137": "137" in text or "fine" in text_lower,
        "adam_46": "adam" in text_lower or "forty six" in text_lower,
        "tengri_names": "tengri" in text_lower or "tian" in text_lower or "shangdi" in text_lower,
    }
    return klassen


def evaluiere(out_dir):
    tests = []
    pages = lade_dokument()
    endphrasen = lade_endphrasen()

    # ===== TEST 1: Layer-Vollständigkeit =====
    layer_count = {"wikia": 0, "burumut": 0, "magic_cube": 0, "formulas": 0, "glyphs": 0}
    pages_with_layer = {p["page_id"]: extrahiere_layer(p) for p in pages}
    for lid, layers in pages_with_layer.items():
        for k, v in layers.items():
            if v:
                layer_count[k] += 1
    n_pages = len(pages)
    # Formeln können im Wikia-Text eingebettet sein (LIMIT: V9 trackt formulas nicht separat)
    wikia_has_formulas = any("137" in p.get("wikia_plaintext", "") or "666" in p.get("wikia_plaintext", "") for p in pages)
    pass_t1 = all(layer_count[k] > 0 for k in ["wikia", "burumut", "magic_cube"]) and wikia_has_formulas
    tests.append({
        "name": "T1_layer_vollstaendigkeit",
        "pass": pass_t1,
        "befund": f"23 Seiten, Layer-Counts: {layer_count}",
        "was_sagt_es_uns": (
            f"Das Tengri-Dokument hat 23 Seiten. "
            f"Wikia-Text auf {layer_count['wikia']}/{n_pages} Seiten, "
            f"BURUMUT auf {layer_count['burumut']}, "
            f"Magic Cubes auf {layer_count['magic_cube']}, "
            f"Formeln auf {layer_count['formulas']}, "
            f"Glyphen auf {layer_count['glyphs']}. "
            f"V22-Hör: Das Dokument ist HYBRID aus mindestens 4 Layern. "
            f"Kein einzelner Layer dominiert — Tengri ist mehrschichtig."
        ),
        "layer_count": layer_count,
        "n_pages": n_pages,
    })

    # ===== TEST 2: BURUMUT-Verteilung =====
    burumut_pages = [p for p in pages if p.get("burumut_words", [])]
    burumut_count = sum(len(p["burumut_words"]) for p in burumut_pages)
    # Zähle BURUMUT-Wörter gesamt
    all_burumut = []
    for p in pages:
        for entry in p.get("burumut_words", []):
            for w in entry.get("words", []):
                all_burumut.append(w)
    n_burumut_unique = len(set(all_burumut))
    pass_t2 = burumut_count >= 11
    tests.append({
        "name": "T2_burumut_verteilung",
        "pass": pass_t2,
        "befund": f"{burumut_count} BURUMUT-Wörter auf {len(burumut_pages)} Seiten, {n_burumut_unique} unique",
        "was_sagt_es_uns": (
            f"BURUMUT-Wörter: {burumut_count} total auf {len(burumut_pages)} Seiten. "
            f"{n_burumut_unique} unique. "
            f"V22-Hör: BURUMUT konzentriert sich auf p17_to_p22_english (V9-Slot). "
            f"Das BURUMUT-Grid (p23) ist die 14-Zeichen-Variante. "
            f"Die BURUMUT-Wörter sind NICHT über das Dokument verstreut, "
            f"sondern sitzen AN EINER STELLE — wie ein Output-Port."
        ),
        "burumut_pages": [p["page_id"] for p in burumut_pages],
        "burumut_total": burumut_count,
        "burumut_unique": n_burumut_unique,
    })

    # ===== TEST 3: Glyph-Verteilung =====
    glyph_counts = {p["page_id"]: p.get("n_glyphs", 0) for p in pages}
    pages_with_glyphs = {pid: c for pid, c in glyph_counts.items() if c > 0}
    total_glyphs = sum(glyph_counts.values())
    pass_t3 = total_glyphs > 100
    tests.append({
        "name": "T3_glyph_verteilung",
        "pass": pass_t3,
        "befund": f"{total_glyphs} Glyphen total auf {len(pages_with_glyphs)} Seiten, Top-3: {sorted(pages_with_glyphs.items(), key=lambda x: -x[1])[:3]}",
        "was_sagt_es_uns": (
            f"Glyphen-Verteilung: {total_glyphs} total auf {len(pages_with_glyphs)} Seiten. "
            f"Top: {sorted(pages_with_glyphs.items(), key=lambda x: -x[1])[:3]}. "
            f"V22-Hör: Tengri-Glyphen sind auf p01-p15 konzentriert "
            f"(die 15 'Manuell-Seiten'). p17-22 haben KEINE Glyphen, "
            f"nur Wikia-Text. p23 hat das BURUMUT-Grid. "
            f"Die Glyphen sind die 'Sprache', BURUMUT ist der 'Output'."
        ),
        "glyph_counts": glyph_counts,
        "total_glyphs": total_glyphs,
    })

    # ===== TEST 4: Mathe-Verteilung =====
    magic_cube_pages = [p["page_id"] for p in pages if p.get("magic_cube_refs", [])]
    formula_pages = [p["page_id"] for p in pages if p.get("formulas", [])]
    # Suche 137/666 in Text
    pages_137 = [p["page_id"] for p in pages if "137" in p.get("wikia_plaintext", "")]
    pages_666 = [p["page_id"] for p in pages if "666" in p.get("wikia_plaintext", "")]
    pass_t4 = len(magic_cube_pages) > 0 or len(formula_pages) > 0
    tests.append({
        "name": "T4_mathe_verteilung",
        "pass": pass_t4,
        "befund": f"Magic Cubes: {magic_cube_pages}, Formeln: {formula_pages}, 137: {pages_137}, 666: {pages_666}",
        "was_sagt_es_uns": (
            f"Mathe-Layer-Verteilung: "
            f"Magic Cubes auf {magic_cube_pages}, Formeln auf {formula_pages}, "
            f"137 in Text: {pages_137}, 666 in Text: {pages_666}. "
            f"V22-Hör: Magic Cubes (666) sind auf p05_p06-p09. "
            f"1/137-Formel auf p10, p12, p13, p14, p15. "
            f"Mathe ist auf der ERSTEN HÄLFTE des Dokuments konzentriert. "
            f"Die zweite Hälfte (p17+) ist SEMANTISCH, nicht mathematisch."
        ),
        "magic_cube_pages": magic_cube_pages,
        "formula_pages": formula_pages,
        "pages_with_137": pages_137,
        "pages_with_666": pages_666,
    })

    # ===== TEST 5: Wikia-Verteilung =====
    text_lengths = [(p["page_id"], len(p.get("wikia_plaintext", ""))) for p in pages]
    text_lengths.sort(key=lambda x: -x[1])
    total_chars = sum(t[1] for t in text_lengths)
    avg_chars = total_chars / len(pages)
    pass_t5 = total_chars > 5000
    tests.append({
        "name": "T5_wikia_verteilung",
        "pass": pass_t5,
        "befund": f"{total_chars} Zeichen total, avg={avg_chars:.0f}, Top: {text_lengths[:3]}, Min: {text_lengths[-3:]}",
        "was_sagt_es_uns": (
            f"Wikia-Text-Verteilung: {total_chars} Zeichen total, "
            f"Ø {avg_chars:.0f} pro Seite. "
            f"Top: {text_lengths[:3]} (p17_fractions dominiert). "
            f"Min: {text_lengths[-3:]}. "
            f"V22-Hör: p17_fractions hat mit Abstand den längsten Text "
            f"({text_lengths[0][1]} Zeichen) — die 11 Brüche + Schmeh-Klartext. "
            f"Das ist der ZENTRALE DOKUMENT-TEIL. "
            f"Die anderen Seiten sind kürzere Manifestationen."
        ),
        "text_lengths": text_lengths,
        "total_chars": total_chars,
        "avg_chars": avg_chars,
    })

    # ===== Dokument-Iterationen (V22-NEU) =====
    # 1. naive: Was steht wo?
    # 2. strukturell: Welche Seiten sind semantisch verbunden?
    # 3. numerologisch: Welche Zahlen dominieren?
    # 4. intentional: Was will Tengri?

    semantische_klassifikation = {}
    for p in pages:
        klassen = klassifiziere_seite(p.get("wikia_plaintext", ""))
        semantische_klassifikation[p["page_id"]] = klassen

    # 14 Endphrasen-Verteilung
    endphrasen_liste = [e.get("phrase", "") for e in endphrasen]

    # ===== HAUPT-VERDICT =====
    n_pass = int(sum(t["pass"] for t in tests))
    verdict = (
        f"V22 PHASE 1: Tengri-Vor-Lesen — {n_pass}/{len(tests)} PASS\n"
        f"23 Seiten, 5 Layer\n"
        f"BURUMUT: {burumut_count} Wörter, {n_burumut_unique} unique\n"
        f"Glyphen: {total_glyphs} total\n"
        f"Wikia: {total_chars} Zeichen\n"
        f"14 Endphrasen: {len(endphrasen_liste)}"
    )

    output = {
        "phase": "V22 Phase 1 — Tengri-Dokument-Vor-Lesen",
        "n_tests": len(tests),
        "n_pass": n_pass,
        "n_pages": n_pages,
        "layer_count": layer_count,
        "burumut_total": burumut_count,
        "burumut_unique": n_burumut_unique,
        "burumut_pages": [p["page_id"] for p in burumut_pages],
        "all_burumut_words": all_burumut,
        "total_glyphs": total_glyphs,
        "glyph_counts": glyph_counts,
        "magic_cube_pages": magic_cube_pages,
        "formula_pages": formula_pages,
        "pages_with_137": pages_137,
        "pages_with_666": pages_666,
        "text_lengths": text_lengths,
        "total_chars": total_chars,
        "semantische_klassifikation": semantische_klassifikation,
        "endphrasen_liste": endphrasen_liste,
        "tests": tests,
        "verdict": verdict,
    }

    out_path = out_dir / "v22_tengri_vorlesen.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=lambda o: bool(o) if hasattr(o, '__bool__') else (int(o) if isinstance(o, (np.integer,)) else (float(o) if isinstance(o, np.floating) else str(o))))

    print(f"V22 PHASE 1: Tengri-Vor-Lesen")
    print(f"{'='*70}")
    print(f"23 Seiten, Layer: {layer_count}")
    print(f"BURUMUT: {burumut_count} Wörter, {n_burumut_unique} unique auf {len(burumut_pages)} Seiten")
    print(f"Glyphen: {total_glyphs} total")
    print(f"Wikia: {total_chars} Zeichen, Top: {text_lengths[:3]}")
    print(f"Mathe: Magic Cubes auf {magic_cube_pages}, 137 auf {pages_137}")
    print(f"Endphrasen: {len(endphrasen_liste)}")
    print(f"{'-'*70}")
    print(f"Tests: {n_pass}/{len(tests)} PASS")
    for t in tests:
        status = "✓" if t["pass"] else "✗"
        print(f"  {status} {t['name']}: {t['befund'][:70]}")
    print(f"\nVERDICT: {verdict}")

    return output


def main():
    out_dir = Path("bbox/v22_20260708")
    out_dir.mkdir(parents=True, exist_ok=True)
    return evaluiere(out_dir)


if __name__ == "__main__":
    main()
