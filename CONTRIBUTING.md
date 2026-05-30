# Contributing

Thanks for considering a contribution. The toolkit is organized for easy
extension — adding a new prompt or template should not require touching
unrelated files.

## Quick map of where things live

```
academic-writing-toolkit/
├── SKILL.md             # routing index — register new prompts here
├── prompts/             # one .md per task (Role/Task/Constraints/Output/Self-Audit)
│   ├── translate-*.md   # translation prompts (zh↔en, LaTeX or Word)
│   ├── polish-*.md      # polishing prompts (en, zh, abstract, title)
│   ├── humanize-*.md    # de-AI / de-translationese prompts
│   ├── write-*.md       # generation prompts (captions, broader impact)
│   ├── draw-diagram.md  # draw.io diagram generation
│   ├── plot-figure.md   # Python plotting code generation
│   └── ...
├── references/          # loaded on demand: long-form rules + templates
│   ├── drawio-reference.md     (rules for architecture diagrams)
│   ├── drawio-templates.md          (15 templates: §1-§4 arch, §5-§15 layouts/classic)
│   ├── plotting-reference.md        (rules for Python plots, rcParams, palettes)
│   ├── plotting-templates.md        (19 chart templates: §I-§VI)
│   ├── writing-anti-patterns.md     (24 patterns: 12 zh + 12 en)
│   ├── writing-templates.md         (7 section structure templates)
│   └── venue-citation-guide.md      (10+ venue citation formats)
├── examples/            # verified end-to-end outputs
│   ├── transformer.drawio       (generated from drawio-templates §1)
│   ├── diffusion.drawio         (generated from drawio-templates §2)
│   └── sota-comparison.py       (generated from plotting-templates §I-1)
├── CHANGELOG.md
├── CONTRIBUTING.md      # you are here
└── README.md
```

**Naming conventions:**

| What | Pattern | Example |
|------|---------|---------|
| Prompt file | `<verb>-<target>-<optional-modifier>.md` | `translate-zh-to-en-latex.md` |
| Reference file | `<topic>-reference.md`, `<topic>-templates.md`, `<topic>-anti-patterns.md`, or `<topic>-guide.md` | `drawio-reference.md`, `writing-anti-patterns.md`, `venue-citation-guide.md` |
| Example drawio | `<descriptive-name>.drawio` | `transformer.drawio` |
| Example Python | `<descriptive-name>.py` | `sota-comparison.py` |

## Commit Rules

### Format

```
<type>: <short description>

<optional body — why, not what>

Author: <Your English Name>
```

**Types:** `feat` (new feature/template/prompt), `fix` (bug fix), `docs`
(documentation only), `refactor` (cleanup, renames, reorganization),
`style` (formatting, whitespace), `chore` (gitignore, CI).

### Staging discipline

Stage files individually — **never use `git add -A` or `git add .`**:

```bash
git add path/to/changed-file.md
git add path/to/another-file.md
git commit -m "..."
```

This keeps diffs auditable and prevents accidentally committing temp files,
editor artifacts, or unrelated changes.

### What to commit

| Commit These | Never Commit These |
|-------------|-------------------|
| `prompts/*.md` | `.pyc`, `__pycache__/` |
| `references/*.md` | `.DS_Store`, `Thumbs.db` |
| `SKILL.md`, `README.md` | Editor temp files (`*~`, `*.swp`) |
| `CHANGELOG.md`, `CONTRIBUTING.md` | `.vscode/`, `.idea/` (unless `settings.json`) |
| `evals/evals.json` | `Claude_Code_Files/` |
| `examples/*.drawio` | `*.egg-info/`, `dist/` |
| `examples/*.py` | `*.lock` (unless `pip freeze` is the intent) |
| `examples/*.pdf`, `examples/*.png` (generated outputs, keep in sync) | |

### Batch size

Commit in small, topic-focused batches. Don't bundle "added 6 templates +
renamed 3 files + updated README + fixed typos" into one commit — split
into one commit per logical change.

