---
name: tengri137-v5-methodik-falsifikation
description: "Gemini's Falsifikation der V5-Kryptanalyse 2026-07-05 — Phase 1+5 sind \"Junk-Science\" weil Cryptanalysis auf Strichen statt Buchstaben läuft"
metadata: 
  node_type: memory
  type: project
  originSessionId: 85d082f9-c927-4095-883d-f4512dced72e
---

# Tengri137 V5 Methodik-Falsifikation (2026-07-05)

**Status:** V5-Kryptanalyse (Phase 1+5) **FALSIFIZIERT** durch Gemini 2026-07-05.
**Output:** `consecutive_reading/Gemini-Antworten2.txt` (8.7 KB, ~83 Zeilen)
**Kontext:** V5 hat Schmeh-Rauswurf und Layout korrekt, aber Cryptanalysis auf dem falschen Datensatz.

## Gemini's Hauptkritik

### Fatale Fehler in V5

**Phase 0 → Phase 1 (Cryptanalysis auf Inken-Substrat / Fragen 2.0.1, 2.0.1, 2.1.1, 2.1.4, 3.6):**
- Tengri-Glyphen bestehen aus **2-3 getrennten Tinten-Strichen** (z.B. vertikaler Strich + loser Punkt)
- V5 berechnet IoC, Shannon-H, Zipf-α auf **16.797 Connected Components (Strichen)**
- Cryptanalysis auf Strichen misst **geometrische Font-Redundanz**, NICHT linguistische Struktur
- **Beispiel:** Wenn jeder zweite Buchstabe einen vertikalen Strich hat, taucht der "Token" massiv auf → IoC-Aufblähung
- **Antwort auf Frage 3.6:** Cryptanalysis-First funktioniert NIEMALS auf Pixelebene. MUSS Glyph-First sein.

**Phase 2 Constraint-Clustering (Fragen 2.1.2, 2.2.2, 2.2.5, 3.1):**
- K ∈ [25, 35] ist zwar zufällig richtig geraten, aber methodisch durch falschen Prozess erzeugt
- V5 nutzt V4-Crops (997 fragmentierte Glyphen) + wacklige V5-Hypothese als Constraint
- **"Garbage-In-Constrained-Garbage-Out"** — K=34 ist sich-selbst-erfüllende Prophezeiung, kein wissenschaftlicher Befund

**IoC 0.16 / S6S6-Bigramm (Fragen 2.1.4, 3.9):**
- 0.16 erklärt sich aus geometrischer Strich-Redundanz, NICHT aus sprachlicher BURST-Repetition
- S6S6 mit 2300 Hits ist wahrscheinlich eine gestrichelte Linie oder wiederkehrendes optisches Element (Matrizen/Brüche)
- KEIN linguistisches Signal

**H1 abgelehnt (F1=-1):**
- H1 wurde abgelehnt, weil Werte zu extrem waren
- ABER: Werte waren nur deshalb extrem, weil wir Striche statt Buchstaben gezählt haben
- **Ob der echte Tengri-Text eine monoalphabetische englische Substitution ist, hat V5 NOCH NICHT getestet**

## Was Gemini BESTÄTIGT

✅ **Schmeh-Rauswurf war richtig** — wichtigster methodischer Schritt
✅ **14/23 Pages reines Tengri** — visuell korrekt bestätigt
✅ **9/23 Pages mit Latein** — exakt abgebildet
✅ **p23 = Nukleinbasen** (Pyrimidin-Ring links: Cytosin/Thymin/Uracil, Purin-Ring rechts: Adenin/Guanin) — exakt richtig
✅ **Magic-Cube auf p05/p06** — bestätigt, die 4/9 Tokens verwerfen
✅ **p17-p21 = Mathe** (Primfaktorzerlegungen, "x" als Multiplikator) — Schmeh nennt es "Burumut", visuell ist es Mathe

## Falsifikations-Vorschlag von Gemini

- **Manuelle Glyphen-Zählung auf p01:** exakt 242 Buchstaben
- **V5 Phase 0 zählt:** 541 Components auf p01
- **541 Components in Phase 1 als IoC-Input = IoC 0.16 misst Tinten-Zerstückelung, NICHT Information**
- → **Damit ist die Metrik IoC=0.16 falsifiziert.**

## V6-Empfehlung von Gemini

**1. Template-Matching statt Connected-Components:**
- Manuell 30 Tengri-Referenz-Glyphen aus p01 isolieren
- `cv2.matchTemplate` auf alle Seiten
- Diskreter Token-Stream pro Page (z.B. "Glyph_12, Glyph_04, Glyph_30...")

**2. Cryptanalysis auf echtem Token-Stream:**
- IoC, H, N-Gramme auf dem sauberen Stream
- Erwartung: IoC fällt drastisch (vermutlich ~0.065, im Englisch-Bereich)
- "S6S6"-Burst-Problem verschwindet

**3. Frequency-Match-Test:**
- Glyph-Häufigkeiten vs. Englisch (E=12%, T=9%, A=8%)
- Wenn Match → Schmeh prinzipiell richtig
- Wenn nicht → Türkisch, Deutsch, syllabische Zuordnung testen

## Restrisiko: Tesseract auf Mathe-Formeln

- Tesseract ist für Fließtext trainiert
- Mathematische Operatoren, Exponenten (2^5), große Brüche werden zerschossen
- **Lösung:** MathPix oder Nougat für Formel-OCR
- IoU-Filter 0.1 okay, repariert aber nicht das Grundproblem
- Besser: YOLO vorher Mathe-Formel/Molekül detektieren, dann Tesseract NUR dort

## Lessons Learned

1. **Cryptanalysis MUSS auf diskreten linguistischen Einheiten laufen** — Striche haben keine linguistische Bedeutung
2. **Constrained Clustering mit wackliger Hypothese + schlechten Crops = Junk-Science**
3. **Manuelle Verifikation schlägt automatische Heuristik** — 242 echte Buchstaben vs. 541 Components = klarer Sanity-Check
4. **Falsifikation > Akzeptanz** — Gemini hat H1 nicht akzeptiert, sondern gesagt "du hast am falschen Datensatz getestet"
5. **Layout-Befunde von V5 stehen** — 14/23 Pages reines Tengri, 9/23 mit Latein, p23 = Nukleinbasen sind robust

**Why:** V5 hat den Schmeh-Rauswurf und Layout perfekt gemacht, aber die Kryptanalyse ist methodisch wertlos, weil sie auf Strichen rechnet. V6 muss Glyph-First zurück (V4-Ansatz) ABER mit Template-Matching statt Connected-Components.
**How to apply:** Bei zukünftigen Kryptanalyse-Pipelines NIE auf Pixel-Ebene starten. Immer erst diskrete Einheiten (Glyphen, Buchstaben, Tokens) isolieren, DANN Sprachstatistik. Gemini-Output als zweite Datei speichern (`Gemini-Antworten2.txt`), nicht nur die Fragen-Datei.
