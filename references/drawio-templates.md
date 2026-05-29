# Canonical Architecture and Layout Templates

Read this file when the user requests any conceptual diagram. Two kinds of
template are available:

- **§1–§8** are specific architectures (Transformer, Diffusion, RAG, etc.).
  If the request matches one of these, copy the template directly.
- **§9–§13** are general layout patterns (vertical stack, horizontal
  pipeline, center hub, side-by-side comparison, grid). If no specific
  template fits, pick the closest layout pattern and adapt it.

All templates follow the Flow Direction and No-Overlap rules from
`drawio-reference.md`. For specific architectures (§1–§4), the convention
is bottom-to-top TB flow (`source.y > target.y`). For general layouts
(§5–§9), the flow direction is stated per pattern.

## Index

### Specific architectures

| Architecture | When to use | Section |
|---|---|---|
| Transformer encoder-decoder | Translation, summarization, encoder-decoder LLM | §1 |
| Diffusion forward/reverse | DDPM/DDIM, score-based, flow-matching | §2 |
| RAG pipeline | Retrieval-augmented LLM systems | §3 |
| Multi-stage training | Pretrain → SFT → RLHF, foundation-model recipes | §4 |

### General layout patterns

| Pattern | When to use | Section |
|---|---|---|
| Vertical stack (TB) | Protocol stacks, layered architectures, dependency chains | §2 |
| Horizontal pipeline (LR) | Data processing pipelines, CI/CD, multi-stage workflows | §3 |
| Center hub + satellites | CPU/system overviews, IoT gateways, star-topology networks | §4 |
| Side-by-side comparison | Before/after, method A vs B, paired-element comparison | §8 |
| Grid / table layout | Feature matrices, parameter tables, ablation grids | §2 |

### Classic diagram types

| Type | When to use | Section |
|---|---|---|
| Flowchart | Decision trees, process flows, algorithm logic | §3 |
| Entity-Relationship Diagram (ERD) | Database schemas, data models, table relationships | §4 |
| UML Class Diagram | OOP design, architecture modeling, inheritance hierarchies | §8 |
| Sequence Diagram | Protocol interactions, API call flows, message passing | §2 |
| State Machine Diagram | State transitions, formal methods, protocol specifications | §3 |
| Data Flow Diagram (DFD) | Software engineering, system data flows, process modeling | §4 |

If the user's request doesn't match any of these, fall back to the general
workflow in `draw-diagram.md` and apply the Flow Direction rule
manually. Don't force-fit a non-matching architecture onto a template.

---

## §1 Transformer encoder-decoder (Vaswani 2017)

**Canvas:** 920×870, portrait. Encoder on the left, decoder on the right,
output stack above the decoder, source input below the encoder, target input
below the decoder.

**Edge convention:** All edges use the orthogonal routing base from
`drawio-reference.md` — `edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic`.
Residuals add `dashed=1;dashPattern=6 3;strokeColor=#666666;strokeWidth=1`.
K,V cross-attention adds `exitX=1;entryX=0;strokeColor=#9673A6`.

**Layout choices that prevent overlap:**

1. Output stack and input groups (3 modules each) have NO dashed container —
   they're floating with color-coding doing the grouping work.
2. Encoder and decoder containers exist (because of `× N` annotation), with
   labels placed INSIDE the container at top-left, not above.
3. Encoder bottom (y=650) is LOWER than decoder bottom (y=590) because the
   encoder is shorter but its TOP aligns with decoder cross-attention. This
   makes K,V cross-attention a clean straight horizontal line and is
   Vaswani's actual layout choice.
4. ≥30px clear gap between every section: linear → decoder (32), encoder →
   source-input (30), decoder → target-input (30).

**Self-check** (before writing):
1. All forward edges: `source.y > target.y` ✓
2. enc_an2 center y (435) == dec_ca center y (435) → K,V straight horizontal ✓
3. Encoder modules inside enc_sec with ≥10px padding. Same for decoder ✓
4. Section gaps: linear→dec(32), enc→src(30), dec→tgt(30) — all ≥30 ✓
5. All coords x/y/w multiples of 10; heights use 30/32/38/42/50 ✓

**Node table** (data-flow order; y decreases as you go up the stack):

```
SECTION       | id          | label                          | x   | y   | w   | h
output        | outp        | Output Probabilities           | 540 | 20  | 340 | 42
output        | softmax     | Softmax                        | 600 | 80  | 220 | 38
output        | linear      | Linear                         | 600 | 140 | 220 | 38
DECODER       | dec_sec     | (container)                    | 520 | 210 | 380 | 380
DECODER       | dec_lbl     | "Decoder × N" (inside top-left)| 530 | 216 | 200 | 16
DECODER       | dec_an3     | Add & Norm                     | 540 | 240 | 340 | 30
DECODER       | dec_ff      | Feed Forward                   | 540 | 290 | 340 | 50
DECODER       | dec_an2     | Add & Norm                     | 540 | 360 | 340 | 30
DECODER       | dec_ca      | Multi-Head Cross-Attention     | 540 | 410 | 340 | 50  ← center y=435
DECODER       | dec_an1     | Add & Norm                     | 540 | 480 | 340 | 30
DECODER       | dec_mmha    | Masked Multi-Head Self-Attn    | 540 | 530 | 340 | 50
ENCODER       | enc_sec     | (container)                    | 40  | 390 | 320 | 260
ENCODER       | enc_lbl     | "Encoder × N" (inside top-left)| 50  | 396 | 200 | 16
ENCODER       | enc_an2     | Add & Norm                     | 60  | 420 | 280 | 30  ← center y=435
ENCODER       | enc_ff      | Feed Forward                   | 60  | 470 | 280 | 50
ENCODER       | enc_an1     | Add & Norm                     | 60  | 540 | 280 | 30
ENCODER       | enc_mha     | Multi-Head Self-Attention      | 60  | 590 | 280 | 50
src_input     | src_pos     | Positional Encoding            | 60  | 680 | 280 | 32
src_input     | src_emb     | Input Embedding                | 60  | 730 | 280 | 38
src_input     | src_tk      | Source Tokens                  | 60  | 790 | 280 | 42
tgt_input     | tgt_pos     | Positional Encoding            | 540 | 620 | 340 | 32
tgt_input     | tgt_emb     | Output Embedding               | 540 | 670 | 340 | 38
tgt_input     | tgt_tk      | Target Tokens (shifted right)  | 540 | 730 | 340 | 42
KV label      | kv_lbl      | "K, V"                         | 420 | 412 | 40  | 16
```

