# Canonical Architecture Templates

Read this file when the user requests a diagram for a common ML architecture.
Each template below gives a node table (with Y assigned bottom-up) and a
complete copy-pasteable XML skeleton. Adapt names and counts; keep the layout
math and edge directions.

All templates follow the Flow Direction rule from `drawio-reference.md`:
data flows bottom-to-top inside each stack, every forward edge satisfies
`source.y > target.y`, the input section sits BELOW the stack, the output
section sits ABOVE.

## Index

| Architecture | When to use | Section |
|---|---|---|
| Transformer encoder-decoder | Translation, summarization, encoder-decoder LLM | §1 |
| Transformer decoder-only | GPT-style autoregressive LM | §2 |
| Seq2Seq with Bahdanau attention | Classic NMT, RNN baselines | §3 |
| CNN classifier | Image classification (VGG/ResNet-style) | §4 |
| Diffusion forward/reverse | DDPM/DDIM, score-based, flow-matching | §5 |
| RAG pipeline | Retrieval-augmented LLM systems | §6 |
| Multi-stage training | Pretrain → SFT → RLHF, foundation-model recipes | §7 |
| GNN message-passing | Graph models, molecular/network papers | §8 |

If the user's request doesn't match any of these, fall back to the general
workflow in `draw-diagram.md` and apply the Flow Direction rule
manually. Don't force-fit a non-matching architecture onto a template.

---

## §1 Transformer encoder-decoder (Vaswani 2017)

**Canvas:** 920×870, portrait. Encoder on the left, decoder on the right,
output stack above the decoder, source input below the encoder, target input
below the decoder.

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

## §2 Transformer decoder-only (GPT-style)

**Canvas:** 600×800. Single stack centered. Output above, target tokens below.

**Node table** (data-flow order; y decreases up the stack):

```
SECTION  | id        | label                         | x   | y   | w   | h
output   | outp      | Output Probabilities          | 100 | 20  | 400 | 42
output   | softmax   | Softmax                       | 160 | 80  | 280 | 38
output   | linear    | Linear                        | 160 | 140 | 280 | 38
DECODER  | dec_an2   | Add & Norm                    | 100 | 200 | 400 | 30
DECODER  | dec_ff    | Feed Forward                  | 100 | 250 | 400 | 50
DECODER  | dec_an1   | Add & Norm                    | 100 | 320 | 400 | 30
DECODER  | dec_mmha  | Masked Multi-Head Self-Attn   | 100 | 370 | 400 | 50
input    | tgt_pos   | Positional Encoding           | 100 | 460 | 400 | 32
input    | tgt_emb   | Token Embedding               | 100 | 512 | 400 | 38
input    | tgt_tk    | Tokens (shifted right)        | 100 | 570 | 400 | 42
```

Edges: chained `tgt_tk → tgt_emb → tgt_pos → dec_mmha → dec_an1 → dec_ff →
dec_an2 → linear → softmax → outp`. All vertical. Add 2 left-side residuals
across each Add & Norm. No cross-attention block — this is decoder-only.

For repeated blocks (×N), draw one block and add a `× N` annotation in the
section label, just like §1. Don't draw all N copies.

---

## §3 Seq2Seq with Bahdanau attention

**Canvas:** 920×740. Encoder (Bi-LSTM) on the left, decoder (LSTM + attention)
on the right. The encoder hidden states feed the decoder attention via a
horizontal arrow. Encoder final state initializes the decoder.

**Node table** (data-flow order; y decreases up each stack):

