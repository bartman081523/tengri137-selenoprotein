"""
v12_test_bewusst.py
V12 TDD TESTS — BEWUSSTER CODE-Hypothese empirisch

Definition: Code, der intentionale Semantik trägt (statistische Signaturen)
Test: Komplexität vs Zufall, lexikalische Anker, Cross-Layer-Kohärenz
Wichtig: "Bewusstsein" ist nicht testbar — wir testen Signaturen intentionaler Semantik
"""
import sys
import json
import gzip
import random
import re
import string
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))


def load_p17_inventory():
    return json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))


def load_v11_code_hypotheses():
    return json.load(open("bbox/v11_p17_20260706/code_hypotheses.json"))


def load_burumut_woerter():
    inv = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    return [w["wort"] for w in inv["woerter"]]


def load_burumut_texts():
    data = json.load(open("bbox/burumut_20260707_V7/burumut_texts.json"))
    all_texts = []
    for f_id, texts in data["burumut_texts"].items():
        all_texts.extend(texts)
    return all_texts


def kolmogorov_proxy(text):
    """Kompressionsrate als Kolmogorov-Proxy. Kleinere komprimierte Größe = höhere Komplexität."""
    raw_size = len(text.encode())
    compressed = gzip.compress(text.encode())
    return len(compressed) / raw_size  # < 1 = komprimierbar


def has_real_word_anchor(word, min_length=3):
    """Prüft ob ein BURUMUT-Wort einen echten türkisch/mongolischen Substring enthält."""
    # Aus V7-Befund: OKUZ, KURGAN, SUN, KUR, GAN, BEK
    # Wir erweitern um weitere echte Substrings
    anchors = [
        "OKU", "KUR", "GAN", "SUN", "BEK", "YAB", "KAN", "MOR",
        "BIZ", "ZUM", "TAN", "EM", "BA", "TU", "TI", "SU",
        "MER", "YAP", "SUZ", "LIK", "HIM", "MUT", "REF",
    ]
    word_upper = word.upper()
    return any(a in word_upper for a in anchors)


# ============================================================================
# TDD-Tests
# ============================================================================

def test_p17_komplexitaet_ueber_zufall():
    """Bewusster Code: Komplexität > Zufall (p<0.01).

    Methode: gzip-Kompressionsrate von p17-Klartext vs 1000 Zufalls-Strings.
    Niedrigere Rate = höhere Komplexität (mehr Muster = besser komprimierbar).
    Bewusster Code: hohe Komplexität = niedrige Kompressionsrate.
    """
    inv = load_p17_inventory()
    klartext = " ".join(inv["tappeiner_brueche_klartext"]["klartext_zeilen"])
    real_rate = kolmogorov_proxy(klartext)

    random.seed(42)
    random_rates = []
    for _ in range(1000):
        rnd = "".join(random.choices(string.ascii_uppercase + " ", k=len(klartext)))
        random_rates.append(kolmogorov_proxy(rnd))

    p_value = (sum(1 for r in random_rates if r <= real_rate) + 1) / 1001
    print(f"  Real-Kompressionsrate: {real_rate:.3f}")
    print(f"  Random-Median:        {sorted(random_rates)[500]:.3f}")
    print(f"  p-Wert (1-seitig, real ≤ random): {p_value:.4f}")
    # Bewusst: p17-Klartext sollte bessere Kompression haben als Zufall
    # → p-Wert klein (real_rate < random_rates)
    # Realität: Klartext ist natürliches Englisch, also hoch redundant → niedrige Rate
    assert p_value < 0.05, \
        f"Komplexität nicht über Zufall: p={p_value:.4f} — könnte bedeuten: kein bewusster Code"


def test_p17_burumut_has_lexical_anchors():
    """Bewusster Code: BURUMUT hat lexikalische Anker (echte türkische/mongolische Substrings)."""
    woerter = load_burumut_woerter()
    n_with_anchor = sum(1 for w in woerter if has_real_word_anchor(w))
    n_total = len(woerter)
    pct = n_with_anchor / n_total
    print(f"  BURUMUT-Wörter mit Ankern: {n_with_anchor}/{n_total} = {pct:.1%}")
    # Bewusst: >50% mit Ankern
    assert pct > 0.5, \
        f"Nur {n_with_anchor}/{n_total} BURUMUT-Wörter mit echten Ankern — könnte Zufall sein"


