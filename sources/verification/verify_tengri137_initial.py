"""
Verifikation der mathematischen und faktischen Behauptungen aus den
Tengri-137-Dokumenten im Workdir.

Es werden folgende Behauptungen geprueft:
  1.  Quartische Gleichung x^4 - 137 x^3 - 10 x^2 + 697 x - 365 = 0
      - positive reelle Wurzel ~ 137,035999 (Feinstrukturkonstante alpha^-1)
  2.  Zyklische Dezimalperioden
      - 1/7 = 0.(142857)         -> Periode 6
      - 1/13 = 0.(076923)        -> Periode 6
      - 1/17 = 0.(0588235294117647) -> Periode 16
      - 1/19 = 0.(052631578947368421) -> Periode 18
      - 1/43 = 0.(023255813953488372093) -> Periode 21
      - Tengri-137 zyklische Sequenz 0434782608695652173913 -> Periode 22/23?
      - 46-stellige Periode (Neun-Zahl: 10^46 - 1)/p
  3.  Element 114 = Flerovium (Fl), benannt 2012 von IUPAC.
      - Symbol ist 'Fl', nicht 'F' (wie im Text behauptet)!
  4.  Aminosaeure-Ein-Buchstaben-Codes (Beispiel: Tc=43, Ir=77, Mn=25, Eu=63)
  5.  72+38 = 110 (Rule 110 / Shem Hamephorash)
  6.  6 perfekte 4x4 pandiagonale magische Quadrate der Summe 666
  7.  Apophenia-Beispiel: BURUMUT-Matrix -> Amharisch?
  8.  Transkategorie: "3 -> 1 Nachbarschafts-Transformation" Rule 110
"""

from sympy import symbols, solve, Rational, sqrt, nsimplify, Integer
from sympy import isprime, factorint, Poly, nroots, log, pi, E as e
from sympy import Symbol, S
import mpmath
mpmath.mp.dps = 60   # 60 Dezimalstellen


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# -----------------------------------------------------------------
section("1. Quartische Gleichung")
# -----------------------------------------------------------------
x = symbols('x', real=True)
quartic = x**4 - 137*x**3 - 10*x**2 + 697*x - 365
roots = solve(quartic, x)
print(f"Gleichung: x^4 - 137 x^3 - 10 x^2 + 697 x - 365 = 0")
print(f"Anzahl reeller Wurzeln: {sum(1 for r in roots if r.is_real)}")
print(f"Anzahl komplexer Wurzeln: {sum(1 for r in roots if not r.is_real)}")
print()
for i, r in enumerate(roots):
    val = complex(r)
    print(f"  Wurzel {i+1}: {r}  (numerisch: {val})")

real_roots = [r for r in roots if r.is_real and r > 0]
if real_roots:
    pos = real_roots[0]
    print(f"\nPos. reelle Wurzel: x ~ {float(pos):.10f}")
    print(f"Aktueller CODATA-Wert fuer 1/alpha: ~ 137.035999084")
    print(f"Abweichung: {abs(float(pos) - 137.035999084):.6e}")
else:
    print("ACHTUNG: keine positive reelle Wurzel gefunden!")


# -----------------------------------------------------------------
section("2. Zyklische Dezimalperioden")
# -----------------------------------------------------------------
def cyclic_period(p):
    """Laenge der Periode von 1/p in Dezimaldarstellung."""
    if not isprime(p) or p in (2, 5):
        return None
    k = 1
    val = 10 % p
    while val != 1:
        val = (val * 10) % p
        k += 1
    return k

# Einige bekannte Perioden
for p in [3, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 73, 101]:
    period = cyclic_period(p)
    if period:
        # tatsaechlich Dezimalstellen
        s = mpmath.mpf(1) / mpmath.mpf(p)
        out = mpmath.nstr(s, period + 5)
        print(f"  1/{p:>3} -> Periode {period:>3}   {out[:period+5]}")


# -----------------------------------------------------------------
section("3. 46-stellige zyklische Dezimalperiode?")
# -----------------------------------------------------------------
# Es wird behauptet, die Tengri-Urheber nutzten Divisionen mit massiven
# Zahlen, um zyklische Dezimalen mit 46-stelliger Periode zu erzeugen.
# Wir testen: welche Primzahl gibt 1/p mit Periode 46?
# Eine Primzahl p (nicht 2,5) hat die Periode len(ord_p(10)).
# Also suche kleinste Primzahl p mit ord_p(10) = 46.
candidates = []
for n in range(2, 200000):
    if not isprime(n):
        continue
    if cyclic_period(n) == 46:
        candidates.append(n)
        if len(candidates) >= 5:
            break
