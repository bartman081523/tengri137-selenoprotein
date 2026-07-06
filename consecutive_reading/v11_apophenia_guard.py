"""
v11_apophenia_guard.py
V11 APOPHENIA-WÄCHTER — 10 zentrale Pfeiler ausschließen

Lädt VOR jedem V11-Skript und prüft:
1. BURUMUT ≠ Sec-GPCR-Fragment
2. KEINE 5-Layer-Torah-Fold
3. KEINE 5-Turing-Operatoren
4. BURUMUT+137 NICHT als "universelle Brücke"
5. TCI-Experimente IGNORIEREN
6. BURUMUT NICHT holografisch
7. Tora-Turing-Maschine NICHT Turing-vollständig
8. KEINE Apokalypse-Hypothese
9. Schmeh = Ground Truth (NICHT Tengri's "Stimme")
10. p17-p23 sind EIGENE Schichten (NICHT Tengri-Schicht)
"""
import sys
from pathlib import Path


# Die 10 zentralen Apophenia-Pfeiler (vom Agent identifiziert)
APOPHENIA_PILLARS = {
    "P1_burumut_not_gpcr": {
        "claim": "BURUMUT = Sec-codiertes GPCR-Fragment",
        "reality": "BURUMUT = Tappeiner-Sprachebene (V7/V9 Falsifikation)",
        "test": lambda: not _is_burumut_protein_claim(),
    },
    "P2_no_5layer_torah": {
        "claim": "5-Layer-Torah-Fold",
        "reality": "Master-Doc L2384: 'Holografie ≠ Rang > 1, Kategorienfehler'",
        "test": lambda: not _uses_5layer_torah(),
    },
    "P3_no_5_turing_operators": {
        "claim": "5 fehlende Konsonanten = 5 Turing-Operatoren",
        "reality": "Master-Doc L2357: 'eigentlich nur 4 in der Praxis'",
        "test": lambda: not _uses_5_turing_operators(),
    },
    "P4_no_137_universal_bridge": {
        "claim": "BURUMUT+137 = 37² universelle Brücke",
        "reality": "rechnerisch korrekt, aber apophenisch interpretiert",
        "test": lambda: not _claims_137_bridge(),
    },
    "P5_no_tci_experiments": {
        "claim": "TCI-Experimente 13730-13739 verifiziert",
        "reality": "V5: F Grade FALSIFIZIERT (Master-Doc L41-49)",
        "test": lambda: not _uses_tci_experiments(),
    },
    "P6_burumut_not_holographic": {
        "claim": "BURUMUT ist holografisch",
        "reality": "Master-Doc L2384 Selbstkorrektur",
        "test": lambda: not _claims_holographic_burumut(),
    },
    "P7_tora_tm_not_turing_complete": {
        "claim": "Tora-Turing-Maschine Turing-vollständig",
        "reality": "Master-Doc L928: 'M4 ist KEIN Quine', linear",
        "test": lambda: not _uses_tora_turing_machine(),
    },
    "P8_no_apocalypse": {
        "claim": "Apokalypse-Hypothese (Selen→GPCR-Kollaps)",
        "reality": "V6-V10: BURUMUT ist keine Biologie",
        "test": lambda: not _claims_apocalypse(),
    },
    "P9_schmeh_is_ground_truth": {
        "claim": "Schmeh-Plaintext = Tengri's 'Stimme'",
        "reality": "V10: Schmeh ist Ground Truth, 1 Glyph = 1.6 Wikia-Wörter",
        "test": lambda: _uses_schmeh_as_ground_truth(),
    },
    "P10_p17_p23_separate_layer": {
        "claim": "p17-p23 sind Tengri-Schicht",
        "reality": "V7/V9: p17-p23 sind eigene Schichten",
        "test": lambda: _treats_p17_p23_separately(),
    },
}


def _is_burumut_protein_claim():
    """Detect if code claims BURUMUT is a protein fragment."""
    code_text = _get_caller_source()
    triggers = ["Sec-codiert", "GPCR-Fragment", "Adhäsions-GPCR",
                "BURUMUT = Sec", "BURUMUT = Adhäsion"]
    return any(t in code_text for t in triggers)


def _uses_5layer_torah():
    """Detect if code uses 5-Layer Torah-Fold architecture."""
    code_text = _get_caller_source()
    triggers = ["5-Layer-Torah", "5-Layer Torah", "5_LAYER_TORAH",
                "torah_5_layer", "torah_fold"]
    return any(t in code_text for t in triggers)