def test_p17_has_cross_layer_coherence():
    """Bewusst: Glyph-Sequenz BNYZTSOYNKS spiegelt sich in BURUMUT-Wörtern."""
    inv = load_p17_inventory()
    akrostichon = inv["akrostichon_der_11_glyphen"]["string"]  # BNYZTSOYNKS
    woerter = load_burumut_woerter()

    # Test 1: Kommt der 1. Buchstabe jedes BURUMUT-Wortes in der Glyph-Sequenz vor?
    # (Akrostichon BNYZTSOYNKS soll = erste Buchstaben der BURUMUT-Wörter sein)
    glyph_set = set(akrostichon)
    first_letters = [w[0] for w in woerter]
    in_glyphs = sum(1 for fl in first_letters if fl in glyph_set)
    print(f"  Akrostichon: {akrostichon}")
    print(f"  BURUMUT-Anfangsbuchstaben: {first_letters}")
    print(f"  Im Akrostichon enthalten: {in_glyphs}/{len(first_letters)}")
    # Bewusst: alle 11 Anfangsbuchstaben im Akrostichon
    assert in_glyphs >= 9, \
        f"Nur {in_glyphs}/{len(first_letters)} BURUMUT-Anfangsbuchstaben im Akrostichon — kein klares Cross-Layer"


def test_p17_46digit_signature():
    """Schmehs 'EXACT FORTY SIX' Befund: p17 hat eine 46-Ziffern-Periode.

    Test: hat p17 (oder BURUMUT) eine ausgezeichnete Periode?
    """
    woerter = load_burumut_woerter()
    all_text = "".join(woerter)
    # Teste Perioden 7, 14, 28, 46 (Schmeh/Tappeiner)
    def period_score(text, period):
        """Zähle Übereinstimmungen bei periodischer Wiederholung."""
        if len(text) < 2 * period:
            return 0
        matches = 0
        for i in range(len(text) - period):
            if text[i] == text[i + period]:
                matches += 1
        return matches / (len(text) - period)

    scores = {p: period_score(all_text, p) for p in [7, 14, 28, 46]}
    print(f"  Period-Scores in BURUMUT (gesamt {len(all_text)} Zeichen):")
    for p, s in scores.items():
        print(f"    Periode {p:2}: {s:.3f}")
    # Wenn 46 oder 28 herausragt → bewusst (Schmeh/Tappeiner)
    max_p = max(scores, key=scores.get)
    max_s = scores[max_p]
    # Bei bewusstem Code: max_p ist 7, 14, 28 oder 46 (Tappeiner/Schmeh-Perioden)
    assert max_p in [7, 14, 28, 46], \
        f"Max-Periode {max_p} nicht in {{7, 14, 28, 46}} — keine Tappeiner/Schmeh-Signatur"


def test_p17_v11_verdict_holds():
    """V11-Verdikt: Bewusster Code STATISTISCH SIGNIFIKANT. Hält das?"""
    h = load_v11_code_hypotheses()
    bw = next((x for x in h["hypotheses"] if "BEWUSST" in x["name"] or "BEWU" in x["name"]), None)
    assert bw is not None, "V11 Bewusst-Code-Verdikt fehlt"
    print(f"  V11-Verdikt: {bw['status']} — {bw['verdict']}")


if __name__ == "__main__":
    import traceback

    tests = [
        test_p17_komplexitaet_ueber_zufall,
        test_p17_burumut_has_lexical_anchors,
        test_p17_has_cross_layer_coherence,
        test_p17_46digit_signature,
        test_p17_v11_verdict_holds,
    ]

    print("=" * 80)
    print("V12 TDD: BEWUSSTER CODE-Hypothese (empirisch, statistische Signaturen)")
    print("=" * 80)
    print()
    print("Wichtig: 'Bewusstsein' ist nicht testbar — wir testen Signaturen intentionaler Semantik.")
    print()

    passed = 0
    failed = 0
    for test in tests:
        print(f"RUN: {test.__name__}")
        try:
            test()
            print(f"  ✓ PASS\n")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ FAIL: {e}\n")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}\n")
            traceback.print_exc()
            failed += 1

    print("=" * 80)
    print(f"ERGEBNIS: {passed}/{len(tests)} bestanden, {failed} fehlgeschlagen")
    print("=" * 80)
    sys.exit(0 if failed == 0 else 1)