**Edge table** (every forward edge satisfies `source.y > target.y`):

```
id          | source     | target     | style                                   | notes
e_tk_emb_s  | src_tk     | src_emb    | solid black                             | input flow ↑
e_emb_pos_s | src_emb    | src_pos    | solid black                             |
e_pos_enc   | src_pos    | enc_mha    | solid black                             | enters encoder bottom
e_e_mha_an1 | enc_mha    | enc_an1    | solid black                             | encoder stack ↑
e_e_an1_ff  | enc_an1    | enc_ff     | solid black                             |
e_e_ff_an2  | enc_ff     | enc_an2    | solid black                             |
e_kv        | enc_an2    | dec_ca     | colored, exitX=1;exitY=0.5;entryX=0;entryY=0.5 | straight horizontal (centers both 435)
e_tk_emb_t  | tgt_tk     | tgt_emb    | solid black                             | target input ↑
e_emb_pos_t | tgt_emb    | tgt_pos    | solid black                             |
e_pos_dec   | tgt_pos    | dec_mmha   | solid black                             | enters decoder bottom
e_d_mha_an1 | dec_mmha   | dec_an1    | solid black                             | decoder stack ↑
e_d_an1_ca  | dec_an1    | dec_ca     | solid black                             |
e_d_ca_an2  | dec_ca     | dec_an2    | solid black                             |
e_d_an2_ff  | dec_an2    | dec_ff     | solid black                             |
e_d_ff_an3  | dec_ff     | dec_an3    | solid black                             |
e_dec_lin   | dec_an3    | linear     | solid black                             | decoder → output
e_lin_sm    | linear     | softmax    | solid black                             | output stack ↑
e_sm_outp   | softmax    | outp       | solid black                             |
```

Residuals: dashed thin gray, `exitX=0;exitY=0.5;entryX=0;entryY=0.5` for
encoder (waypoints at x=45, inside container left edge), and
`exitX=1;exitY=0.5;entryX=1;entryY=0.5` for decoder (waypoints at x=895,
inside container right edge). One residual per (sub-layer → its Add&Norm).

**Self-check after instantiating:**
1. For every adjacent pair in the data-flow order, verify `source.y > target.y`.
2. Encoder modules `bbox` fully inside `enc_sec` bbox with ≥10px padding on
   all sides. Same for decoder.
3. Section labels (`enc_lbl`, `dec_lbl`) inside their container, not above.
4. Output stack bottom (linear y+h = 178) and decoder top (210) have ≥30px
   gap. Same for encoder bottom / source input top, decoder bottom / target
   input top.
5. enc_an2 center y == dec_ca center y (both 435) so K,V is horizontal.

**XML skeleton** — copy this and adjust names/counts:

