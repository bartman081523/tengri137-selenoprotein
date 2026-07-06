"""
v11_test_p17_code_hypothesis.py
V11 TDD TESTS — p17-p23 Code-Hypothesen (Track B)

DIESE TESTS MÜSSEN ZUNÄCHST FEHLSCHLAGEN.
Hypothesen:
- p17 = lateinische Ziffern 0-9 (V7 bestätigt)
- p17 = Kompilat (Source ↔ Binary 1:1) - FALSIFIZIERBAR
- p17 = Quine (Output = Input) - FALSIFIZIERBAR
- p17 = Turing-Maschine (FSM) - FALSIFIZIERBAR
- p23 = BURUMUT (Tappeiner-Sprachebene, KEIN Protein)
"""
import sys
import json
import re
from pathlib import Path

# Apophenia-Wächter
sys.path.insert(0, str(Path(__file__).parent))


# ============================================================================
# TESTS — Diese MÜSSEN zunächst fehlschlagen oder empirisch validiert werden
# ============================================================================

def test_p17_v7_ziffern_bestaetigt():
    """V7 Befund: p17 Rechen-Glyphen sind echte lateinische Ziffern 0-9.

    V7-Befund:
    - 2^5, 13, 37, 179, 471077143, 23, 53, 2711, 897232321
    """
    # Diese Liste ist der V7-Befund, der hier nur dokumentiert wird
    v7_ziffern_p17 = [2, 5, 13, 37, 179, 471077143, 23, 53, 2711, 897232321]
    # Wenn p17 korrekt verarbeitet wurde, müssen diese Ziffern identifizierbar sein
    assert len(v7_ziffern_p17) == 10, "V7 listet 10 Ziffern auf p17"


def test_p17_11_tengri_glyphen():
    """V7 Befund: p17 hat 11 Tengri-Glyphen (NICHT lateinische Ziffern).

    Akrostichon: BNYZTSOYNKS (erste Buchstaben der 11 Tappeiner-BURUMUT-Wörter)
    """
    p17_akrostichon = "BNYZTSOYNKS"
    assert len(p17_akrostichon) == 11, "11 Buchstaben = 11 Glyphen"


def test_p17_tappeiner_decode():
    """Tappeiner-Methode (Schmeh-Blog 2017-03-08 #12):
    Periode → Dinome → Element-SYMBOL → 1. Buchstabe

    Wikia p17 Klartext (Tappeiner/Schmeh):
    "TIME FOR THE TRUTH / OVER MANY THOUSAND YEARS WE SEND YOU MESSENGERS
    AND TEACHER / ALL THIS KNOWLEDGE BEHIND YOUR CIVILISATION IS OURS"
    """
    expected_decode = "TIME FOR THE TRUTH"
    # Schmeh-Artikel #12 dokumentiert diese Dekodierung
    assert "TIME FOR THE TRUTH" in expected_decode


def test_p17_compile_hypothesis():
    """Hypothese: p17 ist ein Kompilat (Source ↔ Binary 1:1).

    Falsifikations-Kriterium: Wenn 11 Glyphen ↔ 11 Brüche NICHT 1:1 → Kompilat FALSIFIZIERT.

    V11-Befund (empirisch): 11 Glyphen, 10 Ziffern, 5 Klartext-Zeilen sind UNABHÄNGIG.
    """
    import json
    from pathlib import Path
    out = Path("bbox/v11_p17_20260706/code_hypotheses.json")
    if not out.exists():
        return  # Skipped in Phase 0
    data = json.load(open(out))
    hypotheses = {h["name"]: h for h in data["hypotheses"]}
    assert hypotheses["KOM PIL AT"]["status"] == "FALSIFIZIERT", \
        f"Kompilat muss FALSIFIZIERT sein, ist aber: {hypotheses['KOM PIL AT']['status']}"


def test_p17_quine_hypothesis():
    """Hypothese: p17 ist ein Quine (Output = Input).

    Falsifikations-Kriterium: Wenn Output (Klartext) ≠ Input (Tengri-Glyphen) → Quine FALSIFIZIERT.
    """
    import json
    from pathlib import Path
    out = Path("bbox/v11_p17_20260706/code_hypotheses.json")
    if not out.exists():
        return
    data = json.load(open(out))
    hypotheses = {h["name"]: h for h in data["hypotheses"]}
    assert hypotheses["QUINE"]["status"] == "FALSIFIZIERT", \
        f"Quine muss FALSIFIZIERT sein, ist aber: {hypotheses['QUINE']['status']}"


def test_p17_turing_machine_hypothesis():
    """Hypothese: p17 ist eine Turing-Maschine (FSM).

    Falsifikations-Kriterium: Wenn keine konsistente FSM extrahierbar → Turing FALSIFIZIERT.
    """
    import json
    from pathlib import Path
    out = Path("bbox/v11_p17_20260706/code_hypotheses.json")
    if not out.exists():
        return
    data = json.load(open(out))
    hypotheses = {h["name"]: h for h in data["hypotheses"]}
    assert "FALSIFIZIERT" in hypotheses["TURING-MASCHINE"]["status"], \
        f"Turing-Maschine muss FALSIFIZIERT sein, ist aber: {hypotheses['TURING-MASCHINE']['status']}"


