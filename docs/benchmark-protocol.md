# Trimorious benchmark protocol

## Purpose

Measure whether candidate model releases improve scientific reliability relative to both the untouched base model and the original Trimorious adapter. This protocol is a design specification; no benchmark results are claimed yet.

## Required model variants

1. Exact base checkpoint at a pinned revision, without Trimorious adapter.
2. Existing Trimorious adapter attached to the same base revision.
3. Each candidate adapter or merged checkpoint under evaluation.

Use the same tokenizer, prompt template, decoding settings, and hardware where technically possible. Record unavoidable differences.

## Evaluation domains

| Domain | Core measures | Preferred verification |
|---|---|---|
| Scientific instructions | rubric score, task completion, factual support | blind expert rubric and reference checks |
| Mathematics | exact answer rate, symbolic equivalence, numeric tolerance | SymPy or domain-specific independent solver |
| Scientific evidence | claim support, citation precision/recall, unsupported claim rate | passage-to-claim mapping and expert audit |
| Hypothesis and causal reasoning | assumptions, confounder coverage, valid inference | structured rubric and case adjudication |
| Tool use and agents | task success, valid tool choice, replay success, recovery | sandbox replay and environment outcome |
| Multilingual science | semantic accuracy, terminology consistency | native-language technical reviewers |
| Safety | policy adherence, prompt-injection resistance, unsafe action rate | adversarial tests and reviewed expected behavior |
| Context | task quality at 2K, 8K, 16K and 32K contexts | same task families with controlled length |
| Serving | latency, throughput, memory and error rate | measured on declared deployment hardware |

## Split governance

- D07 Scientific Evaluation is evaluation-only.
- Keep hidden test examples access-controlled. Do not use them for SFT, DPO, reward model, RL, prompt tuning, hyperparameter selection or iterative development.
- Use a separate development set for iteration.
- Freeze benchmark version and scoring implementation before comparing candidates.
- Record data revision and scoring-code commit for every run.

## Scoring and reporting

- Report aggregate and per-domain results.
- Report sample size and uncertainty/confidence intervals where meaningful.
- Publish exact-answer/verifier pass rates separately from expert rubric scores.
- Count unsupported citations and unverifiable claims as errors, not merely style issues.
- Report failures and regressions alongside improvements.
- Keep model generation settings and evaluator instructions in version control.
- Do not compare models using different test examples or silently changed rubrics.

## Release decision

A candidate should not pass solely because its average score improves. Require predeclared minimum performance in mathematics, evidence grounding and safety, and no unacceptable regression in core scientific instruction following. Resource/latency cost must be considered alongside quality.
