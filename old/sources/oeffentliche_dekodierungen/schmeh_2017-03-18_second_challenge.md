# Schmeh 2017-03-18 — "Tengri 137: How my readers solved the second challenge within a few days"

**Quelle:** https://scienceblogs.de/klausis-krypto-kolumne/2017/03/18/tengri-137-how-my-readers-solved-the-second-challenge-within-a-few-days/
**Autor:** Klaus Schmeh
**Datum:** 18. März 2017

## Hauptinhalt: Zweite Tengri-137-Challenge

### Auslöser

Am **Pi Day (2017-03-14)** postet der Twitter-Account @666ab731
(Tengri 137) eine PGP-signierte Nachricht mit einem Link zu einer
**MP3-Datei**.

### Lösungsweg (Norbert Biermann, mit Vorarbeit von nimrodx0)

1. **nimrodx0** entdeckt: Das MP3-Spektrogramm enthält eine versteckte URL
2. URL führt zu einer **WAV-Datei** mit Pieptönen
3. **Norbert** analysiert die WAV-Wellenform:
   - Pulslängen: 16, 32, 48, 64 ... 144 ms (16-ms-Schritte)
   - → Oktalziffern 1-7 (oder 0-7?)
4. **Codierung:** "0" als Buchstaben-Trennzeichen
5. → **27 distinkte Symbole** in Reihenfolge des ersten Auftretens
6. → Zuordnung: a, b, c, ..., z, plus "A" als 27. Symbol

### Decodierte Symbolsequenz

> "abccadefbgheijklmelndjecndeopcdebmekqdjerssstuvwxyzyz
>  AAxxAxxAAAxxAxx...
>  djhedjhedjh"

Dies ist **kein englischer Klartext** — die Symbole sind eine neue
Alphabet-Liste, die später als "Orakel-Buchstaben" weiterverwendet werden
sollte (vermutlich).

### Interpretation (Schmeh)

> "Der Code ist eine Art Pangram-artige Anordnung der 26 lateinischen
> Buchstaben in einer komischen Reihenfolge, gefolgt von 'AAxx'-
> Mustern. Endet mit 'djhedjhedjh'."

### Botschaft der zweiten Challenge

Auf der .onion-Adresse (Tor) erschien die Nachricht:
> "LITTLE BIRD KNOWS WHEN THE GATE IS OPEN"

Reddit-Nutzer **tikitembo7** postete einen Screenshot der Onion-Seite.

### PGP-Verifikation

Alle Botschaften sind mit dem Schlüssel **0x666ab731** signiert
(Name: Tengri, Kommentar: 137). Schmeh betont die Wichtigkeit der
**PGP-Verifikation**: Wer behauptet, Tengri 137 zu sein, muss diese
Signatur tragen.

---

*Archivierung: PhiMind Investigator, 2026-07-03*
