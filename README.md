# Trimorious — Data and Model Engineering

This repository is the engineering control plane for the Trimorious scientific research model. It governs dataset contracts, provenance, quality validation, training-data preparation, evaluation and release engineering. The source dataset repositories remain separate and are not overwritten by this repository.

## Portfolio

### Existing datasets — D01 to D04

| ID | Dataset | Hugging Face source | Published metadata |
|---|---|---|---:|
| D01 | Scientific Instructions | [trimorious-scientific-instructions](https://huggingface.co/datasets/roime81/trimorious-scientific-instructions) | 3,335 train / 371 validation |
| D02 | Symbolic Trajectories | [trimorious-symbolic-trajectories](https://huggingface.co/datasets/roime81/trimorious-symbolic-trajectories) | 7,784 train |
| D03 | Knowledge Base | [trimorious-knowledge-base](https://huggingface.co/datasets/roime81/trimorious-knowledge-base) | 7,784 train |
| D04 | Agentic Reasoning Knowledge | [trimorious-agentic-reasoning-knowledge](https://huggingface.co/datasets/roime81/trimorious-agentic-reasoning-knowledge) | 225 train |

Published counts have not yet been independently recomputed from decoded Parquet rows.

### Proposed datasets — D05 to D10

| ID | Dataset | Primary role | Planning target |
|---|---|---|---:|
| D05 | Mathematical Verification | Independent mathematical correctness | 50,000 examples |
| D06 | Scientific Preferences | Preference optimization | 30,000–50,000 pairs |
| D07 | Scientific Evaluation | Held-out measurement | 5,000–10,000 cases |
| D08 | Multilingual Science | Multilingual scientific capability | 30,000–50,000 examples |
| D09 | Safety and Reliability | Safety and robust behavior | 15,000–30,000 examples |
| D10 | Scientific Environments | Executable environments for tool use and RL | 100–500 environments |

D05–D10 are proposed assets, not existing datasets. Targets are planning estimates, not commitments or measured quality claims. D07 is evaluation-only and must not leak into training or model selection.

## Engineering principles

1. Preserve original D01–D04 source revisions. Publish cleaned or transformed derivatives as new versions.
2. Store original source documents, extracted chunks, normalized claims and generated training examples as separate artifacts.
3. Require data provenance, rights review, schema validation, deduplication, split-leakage checks and quality reporting.
4. Verify mathematical outputs independently; generated text is not ground truth by itself.
5. Require real execution and replay evidence for agent tool traces and D10 environments.
6. Keep hidden evaluation data isolated from SFT, preference optimization, reward models, RL and prompt tuning.
7. Track model/data revisions, seeds, dependencies, hardware, training configuration and evaluation artifacts for every release.

## Repository layout

- `configs/dataset_registry.json` — D01–D10 registry, source mapping, intended uses and quality gates.
- `schemas/v1/` — observed baseline record contracts.
- `schemas/v2/` — target contracts for upgraded datasets.
- `scripts/audit_datasets.py` — read-only Hugging Face source audit.
- `docs/production-readiness-backlog.md` — master gap register and workstreams.
- `docs/audit-plan.md` — baseline findings and acceptance gates.
- `docs/roadmap.md` — D05–D10 development roadmap.
- `docs/model-release-plan.md` — model release and training strategy.
- `configs/release-gates.json` — proposed production-readiness acceptance gates.

## Run the current baseline audit

```bash
python -m pip install -r requirements.txt
python scripts/audit_datasets.py --revision main --output reports/audit-latest.json
```

The script reads public Hugging Face datasets and writes aggregate statistics. It does not modify or upload source data. Pin a specific Hub commit SHA for a release-grade audit.

## Status

Phase 1 engineering scaffolding is under review in [PR #1](https://github.com/roime81/trimorious-datasets/pull/1). Live record-level audit, source licensing review, baseline inference evaluation and benchmark execution remain outstanding. No retraining or public model release is claimed by this repository state.
