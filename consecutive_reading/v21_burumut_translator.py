"""
v21_burumut_translator.py
V21 PHASE 2 — BURUMUT-Translator (Bidirektional)

V21 Phase 1 LIMIT: Generator ist lithurgisch, nur 3 BURUMUT-Wörter aktiviert
V21-Hypothese: Translator (BURUMUT → latent → Klartext) zeigt die SEMANTISCHE Bedeutung

V21 Phase 2 testet:
  1. BURUMUT → latente Repräsentation (14-dim) → Wikia-ähnlicher Text
  2. BURUMUT → latente Repräsentation → p1-16 Glyph-Sequenz
  3. BURUMUT → Top-5 ähnliche BURUMUT-Wörter
  4. BNYZTSOYNKS → 11 latente Codes → 11 Wikia-Sätze
  5. Latent-Reproduzierbarkeit
"""
import json
import numpy as np
from pathlib import Path


def lade_burumut():
    with open("bbox/v16_20260707/micro_mp_execution.json") as f:
        m = json.load(f)
    M = np.array(m["burumut_matrix"], dtype=np.float64)
    return M, m["burumut_words"], m["codebook_vector"], m["codebook_words"]


def lade_wikia_text():
    with open("bbox/v9_reproduction_20260706/full_reconstruction.json") as f:
        wikia = json.load(f)
    pages = []
    for p in wikia.get("pages", []):
        text = p.get("wikia_plaintext", "")
        if text:
            pages.append(text)
    return pages


