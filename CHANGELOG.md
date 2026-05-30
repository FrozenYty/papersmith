# Changelog

All notable changes to the Academic Writing Toolkit are recorded here. The
format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-05-29

### Added

- **11 new drawio layout and classic diagram templates** (§5–§15):
  vertical stack, horizontal pipeline, center hub + satellites,
  side-by-side comparison, grid/table layout, flowchart, ERD, UML class
  diagram, sequence diagram, state machine diagram, data flow diagram
  (DFD). Total drawio templates: 15 (4 specific architectures + 11
  general patterns and classic types).
- **2 new prompts**: `translate-en-to-zh-word.md` (English → Chinese Word
  translation, Word-ready plain-text output), `write-broader-impact.md`
  (broader impact / ethical considerations statement, 4-dimension
  coverage, venue-specific word budgets). Total prompts: 24.
- **DPI upgrade**: plotting templates now output PNG at 600 dpi minimum,
  with a 3-tier venue-adaptive selection guide (600 / 800 / 1000 dpi).
- **Plotting templates hardening**: all 19 chart templates now include
  explicit `fig.savefig(..., dpi=600)` for PNG output, preventing
  matplotlib's default-100-dpi fallback.
- **Iron Rules**: 7 non-negotiable hard constraints added to SKILL.md
  (no fabricated content, pdf.fonttype=42, flow direction before drawing,
  error bars disclosed, no Markdown in Word, full-width Chinese
  punctuation, prompt before template).
- **Writing anti-patterns reference**: `references/writing-anti-patterns.md`
  — 12 common Chinese academic writing mistakes with Bad → Why → Rewritten
  examples and self-audit checklist.
- **English writing anti-patterns**: expanded `references/writing-anti-patterns.md`
  with 12 English academic writing anti-patterns covering AI-generated
  vocabulary, hollow intensifiers, copula avoidance, forced parallelism,
  padding openers, possessive overuse, passive voice overuse, overclaiming,
  vague comparisons, bookkeeping-style results, template openers, and
  em-dash overuse. Total: 24 patterns (12 Chinese + 12 English).
- **Cross-prompt See also links**: all 24 prompts now include a `## See
  also` section linking to 1-3 semantically related prompts, with I/O
  compatibility annotations for 16 sequential prompt chains (e.g.,
  "Part 1 [LaTeX] output → {{ENGLISH_LATEX}} input").
- **Writing templates reference**: `references/writing-templates.md` —
  canonical section structures for Introduction (CARS model), Related
  Work (taxonomy), Methodology (top-down), Experiments (three-part),
  Conclusion (three-part), and Abstract (five-part), with concrete
  examples and a general principles section.
- **Citation verification system**: `prompts/verify-references.md` —
  5-part audit covering completeness (cite→bib mapping + required field
  check), venue-specific format validation, and optional WebSearch-driven
  existence verification (VERIFIED / MISMATCH / NOT_FOUND). Companion
  `references/venue-citation-guide.md` documents citation formats for
  10+ top venues (NeurIPS, ICML, CVPR, ACL, IEEE, ACM, Nature, Science,
  Chinese journals). Total prompts: 25.
- **SKILL.md frontmatter**: added `author: Tianyu Yao`.
- **Orthogonal edge routing** as the default edge style in all new
  templates. Drawio's built-in `edgeStyle=orthogonalEdgeStyle` with
  `rounded=1;orthogonalLoop=1;jettySize=auto` eliminates most waypoint
  hand-coding.
- **Parent-child containment** as an alternative to absolute coordinates.
  Children use coordinates relative to their container; moving the
  container automatically moves all children. Implements drawio's native
  `container=1;pointerEvents=0;` pattern.
- **Spacing-by-complexity table** in `drawio-reference.md` — 200/280/350px
  gap recommendations based on node count (≤5 / 6-10 / >10).

### Changed

- File renames: `draw-architecture-diagram.md` → `draw-diagram.md`,
  `cover-letter.md` → `draft-cover-letter.md`,
  `plot-academic.md` → `plot-figure.md`.