```xml
<mxfile host="app.diagrams.net">
  <diagram name="Transformer" id="transformer">
    <mxGraphModel dx="1200" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="920" pageHeight="870" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- ===== Output stack (top, no container) ===== -->
        <mxCell id="outp" value="Output Probabilities" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#FFF2CC;strokeColor=#D6B656;strokeWidth=1.5;fontSize=12;fontFamily=Times New Roman;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="540" y="20" width="340" height="42" as="geometry"/>
        </mxCell>
        <mxCell id="softmax" value="Softmax" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#FFE6CC;strokeColor=#D79B00;strokeWidth=1.5;fontSize=12;fontFamily=Times New Roman;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="600" y="80" width="220" height="38" as="geometry"/>
        </mxCell>
        <mxCell id="linear" value="Linear" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#FFE6CC;strokeColor=#D79B00;strokeWidth=1.5;fontSize=12;fontFamily=Times New Roman;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="600" y="140" width="220" height="38" as="geometry"/>
        </mxCell>

        <!-- ===== Decoder section (container y=210..590, label INSIDE top-left) ===== -->
        <mxCell id="dec_sec" value="" style="rounded=1;arcSize=6;fillColor=#F5F5F5;strokeColor=#BDBDBD;strokeWidth=1.5;html=1;dashed=1;dashPattern=10 4" vertex="1" parent="1">
          <mxGeometry x="520" y="210" width="380" height="380" as="geometry"/>
        </mxCell>
        <mxCell id="dec_lbl" value="Decoder  × N" style="text;html=1;strokeColor=none;fontSize=11;fontFamily=Times New Roman;fontStyle=2;fontColor=#666666;align=left;verticalAlign=top" vertex="1" parent="1">
          <mxGeometry x="530" y="216" width="200" height="16" as="geometry"/>
        </mxCell>

        <!-- Decoder modules: top → bottom; data flows ↑ (smaller y is later in flow) -->
        <mxCell id="dec_an3" value="Add &amp; Norm" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#999999;strokeWidth=1;fontSize=11;fontFamily=Times New Roman;fontColor=#666666;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="540" y="240" width="340" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="dec_ff" value="Feed Forward" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#FFE6CC;strokeColor=#D79B00;strokeWidth=1.5;fontSize=12;fontFamily=Times New Roman;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="540" y="290" width="340" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="dec_an2" value="Add &amp; Norm" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#999999;strokeWidth=1;fontSize=11;fontFamily=Times New Roman;fontColor=#666666;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="540" y="360" width="340" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="dec_ca" value="Multi-Head Cross-Attention" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#E1D5E7;strokeColor=#9673A6;strokeWidth=1.5;fontSize=12;fontFamily=Times New Roman;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="540" y="410" width="340" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="dec_an1" value="Add &amp; Norm" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#999999;strokeWidth=1;fontSize=11;fontFamily=Times New Roman;fontColor=#666666;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="540" y="480" width="340" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="dec_mmha" value="Masked Multi-Head Self-Attention" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#E1D5E7;strokeColor=#9673A6;strokeWidth=1.5;fontSize=12;fontFamily=Times New Roman;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="540" y="530" width="340" height="50" as="geometry"/>
        </mxCell>

        <!-- ===== Encoder section (container y=390..650, enc_an2 center y=435 = dec_ca center y=435) ===== -->
        <mxCell id="enc_sec" value="" style="rounded=1;arcSize=6;fillColor=#F5F5F5;strokeColor=#BDBDBD;strokeWidth=1.5;html=1;dashed=1;dashPattern=10 4" vertex="1" parent="1">
          <mxGeometry x="40" y="390" width="320" height="260" as="geometry"/>
        </mxCell>
        <mxCell id="enc_lbl" value="Encoder  × N" style="text;html=1;strokeColor=none;fontSize=11;fontFamily=Times New Roman;fontStyle=2;fontColor=#666666;align=left;verticalAlign=top" vertex="1" parent="1">
          <mxGeometry x="50" y="396" width="200" height="16" as="geometry"/>
        </mxCell>

        <mxCell id="enc_an2" value="Add &amp; Norm" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#999999;strokeWidth=1;fontSize=11;fontFamily=Times New Roman;fontColor=#666666;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="60" y="420" width="280" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="enc_ff" value="Feed Forward" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#FFE6CC;strokeColor=#D79B00;strokeWidth=1.5;fontSize=12;fontFamily=Times New Roman;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="60" y="470" width="280" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="enc_an1" value="Add &amp; Norm" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#999999;strokeWidth=1;fontSize=11;fontFamily=Times New Roman;fontColor=#666666;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="60" y="540" width="280" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="enc_mha" value="Multi-Head Self-Attention" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#E1D5E7;strokeColor=#9673A6;strokeWidth=1.5;fontSize=12;fontFamily=Times New Roman;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="60" y="590" width="280" height="50" as="geometry"/>
        </mxCell>

        <!-- ===== Source input (no container, BELOW encoder, ≥30px gap) ===== -->
        <mxCell id="src_pos" value="Positional Encoding" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#F8CECC;strokeColor=#B85450;strokeWidth=1.5;fontSize=12;fontFamily=Times New Roman;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="60" y="680" width="280" height="32" as="geometry"/>
        </mxCell>
        <mxCell id="src_emb" value="Input Embedding" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#F8CECC;strokeColor=#B85450;strokeWidth=1.5;fontSize=12;fontFamily=Times New Roman;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="60" y="730" width="280" height="38" as="geometry"/>
        </mxCell>
        <mxCell id="src_tk" value="Source Tokens (x&lt;sub&gt;1&lt;/sub&gt;, …, x&lt;sub&gt;n&lt;/sub&gt;)" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#999999;strokeWidth=1.5;fontSize=12;fontFamily=Times New Roman;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="60" y="790" width="280" height="42" as="geometry"/>
        </mxCell>

        <!-- ===== Target input (no container, BELOW decoder, ≥30px gap) ===== -->
        <mxCell id="tgt_pos" value="Positional Encoding" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#F8CECC;strokeColor=#B85450;strokeWidth=1.5;fontSize=12;fontFamily=Times New Roman;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="540" y="620" width="340" height="32" as="geometry"/>
        </mxCell>
        <mxCell id="tgt_emb" value="Output Embedding" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#F8CECC;strokeColor=#B85450;strokeWidth=1.5;fontSize=12;fontFamily=Times New Roman;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="540" y="670" width="340" height="38" as="geometry"/>
        </mxCell>
        <mxCell id="tgt_tk" value="Target Tokens (shifted right)" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#999999;strokeWidth=1.5;fontSize=12;fontFamily=Times New Roman;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle" vertex="1" parent="1">
          <mxGeometry x="540" y="730" width="340" height="42" as="geometry"/>
        </mxCell>

        <!-- ===== EDGES — every forward edge has source.y > target.y ===== -->
        <mxCell id="e_stk_emb" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="src_tk" target="src_emb"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_semb_pos" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="src_emb" target="src_pos"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_spos_enc" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="src_pos" target="enc_mha"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_emha_an1" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="enc_mha" target="enc_an1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_ean1_ff" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="enc_an1" target="enc_ff"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_eff_an2" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="enc_ff" target="enc_an2"><mxGeometry relative="1" as="geometry"/></mxCell>
        <!-- K,V cross-attention: enc_an2 center y=435 = dec_ca center y=435, straight horizontal -->
        <mxCell id="e_kv" style="endArrow=classic;html=1;strokeColor=#9673A6;strokeWidth=1.5;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" parent="1" source="enc_an2" target="dec_ca"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="kv_lbl" value="K, V" style="text;html=1;fontSize=10;fontFamily=Times New Roman;fontColor=#9673A6;fontStyle=2;align=center" vertex="1" parent="1">
          <mxGeometry x="420" y="412" width="40" height="16" as="geometry"/>
        </mxCell>
        <mxCell id="e_ttk_emb" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="tgt_tk" target="tgt_emb"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_temb_pos" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="tgt_emb" target="tgt_pos"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_tpos_dec" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="tgt_pos" target="dec_mmha"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_dmha_an1" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="dec_mmha" target="dec_an1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_dan1_ca" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="dec_an1" target="dec_ca"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_dca_an2" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="dec_ca" target="dec_an2"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_dan2_ff" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="dec_an2" target="dec_ff"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_dff_an3" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="dec_ff" target="dec_an3"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_dec_lin" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="dec_an3" target="linear"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_lin_sm" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="linear" target="softmax"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e_sm_outp" style="endArrow=classic;html=1;strokeColor=#333333;strokeWidth=1.5" edge="1" parent="1" source="softmax" target="outp"><mxGeometry relative="1" as="geometry"/></mxCell>

        <!-- Encoder residuals (left side, dashed thin, x=45 inside enc_sec) -->
        <mxCell id="e_ers1" style="endArrow=classic;html=1;dashed=1;dashPattern=6 3;strokeColor=#666666;strokeWidth=1;exitX=0;exitY=0.5;entryX=0;entryY=0.5" edge="1" parent="1" source="enc_mha" target="enc_an1">
          <mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="45" y="615"/><mxPoint x="45" y="555"/></Array></mxGeometry>
        </mxCell>
        <mxCell id="e_ers2" style="endArrow=classic;html=1;dashed=1;dashPattern=6 3;strokeColor=#666666;strokeWidth=1;exitX=0;exitY=0.5;entryX=0;entryY=0.5" edge="1" parent="1" source="enc_ff" target="enc_an2">
          <mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="45" y="495"/><mxPoint x="45" y="435"/></Array></mxGeometry>
        </mxCell>

        <!-- Decoder residuals (right side, dashed thin, x=895 inside dec_sec) -->
        <mxCell id="e_drs1" style="endArrow=classic;html=1;dashed=1;dashPattern=6 3;strokeColor=#666666;strokeWidth=1;exitX=1;exitY=0.5;entryX=1;entryY=0.5" edge="1" parent="1" source="dec_mmha" target="dec_an1">
          <mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="895" y="555"/><mxPoint x="895" y="495"/></Array></mxGeometry>
        </mxCell>
        <mxCell id="e_drs2" style="endArrow=classic;html=1;dashed=1;dashPattern=6 3;strokeColor=#666666;strokeWidth=1;exitX=1;exitY=0.5;entryX=1;entryY=0.5" edge="1" parent="1" source="dec_ca" target="dec_an2">
          <mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="895" y="435"/><mxPoint x="895" y="375"/></Array></mxGeometry>
        </mxCell>
        <mxCell id="e_drs3" style="endArrow=classic;html=1;dashed=1;dashPattern=6 3;strokeColor=#666666;strokeWidth=1;exitX=1;exitY=0.5;entryX=1;entryY=0.5" edge="1" parent="1" source="dec_ff" target="dec_an3">
          <mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="895" y="315"/><mxPoint x="895" y="255"/></Array></mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```



