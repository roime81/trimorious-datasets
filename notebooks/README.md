# Trimorious 2.0 — Scientific data engineering

The notebooks in this directory reproduce the engineering methods used to audit, reconstruct and generate scientific candidate datasets. They are source-only research artifacts, not approved public data releases.

| Milestone | Purpose |
|---|---|
| M1.2 | Initial schema remediation |
| M1.2.1 | Schema-aware reconstruction and quarantine |
| M1.4 | Initial 1,000-example candidate corpus |
| M1.4.1 | 5,000-example candidate corpus and optional teacher orchestration |
| M1.4.1 GPU pilot | Optional resumable teacher inference |

Some notebooks require privately retained input archives. D07 questions, answer keys, benchmark-generation templates, private audits, reviewer records, candidate data files and tokens are intentionally omitted. Do not publish or train on the private benchmark. No candidate is automatically approved merely because a numerical answer passes a check.

The later notebook convention assigns D01 to scientific instructions and D02 to symbolic trajectories; the older repository README reverses those labels. Use the explicit Hugging Face repository identifiers when resolving inputs, and document the mapping before publishing future dataset revisions.

The recorded experimental v2 training used only 288 development and 36 validation examples; no teacher-generated responses or multi-tool trajectories were used. The generated 5,000 candidates are not equivalent to 5,000 approved training examples.

[Model development, results and handbook companion](https://github.com/roime81/trimorious-model/tree/docs/trimorious-v2-research-release/docs/trimorious-v2).
