# Öffentliche Dekodierungen der Tengri137-Chiffre (2017)

**Zusammenstellung der externen, unabhängigen Lösungen.**

Diese Sammlung dokumentiert, was die **öffentliche Kryptographie-Community**
2017 unter Führung von Klaus Schmeh (Cipherbrain-Blog) zur Tengri137-Chiffre
beigetragen hat — **bevor unser Repo P1 begann**.

**Zweck:** Klarheit darüber, welche Befunde *wir* (P1–P76) gefunden haben
und welche *schon vorher* öffentlich dokumentiert waren. Apophenie-Schutz.

---

## Quellen-Übersicht

| Datum | Artikel / Quelle | Hauptbeitrag | Solver |
|---|---|---|---|
| 2016-08 | Anon. PDF (23 S.) | Original-Veröffentlichung | (Tengri 137 / 0x666ab731) |
| 2016-09-16 | Twitter @666ab731 | PGP-signierte Nachricht kündigt PDF an | Tengri 137 |
| 2017-01-29 | Schmeh, Cipherbrain | "Who can solve this encrypted book?" | Schmeh |
| 2017-03-08 | Schmeh, Cipherbrain | "How a blog reader solved..." | Klaus Tappeiner + Norbert Biermann + Michael |
| 2017-03-18 | Schmeh, Cipherbrain | "Tengri 137: 2nd challenge solved in days" | Norbert Biermann |
| 2017-03-30 | Schmeh, Cipherbrain | "Tengri 137 has posted again" | Thomas, citizenone |
| 2017 | Tengri137 Wikia | Lösung Seiten 1–16 (einfache Substitution) | Community |
| 2017 | Pastebin: PGP-Signaturen | Originalsignaturen von Tengri 137 | 0x666ab731 |
| 2017 | Pastebin: Gate-Botschaften | "Gate is open", "Second gate" | 0x666ab731 |
| 2017 | Reddit r/tengri137 | Hinweise auf .onion-Adresse, Arecibo-Bezug | tikitembo7, citizenone |

---

## Was die Community 2017 bereits gelöst hat

### Seiten 1–16 (Substitution)

Bereits vor Schmehs Januar-2017-Artikel gelöst.
- **Methode:** Monoalphabetische Substitution (geheimes Alphabet ↔ lateinisch)
- **Dokumentation:** Tengri137 Wikia
- **Klartext-Beispiel (Seite 1):** *„THIS CUBES ARE QUITE SIMPLE FOR US. NOW YOU CAN FIND OUT THE MEANING OF SOME OTHER FIGURES..."*
- **Status:** **Vollständig gelöst, vor unserem Repo.**

### Seiten 17–22 (Atom-Dekodierung via dcode.fr)

- **Methode:** Wiederholende Dezimalbrüche → Periodensystem der Elemente
  - Beispiel: 43=Tc→T, 77=Ir→I, 25=Mn→M, 63=Eu→E
  - Erste-Buchstabe-Substitution
- **Solver:** Klaus Tappeiner (Südtirol), mit Vorarbeit von Jim, Klaus Adami, Paolo Bonavoglia, Norbert Biermann
- **Klartext-Beispiel Seite 17 (Tappeiner):** *„TIME FOR THE TRUTH / OVER MANY THOUSAND YEARS WE SEND YOU MESSENGERS AND TEACHER / ALL THIS KNOWLEDGE BEHIND YOUR CIVILISATION IS OURS"*
- **Klartext-Beispiel Seite 18:** *„THE REARE PEOPLE AMONG YOU… WE ARE NOT YOUR GODS / YOU SHOULD KNOW THAT GOD DOES NOT EXIST"*
- **Status:** **Vollständig gelöst durch Community 2017.**

### Seite 23 (BURUMUT-Matrix)

