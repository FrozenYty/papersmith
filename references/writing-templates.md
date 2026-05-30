# Academic Writing Templates

Canonical section structures for CS/ML papers. Read this file when the user
asks you to draft or restructure a paper section. Each template gives a
structure skeleton and a concrete example. Adapt the skeleton to the user's
content; keep the paragraph-level logic intact.

Templates are organized by section. When the user's request matches a named
section ("introduction", "related work", etc.), use the matching template.
If unmatched, fall back to the general principles in §7.

## §1 Introduction (CARS Model)

The three-move CARS model (Swales 1990, adapted for CS):

**Move 1 — Establish territory (1 paragraph, ~3-4 sentences)**
- Sentence 1: State the broad domain and its importance.
- Sentence 2-3: Narrow to the sub-problem. Define key terms.
- Sentence 4: Bridge to Move 2 — signal that a gap exists.

**Move 2 — Establish niche (1 paragraph, ~3-5 sentences)**
- Sentence 1: State the gap explicitly. What prior work cannot do.
- Sentence 2-3: Evidence for the gap (quantitative if possible).
- Sentence 4-5: Why the gap matters. What is blocked by it.

**Move 3 — Occupy the niche (1-2 paragraphs, ~5-8 sentences)**
- Sentence 1: "In this paper, we propose [named method]."
- Sentence 2-4: The key technical idea (1-3 sentences, accessible).
- Sentence 5-6: Experimental setup and headline result.
- Sentence 7-8: Contributions (3-4 items, each one sentence).

**Example (NLP/ML paper):**

> Large language models have achieved remarkable performance across diverse
> NLP benchmarks. However, their inference cost scales with model size,
> making deployment in resource-constrained environments impractical.
> Existing compression methods (quantization, pruning, distillation)
> reduce model size but often degrade performance on long-tail or
> specialized tasks — the very tasks where small models are most needed.
>
> We identify a key limitation: prior compression techniques treat all
> tokens uniformly, discarding information that is critical for rare
> linguistic patterns. On the Bamboo rare-language benchmark, compressed
> Llama-7B models lose 12.3% accuracy on low-frequency tokens versus
> 1.7% on high-frequency ones, confirming that uniform compression is
> the bottleneck.
>
> We propose Token-Adaptive Compression (TAC), a method that dynamically
> allocates representation capacity based on token importance. TAC learns
> a lightweight importance predictor that runs in parallel with the main
> forward pass, adjusting the compression ratio per token at inference
> time with negligible overhead. On Llama-7B and Llama-13B, TAC
> preserves 98.2% of the original accuracy on rare tokens while reducing
> overall inference cost by 1.8×. Our contributions are: (1) the
> token-adaptive compression framework; (2) an importance predictor that
> adds less than 2% latency overhead; and (3) empirical demonstration
> that adaptive strategies close the rare-token gap left by uniform
> methods.

---

## §2 Related Work (Taxonomy Structure)

**Structure: 3-4 thematic groups, not chronological.**

Group the literature by *problem approach*, not by paper. Each group is
one paragraph:

1. **Opening sentence**: Name the approach and its representative works.
   "Prior work on X has primarily followed [approach A]."
2. **Body (2-3 sentences)**: What this approach achieves and where it
   falls short. Cite 2-4 key papers per group.
3. **Closing sentence**: Transition. "While [approach A] addresses Y,
   it does not handle Z."

**The final group is always your position**: "Our work differs from the
above in that..." or "We build on [approach B] and extend it with..."

**Anti-patterns to avoid:**
- Paper-by-paper listing ("Smith et al. proposed X. Jones et al.
  proposed Y. Lee et al. proposed Z.")
- Starting with "There has been a lot of work on..."
- Omitting the "why prior work is insufficient" for each group

**Example (first group):**

> Prior work on efficient LLM inference has largely followed three
> directions. Quantization methods [Dettmers et al. 2022, Frantar et
> al. 2023, Xiao et al. 2023] reduce numerical precision to 4-bit or
> below, achieving 2-4× compression with minimal accuracy loss on
> standard benchmarks. However, these methods apply a static precision
> budget to all tokens, ignoring the fact that some tokens (rare words,
> named entities) require higher precision for accurate prediction.
> Pruning approaches [Sun et al. 2023, Ma et al. 2023] remove entire
> attention heads or FFN neurons but risk degrading performance on
> specialized domains. Our work complements both directions: we keep
> static compression as a base and add token-level adaptation on top.

---

## §3 Methodology (Algorithm Description)

**Structure: Top-down. Architecture → Components → Details.**

**Paragraph 1 — Overview (3-4 sentences)**
- Sentence 1: "We propose [Method Name], a [high-level description]."
- Sentence 2-3: The core idea in one sentence, then the main components.
- Sentence 4: "Figure 1 illustrates the overall architecture."

**Paragraph 2 — Component 1 (3-5 sentences)**
- What it does, what its inputs/outputs are, the key design choice.
- When relevant: a simplified equation or pseudocode.

**Paragraph 3 — Component 2 (same structure)**

**Paragraph 4 — Training / optimization details (3-4 sentences)**
- Loss function, optimizer, key hyperparameters.
- "We train on [dataset] using [optimizer] with learning rate [lr] for
  [N] epochs on [hardware]."

**Conventions:**
- Name the method once (Paragraph 1, Sentence 1). Use the name thereafter.
- Define every symbol before it appears in an equation.
- Write "We" not "The model" or passive voice.
- Equations are prose-connected: "The loss is L = A + B, where A is..."

---

## §4 Experiments (Three-Part Structure)

### §4.1 Setup (1 paragraph, no results)

- Datasets: name, size, metrics. "We evaluate on [D1] (N samples,
  metric M1), [D2] (N2 samples, metric M2)."
