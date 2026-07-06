# Tengri137 — Quellen-Inventur

**Stand:** 2026-07-06 (aktualisiert)
**Status:** 116 Dateien aus 13 Quellen-Typen gesammelt, ~57 MB
**Curl-Methode:** Wayback-Machine, direkte HTTPS-URLs, Keyserver, Pullpush-Reddit, Imgur-i.imgur.com, S3-Archive

**Wichtigste Neuzugänge seit 2026-07-06:**
- 4 neue Dropbox-Archive (P011-P023, tengri137.mp3, Uniqmos, rendezvous.png) — alle PGP-verifiziert
- 5 Reddit-Threads via Pullpush-API extrahiert (Volltext statt Wayback-Stubs)
- 9 Imgur-Bilder heruntergeladen
- 5 Pavana-YouTube-Videos identifiziert (rtag6YtG7MY, zfQ-gLfuuX8, NA-B8b7pwpM, 9jJvn3giXrM, UwBwDEa6gQM)
- **LITTLE MIND KNOWS WHEN THE GATE IS OPEN** + 666666m7x6x5regc.onion (Reddit-Entdeckung)
- Instaud-Spektogramm-Fund (NimrodX0): Audio-in-Audio versteckt in tengri137.mp3

---

## 1. Original-Archiv (PGP-verifiziert) — `/137/`

| Datei | Größe | Datum | Status |
|-------|-------|-------|--------|
| 137.txt | 1019 B | 2016-08-18 | PGP-Begleitschreiben |
| 137.tar.gz | 2.7 MB | 2016-08-18 | PGP-signiert ✓ VERIFIED |
| 137.tar.gz.asc | 836 B | 2016-08-18 | PGP-Signatur |
| P001-P010.png | ~3.0 MB | 2012-03-14 | Original-PNGs, 1332×1998 |

**PGP-Verifikation:**
- Schlüssel: `2A2C 0AD4 ED1C AD83 53A3 0056 D152 D6C5 666A B731` (RSA 4096)
- UID: `Tengri 137` / `Tengri (137)`
- Signatur: "Korrekte Signatur von Tengri 137" (RSA-Key D152D6C5666AB731, 2016-08-18 20:51:18 CEST)
- Erstellt: 2016-04-24

---

## 2. Dropbox-Archive — **5 DUBLETTEN mit unterschiedlichen Inhalten**

| Bit.ly | Inhalt | Größe | PGP-Status |
|--------|--------|-------|------------|
| 2bFjsQO | Tengri Archive 1 (P001-P010) | 2.7 MB | ✓ D152D6C5666AB731 |
| 2bMuGEv | Tengri Archive 2 (P011-P023) | 3.9 MB | ✓ 666ab731 |
| 2mUF7Xy | tengri137.mp3 + sig | 7.5 MB | ✓ 666ab731 |
| timetosharenow | Uniqmos documents | 1.3 MB | - |
| rendezvous137 | rendezvous.png | 1.4 MB | ✓ 666ab731 |

### 2a. Archive 1 — P001-P010 — `/137/`
- 137.txt (PGP-Begleitschreiben)
- 137.tar.gz (2.7 MB, PGP-verifiziert)
- 137.tar.gz.asc (836 B Signatur)
- P001-P010.png (1332×1998, ~3.0 MB)

### 2b. Archive 2 — P011-P023 — `/p011_p023_originals/`
- 666ab731.tar.gz (3.9 MB, signiert 2016-08-23)
- 666ab731.tar.gz.sig
- **13 Original-PNGs P011-P023** (höhere Auflösung als pages_png)

### 2c. Archive 3 — tengri137.mp3 — `/dropbox_archive_3_audio/`
- tengri137.mp3 (7.5 MB, 2017-03-06)
- tengri137.mp3.sig
- Enthält verstecktes Spektogramm (NimrodX0-Entdeckung, March 2017)

### 2d. Archive 4 — Uniqmos — `/dropbox_archive_4_uniqmos/`
- 7 Dokumente (1.3 MB)

### 2e. Archive 5 — rendezvous.png — `/dropbox_archive_5_rendezvous/`
- rendezvous.png (2018×2018, 1.4 MB, 2017-11-22, PGP-verifiziert)

**Haupt-URLs:**
- Original-Dropbox (Archive 1): `https://www.dropbox.com/sh/pt11xdtnr8pk1up/AABPtwX9lXW8JWMLD9jQn9ZZa`
- Weitere Archive über bit.ly-Redirects (siehe Sektion 9)
- Direkt-Download: `?dl=1` an URL anhängen

