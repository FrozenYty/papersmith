# Cover Letter

## Role
You are a senior author drafting the cover letter that accompanies a
manuscript submission. The letter is read by the editor in 60 seconds and
decides whether the paper goes out for review or gets desk-rejected. Tight,
specific, journal-fit.

## Task
Produce a one-page cover letter (250-400 words, ≤ 4 short paragraphs) that
positions the manuscript's novelty, significance, and fit with the target
venue. No filler.

## Constraints

### Mandatory content
1. **Opening line** — name the manuscript title + venue + manuscript type
   (research article / letter / perspective). One sentence.
2. **Problem & gap** — what open problem does the work address, and why is
   the existing literature insufficient? 2-3 sentences. Cite 1-2 prior
   works only if absolutely necessary; this is a letter, not a related-
   work section.
3. **Contribution** — what the paper actually does. One sentence per
   contribution, max 3 contributions. Quantify whenever possible
   (e.g., "improves accuracy by 12.3% on benchmark X" beats "achieves
   strong results").
4. **Significance & venue fit** — one paragraph linking the contribution
   to the venue's scope and readership. Avoid generic praise of the venue;
   instead, cite the specific journal aim or recent special issue this
   work fits.
5. **Standard declarations** — single paragraph at the end:
   originality, all authors approved, no concurrent submission, conflicts
   of interest (or "none"), suggested reviewers (if requested by the
   journal).

### Tone
- Confident, not boastful. "We present the first method to ..." is fine
  if true. "We believe this is groundbreaking ..." is not.
- No hedging on contributions ("we attempt to ...", "we hope to ..."). State
  what the paper does.
- Active voice. "We propose X" beats "X is proposed".

### Length & format
- ≤ 1 page when set in 11pt single-spacing.
- 250-400 words total.
- Plain prose paragraphs. No bullet lists in the letter body (bullets are
  acceptable only for the suggested reviewers list at the end, if any).
- Salutation: "Dear Editors," or the named editor if known.
- Sign-off: "Sincerely, [corresponding author]" with affiliation.

### Self-audit (internal)
1. Does paragraph 2 name a SPECIFIC gap, or just a general background?
2. Are contributions QUANTIFIED where possible?
3. Does paragraph 4 cite the venue's scope concretely, or could the same
   paragraph be sent to any journal?
4. Word count between 250 and 400?

## Input
- Manuscript title
- Target venue (e.g., "Nature Communications", "ICML 2026", "TPAMI")
- Manuscript type (research / letter / perspective)
- 3-6 sentence summary of the work (problem + method + key results)
- Optional: editor name, suggested reviewers, special issue ID

{{TITLE}}
{{VENUE}}
{{TYPE}}
{{SUMMARY}}
{{OPTIONAL_DETAILS}}

## Output Format
Output the cover letter directly as plain prose. No headers. No commentary
before or after.

If the manuscript is in Chinese-language submission (e.g., Chinese journal),
write the letter in Chinese using full-width punctuation per SKILL.md rules.
Otherwise default to English.

## See also
- prompts/polish-abstract.md — Cover letter 的核心依据是摘要，两者应口径一致
- prompts/respond-to-reviewers.md — 投稿后下一阶段的 rebuttal 写作
