# Trimorious model — initial baseline record

## Repository

- Hugging Face: [roime81/trimorious-research-4B](https://huggingface.co/roime81/trimorious-research-4B)
- GitHub mirror: [roime81/trimorious-model](https://github.com/roime81/trimorious-model)

## Declared architecture

The model card describes a causal language model adapted with Unsloth and TRL using QLoRA on `unsloth/Qwen2.5-3B-Instruct-bnb-4bit`.

The upstream base model card identifies approximately 3.09B parameters, 36 layers and a 32,768-token context window: [base model card](https://huggingface.co/unsloth/Qwen2.5-3B-Instruct-bnb-4bit).

Adapter configuration observed in GitHub:

- PEFT type: LoRA
- Rank: 16
- Alpha: 16
- Dropout: 0
- Target modules: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
- Task type: CAUSAL_LM

The README reports batch size 2, gradient accumulation 4, learning rate 2e-4 and cosine scheduling. These are declarations in documentation, not a verified run manifest.

## Artifact inventory

The repository contains the adapter configuration, adapter weights, tokenizer files, chat template, README and Apache-2.0 license. The GitHub tree stores the following as LFS pointer files:

- `adapter_model.safetensors`: 119,801,528 bytes declared by the LFS pointer.
- `tokenizer.json`: 11,422,166 bytes declared by the LFS pointer.

The full upstream base-model weights are not included, which is normal for an adapter-only release. A reproducible loading path must explicitly fetch the correct base-model revision and attach the adapter.

## Correctness and naming issues to resolve

1. The project artifact is named `trimorious-research-4B`, but its declared base is a 3B model (about 3.09B parameters). Confirm model identity and choose an accurate release name; do not rename an existing public revision prematurely.
2. The inference example uses `max_seq_length=2048`, while the tokenizer declares 32,768. Measure actual context performance and memory requirements rather than assuming 32K support for the adapted model.
3. The chat template fallback says the assistant is Qwen. Decide whether a Trimorious-specific system identity is desired and test the tool-call path before changing it.
4. The repository does not contain the complete original training script, package lock, hardware specification, exact dataset commit SHAs, training run ID, seed, epochs/steps, optimizer settings, or evaluation metrics.

## Required baseline capture

Before retraining, produce a versioned manifest with:

- exact base model ID and commit SHA;
- adapter commit SHA and LFS object checksums;
- tokenizer revision and chat-template hash;
- exact dataset IDs, revisions and split selections;
- complete training arguments, random seeds and effective token counts;
- package/environment lock and GPU hardware;
- deterministic inference smoke tests;
- benchmark inputs, scoring code and baseline results.

The baseline must remain immutable. Candidate adapters should be published under a new version or repository revision and compared against it using the same benchmark.