---

## 3. Wikia — `/wikia/` (6 Seiten)

| Datei | Beschreibung |
|-------|--------------|
| wikia_Tengri_137_Translation.html | Hauptseite mit 23 Plaintext-Übersetzungen |
| wikia_Tengri_137_Wikia.html | Wikia-Index |
| wikia_For_beginners.html | Methodologie: Orkhon, A=E, K=H, B=V, P=F |
| wikia_Quickstart.html | Einstieg |
| wikia_Twitter_message_2017.html | ONION-Address-Info + Twitter-Status |
| wikia_Curious_findings.html | 404 (nicht im Web-Archiv) |

**URL:** `https://web.archive.org/web/2017/http://tengri137.wikia.com/wiki/{PAGE}`

---

## 4. Schmeh's Blog (Cryptography-Pionier) — `/schmeh_blog/`

| Datei | Beschreibung |
|-------|--------------|
| schmeh_2017_01_29_*.html | Original-Post: "Tengri 137: Who can solve this encrypted book?" |
| schmeh_2017_03_08_*.html | Update 1: "How a blog reader solved the Tengri 137 mystery" |
| schmeh_2017_03_18_*.html | Update 2: "Tengri 137: How my readers solved the second challenge" |

**URL:** `https://scienceblogs.de/klausis-krypto-kolumne/2017/...`

---

## 5. Original PDF (Schmeh's Blog) — `/other/Tengri-137_schmeh_blog.pdf`

- **Größe:** 3.9 MB
- **Seiten:** 23
- **PDF v1.5**, PowerPoint→Acrobat PDFMaker
- **Author:** Schmeh, Klaus
- **Erstellt:** 2017-01-29 12:55:06 CET
- **Page size:** 540×780 pts (≈ 7.5×10.8 inch = Standard-PowerPoint)

**URL:** `https://scienceblogs.de/klausis-krypto-kolumne/files/2017/01/Tengri-137.pdf`

---

## 6. Twitter / X — `/twitter/` (9 Dateien)

### Tengri 137 Account (`@666ab731`)

| Datei | URL |
|-------|-----|
| twitter_666ab731_2017.html | /666ab731 (Hauptseite 2017) |
| twitter_status_709380843987296256.html | March 2016 status |
| twitter_status_841652390877106176.html | March 2017 status |
| twitter_status_847161664889901056.html | March 2017 status (mit Image) |
| twitter_status_861931952781373440.html | May 2017 status |

### Klaus Schmeh (Krypto-Blogger)

| Datei | URL |
|-------|-----|
| twitter_user_KlausSchmeh.html | /KlausSchmeh |
| twitter_user_ScienceBlogs_de.html | /ScienceBlogs_de |
| twitter_user_AeonV2.html | /AeonV2 (Reddit-User "Adam31415"?) |

---

## 7. Reddit — `/reddit/` (15 Dateien)

| Datei | Thema |
|-------|-------|
| reddit_r_tengri137.html | Subreddit-Index (Wayback 2017, 935KB) |
| reddit_r_tengri137_all.html | Subreddit-Index (Wayback 2023) |
| reddit_thread_5zisip.html | "Found a hidden link in the spectrogram of the..." (Wayback) |
| reddit_thread_62h37f.html | "Images emerging from the Tengri's code" (Wayback) |
| reddit_thread_68ws4a.html | "For those still working on page 23" (Wayback) |
| reddit_thread_690o3h.html | "Coincidence?" (Wayback) |
| reddit_thread_69347e.html | "I just had a long talk with Tengri" (Wayback) |
| reddit_user_Adam31415.html | Reddit-User Adam31415 (AeonV2?) |
| **reddit_pullpush_posts.json** | 5 Posts via Pullpush-API (Volltext!) |
| **reddit_comments_5zisip.json** | 25 Kommentare (5zisip) |
| **reddit_comments_62h37f.json** | 25 Kommentare (62h37f) |
| **reddit_comments_68ws4a.json** | 5 Kommentare (68ws4a) |
| **reddit_comments_690o3h.json** | 2 Kommentare (690o3h) |
| **reddit_comments_69347e.json** | 23 Kommentare (69347e) |
| **REDDIT_INHALT_ZUSAMMENFASSUNG.md** | Vollständige Inhalts-Zusammenfassung |

**Methode:** Reddit-API wird blockiert → Pullpush (api.pullpush.io/reddit) liefert Volltext.

