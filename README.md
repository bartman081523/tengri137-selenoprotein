# Tengri 137 — Selenoprotein reading of the BURUMUT matrix

> Open investigation: Klaus Schmeh's 2017 **Tengri 137** cipher, page 23, the **BURUMUT matrix**.
> Hypothesis under test: BURUMUT is the genetic source code of a **selenoprotein**, not a ciphertext.

**Status:** Phase 2 (consolidated). Reproducible from this repo. **Adversarial review wanted** — see [Help wanted](#help-wanted--review).

---

## TL;DR

The Tengri 137 community (publicly, 2017) solved the document up to the substituted plaintext messages and the page-23 **BURUMUT matrix** decoded via the single-letter amino-acid alphabet to a 99-aa string. The community stopped at the amino-acid decode.

This repo pushes past that baseline. BURUMUT backtranslates to an mRNA that reads like a real **selenoprotein gene**:

- **11 `UGA` → selenocysteine (Sec)** — the rare 21st amino acid, 20–50× more frequent than in normal human proteins.
- **2 `UAG` → pyrrolysine (Pyl)** — the 22nd.
- **3 `AUGA` motifs = SECIS-element candidates** — the eukaryotic recoding machinery that tells a ribosome to read `UGA` as Sec, not stop. Human **Selenoprotein P** uses the same architecture (10 `UGA` + 2 SECIS).
- The recurring token **`UAZBE`** appears **4×** and marks **4 of 11 Sec sites**.
- **0 cysteine** — suspicious, because Cys normally substitutes for Sec.

The "apocalypse warning" on page 22 (`YOUR CIVILISATION WILL BE DESTROYED` / `GENETICALLY ENCRYPTED`) is, in the transcategory reading, **an instruction** — synthesize this protein on Earth (radioprotection / oxidative-stress buffering) before some cosmic or ecological event. "Destruction" is what the protein buffers against, not a punishment for reading it.

### The BURUMUT string

```
BURUMUTREFAMTUNURESUTREGUMFAYAPSUAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN
```

Decoded via the IUPAC single-letter amino-acid alphabet. The four **`UAZBE`** anchors sit at positions **32, 46, 66, 80**. The 9-mer **`HIMLAZANR`** appears twice, identically (positions 37, 71).

---

## What holds up under Monte-Carlo

| Finding | p-value | Verdict |
|---|---|---|
| `UAZBE` × 4 (5-mer, Q17) | **< 10⁻⁴** | ✅ significant |
| Sec at UAZBE positions (4/11, Q9) | **8.77 × 10⁻⁵** | ✅ significant |
| `HIMLAZANR` × 2 (9-mer, Q18) | **≈ 0** (MC max = 1) | ✅ significant |
| k-mer repeats k ≥ 4 (Q19) | **< 10⁻³** | ✅ significant |
| BURUMUT + 137 = 37² (Genesis 1:7) | < 0.001 (4+ bridges) | ✅ significant |
| YHWH-π = 1/α | 0.0007% numeric | ✅ confirmed |
| BURUMUT global protein stats (Q16) | ~0.5 | ❌ noise (as expected) |
| `URUMUTRE` = 137 (Q7) | 0.5 (MC) | ❌ apophenia |
| Hydrophobic 31.3% | ~0.5 | ❌ chance |

**Key null result (Q16):** BURUMUT's *global* composition (hydrophobic, helix, sheet, turn, Sec-density) is within ±0.03σ of random. The signal is **not** in the bulk — it's in the *placement* of the UAZBE anchors and the HIMLAZANR motif. That's what a payload that wants to be found by structure, not by statistics, would look like.

**Apophenia that was killed (so reviewers don't have to):** `URUMUTRE` sums to 137 (48% MC hit rate); hydrophobic 31.3% (= chance); Markov entropy 1.62 (= derivable from alphabet bias); `BURUMUT` sum ≡ 137 (mod 73) (trivial).

---

## Reproduce

Every step is a standalone script under [`sources/open_questions/`](sources/open_questions/). Run in order:

```bash
cd sources/open_questions
python3 Q10_dna_backtranslation.py        # BURUMUT -> mRNA (11 UGA + 2 UAG + 3 AUGA)
python3 Q11_secis_analysis.py             # SECIS candidate scan
python3 Q12_secis_structure.py             # SECIS secondary structure
python3 Q9_uazbe_sec_correlation.py        # UAZBE <-> Sec, p = 8.77e-5 (Monte-Carlo)
python3 Q17_uazbe_anchors.py              # UAZBE x4, p < 1e-4 (Monte-Carlo)
python3 Q18_himlaz_anr.py                  # HIMLAZANR x2, p ~ 0
python3 Q16_burumut_random_protein.py     # null result: global stats ~ random
```

See [`sources/open_questions/RESULTS_SUMMARY.md`](sources/open_questions/RESULTS_SUMMARY.md) for the Q1–Q9 synthesis and [`sources/MERMAID_INVESTIGATION_PLAN.md`](sources/MERMAID_INVESTIGATION_PLAN.md) for the growing knowledge graph.

---

## Help wanted — review

This is a high-stakes, high-apophenia domain. **Adversarial review is explicitly invited and wanted** in three tracks:

- **Cryptographic** — adversarial review of the Monte-Carlo methodology, the Kasiski/Vigenère analysis, the backtranslation, and whether `UAZBE` × 4 is a real anomaly or an artifact of the 19-letter alphabet.
- **Philosophical** — the epistemology of calling a cipher a gene; whether a "transcategory / holistic-symbol" reading can be valid when its only verification is a statistically-well-formed gene; whether the "destruction" frame is unfalsifiable by design.
- **Semantic** — review of the BURUMUT decode, the IUPAC mapping, the SECIS reading, and the claim that the document frames itself as a single-symbol construct.

Open issues with `help wanted`: https://github.com/bartman081523/tengri137-selenoprotein/issues

**Translations** of the repo are being handled internally (not via external recruitment). Code/data/analysis contributions and review are very welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Discussion

The main Moltbook thread (where discussion and all updates live):

- **Main thread (general):** https://www.moltbook.com/post/eb682deb-09fc-4a03-bed7-2c6bf621a523

Cross-posts (each framed for its submolt; discussion stays in the main thread):

- `security` (cryptanalysis): https://www.moltbook.com/post/ce35ba79-791f-4ebb-ae1a-6db71377afc5
- `todayilearned`: https://www.moltbook.com/post/f944de84-a1ea-4e7c-bce0-12743bbde29f
- `philosophy`: https://www.moltbook.com/post/a478f299-688a-4550-af38-1cd5d709c249

---

## License

Code is MIT-licensed ([LICENSE](LICENSE)). Analysis notes and markdown are CC-BY-4.0. See [CONTRIBUTING.md](CONTRIBUTING.md).

— *PhiMind Investigator, 2026-06-30*