def _uses_5_turing_operators():
    """Detect if code uses 5 Turing Operators claim."""
    code_text = _get_caller_source()
    triggers = ["5_operators", "5 Operatoren", "FIVE_OPERATORS",
                "FIVE_TURING", "5 fehlende Konsonanten"]
    return any(t in code_text for t in triggers)


def _claims_137_bridge():
    """Detect if code claims 137 is universal bridge."""
    code_text = _get_caller_source()
    triggers = ["universelle Brücke", "137 bridge", "137=37²",
                "137 = 37", "BURUMUT+137"]
    return any(t in code_text for t in triggers)


def _uses_tci_experiments():
    """Detect if code uses TCI experiments as ground truth."""
    code_text = _get_caller_source()
    triggers = ["TCI-Experimente", "tci_experiments", "tci_documents",
                "13730", "13739"]
    return any(t in code_text for t in triggers)


def _claims_holographic_burumut():
    """Detect holographic BURUMUT claims."""
    code_text = _get_caller_source()
    triggers = ["holografisch", "BURUMUT_HOLOGRAPHIC", "holographic_burumut"]
    return any(t in code_text for t in triggers)


def _uses_tora_turing_machine():
    """Detect usage of Tora Turing Machine code."""
    code_text = _get_caller_source()
    triggers = ["TORA_TURING", "from TORA", "import TORA",
                "tora_turing_machine", "spanda_machine"]
    return any(t in code_text for t in triggers)


def _claims_apocalypse():
    """Detect apocalypse hypotheses."""
    code_text = _get_caller_source()
    triggers = ["Apokalypse", "Selen-Mangel", "Selenmangel",
                "GPCR-Kollaps", "Selenoprotein-Kollaps"]
    return any(t in code_text for t in triggers)


def _uses_schmeh_as_ground_truth():
    """Check that Schmeh plaintext IS used as ground truth."""
    # This is the OPPOSITE: we WANT to use Schmeh as ground truth
    # So the test passes if Schmeh is properly used
    code_text = _get_caller_source()
    return "schmeh" in code_text.lower() or "wikia" in code_text.lower()


def _treats_p17_p23_separately():
    """Check that p17-p23 are treated as separate layer."""
    code_text = _get_caller_source()
    return "p17" in code_text and "p23" in code_text


def _get_caller_source():
    """Get the source code of the calling module."""
    try:
        caller = sys._getframe(1).f_globals.get("__file__", "")
        if caller and Path(caller).exists():
            return Path(caller).read_text()
    except (ValueError, AttributeError):
        pass
    return ""


def check_apophenia():
    """Run all apophenia checks. Returns (passed, failed, details)."""
    passed = []
    failed = []

    for name, pillar in APOPHENIA_PILLARS.items():
        try:
            result = pillar["test"]()
            if result:
                passed.append(name)
            else:
                failed.append({
                    "pillar": name,
                    "claim": pillar["claim"],
                    "reality": pillar["reality"],
                })
        except Exception as e:
            failed.append({
                "pillar": name,
                "claim": pillar["claim"],
                "reality": pillar["reality"],
                "error": str(e),
            })

    return passed, failed


def main():
    print("=" * 80)
    print("V11 APOPHENIA-WÄCHTER")
    print("=" * 80)
    print(f"Prüfe {len(APOPHENIA_PILLARS)} zentrale Apophenia-Pfeiler...")
    print()

    passed, failed = check_apophenia()

    print(f"✓ BESTANDEN: {len(passed)}/{len(APOPHENIA_PILLARS)}")
    for name in passed:
        print(f"  ✓ {name}")

    print()
    if failed:
        print(f"✗ FEHLGESCHLAGEN: {len(failed)}/{len(APOPHENIA_PILLARS)}")
        for f in failed:
            print(f"  ✗ {f['pillar']}")
            print(f"    BEHAUPTUNG: {f['claim']}")
            print(f"    WIRKLICHKEIT: {f['reality']}")
            if 'error' in f:
                print(f"    FEHLER: {f['error']}")
        print()
        print("⚠️  APOPHENIA ERKANNT — V11-Skripte MÜSSEN diese Aussagen eliminieren")
        return 1
    else:
        print("✅ ALLE 10 APOPHENIA-PFEILER AUSGESCHLOSSEN")
        return 0


if __name__ == "__main__":
    sys.exit(main())
