# Stufe 3 — Befund: Was liest das ML-Modell, was Schmeh nicht hat

**Brille:** "Vision und Schmeh — wo decken sie sich, wo widersprechen sie sich?"
**Methode:** Token-für-Token-Vergleich der 88 Vision-Tokens gegen 368 Schmeh-Tokens.

---

## 1) Übersicht der Konfidenz

```
Vision-Conf ≥ 0.90:  58  (66%)  — sehr zuverlässig
Vision-Conf 0.80-0.89:  27  (31%)  — zuverlässig
Vision-Conf < 0.80:    3  (3%)   — unsicher (DHJG, WARD, NUMBE)
```

**88% der Vision-Tokens sind ≥ 0.85 confident.** Das ML-Modell ist kein Raten.

---

## 2) Vision-Verteilung — drei Schwerpunkte

| Region-Type | Vision-Tokens | Bedeutung |
|-------------|---------------|-----------|
| `latin_text` | 51 | Normaler Fließtext |
| `formula_block` | 21 | Mathematische Formeln |
| `header` | 16 | Seiten-Header |

**Vision liest in DREI Kontexten** — Text, Formeln UND Header.

**Page-Verteilung:**
- **p23: 40 Tokens** (Maximum) — die BURUMUT-Matrix-Seite, das Vision-Modell liest hier die chemischen Symbole (C, N, O, H, CH, NH, NH2, CH3, HC, HN, H2N).
- **p19: 15 Tokens** — die **Riesenzahlen** in p19_R13: 20894347, 96597344975787088534999, 16098000200684290000046401. Das sind die großen Faktoren.
- **p11: 10 Tokens** — die "COMPLETE SERIES WITHOUT GAPS"-Stelle.
- p07, p15: 4 Tokens
- Rest: 1-3 Tokens

---

## 3) Drei Klassen von Vision-Discovery

### Klasse A: Vision bestätigt Schmeh (mit Variation)

**p11_R2 — beide Quellen, semantisch identisch, Reihenfolge anders:**

Schmeh: *"A COMPLETE SERIES WITHOUT GAPS BETWEEN THE NUMBERS. PERFECT ARRANGED NUMBER GROUPS..."*
Vision (in p11_R2): `N. | A | THE | COMPLETE | GAPS | SERIES | WITHOUT | BETWEEN | NUMBE`

→ **Beide erkennen dieselbe Phrase, aber Vision liest die Wörter in einer anderen Reihenfolge als sie auf der Seite stehen** (vielleicht, weil das ML-Modell spalten- oder zeilenweise liest, nicht linear).

**p09_R5 — Vision verschluckt Präfix:**

Schmeh: *"NOT ORDINARY INDIVIDUALS"*
Vision: `DINARY | INDIVIDUALS`

→ Vision liest den Hauptteil, verliert aber **"NOT OR"** am Anfang. Das ist ein typischer ML-Lesefehler (Truncation am Region-Rand).

### Klasse B: Vision entdeckt Neues (nicht in Schmeh)

**p01_R11: `I CAN READ` (conf=0.96)** — kommt in Schmehs `Tengri137_raw_text.txt` **NICHT vor**.

Das ist bemerkenswert: Auf der ersten Seite steht "I CAN READ" — eine **direkte Aussage des Dokuments an den Leser**, die Schmeh übersehen hat (oder als Tengri-Fragment interpretiert hat, das er nicht eindeutig zuordnen konnte).

**p23_R1, R3, R4, R17: Chemische Symbole (C, N, H, O, CH, NH, NH2, CH3)**

Vision liest auf p23 chemische Summenformeln. Das ist die **BURUMUTREFAMTU-Region** — Vision liest hier eine Protein-/Molekül-Struktur.

Schmeh seinerseits interpretiert p23 als "C N C O O C C O C N" — also als lateinische Buchstaben C und N in einem Muster. Vision liest es als **chemische Atome** (C, N, H, O). **Beide Quellen beschreiben den gleichen Buchstabensatz, aber mit unterschiedlicher Semantik.**

**p19_R13: 20894347, 96597344975787088534999, 16098000200684290000046401** (conf=0.99)

Schmeh hat hier einen anderen Zahlen-String. Vision liest die **echten Werte** direkt aus der Formel-Region.

### Klasse C: Vision-only-Fragmente (nicht in Schmeh)

```
DHJG (p07_R5, conf=0.70) — unklar, ev. Beschädigung
WARD (p15_R9, conf=0.70) — unklar
EXY (p10_R9, conf=0.85) — unklar
IX (p01_R5, conf=0.85) — römische 9?
II (p23_R11, conf=0.80) — römische 2?
HH (p15_R6, conf=0.80)
```

Diese sind **Conf < 0.85 oder echte Lese-Artefakte**.

---

## 4) WORT-ÜBEREINSTIMMUNG (22 gemeinsame Wörter)