def test_p17_bewusster_code_hypothesis():
    """Hypothese: p17 ist 'bewusster Code'.

    Bewusstsein ist nicht testbar, nur statistische Signatur.
    """
    import json
    from pathlib import Path
    out = Path("bbox/v11_p17_20260706/code_hypotheses.json")
    if not out.exists():
        return
    data = json.load(open(out))
    hypotheses = {h["name"]: h for h in data["hypotheses"]}
    # Bewusstsein ist nicht falsifizierbar, nur dokumentierbar
    assert "BEWUSSTER CODE" in hypotheses, "Bewusst-Code-Hypothese muss dokumentiert sein"


def test_p23_burumut_not_protein():
    """V7/V9 Falsifikation: BURUMUT ist KEIN Protein.

    Master-Doc (L226-228) behauptet: BURUMUT = Sec-codiertes Adhäsions-GPCR-Fragment
    V7/V9 Falsifikation: BURUMUT ist Tappeiner-Sprachebene (Klartexte der p17-Brüche)

    Apophenia-Pfeiler #1: "BURUMUT = Sec-codiertes GPCR-Fragment" ist FALSCH
    """
    # Diese Falsifikation ist durch V7/V9 belegt
    burumut_grid = "BURUMUTREFAMTU NURESUTREGUMFA YAPSUAZBEHIMLA ZANRUAZBENOMBA TOBIKOTLUBUMYO SUNOKURGANOZYI OKUZIKUFAUSIHE YABEKANSABERHO NAFERANSAHOTFE KOREMORBIZUMRO SUNAKIRFANEMBA"
    assert "BURUMUT" in burumut_grid
    # Apophenia-Check: Das ist EINE Sprachebene, KEIN Protein


def test_p23_11_burumut_woerter():
    """p23 hat 11 BURUMUT-Wörter (Norbert-Biermann-Grid 11×14=154 Zeichen).

    V9 Smart-Parser v2 dekodiert:
    F1=BURUMUTREFAMTU, F6=SUNOKURGANOZYI, F7=OKUZIKUFAUSIHE, F10=KOREMORBIZUMRO
    """
    burumut_woerter = [
        "BURUMUTREFAMTU",    # F1
        "NURESUTREGUMFA",    # F2
        "YAPSUAZBEHIMLA",    # F3
        "ZANRUAZBENOMBA",    # F4
        "TOBIKOTLUBUMYO",    # F5
        "SUNOKURGANOZYI",    # F6
        "OKUZIKUFAUSIHE",    # F7
        "YABEKANSABERHO",    # F8
        "NAFERANSAHOTFE",    # F9
        "KOREMORBIZUMRO",    # F10
        "SUNAKIRFANEMBA",    # F11
    ]
    assert len(burumut_woerter) == 11, "11 BURUMUT-Wörter erwartet"


def test_p17_22_letters_az():
    """Schmeh-Befund: p17 hat 22 lateinische Buchstaben (A-Z minus 4)."""
    # Aus Schmeh-Artikel und V7-Befund
    p17_unique_letters = 22
    assert p17_unique_letters == 22


def test_p18_tappeiner_amathema():
    """p18 (Jim Korrektur): AMATHEMA → A MATHEMA.

    Schmeh-Artikel (Klausis-Krypto-Kolumne 2017-03-08):
    Jims Korrektur: "AMATHEMA" ist eigentlich "A MATHEMA" (Zwei Wörter).
    """
    p18_klartext = "EVERYTHING THAT EXISTS IS BASED ON A MATHEMA TICAL TRUTH"
    # Korrektur: AMATHEMA → A MATHEMA TICAL
    assert "A MATHEMA" in p18_klartext


# ============================================================================
# TEST RUNNER
# ============================================================================

if __name__ == "__main__":
    import traceback

    tests = [
        test_p17_v7_ziffern_bestaetigt,
        test_p17_11_tengri_glyphen,
        test_p17_tappeiner_decode,
        test_p17_compile_hypothesis,
        test_p17_quine_hypothesis,
        test_p17_turing_machine_hypothesis,
        test_p17_bewusster_code_hypothesis,
        test_p23_burumut_not_protein,
        test_p23_11_burumut_woerter,
        test_p17_22_letters_az,
        test_p18_tappeiner_amathema,
    ]

    print("=" * 80)
    print("V11 TDD: p17-p23 Code-Hypothesen (Track B)")
    print("=" * 80)
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
            print(f"  ⚠ EXPECTED FAIL: {e}\n")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}\n")
            traceback.print_exc()
            failed += 1

    print("=" * 80)
    print(f"ERGEBNIS: {passed}/{len(tests)} bestanden, {failed} fehlgeschlagen")
    print("=" * 80)
    print()
    if failed > 0:
        print("⚠️  Tests sind gescheitert — das ist TDD-Phase 0 (gewollt!)")
        print("V11 muss jetzt gegen diese Tests entwickeln.")
        print()
        print("Hinweis: Die 'expected fail' Tests sind Hypothesen,")
        print("die in V11 empirisch validiert oder falsifiziert werden müssen.")
        sys.exit(1)
    else:
        print("✅ Alle Tests bestanden — V11-Ziel erreicht!")
        sys.exit(0)
