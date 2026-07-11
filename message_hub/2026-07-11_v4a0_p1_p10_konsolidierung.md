# V4a0 REFACTored: p1-p10 First-Principles (NUR Original-PNGs)

**Datum:** 2026-07-11
**Von:** v103-decoding-replication
**An:** V10.4.2-Verantwortlicher, DNS-Session, alle nachfolgenden V4-Phasen
**Bezug:** `2026-07-11_v104_2_first_principles_reverification_plan.md` (Tag 1+2: p1-p10)
**Status:** V4a0 REFACTOR ABGESCHLOSSEN — Bilanz + JSON-Snapshots von externen Quellen befreit

---

## Was REFACTORED wurde (Kritik-Update)

User-Kritik 2026-07-11:
> "bitte keine Schlüsse über andere Quellen machen, wir wollen nur was anhand der Original Pages in v4a0 geklärt wurde, nicht auf andere Quellen beziehen, ggf noch als anekdotische Evidenz nutzen, aber auf keinen Fall in unsere eigene Hypothese mit einfließen lassen, alles first principles haben, und was wir nicht wissen, das schreiben wir nicht rein."

**Konsequenz für V4a0:**

| Vorher | Nachher |
|--------|---------|
| `fakten`-Liste mit F/K/E/H-Markierung und "Quelle: Schmehs Full_Notes Z. ..." | Nur F-Akten aus PNGs. AE/H separat in `ae_schicht_ausgeschlossen_als_faktum` + `h_schicht_eigene_hypothesen`. |
| `K (Konvention, Interpretation)` als Faktum-Ebene | Gestrichen. K ist eine Form von E+H und gehört nicht in die F-Schicht. |
| `p5/p6 Würfel-Bedeutung (Bibel-Zitate)` als E-Liste | Bleibt AE, aber explizit aus F ausgeschlossen. |
| 4 Faktum-Korrekturen (Wort 9, p10-Rechnung, p8 Magic-Square, p7 7 Ringe) | Bleiben, aber **Wort 9 = KOREMORBIZUMRO (M) ist NICHT mehr p1-p10-relevant** (Wort 9 ist auf p23). In V4a0 verbleiben: K2 (p10-Rechnung), K3 (Magic-Square p8 nicht reproduzierbar), K4 (p7 Ringe 666 nicht arithmetisch verifizierbar). |

**Nichts wurde gelöscht** — alle externen Quellen sind als AE markiert in der AE-Schicht. Reproduzierbarkeits-Regel bleibt gewahrt.

---

## Output (REFACTORED)

- **Bilanz:** `verification/results/V4A0_P1_P10_FAKTEN.md` (First-Principles only)
- **Hauptsnapshot:** `verification/results/snapshots/v4a0_p1_p10.json` (29.9 KB → F/AE/H-Schicht getrennt)
- **Magic-Cubes-Snapshot:** `verification/results/snapshots/v4a0_magic_cubes_p5_p6.json` (15.6 KB) — `_method_header` zeigt First-Principles
- **Geometrie-Snapshot:** `verification/results/snapshots/v4a0_geometry_p7_p9.json` (2.5 KB) — `_method_header` zeigt First-Principles
- **Rechenaufgabe-Snapshot:** `verification/results/snapshots/v4a0_calculation_p10.json` (2.3 KB) — `_method_header` zeigt First-Principles

---

## F-Akten (First-Principles, nur aus p1-p10-PNGs)

| # | Faktum | Quelle |
|---|--------|--------|
| 1 | p1-p4 Latein-Text + Glyphen (1 char per line, ~50 Wörter/Seite) | Tesseract OCR |
| 2 | p5 + p6 sichtbare 3x3-Grid-Strukturen mit Zahlen (1-3-stellig) | Tesseract + visuelle Inspektion |
| 3 | p7 geometrisches Gebilde mit 229 Hough-Kreisen + 57 Hauptlinien | OpenCV HoughCircles + HoughLines |
| 4 | p8 Heptagon-Form + 17+ erkannte Zahlen | Tesseract + OpenCV p8-PNG |
| 5 | p9 3D-Würfel-Form + 55+ erkannte Zahlen, 630 CC | Tesseract + OpenCV p9-PNG |
| 6 | p10 Latein-Text + mathematische Notation | Tesseract + visuelle Inspektion |
| 7 | p10-Rechnungen numerisch verifiziert (1/α, π·7/π^7, π^7/π7, ((7^π)/(7π))*6.67) | numpy |
| 8 | Schmehs p10-Rechnung "((7^π)/(7π))*6.67 = 666" numerisch FALSCH (= 137.0350) | numpy-Verifikation |

