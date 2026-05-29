# Changelog

All notable changes to the Academic Writing Toolkit are recorded here. The
format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- `drawio-templates.md` — 8 canonical architecture templates: Transformer
  encoder-decoder (Vaswani 2017), Transformer decoder-only (GPT-style),
  Seq2Seq with Bahdanau attention, CNN classifier, Diffusion
  forward/reverse process, RAG pipeline, Multi-stage training (Pretrain
  → SFT → RLHF), GNN message-passing
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