- Baselines: name each one, state why it's included. "We compare against
  [B1] as the SOTA in [task], [B2] as a representative of [approach]."
- Implementation: framework, hardware, hyperparameters, seeds. "All
  experiments use 5 random seeds; we report mean ± 1 SD."

### §4.2 Main Results (2-4 paragraphs)

**Paragraph 1 — Headline table.** "Table 1 shows..." followed by the
key takeaway in prose, not a re-listing of numbers. "Our method
outperforms the strongest baseline by 3.4 points on MMLU (p < 0.01,
paired t-test)."

**Paragraph 2-3 — Drill-down.** One finding per paragraph. Connect
results to claims. "The gains are largest on [subset], consistent with
our hypothesis that [mechanism] is the key driver."

### §4.3 Ablation / Analysis (2-3 paragraphs)

- Remove one component at a time. Show it matters.
- Sensitivity analysis (hyperparameters, seeds).
- Qualitative examples if applicable (1-2 representative cases).

**Conventions:**
- Every table/figure reference must have a prose takeaway.
- Never write "Table 2 shows the results." Write "Table 2 shows that
  removing [component] reduces accuracy by X%, confirming its role."
- Report statistical significance for all headline claims.
- State the hardware and runtime for reproducibility.

---

## §5 Conclusion (Three-Part)

**Paragraph 1 — Summary (2-3 sentences)**
- Restate the problem, method name, and headline result.
- No new information. No citations.

**Paragraph 2 — Limitations (2-4 sentences)**
- Be honest. Scope limitations, methodological caveats, dataset bias.
- "Our method requires labeled data for the importance predictor,
  limiting applicability to fully unsupervised settings."

**Paragraph 3 — Future work (1-2 sentences)**
- One or two concrete directions. Not "more research is needed."
- "We plan to extend TAC to vision-language models and investigate
  online importance prediction for streaming inputs."

**Anti-patterns:**
- "Future work will explore..." (vague) → "We plan to extend X to Y."
- Ending with a grand societal claim unrelated to the method.
- Introducing new results or claims not supported by the paper.

---

## §6 Abstract (Five-Part)

See `prompts/polish-abstract.md` for the full template. The five parts
in order: (1) Background — 1-2 sentences. (2) Gap — 1-2 sentences.
(3) Method — 2-4 sentences, name the method. (4) Results — 2-3
sentences, concrete numbers. (5) Impact — 1 sentence.

---

## §7 General Principles

When no template matches the user's request, follow these:

1. **Structure before prose.** Name the 2-4 logical blocks before
   writing any sentence. If you can't name them, the section is
   under-organized.
2. **One claim per paragraph.** A paragraph that makes two unrelated
   points should be two paragraphs.
3. **Numbers over adjectives.** "3.4 points improvement" beats
   "significant improvement."
4. **Breadcrumb the reader.** The first sentence of each paragraph
   should connect to the previous paragraph's conclusion.
5. **Active voice, present tense.** "We propose X." "Table 1 shows Y."
   Past tense only for completed experimental actions.
6. **Citations are evidence, not decoration.** Every citation should
   support a claim the sentence makes. If a sentence with three
   citations could mean any of them, it's under-specified.

## Self-Check

Before delivering a drafted section, verify:
1. Does each paragraph have a single clear topic sentence?
2. Are all quantitative claims backed by specific numbers?
3. Are all citations justified (each one supports a specific claim)?
4. Does the section match the template structure (correct number of
   paragraphs, correct flow)?
5. Are there any anti-patterns from `references/writing-anti-patterns.md`?
