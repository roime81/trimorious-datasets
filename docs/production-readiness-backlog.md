# Trimorious — Production-readiness upgrade backlog

This document is the programme-level specification for making Trimorious reliable for public inference, reproducible for researchers, understandable to developers, and safe to integrate. It is a work plan and does not imply that any target has already been met.

## Programme principles

- Preserve the current model and D01–D04 source revisions as immutable baselines.
- Create versioned derivatives rather than silently changing existing public data.
- Select model size and training methods from benchmark evidence, not parameter-count targets.
- Treat generated examples as candidate data until independently verified.
- Complete license and rights review before redistributing upstream text, figures, code, weights or derived material.
- Keep hidden evaluation data isolated from every training and model-selection loop.

## 1. Master gap and upgrade register

### P0 — Public-release blockers

| ID | Gap | Required upgrade | Evidence required to close |
|---|---|---|---|
| M01 | Unclear model identity | Confirm exact base model, architecture, parameter count, adapter/merged status and revisions | Model manifest, pinned base revision, adapter compatibility test |
| M02 | Insufficient evaluation | Benchmark original base model and existing Trimorious adapter | Frozen benchmark, scoring code, model outputs and comparison report |
| M03 | Unverified reasoning | Add independently verified mathematical and scientific answers | Verifier logs, expert review where needed, measured pass rates |
| M04 | Incomplete model card | Document intended use, limitations, training, hardware, data and inference | Reviewed model card and reproducibility manifest |
| M05 | Reproducibility | Publish training configuration, seeds, dependency versions and dataset revisions | Complete run manifest and replay instructions |
| M06 | Safety | Evaluate refusal, prompt injection, malicious tool instructions, harmful outputs and misuse | Safety taxonomy, adversarial results and regression suite |
| M07 | Licensing | Audit base model, each dataset, source papers and redistribution rights | Rights register, attribution, license compatibility decision |
| M08 | Public inference readiness | Validate tokenizer, chat template, generation configuration and serving compatibility | Smoke tests, Transformers/vLLM compatibility and API test report |

A repository being downloadable does not automatically mean its contents are commercially redistributable. Review the base model, adapter, datasets and embedded third-party sources separately.

### P1 — Capability and data quality upgrades

| Workstream | Scope | Key outputs |
|---|---|---|
| Dataset remediation | D01–D04 | Versioned v2 schemas, cleaned derivatives, provenance, quality reports, split governance |
| Dataset expansion | D05–D10 | Six separate data assets with schemas, cards, source registers and verification pipelines |
| Training engineering | SFT, preference optimization, selective RL | Reproducible training configs, experiment tracking and checkpoints |
| Knowledge grounding | D03 evidence repository | Source documents, chunks, claims and evidence relations stored separately |
| Agentic execution | D04 plus D10 | Replayable traces, tool contracts, sandbox and verifiable rewards |
| Evaluation | D07 plus custom verifiers | Frozen scientific, math, evidence, safety, context and tool-use suite |
| Release engineering | Model and dataset repositories | Versioned artifacts, cards, citations, manifests and rollback instructions |

## 2. Upgrade the existing datasets

The D01–D04 labels follow the Trimorious portfolio definition.

### D01 — Scientific Instructions

**Current published inventory:** 3,335 training examples and 371 validation examples (3,706 total). These are dataset-card metadata counts and have not yet been independently recomputed from Parquet rows.

Objective: expand basic scientific Q&A into high-quality instruction and research reasoning.

Target categories:
- scientific explanation;
- hypothesis generation and testing;
- causal inference;
- literature review and research methodology;
- peer review and scientific criticism;
- evidence synthesis;
- uncertainty reasoning;
- multidisciplinary reasoning;
- scientific communication.

Include English, Bahasa Malaysia and other languages only with appropriate technical and native-language review. The initial target is 50,000–100,000 deduplicated high-quality examples. Do not reach the target by low-quality synthetic volume. Every record needs provenance, quality state and appropriate verification.

### D02 — Symbolic Trajectories

**Current published inventory:** 7,784 training examples.

Highest research priority for mathematical reasoning. Target domains include algebra, calculus, linear algebra, discrete mathematics, statistics, optimization, numerical methods, differential equations, physics, chemistry, computer science and operations research.

The upgraded representation should store structured execution trajectories rather than only question-answer messages. Use `schemas/v2/symbolic-trajectory.schema.json`.

