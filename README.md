# Trimorious Dataset Engineering

This repository is the engineering control plane for the Trimorious research-model datasets.

It contains dataset contracts, provenance and quality checks, preprocessing utilities, evaluation-set governance, and reproducible training-data preparation. The large source datasets remain in their dedicated Hugging Face repositories; this repository does not duplicate their Parquet payloads.

## Source datasets

| ID | Dataset | Hugging Face source | Current metadata |
|---|---|---|---:|
| D01 | Symbolic Trajectories | [roime81/trimorious-symbolic-trajectories](https://huggingface.co/datasets/roime81/trimorious-symbolic-trajectories) | 7,784 train |
| D02 | Scientific Instructions | [roime81/trimorious-scientific-instructions](https://huggingface.co/datasets/roime81/trimorious-scientific-instructions) | 3,335 train / 371 validation |
| D03 | Knowledge Base | [roime81/trimorious-knowledge-base](https://huggingface.co/datasets/roime81/trimorious-knowledge-base) | 7,784 train |
| D04 | Agentic Reasoning Knowledge | [roime81/trimorious-agentic-reasoning-knowledge](https://huggingface.co/datasets/roime81/trimorious-agentic-reasoning-knowledge) | 225 train |

Counts above are the published dataset metadata observed during the initial repository audit. They are not yet a quality certification. See [the audit plan](docs/audit-plan.md).

## Working principles

1. Preserve D01–D04 as immutable baselines while remediation is performed in versioned derived datasets.
2. Treat D03 as a retrieval/evidence corpus by default, not automatically as supervised fine-tuning data.
3. Require schema validation, provenance, deduplication, split-leakage checks, and documented licensing before training.
4. Keep a held-out evaluation set out of all training and preference-optimization pipelines.
5. Record the base-model revision, tokenizer, data revisions, preprocessing code, training configuration, seeds, environment, and evaluation results for every model release.

## Repository layout

- `configs/dataset_registry.json` — source registry and schema mapping.
- `schemas/v1/` — record-level data contracts.
- `scripts/audit_datasets.py` — read-only Hub dataset audit.
- `docs/audit-plan.md` — findings, limitations, and next steps.
- `docs/roadmap.md` — D05–D10 expansion proposal.

## Run the first audit

```bash
python -m pip install -r requirements.txt
python scripts/audit_datasets.py --output reports/audit.json
```

The script reads the public Hugging Face datasets and writes aggregate quality statistics. It does not modify or upload the source datasets.

## Status

**Phase 1 — baseline audit and data contracts.** The current source Parquet files and model artifacts are preserved. Detailed record-level validation, source attribution review, and baseline model evaluation remain to be run before data remediation or retraining.
