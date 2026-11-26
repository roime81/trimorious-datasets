# Phase 1 — Baseline audit and remediation plan

## Scope

The baseline consists of one model repository and four dataset repositories under the `roime81` Hugging Face and GitHub accounts. The source datasets remain the authoritative data artifacts. GitHub mirrors are for engineering workflows and review; they are not a reason to fork or alter source data.

## Findings verified from repository metadata

### Dataset inventory

| ID | Repository | Published split counts | Record fields |
|---|---|---:|---|
| D01 | `trimorious-symbolic-trajectories` | 7,784 train | `messages: [{role, content}]` |
| D02 | `trimorious-scientific-instructions` | 3,335 train; 371 validation | `messages: [{role, content}]` |
| D03 | `trimorious-knowledge-base` | 7,784 train | `doc_id, title, source, section, text` |
| D04 | `trimorious-agentic-reasoning-knowledge` | 225 train | `messages, ground_truth` |

Counts and feature definitions are from the published dataset metadata reproduced in the GitHub mirror READMEs. They have not yet been independently recomputed from decoded Parquet rows.

The Parquet paths in GitHub are Git LFS pointers. The pointer metadata identifies the stored object sizes as approximately 13.5 MB (D01), 6.28 MB plus 0.71 MB (D02), 4.37 MB (D03), and 0.58 MB (D04). The LFS payloads themselves are not ordinary 131-byte Git files.

### Initial usage decisions

- **D01:** candidate supervised fine-tuning data, pending symbolic correctness, diversity, source and duplicate checks.
- **D02:** candidate supervised fine-tuning data. Preserve the existing validation split; measure train/validation leakage before using it as a release benchmark.
- **D03:** retrieval/evidence corpus by default. It needs source-level provenance, document-level rights review, chunking strategy and retrieval evaluation before use.
- **D04:** agentic supervision candidate. It is only 225 records and has no published validation split; inspect tool traces, outcome verifiability and diversity before using it for agentic training.

## Model baseline

The model repository describes `trimorious-research-4B` as a QLoRA adapter over `unsloth/Qwen2.5-3B-Instruct-bnb-4bit`. Its adapter configuration confirms LoRA rank 16, alpha 16, dropout 0, and target modules covering Q/K/V/O plus the MLP projections.

The base model card reports 3.09 billion parameters, 36 transformer layers and a 32,768-token context window. Therefore, the current repository name `4B` does not match the documented base checkpoint. Do not rename or replace the published model until the actual adapter and original training run are verified.

The model README reports batch size 2, gradient accumulation 4, learning rate 2e-4 and cosine scheduling. It does not provide a complete run manifest: epochs, optimizer, warmup, seed, dataset revisions, effective token count, training steps, hardware, package lock, checkpoints, or evaluation results are not present in the inspected GitHub tree.

The README inference example sets `max_seq_length=2048`, while the tokenizer configuration declares `model_max_length=32768`. The supported context length of the base model is not evidence that this adapter was trained or evaluated at 32K. Benchmark context lengths explicitly.

The checked-in chat template has a fallback system prompt identifying the assistant as Qwen. Review this behavior against the intended Trimorious persona and tool-call format before changing it.

## What remains unverified

1. Actual decoded Parquet records, content quality, correctness, duplicate rate and language distribution.
2. Whether the Git LFS payloads for every mirror are downloadable and hash-identical to the Hugging Face source payloads.
3. Per-record upstream source, license and attribution.
4. Exact model adapter compatibility with its base checkpoint and tokenizer.
5. Whether the advertised training settings match the original completed run.
6. Baseline generation quality, factuality, mathematical validity, instruction following and tool-use reliability.

## Phase 1 acceptance gates

- [ ] Run `scripts/audit_datasets.py` against all four public Hub datasets.
- [ ] Review nulls, blanks, malformed messages, duplicate rows, role distributions and train/validation exact overlap.
- [ ] Sample and manually review at least 100 examples per dataset, stratified by data source or topic where available.
- [ ] Verify source URLs, identifiers, licenses and attribution requirements.
- [ ] Pin each source dataset to a commit SHA and record the SHA in the audit report.
- [ ] Load the exact base model plus adapter and run a deterministic smoke test.
- [ ] Capture a baseline evaluation set and metrics before any retraining.

## Safety and reproducibility rules

- Never edit D01–D04 in place. Publish cleaned derivatives as new versioned datasets.
- Never use validation or test examples for training, augmentation, preference construction or prompt tuning.
- Never treat a generated answer as verified ground truth without an independent verifier or qualified review.
- Keep original text and binary payloads out of audit logs. Reports should contain aggregate statistics and hashes only.
- Do not claim model improvement until matched evaluation demonstrates it.