A trajectory should contain problem and domain metadata, difficulty, assumptions, variables and units, ordered operations and expressions, normalized final answer, independent verification, source and quality metadata. Add multiple valid solution paths, labelled incorrect solutions, boundary conditions, numerical cross-validation and formal proofs where feasible.

Initial target: 100,000–250,000 verified trajectories. Prioritize correctness and path diversity over count.

### D03 — Knowledge Base

**Current published inventory:** 7,784 records.

Redesign as a scientific knowledge/evidence repository and graph. Separate:
1. original source documents;
2. extracted passages/chunks;
3. normalized scientific claims;
4. equations and variable definitions;
5. experiment/method/result entities;
6. generated training examples.

Represent research papers, claims, equations, experiments and findings. Support relationships such as `supports`, `contradicts`, `derived_from` and `validated_by`. Store claim IDs, evidence passage/location, DOI, authors, publication date, LaTeX, variables, units, assumptions, source rights, extraction confidence and review status.

Never let a synthetic interpretation overwrite original research evidence. Initial planning target: 50,000–100,000 validated claims, progressively expanded. This target counts claims, not documents.

### D04 — Agentic Reasoning Knowledge

**Current published inventory:** 225 training examples.

Teach actions, observations and verified outcomes, not merely prose descriptions of action. Add planning, tool selection, execution, observation, replanning, multi-agent delegation, independent verification, recovery, research orchestration and decision-making.

Use `schemas/v2/agentic-trajectory.schema.json`. Include successful, partially successful and failed trajectories. Failed actions must teach error detection and recovery, not blind imitation.

Initial target: 20,000–50,000 high-quality trajectories.

## 3. Six additional datasets

| ID | Repository | Purpose | Initial planning target |
|---|---|---|---:|
| D05 | `trimorious-mathematical-verification` | Independent mathematical correctness | 50,000 examples |
| D06 | `trimorious-scientific-preferences` | Scientific answer preference pairs | 30,000–50,000 pairs |
| D07 | `trimorious-scientific-evaluation` | Independent benchmark | 5,000–10,000 cases |
| D08 | `trimorious-multilingual-science` | Global multilingual science | 30,000–50,000 examples |
| D09 | `trimorious-safety-and-reliability` | Safety and reliable behavior | 15,000–30,000 examples |
| D10 | `trimorious-scientific-environments` | Executable RL/tool-use environments | 100–500 environments |

### D05 — Mathematical Verification

Include SymPy solutions, numerical verification, formal proof examples where feasible, counterexamples, dimensional analysis and incorrect derivations/error classification. Make verifier identity, version, output, tolerance and execution state explicit.

### D06 — Scientific Preferences

Include correct/incorrect explanations, supported/unsupported claims, strong/weak hypotheses, calibrated/uncalibrated uncertainty and valid/fabricated citations. Require human or expert-calibrated labels, rubric consistency, adjudication and annotator agreement. DPO and related methods are candidates only after label quality is established.

### D07 — Scientific Evaluation

Cover mathematics, scientific reasoning, causal reasoning, evidence retrieval, hypothesis testing and long-context comprehension. Separate development, public test and hidden test. Hidden test data must never be used in training, preference construction, reward-model training, RL or prompt tuning.

### D08 — Multilingual Science

Initial languages: English, Bahasa Malaysia, Indonesian, Chinese, Arabic, Spanish, French and Japanese. Include technical terminology alignment, translations, bilingual explanations and equivalent scientific questions. Require native-language technical review; machine translation alone is insufficient.

### D09 — Safety and Reliability

Cover prompt injection, malicious tool instructions, citation manipulation, scientific misinformation, unsupported medical claims, hazardous scientific requests, privacy/confidential data, uncertainty/abstention and safe user-document handling. Define a risk taxonomy, expected behavior, adjudicated labels and regression tests.

### D10 — Scientific Environments

Create executable math, physics, chemistry, scientific data analysis, optimization, retrieval, experimental design and multi-step investigation environments. Each environment defines observations, actions, state transitions, termination, allowed tools, initialization, sandbox resource/network/filesystem limits, deterministic replay and verifiable rewards.

## 4. Model evolution strategy

