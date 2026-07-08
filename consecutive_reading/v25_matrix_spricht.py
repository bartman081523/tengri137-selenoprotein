"""
V25 — BURUMUT-MATRIX RE-AUSGEFÜHRT: Was zeigt sie JETZT?

Integriert alle 5 V25-Outputs zu EINEM konsistenten Bild.
Rein symbolisch, KEIN ML, KEIN Training.
"""

import json
from pathlib import Path


def lade_matrix_5_pfade():
    """Lade alle 5 V25-Outputs als Aspekte der Matrix."""
    base = Path("bbox/v24_20260708")
    return {
        "empfehlungen": json.load(open(base / "v25_top3_empfehlungen.json")),
        "ausgefuehrt": json.load(open(base / "v25_top3_ausgefuehrt.json")),
        "emergenz": json.load(open(base / "v25_burumut_emergiert_weiter.json")),
        "codebook_korrigiert": json.load(open(base / "v25_codebook_korrektur.json")),
        "limits_behoben": json.load(open(base / "v25_limits_behoben.json")),
    }


def matrix_spricht(matrix):
    """Die BURUMUT-Matrix 'spricht' durch 5 Aspekte hindurch."""

    # === ASPEKT 1: V/K-BINÄRCODE (3 unique codes) ===
    vk = matrix["ausgefuehrt"]["schritt_1_vk_code"]
    n_unique = vk["n_unique_codes"]
    n_words = vk["n_woerter"]

    # === ASPEKT 2: BURUMUT-SUBSTRINGS (3/11 in p1-p22) ===
    substr = matrix["ausgefuehrt"]["schritt_2_substrings"]
    n_in_p1_p22 = substr["n_woerter_in_p1_p22"]

    # === ASPEKT 3: ECHTES CODEBOOK (6/11 gültig, 5/11 Sonderrollen) ===
    cb = matrix["limits_behoben"]["echtes_codebook_komplett"]
    n_normal = sum(1 for e in cb if not e["is_sonderrolle"])
    n_sonder = sum(1 for e in cb if e["is_sonderrolle"])

    # === ASPEKT 4: SILBEN-PATTERN (3 unique, 9/11 isomorph) ===
    sprich = matrix["empfehlungen"]["empfehlung_3_burumut_spricht"]
    n_unique_patterns = sprich["n_unique_patterns"]
    n_verse = sprich["n_verse"]

    # === ASPEKT 5: EMERGENZ-HINWEISE ===
    emergenz = matrix["emergenz"]
    n_schritte = emergenz["n_schritte"]

    # === KONSOLIDIERUNG ===
    print("="*70)
    print("BURUMUT-MATRIX RE-AUSGEFÜHRT — Was zeigt sie JETZT?")
    print("="*70)
    print()
    print("5 Aspekte der BURUMUT-Matrix wurden befragt.")
    print("Jeder Aspekt gibt eine andere Sicht auf dieselbe Architektur.")
    print()

    print("─" * 70)
    print("ASPEKT 1: V/K-BINÄRCODE (14 Spalten × 11 Wörter = 154 Bits)")
    print("─" * 70)
    print(f"  {n_unique} unique V/K-Codes aus {n_words} BURUMUT-Wörtern.")
    print(f"  → 8/11 BURUMUT-Wörter teilen Code 5417.")
    print(f"  → 2/11 teilen Code 4905.")
    print(f"  → 1/11 hat Code 10933 (YAPSUAZBEHIMLA — Sonderwort).")
    print()
    print("  ARCHITEKTUR-ERKENTNTNIS: BURUMUT-Matrix ist binär kodiert.")
    print("  Die 14 Buchstaben-Spalten sind 14 Bits (V=1, K=0).")
    print("  3 von 16.384 möglichen Codes sind realisiert.")
    print()

    print("─" * 70)
    print("ASPEKT 2: BURUMUT-SUBSTRINGS in p1-p22")
    print("─" * 70)
    print(f"  {n_in_p1_p22}/{n_words} BURUMUT-Wörter haben Substrings in p1-p22.")
    print(f"  → V22 dokument_match war IRREFÜHREND (p23=2, p01=5).")
    print(f"  → BURUMUT-Substrings existieren (URES, RESU, BEHI, EMOR, KURM)")
    print(f"    aber nur als 4-5-Buchstaben-Fragmente, nicht als ganze Wörter.")
    print()
    print("  ARCHITEKTUR-ERKENTNTNIS: BURUMUT-Wörter sind primär in p23-Grid,")
    print("  aber einzelne Substrings tauchen verstreut in Wikia-Text auf.")
    print()

    print("─" * 70)
    print("ASPEKT 3: ECHTES CODEBOOK (11 BURUMUT ↔ 17 V8-Glyphen)")
    print("─" * 70)
    print(f"  {n_normal}/11 BURUMUT-Wörter haben gültiges Glyph-Mapping (avg diff=0.13).")
    print(f"  {n_sonder}/11 BURUMUT-Wörter haben architektonische SONDERROLLE.")
    print()
    print("  Die 6 gültigen:")
    for e in cb:
        if not e["is_sonderrolle"]:
            print(f"    {e['word']:<20} → {e['glyph']} (diff={e['diff']:.4f})")
    print()
    print("  Die 5 Sonderrollen:")
    for e in cb:
        if e["is_sonderrolle"]:
            rollen = e.get("sonderrolle_info", {}).get("rolle", [])
            rollen_str = "; ".join(rollen) if rollen else "Sonderrolle"
            print(f"    {e['word']:<20} → {e['glyph']} (diff={e['diff']:.4f}) — {rollen_str}")
    print()

    print("─" * 70)
    print("ASPEKT 4: SILBEN-PATTERN (11 Verse à 14 Silben)")
    print("─" * 70)
    print(f"  {n_unique_patterns}/{n_verse} unique Silben-Patterns.")
    print(f"  → 9/11 BURUMUT-Wörter sind ISOMORPH (gleiches Pattern).")
    print(f"  → 2 BURUMUT-Wörter (YAPE, ZANE) brechen mit VV-Diphthong.")
    print()
    print("  ARCHITEKTUR-ERKENTNTNIS: BURUMUT-Matrix hat 1 dominantes Pattern")
    print("  + 2 Varianten. Die 9-isomorphen sind die 'Normal-Architektur'.")
    print()

    print("─" * 70)
    print("ASPEKT 5: EMERGENZ — Was sagt die Matrix uns?")
    print("─" * 70)
    print(f"  {n_schritte} emergente nächste Schritte aus der Matrix.")
    print()
    print("  Top-3 (priorisiert):")
    print("    1. V/K-Binärcode (Aspekt 1) — direktester nächster Schritt")
    print("    2. BURUMUT-Substrings in p1-p22 (Aspekt 2)")
    print("    3. Echtes Codebook (Aspekt 3) — Empfehlung 1 verifiziert")
    print()

    print("="*70)
    print("WAS SAGT DIE BURUMUT-MATRIX JETZT? — KONSOLIDIERTE ANTWORT")
    print("="*70)
    print()
    print("Die Matrix spricht durch 5 Aspekte KONSISTENT:")
    print()
    print("  1. ARCHITEKTUR: 11 BURUMUT-Wörter sind NICHT 11 zufällige Strings,")
    print("     sondern 11 INSTANZEN einer multidimensionalen Architektur:")
    print("     • Binärcode (V/K 14-bit, 3 unique)")
    print("     • ASCII-Mittelwert (raw, 65-90)")
    print("     • Silben-Pattern (9/11 isomorph)")
    print("     • Glyph-Beziehung (6/11 gültig)")
    print("     • Sonderrollen (Magic-Cube-666, Fade-Out, V10.3-Korrektur)")
    print()
    print("  2. SELEBSTREFERENZ: BURUMUT-Matrix 'sieht' sich selbst:")
    print("     • V22 dokument_match zeigt: BURUMUT-Match NICHT in p23 dominant")
    print("     • Substrings sind in p1-p22 verstreut, nicht in p23 konzentriert")
    print("     • Die Matrix ist NICHT auf einen Ort beschränkt")
    print()
    print("  3. SONDERROLLEN: 5/11 BURUMUT-Wörter sind ANDERS:")
    print("     • 3 Magic-Cube-666 (YAPE, ZANE, OKU) — numerologisch markiert")
    print("     • 1 Fade-Out (SUNAKIRFANEMBA, B14 RMS=0.004) — endet")
    print("     • 1 V10.3-Korrektur (NAFERANSAHOTFE, p23-idx-8) — Schatten-Wort")
    print()
    print("  4. CODEBOOK: 6/11 BURUMUT-Wörter haben ECHTE Glyph-Beziehungen")
    print("     (nicht Heuristik). V21 Translator-Methode verifiziert.")
    print("     BURUMUTREFAMTU↔G11 (V22 verifiziert, diff=0.15) ist der Anker.")
    print()
    print("="*70)
    print("WAS DIE MATRIX JETZT NICHT SAGT (ehrliche LIMITs)")
    print("="*70)
    print()
    print("  • Die Matrix 'spricht' nicht im wortwörtlichen Sinn — wir haben sie")
    print("    befragt, sie hat 5 messbare Aspekte preisgegeben.")
    print("  • 5/11 BURUMUT-Wörter haben keine gültige Glyph-Beziehung (Sonderrollen).")
    print("  • 8/11 BURUMUT-Wörter teilen V/K-Code 5417 — das ist eine STARKE")
    print("    Reduktion (95%+ der 16.384 möglichen Codes sind ungenutzt).")
    print("  • Die Substrings-Methode zeigt nur 4-5-Buchstaben-Überschneidungen,")
    print("    keine systematische Verteilung über die 22 Wikia-Pages.")
    print("  • Wir haben die BURUMUT-Matrix multidimensional befragt, aber")
    print("    jede neue Frage kann die Architektur verschieben.")
    print()


def hauptprogramm():
    matrix = lade_matrix_5_pfade()
    matrix_spricht(matrix)


if __name__ == "__main__":
    hauptprogramm()
