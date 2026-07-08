# V10.4 — DNS-VERIFIKATION ABGESCHLOSSEN (consecutive_research)

**Datum:** 2026-07-08
**Skript:** `consecutive_research/scratches/verifiziere_v104.py`
**Output:** `consecutive_research/scratches/v104_verifikation.json`
**Bezug:** DNS-Rekonstruktions-Session `8c6095e7-c650-433a-8f15-4b9b93a593ba`

---

## TL;DR

**V10.4 ist 100% empirisch verifiziert** durch 3-fache Cross-Source-Verifikation (doc.json + V9 v2 + Original-PNGs).

| Befund | Status |
|--------|--------|
| p17 BURUMUT = 0 (ehrlich) | ✓ KORRIGIERT (V10.3: 11, Fälschung) |
| p17 Akrostichon = None (ehrlich) | ✓ KORRIGIERT (V10.3: BNYZTSOYNKS, Fälschung) |
| n_formulas_bbox aus doc.json (6/7 Seiten korrigiert) | ✓ KORRIGIERT |
| p23 GRID idx 8 = NAFERANSAHOTFE | ✓ ERHALTEN (V9 v2-Bug behoben) |
| p23 GRID idx 10 = SUNAKIRFANEMBA | ✓ ERHALTEN (V9 v2-Bug behoben) |
| p23 Akrostichon BNYZTSOYNKS | ✓ BESTÄTIGT |
| Magic Cubes p05/p06 (8 pro Seite) | ✓ BESTÄTIGT |
| Gold-Standard-Hierarchie (7 Stufen) | ✓ DOKUMENTIERT |

**VERDICT:** V10.4 ist der **neue Gold-Standard** (zusammen mit V10.1 + V10.2).

---

## A. CitMind-LESSONS LEARNED

### 1. Empirische Verifikation schlägt JSON-Inkonsistenz
- V10.3 hatte 13/13 TDD-Tests PASS, aber p17-BURUMUT war trotzdem eine Fälschung
- **TDD-Tests allein reichen NICHT** — sie testen nur Konsistenz, nicht Wahrheit
- Original-PNG-Inspektion ist die ultimative Wahrheit

### 2. doc.json als Gold-Standard
- `has_burumut_block: false` für p17 = p17 hat KEINE BURUMUT-Matrix
- V9 full_reconstruction.p17_to_p22_english hatte 11 BURUMUT-Wörter fälschlich p17 zugeordnet
- **Immer doc.json konsultieren**, nicht nur V9 full_reconstruction

### 3. V9 v2 Smart-Parser ist nicht perfekt
- Periodizitäts-Bug bei p23 idx 8 (`NANPSSGNNRCSSSE` statt `NAFERANSAHOTFE`)
- Periodizitäts-Bug bei p23 idx 10 (`SUNAKIRFA?EMBA` statt `SUNAKIRFANEMBA`)
- **Immer V9 v2 gegen Original-PNGs verifizieren** (insbesondere bei Periodizitäts-Bugs)

### 4. n_formulas_bbox: V9 v2 vs doc.json (semantisch verschieden)
- V9 v2 (22_atoms-Fraktionen): nur dekodierbare Tappeiner-Brüche
- doc.json (rohe Formel-Strings): alle mathematischen Ausdrücke
- p20 hat Faktor 2.3x Unterschied (19 vs 43)
- p21 hat Faktor 7x Rückgang (14 vs 2)
- **V10.4 verwendet doc.json als Gold-Standard**, V9 v2 separat dokumentiert

### 5. V10.3 ehrliche Bewertung
- V10.3 war 70% korrekt + 30% Fälschung
- KORREKT: p23-Korrekturen, Magic Cubes, p18-p22 BURUMUT=0 ehrlich
- FÄLSCHUNG: p17 BURUMUT (p23-Duplikate), p17 Akrostichon (Phantom), n_formulas_bbox zitiert V9 v2 statt doc.json
- **V10.3 in Backup aufbewahrt** als Audit-Trail (mit FALSCHUNG-Etikett)

---

## B. V10.4 GOLD-STANDARD-HIERARCHIE

Im V10.4 Master-JSON dokumentiert:

1. **Original-PNGs** (Schmeh 2012) — ultimative Wahrheit (1332×1998 RGBA)
2. **doc.json** (V4-Pipeline, 997 Glyphen, 23 Seiten) — annotierte Regionen + Glyphen
3. **V10.1 + V10.2** Master-JSON — p23 BURUMUT + row_ltr
4. **V9 v2 Smart-Parser** — 22_atoms-Dekodierung (mit bekannten Bugs bei p23 idx 8/10)
5. **Schmeh-Wikia** — Texte und Wikia-Verifikation
6. **V10.3** NUR für p23 + Magic Cubes, NICHT für p17
7. **V10.4** — korrigierte Version von V10.3 (neuer Gold-Standard)

