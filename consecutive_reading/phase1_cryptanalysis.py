#!/usr/bin/env python3
"""
phase1_cryptanalysis.py — CryptanalysisMind Phase 1.

V5 PIVOT: V4 hat Schmehs Klartext als OCR-Ground-Truth missbraucht. V5 ignoriert
Schmeh komplett und macht echte Kryptanalyse auf dem visuellen Substrat:
  - Shannon-Entropie H
  - Index of Coincidence (IoC)
  - N-Gramm-Frequenzen
  - Hypothese: monoalphabetische Substitution für englischen Klartext?

Erwartete Befunde (Englisch-Referenz):
  - Shannon-Entropie H ≈ 4.0-4.5 bit/Zeichen
  - IoC ≈ 0.067 (Englisch) vs 0.038 (Zufallstext bei N=26)
  - Top-Bigramme: TH, HE, IN, ER, AN, RE, ON, AT, EN, ND
  - Wenn Befunde passen → H1 akzeptiert, ~25-35 Glyphen erwartet

Input:  bbox/components_20260704_V4/p{NN}/p{NN}_components.json
        (V4-Substrat = V5-Phase-0-Substrat — gleiche Datenstruktur)
Output: bbox/cryptanalysis_20260705_V5/crypto_report.json
        {
          "hypothesis": "monoalphabetische_substitution" | "poly..." | "...",
          "shannon_entropy": 4.32,
          "ioc": 0.0645,
          "ngram_frequencies": {...},
          "predicted_alphabet_size": [25, 35],
          "predicted_zipf_alpha": 1.0,
          "falsification_criteria": {...}
        }
"""
import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")

# Englisch-Referenz-Werte (aus Standard-Krypto-Literatur)
ENGLISH_REFERENCE = {
    "shannon_entropy": 4.14,  # bit/Zeichen
    "ioc": 0.0667,            # Index of Coincidence
    "top_bigrams": ["TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND"],
    "top_letters": ["E", "T", "A", "O", "I", "N", "S", "H", "R", "D",
                    "L", "C", "U", "M", "W", "F", "G", "Y", "P", "B",
                    "V", "K", "J", "X", "Q", "Z"],
    # Englisch-Buchstaben-Frequenzen (%)
    "letter_freq": {
        "E": 12.7, "T": 9.1, "A": 8.2, "O": 7.5, "I": 7.0, "N": 6.7,
        "S": 6.3, "H": 6.1, "R": 6.0, "D": 4.3, "L": 4.0, "C": 2.8,
        "U": 2.8, "M": 2.4, "W": 2.4, "F": 2.2, "G": 2.0, "Y": 2.0,
        "P": 1.9, "B": 1.5, "V": 1.0, "K": 0.8, "J": 0.2, "X": 0.2,
        "Q": 0.1, "Z": 0.1,
    },
}

# Zufallstext-Referenz (für IoC)
RANDOM_IOC_N26 = 1.0 / 26  # ≈ 0.0385


def shannon_entropy(freqs: dict) -> float:
    """Berechne Shannon-Entropie H = -Σ pᵢ log₂(pᵢ)."""
    total = sum(freqs.values())
    if total == 0:
        return 0.0
    h = 0.0
    for count in freqs.values():
        if count > 0:
            p = count / total
            h -= p * math.log2(p)
    return h


def index_of_coincidence(freqs: dict) -> float:
    """IoC = Σ nᵢ(nᵢ-1) / N(N-1). Englisch: 0.0667, Zufall: 1/N."""
    total = sum(freqs.values())
    if total < 2:
        return 0.0
    ioc = 0.0
    for count in freqs.values():
        ioc += count * (count - 1)
    return ioc / (total * (total - 1))


