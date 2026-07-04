# Stufe 10 — Befund: p18 ist eine 16-Zeilen-Primfaktorzerlegungs-Tabelle

**Brille:** "Was ist die Struktur von p18?"

**Methode:** Glyphen sortiert nach y, x; Vergleich mit Schmehs Transkription; Analyse der Math-Cluster.

---

## 1) Die wichtigste Entdeckung: p18 ist KEINE tabula rasa

**Schmehs Transkription** (`/run/media/julian/ML4/tengri137/consecutive_reading/Tengri137_raw_text.txt`):
- p18 enthält **16 gepaarte Primfaktorzerlegungs-Quotienten** (Z.682-758)
- Insgesamt **32 einzelne Zeilen** (16 Zähler + 16 Nenner)
- Insgesamt **112 `*` Multiplikations-Operatoren**
- "Dash rows act as fraction bars"

**Aber das Vision-System sieht nur 24 Glyphen!** Die Multiplikationszeichen und Ziffern sind geometrisch **miteinander verschmolzen** — sie können nicht als getrennte Glyphen erkannt werden.

---

## 2) Die zwei Math-Cluster auf p18

| Cluster | Anzahl | Mittlere Breite | y-Range | Was es ist |
|---|---|---|---|---|
| **GEOM_MEDIUM_MATH_TIMES_0018** | 13 Glyphen | ~390 px | 272-1352 | Breite Quotienten (3+ Faktoren) |
| **GEOM_MEDIUM_MATH_TIMES_0017** | 3 Glyphen | ~214 px | 1018-1416 | Schmale Quotienten (1-2 Faktoren) |

→ **0017 = kurze Ausdrücke, 0018 = lange Ausdrücke.** Das passt zu Schmehs Strukur:
- Schmehs Zeile 19 (1 `*`): `3 * 227 * 259009 * 84754841` (schmal)
- Schmehs Zeile 25 (1 `*`): `5^2 * 139795778583407753912923` (sehr schmal, nur 1 `*`)
- Schmehs Zeile 16 (8 `*`): `2 * 11 * 17 * 43 * 113 * 163 * 23669 * 316964629 * ...` (sehr breit)

---

## 3) Die 3 math_times markieren Schlüssel-Brüche

| idx | y | size | w | Bedeutung |
|---|---|---|---|---|
| **840** | 272 | 1982 | 322 | 1. Zähler (sehr frühe Position) |
| **844** | 548 | 3278 | 434 | Mitte der Seite |
| **852** | 878 | 2284 | 274 | Nach 6 Brüchen (Block A→B Übergang) |

→ Die 3 math_times sind die **3 wichtigsten Multiplikations-Zeichen** — eines pro Y-Block (A: 272, B: 548, C: 878).

---

## 4) Die 49755-px-Zwillings-Linie: Bezugslinie

```
p18 idx=849  cx=893  cy=845  w=138  h=1170  cluster=GEOM_MEDIUM_UNKNOWN_0019
p17 idx=825  cx=893  cy=845  w=138  h=1170  cluster=GEOM_MEDIUM_UNKNOWN_0019
```

→ **Die 49755-px-Linie ist eine IDENTISCHE senkrechte Spalte** auf p17 und p18. Sie beginnt bei y=260 (kurz unter Seitenheader) und endet bei y=1430 (kurz über Footer). **Sie ist eine Bezugslinie, die die mathematische Notation einrahmt** — sie markiert den **rechten Rand des Quotienten-Bereichs** und ist 1170px hoch, fast die volle Seitenhöhe.

---

## 5) Die vollständige Architektur von p18

| Y-Range | Glyphen | Was es ist |
|---|---|---|
| **260-680** (Block A) | 5 complex_symbols (0018) + 2 math_times | Erste 5 Zähler/Nenner |
| **735-878** (Block B) | 4 complex_symbols + 1 unknown + 1 49755-Linie + 1 math_times | Trennlinie + Bezugslinie + 4 weitere Brüche |
| **1018-1416** (Block C) | 5 complex_symbols (0018+0017) | Letzte 5 Zähler/Nenner |
| **1418-1625** (Block D) | 1 turkic_round_rune + 1 unknown + Footer | Unklare Glyphen + Footer |

