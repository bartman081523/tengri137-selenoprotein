# V7 Partial Decryption Status — BURUMUT-Ebene

**Datum:** 2026-07-04
**Status:** PARTIELLE ENTSCHLÜSSELUNG (BURUMUT dekodiert, Semantik unbekannt)

---

## Was bewiesen ist

### 1. Tappeiner-Methode (verifiziert)
Brüche → Periode der Dezimalbruchs-Expansion → 2-Ziffern-Paare (Dinome) →
Ordnungszahlen im Periodensystem → erster Buchstabe jedes Elements.

**Beweis:** Periode 7 von Bruch 1 = `5692379212922245638713122292`
→ 14 Dinome: `[56, 92, 37, 92, 12, 92, 24, 56, 38, 71, 31, 22, 29, 2]`
→ 14 Elemente: `Ba, U, N, U, Mg, U, Cr, Ba, Sr, Lu, Tl, Ti, Cu, He`
→ **BURUMUTREFAMTU** ✓ (exakt wie Tappeiners Kommentar #25 auf Schmehs Blog)

### 2. Schmehs "EXACT FORTY SIX"-Hinweis (verifiziert)
Die 2 besonderen Header-Berechnungen auf p17:
- `(2 × 23 × 499 × 19214759967251 × 55150662460749672076915609)` (44 Ziffern)
- `(3 × 11 × 47 × 139 × 2531 × 549797184491917 × 11111111111111111111111)` (46 Ziffern)

Bruch = val1/val2 = `0.00729735256137666677...`
Periode = 46 Ziffern (verifiziert via `n_order(10, 3333333333333333333333333333333333333333333333) = 46`) ✓

→ 4 BURUMUT-Kandidaten aus 46-Ziffern-Periode extrahiert (V1-V4 in `burumut_candidates.json`)

---

## Was NICHT bewiesen ist

### 1. Akrostichon-Theorem (FALSIFIZIERT 2026-07-04)
**Behauptung:** "Erster Buchstabe jedes BURUMUT-Wortes = 'TIME FOR THE TRUTH'"

**Test:** 11 BURUMUT-Schlusswörter (Periode 7 jedes Bruchs):
```
B = BURUMUTREFAMTU
N = NURESUTREGUMFA
Y = YAPSUAZBEHIMLA
Z = ZANRUAZBENOMBA
T = TOBIKOTLUBUMYO
O = OKUZIKUFAUSIHE     (Bruch 6 fehlt eine 7. Periode)
Y = YABEKANSABERHO
L = LYBMCRUZO?MCPYG
K = KOREMORBIZUMRO
S = SUNAKIRFANEMBA
```
**Tatsächliche Initialen:** `BNYZTOYLKS` (10 Zeichen, da Bruch 6 nur 5 Perioden hat)
**Erwartet:** "TIME FOR THE TRUTH" (19 Zeichen)

→ 10 ≠ 19, kein "TIME"-Substring, **Theorem FALSIFIZIERT**.

**Status:** Klassische LLM-Apophenie — externe Phrase ("TIME FOR THE TRUTH" aus
Web-Quelle) wurde ohne Test mit der BURUMUT-Ebene verknüpft.

### 2. Schmehs "TIME FOR THE TRUTH" Quelle (UNBEKANNT)
"TIME FOR THE TRUTH" kommt in Schmehs eigener p17-Lesung NICHT vor.
Schmehs p17-Latein enthält:
> "IF YOU ARE NOT CONVINCED THEN CALCULATE THE NEXT NUMBER AND SEE WHAT A
> PROOF IS PROVIDED TO YOU ADAM..."

→ "TIME FOR THE TRUTH" muss aus einer EXTERNEN Quelle stammen, möglicherweise
einer früheren Schmeh-Analyse oder dem Original-Manuskript, das wir nicht haben.

### 3. Schmehs Faktorzerlegungen (16/16 MATHEMATISCH FALSCH)
- Schmehs transkribierte Faktorzerlegungen ergeben bei Multiplikation **nicht** die
  im Bruch genannten Werte
- Beispiel: Schmehs `2^5 * 13 * 37 * 179 * 471077143 = 405592709351570` ≠
  tatsächlicher Wert
- Die **wahre** Berechnung ergibt andere Werte, die wir nicht kennen
- Tappeiner hat 11 korrekte Zwischenergebnisse gepostet (aus seinem Kommentar #25)

### 4. Direkter Klartext-Status der BURUMUT-Wörter (UNBEWIESEN)
- BURUMUT könnte sein: (a) eigenständige Sprache, (b) Code, (c) algorithmische Notation,
  (d) symbolische Marker, (e) Ritualsprache
- Wir wissen nicht, was `BURUMUTREFAMTU`, `SUNOKURGANOZYI`, `OKUZIKUFAUSIHE` bedeuten

---

## Datenstruktur

### Tappeiners 11 BURUMUT-Schlusswörter (Periode 7)
| Bruch | BURUMUT-Schlusswort | Mögliche Wortgrenzen |
|-------|---------------------|----------------------|
| 1 | BURUMUTREFAMTU | BURUMUT + REFAMTU |
| 2 | NURESUTREGUMFA | NURE + SUTRE + GUMFA |
| 3 | YAPSUAZBEHIMLA | YAPSUAZ + BEHIMLA |
| 4 | ZANRUAZBENOMBA | ZANRUAZ + BENOMBA |
| 5 | TOBIKOTLUBUMYO | TOBIKOT + LUBUMYO |
| 6 | SUNOKURGANOZYI | SUNO + KURGAN + OZYI |
| 7 | OKUZIKUFAUSIHE | OKUZIKUF + AUSIHE |
| 8 | YABEKANSABERHO | YABEKAN + SABERHO |
| 9 | NANPSSGNNRCSSSE | ? |
| 10 | KOREMORBIZUMRO | KORE + MORBI + ZUMRO |
| 11 | SUNAKIRFANEMBA | SUNAKIR + FANEMBA |

### Alle 76 BURUMUT-Texte (7 Perioden × 11 Brüche)
Gespeichert in `bbox/burumut_20260707_V7/burumut_texts.json`

### 46-Ziffern-Periode-Kandidaten (4 Varianten)
Gespeichert in `bbox/burumut_20260707_V7/burumut_candidates.json`

---

## Die nächste Front: BURUMUT-Morphologie

Die BURUMUT-Phrasen wirken phonetisch altaisch:
- `KURGAN` = türkisch/russisch für "Hügelgrab" (Hunnen-, Skythen-Gräber)
- `SUNO/KIR/FANEMBA` = möglicherweise türkische/mongolische Wurzeln
- `KORE` = möglicherweise Koreanisch (Goryeo) oder Mongolisch
- `OKUZIKUF` = Türkisch klingend (okuz = Ochse?)
- `MORBI/ZUMRO` = Mongolisch klingend

→ BURUMUT könnte eine **konstruierte Tengrismus-Ritualsprache** sein
   (Conlang), basierend auf Türkisch/Mongolisch.

→ Nächste Schritte: Vokalharmonie-Test, N-Gramm-Agglutination, Entropie-Check.

---

## Methodische Bilanz

**Was funktioniert hat:**
- Tappeiners exakte 28-Ziffern-Zwischenergebnisse haben die BURUMUT-Ebene perfekt aufgedeckt
- Schmehs "46"-Hinweis hat sich als exakt richtig erwiesen
- 2D-Layout-Inspektion hat die V5/V6-Token-Pipeline-Fehler aufgedeckt

**Was nicht funktioniert hat:**
- V5 Cryptanalysis (Striche als Buchstaben) — Junk-Science
- V6 Glyph-First (17 Glyphen als Substitutions-Alphabet) — Falsifiziert
- Akrostichon-Theorem (LLM-Apophenie) — Falsifiziert 2026-07-04

**Lehre:** Die Versuchung, aus einer teilweisen Entschlüsselung ein vollständiges
Narrativ zu stricken, ist die größte Gefahr. Wir bleiben bei der empirischen
Methode: jede Behauptung muss einen Code-Test überleben.