- `drawio-reference.md` now has a Table of Contents for fast navigation.
- Prompt index references updated for renamed files.

### Design

- Figure Routing section added to `SKILL.md` — explicit drawio-vs-Python
  decision tree with "ambiguous → ask" fallback.
- Renamed prompts now follow verb-object kebab-case convention throughout.

## [0.1.0] — 2026-05-29

Initial release. **No license** — mirrors the upstream
[Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing)
which the prompt templates are adapted from.

### Added

**Prompts (22 total, organized by category):**
- Translation: zh→en LaTeX, en→zh LaTeX, zh→en Word
- Rewriting & polishing: rewrite-zh-draft, polish-en, polish-zh,
  polish-abstract (5-part structure), polish-title (6 type candidates +
  scoring)
- Length adjustment: shorten-en, expand-en
- Quality & style: check-logic, humanize-en, humanize-zh
- Figures & charts: draw-diagram, recommend-chart,
  plot-figure, write-figure-caption, write-table-caption
- Analysis & review: analyze-experiments, simulate-peer-review,
  respond-to-reviewers (concession / clarification / disagreement
  pattern), cover-letter (250-400 word template)

**References (4 total):**
- `drawio-reference.md` — Hard rules, Flow Direction rule, No-Overlap
  rule, Cross-Stack Y-Alignment, Section Container Layout, 7 Common
  Pitfalls, Self-check
- `drawio-templates.md` — 4 canonical architecture templates: Transformer
  encoder-decoder (Vaswani 2017), Diffusion forward/reverse process, RAG
  pipeline, Multi-stage training (Pretrain → SFT → RLHF)
- `plotting-reference.md` — Publication rcParams, IEEE / Nature / Science
  / Cell color palettes, figure sizing per venue, statistical
  conventions, broken axis / log scale snippets, 10-item self-check
- `plotting-templates.md` — 19 chart-type templates aligned with
  recommend-chart numbering: grouped bar, horizontal bar, Pareto, radar,
  stacked bar, line + CI band, line + zoomed inset, scatter + fit, ROC,
  PR, heatmap, predicted-vs-true scatter, bubble, violin, box,
  donut, dual y-axis, bar+line combo, faceted grid

**Examples (3 verified end-to-end):**
- `examples/transformer.drawio` — Transformer encoder-decoder, K,V
  cross-attention as straight horizontal arrow
- `examples/diffusion.drawio` — DDPM forward/reverse Markov chain
- `examples/sota-comparison.{py,pdf,png}` — Grouped bar with ±1 SD
  error bars, IEEE single-column sizing, Type-42 font embedding verified

**Evals scaffolding:** `evals/evals.json` with 8 representative test
prompts covering diagrams, plots, polishing, and writing tasks.

### Design rules baked into the toolkit

- **Drawio Flow Direction**: ML stacks flow bottom-to-top by convention
  — input at the largest y, output at the smallest y, every forward
  edge satisfies `source.y > target.y` (TB) or `source.x < target.x`
  (LR). Inverted stacks were the most common failure mode in early
  drafts.
- **Drawio No-Overlap**: no two vertex bounding boxes intersect, except
  a section container may contain modules with ≥10px padding on all
  four sides. Section labels go INSIDE the container at top-left, never
  above (which would intrude on the section above).
- **Plotting `pdf.fonttype = 42`**: enforced everywhere — Type-3 fonts
  fail ACM/IEEE PDF eXpress submission checks.
- **Chinese typography**: full-width quotation marks (U+201C/U+201D)
  and punctuation (， 。 ； ：) throughout any Chinese output.

### Known limitations

- WebSearch / WebFetch unavailable in the dev environment, so the
  templating priorities were chosen from training-knowledge survey
  rather than live GitHub research.
- The Python plotting templates assume English axis labels by default;
  Chinese-language figures require additional CJK font configuration
  not yet documented.
- Skill-creator's eval flow (run_loop.py, generate_review.py) requires
  Anthropic CLI + subagent support; `evals/evals.json` provides the
  prompt set but running them is environment-dependent.