print(f"Kleinste Primzahlen mit dezimaler Periode 46: {candidates}")

# (10^46 - 1)/p -> dechiffrierter String
if candidates:
    p = candidates[0]
    s = mpmath.mpf(10)**46 - 1
    s = s / mpmath.mpf(p)
    out = mpmath.nstr(s, 50)
    print(f"  1/{p} hat Periode 46, Ziffern: {out}")

# Auch: 46-stellige Neun-Zahl (10^46-1)/p
print("\nBehauptung: 46-stellige Zahl, die nur aus Neunen besteht.")
# Wenn N = 9999...9 (46 Neunen) = 10^46 - 1, dann ist 1/N die Kehrwert-
# dezimalperiode. Aber die Behauptung in PX Construct: '46-stellige Zahl,
# die ausschliesslich aus Neunen besteht' als Divisor.
# Wir testen: (10^46 - 1) / 7 = ?
N = mpmath.mpf(10)**46 - 1
print(f"  (10^46 - 1)/7 = {mpmath.nstr(N / 7, 50)}")
print(f"  (10^46 - 1)/9999991 (Beispiel-Primzahl) = ...")
# Beispiel: zyklische Primzahlen mit Periode 46 existieren.


# -----------------------------------------------------------------
section("4. Beispiel-Sequenz 0434782608695652173913")
# -----------------------------------------------------------------
# Dies ist eine zyklische Zahl. Sie beginnt mit '04347826...' was die
# Periode 1/23 ist. Test:
s23 = mpmath.nstr(mpmath.mpf(1) / mpmath.mpf(23), 30)
print(f"  1/23 = {s23}")
# Auch bekannt: 1/23 = 0.(0434782608695652173913)
# -> diese Sequenz hat tatsaechlich 22 Ziffern (0434782608695652173913) Periode 22.
print(f"  Zyklische Laenge 1/23 = {cyclic_period(23)}")


# -----------------------------------------------------------------
section("5. Element 114 = Flerovium (Element-Symbol)")
# -----------------------------------------------------------------
# ACTUAL DATA: Element 114 ist Flerovium, Symbol 'Fl' (NICHT 'F')
# benannt am 31. Mai 2012 von IUPAC.
print("WAHR:   Element 114 heisst Flerovium.")
print("        Offizielles Symbol: Fl (Flerovium)")
print("        Vorlaeufiger Platzhalter vor 2012: Uuq (Ununquadium)")
print("        Benannt 2012 von IUPAC.")
print()
print("BEHAUPTUNG im PX Construct / Transkategorische Texte:")
print("        Element 114 = 'F' (Flerovium)")
print("        -> FALSCH! Das offizielle Symbol ist 'Fl'.")
print()
print("Auswirkung auf die Chiffre:")
print("Wenn Element 114 das Symbol 'Fl' hat, dann liefert es ZWEI")
print("Buchstaben (F+l), nicht einen einzelnen 'F'. Die naive")
print("Buchstaben-Extrahierung in Tappeiners Loesung ist daher")
print("fragwuerdig.")


# -----------------------------------------------------------------
section("6. Aminosaeure-Ein-Buchstaben-Codes (Beispiel)")
# -----------------------------------------------------------------
amino = {
    43: "Tc",  # <- Technetium, NICHT Ala oder Arg
    77: "Ir",  # <- Iridium
    25: "Mn",  # <- Mangan
    63: "Eu",  # <- Europium
}
print("Im PX Construct wird behauptet:")
print("  43 -> Tc, 77 -> Ir, 25 -> Mn, 63 -> Eu  (-> Aminosaeure-Codes)")
print()
print("WAHR: 43 ist Technetium (Tc), 77 ist Iridium (Ir),")
print("      25 ist Mangan (Mn), 63 ist Europium (Eu).")
print()
print("Diese sind ELEMENT-SYMBOLE, NICHT Aminosaeure-Codes!")
print("Echte Aminosaeure-Codes (3-Buchst. bzw. 1-Buchst.):")
amino_table = {
    'A': 'Ala', 'R': 'Arg', 'N': 'Asn', 'D': 'Asp', 'C': 'Cys',
    'E': 'Glu', 'Q': 'Gln', 'G': 'Gly', 'H': 'His', 'I': 'Ile',
    'L': 'Leu', 'K': 'Lys', 'M': 'Met', 'F': 'Phe', 'P': 'Pro',
    'S': 'Ser', 'T': 'Thr', 'W': 'Trp', 'Y': 'Tyr', 'V': 'Val',
}
print(f"  Ala=A, Arg=R, Asn=N, Asp=D, Cys=C, Gln=Q, Glu=E, Gly=G,")
print(f"  His=H, Ile=I, Leu=L, Lys=K, Met=M, Phe=F, Pro=P, Ser=S,")
print(f"  Thr=T, Trp=W, Tyr=Y, Val=V   (Stop: *, U, O)")
print()
print("Die PX-Construct-Behauptung ist UNSCHARF: die Symbole Tc/Ir/Mn/Eu")
print("sind Elementsymbole, und die Aminosaeure-Analogie ist ein anderes")
print("Dekodierschema (Biermann fuer Seite 23), nicht fuer Seiten 17-22.")