def zipf_alpha(freqs: dict) -> float:
    """Zipf'scher Exponent: log(rank) vs log(freq) lineare Regression."""
    if len(freqs) < 3:
        return 1.0
    sorted_freqs = sorted(freqs.values(), reverse=True)
    log_ranks = [math.log(i + 1) for i in range(len(sorted_freqs))]
    log_freqs = [math.log(f) for f in sorted_freqs if f > 0]
    if len(log_ranks) != len(log_freqs):
        return 1.0
    n = len(log_ranks)
    mean_x = sum(log_ranks) / n
    mean_y = sum(log_freqs) / n
    num = sum((log_ranks[i] - mean_x) * (log_freqs[i] - mean_y) for i in range(n))
    den = sum((log_ranks[i] - mean_x) ** 2 for i in range(n))
    if den == 0:
        return 1.0
    return -num / den  # Negativ, weil f ~ r^-α


def ngram_frequencies(sequence: list, n: int) -> Counter:
    """Berechne N-Gramm-Häufigkeiten aus einer Sequenz von Tokens."""
    grams = Counter()
    for i in range(len(sequence) - n + 1):
        gram = tuple(sequence[i:i + n])
        grams[gram] += 1
    return grams


def load_substrate(components_dir: Path) -> dict:
    """Lade alle 23 Pages und erstelle eine flache Token-Sequenz.

    Token = Component-ID (jede sichtbare Tinteinheit).
    WICHTIG: Wir gruppieren NICHT zu Glyphen (V4-Fehler).

    Unterstützt zwei Strukturen:
    - V4: <root>/p{NN}/p{NN}_components.json
    - V5-Phase-0: <root>/p{NN}.json
    """
    all_components = []
    for i in range(1, 24):
        page_id = f"p{i:02d}"
        # V5-Phase-0-Struktur: <root>/p{NN}.json
        v5_path = components_dir / f"{page_id}.json"
        # V4-Struktur: <root>/p{NN}/p{NN}_components.json
        v4_path = components_dir / page_id / f"{page_id}_components.json"
        if v5_path.exists():
            data = json.loads(v5_path.read_text())
        elif v4_path.exists():
            data = json.loads(v4_path.read_text())
        else:
            print(f"  WARNUNG: weder {v5_path} noch {v4_path} existiert, skip",
                  file=sys.stderr)
            continue
        for comp in data.get("components", []):
            all_components.append({
                "page": page_id,
                "id": comp["id"],
                "size_px": comp["size_px"],
                "centroid_y": comp["centroid"][1] if "centroid" in comp else 0,
                "bbox": comp["bbox"],
            })
    return all_components


def discretize_by_size(components: list) -> list:
    """Diskretisiere Komponenten-Größen in Klassen.

    Hintergrund: Wenn Tengri ein Substitutions-Alphabet ist, dann sind
    gleich-große Komponenten wahrscheinlich gleiche Glyphen (gleicher "Buchstabe").
    Verschiedene Größen = verschiedene Glyphen.

    Heuristik: Binning der size_px in ~20 Bins, dann eine Klassen-ID pro Bin.
    """
    if not components:
        return []
    sizes = sorted(set(c["size_px"] for c in components))
    # Logarithmisches Binning (Größen variieren über 3 Größenordnungen)
    min_size = min(sizes) if sizes else 1
    max_size = max(sizes) if sizes else 1
    n_bins = 20
    log_min = math.log(max(min_size, 1))
    log_max = math.log(max(max_size, 1))
    if log_max == log_min:
        return [(c, "S0") for c in components]
    bin_width = (log_max - log_min) / n_bins

    out = []
    for c in components:
        log_s = math.log(max(c["size_px"], 1))
        bin_idx = int((log_s - log_min) / bin_width)
        bin_idx = min(bin_idx, n_bins - 1)
        out.append((c, f"S{bin_idx}"))
    return out


def read_order_by_page(components: list) -> list:
    """Lese-Reihenfolge: Page-aufsteigend, dann Y-aufsteigend (oben→unten), dann X-aufsteigend (links→rechts)."""
    return sorted(components, key=lambda c: (c["page"], c["centroid_y"], c["bbox"][0]))


def build_token_sequence(components: list) -> list:
    """Baue eine Token-Sequenz in Lese-Reihenfolge.

    Token = diskretisierte Größenklasse (S0..S19).
    """
    ordered = read_order_by_page(components)
    discretized = discretize_by_size(ordered)
    return [tok for _, tok in discretized]


