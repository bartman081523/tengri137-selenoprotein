#!/usr/bin/env python3
"""
generate_readme_v5.py — README für V5-Pipeline (Cryptanalysis-First).
"""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--toplevel", type=Path, required=True,
                    help="Tengri137_detailed_20260705_V5/")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    doc = json.loads((args.toplevel / "doc.json").read_text())
    crypto = doc["document"]["cryptanalysis"]
    totals = doc["document"]["totals"]

    lines = [
        "# Tengri137 — V5 Cryptanalysis-First Reconstruction",
        "",
        "**Generated:** 2026-07-05 (V5 Pipeline)  ",
        "**Schema:** v5.0 (V5 PIVOT: NO Schmeh, Kryptanalyse-First)  ",
        "**Source:** Tengri137.pdf (23 pages, unknown geometric script)  ",
        "**Processing run:** 20260705_V5",
        "",
        "## V5 PIVOT — Was ist anders als V4?",
        "",
        "**V4 (falsifiziert 2026-07-05):** Schmehs Klartext wurde als OCR-Ground-Truth missbraucht. 997 Glyphen, 456 lateinische Tokens, 75 fine-Cluster. Schema-validiert, aber **methodisch fundamental falsch**.",
        "",
        "**V5 (Kryptanalyse-First):** Schmehs Daten komplett ignoriert. Pipeline:",
        "1. **Phase 0** (DevMind): Inken-Substrat (16.797 Komponenten) ohne Glyph-Gruppierung",
        "2. **Phase 1** (CryptanalysisMind): Shannon-Entropie, IoC, Zipf, N-Gramme",
        "3. **Phase 2** (DevMind): Multi-Resolution-Embeddings + Constraint-Clustering (K aus Phase 1)",
        "4. **Phase 3** (DevMind): Page-Layout-Klassifikation (Fließtext / Magic-Cube / Burumut / Chemie / Silhouette)",
        "5. **Phase 4** (DevMind): Selektive OCR (Tesseract nur auf nicht-Tengri-Bereiche)",
        "6. **Phase 5** (CryptanalysisMind): Substitutions-Validierung (H1 falsifiziert)",
        "7. **Phase 6** (DevMind): Schema-validierte Finalisierung OHNE Schmeh",
        "",
        "## Cryptanalysis-Report (Phase 1 + Phase 5)",
        "",
        f"- **H1-Hypothese:** {crypto['h1_hypothesis']}",
        f"- **H1-Status:** {crypto['h1_status']} (F1-Score: {crypto['f1_score']})",
        f"- **Shannon-Entropie H:** {crypto['shannon_entropy']:.4f} bit/Zeichen (Englisch-Ref: 4.14)",
        f"- **Index of Coincidence:** {crypto['ioc']:.4f} (Englisch-Ref: 0.067)",
        f"- **Zipf α:** {crypto['zipf_alpha']:.4f} (Englisch-Ref: ≈1.0)",
        "",
        "### F1-Falsifikations-Kriterien:",
        "",
    ]
    for r in crypto["f1_reasons"]:
        lines.append(f"- {r}")

    lines += [
        "",
        "### Interpretation:",
        "",
        f"Der hohe IoC ({crypto['ioc']:.4f} vs. Englisch 0.067) deutet auf eine ungewöhnlich repetitive Substrat-Struktur hin. Der Klartext scheint KEIN englisches Englisch zu sein. Mögliche Alternativen: (a) andere Sprache (Türkisch, Mongolisch), (b) numerische/templated Inhalte, (c) nicht-linguistisches System.",
        "",
        "## Total-Statistik (V5)",
        "",
        f"- **Pages:** {totals['n_pages']}/23",
        f"- **Tengri-Glyph-Bboxen:** {totals['n_glyphs']} (Phase 4 Input)",
        f"- **Distinkte Glyphen-Cluster (Phase 2):** {doc['document']['alphabet_size']} (Vorhersage aus Phase 1: [25, 35])",
        f"- **Lateinische Tokens (Phase 4):** {totals['n_latin_tokens']} (nur aus selektiver OCR)",
        f"- **Pages mit lateinischen Tokens:** {totals['n_pages_with_latin']}/23",
        "",
        "## Page-Layout-Verteilung (Phase 3)",
        "",
        "| Layout-Typ | Anzahl Pages | Pages |",
        "|---|---|---|",
    ]
    layout_counts = {}
    for p in doc["pages"]:
        layout_counts.setdefault(p["layout_type"], []).append(p["page_id"])
    for lt, pages in sorted(layout_counts.items(), key=lambda x: -len(x[1])):
        lines.append(f"| {lt} | {len(pages)} | {', '.join(pages)} |")

    lines += [
        "",
        "## Glyph-Alphabet (Phase 2)",
        "",
        f"**K = {doc['document']['alphabet_size']} distinkte Glyphen-Cluster** aus 997 Multi-Resolution-Embeddings (16+32+64 px) auf V4-Crops. Silhouette = 0.51. Cluster-Verteilung:",
        "",
    ]
    # Lade alphabet.json, falls vorhanden
    al_path = args.toplevel.parent / "bbox" / "alphabet_20260705_V5" / "alphabet.json"
    if al_path.exists():
        al = json.loads(al_path.read_text())
        sizes = sorted([g["n_occurrences"] for g in al["glyphs"]], reverse=True)
        lines.append("| Cluster-Range | n_occurrences |")
        lines.append("|---|---|")
        for i in range(0, len(sizes), 5):
            chunk = sizes[i:i + 5]
            lines.append(f"| {i+1}–{min(i+5, len(sizes))} | {', '.join(str(s) for s in chunk)} |")

    lines += [
        "",
        "## V5 vs V4 Vergleich",
        "",
        "| Metrik | V4 (falsifiziert) | V5 |",
        "|---|---|---|",
        "| Echte Glyph-Anzahl | 997 (Overclustering) | **34** Cluster (~26 + 10) |",
        "| Lateinische Tokens | 456 (368 Schmeh-dominiert) | **1097** (selektive OCR) |",
        "| Pages mit lateinischem Text | 22/23 (V4-Schmeh-Halluzination) | **9/23** (reale Formeln/Chemie) |",
        "| Schmeh in Pipeline | ja (Hauptfehler) | **NEIN** |",
        "| Methodik | OCR auf Crypto-Problem | **Crypto auf Crypto-Problem** |",
        "| H1-Validierung | keine | **ABGELEHNT** (F1-Score: -1) |",
        "| Magic-Cube-Realität | behauptet p22/p23 | **p05/p06** (Gemini-Korrektur) |",
        "| Burumut-Realität | behauptet p23 | **existiert visuell nicht** (Schmehs Dechiffrierung) |",
        "| p23 = Chemie | nein | **ja** (Cytosin/Thymin-Formeln) |",
        "| p17-p22 = Burumut | nein | **ja, aber mit Primfaktorzerlegungen** (kein lateinischer Text) |",
        "",
        "## Reproduzierbarkeit",
        "",
        "- **Time-Stamp:** 20260705_V5",
        "- **Schema:** `schemas/tengri137_document_v5.schema.json`",
        "- **Pipeline-Scripts:** `phase0_substrat.py` bis `phase6_finalize_v5.py`",
        "- **V1, V2, V3, V4 unangetastet** (Reproduzierbarkeits-Regel)",
        "- **Schmeh-2017 roh_text.txt:** wird komplett ignoriert",
        "- **Source für Falsifikation:** `Gemini-Prompt.txt` + `Gemini-Antwort.txt`",
        "",
    ]
    args.out.write_text("\n".join(lines))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