```
Wörter in BEIDEN Quellen:    22
Wörter NUR in Vision:        23
Wörter NUR in Schmeh:       778
```

**Schmeh hat 778 exklusive Wörter.** Das ist eine ganze Bibliothek. Vision liefert 23 zusätzliche.

**Top-Schmeh-only-Wörter:**
- YOU (160), THIS (138), OUR (109), OF (94), NOT (90), WE (79), AND (74), TO (71), WILL (63)

Das ist **das Vokabular des Schmeh-Textes**: viele Possessivpronomen, viele Verben im Plural, viele Funktionswörter.

**Top-Vision-only-Wörter:**
- C (11), CH (4), NH (3), HN (2), NH2 (1), CH3 (1), H2N (1), HC (1)

Das ist **chemisches Vokabular** (Kohlenstoff C, Wasserstoff H, Stickstoff N, plus funktionale Gruppen CH, NH, NH2, CH3, H2N, HC, HN).

---

## 5) Was Vision besser sieht als Schmeh

| Was | Vision | Schmeh |
|-----|--------|--------|
| "I CAN READ" auf p01 | ✅ conf=0.96 | ❌ fehlt komplett |
| Chemische Symbole auf p23 | ✅ C, N, H, O, CH, NH, NH2, CH3 | ⚠️ als lateinische C/N interpretiert |
| Konkrete Zahlen auf p19 | ✅ 20894347, 96597344975787088534999, 16098000200684290000046401 | ⚠️ als "große Zahlen" interpretiert |
| Wortreihenfolge | liest Region, nicht linear | linear |

---

## 6) Was Schmeh besser sieht als Vision

- **Den linearen Fließtext** — die Sätze als Ganzes, in der richtigen Reihenfolge.
- **Die längeren Phrasen** — Schmeh rekonstruiert vollständige Sätze, Vision liest Wortfetzen.
- **Die Possessiv-/Pronomen-Struktur** — YOU, WE, OUR, THIS.

---

## 7) Die zentrale Frage: Was bedeutet das für die DEKODIERUNG?

**Zwei unabhängige Lesarten desselben lateinischen Materials:**

1. **Schmehs Lesart:** Linearer Text, komplette Sätze, narratives Englisch.
2. **Vision-Lesart:** Region-basiert, fragmentarisch, aber präzise auf Zahlen und chemische Symbole.

**Beide zusammen ergeben eine dritte Lesart:**
- Vision liefert **die korrekten Zahlen** auf p19 (Faktorisierung).
- Schmeh liefert **die narrativen Erklärungen** drumherum.
- Auf p23 sind die "Buchstaben" **keine lateinischen Wörter, sondern chemische Symbole** — Schmehs Interpretation als "C N C O O..." ist semantisch falsch, aber formal korrekt.

**Was noch fehlt:** Was sind die chemischen Symbole auf p23 *konkret*? Eine BURUMUT-artige Protein-Sequenz? Eine kleine Molekül-Formel? Wir werden das in Stufe 6 vertiefen (BURUMUT-Matrix).

---

## 8) Hypothesen

1. **Vision ist ein zweiter, unabhängiger "Leser"** des Tengri-Dokuments. Wo Vision und Schmeh übereinstimmen, ist der Text sehr wahrscheinlich korrekt.
2. **p23 ist eine chemische Formel**, kein lateinischer Text. Die lateinischen Buchstaben C, N, H, O sind Atome.
3. **p19 enthält eine Faktorisierungs-Aufgabe** — die Zahlen sind so groß, dass sie eine spezifische Bedeutung haben.
4. **p11 hat einen lateinischen "Spruch"** ("A COMPLETE SERIES WITHOUT GAPS") — den Vision in der gleichen Reihenfolge wie Schmeh erkennt, aber in einer anderen Token-Reihenfolge liest.

---

## Konkrete nächste Brille (Stufe 4)

**Stufe 4 — Die 332 Unknown-Glyphen**

Frage: Wo konzentrieren sich die 332 Glyphen mit `type_hint=unknown`? Welche Seiten, welche Region-Typen, welche Cluster-IDs?

Methode:
- Heatmap Page × Region-Typ für unknown-Glyphen
- Welcher Vision-Kind (wenn vorhanden) dominiert bei den Unbekannten?
- Welcher Cluster-ID gehören sie an?
- Größen-/Form-Vergleich mit den "bekannten" Glyphen

Erwartung:
- p05, p06 (Magic-Cube-Bereich) werden die meisten Unbekannten haben.
- Vielleicht sind die Unbekannten **die echten Rätsel-Glyphen** — jenseits der vom Vision-Modell erkannten 17 Standard-Symbole.

**Außerdem:** p18 (0 Latin, 24 Glyphen) — ist sie komplett unknown? Das wäre ein klarer "Fokuspunkt".