# -----------------------------------------------------------------
section("7. Pandiagonale 4x4 magische Quadrate")
# -----------------------------------------------------------------
# Behauptung: Es existieren exakt 3 distinkte vollkommene 4x4 Quadrate.
# Wahr: Es gibt 48 pandiagonale 4x4 magische Quadrate MIT Rotation/Reflexion,
# aber genau 3 AEQ (Aequivalenz-Klassen), also 3 grundsaetzlich verschiedene.
# Genau: 48 / 16 (D4 Symmetriegruppe) = 3. Korrekt.
#
# Die 6 Tengri-Quadrate leiten sich durch lineare Operationen aus 3 ab.
def is_pandiagonal(M):
    n = len(M)
    s = sum(M[0])
    # Reihen, Spalten, beide Diagonalen
    if any(sum(row) != s for row in M):
        return False
    if any(sum(M[i][j] for i in range(n)) != s for j in range(n)):
        return False
    if sum(M[i][i] for i in range(n)) != s:
        return False
    if sum(M[i][n-1-i] for i in range(n)) != s:
        return False
    # pandiagonal: alle gebrochenen Diagonalen
    for k in range(1, n):
        if sum(M[i][(i+k) % n] for i in range(n)) != s:
            return False
        if sum(M[i][(i-k) % n] for i in range(n)) != s:
            return False
    return True

# Klassisches 4x4 pandiagonales Quadrat (Duerer-Variante 1..16 -> 34)
base = [[1,8,10,15],[12,13,3,6],[7,2,16,9],[14,11,5,4]]
print(f"  Standard 4x4 Quadrat 1..16, Summe {sum(base[0])}: pandiagonal={is_pandiagonal(base)}")
# Skaliere auf magische Konstante 666:
# linear: M' = a*M + b, Summe -> 4a + 4b pro Zeile?
# Summe einer Zeile ist 34; brauchen 666. => 666 = 34a.
# => a = 666/34 = 19.588.. nicht ganzzahlig.
# Es gibt jedoch ein vollkommenes pandiagonales 4x4 mit Summe 666, das
# aus mehreren konstruiert werden kann.
print("  -> Quadrate mit Summe 666 erfordern nichttriviale Konstruktion.")
print("     (Es gibt genau 880 magische 4x4 Quadrate ueberhaupt;")
print("      davon sind 48 pandiagonal, in 3 Aequivalenz-Klassen.)")


# -----------------------------------------------------------------
section("8. 72 + 38 = 110")
# -----------------------------------------------------------------
print(f"  72 + 38 = {72 + 38}")
print("  Rule 110 ist ein bekannter Turing-vollstaendiger")
print("  zellularer Automat (Cook 2004).")
print("  Shem Hamephorash: 72 Namen Gottes aus Exodus 14:19-21.")
print("  Numerische Identitaet 72+38=110 ist ARITHMETISCH KORREKT,")
print("  aber die behauptete Tiefenbedeutung (Turing-Vollstaendigkeit")
print("  des Vakuums) ist NICHT durch diese Addition bewiesen.")


# -----------------------------------------------------------------
section("9. BURUMUT-Matrix: Amharisch-Test")
# -----------------------------------------------------------------
# Behauptung: Die Sequenz BURUMUTREFAMTU enthalte Amharisch-Bruchstuecke
# und verweise auf aethiopische Orte.
# Realitaet: BURUMUT ist KEIN amharisches Wort.
amharic_substr = ["buru", "mut", "refa", "mtu", "amu"]
print(f"  Hypothetische Amharisch-Substrings: {amharic_substr}")
print("  Amharisch nutzt das Fidel-Alphabet (Syllabogramm).")
print("  Ein Silbenmuster 'bu-ru-mut' existiert nicht als Wort.")
print("  Realistische Einschaetzung: Das ist APOPHENIE (Musterwahn).")


