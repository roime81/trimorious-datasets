# Dataset expansion roadmap — D05 to D10

D05–D10 are proposed datasets, not existing or completed data assets. Each should have a source register, versioned schema, documented collection method, license review, train/validation/test policy, quality report and dataset card before publication.

| ID | Proposed dataset | Capability | Primary verification |
|---|---|---|---|
| D05 | Verifiable Mathematics and Symbolic Reasoning | Derivations, equation solving, proof steps and executable symbolic work | SymPy or another appropriate solver; proof checks; unit tests |
| D06 | Evidence-Grounded Scientific Synthesis | Multi-source synthesis with claim-level citations and uncertainty | DOI/URL resolution, passage-to-claim support, citation entailment review |
| D07 | Experimental Design and Causal Reasoning | Hypotheses, variables, controls, confounding, study design and limitations | Structured rubric and expert review; causal assumptions made explicit |
| D08 | Reproducible Scientific Tool Use | Tool selection, tool arguments, execution traces, code, outputs and result interpretation | Sandboxed replay, deterministic tests, artifact checksums |
| D09 | Scientific Preference and Critique Pairs | Chosen/rejected answers and critique for preference optimization | Expert preference labels, rubric consistency, adjudication and annotator agreement |
| D10 | Held-Out Scientific Reasoning Benchmark | Independent evaluation across mathematics, evidence, methods and tools | Hidden answers where appropriate, verifiers, stable benchmark versioning |

## D05 — Verifiable Mathematics and Symbolic Reasoning

Recommended record fields:

- problem statement and subject taxonomy;
- assumptions, units and variable definitions;
- candidate derivation in structured steps;
- final answer in normalized form;
- executable verification expression or test;
- verifier name/version, execution status and tolerances;
- source/provenance and license.

Do not optimize only for long chains of text. Prefer concise derivations with explicit assumptions and machine-checkable endpoints. Include both solvable and intentionally under-specified cases.

## D06 — Evidence-Grounded Scientific Synthesis

Represent answers as claims linked to exact supporting passages or metadata, not a bibliography appended after free-form prose. Keep DOI, title, authors, year, source URL, retrieval date, passage identifier, claim identifier and support relationship. Store only text that can lawfully be redistributed; otherwise keep bibliographic metadata and permitted excerpts.

## D07 — Experimental Design and Causal Reasoning

Capture the research question, target estimand, hypothesis, population, variables, intervention/exposure, comparator, outcome, confounders, measurement plan, analysis design, assumptions, limitations and failure modes. Include cases where the correct answer is that the evidence is insufficient to infer causality.

## D08 — Reproducible Scientific Tool Use

Use explicit structured tool-call and tool-result fields. Every task should specify allowed tools, inputs, environment, expected artifacts, success criteria, timeout/resource limits and deterministic replay instructions. A prose description of a tool action is not equivalent to a successfully executed trace.

## D09 — Preference and Critique Data

Each pair should include the prompt, chosen response, rejected response, rubric dimensions, rationale, annotator or adjudication metadata, and provenance. Remove pairs that differ only stylistically or that reward unsupported confidence. DPO/ORPO should only be considered after preference quality and evaluator reliability are established.

## D10 — Held-Out Benchmark

D10 is evaluation-first and must never be mixed into SFT, DPO, reward-model or RL training. Maintain a private or controlled test split where feasible, publish benchmark methodology, and report aggregate and per-domain metrics. Add executable checks for mathematics and code/tool tasks, and evidence-support scoring for literature tasks.

## Suggested release sequence

1. Stabilize D01–D04 and freeze a baseline.
2. Build D05 and D06 first; they add objective correctness and evidence provenance.
3. Build D07 and D08 next; they expand scientific method and reproducible tool behavior.
4. Collect D09 only with reliable human or expert preference labels.
5. Establish D10 before model optimization, then run it unchanged across the baseline and every candidate release.

D05–D10 should be separate Hub datasets with immutable version tags and linked dataset cards. This avoids mixing incompatible objectives and makes ablations possible.
