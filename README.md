# Academic Writing Toolkit

A Claude Code / Claude.ai skill for academic research writing, paper
diagrams, and publication-ready figures. Drop it in, and Claude will
route paper-related requests through 22 specialist prompts and 27
templates calibrated for top-venue conventions.

> 🙏 Built on top of [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) by Leey21. Prompts adapted with gratitude; diagram and plotting reference layers added on top.

> **What it covers:** translation, polishing, abstract / title /
> cover-letter / rebuttal drafting, peer-review simulation, drawio
> architecture diagrams (Transformer, Diffusion, RAG, GNN, …), and
> publication-ready Python plots (bar, line, ROC, heatmap, violin,
> Pareto, …) with ACM/IEEE-compliant Type-42 font embedding.

## Why this exists

LLMs writing paper diagrams and plots routinely make the same mistakes:

- Transformer figures drawn upside-down (data flows top-down instead of
  the canonical bottom-up).
- Cards overlapping because section labels intrude on neighboring
  containers.
- PDFs failing ACM/IEEE submission because matplotlib defaults to
  Type-3 fonts.
- Abstracts that bury the contribution under three sentences of
  background.
- Cover letters that read like AI-generated form mail.

This toolkit encodes the conventions, hard rules, and copy-pasteable
templates that prevent each of those failures. Most rules are stated
with their *why* — past failure modes traced into prescriptions you can
override when the situation warrants.

## Install

### Claude Code (CLI)

```bash
git clone <this-repo-url> ~/.claude/skills/academic-writing-toolkit
```

Claude Code auto-discovers skills under `~/.claude/skills/`. Restart
your session if it's already running. Verify:

```
> /skills
```

The skill should appear as `academic-writing-toolkit`. Any paper-related
request should now trigger it.

### Claude.ai

Package as a `.skill` file (zip with the right structure):

```bash
cd academic-writing-toolkit
zip -r academic-writing-toolkit.skill SKILL.md prompts/ references/
```

Upload via Settings → Capabilities → Skills.

### Manual / one-off use

Even without installing as a skill, you can drop the relevant prompt
content into a Claude conversation directly. Each prompt is a
self-contained Markdown file in `prompts/`.

## Quick start

After installing, ordinary conversational requests trigger the toolkit:

**Drawing an architecture figure:**
> Draw a Transformer encoder-decoder for our translation paper. 6
> encoder layers, 6 decoder layers.

Claude reads `references/drawio-templates.md` §1, adapts the canonical
template to your spec, and writes a `.drawio` file ready to open in
[draw.io](https://app.diagrams.net/).

**Plotting an experiment:**
> Plot a bar chart comparing 3 methods on 4 metrics, with ±1 SD error
> bars, IEEE single-column.

Claude reads `references/plotting-templates.md` §I-1, applies the
publication style block (Type-42 fonts, IEEE palette), and writes a
self-contained Python script that produces both `.pdf` (vector) and
`.png` (300 dpi).

**Polishing an abstract:**
> Polish this abstract for ICML, 250 words max: <abstract text>

Claude routes to `prompts/polish-abstract.md`, restructures into the
canonical 5-part form (background → gap → method → results → impact),
trims to budget, and returns the rewrite + a sentence-to-part map.

**Drafting a rebuttal:**
> Reviewers said: [comments]. Help me draft a response.

Claude routes to `prompts/respond-to-reviewers.md`, produces a
point-by-point reply with the three response types (concession /
clarification / disagreement) clearly signaled.

See [`SKILL.md`](SKILL.md) for the full prompt index — 22 prompts in 6
categories.

## Examples

Three end-to-end verified outputs are in [`examples/`](examples/):

| File | Generated using | What it shows |
|---|---|---|
| `transformer.drawio` | drawio-templates §1 | Transformer encoder-decoder with K,V cross-attention as straight horizontal arrow |
| `diffusion.drawio` | drawio-templates §5 | DDPM forward (q) + reverse (p_θ) Markov chain |
| `sota-comparison.{py,pdf,png}` | plotting-templates §I-1 | Grouped bar with ±1 SD error bars, Type-42 font verified |

See [`examples/README.md`](examples/README.md) for adaptation tips.

## Repository structure

```
academic-writing-toolkit/
├── SKILL.md             # entry point — Claude reads this first
├── README.md            # you are here
├── CONTRIBUTING.md      # how to add prompts / templates
├── CHANGELOG.md         # version history
├── prompts/             # 22 task-specific prompts
├── references/          # 4 long-form references
│   ├── drawio-reference.md      # rules for architecture diagrams
│   ├── drawio-templates.md      # 8 canonical architecture templates
│   ├── plotting-reference.md    # rules for Python plots
│   └── plotting-templates.md    # 19 chart templates
├── examples/            # verified end-to-end outputs
└── evals/evals.json     # representative test prompts
```

## What's covered

**Writing tasks** — translate (zh↔en, LaTeX or Word), polish (Chinese,
English, abstract, title), shorten/expand, humanize, logic-check,
analyze experiments, simulate peer review, respond to reviewers, draft
cover letter.

**Architecture diagrams** (drawio XML) — Transformer encoder-decoder,
Transformer decoder-only (GPT), Seq2Seq + Bahdanau, CNN classifier,
Diffusion forward/reverse, RAG pipeline, multi-stage training, GNN
message-passing.

**Charts** (Python / matplotlib) — grouped bar, horizontal bar, Pareto
front, radar, stacked bar, line + CI band, line + zoomed inset, scatter
+ fit, ROC, PR, heatmap, predicted-vs-true scatter, bubble, violin,
box, donut, dual y-axis, bar+line combo, faceted grid.

## Design rules baked in

- **Drawio Flow Direction**: ML stacks flow bottom-to-top — input at
  the largest y, output at the smallest y, every forward edge satisfies
  `source.y > target.y`. Inverted stacks were the #1 failure mode in
  early drafts.
- **Drawio No-Overlap**: vertex bboxes don't intersect (containers +
  modules excepted with ≥10px padding). Section labels go *inside* the
  container at top-left, never above.
