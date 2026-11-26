# Trimorious data and model factory

## Lifecycle

1. **Acquire:** register source, owner, URL/DOI, retrieval timestamp, license and redistribution decision.
2. **Extract:** parse papers/documents with source-specific parsers (Docling where suitable); preserve original source and extraction metadata.
3. **Normalize:** standardize fields, IDs, Unicode, equations, units, language tags and source references.
4. **Deduplicate:** exact content hash plus domain-appropriate semantic near-duplicate checks; record thresholds and review decisions.
5. **Validate:** schema, required fields, provenance, rights, source resolvability, content-quality checks and domain verifiers.
6. **Curate:** stratified human review; maintain rejection and adjudication reasons.
7. **Split:** group by source/work/topic where appropriate to reduce leakage; keep D07 hidden evaluation isolated.
8. **Publish:** immutable Hub revision/tag, dataset card, schema, quality report, source register and checksum manifest.
9. **Train:** pin dataset revisions, training code commit, config, environment, seed and hardware.
10. **Evaluate:** matched frozen benchmark, verifier results, safety and serving measurement.
11. **Release:** version model and adapters, publish model card and manifest, keep rollback path.

## Candidate toolchain

| Function | Candidate technology | Adoption condition |
|---|---|---|
| Document extraction | Docling | Validate extraction accuracy on representative papers and tables |
| Dataset processing | Hugging Face Datasets / PyArrow | Pin versions and retain deterministic transforms |
| Data validation | JSON Schema, Pandera, custom validators | Version contracts and run in CI |
| Mathematics | SymPy and numerical libraries | Independent verification and timeout limits |
| Experiment tracking | MLflow | Store run metadata, artifacts and model/data lineage |
| Fine-tuning | Transformers, PEFT, TRL, Unsloth | Compatibility test against selected base and GPU stack |
| Preference optimization | TRL DPO/related algorithms | Only after preference-label reliability is measured |
| RL | TRL or a suitable RL framework | Only with sandboxed environments and verifiable rewards |
| Evaluation | lm-evaluation-harness plus custom tasks | Frozen scoring code and leakage controls |
| Serving | vLLM / Transformers | Correct chat template, tool-call compatibility and load tests |
| API | FastAPI | Authentication, quotas, validation and error handling |
| Monitoring | Prometheus / Grafana | Privacy-aware latency, error and resource telemetry |

## Artifact lineage

Every released model must link to:
- source dataset repository and immutable revision;
- derivative dataset revision and transformation commit;
- schema and validator versions;
- training code commit and configuration hash;
- model base revision and adapter/merged artifact hashes;
- benchmark and scoring code revision;
- license/rights review status.

## Security controls

- Run untrusted code and tool actions only in isolated sandboxes with explicit CPU, memory, wall-time, filesystem and network policy.
- Never place credentials or tokens in training examples, logs or public artifacts.
- Treat retrieved documents and tool outputs as untrusted input.
- Do not publish confidential documents or personal data as scientific examples.
- Keep a release and incident rollback process.