- **Methode:** Periodensystem-Dezimalbrüche → 154 lateinische Buchstaben
- **Solver:** Norbert Biermann (Kommentar #15, #24 auf Schmehs Blog)
- **Resultat:** 11×14-Raster
  ```
  B U R U M U T R E F A M T U
  N U R E S U T R E G U M F A
  Y A P S U A Z B E H I M L A
  Z A N R U A Z B E N O M B A
  T O B I K O T L U B U M Y O
  S U N O K U R G A N O Z Y I
  O K U Z I K U F A U S I H E
  Y A B E K A N S A B E R H O
  N A F E R A N S A H O T F E
  K O R E M O R B I Z U M R O
  S U N A K I R F A N E M B A
  ```
- **Index of Coincidence:** 0.067 (≈ englisch, Thomas)
- **Status:** 2017 NICHT gelöst. **Norbert lieferte die Atomsubstitution, aber das ergab keinen Klartext. Michael (Kommentar #76) versuchte die Amino-Acid-Decodierung (siehe unten).**

### Amino-Acid-Decodierung (Michael, 2017)

- **Methode:** IUPAC-Ein-Buchstaben-Code für Aminosäuren
- **Mapping:**
  - B → Asx (Asparagin oder Asparaginsäure)
  - U → Sec (Selenocystein)
  - R → Arg (Arginin)
  - M → Met (Methionin)
  - T → Thr (Threonin)
  - E → Glu (Glutaminsäure)
  - F → Phe (Phenylalanin)
  - A → Ala (Alanin)
  - N → Asn (Asparagin)
  - S → Ser (Serin)
  - G → Gly (Glycin)
  - Y → Tyr (Tyrosin)
  - P → Pro (Prolin)
  - Z → Glx (Glutamin oder Glutaminsäure)
  - H → His (Histidin)
  - I → Ile (Isoleucin)
  - L → Leu (Leucin)
  - O → Pyl (Pyrrolysyl)
  - K → Lys (Lysin)
- **Status:** 2017 KEIN fertiger Klartext. Die Idee, BURUMUT als Aminosäuresequenz zu lesen, war 2017 bereits in der Community. **Was wir (P2) daraus machten: Selenoprotein-Hypothese mit 11 UGA-Codons und SECIS-Analyse.**

### Zweite Challenge (März 2017, Norbert Biermann)

- **Quelle:** PGP-signierte PGP-Mail, Pi Day (2017-03-14), MP3
- **Methode:** Spektrogramm → URL → WAV-Datei → Pulslängen 16/32/48... ms → Oktal (0-7) → 27 Buchstaben
- **Resultat:** Symbol-Sequenz beginnend mit „abccadefbgheijklmelndjecndeopcdebmekqdjerssstuvwxyzyz" + "AAxxAxxAAAxxAxx..." + "djhedjhedjh"
- **Klartext-Botschaft:** *„LITTLE BIRD KNOWS WHEN THE GATE IS OPEN"*

### Dritte Challenge (30. März 2017, 11×11-Würfel)

- **Quelle:** PGP-signierte Nachricht mit „NOTHING IS RANDOM"
- **Resultat:** 11×11-Raster, Header „U T M A F E R T U M U R U B"
- **Beobachtung (Thomas):** Inverse des BURUMUT-Würfels, jede Spalte enthält nur Vokale oder nur Konsonanten
- **Status:** 2017 ungelöst
- **Anschluss-Hinweis:** Thomas postete eine 6.448-Buchstaben-Geheimtext + Zahl 3151 = 23 × 137
- **Arecibo-Hinweis:** citizenone identifizierte die Nachricht als Variante der Arecibo-Botschaft
- **Bezug zu DNA/RNA:** Jim hatte schon im Januar 2017 die chemischen Diagramme auf Seite 23 als ACGT/ACGU identifiziert

### PGP-Schlüssel

- **Schlüssel-ID:** 0x666ab731
- **Name:** Tengri
- **Kommentar:** 137
- **Twitter:** @666ab731
- **Verifikation:** Alle Botschaften sind PGP-signiert (OpenPGP / GnuPG v2)

### Tor-.onion-Adresse (2017)

- **Adresse:** `666666m7x6x5regc.onion`
- **Bedeutung 666666m(7×6×5) = 666666 × 210 = ... 126 = Alex** (Nuclear Magic Number)
- **Status:** "LITTLE BIRD KNOWS WHEN THE GATE IS OPEN" — Reddit-Nutzer tikitembo7 hat Screenshot gepostet

---

## Was unser Repo P1–P76 beigetragen hat

| Befund | Phase | Stand vor uns |
|---|---|---|
| BURUMUT als lat. Sequenz extrahiert | P39 (Z.652–662) | Norbert 2017 |
| IUPAC-Amino-Acid-Mapping | (Biermann/Michael 2017) | 2017 |
| BURUMUT = 99 AS (korrekte Anzahl) | P2 | Biermann-Grid 11×14, aber NICHT in 99er-Sequenz |
| 11 UGA / 2 UAG Codons | P9 | nicht öffentlich |
| SECIS-Element-Analyse | P10 | nicht öffentlich |
| BLAST-Verifikation Adhäsion-GPCR | P11 | nicht öffentlich |
| Selenocystein-Hypothese | P2-P9 | nur als einzelner Buchstabe in Mapping erwähnt |
| 5-Layer-Tora-Turing-Maschine M4 | P30+ | nicht öffentlich |
| BURUMUTREFAMTU an Pos 15986 | (Quellen-Befund) | im Volltext gelesen, nicht entdeckt |
| 7-Tage-Architektur (168 = 7×24) | P60, P68 | nicht öffentlich |
| 19/22 Konsonanten First-Fail | P76 | nicht öffentlich |

**Wichtigste Klarstellung (P65a, korrigiert durch User):**
> „Die BURUMUTREFAMTU-Phrase steht **verbatim** in Tengri137. Sie wurde
> gelesen, nicht entdeckt. Das ist eine Quellen-Beobachtung, kein
> Decodierungs-Erfolg."

---

## Original-Dateien

Siehe in diesem Ordner:
- `schmeh_2017-01-29_first_article.md` — Schmehs erster Blog-Artikel
- `schmeh_2017-03-08_pages_17-22_solved.md` — Tappeiners Atom-Dekodierung
- `schmeh_2017-03-18_second_challenge.md` — Norberts 2. Challenge
- `schmeh_2017-03-30_third_challenge.md` — 11×11-Würfel
- `pastebin_messages.md` — PGP-signierte Originale
- `community_decoders.md` — Liste der Solver mit Beiträgen

---

*Zusammenstellung: PhiMind Investigator, 2026-07-03*
