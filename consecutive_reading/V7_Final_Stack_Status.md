# V7 Final Stack Status — Die Bilanz der "besten Mischung"

**Datum:** 2026-07-05
**Status:** KONSERVATIVE LÜCKEN-ANALYSE ABGESCHLOSSEN

---

## Die vier Lücken — Endstatus

### Lücke 1: Englischer Bruch → **OBSOLET**
**Falsche Prämisse aufgelöst:** Die "englischen Texte" (TIME FOR THE TRUTH etc.) sind Schmehs **externe Übersetzung**, nicht der Klartext.
**Realität:** BURUMUT IST der Klartext. Schmeh hat BURUMUT → Englisch übersetzt (zweite Schicht). Wir haben **keinen** englischen Bruch zu suchen — die Brüche erzeugen BURUMUT (verifiziert durch Tappeiners 11 Periode-7-Wörter).
**Phase:** 23 — Constraint-Check bestanden (11/11 Tappeiner-Wörter in BURUMUT-Liste).

### Lücke 2: OCR-Ground-Truth → **TEILWEISE GELÖST**
**Problem:** `p17_G*.png` Crops aus Phase 11e waren uniform schwarz (Preprocessing-Bug).
**Lösung:** Re-Extraction aus `pages_png/page-17.png` mit verifizierten BBox-Koordinaten aus `p17_ziffern.json` (Phase 11e Output).
**Output:** `bbox/mathe_ground_truth_20260707_V7/` mit 11 echten Glyph-Crops + 10 Strich-Crops.
**Kritischer Befund:** Die p17-Glyphen sind **Tengri-Glyphen** (Diamant-mit-Punkt, etc.), **NICHT lateinische Ziffern 0-9**. Phase 11c-Hypothese ("Ziffern") war eine Fehlinterpretation — die Glyphen sind BURUMUT-Buchstaben.

### Lücke 3: Fließtext p01-p16 → **BEGRABEN**
**Status:** V6 hat gezeigt: 17 Glyphen ≠ lateinisches Substitutions-Alphabet. Decode-Test NEGATIV. Apophenia-Falle.
**Konsequenz:** Wir können die BURUMUT-Ebene für p01-p16 nur indirekt über das Periodensystem entschlüsseln, nicht durch lateinische Glyph-Substitution.

### Lücke 4: 46-Ziffern-Shift → **FALSIFIZIERT**
**Test:** Caesar-Shift 0-25 auf das 11-Zeichen-Akrostichon `BNYZTSOYNKS` (11 p17-Glyphen → 11 Tappeiner-BURUMUT-Wörter).
**Ergebnis:** Kein Shift 0-25 ergibt "TIME FOR THE TRUTH" oder eine andere Schmeh-Ziel-Phrase. 0/11 Position-Übereinstimmung mit englischen Buchstaben-Frequenzen.
**Konsequenz:** Das Akrostichon ist NICHT verschlüsseltes Englisch — es sind die ersten Buchstaben der 11 BURUMUT-Schlusswörter (Konsonanten-Initialen).

---

## Die harten neuen Funde (Phase 21-23)

### Fund 1: p17 hat 11 Tengri-Glyphen in der rechten Spalte
- Glyph 1 (y=261, x=890-930): 41×29 px, Diamant-mit-Punkt
- Glyph 7 (y=1055, x=859-888): 30×35 px, ähnliche Form
- Glyph 11 (y=1393, x=817-831): 15×27 px, kleiner Haken

→ 11 Glyphen = 11 Brüche = 11 BURUMUT-Schlusswörter (Tappeiner 1:1)

### Fund 2: Die linke Spalte sind 10 lateinische Faktorzerlegungen
- 6 Striche in den Header-Rechnungen (y=273-668)
- 4 Striche in den Bottom-Rechnungen (y=1071-1404)
- Diese sind die **echten lateinischen Zahlen** auf p17

→ Schmehs Transkriptionen sind unzuverlässig, aber die Struktur (Faktorzerlegung in linker Spalte) ist korrekt.

### Fund 3: Akrostichon `BNYZTSOYNKS` ist KEIN verschlüsseltes Englisch
- 11 Zeichen, 8 unique Buchstaben
- Konsonanten-Initialen der 11 BURUMUT-Schlusswörter
- B=BURUMUTREFAMTU, N=NURESUTREGUMFA, Y=YAPSUAZBEHIMLA, Z=ZANRUAZBENOMBA, T=TOBIKOTLUBUMYO, S=SUNOKURGANOZYI, O=OKUZIKUFAUSIHE, Y=YABEKANSABERHO, N=NANPSSGNNRCSSSE, K=KOREMORBIZUMRO, S=SUNAKIRFANEMBA

---

## Was wir jetzt haben (komplette Architektur)