```
SECTION   | id          | label                         | x   | y   | w   | h
output    | dec_out     | Decoder Output (y₁ … y_m)     | 540 | 30  | 340 | 48
output    | softmax     | Softmax                       | 600 | 100 | 220 | 38
DECODER   | dec_lstm2   | LSTM Layer 2                  | 540 | 170 | 340 | 50
DECODER   | dec_lstm1   | LSTM Layer 1                  | 540 | 240 | 340 | 50
DECODER   | dec_attn    | Attention (Bahdanau)          | 540 | 310 | 340 | 50  ← center y=335
DECODER   | dec_state   | Decoder Hidden s_{t-1}        | 540 | 380 | 340 | 40
input_t   | tgt_emb     | Output Embedding              | 540 | 460 | 340 | 38
input_t   | tgt_tk      | Target Tokens (shifted right) | 540 | 520 | 340 | 42
ENCODER   | enc_hn      | Hidden States h_1 … h_n       | 60  | 320 | 280 | 50  ← center y=345 ≈ dec_attn 335
ENCODER   | enc_h2      | Bi-LSTM Layer 2               | 60  | 390 | 280 | 50
ENCODER   | enc_h1      | Bi-LSTM Layer 1               | 60  | 460 | 280 | 50
input_s   | src_emb     | Input Embedding               | 60  | 540 | 280 | 38
input_s   | src_tk      | Source Tokens                 | 60  | 600 | 280 | 42
```

**Cross-attention arrow:** `enc_hn → dec_attn` with `exitX=1;exitY=0.5;
entryX=0;entryY=0.5`. Y centers (345 vs 335) are within 10px so the line
appears horizontal.

**Initial state arrow** (encoder final → decoder LSTM): dashed orange,
`enc_h2 → dec_lstm1` (or `dec_lstm2`). Goes diagonally up-right; that's OK
because it's a special initialization edge, semantically distinct from the
main flow. Use a single waypoint at the gap if needed.

**Decoder hidden state feedback** (`s_{t-1}` → attention): dashed loop on
the LEFT of the decoder, exits dec_state at the left side and re-enters
dec_attn from the left. Two waypoints in the gap.

Edges for the main vertical chains follow the same source.y > target.y
pattern as §1.

---

## §4 CNN classifier (VGG/ResNet block)

**Canvas:** 500×900, portrait. Single vertical stack. For ResNet-style,
add residual side-arrows; for VGG-style, omit them.

**Node table** (data-flow order; y decreases up the stack):

```
id         | label                         | x   | y   | w   | h
outp       | Class Probabilities           | 100 | 20  | 300 | 42
softmax    | Softmax                       | 140 | 80  | 220 | 38
fc         | FC (num_classes)              | 140 | 140 | 220 | 38
gap        | Global Avg Pool               | 140 | 200 | 220 | 38
block_n    | Conv Block × N (3×3, BN, ReLU)| 100 | 270 | 300 | 50
pool2      | Max Pool 2×2                  | 140 | 350 | 220 | 38
block_2    | Conv Block (3×3, BN, ReLU)    | 100 | 410 | 300 | 50
pool1      | Max Pool 2×2                  | 140 | 490 | 220 | 38
block_1    | Conv Block (3×3, BN, ReLU)    | 100 | 550 | 300 | 50
input_img  | Input Image (H × W × 3)       | 100 | 640 | 300 | 50
```

Edges: chained input_img → block_1 → pool1 → block_2 → pool2 → block_n →
gap → fc → softmax → outp. All vertical, source.y > target.y.

**ResNet variant:** for each `block_k`, add a dashed residual arc on the
LEFT side from block input to block output (skip the inner 3×3 conv path).
Keep waypoints close to the block (~30px to the left).

**Color mapping:** Conv blocks `#DAE8FC`/`#6C8EBF` (Convolution palette
from `drawio-reference.md`), pooling `#D5E8D4`/`#82B366`, FC `#FFE6CC`/
`#D79B00`, softmax/output `#FFF2CC`/`#D6B656`, input `#F8CECC`/`#B85450`.

---

## §5 Diffusion (forward + reverse process)

**When to use:** DDPM/DDIM/score-based/flow-matching figures showing the
two-direction Markov chain. Canonical Ho et al. 2020 Figure 2 layout.