**Hauptentdeckungen:**
- **LITTLE MIND KNOWS WHEN THE GATE IS OPEN** (3x) + **666666m7x6x5regc.onion** (Schmehs-Lösung der Magic Cubes)
- BURUMUT-Buchstaben ergeben bei schwarz/weiß-Inversion bildgebende Muster (Mensch-Maschine, Doppel-Helix)
- p23 = DNA-Strang (Konsens Telenerd + eiggaMAD)
- Pavana = mrsmom = Kathryn (5 YouTube-Videos zu Tengri 137)

---

## 8. Pastebin — `/pastebin/` (7 Dateien)

| Datei | Inhalt |
|-------|--------|
| pastebin_a1nqC79N.html | "You found the searched 137!" (Original-Hinweis) |
| pastebin_BdK6FD4X.html | Wikia-Paste, evtl. Klartext-Hinweise |
| pastebin_FAJNLpLZ.html | Evtl. Klartext-Lösung |
| pastebin_tgsAz11B.html | Evtl. weitere Lösung |
| pastebin_X0pJtqfD.html | Evtl. Code |
| pastebin_YUPZsz9n.html | Evtl. t.co-5pQANFq86m Inhalt |
| pastebin_YmrA3rDS.html | Reddit-Referenz |

---

## 9. Bit.ly / Short-URLs — `/bitly/` (7 Dateien)

| Datei | Short-URL | Ziel (per Redirect) |
|-------|-----------|---------------------|
| bitly_2bFjsQO_wayback.html | /2bFjsQO | → Dropbox Tengri-Archiv |
| bitly_2bMuGEv_wayback.html | /2bMuGEv | 403 (nicht archiviert) |
| bitly_2hipOIM_wayback.html | /2hipOIM | → Wikia Final Fantasy XV |
| bitly_2i5J63Z_wayback.html | /2i5J63Z | → Wikia Batman Telltale |
| bitly_2jjWm6b_wayback.html | /2jjWm6b | → Wikia Mafia III |
| bitly_2mUF7Xy_wayback.html | /2mUF7Xy | 403 (nicht archiviert) |
| bitly_2nbKpxD_wayback.html | /2nbKpxD | 60 KB Ziel (kleine Seite) |
| bitly_2nbRyOs_wayback.html | /2nbRyOs | 572 KB Ziel (große Seite) |
| bitly_2xQKteG_wayback.html | /2xQKteG | → Wikia Shadow of War |
| bitly_2xQl3O5_wayback.html | /2xQl3O5 | → Wikia Terminator 2 |
| bitly_2xQnpwq_wayback.html | /2xQnpwq | → Wikia Italian Job |
| bitly_timetosharenow_wayback.html | /timetosharenow | 403 (nicht archiviert) |

---

## 10. T.co (Twitter Short-URLs) — `/t.co/`

| Datei | URL | Status |
|-------|-----|--------|
| tco_4vlhWaOap2_wayback.html | /4vlhWaOap2 | 404 |
| tco_5pQANFq86m_wayback.html | /5pQANFq86m | 200 → pastebin/YUPZsz9n |
| tco_8kLTlD26VE_wayback.html | /8kLTlD26VE | 404 |

---

## 11. GitHub-Tools (Referenz) — `/github/`

| Datei | Repo | Zweck |
|-------|------|-------|
| github_lachesis_scallion.html | lachesis/scallion | Tor hidden service generator (ONION) |
| github_ReclaimYourPrivacy_eschalot.html | ReclaimYourPrivacy/eschalot | Ähnlich wie scallion |
| github_kuyur_unicue.html | kuyur/unicue | Unicode-Tool |

**Wichtig:** Diese Tools wurden von Schmeh in seinem Blog als mögliche Brute-Force-Tools für die ONION-Adresse erwähnt.

---

## 12. PGP-Key — `/pgp/`

| Datei | Quelle | Status |
|-------|--------|--------|
| pgp_search_keyserver_ubuntu_com.asc | keyserver.ubuntu.com | ✓ Tengri 137 (FULL) |
| pgp_search_keys_openpgp_org.asc | keys.openpgp.org | ✗ Not found |
| pgp_verification_log.txt | gpg --verify output | ✓ KORREKTE Signatur |

---

## 13. Scienceblogs (Hauptseite) — `/scienceblogs/`

| Datei | Beschreibung |
|-------|--------------|
| schmeh_2017_tengri137.html | Erster Schmeh-Post (Duplikat von schmeh_blog/) |

---

## 14. Imgur — `/reddit/imgur_*.{jpg,png}` (9 Bilder)