def analyze_substrate(components: list) -> dict:
    """CryptanalysisMind Hauptanalyse."""
    print(f"  Substrat: {len(components)} Komponenten über 23 Seiten")

    # 1) Token-Sequenz bauen
    tokens = build_token_sequence(components)
    print(f"  Token-Sequenz (Länge): {len(tokens)}")
    print(f"  Unique Tokens: {len(set(tokens))}")

    # 2) Frequenz-Analyse
    freqs = Counter(tokens)
    print(f"  Top-10 Tokens: {freqs.most_common(10)}")

    # 3) Shannon-Entropie
    H = shannon_entropy(freqs)
    print(f"  Shannon-Entropie H = {H:.4f} bit/Zeichen "
          f"(Englisch-Ref: {ENGLISH_REFERENCE['shannon_entropy']:.4f})")

    # 4) Index of Coincidence
    ioc = index_of_coincidence(freqs)
    print(f"  IoC = {ioc:.4f} "
          f"(Englisch-Ref: {ENGLISH_REFERENCE['ioc']:.4f}, "
          f"Zufall-N26: {RANDOM_IOC_N26:.4f})")

    # 5) Zipf'scher Exponent
    alpha = zipf_alpha(freqs)
    print(f"  Zipf α = {alpha:.4f} (Englisch-Ref: ≈1.0)")

    # 6) N-Gramm-Frequenzen
    bigrams = ngram_frequencies(tokens, 2)
    trigrams = ngram_frequencies(tokens, 3)
    top_bigrams = [("".join(g), c) for g, c in bigrams.most_common(10)]
    top_trigrams = [("".join(g), c) for g, c in trigrams.most_common(10)]
    print(f"  Top-10 Bigramme: {top_bigrams}")

    # 7) Hypothesen-Bewertung
    hypothesis = evaluate_hypotheses(H, ioc, len(set(tokens)), alpha, top_bigrams)

    return {
        "n_components_total": len(components),
        "n_unique_tokens": len(set(tokens)),
        "token_sequence_length": len(tokens),
        "shannon_entropy": round(H, 4),
        "ioc": round(ioc, 4),
        "zipf_alpha": round(alpha, 4),
        "top_bigrams": [{"ngram": n, "count": c} for n, c in top_bigrams],
        "top_trigrams": [{"ngram": n, "count": c} for n, c in top_trigrams],
        "hypothesis": hypothesis,
        "english_reference": ENGLISH_REFERENCE,
        "falsification_criteria": build_falsification_criteria(H, ioc, alpha),
    }