# -----------------------------------------------------------------
section("10. '3 -> 1 Nachbarschaftstransformation' Rule 110")
# -----------------------------------------------------------------
# Rule 110: 1D zellularer Automat. Jede Zelle hat 3 Nachbarn (links, mitte,
# rechts), bestimmt naechsten Zustand. NICHT '3 -> 1' im engeren Sinne,
# sondern 8 Eingabe-Muster (2^3 = 8) -> 2 Ausgaenge. Daher: 3-bit lookup.
print("  Rule 110 nutzt 3-Zellen-Nachbarschaft (8 moegliche Eingaben).")
print("  Die Beschreibung '3 -> 1 Transformation' ist eine Verzerrung.")
print("  Korrekt waere: 3 Eingabe-Bits -> 1 Ausgabe-Bit (lookup-Tabelle).")


# -----------------------------------------------------------------
section("11. 'Rule 110 = minimaler Turing-vollstaendiger Automat'?")
# -----------------------------------------------------------------
# Cook bewies 1998: Rule 110 ist Turing-vollstaendig.
# Aber: Rule 110 ist nicht der EINFACHSTE. Andere elementare
# zellulaere Automaten (Rule 30, Rule 54 etc.) sind ebenfalls TU.
# Die Behauptung 'einfachster' ist also UNGENAU.
print("  WAHR: Rule 110 ist Turing-vollstaendig (Cook 1998/2004).")
print("  FALSCH: Rule 110 ist NICHT der 'einfachste' TU zellulaere")
print("          Automat. Auch Rule 30 etc. gelten als TU.")


# -----------------------------------------------------------------
section("12. Zyklische Dezimalperiode 1/46?")
# -----------------------------------------------------------------
# 1/46 = 1/(2*23) -> Periode = max(1, ord_23(10)) = 22
# Falls die Zahl 46 explizit gemeint ist: 46 ist NICHT prim.
print(f"  46 = 2 * 23. Nicht prim.")
print(f"  1/46 = {mpmath.nstr(mpmath.mpf(1)/mpmath.mpf(46), 30)}")
print(f"  Periode 1/46 = {cyclic_period(23)}")


# -----------------------------------------------------------------
section("13. 10^46 - 1 / p (46 Neunen)")
# -----------------------------------------------------------------
# Wenn N = (10^46 - 1) aus repetitiven 9ern besteht (46 Stueck),
# ist N = 9...9 = 9 * R(46), wobei R(46) = 123456790123456790... (repunit).
# Die Behauptung im PX-Construct, dass eine 46-stellige Periode existiert,
# ist konsistent mit der Existenz einer Primzahl p mit ord_p(10) = 46.
print(f"  (10^46 - 1)/9 = {mpmath.nstr((mpmath.mpf(10)**46 - 1)/9, 50)}")
print("  Dies ist der 46-stellige Repunit R_46 (Beginnend mit 1).")


# -----------------------------------------------------------------
section("14. Syntaktische Pruefung RECIEVE")
# -----------------------------------------------------------------
print("  Im PX Construct wird gesagt, 'RECIEVE' sei ein Tippfehler.")
print("  Im Transkategorischen Mathematik-Text wird behauptet, das Wort")
print("  sei eine algorithmische Direktive 'RE-SIEVE'.")
print()
print("  TATSACHE: 'receive' mit 'ei' statt 'ie' ist ein bekannter")
print("            und extrem haeufiger ENGLISCHER Rechtschreibfehler.")
print("            Die 'recieve'-Schreibung kommt in Millionen von")
print("            Texten vor (Google n-gram, etc.).")
print("  Es gibt KEINE Notwendigkeit, dies als 'Homophon RE-SIEVE'")
print("  umzudeuten -- die einfachste Erklaerung ist ein Tippfehler.")


# -----------------------------------------------------------------
section("15. Quanten-Eichtransformation / 666 / Calabi-Yau")
# -----------------------------------------------------------------
print("  Es gibt KEIN physikalisches Theorem, das 6 magische 4x4")
print("  Quadrate der Summe 666 mit 6D Calabi-Yau-Mannigfaltigkeiten")
print("  verbindet. Die '6 Matrizen -> 6 Dimensionen' Analogie ist")
print("  WILLKUERLICH.")