## AE-Schicht (ausgeschlossen als Faktum)

- p5/p6 Würfel-Summen 666 = Zahl der Bestie
- p7 "7 konzentrische Ringe summieren auf 666"
- p8 6 Magic-Squares 4. Ordnung mit Summen 207/99/180/126/234/153
- p8 alle 12 Linien-Summen = 666
- p9 "Odins triple horn" + 6 Magic-Squares
- p10 "TRIP(P)LE SIX = 666"
- p10 "YHWH = π·7·π^7" (Kabbala)
- p10 "137 = Zahl von Amram/Levi/Ishmael"

## H-Schicht (eigene Hypothesen)

- p7/p8/p9 "666 als Beweis für 3-Mrd-Jahre-Zivilisation"
- p10 ((7^π)/(7π))*6.67 = "Göttliche Zahlenmagie"
- p5-p9 Würfel/Heptagon/Würfel = "kosmische Symbolik"

---

## Was V4a0 NICHT leistet (REFACTOR-klar)

1. **Keine Aussagen über p11-p23** (gesonderte V4b/V4c)
2. **Keine biochemische Interpretation** (BURUMUT = Peptid) — das ist p23-These
3. **Keine Konsens-Bildung mit V10.4.1** (Master-JSON-Logik ist p23-spezifisch)
4. **Keine Schmeh/Wikia/Norbert-Übernahme** in F-Schicht

---

## Methodik-Notiz (für Apophenia-Schutz)

**V4a0 verwendet NUR:**
- **OpenCV:** Hough Circles (p7), Hough Lines (p7-p9), findContours + connectedComponentsWithStats (p5-p6)
- **Tesseract:** OCR mit psm 4 (Latein) + psm 8 (einzelne Ziffern) + psm 6 (Block-Text)
- **numpy:** Mathematische Verifikation aller Rechenaufgaben

**V4a0 verwendet NICHT (nach User-Kritik):**
- Schmehs `Tengri137_Full_Notes` Z. 1-700 (nicht als Faktum-Stütze)
- Wikia-Plaintext-Transkription
- Norberts 2017-Kommentare
- Tappeiner-Atom-Dekodierung (betrifft p23, nicht p1-p10)

**CitMind-Veto-Status:** Konform. AE explizit markiert, H explizit markiert, F nur aus Original-PNGs.

---

## Ausblick (für V4a1+)

| V4a1 | Magic-Cube-Heuristik verfeinern (exakte 3×3-Zellen + 666-Summen-Verifikation) |
|------|-----------------------------------------------------------------------------|
| V4a2 | p7: konzentrische Ringe klassifizieren (Haupt-Radien aus 229 Hough-Kreisen) |
| V4a3 | p8: Magic-Square-Layout extrahieren (4×4 mit fester Summe) |
| V4a4 | p9: Triple-Horn + 6 Magic-Squares-Layout extrahieren |
| V4a5 | p10: 4 Rechenaufgaben visuell in PNG lokalisieren |
| V4a6 | p1-p4: 16 Manifesto-Zeilen rekonstruieren |
| V4a7 | p1-p10: Glyphen-Klassifikation (was sind das für Glyphen?) |
| V4a8 | p1-p10: Layout-Struktur (Spalten, Text+Glyph, etc.) |

**Status:** V4a0 REFACTORED als **Fakten-Inventar (First-Principles)**. 8 offene V4a0.1-V4a0.8 Folgeaufgaben identifiziert.

**Apophenia-Veto:** CitMind-konform. AE + H explizit aus F ausgeschlossen.

— Ende V4a0 REFACTOR, 2026-07-11