---

## §2 Diffusion (forward + reverse process)

**When to use:** DDPM/DDIM/score-based/flow-matching figures showing the
two-direction Markov chain. Canonical Ho et al. 2020 Figure 2 layout.

**Canvas:** 1100×440. Two parallel chains stacked vertically — forward on
top (q, →), reverse on bottom (p_θ, ←). Nodes are square placeholders for
sample images (h=80, w=100-120).

**Edge convention:** All edges use the orthogonal routing base from
`drawio-reference.md`. Forward edges (blue): `endArrow=classic;strokeColor=#1976D2`. Reverse edges (orange): `endArrow=classic;strokeColor=#E65100` (these have `source.x > target.x` because the reverse process flows right-to-left — this is a documented exception per-chain per `drawio-reference.md`). Dashed edges across the "…" gaps: `dashed=1;dashPattern=6 3`.

**Layout choices:**
- The reverse chain renders edges with `source.x > target.x` because the
  process flows right-to-left. This is allowed: the rule "every forward
  edge has source.x < target.x for LR" applies per-flow within a single
  chain. Treat the reverse chain as its own LR flow with its own positive
  direction (right-to-left here).
- Five visible nodes per chain: x_0, x_1, x_{t-1}, x_t, x_T, with text "..."
  fillers between x_1↔x_{t-1} and x_t↔x_T to indicate omitted steps.
- Color: x_0 light green (data), x_T light red (noise), intermediates white.
- Forward arrows blue, reverse arrows orange (or any two distinguishable
  colors with a legend).

**Node table:**

```
SECTION  | id           | label                              | x   | y   | w   | h
title    | t_fwd        | Forward Process: q(x_t | x_{t-1})  | 280 | 30  | 540 | 24
forward  | f_x0         | x_0  (data)                        | 80  | 80  | 100 | 80
forward  | f_x1         | x_1                                | 240 | 80  | 100 | 80
forward  | f_dots1      | …                                  | 380 | 110 | 80  | 20
forward  | f_xtm1       | x_{t-1}                            | 480 | 80  | 120 | 80
forward  | f_xt         | x_t                                | 640 | 80  | 120 | 80
forward  | f_dots2      | …                                  | 800 | 110 | 80  | 20
forward  | f_xT         | x_T  (noise)                       | 900 | 80  | 100 | 80
title    | t_rev        | Reverse Process: p_θ(x_{t-1} | x_t)| 280 | 240 | 540 | 24
reverse  | r_xT         | x_T                                | 900 | 290 | 100 | 80
reverse  | r_dots2      | …                                  | 800 | 320 | 80  | 20
reverse  | r_xt         | x_t                                | 640 | 290 | 120 | 80
reverse  | r_xtm1       | x_{t-1}                            | 480 | 290 | 120 | 80
reverse  | r_dots1      | …                                  | 380 | 320 | 80  | 20
reverse  | r_x1         | x_1                                | 240 | 290 | 100 | 80
reverse  | r_x0         | x_0                                | 80  | 290 | 100 | 80
```

**Edge table:**

```
id    | source   | target   | style
e_f01 | f_x0     | f_x1     | →, blue, label "q"
e_f12 | f_x1     | f_xtm1   | →, blue, dashed (over the dots)
e_f23 | f_xtm1   | f_xt     | →, blue, label "q(x_t | x_{t-1})"
e_f34 | f_xt     | f_xT     | →, blue, dashed
e_r10 | r_x1     | r_x0     | ←, orange, label "p_θ"
e_r21 | r_xtm1   | r_x1     | ←, orange, dashed
e_r32 | r_xt     | r_xtm1   | ←, orange, label "p_θ(x_{t-1} | x_t)"
e_r43 | r_xT     | r_xt     | ←, orange, dashed
```

**Style hint** for sample-image placeholder nodes:
`rounded=1;arcSize=8;fillColor=#FFFFFF;strokeColor=#666666;strokeWidth=1.5;
fontFamily=Times New Roman;fontSize=14;fontStyle=2;align=center;verticalAlign=middle`

If you want to embed actual sample images, replace each square's `value=""`
with `<img src="data:image/png;base64,...">` HTML or use drawio's image
shape (`shape=image;image=...`).

**Self-check:**
1. Forward chain: all edges `source.x < target.x`
2. Reverse chain: all edges `source.x > target.x` (documented exception)
3. Row gap: forward bottom (160) to reverse top (290) = 130px, no overlap
4. Canvas 1100x440: all nodes within bounds

---

## §3 RAG pipeline

**When to use:** Retrieval-augmented LLM system figures. Common in 2024+
LLM application papers.

**Edge convention:** All edges use the orthogonal routing base from `drawio-reference.md`.
LR pipeline edges: `endArrow=classic;strokeColor=#333333;strokeWidth=1.5;exitX=1;entryX=0`.
Vertical edges (DB→retriever, LLM→answer): `exitX=0.5` with bend waypoints.

**Canvas:** 1180×360. Single LR pipeline. The vector DB hangs below the
retriever as a cylinder (the canonical "external knowledge" symbol).

**Node table:**

```
SECTION  | id          | label                               | x    | y   | w   | h
input    | q           | User Query                          | 30   | 140 | 130 | 60
process  | enc         | Query Encoder (e.g., BGE)           | 200  | 140 | 150 | 60
process  | retr        | Retriever (top-k similarity)        | 390  | 140 | 160 | 60
data     | docs        | Top-k Documents                     | 590  | 140 | 150 | 60
process  | rerank      | Reranker (cross-encoder)            | 780  | 140 | 150 | 60
process  | llm         | LLM Generator                       | 970  | 140 | 130 | 60
output   | ans         | Answer                              | 970  | 260 | 130 | 60
storage  | kb          | Vector DB (knowledge base)          | 390  | 260 | 160 | 60
```

The Vector DB cylinder uses `shape=cylinder3;fillColor=#E1F5FE;strokeColor=#0288D1`.

**Edge table:**