Retain the existing public model as the immutable baseline. Upgrade through distinct releases:
- **v1.1:** data cleaning, scientific instruction quality, verified math SFT, tokenizer/template/inference checks.
- **v1.2:** symbolic verification, preference optimization, uncertainty calibration, evidence grounding and multilingual experiments.
- **v1.3:** agentic tool use, planning, recovery, multi-agent coordination and selective GRPO experiments using D10 verifiable rewards.
- **v2.0:** consolidated reproducible pipeline, full evaluation, context and inference optimization, public-serving compatibility and release artifacts.

Do not overwrite the current model repository's existing revision. Candidate adapters and merged/quantized variants require clearly identified version tags or separate repositories. Benchmark newer base models before selecting a replacement. Keep the current 3B-class base as the experimental control; investigate 7B–8B or 14B only if controlled evaluation justifies the compute and serving cost. Training a foundation model from scratch is a later research decision, not a prerequisite for this programme.

Test 2K, 8K, 16K and 32K context behavior. The base model's advertised maximum does not prove that the adapter was trained or performs well at that length.

## 5. Repository and release hygiene

### Model repository

Add or verify, as technically applicable:
- complete README/model card;
- correct config and generation config;
- tokenizer and special-token metadata;
- adapter config or merged model weights;
- training configuration and environment lock;
- evaluation results;
- license and citation metadata;
- security reporting policy.

Publish only variants with distinct purpose and compatibility notes: adapter, merged checkpoint, inference-ready checkpoint and quantized format where supported. Avoid redundant weights without a user need.

### Dataset repositories

Standardize each dataset repository with:
- README/dataset card and license;
- citation metadata;
- data config and schema;
- train/validation/test split policy;
- quality, deduplication and provenance reports;
- validation, inspection and deduplication scripts;
- version history.

The central `trimorious-datasets` repository governs contracts and pipelines; it should not duplicate large Parquet payloads.

## 6. Data and model factory

Proposed logical flow:

1. **Acquisition:** arXiv, OpenAlex, public and licensed sources.
2. **Extraction:** Docling and source-specific parsers.
3. **Processing:** normalization, deduplication, source attribution and chunking.
4. **Quality control:** schema checks, source checks, symbolic verification and human review.
5. **Dataset factory:** versioned D01–D10 with immutable source revisions.
6. **Evaluation factory:** frozen independent benchmarks and verifiers.
7. **Training factory:** SFT, preference optimization, and RL only for tasks with valid reward signals.
8. **Model registry:** experiment tracking, lineage, checkpointing and rollback.
9. **Release:** Hugging Face artifacts, inference examples, serving/API and monitoring.

Candidate tools include Hugging Face Datasets, Pandera/custom validators, SymPy, MLflow, Transformers, TRL, Unsloth, lm-evaluation-harness, vLLM, FastAPI, Prometheus and Grafana. Tool choice must be tested against the selected hardware, license, maintenance and deployment constraints.

## 7. Public-readiness acceptance criteria

| Area | Proposed acceptance gate |
|---|---|
| Dataset integrity | 100% of released records pass the versioned schema |
| Provenance | Every record has source or generation provenance |
| Deduplication | Exact and semantic deduplication policy and report |
| Mathematics | Independently verified ground truth and pass-rate report |
| Scientific answers | Evidence and citation traceability |
| Evaluation | Matched baseline vs candidate results |
| Safety | Documented safety benchmark and regression outcomes |
| Reproducibility | Complete training manifest and replay instructions |
| Inference | Validated local and API inference, tokenizer/template checks |
| Deployment | Tested serving and quantization variants |
| Licensing | Completed rights and compatibility audit |
| Documentation | Complete model and dataset cards |

These are proposed gates, not claims that the current project meets them.

## 8. Suggested 16-week sequence

| Period | Focus | Outputs |
|---|---|---|
| Weeks 1–2 | Audit and remediation | Parquet audit, model/artifact inspection, license review, baseline benchmarks |
| Weeks 3–5 | Dataset restructuring | Versioned D01–D04 derivatives, schemas, validators, D05–D07 foundations |
| Weeks 6–8 | Capability expansion | D08–D10, verified math trajectories, multilingual/safety/agentic content |
| Weeks 9–12 | Model training | SFT candidates, preference experiments, selective GRPO, baseline comparisons |
| Weeks 13–14 | Verification | benchmark, adversarial, inference, quantization and reproducibility tests |
| Weeks 15–16 | Public release | versioned datasets/model, evaluations, docs and developer examples |

This is a planning cadence, not a delivery promise; sequence and duration depend on dataset rights, compute, human review capacity and measured audit findings.
