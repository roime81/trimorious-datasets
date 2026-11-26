# Trimorious model release and training strategy

## Baseline preservation

Current public baseline:
- Hugging Face: `roime81/trimorious-research-4B`
- GitHub mirror: `roime81/trimorious-model`
- Declared base: `unsloth/Qwen2.5-3B-Instruct-bnb-4bit`
- Declared method: QLoRA/LoRA via Unsloth and TRL
- Declared adapter: rank 16, alpha 16, dropout 0, causal language modeling

The current artifact remains the baseline. Do not overwrite its current revision or relabel it until the exact base revision, adapter compatibility, parameter count and training provenance have been confirmed.

## Release train

### Trimorious Research 4B v1.1 — Data and SFT quality

Foundation: existing Qwen2.5-3B-Instruct base, subject to compatibility verification.

Scope:
- remediate D01–D04 into versioned derivatives;
- improve scientific instruction data;
- add independently verified mathematical SFT from D02/D05;
- validate tokenizer, special tokens, chat template and generation config;
- standardize Transformers and Unsloth inference;
- capture matched baseline metrics.

Exit gate: training data rights cleared, all records schema-valid, leakage checks passed, training manifest complete, and candidate beats or justifiably trades off with baseline on predeclared metrics without unacceptable safety regressions.

### Trimorious Research 4B v1.2 — Verification, evidence and preferences

Scope:
- add D05 symbolic verification signals;
- use D03 evidence graph for cited/grounded response behavior;
- introduce D06 preference optimization after expert-label quality checks;
- improve uncertainty and abstention;
- test D08 multilingual capability with native-language review.

Exit gate: independently verified math gains, evidence-support gains, calibrated preference data and no material regressions on general scientific instruction or safety evaluations.

### Trimorious Research 4B v1.3 — Agentic tools and selective RL

Scope:
- expand D04 replayable agentic trajectories;
- integrate D10 sandboxed environments;
- train planning, tool selection, execution, observation, recovery and verification;
- test multi-agent delegation where tasks genuinely benefit;
- experiment with GRPO or another appropriate RL method only where rewards are executable and difficult to game.

Exit gate: tool traces replay, reward functions pass exploit tests, success is measured on unseen environments, and tool safety controls remain effective.

### Trimorious Research v2.0 — Consolidated public release

Scope:
- consolidated reproducible data/model factory;
- complete held-out evaluation using D07;
- long-context and inference optimization;
- Transformers/vLLM/API compatibility;
- safety, licensing and documentation review;
- release manifests, checksums, model/dataset cards and rollback procedure.

Model size is a separate decision. Benchmark newer open-weight base models against the retained Qwen baseline before moving to 7B–8B or 14B. A larger parameter count is not itself an acceptance criterion. Foundation-model pretraining from scratch is outside the initial scope.

## Benchmark protocol

Run the same frozen benchmark against:
1. the untouched base model;
2. the existing Trimorious adapter;
3. each candidate adapter/checkpoint.

Track at minimum:
- scientific instruction following;
- mathematical exact/solver verification;
- evidence retrieval and claim support;
- citation correctness;
- hypothesis and causal reasoning;
- agentic task success and tool replay;
- context-length performance at 2K, 8K, 16K and 32K where feasible;
- safety, prompt injection and refusal behavior;
- latency, throughput, memory and serving compatibility.

Report per-domain scores and confidence intervals where sampling supports them. Keep D07 hidden test cases sealed and do not use them in training or iterative tuning.

## Required run manifest

Every training run must record:
- run ID, timestamp, code commit and config hash;
- base model ID and exact commit SHA;
- adapter/checkpoint input and output hashes;
- tokenizer revision, chat-template hash and special-token map;
- exact dataset IDs, commit SHAs, split selections and filtering version;
- sequence length, packing, sample/token counts and data-mixture weights;
- optimizer, learning rate, scheduler, warmup, epochs/steps, batch size, gradient accumulation and precision;
- random seeds and determinism settings;
- GPU type/count, memory and runtime;
- Python, CUDA, PyTorch, Transformers, PEFT, TRL and Unsloth versions;
- checkpoints, logs, evaluation config and measured results;
- license and source-rights status for all training inputs.

## Publication variants

Publish a LoRA adapter, merged checkpoint, inference-ready package or quantized variant only when each has a distinct use case, validated loading path, compatibility notes and checksums. The adapter-only variant must always identify and pin the required base model. Avoid duplicated multi-gigabyte artifacts without an explicit distribution reason.