```
id      | source | target | style
e_q_e   | q      | enc    | → solid black
e_e_r   | enc    | retr   | → solid black
e_r_d   | retr   | docs   | → solid black
e_d_rr  | docs   | rerank | → solid black
e_rr_l  | rerank | llm    | → solid black
e_l_a   | llm    | ans    | ↓ solid black (LLM down to Answer)
e_kb_r  | kb     | retr   | ↑ dashed gray, label "embeddings + index"
```

**Layout choices:**
- LR primary flow at y=140. Vector DB and Answer sit at y=260, BELOW the
  pipeline, with vertical arrows feeding/exiting. Source and target are
  always y_source > y_target for upward arrows (e.g., kb → retr, since
  data flows from DB up into retriever).
- llm → ans is a downward arrow (data exits the pipeline toward the user).
  Treat this as a "pipeline outlet" not a forward flow edge.
- Use Operators palette colors: process boxes light blue (`#DAE8FC`/
  `#6C8EBF`), data boxes light orange (`#FFE6CC`/`#D79B00`), input red
  (`#F8CECC`/`#B85450`), output yellow (`#FFF2CC`/`#D6B656`), DB cyan.

**Optional extensions:**
- Add a "Prompt Template" box between rerank and llm if showing prompt
  construction explicitly.
- Add a "Citation extractor" between llm and ans for citation-grounded
  RAG.



---

## §4 Multi-stage training pipeline

**When to use:** Foundation-model recipe figures: Pretrain → SFT → RLHF
→ Eval, or analogous multi-stage workflows. Common in LLM/VLM/codegen
papers since 2023.

**Edge convention:** All edges use the orthogonal routing base from `drawio-reference.md`.
Stage→stage edges: `strokeWidth=2.5` (bold, parameter inheritance).
Data source→stage edges: `strokeWidth=1;strokeColor=#999` (↑ thin gray).

**Canvas:** 1180×360. LR pipeline of 4-5 stage boxes; below each stage,
a small "data" box names the dataset / objective / size.

**Node table:**

```
SECTION  | id          | label                            | x    | y   | w   | h
stage    | s1          | Stage 1: Pretrain                | 60   | 100 | 220 | 70
data     | d1          | C4 + Common Crawl (1.5T tokens)  | 60   | 200 | 220 | 50
stage    | s2          | Stage 2: SFT                     | 320  | 100 | 220 | 70
data     | d2          | 50K instruction pairs            | 320  | 200 | 220 | 50
stage    | s3          | Stage 3: RLHF (PPO)              | 580  | 100 | 220 | 70
data     | d3          | 100K preference pairs            | 580  | 200 | 220 | 50
stage    | s4          | Stage 4: Eval                    | 840  | 100 | 220 | 70
data     | d4          | MMLU + HumanEval + ARC           | 840  | 200 | 220 | 50
output   | model       | Final Model                      | 1080 | 100 | 70  | 70
```

**Edge table:**

```
id      | source | target | style
e_s1_s2 | s1     | s2     | → bold, label "θ₀"
e_s2_s3 | s2     | s3     | → bold, label "θ_SFT"
e_s3_s4 | s3     | s4     | → bold, label "θ_RLHF"
e_s4_m  | s4     | model  | → bold
e_d1_s1 | d1     | s1     | ↑ thin gray, "trains"
e_d2_s2 | d2     | s2     | ↑ thin gray
e_d3_s3 | d3     | s3     | ↑ thin gray
e_d4_s4 | d4     | s4     | ↑ thin gray, "evaluates"
```

**Layout choices:**
- Stages aligned at y=100, data tags aligned at y=200. Both rows form
  parallel bands.
- Stage boxes use a stronger fill (`#DAE8FC`/`#6C8EBF` blue), data tags
  use a lighter fill or just a white background with thin border.
- Stage→stage edges are bold (`strokeWidth=2.5`) with the running
  parameter label (θ₀, θ_SFT, etc.) above the arrow. This shows
  parameter inheritance, which is the figure's main point.
- Data→stage edges thin gray (`strokeWidth=1`, `strokeColor=#999`).

**Variants:**
- Add a "Reward Model" subbox during Stage 3 if the RLHF figure needs to
  show RM training separately.
- For DPO instead of PPO, change the Stage 3 label and skip the reward
  model subbox.
- For continual pretraining, add a feedback loop from Stage 4 back to
  Stage 1 with a dashed curve.



---

## §5 Vertical stack (TB)

**When to use:** Protocol stacks, layered architectures, dependency chains,
hierarchies — any figure where nodes are logically stacked top-to-bottom
in a single column. Not specifically ML; use the Flow Direction rule to
decide which end is "input" and which is "output."

**Canvas:** 600×750 portrait. Single column centered.

**Layout conventions:**
- All nodes share the same `x` and `w`, vertically centered in the canvas
  (`x = (pageWidth - w) / 2`).
- Equal vertical gap between adjacent nodes (24–30px).
- Arrows between adjacent nodes only. No diagonal or long cross-arrows.
- Flow direction: decide which way data flows. If bottom-to-top (ML
  convention), place input at the largest y and ensure `source.y > target.y`
  for every forward edge. If top-to-bottom (protocol stack convention,
  e.g. OSI), place the topmost layer at the smallest y and arrows go DOWN.
  **Disclose the convention in the first comment of the XML.**

**Node table** (6-node example, bottom-up data flow):

```
id      | label        | x   | y   | w   | h
n6_out  | Output       | 140 | 40  | 320 | 50
n5      | Layer 5      | 140 | 120 | 320 | 50
n4      | Layer 4      | 140 | 200 | 320 | 50
n3      | Layer 3      | 140 | 280 | 320 | 50
n2      | Layer 2      | 140 | 360 | 320 | 50
n1_in   | Input        | 140 | 440 | 320 | 50
```

Edge chain: n1_in → n2 → n3 → n4 → n5 → n6_out. All vertical, no
waypoints. Every edge satisfies `source.y > target.y` (arrows go UP).

**To adapt:** change node count, labels, and the flow direction comment.
Shift all `y` values by the same offset to move the stack up or down.



---

## §6 Horizontal pipeline (LR)

**When to use:** Data processing pipelines, CI/CD, multi-stage workflows
— anything where stages are sequential and flow left to right.

**Canvas:** 1100×300 landscape. Single row centered vertically.

**Layout conventions:**
- All stage nodes share the same `y` and `h`, spaced equally along X.
- Arrows between adjacent stages, going RIGHT (`source.x < target.x`).
- Labels above or below each stage naming the input/output of that stage.
  Small data-source boxes can hang below stages (e.g., dataset names).
- Use vertical arrows from data-source boxes UP into the pipeline stage.