```bash
# Good: one topic per commit
git add references/drawio-reference.md
git commit -m "docs: add orthogonal routing convention to drawio-reference"

# Bad: unrelated changes squashed together
git add references/ prompts/ README.md
git commit -m "various updates"
```

### Before committing

```bash
git pull --rebase          # avoid push conflicts
git status                 # review what changed
git diff --stat            # confirm scope
```

## Adding a new prompt

The toolkit's prompts share a four-section structure. Match it.

**File:** `prompts/<kebab-case-name>.md`. The name should describe the
*action*, not the input. Examples that work: `polish-abstract`,
`respond-to-reviewers`, `recommend-chart`. Examples that don't:
`for-conferences`, `chinese-output`.

**Required sections:**

```markdown
# <Title Case Name>

## Role
You are <a specific persona with credibility for this task>.

## Task
<One paragraph: what the prompt does, what it produces.>

## Constraints
### <Constraint group 1>
- specific rule
- specific rule

## Output Format
<Structure of the output. Use Part 1 / Part 2 / Part 3 if multi-part.>

## Self-Audit (before delivering)
1. <Check 1>
2. <Check 2>

## Input
{{PLACEHOLDER}}
```

**Style conventions:**
- Imperative mood (`Polish the snippet`, not `This prompt polishes...`).
- One placeholder per input, in `{{ALL_CAPS}}` form.
- If the prompt outputs Chinese, reference the Chinese typography rules
  in SKILL.md explicitly: "Apply the Chinese typography rules from
  SKILL.md when outputting Chinese."
- For Word-targeted output: ban Markdown bold/italic in the output (Word
  doesn't render them).
- For LaTeX-targeted output: preserve `\cite{}`, `\ref{}` etc. verbatim.

**Register the prompt in SKILL.md:**

Find the appropriate "### Category" section in the Prompt Index table
and add a row:

```markdown
| User Intent | Expected Input | Prompt File |
|---|---|---|
| <one-line description of when to trigger> | <input description> | `prompts/<your-file>.md` |
```

Categories so far: Translation, Rewriting & Polishing, Length Adjustment,
Quality & Style, Figures & Charts, Analysis & Review. Add a new category
section if your prompt doesn't fit.

## Adding a new drawio architecture template

Templates live in `references/drawio-templates.md` as `## §N <name>`
sections. Each template needs:

1. **When to use** — one-paragraph description of the architecture and
   when this template fits.
2. **Canvas size** — `pageWidth × pageHeight`.
3. **Layout choices** — what conventions this template uses (e.g.,
   K,V cross-attention horizontal alignment, ≥30px section gaps).
4. **Node table** — every vertex with `id | label | x | y | w | h`.
   Rows in DATA-FLOW ORDER, y assigned in DECREASING order. This is
   the most important convention — see "Flow Direction" in
   `references/drawio-reference.md`.
5. **Edge table** — `id | source | target | style`. Verify each forward
   edge satisfies `source.y > target.y` (TB) or `source.x < target.x`
   (LR).
6. **XML skeleton** — complete copy-pasteable XML.
7. **Self-check** — list of 3-5 verifications specific to this template.

**Hard rules to obey** (full list in `references/drawio-reference.md`):
- Flow Direction: ML stacks bottom-to-top.
- No-Overlap: vertices don't intersect (containers + their modules
  excepted, with ≥10px padding).
- Section labels INSIDE the container at top-left, never above.
- `pdf.fonttype = 42` doesn't apply (this is drawio not Python).
- All x/y/w multiples of 10; heights may use 30/32/38/42/50.
- Every edge has `<mxGeometry relative="1" as="geometry"/>` (not
  self-closing).
- HTML escapes: `&amp;` once for `&`, never `&amp;amp;`.

**Register in templates index** at the top of the file, and update the
SKILL.md "Canonical templates" row to include the new architecture name.

## Adding a new Python plotting template

Templates live in `references/plotting-templates.md` as
`### §<group>-<num> <name>` sections. The numbering aligns with
`prompts/recommend-chart.md`. If you're adding a chart type that isn't
in recommend-chart yet, add it there first.

