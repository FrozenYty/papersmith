---
name: academic-writing-toolkit
description: >
  Academic research writing, diagramming, and plotting toolkit. Use whenever
  the user is working on a paper, thesis, or scholarly document — translation
  (zh↔en), polishing, abstract/title drafting, cover letters, rebuttals,
  peer-review simulation, experiment analysis, and figure/table captions.
  Also use for academic figures: model architecture diagrams (draw.io XML)
  and publication-ready Python plots (matplotlib, Type-42 fonts). Trigger on
  requests like "draw a diagram of X", "polish this abstract", "plot this
  experiment", or "write a rebuttal".
---

# Academic Writing Toolkit

Route the user's request to the correct prompt template below. Read the
matched file in full, then follow its instructions to accomplish the task.
Do not deviate from the prompt template unless the user explicitly asks.

## Prompt Index

### Translation

| User Intent | Expected Input | Prompt File |
|---|---|---|
| Translate Chinese draft to English LaTeX | Chinese text + LaTeX needed | `prompts/translate-zh-to-en-latex.md` |
| Translate English LaTeX to plain Chinese | English LaTeX snippet | `prompts/translate-en-to-zh-latex.md` |
| Translate English to Chinese for Word | English text (for Word) | `prompts/translate-en-to-zh-word.md` |
| Translate Chinese draft to English for Word | Chinese text (for Word) | `prompts/translate-zh-to-en-word.md` |

### Rewriting & Polishing

| User Intent | Expected Input | Prompt File |
|---|---|---|
| Rewrite fragmented Chinese draft into formal academic prose | Chinese draft (scattered points, colloquial) | `prompts/rewrite-zh-draft.md` |
| Polish English LaTeX for clarity and rigor | English LaTeX snippet | `prompts/polish-en.md` |
| Polish Chinese text with minimal intervention | Chinese paragraph (near-final) | `prompts/polish-zh.md` |
| Polish abstract into the 5-part structure | Current abstract + optional venue limit | `prompts/polish-abstract.md` |
| Generate 5-10 candidate titles + scoring | Abstract or summary | `prompts/polish-title.md` |

### Length Adjustment

| User Intent | Expected Input | Prompt File |
|---|---|---|
| Slightly shorten English LaTeX (~5-15 words) | English LaTeX snippet | `prompts/shorten-en.md` |
| Slightly expand English LaTeX (~5-15 words) | English LaTeX snippet | `prompts/expand-en.md` |

### Quality & Style

| User Intent | Expected Input | Prompt File |
|---|---|---|
| Final consistency and logic check before submission | English LaTeX (near-final) | `prompts/check-logic.md` |
| Remove AI-generated writing patterns from English LaTeX | English LaTeX snippet | `prompts/humanize-en.md` |
| Remove machine-translation tone from Chinese text | Chinese paragraph | `prompts/humanize-zh.md` |

### Figures & Charts

| User Intent | Expected Input | Prompt File |
|---|---|---|
| Generate a paper diagram (architecture, pipeline, training stages, GNN, diffusion, RAG, etc.) | Methodology description + target conference | `prompts/draw-diagram.md` |
| Draw.io XML syntax reference | — (loaded on demand) | `references/drawio-reference.md` |
| Canonical templates (15 total: 4 architecture + 11 layout/classic types) | — (loaded on demand) | `references/drawio-templates.md` |
| Recommend the best chart type for given data | Experiment data (table/CSV) + conclusion to emphasize | `prompts/recommend-chart.md` |
| Generate Python plotting code (publication-ready) | Chart type + data + optional target venue | `prompts/plot-figure.md` |
| Python plotting style reference (rcParams, palettes, conventions) | — (loaded on demand) | `references/plotting-reference.md` |
| Python plotting templates (19 chart types) | — (loaded on demand) | `references/plotting-templates.md` |
| Write a figure caption in English | Chinese description of the figure | `prompts/write-figure-caption.md` |
| Write a table caption in English | Chinese description of the table | `prompts/write-table-caption.md` |

### Analysis & Review

| User Intent | Expected Input | Prompt File |
|---|---|---|
| Analyze experiment results and write LaTeX analysis | Experiment data table + key findings | `prompts/analyze-experiments.md` |
| Simulate a peer review for a paper draft | Paper PDF + target conference name | `prompts/simulate-peer-review.md` |
| Draft a point-by-point response to reviewers | Reviewer comments + optional list of changes | `prompts/respond-to-reviewers.md` |
| Draft a 250-400 word cover letter for submission | Title + venue + manuscript summary | `prompts/draft-cover-letter.md` |
| Write broader impact / ethical considerations statement | Title + abstract + method description + optional venue | `prompts/write-broader-impact.md` |

## Chinese Typography Rules (CRITICAL)

When writing **any Chinese text** — whether in prompts, output format
descriptions, translations, or inline examples — follow these rules:

1. **Quotation marks**: ALWAYS use full-width Chinese quotation marks `""`
   (U+201C / U+201D). NEVER use ASCII half-width `""` (U+0022) around or
   within Chinese text. This is the single most common formatting error.
2. **Punctuation**: Use Chinese full-width marks throughout: `， 。 ； ：`
   (not ASCII `, . ; :`). The only exception is when the surrounding
   paragraph is entirely in English.
3. **Self-check**: Before finalizing any output containing Chinese, scan
   for ASCII `"` (0x22) characters adjacent to Chinese text and replace
   them with full-width `""`.

This rule applies to ALL prompt templates in this toolkit and to any ad-hoc
Chinese text you generate while assisting the user.

## Routing Rules

1. **Single intent**: If the user's request clearly matches one scenario, read
   and execute that file only.
2. **Ambiguous intent**: If the request could match multiple scenarios, ask the
   user to clarify before proceeding. Present the top 2-3 matches briefly.