**Node table** (5-stage example with 3 data-source boxes):

```
id      | label              | x   | y   | w   | h
s1      | Stage 1: Ingest   | 30  | 100 | 170 | 60
s2      | Stage 2: Process  | 240 | 100 | 170 | 60
s3      | Stage 3: Validate | 450 | 100 | 170 | 60
s4      | Stage 4: Export   | 660 | 100 | 170 | 60
s5      | Stage 5: Archive  | 870 | 100 | 170 | 60
d1      | Raw Data (S3)     | 30  | 200 | 170 | 40
d3      | Schema V2         | 450 | 200 | 170 | 40
d5      | Parquet / Iceberg | 870 | 200 | 170 | 40
```

Edge chain: s1 → s2 → s3 → s4 → s5 (all LR, `source.x < target.x`).
Data-source → stage edges: d1 → s1 (↑), d3 → s3 (↑), d5 → s5 (↑).

**To adapt:** add/remove stages, rename labels, change data-source box
labels to match your pipeline's artifacts. Keep `x` spacing uniform:
`gap = (pageWidth - n * w) / (n + 1)` for n equally-spaced stages.



---

## §7 Center hub + satellites

**When to use:** System overviews, CPU/SoC block diagrams, IoT gateway
topologies, any star-topology or hub-and-spoke figure.

**Canvas:** 750×600.

**Layout conventions:**
- One central component (the "hub") placed at the canvas center.
- 2–6 satellite nodes placed around it: left, right, above, below, and
  optionally at the four corners.
- Radial connecting arrows from hub to each satellite (or bidirectional).
- Satellites may connect to each other with dashed side edges.
- **Flow direction is not TB or LR.** The hub pattern is inherently radial.
  Edges exit the hub at the side closest to each satellite. Direct edges,
  no waypoints unless satellites are at the same angle from the hub.
- Hub uses a distinct fill color or heavier stroke to stand out.

**Node table** (4-satellite example):

```
id      | label                 | x   | y   | w   | h
hub     | System Core (Hub)     | 255 | 230 | 240 | 100
top     | Satellite A (Input)   | 255 | 60  | 240 | 60
right   | Satellite B (Output)  | 560 | 250 | 150 | 60
bottom  | Satellite C (Storage) | 255 | 460 | 240 | 60
left    | Satellite D (Control) | 40  | 250 | 150 | 60
```

Edges:
- top → hub (↓, enters hub top)
- hub → right (→, exits hub right)
- hub → bottom (↓, exits hub bottom)
- left → hub (→, exits left right, enters hub left)

All edges are direct `exitX=0.5;exitY=1` or `exitX=1;exitY=0.5` etc.
No waypoints needed because satellites are axis-aligned with the hub.

**To adapt:** change hub and satellite labels, add corner satellites
at (40, 60), (560, 60), (560, 460), (40, 460) for an 8-node star.



---

## §8 Side-by-side comparison

**When to use:** Before/after comparisons, Method A vs Method B, paired
element mapping between two systems.

**Canvas:** 900×650. Two vertical columns side by side.

**Layout conventions:**
- Left and right columns share the same module count, heights, and Y
  positions so paired elements sit at the same visual row.
- A vertical separator line (dashed, gray, no arrowheads) runs down the
  middle gap.
- Dashed thin mapping lines (no arrowheads) connect corresponding
  elements between columns.
- Column labels sit ABOVE each column (or at the top of each column as a
  colored header bar).

**Node table** (4-pair example):

```
id         | label            | x   | y   | w   | h
a1         | Element A1       | 40  | 120 | 320 | 70
a2         | Element A2       | 40  | 230 | 320 | 70
a3         | Element A3       | 40  | 340 | 320 | 70
a4         | Element A4       | 40  | 450 | 320 | 70
b1         | Element B1       | 540 | 120 | 320 | 70
b2         | Element B2       | 540 | 230 | 320 | 70
b3         | Element B3       | 540 | 340 | 320 | 70
b4         | Element B4       | 540 | 450 | 320 | 70
```

Mapping edges: a1 → b1, a2 → b2, a3 → b3, a4 → b4 — all dashed gray,
`endArrow=none`, `entryX=0;entryY=0.5;exitX=1;exitY=0.5`. Direct
horizontal lines because Y positions are matched. No waypoints.

Separator: a vertical edge at x=450 from y=90 to y=540, `endArrow=none`,
`dashed=1;dashPattern=12 6;strokeColor=#AAAAAA;strokeWidth=1`.

**To adapt:** change element count (add/remove pairs with corresponding
Y shifts), rename labels, optionally use different fill colors for
column A vs column B.



---

## §9 Grid / table layout

**When to use:** Feature comparison matrices, parameter tables,
ablation-configuration matrices — anything that's essentially a labeled
grid with cells.

**Canvas:** 800×550. Row×column grid with headers.

**Layout conventions:**
- Top row = column headers (dark fill, white text, bold).
- Leftmost column = row headers (lighter header fill).
- Body cells = uniform fill, light border.
- Equal cell sizes: `cell_w = (pageWidth - rowHeader_w) / n_cols`,
  `cell_h = (pageHeight - colHeader_h) / n_rows`.
- No edges between cells — adjacent rectangles with thin borders imply
  the grid structure.

**Node table** (3×4 example with 3 columns + row header, 4 data rows):

```
id      | label         | x   | y   | w   | h   | style
h_r1    |               | 30  | 60  | 110 | 44  | (top-left corner, empty or "Metric")
h_c1    | Method A      | 140 | 60  | 200 | 44  | (column header)
h_c2    | Method B      | 340 | 60  | 200 | 44  | (column header)
h_c3    | Ours          | 540 | 60  | 200 | 44  | (column header)
r1_l    | Accuracy (%)  | 30  | 104 | 110 | 40  | (row header)
c11-c13 | 78.2/80.4/83.7| 140 | 104 | 200 | 40  | (body cells)
r2_l    | F1 Score      | 30  | 144 | 110 | 40  | (row header)
c21-c23 | 75.1/78.3/81.9| 140 | 144 | 200 | 40  |
r3_l    | Latency (ms)  | 30  | 184 | 110 | 40  | (row header)
c31-c33 | 12/15/10      | 140 | 184 | 200 | 40  |
r4_l    | Params (M)    | 30  | 224 | 110 | 40  | (row header)
c41-c43 | 85/120/78     | 140 | 224 | 200 | 40  |
```

Body cell style: `rounded=0;fillColor=#FFFFFF;strokeColor=#DDDDDD;
strokeWidth=0.5;html=1;align=center;verticalAlign=middle;
fontFamily=Times New Roman;fontSize=11;fontColor=#333333`.