**Drei unbekannte Glyphen auf p18:**
- idx 848 (Y=735, x=796, size=235) — cluster=GEOM_MEDIUM_UNKNOWN_0004
- idx 851 (Y=819, x=786, size=155) — cluster=GEOM_MEDIUM_UNKNOWN_0005
- idx 861 (Y=1477, x=810, size=580) — vk=unknown, cluster=GEOM_MEDIUM_TURKIC_ROUND_RUNE_0010

Diese 3 Unbekannten sind alle im **rechten Drittel** der Seite (x ≥ 786), in der **Nähe der 49755-px-Bezugslinie** (x=824-962). Sie sind möglicherweise:
- Resultat-Markierungen neben den Brüchen?
- Hinweise auf die zu berechnenden Werte?

---

## 6) Hypothesen

1. **p18 ist eine 16-Zeilen-Primfaktorzerlegungs-Tabelle** mit 16 Brüchen (Zähler/Nenner), getrennt durch Bindestrich-Reihen als Bruchstriche.
2. **Das Vision-System kann die `*`-Multiplikationszeichen und die Ziffern nicht trennen** — beide werden als "complex_symbol" (Cluster MATH_TIMES_0017/0018) klassifiziert. Die mathematische Information ist in der Geometrie **nicht direkt** lesbar.
3. **Die 3 expliziten math_times** sind die 3 wichtigsten/brüche-relevantesten Multiplikations-Operatoren — sie wurden als besondere Form erkannt.
4. **Die 49755-px-Bezugslinie** ist auf p17 UND p18 identisch — sie ist die "rechte Klammer" des Formel-Bereichs und verbindet die beiden Formel-Seiten.
5. **Die 0017/0018-Cluster-Unterscheidung** korreliert mit der ANZAHL der Multiplikations-Operatoren in der Zeile (0017 = schmal = wenige Operatoren, 0018 = breit = viele Operatoren).
6. **Die 3 unbekannten Glyphen** im rechten Bereich (idx 848, 851, 861) sind möglicherweise **Resultat-Markierungen** — sie stehen nicht IN den Brüchen, sondern NEBEN ihnen.

---

## 7) Was heißt das für die DEKODIERUNG?

**p18 ist mathematisch verschlüsselt, nicht geometrisch lesbar.**

Das Vision-System kann die algebraische Information (Ziffern, `*`, `^`) **nicht dekodieren** — alles wird zu "complex_symbol". Die 3 math_times sind die einzigen direkten Hinweise auf Multiplikation.

**Schlussfolgerung:** Die geometrische Beschreibung von p18 liefert nur:
- Anzahl der Brüche (16, aber ungenau als ~13+3+4 sichtbare Strukturen)
- Position der wichtigen Multiplikations-Operatoren (3 explizite math_times)
- Die Bezugslinie (geteilt mit p17)

**Die algebraische Information muss aus SCHMEHS Transkription kommen**, nicht aus dem Vision-System.

→ **V4-Glyph-Pipeline + Schmeh-Transkription sind KOMPLEMENTÄR:**
- V4 = Geometrie, Struktur, Symmetrie, Position
- Schmeh = Algebra, Zahlen, Faktoren, Beziehungen

**p18 ist der Beweis, dass die V4-Pipeline NICHT für die algebraische Dekodierung ausreicht.** Sie ist ein **Struktur-Detektor**, kein **Inhalt-Leser**.

---

## Konkrete nächste Brille (Stufe 11)

**Stufe 11 — Die hidden math: π, ^, ×**

Frage: Schmehs p18 hat nur `*` und `^`. Das V4-System hat 3 math_times, 1 math_pi (auf p14), 1 math_exponentiation (auf p14). Wo ist die **mathematische Spezialsymbolik** im Dokument?

Methode:
- Suche nach math_pi, math_exponentiation, math_times über alle Seiten
- Welche Glyphen sind als "math_X" markiert?
- Was bedeuten sie im Kontext der Schmehs-Transkription?

Erwartung:
- π und ^ sind EXOTISCHE Operatoren — sie kommen nur an besonderen Stellen vor
- Vielleicht sind sie auf p14 (BURUMUT-Matrix-Seite)
- Vielleicht ist die **Anzahl und Position** der math-Operatoren signifikant
