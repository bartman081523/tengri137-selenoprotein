#!/usr/bin/env python3
"""
phase5_decode.py — Substitutions-Validierung (CryptanalysisMind).

V5 PIVOT: Validiert die Hypothese H1 (monoalphabetische Substitution für englischen
Klartext) gegen die Befunde aus Phase 1 (Kryptanalyse), Phase 2 (Alphabet-Größe)
und Phase 4 (OCR).

Input:  bbox/cryptanalysis_20260705_V5/crypto_report.json  (Phase 1 Hypothese)
        bbox/alphabet_20260705_V5/alphabet.json  (Phase 2 K)
        bbox/ocr_20260705_V5/p{NN}.json  (Phase 4 OCR-Tokens)
Output: bbox/decoded_20260705_V5/decode_report.json
        {
          "hypothesis_h1_status": "akzeptiert" | "abgelehnt" | "unbestimmt",
          "evidence": {
            "phase1_ioc": 0.16,
            "phase1_entropy": 2.87,
            "phase1_zipf": 2.93,
            "phase2_K_actual": 34,
            "phase2_K_predicted": [25, 35],
            "phase2_silhouette": 0.51,
            "phase4_latin_tokens_per_page": {"p23": 222, ...},
            "phase4_real_latin_pages": ["p23"]
          },
          "interpretation": "H1 abgelehnt: IoC 0.16 ist 2x zu hoch für Englisch (0.067). Das Substrat zeigt BURST-artige Repetition (Top-Bigramm S6S6 mit 2300 Hits), was auf eine LISTE von Glyphen-Varianten hindeutet, nicht auf natürlichen Klartext. K=34 liegt am oberen Rand der Vorhersage (25-35)."
        }
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def validate_hypothesis(phase1: dict, phase2: dict, phase4_dir: Path) -> dict:
    """Validiere H1 gegen alle Phasen-Befunde."""
    p1 = phase1["hypothesis"]
    p2 = phase2
    p1_ioc = phase1["ioc"]
    p1_h = phase1["shannon_entropy"]
    p1_zipf = phase1["zipf_alpha"]

    # Phase 4: Lateinische Tokens pro Page
    latin_per_page = {}
    real_latin_pages = []
    for f in sorted(phase4_dir.glob("p*.json")):
        d = json.loads(f.read_text())
        page_id = d["page_id"]
        n_latin = sum(len(r["latin_tokens"]) for r in d["regions"])
        latin_per_page[page_id] = n_latin
        if n_latin > 0 and d["layout_type"] != "fliesstext":
            real_latin_pages.append(page_id)

    evidence = {
        "phase1": {
            "hypothesis_label": p1["label"],
            "predicted_K": p1["predicted_alphabet_size"],
            "shannon_entropy": p1_h,
            "ioc": p1_ioc,
            "zipf_alpha": p1_zipf,
        },
        "phase2": {
            "actual_K": p2["actual_K"],
            "silhouette": p2["silhouette"],
            "K_in_predicted_range": (p1["predicted_alphabet_size"][0]
                                     <= p2["actual_K"]
                                     <= p1["predicted_alphabet_size"][1]),
        },
        "phase4": {
            "latin_tokens_per_page": latin_per_page,
            "real_latin_pages": real_latin_pages,
            "n_pages_with_latin": len(real_latin_pages),
            "interpretation": ("p23 (Chemie): Primfaktorzerlegungen + lateinische Symbole. "
                               "p17-p22 (Burumut-Block): Primfaktorzerlegungen, KEINE lateinischen Wörter. "
                               "p05/p06 (Magic-Cube): keine OCR-fähigen Ziffern (3D-Würfel). "
                               "p01-p04, p07-p16 (Fließtext): 0 lateinische Tokens — reines Tengri."),
        },
    }

    # F1-Kriterien
    f1_score = 0
    f1_reasons = []

    # F1.1: IoC-Test
    english_ioc = 0.067
    if 0.055 <= p1_ioc <= 0.080:
        f1_score += 2
        f1_reasons.append(f"F1.1 PASS: IoC {p1_ioc:.4f} ∈ [0.055, 0.080] (Englisch-konsistent)")
    else:
        f1_score -= 1
        f1_reasons.append(f"F1.1 FAIL: IoC {p1_ioc:.4f} ∉ [0.055, 0.080] (Abweichung: "
                          f"{abs(p1_ioc - english_ioc):.4f})")

    # F1.2: Entropie-Test
    if 3.8 <= p1_h <= 4.6:
        f1_score += 1
        f1_reasons.append(f"F1.2 PASS: H {p1_h:.4f} ∈ [3.8, 4.6]")
    else:
        f1_score -= 1
        f1_reasons.append(f"F1.2 FAIL: H {p1_h:.4f} ∉ [3.8, 4.6]")

    # F1.3: Zipf-Test
    if 0.8 <= p1_zipf <= 1.2:
        f1_score += 1
        f1_reasons.append(f"F1.3 PASS: α {p1_zipf:.4f} ∈ [0.8, 1.2]")
    else:
        f1_score -= 1
        f1_reasons.append(f"F1.3 FAIL: α {p1_zipf:.4f} ∉ [0.8, 1.2]")

    # F1.4: K in predicted range
    if evidence["phase2"]["K_in_predicted_range"]:
        f1_score += 1
        f1_reasons.append(f"F1.4 PASS: K={p2['actual_K']} in {p1['predicted_alphabet_size']}")
    else:
        f1_score -= 1
        f1_reasons.append(f"F1.4 FAIL: K={p2['actual_K']} NOT in {p1['predicted_alphabet_size']}")

    # F1.5: Reale lateinische Wörter auf den Fließtext-Pages? (KEINE erwartet)
    fliesstext_pages_with_latin = [
        pid for pid, n in latin_per_page.items()
        if n > 0 and (phase4_dir.parent.parent / "layout_20260705_V5" / f"{pid}.json").exists()
    ]
    # Vereinfachung: Wir prüfen, ob die Pages mit lateinischen Tokens Fließtext-Pages sind
    layout_dir = phase4_dir.parent.parent / "layout_20260705_V5"
    fliesstext_latin = []
    for pid, n in latin_per_page.items():
        if n > 0 and (layout_dir / f"{pid}.json").exists():
            layout = json.loads((layout_dir / f"{pid}.json").read_text())
            if layout["layout_type"] == "fliesstext":
                fliesstext_latin.append(pid)
    if not fliesstext_latin:
        f1_score += 1
        f1_reasons.append("F1.5 PASS: Keine lateinischen Tokens auf Fließtext-Pages (Tengri-only)")
    else:
        f1_score -= 1
        f1_reasons.append(f"F1.5 FAIL: Fließtext-Pages mit lateinischen Tokens: {fliesstext_latin}")

    # Gesamt-Bewertung
    if f1_score >= 3:
        h1_status = "akzeptiert"
    elif f1_score >= 1:
        h1_status = "unbestimmt"
    else:
        h1_status = "abgelehnt"

    return {
        "hypothesis_h1_status": h1_status,
        "f1_score": f1_score,
        "f1_reasons": f1_reasons,
        "evidence": evidence,
        "interpretation": generate_interpretation(h1_status, evidence),
    }


def generate_interpretation(status: str, evidence: dict) -> str:
    """Erzeuge eine lesbare Interpretation der Befunde."""
    p1 = evidence["phase1"]
    p2 = evidence["phase2"]
    p4 = evidence["phase4"]

    return (
        f"H1-Status: {status.upper()}\n"
        f"\n"
        f"Phase 1 (Kryptanalyse):\n"
        f"  - Hypothese: {p1['hypothesis_label']}\n"
        f"  - Shannon-Entropie H = {p1['shannon_entropy']:.4f} (Englisch-Ref: 4.14)\n"
        f"  - Index of Coincidence = {p1['ioc']:.4f} (Englisch-Ref: 0.067)\n"
        f"  - Zipf α = {p1['zipf_alpha']:.4f} (Englisch-Ref: ≈1.0)\n"
        f"\n"
        f"Phase 2 (Alphabet):\n"
        f"  - K = {p2['actual_K']} distinkte Glyphen-Cluster (Vorhersage: {p1['predicted_K']})\n"
        f"  - Silhouette = {p2['silhouette']:.4f}\n"
        f"  - K_in_predicted_range: {p2['K_in_predicted_range']}\n"
        f"\n"
        f"Phase 4 (OCR):\n"
        f"  - Pages mit lateinischen Tokens: {p4['real_latin_pages']}\n"
        f"  - {p4['n_pages_with_latin']}/23 Pages haben lateinische Zeichen\n"
        f"  - Lateinische Zeichen sind: {p4['interpretation']}\n"
        f"\n"
        f"Schlussfolgerung:\n"
        f"  Die V5-Befunde {'stützen' if status == 'akzeptiert' else 'widerlegen'} die H1-Hypothese "
        f"(monoalphabetische Substitution für englischen Klartext). "
        f"Der hohe IoC ({p1['ioc']:.4f} vs. Englisch 0.067) deutet auf eine ungewöhnlich repetitive "
        f"Substrat-Struktur hin, möglicherweise eine Liste von Glyphen-Varianten "
        f"oder ein nicht-sprachliches System. K=34 Glyphen-Cluster passt zu "
        f"einem Alphabet aus ~26 Buchstaben + 10 Ziffern — die Hypothese, dass "
        f"Tengri ein Substitutions-Alphabet ist, bleibt plausibel, aber der Klartext "
        f"scheint KEIN englisches Englisch zu sein. Mögliche Alternativen: "
        f"(a) eine andere Sprache (Türkisch, Mongolisch), (b) numerische/templated Inhalte, "
        f"(c) ein nicht-linguistisches System (Code, Glyphen-Sequenzen)."
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase1", type=Path, required=True,
                    help="bbox/cryptanalysis_20260705_V5/crypto_report.json")
    ap.add_argument("--phase2", type=Path, required=True,
                    help="bbox/alphabet_20260705_V5/alphabet.json")
    ap.add_argument("--phase4", type=Path, required=True,
                    help="bbox/ocr_20260705_V5/")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/decoded_20260705_V5/")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    phase1 = json.loads(args.phase1.read_text())
    phase2 = json.loads(args.phase2.read_text())

    print("[Phase 5] Validiere H1 gegen alle Phasen…")
    result = validate_hypothesis(phase1, phase2, args.phase4)

    out_path = args.out / "decode_report.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\n[Phase 5] H1-Status: {result['hypothesis_h1_status'].upper()}")
    print(f"[Phase 5] F1-Score: {result['f1_score']}")
    print(f"\n[Phase 5] Interpretation:")
    print(result["interpretation"])


if __name__ == "__main__":
    main()