Header style: `rounded=0;fillColor=#37474F;strokeColor=#333333;
strokeWidth=0.5;html=1;fontFamily=Times New Roman;fontSize=11;
fontStyle=1;fontColor=#FFFFFF;align=center;verticalAlign=middle`.

Row header style: `rounded=0;fillColor=#ECEFF1;strokeColor=#DDDDDD;
strokeWidth=0.5;html=1;fontFamily=Times New Roman;fontSize=11;
fontStyle=1;fontColor=#333333;align=left;verticalAlign=middle`.

"Houdini" cell (ours, best value): `fillColor=#E8F5E9;fontStyle=3` to
highlight the winning entry.

**To adapt:** change n_rows and n_cols, recalculate `cell_w` and `cell_h`,
replace labels and values. The header row and body cell styles stay
constant.



---

## §10 Flowchart

**When to use:** Decision trees, algorithm logic, process flows, approval
workflows — any step-by-step branching logic.

**Canvas:** 650×800 portrait. TB flow, decisions branch LR then rejoin.

**Shape vocabulary (each a distinct semantic role):**

| Element | Style keywords | Example |
|---|---|---|
| Start / End | `ellipse;fillColor=#D5E8D4;strokeColor=#82B366` | Green oval |
| Process | `rounded=0;fillColor=#DAE8FC;strokeColor=#6C8EBF` | Blue rect |
| Decision | `rhombus;fillColor=#FFF2CC;strokeColor=#D6B656` | Yellow diamond |
| I/O | `shape=parallelogram;perimeter=parallelogramPerimeter;fillColor=#FFE6CC;strokeColor=#D79B00` | Orange |
| Subprocess | `rounded=1;fillColor=#E1D5E7;strokeColor=#9673A6` | Purple |

**All nodes:** `whiteSpace=wrap;html=1;fontFamily=Times New Roman;fontSize=12;fontStyle=1;fontColor=#333333;align=center;verticalAlign=middle`

**Layout conventions:**
- Start node at top-center, end node at bottom-center.
- Process and I/O nodes form the vertical spine (center aligned).
- Decision nodes branch left/right, then rejoin below.
- **Always label decision branches** `"Yes"` / `"No"` (or specific
  conditions) on the outgoing edges.
- Vertical gap 150px, horizontal gap 200px between decision branches.
- Use orthogonal routing for all edges — `exitX=0.5;exitY=1` on process
  nodes, `exitX=0;exitY=0.5` and `exitX=1;exitY=0.5` on decision nodes.

**Edge style:**
```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=1.5
```

**Example node table** (3-step process with one decision):

```
id     | label             | x   | y   | w   | h   | style
start  | Start             | 225 | 30  | 200 | 60  | ellipse green
p1     | Read Input        | 225 | 200 | 200 | 60  | process blue
dec    | Valid?            | 250 | 360 | 150 | 80  | decision yellow
p2     | Process Data      | 100 | 510 | 200 | 60  | process blue (left branch)
p3     | Fix & Retry       | 350 | 510 | 200 | 60  | process blue (right branch)
out    | Output Result     | 225 | 680 | 200 | 60  | process blue
end    | End               | 275 | 810 | 100 | 50  | ellipse green
```

**Edges:** start→p1→dec. dec→p2 ("Yes", exitX=0;exitY=0.5),
dec→p3 ("No", exitX=1;exitY=0.5). p2→out (exitX=1;exitY=0.5, bends
back center). p3→out (exitX=0;exitY=0.5, bends back center). out→end.



---

## §11 Entity-Relationship Diagram (ERD)

**When to use:** Database schemas, data models, table relationships,
SQL schema documentation.

**Canvas:** 800×600. TB layout. Tables stacked vertically with FK
relationship lines between them.

**Shape vocabulary:**

| Element | Style keywords |
|---|---|
| Table container | `shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;strokeColor=#6C8EBF;fillColor=#DAE8FC` |
| Table row (column) | `shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12` — parent = table container ID |
| PK column | `fontStyle=1` (bold) on the row. Prefix label with `PK` or a key icon. |

**Layout conventions:**
- 3–7 tables, vertically stacked or arranged in 2 columns.
- Table width ~220px, row height ~26px.
- Gap between tables: 300px horizontal, 150px vertical.
- Entity relationships drawn as edges between table containers.
- FK → PK: `endArrow=ERmandOne;startArrow=ERmandOne;` with
  `exitX=0;exitY=0.5;entryX=1;entryY=0.5` or the reverse.
- For cardinality annotations, add a small label on the edge:
  `value="1"` at one end, `value="*"` at the other.

**Edge style (ER):**
```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=ERmandOne;startArrow=ERmandOne;strokeColor=#333333;strokeWidth=1.5
```



---

## §12 UML Class Diagram

**When to use:** Object-oriented design papers, architecture
modeling, inheritance/interface hierarchies.

**Canvas:** 800×700. TB layout. Classes as swimlane boxes with 3
compartments (name / attributes / methods).

**Shape vocabulary:**

| Element | Style keywords |
|---|---|
| Class box | `swimlane;startSize=26;fontStyle=1;align=center;html=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;fontFamily=Times New Roman` |
| Separator line | `line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=10;rotatable=0;labelPosition=left;points=[];portConstraint=eastwest` — placed between sections |
| Inheritance (→) | `endArrow=block;endFill=0` — hollow triangle |
| Composition (◆─) | `endArrow=diamondThin;endFill=1` — filled diamond |
| Aggregation (◇─) | `endArrow=diamondThin;endFill=0` — hollow diamond |
| Realization (dashed →) | `endArrow=block;endFill=0;dashed=1` — dashed hollow triangle |

**Layout conventions:**
- 4–8 classes vertically stacked or arranged in a column.
- Class width ~250px, height auto-fits content (~120-200px for 3-4
  attributes + 3-4 methods).
- Gap between classes: 200px TB, 280px LR.
- Superclasses above subclasses (inheritance arrows point UP).
- Composition/aggregation edges connect the containing class to the
  contained class with the diamond at the container end.

**Edge style base:**
```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1.5
```



---

## §13 Sequence Diagram

**When to use:** Protocol handshakes, API call chains, message-passing
between actors/objects — any interaction where time flows top-to-bottom
and participants are shown as vertical lifelines.

**Canvas:** 900×700. LR layout (actors placed horizontally).

**Shape vocabulary:**

