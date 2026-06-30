# Contributing

This is an open investigation into Klaus Schmeh's Tengri 137 cipher. The domain is
high-stakes and high-apophenia — almost anything 137-adjacent and amino-acid-coded
*looks* a bit gene-like. The most valuable contribution is **adversarial review**,
not confirmation.

## What is wanted

Three review tracks (see the `help wanted` issues):

1. **Cryptographic review** — Monte-Carlo methodology, Kasiski/Vigenère analysis,
   the BURUMUT → mRNA backtranslation, the SECIS candidate scan. Specifically:
   is `UAZBE` × 4 a real anomaly or an artifact of the 19-letter alphabet and
   its letter frequencies?
2. **Philosophical review** — the epistemology of calling a cipher a gene. Can a
   "transcategory / holistic-symbol" reading be valid when its only verification
   is a statistically-well-formed gene? Is the "destruction" frame unfalsifiable
   by design?
3. **Semantic review** — the BURUMUT decode, the IUPAC single-letter mapping, the
   SECIS reading, the claim that the document frames itself as a single-symbol
   construct.

## How to submit a review

- **Prefer an issue** for anything that could change the conclusion (a methodological
  flaw, a refutation of a p-value, an alternative explanation). Reference the
  specific script (`sources/open_questions/Q*.py`) and the finding.
- **Prefer a PR** for concrete fixes: a corrected Monte-Carlo, an additional null
  model, a refactored script, a missing control. Keep changes reproducible.
- For a *new* analysis (a new Q), add a standalone `sources/open_questions/Q<n>_*.py`
  following the existing naming, and update `RESULTS_SUMMARY.md` and the mermaid plan.

## Reproducibility rules (from this repo's house style)

- Every factual claim ties to a specific `file:line` or a script output. A claim
  with no source is a hypothesis — label it as such.
- Monte-Carlo is essential for any "this is unusual" claim. State `n`, the null
  model, the statistic, and the p-value.
- Distinguish **significant** (p < 0.001, ideally 3+ independent lines) from
  **apophenia** (p ≈ 0.5). Both are useful: killing a false bridge is a contribution.
- Don't revise existing findings silently — add new nodes to the mermaid plan
  (`sources/MERMAID_INVESTIGATION_PLAN.md`); the graph grows, it doesn't rewrite.

## What is NOT recruited

- **Translations** of the repo are handled internally. Please don't open
  translation PRs or issues — they'll be closed. (If a translation is published
  later, it will be linked from the README.)

## License

By contributing, you agree your code contributions are licensed under the MIT
License (`LICENSE`). Markdown/analysis notes are CC-BY-4.0.