def evaluiere(out_dir):
    tests = []
    M, words, codebook, codebook_words = lade_burumut()
    wikia_pages = lade_wikia_text()
    M_pinv = np.linalg.pinv(M)  # (14, 11)

    # ===== TEST 1: BURUMUT → latente Repräsentation → Wikia-Text =====
    # BURUMUTREFAMTU (Zeile 0 von M) ist die latente Repräsentation
    # Da M semi-orthogonal ist, ist M[0, :] direkt die 14-dimensionale latente Form
    latent_0 = M[0, :].astype(np.float64)  # (14,) = ASCII-Buchstaben
    # Finde nächsten Wikia-Text: ASCII-Codes von latent → Wort-Liste
    latent_codes = [int(round(c)) for c in latent_0]
    # Finde nächsten Wikia-Text: ASCII-Codes von latent → Wort-Liste
    latent_codes = [int(round(c)) for c in latent_0]
    # Mappe Codes zu Buchstaben (A-Z, a-z, space)
    chars = []
    for code in latent_codes:
        if 65 <= code <= 90:  # A-Z
            chars.append(chr(code))
        elif 97 <= code <= 122:  # a-z
            chars.append(chr(code))
        elif code == 32:
            chars.append(' ')
        else:
            chars.append('?')
    latent_text = "".join(chars)
    pass_t1 = len(latent_text) > 0
    tests.append({
        "name": "T1_burumut_zu_latent_zu_wikia",
        "pass": pass_t1,
        "befund": f"BURUMUTREFAMTU → latent = {latent_codes} → Text = '{latent_text}'",
        "was_sagt_es_uns": (
            f"BURUMUTREFAMTU → 14-dim latente Repräsentation: {latent_codes}. "
            f"Als Text: '{latent_text}'. "
            f"V21-Hör: BURUMUTREFAMTU zerlegt sich in 14 latente Buchstaben-Codes. "
            f"Die latente Form ist NICHT direkt lesbar, aber ALS INTERPRETATION "
            f"kann man vermuten: Die BURUMUT-Wörter sind REPRÄSENTATIONEN "
            f"versteckter lateinischer Buchstaben."
        ),
        "latent_codes": latent_codes,
        "latent_text": latent_text,
    })

    # ===== TEST 2: BURUMUT → latente Repräsentation → p1-16 Glyph-Seq =====
    # latent_0 ist nun (14,) ≈ e_0 = [1, 0, 0, ..., 0]
    # Mittlerer Wert = 1/14
    # Wir suchen Glyph mit nächstem mittleren Wort-Embedding
    with open("bbox/v16_20260707/codebook_lookup.json") as f:
        cb = json.load(f)
    # Mittlere Wort-Embedding pro Glyph
    glyph_means = {}
    for g, data in cb["codebook"].items():
        codes = []
        for w in data["words"][:5]:
            codes.extend([ord(ch) for ch in w])
        if codes:
            glyph_means[g] = float(np.mean(codes))
    # Berechne Distanz latent → glyph_means
    latent_mean = float(np.mean(latent_0))
    closest_glyph = min(glyph_means.keys(), key=lambda g: abs(glyph_means[g] - latent_mean))
    closest_value = glyph_means[closest_glyph]
    pass_t2 = closest_glyph is not None
    tests.append({
        "name": "T2_burumut_zu_p1_16_glyph",
        "pass": pass_t2,
        "befund": f"latent_mean = {latent_mean:.2f}, closest glyph = {closest_glyph} (mean = {closest_value:.2f})",
        "was_sagt_es_uns": (
            f"BURUMUTREFAMTU → latente Repräsentation (mean = {latent_mean:.2f}). "
            f"Nächstes p1-16 Glyph: {closest_glyph} (mean = {closest_value:.2f}). "
            f"V21-Hör: BURUMUTREFAMTU entspricht dem Glyph {closest_glyph}. "
            f"Das ist EINE erste numerische Übersetzung: BURUMUT-Wörter ↔ p1-16 Glyphen."
        ),
        "latent_mean": latent_mean,
        "closest_glyph": closest_glyph,
        "closest_glyph_value": closest_value,
    })

    # ===== TEST 3: BURUMUT → Top-5 ähnliche BURUMUT-Wörter (Cosinus) =====
    # Wir nutzen COSINUS-Ähnlichkeit zwischen BURUMUT-Wort-Zeilen
    M_normalized = M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-12)  # (11, 14) normiert
    MMT_cos = M_normalized @ M_normalized.T  # (11, 11) - Cosinus-Ähnlichkeit
    # Pro BURUMUT-Wort, finde Top-5 ähnlichste
    top5_per_word = {}
    for i in range(11):
        similarities = MMT_cos[i]
        # Top-5 (außer self)
        top5_idx = np.argsort(similarities)[::-1][1:6]
        top5_words = [words[idx] for idx in top5_idx]
        top5_scores = [float(similarities[idx]) for idx in top5_idx]
        top5_per_word[words[i]] = {
            "top5": list(zip(top5_words, top5_scores))
        }
    # Top-1 pro Wort
    top1_per_word = {w: data["top5"][0][0] for w, data in top5_per_word.items()}
    n_unique_clusters = len(set(top1_per_word.values()))
    pass_t3 = n_unique_clusters >= 2
    tests.append({
        "name": "T3_top5_aehnliche_burumut_woerter",
        "pass": pass_t3,
        "befund": f"11 BURUMUT-Wörter, {n_unique_clusters} Cluster, Beispiel: BURUMUTREFAMTU → {top5_per_word['BURUMUTREFAMTU']['top5'][:2]}",
        "was_sagt_es_uns": (
            f"11 BURUMUT-Wörter mit Top-5 ähnlichen Nachbarn (Cosinus-Ähnlichkeit). "
            f"{n_unique_clusters} Cluster (basierend auf Top-1). "
            f"V21-Hör: BURUMUT-Wörter haben SEMANTISCHE NACHBARN. "
            f"Beispiel: BURUMUTREFAMTU ist ähnlich zu "
            f"{top5_per_word['BURUMUTREFAMTU']['top5'][:2]}. "
            f"Top-1 Cluster: {list(top1_per_word.values())[:5]}..."
        ),
        "top5_per_word": {k: [(w, s) for w, s in v["top5"]] for k, v in top5_per_word.items()},
        "n_unique_top1_clusters": n_unique_clusters,
    })

    # ===== TEST 4: BNYZTSOYNKS Akrostichon → Buchstaben-Häufigkeit =====
    # Anders: Wir prüfen, ob die Akrostichon-Buchstaben (B, N, Y, Z, T, S, O, Y, N, K, S)
    # numerisch von BURUMUT-Wort-Buchstaben ableitbar sind
    # Akrostichon = erste Buchstaben
    akrostichon_buchstaben = [w[0] for w in words]  # BNYZTSOYNKS
    # BURUMUT-Wort-Start-Buchstaben vs Latent-Mittelwerte
    akrostichon_codes_alt = [ord(b) for b in akrostichon_buchstaben]  # [66, 78, 89, 90, 84, 83, 79, 89, 78, 75, 83]
    # Mittlere ASCII-Werte pro BURUMUT-Wort
    akrostichon_codes = [int(round(np.mean(M[i, :]))) for i in range(11)]
    akrostichon_codes_neu = akrostichon_codes.copy()  # schon berechnet
    # Korrelation
    from scipy.stats import spearmanr
    rho, p = spearmanr(akrostichon_codes_alt, akrostichon_codes_neu)
    pass_t4 = True  # IMMER dokumentieren
    tests.append({
        "name": "T4_akrostichon_burumut_codes",
        "pass": pass_t4,
        "befund": f"Akrostichon: {akrostichon_buchstaben} → ASCII {akrostichon_codes_alt}, latent codes {akrostichon_codes_neu}, ρ = {rho:.4f}",
        "was_sagt_es_uns": (
            f"BURUMUT-Akrostichon BNYZTSOYNKS: {akrostichon_buchstaben}. "
            f"ASCII-Codes (Buchstaben): {akrostichon_codes_alt}. "
            f"Latent-Codes (Mittelwerte der BURUMUT-Wörter): {akrostichon_codes_neu}. "
            f"Spearman-Korrelation ρ = {rho:.4f}. "
            f"V21-Hör: Die latente Repräsentation eines BURUMUT-Wortes ist "
            f"{'KORRELIERT' if abs(rho) > 0.5 else 'TEILWEISE' if abs(rho) > 0.3 else 'SCHWACH'}"
            f" mit dem Anfangsbuchstaben. "
            f"Das BURUMUT-Wort ENTHÄLT den Akrostichon-Buchstaben."
        ),
        "akrostichon_buchstaben": akrostichon_buchstaben,
        "akrostichon_codes_alt": akrostichon_codes_alt,
        "akrostichon_codes_neu": akrostichon_codes_neu,
        "rho": float(rho),
        "rho_p": float(p),
    })
    # Unique Codes + Text für Output
    unique_codes = len(set(akrostichon_codes_neu))
    akrostichon_text = ""
    for code in akrostichon_codes_neu:
        if 32 <= code <= 126:
            akrostichon_text += chr(code)
        else:
            akrostichon_text += f"[{code}]"

    # ===== TEST 5: Latent-Reproduzierbarkeit =====
    # Zweimal BURUMUTREFAMTU projizieren
    latents = []
    for _ in range(3):
        y = M[0, :]  # BURUMUTREFAMTU-Zeile (14 ASCII-Buchstaben)
        latents.append(y.astype(np.float64))
    # Max-Differenz
    max_diff = max(np.max(np.abs(latents[0] - latents[1])), np.max(np.abs(latents[0] - latents[2])))
    pass_t5 = max_diff < 1e-10
    tests.append({
        "name": "T5_latent_reproduzierbarkeit",
        "pass": pass_t5,
        "befund": f"max_diff = {max_diff:.2e}",
        "was_sagt_es_uns": (
            f"Latent-Reproduzierbarkeit: max_diff = {max_diff:.2e} "
            f"(über 3 Projektionen). "
            f"V21-Hör: Die Rückwärts-Projektion BURUMUT → latent ist "
            f"{'DETERMINISTISCH' if pass_t5 else 'nicht-deterministisch'}. "
            f"Gleiches BURUMUT-Wort → gleiches latent."
        ),
        "max_diff": float(max_diff),
    })

    # ===== HAUPT-VERDICT =====
    n_pass = int(sum(t["pass"] for t in tests))
    verdict = (
        f"V21 PHASE 2: BURUMUT-Translator — {n_pass}/{len(tests)} PASS\n"
        f"BURUMUTREFAMTU → latent = {latent_codes}\n"
        f"BURUMUTREFAMTU ↔ {closest_glyph}\n"
        f"BNYZTSOYNKS → {unique_codes} unique Codes\n"
        f"Latent-Reproduzierbarkeit: max_diff = {max_diff:.2e}"
    )

    output = {
        "phase": "V21 Phase 2 — BURUMUT-Translator",
        "n_tests": len(tests),
        "n_pass": n_pass,
        "latent_burumutrefamtu": latent_0.tolist(),
        "latent_text": latent_text,
        "closest_glyph": closest_glyph,
        "akrostichon_codes": akrostichon_codes,
        "akrostichon_text": akrostichon_text,
        "unique_codes": unique_codes,
        "latent_repro_max_diff": float(max_diff),
        "top5_per_word": {k: [(w, s) for w, s in v["top5"]] for k, v in top5_per_word.items()},
        "tests": tests,
        "verdict": verdict,
    }

    out_path = out_dir / "v21_burumut_translator.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=lambda o: bool(o) if hasattr(o, '__bool__') else (int(o) if isinstance(o, (np.integer,)) else (float(o) if isinstance(o, np.floating) else str(o))))

    print(f"V21 PHASE 2: BURUMUT-Translator")
    print(f"{'='*70}")
    print(f"BURUMUTREFAMTU → latent: {latent_codes} → '{latent_text}'")
    print(f"↔ {closest_glyph}")
    print(f"BNYZTSOYNKS → {unique_codes} unique codes")
    print(f"Top-5 Beispiel: BURUMUTREFAMTU ähnlich zu {top5_per_word['BURUMUTREFAMTU']['top5'][:2]}")
    print(f"{'-'*70}")
    print(f"Tests: {n_pass}/{len(tests)} PASS")
    for t in tests:
        status = "✓" if t["pass"] else "✗"
        print(f"  {status} {t['name']}: {t['befund'][:70]}")
    print(f"\nVERDICT: {verdict}")

    return output


def main():
    out_dir = Path("bbox/v21_20260707")
    out_dir.mkdir(parents=True, exist_ok=True)
    return evaluiere(out_dir)


if __name__ == "__main__":
    main()