def evaluate_hypotheses(H: float, ioc: float, n_unique: int, alpha: float,
                        top_bigrams: list) -> dict:
    """Bewerte die monoalphabetische-Substitution-Hypothese H1."""
    # H1: Monoalphabetische Substitution für englischen Klartext
    # H2: Polyalphabetische Substitution (z.B. Vigenère)
    # H3: Nicht-linguistisch (Zahlen, Symbole, Code)
    # H4: Anderes Alphabet (z.B. Türkisch, Mongolisch)

    h1_score = 0
    reasons = []

    # IoC-Kriterium: Englisch 0.067, Zufall 0.038
    ioc_diff_english = abs(ioc - ENGLISH_REFERENCE["ioc"])
    ioc_diff_random = abs(ioc - RANDOM_IOC_N26)
    if ioc > 0.05 and ioc < 0.08:
        h1_score += 3
        reasons.append(f"IoC {ioc:.4f} ∈ [0.05, 0.08] — passt zu Englisch")
    elif ioc_diff_random < ioc_diff_english:
        h1_score -= 2
        reasons.append(f"IoC {ioc:.4f} näher an Zufall als an Englisch")
    else:
        h1_score += 1
        reasons.append(f"IoC {ioc:.4f} intermediär, leicht erhöht")

    # Entropie-Kriterium: Englisch ≈ 4.0-4.5
    if 3.5 <= H <= 4.8:
        h1_score += 2
        reasons.append(f"Entropie H {H:.4f} ∈ [3.5, 4.8] — passend für natürliche Sprache")
    else:
        h1_score -= 1
        reasons.append(f"Entropie H {H:.4f} außerhalb des Sprach-Bereichs")

    # Zipf-Kriterium: α ≈ 1.0
    if 0.7 <= alpha <= 1.3:
        h1_score += 1
        reasons.append(f"Zipf α {alpha:.4f} ∈ [0.7, 1.3] — typisch für Sprache")

    # Token-Anzahl-Kriterium: 20-50 unique
    if 15 <= n_unique <= 50:
        h1_score += 1
        reasons.append(f"{n_unique} unique Tokens — passend für Substitutions-Alphabet")
    else:
        h1_score -= 1
        reasons.append(f"{n_unique} unique Tokens — ungewöhnlich")

    # Hypothese
    if h1_score >= 4:
        hypothesis_label = "monoalphabetische_substitution"
        confidence = "hoch"
    elif h1_score >= 1:
        hypothesis_label = "wahrscheinlich_monoalphabetisch"
        confidence = "mittel"
    elif h1_score >= -1:
        hypothesis_label = "unbestimmt"
        confidence = "niedrig"
    else:
        hypothesis_label = "nicht_monoalphabetisch"
        confidence = "mittel"

    # Vorhersage für Phase 2
    if hypothesis_label in ("monoalphabetische_substitution", "wahrscheinlich_monoalphabetisch"):
        predicted_size = [25, 35]
        predicted_zipf = "1.0-1.2"
    elif hypothesis_label == "unbestimmt":
        predicted_size = [15, 50]
        predicted_zipf = "0.8-1.4"
    else:
        predicted_size = [10, 100]
        predicted_zipf = "0.5-1.5"

    return {
        "label": hypothesis_label,
        "confidence": confidence,
        "h1_score": h1_score,
        "reasons": reasons,
        "predicted_alphabet_size": predicted_size,
        "predicted_zipf_range": predicted_zipf,
    }


def build_falsification_criteria(H: float, ioc: float, alpha: float) -> dict:
    """Definiere Falsifikations-Kriterien für Phase 5."""
    return {
        "f1_h1_rejected_if": [
            f"IoC < 0.040 (Zufall-Niveau), aktuell {ioc:.4f}",
            f"H > 5.0 oder H < 3.0 (keine natürliche Sprache), aktuell {H:.4f}",
            f"α < 0.5 oder α > 2.0 (keine Zipf-Verteilung), aktuell {alpha:.4f}",
        ],
        "f1_h1_accepted_if": [
            f"IoC ∈ [0.055, 0.080], aktuell {ioc:.4f}",
            f"H ∈ [3.8, 4.6], aktuell {H:.4f}",
            f"α ∈ [0.8, 1.2], aktuell {alpha:.4f}",
        ],
        "next_phase_constraint": "Cluster-Anzahl K muss in predicted_alphabet_size sein",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--components", type=Path, required=True,
                    help="bbox/components_20260704_V4/  (V4-Substrat = V5-Phase-0)")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/cryptanalysis_20260705_V5/")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    # Substrat laden
    print("[Phase 1] CryptanalysisMind — Lade Substrat…")
    components = load_substrate(args.components)
    if not components:
        print("FEHLER: Kein Substrat gefunden", file=sys.stderr)
        sys.exit(1)

    # Analyse
    print(f"[Phase 1] Analysiere {len(components)} Komponenten…")
    report = analyze_substrate(components)

    # Speichern
    report_path = args.out / "crypto_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n[Phase 1] Report geschrieben: {report_path}")
    print(f"[Phase 1] Hypothese: {report['hypothesis']['label']} "
          f"(confidence: {report['hypothesis']['confidence']})")
    print(f"[Phase 1] Vorhersage Alphabet-Größe: "
          f"{report['hypothesis']['predicted_alphabet_size']}")


if __name__ == "__main__":
    main()
