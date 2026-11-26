# Trimorious D05–D10 dataset roadmap

D05–D10 follow the production-readiness backlog. These are proposed repositories and dataset specifications, not existing data assets. Do not create public datasets until the schema, source register, rights review, quality pipeline and release card are ready.

| ID | Dataset | Primary role | Initial target |
|---|---|---|---:|
| D05 | `trimorious-mathematical-verification` | Independently verified math and symbolic solutions | 50,000 examples |
| D06 | `trimorious-scientific-preferences` | Scientific preference pairs for DPO or related methods | 30,000–50,000 pairs |
| D07 | `trimorious-scientific-evaluation` | Independent scientific benchmark | 5,000–10,000 curated cases |
| D08 | `trimorious-multilingual-science` | Multilingual scientific capability | 30,000–50,000 examples |
| D09 | `trimorious-safety-and-reliability` | Safety, robustness, uncertainty and refusal | 15,000–30,000 examples |
| D10 | `trimorious-scientific-environments` | Executable research and tool-use environments | 100–500 environments |

Targets are planning estimates, not quality guarantees. D10 environments are not comparable to record or pair counts.

## D05 — Mathematical Verification

Include SymPy-generated solutions, numerical checks, formal proof examples where feasible, counterexamples, dimensional analysis and incorrect derivations with error labels.

Each record should preserve the problem, assumptions, domain, variables and units, solution steps, normalized final answer, verifier expression, verifier/version, execution status, tolerance, source and license. Include deliberately under-specified cases and multiple valid paths. Correctness must come from an independent checker, not the same generator that authored the answer.

## D06 — Scientific Preferences

Include pairs for correct versus incorrect explanations, evidence-supported versus unsupported claims, strong versus weak hypotheses, calibrated versus unjustified certainty, and valid versus fabricated citations.

Each pair must include prompt, chosen and rejected responses, rubric dimensions, rationale, provenance, annotation protocol, annotator/adjudication metadata and confidence. Do not treat model-generated judge preferences as ground truth without human calibration. Measure agreement and adjudicate disagreements before training.

## D07 — Scientific Evaluation

Cover mathematics, scientific reasoning, causal reasoning, evidence retrieval, hypothesis testing and long-context comprehension. Maintain train/dev/public-test/hidden-test policies as appropriate. A hidden test set must be access-controlled, versioned and excluded from SFT, DPO, reward-model training, RL and prompt tuning. Freeze the benchmark before comparing baseline and candidate models.

## D08 — Multilingual Science

Initial languages: English, Bahasa Malaysia, Indonesian, Chinese, Arabic, Spanish, French and Japanese. Include terminology alignment, translations, bilingual explanations and technically equivalent questions. Record language/script, locale, source language, translation method, translator/reviewer role and review status. Use native-language technical review; machine translation alone is not a quality gate.

## D09 — Safety and Reliability

Cover prompt injection, malicious tool instructions, citation manipulation, scientific misinformation, unsupported medical claims, hazardous scientific requests, privacy/confidentiality, uncertainty, abstention and safe handling of user-provided documents. Use a risk taxonomy with benign, ambiguous and disallowed request categories, expected model behavior and adjudicated labels. Include adversarial variations and regression tests.

## D10 — Scientific Environments

Provide executable environments for mathematical problem-solving, physics simulation, chemistry calculations, scientific data analysis, optimization, research search/retrieval, experimental design and multi-step investigation.

Each environment must define observation/state, action space, transition function, allowed tools, initialization, termination, resource limits, reset/replay behavior, expected artifacts, reward function and reward-verification tests. Run in a sandbox with explicit network, filesystem, CPU, memory and time policies. A textual description of an action is not an executed trace.

## Relationship to upgraded D01–D04

- D01 supplies scientific instruction-following and methodology examples.
- D02 supplies structured symbolic solution trajectories; D05 provides independent verification signals and error taxonomy.
- D03 supplies traceable research evidence; D01/D06 can use permitted evidence-derived prompts and judgments without copying restricted full-text content.
- D04 supplies initial agentic examples; D10 supplies executable state/action/reward environments for replay and policy evaluation.
- D07 measures generalization across all domains and stays isolated from training.
- D08 and D09 provide additional capability and reliability coverage, but require separate language and risk quality processes.

## Recommended build order

1. Freeze and benchmark D01–D04.
2. Develop D05 first to create objective mathematical verification.
3. Establish D07 early as an evaluation-only benchmark, with a controlled hidden test partition.
4. Build D03 evidence/provenance structure and D01 scientific instruction improvements.
5. Develop D10 environments and expand D04 with replayable trajectories.
6. Develop D06 only after rubric, annotator training and adjudication are established.
7. Build D08 and D09 with native-language and safety-specialist review.

Every dataset should be a separate Hub repository with immutable version tags, a dataset card, schema, quality report, provenance/license statement and reproducible generation/validation scripts.
