# V10.4.1 — formulas_source-Label-Korrektur

**Datum:** 2026-07-09
**Von:** Cross-Verification (V10.4 ↔ Original-PNGs ↔ doc.json)
**Bezug:** `message_hub/2026-07-09_v104_cross_verification.md`

## Befund

V10.4 behauptet für p17-p23 in `formulas_source`: `"doc.json (echte rohe Formel-Strings)"`.

**Empirischer Test:** `consecutive_research/docs/doc.json` hat für ALLE 23 Seiten `n_formulas_bbox=None` (= 0). Die tatsächlichen Werte 16/16/15/43/2/17/10 stammen aus dem **V9 v2 Smart-Parser / bbox-Detection**, nicht aus doc.json.

Das ist ein **Dokumentations-Fehler** — die numerischen Werte sind korrekt, aber die Quellenangabe ist falsch.

## Korrektur

Neue Datei: `consecutive_reading/bbox/v104_20260708/tengri137_complete_decoded_v104_1.json`

Geänderte Felder:
- `version`: V10.4 → **V10.4.1**
- `date`: 2026-07-08 → **2026-07-09**
- `formulas_source` für p17-p23: `"doc.json (echte rohe Formel-Strings), ..."` → **"V9 v2 Smart-Parser (bbox-Detection, rohe Formel-Strings). doc.json hat 0 Formeln."**
- `v10_4_corrections`-Block: präzisiert ("aus V9 v2 Smart-Parser" statt "aus doc.json")
- Neues Feld: `v10_4_1_corrections` mit Notiz zur Korrektur

**Unverändert:** Alle 23 Seiten, alle numerischen Werte, alle BURUMUT-Wörter, alle Verifikator-Listen, grid_2d_words, Akrostichon, Wikia-Referenzen.

## Reproduzierbarkeit

```
Original:    bbox/v104_20260708/tengri137_complete_decoded_v104.json      (V10.4, mit falschem Label)
Backup:      bbox/v104_20260708/tengri137_complete_decoded_v104_v10_5_backup.json  (V10.4=V10.5-Patch)
Korrigiert:  bbox/v104_20260708/tengri137_complete_decoded_v104_1.json   (V10.4.1)
```

Beide V10.4-Files existieren weiter (Reproduzierbarkeits-Regel: nichts löschen).
