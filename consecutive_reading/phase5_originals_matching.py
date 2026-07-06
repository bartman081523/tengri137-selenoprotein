"""
phase5_originals_matching.py
V8 Phase 5 — CV-Template-Matching V6-Token ↔ PGP-Original (Konsolidierung)

Input:
- bbox/originals_compare_20260706_V8/phase1_summary.json (Phase 1 Ergebnisse)
- bbox/originals_compare_20260706_V8/p{NN}_re_extract/ (Re-Extract Crops)

Output:
- bbox/template_matcher_20260706_V8/p{NN}_matched.json
- bbox/template_matcher_20260706_V8/phase5_summary.json

Konsolidiert die Phase-1-Re-Extract-Ergebnisse und generiert eine
konsolidierte Match-Tabelle pro Seite.
"""
import json
import re
import os
from pathlib import Path
from datetime import datetime
from collections import Counter

PHASE1_SUMMARY = Path("bbox/originals_compare_20260706_V8/phase1_summary.json")
OUT_DIR = Path("bbox/template_matcher_20260706_V8")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("=" * 80)
    print("V8 PHASE 5: CV-TEMPLATE-MATCHING KONSOLIDIERUNG")
    print("=" * 80)

    with open(PHASE1_SUMMARY) as f:
        phase1 = json.load(f)

    pages_data = phase1['pages']

    # 1. Pro-Seite Match-Tabelle
    print("\n[1/2] Generiere Match-Tabelle pro Seite...")
    total_v6 = 0
    total_match = 0
    total_id_match = 0
    total_high_iou = 0

    for page_id, data in pages_data.items():
        matches = data.get('matches_sample', [])
        # Konsolidiere: Bilde die Match-Tabelle
        match_table = {
            "page_id": page_id,
            "n_v6_tokens": data['n_v6_tokens'],
            "n_bbox_matches": data['n_bbox_matches'],
            "n_glyph_id_matches": data['n_glyph_id_matches'],
            "n_high_iou_matches": data['n_high_iou_matches'],
            "n_unmatched_v6": data['n_unmatched_v6'],
            "glyph_id_agreement_rate": (
                data['n_glyph_id_matches'] / max(1, data['n_bbox_matches'])
            ),
            "high_iou_rate": (
                data['n_high_iou_matches'] / max(1, data['n_bbox_matches'])
            ),
            "first_10_matches": matches[:10],
        }
        with open(OUT_DIR / f"{page_id}_matched.json", 'w') as f:
            json.dump(match_table, f, indent=2, ensure_ascii=False)

        total_v6 += data['n_v6_tokens']
        total_match += data['n_bbox_matches']
        total_id_match += data['n_glyph_id_matches']
        total_high_iou += data['n_high_iou_matches']

        if int(page_id[1:]) <= 10:
            rate_id = 100 * data['n_glyph_id_matches'] / max(1, data['n_bbox_matches'])
            rate_iou = 100 * data['n_high_iou_matches'] / max(1, data['n_bbox_matches'])
            print(f"  {page_id}: {data['n_v6_tokens']:3} v6, "
                  f"{data['n_bbox_matches']:3} match, "
                  f"{rate_id:5.1f}% ID-agree, "
                  f"{rate_iou:5.1f}% high-IoU")

    # 2. Phase 5 Summary
    summary = {
        "metadata": {
            "phase": "V8 / Phase 5",
            "datum": datetime.now().isoformat(),
            "input": "Phase 1 Re-Extract Ergebnisse",
            "scale_x": 1.184,
            "scale_y": 1.229,
        },
        "aggregate_stats": {
            "total_v6_tokens": total_v6,
            "total_bbox_matches": total_match,
            "total_glyph_id_matches": total_id_match,
            "total_high_iou_matches": total_high_iou,
            "match_rate_bbox": total_match / max(1, total_v6),
            "match_rate_glyph_id": total_id_match / max(1, total_match),
            "match_rate_high_iou": total_high_iou / max(1, total_match),
        },
        "verdict": {
            "v6_pipeline_robust": total_match / max(1, total_v6) > 0.95,
            "v6_glyph_classification_robust": total_id_match / max(1, total_match) > 0.75,
            "scale_factor_confirmed": total_high_iou / max(1, total_match) > 0.6,
        },
    }
    with open(OUT_DIR / "phase5_summary.json", 'w') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 80}")
    print(f"PHASE 5 ABGESCHLOSSEN (Konsolidierung)")
    print(f"{'=' * 80}")
    print(f"  Total V6-Tokens: {total_v6}")
    print(f"  Bbox-Match-Rate: {100*total_match/max(1,total_v6):.1f}%")
    print(f"  Glyph-ID-Agreement: {100*total_id_match/max(1,total_match):.1f}%")
    print(f"  High-IoU-Rate: {100*total_high_iou/max(1,total_match):.1f}%")
    print(f"  V6-Pipeline-Robustheit: {'BESTÄTIGT' if summary['verdict']['v6_pipeline_robust'] else 'FALSIFIZIERT'}")
    print(f"  V6-Glyph-Klassifikation: {'BESTÄTIGT' if summary['verdict']['v6_glyph_classification_robust'] else 'FALSIFIZIERT'}")
    print(f"  Output: bbox/template_matcher_20260706_V8/")


if __name__ == "__main__":
    main()