**Canvas:** 1100×440. Two parallel chains stacked vertically — forward on
top (q, →), reverse on bottom (p_θ, ←). Nodes are square placeholders for
sample images (h=80, w=100-120).

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

---

## §6 RAG pipeline

**When to use:** Retrieval-augmented LLM system figures. Common in 2024+
LLM application papers.

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

## §7 Multi-stage training pipeline

**When to use:** Foundation-model recipe figures: Pretrain → SFT → RLHF
→ Eval, or analogous multi-stage workflows. Common in LLM/VLM/codegen
papers since 2023.

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

## §8 GNN message-passing

**When to use:** Graph neural network figures showing how a node aggregates
information from its neighbors. Common in graph papers, molecular property
prediction, recommender systems.

**Canvas:** 800×620. Two parts: a small graph showing structure (left),
and a "zoomed in" view of one node's update equation (right).

**Node table:**

```
SECTION    | id      | label                    | x   | y   | w   | h
graph      | n1      | v_1                      | 100 | 80  | 60  | 60   ← circle
graph      | n2      | v_2                      | 240 | 60  | 60  | 60
graph      | n3      | v_3                      | 240 | 200 | 60  | 60
graph      | nv      | v (target)               | 60  | 220 | 60  | 60   ← highlighted
graph      | n4      | v_4                      | 200 | 360 | 60  | 60
update     | agg     | Aggregate(·)             | 460 | 100 | 220 | 60
update     | upd     | Update: h_v^t = σ(W·m + B·h_v^{t-1}) | 460 | 200 | 280 | 80
update     | hnew    | h_v^t                    | 540 | 320 | 120 | 60
formula    | eq_lbl  | m = AGG({h_u : u ∈ N(v)})| 460 | 30  | 280 | 50
```

All graph nodes use `ellipse;fillColor=#FFFFFF;strokeColor=#333` except
the target `nv`, which is highlighted: `fillColor=#FFE6CC;strokeColor=
#D79B00;strokeWidth=2.5`.

**Edge table:**

```
GRAPH EDGES (undirected, no arrowheads):
id     | source | target | style
g_12   | n1     | n2     | endArrow=none, strokeWidth=1.5
g_13   | n1     | n3     | endArrow=none
g_23   | n2     | n3     | endArrow=none
g_v1   | nv     | n1     | endArrow=none, bold (target's edge)
g_v3   | nv     | n3     | endArrow=none, bold
g_v4   | nv     | n4     | endArrow=none, bold

MESSAGE-PASSING EDGES (directed, dashed colored):
m_1v   | n1     | agg    | →, dashed, blue, "h_1"
m_3v   | n3     | agg    | →, dashed, blue, "h_3"
m_4v   | n4     | agg    | →, dashed, blue, "h_4"

UPDATE EDGES (solid black):
u_a_u  | agg    | upd    | ↓, "m"
u_v_u  | nv     | upd    | →, "h_v^{t-1}"
u_u_h  | upd    | hnew   | ↓
```

**Layout choices:**
- The graph zone (x=30..340, y=30..440) shows topology — nodes laid out
  to suggest a 4-neighbor structure with the target on the left.
- The update zone (x=440..760, y=30..400) shows the math: aggregate first,
  then update, then the new hidden state.
- Message arrows from neighbors → aggregator are dashed colored (one
  hue), to visually separate from graph edges (which are solid undirected).
- The target node's graph edges are bold to draw the eye to the
  neighborhood being aggregated.
- The textual formula "m = AGG({h_u : u ∈ N(v)})" sits above the
  aggregator as a caption.

**Variants:**
- For GAT: replace `Aggregate(·)` with `Σ_u α_{vu} W h_u` and add an
  attention coefficient label `α_{vu}` on each message arrow.
- For GraphSAGE / GIN: change the aggregator label (mean/max/sum/MLP).
- For multi-hop: stack two layers vertically with a transition arrow
  between hidden states.