**Each template needs:**
1. One-line "when to use".
2. Concrete data setup (small example arrays).
3. Plotting code that produces a publication-ready figure.
4. Conventions specific to this chart type (e.g., "always sort
   horizontal bars", "use sqrt scaling for bubble sizes since `s` is
   area").

**Style invariants to obey** (from `references/plotting-reference.md`):
- Use the rcParams block from the reference (not matplotlib defaults).
- `pdf.fonttype = 42`. Always.
- Color palette from the reference: IEEE-semantic for ML papers;
  Nature/Science/Cell palettes otherwise.
- Don't use `jet` / `rainbow` colormaps.
- Disclose error bars / bands meaning (caption note).
- Save as both `.pdf` (vector) and `.png` (600 dpi minimum).

**Register in plotting-templates.md index** at the top, and verify the
numbering matches `prompts/recommend-chart.md`.

## Adding a new reference file

Add a `<topic>-reference.md` in `references/` if you're documenting a
new toolkit area (e.g., a `tikz-reference.md` for LaTeX TikZ figures).

Add a row to the SKILL.md Prompt Index marked "loaded on demand".

Don't add a new reference file just to extend an existing area — extend
the existing reference instead.

## Style: the rest of the toolkit's writing

- **Imperative voice** in instructions ("Apply the rule", not "The user
  should apply the rule").
- **State the why.** When a rule seems arbitrary, add one sentence on
  the rationale. The Hard Rules in `references/drawio-reference.md` each have a
  one-line "why" because past failures showed which rules need
  emphasis.
- **No "MUST" / "SHALL" all-caps unless rare.** If you find yourself
  capitalizing every directive, consider whether the prompt is too
  rigid; smarter LLMs follow soft guidance better than rigid commands.
- **One placeholder per input.** Templates with 5+ placeholders are
  fragile.

## Testing your changes

1. **Read the new file in full.** Manual once-over catches more than
   any tool.
2. **Try the prompt on a realistic input.** If you added
   `polish-japanese-paper.md`, write a short Japanese paragraph and run
   the toolkit on it.
3. **Add a representative case to `evals/evals.json`** if your addition
   is non-trivial. The eval set is also a regression check for future
   contributors.
4. **For diagram templates:** generate the XML, open it in
   [draw.io](https://app.diagrams.net/), and visually confirm:
   - No overlapping cards
   - All arrows point the correct direction
   - K,V or cross-stack edges are clean (no waypoint jogs)
5. **For plotting templates:** run the script. The figure should save
   without warnings, and the PDF should pass:
   ```python
   import re, zlib
   raw = open("fig.pdf", "rb").read()
   for s in re.findall(rb"stream\n(.*?)\nendstream", raw, re.DOTALL):
       try: d = zlib.decompress(s)
       except: continue
       assert b"/Subtype /Type3" not in d, "Type-3 fonts in PDF — set pdf.fonttype=42"
   ```

## What NOT to do

- Don't introduce new tools / dependencies (numpy + matplotlib + scipy
  + scikit-learn + seaborn already cover the plotting needs).
- Don't write prompts that depend on each other ("call X then Y then
  Z"). Each prompt should be standalone; SKILL.md handles
  composition.
- Don't add LICENSE-style headers to individual files. The repo's
  license (or absence thereof) is at the root.
- Don't hardcode personal lab information (institution names,
  funding sources, author names) in templates. Use placeholders.
- Don't write Markdown documents (ad-hoc analysis notes, design
  rationales) unless they're a `*-reference.md` registered in
  SKILL.md.

## Submitting

1. Fork the repo, branch off `main`.
2. Make your changes, commit with a message that names the feature
   (`Add §9 ablation comparison template` not `Update files`).
3. Open a PR with:
   - What was added/changed
   - Why (one sentence)
   - Verification: how you tested
   - If you added an architecture / chart template, attach the rendered
     output (PNG screenshot is fine).

Substantive feedback over rubber-stamps. Honest reviews of edge cases
and counter-examples make the toolkit stronger.