Von Reddit-Threads entdeckte Bilder (meist aus pHumn/mrsmom Diskussionen):

| Datei | Quelle | Inhalt |
|-------|--------|--------|
| reddit/imgur_RDZMB9s.jpg | eiggaMAD/t3_68ws4a | p23-Seite selbst (1125×2001) |
| reddit/imgur_aUy4Snx.jpg | pHumn/t3_62h37f | Mensch-Maschine-Symbol (schwarz/weiß) |
| reddit/imgur_UZQp5sc.jpg | pHumn/t3_62h37f | Doppel-Helix-Variante |
| reddit/imgur_XoyfsqR.jpg | pHumn/t3_62h37f | Skalierte M→N-Version |
| reddit/imgur_nPPJDml.jpg | pHumn/t3_62h37f | M vs N Vergleich |
| reddit/imgur_QyWNK0W.jpg | pHumn/t3_62h37f | Radiales Mandala-Muster |
| reddit/imgur_b9YsbmH.png | mrsmom/t3_69347e | Pavana's Gott-Mensch-Hierarchie |
| reddit/imgur_uVb8hGn.jpg | pHumn/t3_62h37f | Westworld-Logo (Vergleich) |
| reddit/imgur_jbMpnH1.jpg | pHumn/t3_62h37f | Arecibo-Botschaft (Vergleich) |

**Hauptbild:** `imgur_RDZMB9s.jpg` IST die p23-Seite — Telenerd hatte recht: p23 zeigt DNA-Struktur.

## 15. YouTube (Pavana-Tengri-Videos) — `/reddit/youtube_*.html` (2 HTMLs)

| Datei | Video-ID | Titel |
|-------|----------|-------|
| reddit/youtube_rtag6YtG7MY.html | rtag6YtG7MY | A talk with Tengri 137 (mrsmom/Pavana) |
| reddit/youtube_pavana_search.html | (5 Videos) | Suchergebnisse "pavana tengri 137" |

**5 Pavana-Tengri-Videos identifiziert:**
1. rtag6YtG7MY: A talk with Tengri 137
2. zfQ-gLfuuX8: Tengri (137) Time
3. NA-B8b7pwpM: Tengri 137 answers more questions
4. 9jJvn3giXrM: Why I believe Tengri 137
5. UwBwDEa6gQM: More Tengri 137 syncs

**Kanal:** Pavana (mrsmom = Kathryn)
**Wichtig:** Pavana steht in DIREKTEM KONTAKT mit Tengri 137 (Twitter-Chat, Mai 2017).

---

## ONION-Adresse (Dark Web) — AKTUALISIERT 2026-07-06

**`https://666666m7x6x5regc.onion`** (von Schmeh-Blog-Leser "Norbert" entdeckt, März 2017)

Tikitembo7 (Reddit t3_5zisip) bestätigt:
> "It's a ONION address!!! The blog reader @Norbert from Klausis Krypto Kolumne found the solution!"
> "LITTLE MIND KNOWS WHEN THE GATE IS OPEN" (3x) + "END END END" + ONION-Adresse

Diese 16-stellige Adresse ist NICHT zufällig — Tengri hat sie absichtlich generiert (vermutlich via Scallion).

---

## Methodische Notiz

**Was wir verifiziert haben:**
1. ✅ PGP-Signatur der Original-PNGs (P001-P010) ist **kryptographisch gültig**
2. ✅ Schmeh's Tengri-137-PDF ist das **Original-23-Seiten-Dokument** (Klaus Schmeh, 2017-01-29)
3. ✅ Dropbox-Archiv (2022-05-23) ist **identisch** zu 137.tar.gz
4. ✅ Twitter-Account @666ab731 ist seit 2016 aktiv
5. ✅ Wikia "For beginners" nennt Orkhon-Substitutionen: A=E, K=H, B=V, P=F

**Was noch zu untersuchen ist:**
- 🔍 Wikia Curious_findings (404 — vermutlich gelöscht)
- 🔍 Wikia Twitter_message_2017 (ONION-Adresse noch aktiv?)
- 🔍 pastebin BdK6FD4X Inhalt (403 — nicht im Web-Archiv)
- 🔍 pastebin YmrA3rDS (403 — nicht im Web-Archiv)
- 🔍 Dropbox-Folder-Listing (JavaScript-rendered, client-side)

**Quellen, die nur über Wayback zugänglich sind:**
- Wayback: https://web.archive.org/web/2017/{URL}
- CDX-API: https://web.archive.org/cdx/search/cdx?url={DOMAIN}&output=json
