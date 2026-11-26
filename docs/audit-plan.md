# Phase 1 — Baseline audit and remediation plan

## Scope

The baseline consists of the existing model repository and four dataset repositories under the `roime81` Hugging Face and GitHub accounts. The source datasets remain authoritative. GitHub mirrors are engineering mirrors; they are not a reason to fork or alter source data.

## Dataset inventory

The D01–D04 labels below follow the Trimorious production-readiness backlog.

| ID | Dataset | Published split counts | Existing record fields |
|---|---|---:|---|
| D01 | Scientific Instructions | 3,335 train; 371 validation | `messages: [{role, content}]` |
| D02 | Symbolic Trajectories | 7,784 train | `messages: [{role, content}]` |
| D03 | Knowledge Base | 7,784 train | `doc_id, title, source, section, text` |
| D04 | Agentic Reasoning Knowledge | 225 train | `messages, ground_truth` |

Counts and features are from the published Hugging Face dataset metadata reproduced in GitHub mirror READMEs. They have not yet been independently recomputed from decoded Parquet rows.

## Initial usage and upgrade decisions

- **D01 — Scientific Instructions:** candidate scientific instruction SFT. Expand coverage across explanations, hypothesis generation/testing, causal inference, literature review, methodology, peer review, criticism, evidence synthesis, uncertainty, multidisciplinary reasoning and scientific communication. Preserve current validation split until exact and semantic leakage checks are complete.
- **D02 — Symbolic Trajectories:** highest research priority for mathematical and symbolic reasoning. Replace chat-only records in a versioned derivative with structured trajectories: assumptions, domains, subdomains, difficulty, problem, typed steps, normalized answer, verifier, verification status, source and quality assessment. Include multiple paths, labelled errors, boundary conditions and numerical cross-validation.
- **D03 — Knowledge Base:** redesign as a scientific evidence repository/graph. Separate raw documents, extracted chunks, normalized claims and generated examples. Add paper, claim, equation, experiment and finding entities with supports, contradicts, derived-from and validated-by relationships. Never overwrite original research evidence with generated interpretation.
- **D04 — Agentic Reasoning Knowledge:** expand from action descriptions into executable trajectories: task, goal, plan, tool calls, observations, replanning, verification, outcome and reward. Include successful, partially successful and failed trajectories; failed actions should teach recovery rather than blind imitation.

## Model baseline findings

The model README describes `trimorious-research-4B` as a QLoRA adapter over `unsloth/Qwen2.5-3B-Instruct-bnb-4bit`. Its adapter configuration confirms LoRA rank 16, alpha 16, dropout 0 and target modules covering attention and MLP projections.

The documented base model reports approximately 3.09B parameters, 36 layers and a 32,768-token context window. The repository name "4B" therefore does not match the documented base checkpoint. Verify actual adapter/base compatibility before renaming or replacing the public artifact.

The model README reports batch size 2, gradient accumulation 4, learning rate 2e-4 and cosine scheduling. The inspected repository does not provide a complete run manifest containing epochs/steps, optimizer, warmup, seed, exact dataset commit SHAs, effective token count, hardware, package lock, training logs or evaluation metrics.

The inference example sets `max_seq_length=2048`, while tokenizer configuration declares `model_max_length=32768`. Benchmark 2K, 8K, 16K and 32K contexts explicitly; a base-model limit is not proof that the adapter was trained or evaluated at that length.

The checked-in chat template uses a fallback system prompt identifying the assistant as Qwen. Test persona and tool-call behavior before modifying it.

## Unverified items

1. Decoded Parquet rows, correctness, quality, duplicate rate, language and topic distributions.
2. Git LFS object integrity and byte-level equivalence between Hugging Face source payloads and GitHub mirrors.
3. Per-record source provenance, upstream licensing and attribution obligations.
4. Adapter loading with the exact base-model and tokenizer revisions.
5. Whether documented training parameters match the completed training run.
6. Baseline factuality, mathematical validity, instruction following, citation quality, safety and tool-use reliability.

## Phase 1 acceptance gates

- [ ] Run `scripts/audit_datasets.py` for D01–D04 using pinned Hub commit SHAs.
- [ ] Review nulls, blanks, malformed messages, exact duplicates, role distributions and train/validation overlap.
- [ ] Review at least 100 stratified records per dataset, where licensing permits local inspection.
- [ ] Verify source URLs, identifiers, publication details, licenses and attribution.
- [ ] Load the exact base model plus adapter and run deterministic inference smoke tests.
- [ ] Evaluate context lengths 2K, 8K, 16K and 32K where hardware permits.
- [ ] Capture original-model and base-model results on a frozen, leakage-checked benchmark before any training.
- [ ] Record exact source revisions and binary checksums.

## Non-negotiable controls

- Never edit original D01–D04 revisions in place. Publish cleaned derivatives with new version identifiers.
- Never use hidden D07 evaluation cases for training, augmentation, preference construction, reward-model training, RL or iterative prompt tuning.
- Never treat generated answers as verified ground truth without an independent verifier or qualified review.
- Keep source text and binary payloads out of audit logs; aggregate statistics and hashes are sufficient for routine reports.
- Do not claim model improvement without matched baseline evaluation.