# -----------------------------------------------------------------
section("16. Tetragrammaton / Hebraeisch / 137")
# -----------------------------------------------------------------
print("  Im Transkategorischen Text wird behauptet:")
print("    alpha^-1 ~ pi^7 / (7^pi * sqrt(x))")
print()
# Numerisch pruefen
alpha_inv = 137.035999084
val = mpmath.pi**7 / (7**mpmath.pi * mpmath.sqrt(alpha_inv))
print(f"  pi^7 / (7^pi * sqrt(137.036)) = {val}")
print(f"  Tatsaechliches alpha^-1     = {alpha_inv}")
print(f"  Abweichung: {abs(float(val) - alpha_inv):.2f}")


# -----------------------------------------------------------------
section("17. Summe magisches 4x4 Quadrat = 666")
# -----------------------------------------------------------------
print("  Die magische Konstante 666 ist nur eine ZAHL.")
print("  Es gibt keinen mathematischen Grund, warum 666 speziell")
print("  mit einer physikalischen Konstante verbunden waere.")
print("  4x4 pandiagonale Quadrate existieren fuer jede Summe,")
print("  die durch 4 teilbar >= 16 ist (mit gewissen Einschraenkungen).")


# -----------------------------------------------------------------
section("18. 'Landauer-Penrose-Bruecke' / Orch-OR")
# -----------------------------------------------------------------
print("  Penrose-Hameroff Orch-OR ist eine HYOTHETISCHE Theorie")
print("  und NICHT empirisch bestaetigt (Stand 2024/2026).")
print("  Die 'Landauer-Penrose-Bruecke' ist kein etablierter")
print("  naturwissenschaftlicher Begriff.")


# -----------------------------------------------------------------
section("19. Genesis-Test: 6 perfekte 4x4 pandiagonale Quadrate")
# -----------------------------------------------------------------
# Konstruiere ein pandiagonales 4x4 mit Summe 666
# Basisquadrat (mit Summe 34), dann linear transformieren.
# M' = a*M + b, Summe wird 4a*Sum/4 + 4b = a*34 + 4b.
# Ziel 666 = 34a + 4b
# z.B. a=18, 666 = 612 + 4b => 4b = 54 => b = 13.5 (nicht ganzzahlig)
# z.B. a=19, 666 = 646 + 4b => 4b = 20 => b = 5
a, b = 19, 5
sq = [[a * base[i][j] + b for j in range(4)] for i in range(4)]
print(f"  Konstruiertes Quadrat (a=19, b=5), Summe={sum(sq[0])}:")
for row in sq:
    print(f"    {row}")
print(f"  pandiagonal: {is_pandiagonal(sq)}")


# -----------------------------------------------------------------
section("20. IUPAC + Flerovium-Symbol")
# -----------------------------------------------------------------
print("  Periodensystem der Elemente (IUPAC):")
print("    Element 114 = Flerovium, Symbol 'Fl', benannt 2012-05-31.")
print("    Aequivalent in Codex-Sinn: Element 114 -> Symbol 'Fl' -> 2 Buchstaben")
print("    -> 'F'+'l' NICHT 'F' (wie in den Texten behauptet).")
print()
print("  Folge: Wenn der dechiffrierte Text N A F E R A N S A H O T F E")
print("  heisst und 'F' aus Element 114 stammen soll, dann ist das entweder:")
print("    (a) Element 114 -> 'F' (alte Konvention?) -- nicht standard,")
print("        IUPAC-Symbol war nie 'F', sondern 'Uuq' vor 2012 und 'Fl' nach 2012.")
print("    (b) Ein Fehler / freie Erfindung des Autors.")


# -----------------------------------------------------------------
section("21. Zyklische Zahl 0.0434782608695652173913")
# -----------------------------------------------------------------
seq = "0434782608695652173913"
print(f"  Behauptete Sequenz: {seq} (Laenge {len(seq)})")
print(f"  1/23 = {mpmath.nstr(mpmath.mpf(1)/23, 30)}")
print(f"  Tatsaechlich: 1/23 = 0.0434782608695652173913...")
print(f"  Periode: {cyclic_period(23)}")


# -----------------------------------------------------------------
section("22. Cyclic numbers / Repunit Factors")
# -----------------------------------------------------------------
# Wenn p eine 'zyklische Primzahl' ist mit Periode p-1, dann ist
# 1/p = 0.(repeating sequence of length p-1).
# Beispiele: p = 7 (Periode 6), p = 17 (16), p = 19 (18), p = 23 (22).
for p in [7, 17, 19, 23, 29, 47, 59, 61, 97]:
    period = cyclic_period(p)
    repunit = int((mpmath.mpf(10)**period - 1) / mpmath.mpf(p))
    print(f"  p={p}: Periode={period}, (10^periode - 1)/p = {repunit}")


print("\nFertig.")