- **Plotting `pdf.fonttype = 42`**: enforced everywhere — Type-3 fonts
  fail ACM/IEEE submission. Verified via PDF stream inspection in the
  reference example.
- **Chinese typography**: full-width quotation marks (U+201C/U+201D)
  and punctuation (， 。 ； ：) throughout any Chinese output.

Full rationale in [`references/drawio-reference.md`](references/drawio-reference.md)
and [`references/plotting-reference.md`](references/plotting-reference.md).

## Versioning

Semver. See [`CHANGELOG.md`](CHANGELOG.md). Current: **v0.1.0**.

## Contributing

Contributions welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the
conventions — file formats, registration locations, testing guidance.

The big picture: toolkit content is roughly half *prompts* (per-task
behavior) and half *references* (rules + templates loaded on demand).
Adding a new prompt shouldn't require editing references; adding a new
template shouldn't require editing prompts. The structure is designed
to keep these orthogonal.

## License & Attribution

**No license** — this toolkit mirrors the licensing approach of its primary
upstream source (see Acknowledgments below).

The prompt templates under `prompts/` are adapted and extended from
[Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing),
a Chinese-language collection of academic writing prompts curated from
researchers at MSRA, ByteDance Seed, Shanghai AI Lab, and several
universities. The original repository carries no explicit license, so
this fork maintains the same posture: shared publicly for reference and
discussion, with the intent to defer to the upstream author's wishes.

**Original components in this repository** (drawio templates, Python
plotting templates, drawio/plotting reference rules, SKILL.md routing
structure, examples, contributing guide) are likewise shared as-is, no
specific license attached.

If you'd like to use, redistribute, or relicense any part of this work,
please reach out to the upstream author for the prompts, or open an
issue here for the original components.

## Acknowledgments

- **Prompt templates adapted from
  [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing)** —
  a community-curated collection of academic writing prompts from
  researchers at top labs and universities. The `prompts/` directory in
  this repository builds on those patterns, extending them into a routed
  skill structure and adding new prompts (cover letter, response to
  reviewers, polish abstract, polish title, plot figure) along with
  the diagram and plotting reference layers.
- Color palettes adapted from Nature, Science, Cell, Nature Physics
  2025 publication conventions.
- IEEE semantic palette adapted from the NN-Models drawio library.
- Style block conventions informed by SciencePlots (`science`, `ieee`,
  `nature` styles).
- Skill structure follows the patterns documented in Anthropic's
  skill-creator framework.

Inspired by, derived from, and indebted to the above. Not affiliated
with any of them.