| Element | Style keywords |
|---|---|
| Actor/Object header | `shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=1;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;fillColor=#DAE8FC;strokeColor=#6C8EBF;size=40;fontFamily=Times New Roman;fontStyle=1;fontSize=12` |
| Activation box | `rounded=0;fillColor=#F5F5F5;strokeColor=#999999;strokeWidth=0.5` — narrow (w=16) rectangles placed on the lifeline |
| Sync message (→) | `endArrow=block;endFill=1` — solid filled arrow |
| Async message (→>) | `endArrow=open;dashed=1` — dashed open arrow |
| Return/Reply (<--) | `endArrow=open;dashed=1;strokeColor=#999999` — grey dashed |
| Self-call | `endArrow=block;curved=1` — loops back to same lifeline |

**Layout conventions:**
- 3-6 lifelines, evenly spaced at x=80, x=280, x=480, x=680, ...
- Lifelines start at y=80 with the actor header box.
- Vertical dashed lines extend from the header down to the last message
  (these are auto-rendered by the `umlLifeline` shape).
- **Time flows top-to-bottom** — the first message is at y=120, the next
  at y=180, etc., incrementing by ~60px per message.
- Activation boxes (w=16) are placed on the lifeline starting at the
  message entry y, ending at the reply y.
- Message labels sit above the arrow line.

**Edge style (sync message):**
```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;strokeColor=#333333;strokeWidth=1.5
```

**Edge style (return):**
```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=open;dashed=1;strokeColor=#999999;strokeWidth=1.5
```

**Minimal X positions for 4 participants:**
```
Participant  | x    | w   | h
Client       | 40   | 60  | 40 (header), then lifeline auto-extends
API Gateway  | 240  | 60  | 40
Service      | 440  | 60  | 40
DB           | 640  | 60  | 40
```



---

## §14 State Machine Diagram

**When to use:** State transition specifications, protocol state
machines, embedded system modes, formal-method visualizations.

**Canvas:** 800×650. Variable layout — states can be arranged
horizontally (LR) or in a circle depending on transition count.

**Shape vocabulary:**

| Element | Style keywords |
|---|---|
| State | `rounded=1;arcSize=12;fillColor=#DAE8FC;strokeColor=#6C8EBF;strokeWidth=1.5;whiteSpace=wrap;html=1;fontFamily=Times New Roman;fontStyle=1;fontSize=13;fontColor=#333333;align=center;verticalAlign=middle` — rounded rect, blue |
| Initial state (●) | `ellipse;fillColor=#333333;strokeColor=#333333` — filled black circle, w=20 h=20 |
| Final state (◎) | `ellipse;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=2.5` — double circle: outer ellipse w=30 h=30 filled white, inner filled black ellipse w=16 h=16 |
| Transition | Edge with `edgeStyle=orthogonalEdgeStyle;rounded=1;endArrow=classic` |
| Self-transition | `curved=1;exitX=0;exitY=0.5;entryX=0;entryY=0.8` — loops from state left side back to itself |
| Choice/Junction (●) | `rhombus;fillColor=#FFF2CC;strokeColor=#D6B656` — yellow diamond |

**Edge label:** `value="event / action"` on the transition edge
(e.g., "e_acc_on / init()").

**Layout conventions:**
- 4–8 states arranged in a natural reading order (LR or TB).
- Initial state (small black circle) connects to the first state via
  an arrow with no label.
- Final state (bullseye) is reached from terminal transitions.
- Distribute states with 250-300px spacing for readability.
- Self-transitions use `curved=1` with exit/entry both on the same
  side of the state (left side, y=0.5 and y=0.8).

**Edge style (transition):**
```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=1.5;fontFamily=Times New Roman;fontSize=10;fontColor=#333333
```

**Edge style (self-loop):**
```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=1.5;curved=1;exitX=0;exitY=0.5;entryX=0;entryY=0.2
```



---

## §15 Data Flow Diagram (DFD)

**When to use:** Software engineering papers, system analysis — showing
how data moves through processes and stores. Distinct from a flowchart:
DFD shows **data movement**, not control flow.

**Canvas:** 800×600. Variable layout — processes form the center, external
entities on the edges, data stores at the bottom.

**Shape vocabulary:**

| Element | Style keywords | Visual |
|---|---|---|
| Process | `ellipse;fillColor=#DAE8FC;strokeColor=#6C8EBF;strokeWidth=1.5` | Blue circle/ellipse |
| External Entity | `rounded=1;arcSize=8;fillColor=#F8CECC;strokeColor=#B85450;strokeWidth=1.5` | Red rounded rect (source/sink of data) |
| Data Store | `shape=partialRectangle;whiteSpace=wrap;html=1;fillColor=#FFF9C4;strokeColor=#F9A825;bottom=0;right=0;top=0;left=0;strokeWidth=1.5` or `rounded=0;fillColor=#FFF9C4;strokeColor=#F9A825;strokeWidth=1.5` + two parallel horizontal lines | Yellow open-ended box |
| Data Flow | Edge with `endArrow=classic` | Solid arrow with data label |

**All element styles** include: `fontFamily=Times New Roman;fontSize=12;fontColor=#333333;align=center;verticalAlign=middle`

**Layout conventions:**
- Processes numbered (P1, P2, P3) with a brief verb-noun label.
- External entities placed around the edges (top-left, top-right,
  bottom corners).
- Data stores at the bottom center.
- Data flow edges are labeled with the data being moved
  (e.g. `value="Customer Data"`, `value="Validation Result"`).
- Processes form the central hub — data flows IN from entities,
  is transformed by processes, and flows OUT to stores or entities.
- Spacing: 200-300px between processes.

**Edge style (data flow):**
```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=1.5;fontFamily=Times New Roman;fontSize=10;fontColor=#333333
```

**4-process example layout:**

```
id     | label               | x   | y   | w   | h   | shape
ent1   | Customer            | 40  | 80  | 120 | 60  | entity (red rounded)
ent2   | Warehouse           | 640 | 80  | 120 | 60  | entity
p1     | 1. Validate Order   | 280 | 100 | 150 | 70  | process (blue ellipse)
p2     | 2. Check Inventory  | 280 | 240 | 150 | 70  | process
p3     | 3. Ship Order       | 280 | 380 | 150 | 70  | process
store1 | Orders DB           | 160 | 480 | 120 | 50  | data store (yellow)
store2 | Inventory DB        | 520 | 480 | 120 | 50  | data store
```

Edges: ent1→p1 ("Order"), p1→p2 ("Validated Order"), p2→p3
("Available Qty"), p3→ent2 ("Shipping Label"). p1↔store1
("Order Record"), p2↔store2 ("Stock Level").