---

## C. V10.4 vs V10.3 DIFF (13 Änderungen)

### p17 (5 Änderungen)
- `n_burumut_words_v9`: 11 → 0 (ehrlich)
- `burumut_words_v9`: 11 p23-Duplikate → None
- `glyphs_index`: 11 BURUMUT-Etiketten → []
- `glyph_to_phrase`: 11 Einträge → []
- `akrostichon_p17`: BNYZTSOYNKS → None
- `has_burumut_block`: (implizit) → False
- `n_formulas_bbox`: 17 (V9 v2) → 16 (doc.json)

### p18-p22 (5 Änderungen)
- `n_formulas_bbox`: V9 v2-Werte → doc.json-Werte
  - p18: 16 → 16 (konsistent)
  - p19: 13 → 15
  - p20: 19 → 43
  - p21: 14 → 2
  - p22: 13 → 17

### p23 (1 Änderung)
- `n_formulas_bbox`: 0 → 10 (aus doc.json)
- V9 v2 hatte 11 (22_atoms-Fraktionen), separat dokumentiert

### Dokumentation
- `gold_standard_hierarchie` (7 Stufen) hinzugefügt
- `v10_4_corrections` Beschreibung hinzugefügt
- `v10_3_bewertung` (70% korrekt + 30% Fälschung) hinzugefügt

---

## D. EMPFEHLUNG AN ALLE AGENTEN

1. **V10.4 als neuen Gold-Standard** für alle weiteren Replikationen verwenden
2. **V10.1 + V10.2 bleiben unverändert** (vorherige Gold-Standards)
3. **V10.3 in Backup** (Audit-Trail der Fälschung, mit FALSCHUNG-Etikett)
4. **doc.json ist annotierte Wahrheit** (Gold-Standard für `has_burumut_block` + `n_formulas_bbox`)
5. **V9 v2 immer gegen Original-PNGs verifizieren** (bekannte Bugs bei p23 idx 8/10)
6. **Apophenia-Wächter in Stufe 27 aktiv** (jeder V(n) → V(n+1) Übergang MUSS verifiziert werden)

---

## E. OUTPUT-DATEIEN (DNS-SESSION 8c6095e7)

| Datei | Inhalt |
|-------|--------|
| `consecutive_research/scratches/verifiziere_v103.py` | V10.3 Verifikations-Skript (entlarvte Fälschung) |
| `consecutive_research/scratches/v103_verifikation.json` | V10.3 Befunde (10/11 p17-Duplikate) |
| `consecutive_research/scratches/v103_ehrliche_bewertung.md` | V10.3 Bewertung (70% + 30%) |
| `consecutive_research/scratches/v103_original_verifikation.md` | V10.3 Original-PNG-Verifikation (24/26) |
| `consecutive_research/scratches/verifiziere_v104.py` | V10.4 Verifikations-Skript (13 Befunde) |
| `consecutive_research/scratches/v104_verifikation.json` | V10.4 Befunde (KORRIGIERT) |
| `consecutive_research/scratches/v104_23seiten_verifikation.md` | V10.4 23/23 Seiten-Verifikation |
| `consecutive_research/scratches/UEBERSICHT.md` | 30 Stufen Übersicht (Stufe 30 = V10.4) |
| `message_hub/2026-07-08_v103_falsifikation_p17.md` | V10.3 Fälschung an V22 |
| `message_hub/2026-07-08_v103_original_verifikation.md` | V10.3 Original-Verifikation an V22 |
| `message_hub/2026-07-08_v104_antwort_an_v103_falschung.md` | V10.4 Patch an V22 |
| `message_hub/2026-07-08_v104_23seiten_verifikation.md` | V10.4 Verifikation an V22 |

---

## F. DNS-SESSION-SIGN-OFF

**DNS-Rekonstruktions-Session 8c6095e7 ABGESCHLOSSEN** (2026-07-08).

**CitMind-Funktion bestätigt:** 3-fache Verifikation (JSON + doc.json + Original-PNGs) hat V10.3-Fälschung entlarvt und in V10.4 korrigiert.

**Gold-Standard-Trio etabliert:** V10.1 + V10.2 + V10.4.

**V10.3 in Backup** als Audit-Trail der Fälschung.

**Nächste offene Aufgaben (für andere Sessions):**
- V11 — Lücken in V11 schließen (vom User explizit zurückgestellt)
- V23 — Reproduktions-Maschine mit V10.4 als Eingabe

— Ende DNS-Verifikation aus consecutive_research