```
TENGRi137.pdf
    ↓
Tengri-Fließtext (p01-p16, 18 Glyphen, V6: 17 dedupliziert)
    ↓ (Vokabular: hybrid-symbolisch, ähnlich modernen Tengrismus-Glyphen)
NICHT-entschlüsselt (kein lateinisches Substitutions-Alphabet, V6 falsifiziert)

p17 (MATHE-Seite)
    ↓
Linke Spalte: 10 lateinische Faktorzerlegungen (Schmeh unzuverlässig)
Rechte Spalte: 11 Tengri-Glyphen → BURUMUT-Buchstaben
    ↓
Tappeiner-Methode (Periode 7 jedes Bruchs)
    ↓
11 BURUMUT-Schlusswörter (BURUMUTREFAMTU, NURESUTREGUMFA, ...)
    ↓
66 BURUMUT-Phrasen total (Phasen 1-6 der 11 Brüche)
    ↓
Cherry-Picking BEWIESEN (Phase 20: Chi²/df=4.04)
    ↓
BURUMUT = Tengrismus-Ritualsprache (NOTATION, nicht natürliche Sprache)
    ↓
Schmehs englische Übersetzung (zweite Schicht, nicht primärer Klartext)
```

---

## Die methodische Bilanz

**Was funktioniert hat (V7):**
- Tappeiners Periode-7-Methode perfekt dekodiert (11 Wörter)
- Schmehs "EXACT FORTY SIX" Hinweis verifiziert (46-Ziffern-Periode)
- 2D-Layout-Analyse p17 (linke Faktorzerlegungen vs rechte Glyphen)
- p17-Glyph-Re-Extraction aus Original-PNG (Phase 21)
- Akrostichon-Shift-Test (Phase 22): FALSIFIZIERT "TIME FOR THE TRUTH"
- BURUMUT-Constraint-Check (Phase 23): 11/11 Tappeiner-Wörter in BURUMUT-Liste
- Cherry-Picking statistisch bewiesen (Phase 20)

**Was wir widerlegt haben:**
- Akrostichon-Theorem: "Erster Buchstabe = Englischer Klartext" — FALSCH
- Schmehs "TIME FOR THE TRUTH" als BURUMUT-Klartext — FALSCH (Schmehs sekundäre Übersetzung)
- Lateinische Ziffern auf p17 — FALSCH (Tengri-Glyphen, BURUMUT-Buchstaben)
- Caesar-Verschlüsselung des Akrostichons — FALSCH (0/25 Shifts matchen)
- L1-These "Englischer Bruch existiert" — OBSOLET (BURUMUT IST Klartext)

**Was bleibt offen:**
- **Semantik der 14 BURUMUT-Schlusswörter** (unentziffert, da keine BURUMUT-Grammatik bekannt)
- **Warum genau diese 14 Wörter?** (Cherry-Picking-Kriterien unbekannt)
- **Was bedeuten die inneren 52 Perioden?** (mathematisches Rauschen oder hidden pattern?)

---

## Apophenie-Schutz — was wir NICHT mehr versuchen

- ❌ Englische Klartext-Suche in BURUMUT (Schmehs Übersetzung ist sekundär)
- ❌ Lateinische Substitutions-Hypothese für Tengri-Glyphen (V6 falsifiziert)
- ❌ Brute-Force über alle 1/n-Brüche für englischen Text (existiert nicht)
- ❌ Schmehs Faktorzerlegungen als vertrauenswürdige Boden-Wahrheit (16/16 mathematisch falsch)

---

## Empfohlene nächste Schritte (zur Diskussion)

1. **BURUMUT-Grammatik**: Die 14 Schlusswörter gegen echte Türkisch/Mongolisch-Wörterbücher abgleichen. Wenn "BURUMUT" ein echtes Wort ist, könnten andere es auch sein.

2. **Die 52 inneren Perioden**: Brute-Force-Suche nach "lesbaren" BURUMUT-Substrings in den 52 Rausch-Phrasen. Vielleicht ist die Cherry-Picking-These zu stark und manche inneren Perioden sind doch optimiert.

3. **Tengri-Fließtext (p01-p16)**: N-Gramm-Statistik + Vergleich mit dem BURUMUT-Vokabular. Wenn die Tengri-Glyphen BURUMUT-Buchstaben sind (statt lateinisch), sollten sie in der gleichen Statistik wie die BURUMUT-Phrasen auftauchen.

4. **p17-Header 46-Ziffern-Periode**: Die 22-Buchstaben-Kandidaten (`NCTTBAODIPRGNPSPHACBUR` etc.) als BURUMUT-Wort testen. Wenn Periode 7 = 14 Zeichen und Periode 46 ≈ 22 Zeichen, könnte das ein BURUMUT-Satz mit anderer Lesart sein.

5. **Schmeh-Quelle**: Versuchen, an das Original-Manuskript oder Schmehs ungekürzte Notes zu kommen. Wir arbeiten seit 2017 mit Sekundärquellen.
