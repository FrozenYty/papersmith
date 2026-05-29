# Draw.io Academic Diagram Reference

## Index

- [Workflow](#workflow-mandatory) — Phase 1-3 planning loop
- [XML Skeleton](#xml-skeleton) — bare minimum mxfile structure
- [Flow Direction](#flow-direction-read-first----most-common-failure-mode) — bottom-to-top rule (most common failure mode)
- [Cross-Stack Y-Alignment](#cross-stack-y-alignment) — encoder-decoder horizontal edge alignment
- [Hard Rules](#hard-rules-always-enforced) — 11 non-negotiable rules
- [Section Container Layout](#section-container-layout) — labels inside containers, no overlap
- [XML Escapes](#xml-escapes) — `&amp;`, `&lt;`, `&#xa;`, etc.
- [Layout Rules](#layout-rules) — spacing, margins, line limits
- [Arrow Routing](#arrow-routing-critical----most-common-source-of-errors) — waypoints, diagonals, residuals
- [Visual Style Guide](#visual-style-guide) — typography, stroke weights, color conventions
- [Common Pitfalls](#common-pitfalls-real-failures-from-past-generations) — 7 real failures and their fixes
- [Self-Check](#self-check-output-passfail-for-each) — 13-item output checklist

---

## Workflow (MANDATORY)

### Phase 1 — Plan (output these before any XML)

**1. Figure purpose** (one sentence)

**2. Figure type** — `pipeline` | `architecture` | `comparison` | `flowchart` | `taxonomy`

**3. Canvas** — `pageWidth` × `pageHeight` (A4: 827×1169; wider: scale up)

**4. Layout zones**
```
Zone A: x=... y=... w=... h=...   (what goes here)
Zone B: x=... y=... w=... h=...   (what goes here)
```

**5. Node table**
```
id | label | x | y | w | h | role
```

**6. Edge table**
```
id | source | target | style (solid/dashed)
```

Proceed to Phase 2 only after layout is confirmed.

### Phase 2 — Generate XML

Follow the rules below. Generate ALL vertex cells first, then ALL edge cells.

### Phase 3 — Self-check

Run the checklist and report each item `pass/fail`.

---

## XML Skeleton

```xml
<mxfile host="app.diagrams.net">
  <diagram name="Figure" id="fig">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1" page="1"
                  pageScale="1" pageWidth="1200" pageHeight="800"
                  math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Flow Direction (READ FIRST — most common failure mode)

**ML architecture diagrams flow BOTTOM-TO-TOP by convention.** This is the
single most common thing models get wrong. The Vaswani 2017 Transformer figure,
ResNet figures, every textbook RNN diagram — input at the bottom, output at the
top, arrows pointing UP.

**The rule, mechanically:**

1. The FIRST computation in a stack (input embedding, layer 1) gets the
   LARGEST y-coordinate (bottom of the section).
2. The LAST computation (final projection / softmax / output) gets the
   SMALLEST y-coordinate (top of the section).
3. Every forward arrow points UP: `source.y > target.y`.
4. When you write the Phase 1 node table, list rows in DATA-FLOW ORDER
   (input first, output last), then assign y values in DECREASING order.

**Why this trips models up:** Reading order is top-to-bottom, so the natural
instinct is to put "layer 1" at the top of your text plan and the small y
values. That puts the encoder upside-down. Resist it.

**Concrete example for Transformer encoder (encoder section spans y=300..580):**

```
data-flow order      y assignment (decreasing)     resulting layout
1. Input Embedding   y = 870  (BELOW the section)  ┌─ section top ──┐
2. Encoder MHA       y = 540                       │ Add & Norm 2   │ ← y=510
3. Add & Norm 1      y = 470                       │ Feed Forward   │ ← y=440
4. Feed Forward      y = 400                       │ Add & Norm 1   │ ← y=370
5. Add & Norm 2      y = 330  (TOP of stack)       │ Multi-Head Atn │ ← y=300
                                                    └────────────────┘
                                                    ↑ from Embedding (y=870)
```

The encoder OUTPUT (Add & Norm 2) is at the TOP and feeds K,V to the decoder
cross-attention. The encoder INPUT enters at the BOTTOM. Source tokens and
embeddings sit BELOW the encoder section, with arrows pointing UP into it.

The output stack (Linear → Softmax → Output Probabilities) sits ABOVE the
decoder, ordered the same way: Linear at the bottom (closest to decoder),
Output Probabilities at the top.

**Quick self-test** — before writing XML, scan your node table:
- For every adjacent pair `A → B` in your data-flow order, check `A.y > B.y`.
- If any pair fails, your stack is inverted. Fix it before generating XML.

**When NOT to use bottom-up:** Pipeline / system / data-flow diagrams (not ML
architectures) typically flow LEFT-TO-RIGHT. Use the same logic with x instead
of y: source on the left, target on the right, every forward arrow has
`source.x < target.x`. Don't mix LR and TB in one figure.

## Cross-Stack Y-Alignment

For encoder-decoder diagrams, align the Y-coordinates of layers connected by
horizontal arrows so the connection is a clean horizontal line, not a diagonal
or a multi-waypoint detour.

**The K,V cross-attention case** — encoder output (Add & Norm at the top of
the encoder stack) feeds into decoder cross-attention. Set:

```
enc_an_top.y == dec_cross_attn.y   (same Y center, different X)
```

A direct edge with `exitX=1;exitY=0.5;entryX=0;entryY=0.5` then renders as a
straight horizontal arrow with no waypoints needed. If the Y values can't
match exactly (different module heights), pad with vertical whitespace inside
the decoder so the cross-attention center lines up with the encoder output
center.

**The encoder-output → linear case** — when both the decoder top and the
output stack are visible, position the output stack so its bottom (Linear)
aligns with the decoder top (Add & Norm). Same trick: direct edge, no
waypoints.

If alignment is genuinely impossible (e.g. asymmetric stacks), use ONE
waypoint at the midline x between stacks, never multiple waypoints chasing
a node center.

## Hard Rules (always enforced)

1. `id="0"` and `id="1"` always present as first two cells
2. Every vertex HAS `<mxGeometry x y width height as="geometry"/>`
3. Every edge HAS `<mxGeometry relative="1" as="geometry"/>` — self-closing edges are INVALID
4. Edge `source`/`target` must reference existing vertex IDs
5. IDs unique, semantic, lowercase_underscore — no random strings
6. All x/y coordinates multiples of 10; widths multiples of 10; heights may use 2-multiples (30, 32, 38, 42, 50) when needed to encode visual hierarchy
7. All elements within page bounds (x+w ≤ pageWidth, y+h ≤ pageHeight)
8. Uncompressed XML only (no `compressed="true"`)
9. No `--` in XML comments
10. **Flow direction consistent** — every forward edge satisfies `source.y > target.y` for TB diagrams or `source.x < target.x` for LR diagrams. If not, the stack is inverted.
11. **No-Overlap** — no two vertex bounding boxes may intersect, with one allowed exception: a *section container* may contain modules whose bbox is FULLY INSIDE the container's bbox (with ≥10px padding on all four sides). Edges (arrows) are exempt from this rule. See § Section Container Layout for the exact pattern.

## Section Container Layout

Section containers (the dashed gray boxes around encoder/decoder/etc.) are
the most common source of card overlap. Past failures placed section labels
ABOVE their containers, where they intrude on the container of the section
above. Use this pattern instead:

**1. Label INSIDE the container, top-left corner.** Not above. Pattern:

```xml
<mxCell id="enc_sec" value="" style="rounded=1;arcSize=6;fillColor=#F5F5F5;strokeColor=#BDBDBD;strokeWidth=1.5;html=1;dashed=1;dashPattern=10 4" vertex="1" parent="1">
  <mxGeometry x="40" y="200" width="320" height="260" as="geometry"/>
</mxCell>
<mxCell id="enc_lbl" value="Encoder  × N" style="text;html=1;strokeColor=none;fontSize=11;fontFamily=Times New Roman;fontStyle=2;fontColor=#666666;align=left;verticalAlign=top" vertex="1" parent="1">
  <mxGeometry x="50" y="206" width="200" height="16" as="geometry"/>
</mxCell>
```

Label `x` = container.x + 10, `y` = container.y + 6, `align=left`,
`verticalAlign=top`, height 16-18px. Label is fully inside container.

**2. Container padding ≥10px on all sides.** First module's `y` =
container.y + 10 (or +28 if a top-left label takes the first 18px row).
Last module's `y + h` = container.y + container.h − 10. Modules' `x`
≥ container.x + 10 and `x + w` ≤ container.x + container.w − 10.

**3. Section gap ≥30px between adjacent containers.** For two stacked
sections A (above) and B (below), require `B.y − (A.y + A.h) ≥ 30`. Same
horizontally for side-by-side sections.

**4. Drop containers for 2-3 module groups.** Output stack
(Linear/Softmax/Output Probabilities) and input stack (Token/Embedding/
PosEnc) are usually only 3 modules. Skip the dashed container — just float
the modules. Color coding (input red, output yellow) already conveys their
role. This eliminates a whole class of overlap bugs.

**5. When you DO use a container, only for repeated blocks.** Encoder ×N
and decoder ×N benefit from containers because the `× N` annotation lives
in the section label. Single-use groups don't.

## XML Escapes

| Char | Write as |
|------|----------|
| `&` | `&amp;` |
| `<` | `&amp;#60;` (or `&amp;lt;`) | Use numeric ref for safety inside `html=1` |
| `>` | `&amp;#62;` (or `&amp;gt;`) | Numeric ref avoids being parsed as HTML tag |
| `"` | `&quot;` |
| newline | `&#xa;` |

HTML tags in `value` supported with `html=1`, must be XML-escaped:
`&lt;b&gt;Bold&lt;/b&gt;` `&lt;br&gt;` `&lt;sub&gt;x&lt;/sub&gt;`

## Layout Rules

- Content 65-80% of canvas, 20-35% whitespace
- External margin ≥40px, zone gap 40-80px
- **Vertical gap between stacked modules: 24-30px** — shorter than 20px makes arrow shafts invisible
- Same-tier nodes share Y (LR flow) or X (TB flow), equal size
- Main flow direction consistent — don't mix LR and TB in one figure
- No arrow passes through a shape
- Max 2 line crossings
- 3 lines max per node, 25 chars/line English

## Arrow Routing (critical — most common source of errors)

**Golden rule: design the layout so arrows are short and direct.** If you find
yourself adding 3+ waypoints to route around obstacles, the layout is wrong.
Redesign it.

**Tight vertical stacks (preferred):** Place all nodes for one stack
(Encoder/Decoder) in a single vertical column with 24-30px gaps. Integrate
input tokens and embeddings directly into the stack — don't put them in a
separate section far below. This makes ALL arrows short vertical connections
between adjacent nodes that route automatically.

Remember the Flow Direction rule: input at the BOTTOM (largest y), output at
the TOP (smallest y), arrows point UP. The Good column below shows correct
data flow — `Tokens` is at the bottom (largest y) and arrows point upward
through Embed → LSTM 1 → LSTM 2 → Output.

```
Good (arrows ↑):                   Bad (arrows ↓ — inverted stack):
┌─────────┐ ← y=100  output         ┌─────────┐ ← y=100  decoder
│ Output  │                          │ Decoder │
├─────────┤   ↑                      └────┬────┘ y=170
│ LSTM 2  │   ↑ short, vertical           │
├─────────┤   ↑ adjacent arrows            │  ← diagonal arrow
│ LSTM 1  │   ↑                       ┌────┴────┐ y=540
├─────────┤   ↑                       │ Input   │  (far away)
│ Embed   │   ↑                       └─────────┘
├─────────┤   ↑
│ Tokens  │ ← y=600  input
└─────────┘
```

**Horizontal cross-arrows (between left/right stacks):** When two nodes are at
different Y levels, a direct source→target connection will produce an ugly
diagonal. Force right-angle routing with a waypoint in the gap between stacks:

```xml
<mxCell id="e_cross" style="...exitX=1;exitY=0.5;entryX=0;entryY=0.5" ... source="enc_node" target="dec_node">
  <mxGeometry relative="1" as="geometry">
    <Array as="points"><mxPoint x="390" y="484"/><mxPoint x="390" y="324"/></Array>
  </mxGeometry>
</mxCell>
```

The first waypoint starts the horizontal exit at the source's Y, the second
aligns with the target's Y. Use `x` in the gap between the two stacks (e.g.
halfway between encoder and decoder containers).

**Residual / skip connections:** Use dashed lines on the LEFT side of a stack,
exiting/entering at `exitX=0;exitY=0.5` with waypoints. Follow the same pattern
as the vertical main stack — short segments between adjacent layers.

```xml
<mxCell id="e_skip" style="endArrow=classic;html=1;dashed=1;dashPattern=6 3;strokeColor=#666666;strokeWidth=1;exitX=0;exitY=0.5;entryX=0;entryY=0.5" edge="1" parent="1" source="enc_mha" target="enc_an1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points"><mxPoint x="55" y="334"/><mxPoint x="55" y="398"/></Array>
  </mxGeometry>
</mxCell>
```

**Feedback loops:** Route on the outside of the diagram using `curved=1` or
waypoints that stay outside the main structure. Label feedback arrows briefly
(e.g. `s<sub>t-1</sub>`).

**Forbidden:** Never use diagonal arrows crossing through shapes. Never route
arrows "around the outside" of the entire diagram to connect distant nodes —
fix the layout instead. Never use multiple short edge segments pretending to
be one arrow — a single edge with waypoints is always cleaner.

## Visual Style Guide

**Typography:**
- Module titles: 12-14px bold, subsidiary labels 11-12px, details 9-10px
- Unified `fontFamily=Times New Roman`; code uses `Courier New`
- **Text in `value` with multiple lines**: use `&#xa;` (e.g. `value="Line 1&#xa;Line 2"`)
- **Quotes in `value`**: use `&quot;` (e.g. `&quot;Should NEVER happen&quot;`)

**Stroke weights:**
- Main container / emphasis: `strokeWidth=2.5`
- Module box: `strokeWidth=1.5`–`2`
- Subtle border: `strokeWidth=1`
- Key relationship arrow: `strokeWidth=3`–`5` (e.g. isomorphism, main theorem)
- Normal arrow: `strokeWidth=1.5`

**Arrow variants:**
- **Feedback / loop arrow**: `curved=1` with `<Array as="points">` waypoints outside the main structure. Curves look more natural than orthogonal routing for loops.
- **Dashed thin connector**: `endArrow=none;dashed=1;dashPattern=4 3;strokeWidth=1;strokeColor=#999` — used for mapping lines between corresponding elements in side-by-side comparisons
- **Separator line**: `endArrow=none;dashed=1;dashPattern=12 6;strokeColor=#AAAAAA;strokeWidth=1`

**Visual markers:**
- Use Unicode symbols (📐 ⚡ 🧪 ✗ ✓ ▲) as visual tags in phase/role labels — they add instant category recognition without relying solely on color
- `fontStyle` bitmask: 0=normal, 1=bold, 2=italic, 4=underline; 3=bold+italic

**Color conventions:**
- Each color encodes one semantic role. Max 5-6 colors per figure.
- Legend required when colors/lines encode meaning.
- Prefer light fills (`#BBDEFB`, `#C8E6C9`, `#FFCDD2`, `#FFF9C4`, `#FFE0B2`, `#F3E5F5`, `#E3F2FD`, `#F5F5F5`) with matching darker strokes.

## Common Pitfalls (real failures from past generations)

These are the failure modes most often seen in generated diagrams. Scan for
them before writing XML and re-check after.

**1. Inverted stack** — first sub-layer placed at the smallest y, arrows
point downward through the stack. Symptom: in a Transformer encoder you have
`enc_mha (y=310) → enc_an1 (y=380) → enc_ff (y=440) → enc_an2 (y=510)` and
the encoder INPUT is below at y=730 with an arrow going UP into MHA at the
top. This is wrong. Reason: data flows bottom-to-top, so `enc_mha` (first
sub-layer) belongs at the LARGEST y inside the encoder, `enc_an2` at the
smallest. See Flow Direction at the top of this file.

**2. Output stack ordered by reading order, not data flow** — Linear at top
y, Softmax middle, "Output Probabilities" at bottom y, with arrows going
DOWN. Wrong: Output Probabilities is the FINAL output and belongs at the
SMALLEST y (top of canvas). Order from bottom to top should be: decoder
top → Linear → Softmax → Output Probabilities.

**3. e_out connects to wrong source** — the edge from decoder to Linear is
sourced from the FIRST decoder sub-layer (e.g. `dec_mmha`) instead of the
LAST one (the topmost Add & Norm). Symptom: a long edge with 3+ waypoints
wrapping around the diagram. Fix: the edge source is the node with the
SMALLEST y inside the decoder stack (the "top" of the stack = the last
computation in data-flow order).

**4. Input section internally inverted** — Source Tokens at smaller y
than Input Embedding, with arrow tokens→embedding going DOWN. Wrong:
embedding processes tokens, so embedding is the next step and belongs ABOVE
tokens (smaller y). Same rule applies to (token → embedding → positional
encoding) — list in data-flow order, assign decreasing y.

**5. Cross-stack Y misalignment** — encoder output at y=510, decoder
cross-attention at y=440. The K,V edge between them needs waypoints to
route the 70px height difference, producing a visible jog. Fix: make
`enc_an_top.y == dec_cross_attn.y` (set the same y center), then a direct
horizontal edge with `exitX=1;entryX=0` renders cleanly with no waypoints.

**6. Section header collision with neighbor section** — older diagrams
placed section labels ABOVE their container (e.g. label y = container.y −
22), which intruded into the section above when sections were stacked
close together. Wrong. Place labels INSIDE the container at top-left
(label x = container.x + 10, y = container.y + 6, with `align=left;
verticalAlign=top`). See § Section Container Layout for the full pattern.

**7. Double-escaped HTML in `value`** — writing `Add &amp;amp; Norm` when
you only meant one level of escape. Inside `value="..."` with `html=1`,
write `&amp;` for a literal `&` (XML-level escape). Drawio renders that
as `&`. Writing `&amp;amp;` displays as `&amp;` — the literal HTML entity
text shown to the reader. Use `&amp;` once, not twice.

## Self-Check (output pass/fail for each)

```
1.  XML well-formed:                  pass/fail
2.  Wrappers present:                 pass/fail  
3.  IDs unique:                       pass/fail
4.  Edge refs valid:                  pass/fail
5.  All vertices have geometry:       pass/fail
6.  All edges have mxGeometry:        pass/fail
7.  No out-of-page elements:          pass/fail
8.  No unescaped &lt;&gt;&amp; in values:    pass/fail
9.  All x/y coords multiples of 10; widths multiples of 10; heights may be 30/32/38/42/50/etc:  pass/fail
10. No arrows through shapes:         pass/fail
11. Fonts consistent:                 pass/fail
12. Flow direction consistent (every forward edge source.y > target.y for TB, source.x < target.x for LR):  pass/fail
13. No double-escaped &amp;amp; in values:   pass/fail
```