3. **Compound request**: If the user asks for multiple operations (e.g.,
   "translate this, then polish it"), execute them sequentially in the natural
   order (translate first, then polish, then check).
4. **No match**: If no scenario fits, state that clearly and ask what the user
   intended.

## Figure Routing: Diagram vs. Plot (READ FIRST)

When the user asks for a "figure", "diagram", "chart", "plot", "graph",
or "illustration", decide which path to take BEFORE starting work. The
wrong choice produces a bar chart in drawio (waste) or a Transformer
architecture in matplotlib (waste).

**Decision rules — evaluate in order:**

1. **Is it a conceptual structure with discrete components connected by
   arrows?** → Read `prompts/draw-diagram.md`. This covers: model
   architectures, training/inference pipelines, RAG pipelines, GNN
   message-passing, diffusion chains, flowcharts, system overviews,
   comparison diagrams. No numerical axes needed. Goto § Diagram Workflow
   below.

2. **Does it have numerical axes (X/Y bar, line, scatter, curve)?** →
   Read `prompts/plot-figure.md` (after running `prompts/recommend-chart.md`
   if the chart type hasn't been chosen yet). This covers: bar charts,
   line curves, scatter plots, ROC/PR, heatmaps, violin/box, Pareto, etc.
   Goto § Plotting Workflow below.

3. **Still ambiguous?** (e.g. "visualize my training process" — could be a
   Python loss curve or a drawio multi-stage pipeline; "compare our
   methods" — could be a Python bar chart or a drawio comparison table).
   **Ask the user to clarify.** Present the two interpretations in one
   sentence each and let them pick. Never silently guess — a diagram and
   a plot use completely different tools and both take non-trivial time.

**Self-check before proceeding:** did you read one of the two workflow
sections below? If not, the routing decision was skipped. Pause and
re-evaluate.

## Diagram Workflow (drawio)

Drawing directly without planning produces overlapping shapes, diagonal
arrows, broken labels, and inverted stacks. A 30-second layout plan
eliminates these problems entirely. When routed here from Figure Routing
(conceptual diagram):

1. **Check templates first** — if the request matches a common architecture
   (Transformer encoder-decoder, GPT decoder-only, Seq2Seq, CNN classifier,
   Diffusion forward/reverse, RAG pipeline, multi-stage training, GNN
   message-passing), read `references/drawio-templates.md` and adapt the
   matching template. Skip Phase 1 planning when a template fits — the
   layout math is already done.
2. **Plan first** (if no template fits) — follow the Phase 1 workflow in
   `references/drawio-reference.md`. Decide flow direction up front
   (default bottom-up for ML stacks, left-to-right for pipelines), then
   determine canvas size, layout zones, node table (in data-flow order),
   and edge table. Present the plan concisely.
3. **Generate XML** — write the `.drawio` file to `./diagrams/<name>.drawio` in
   the working directory. Follow all hard rules: every vertex has geometry,
   every edge has `<mxGeometry relative="1" as="geometry"/>`, all coords
   multiples of 10, XML escapes applied, every forward edge has
   `source.y > target.y` (TB) or `source.x < target.x` (LR).
4. **Self-check** — verify edges reference existing vertices, no out-of-page
   elements, no unescaped characters, no inverted stacks (flow direction
   consistent).

**Key rules enforced by `references/drawio-reference.md`:**
- **Flow direction**: ML stacks flow bottom-to-top — input at largest y,
  output at smallest y, arrows always point UP. Inverted stacks are the
  most common failure mode.
- Tight vertical stacks preferred — integrate inputs/embeddings into the stack,
  don't place them far away. This makes all arrows short and direct.
- Cross-stack horizontal arrows (e.g. encoder→decoder K,V): align Y-centers
  so the line is straight, no waypoint jogs.
- Vertical gap 24-30px between stacked modules.
- Fonts 12-14px for titles, strokeWidth 1.5-2.5, A4 page (827×1169) default.

## Plotting Workflow (Python charts)

Arrive here from § Figure Routing when the user wants data visualization
(numerical axes). Don't enter this section unless Figure Routing resolved
to "Python plot."

1. **Pick the chart type** — if the user hasn't specified, route through
   `prompts/recommend-chart.md` first. The recommend prompt outputs one or
   two chart types matched to the data.
2. **Read references** — `references/plotting-reference.md` for rcParams,
   palettes, sizing, statistical conventions. Then
   `references/plotting-templates.md` for the matching template (19 chart
   types, indexed by recommend-chart's numbering).
3. **Generate code** — follow `prompts/plot-figure.md`. Output one
   self-contained `.py` file that produces both `.pdf` (vector) and `.png`
   (600 dpi minimum, venue-adaptive) versions of the figure.
4. **Self-check** — output the 10-item checklist from
   `plotting-reference.md` § Self-check, especially `pdf.fonttype = 42`
   (Type-3 fonts fail ACM/IEEE submission).

**Key rules enforced by `references/plotting-reference.md`:**
- `pdf.fonttype = 42` always — this is the most-failed paper submission
  check.
- Figure size matches the venue (IEEE single-column 3.5", NeurIPS 5.5",
  Nature 3.5"/7.2"). Don't use matplotlib defaults.
- Color palette from this file (Nature / Science / Cell / IEEE-semantic).
  Don't use matplotlib defaults; don't use `jet` / `rainbow`.
- Error bars / bands MUST be disclosed in the caption — never silent.
- Title omitted for paper figures (caption is in LaTeX), set for slides.

## Input Handling

Each prompt template expects user input signaled by `{{PLACEHOLDER}}` markers.
Before executing a prompt, confirm you have the required input from the user.
If the user already provided the content inline, use it directly. If input is
missing, ask for it explicitly before proceeding.
