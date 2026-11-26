# Trimorious repository standard

This layout is a target standard. Preserve source dataset layouts until the audit establishes a safe, versioned migration plan.

## Dataset repositories

```text
dataset-repository/
├── README.md                  # Hugging Face dataset card
├── LICENSE
├── CITATION.cff
├── dataset_card.yaml
├── data/
│   ├── train/
│   ├── validation/
│   └── test/
├── configs/
│   └── dataset_config.yaml
├── schemas/
│   └── schema.json
├── quality/
│   ├── validation_report.json
│   ├── deduplication_report.json
│   └── provenance_report.json
└── scripts/
    ├── validate.py
    ├── deduplicate.py
    └── inspect.py
```

For repositories with hidden evaluation cases, keep private or controlled test artifacts outside public dataset payloads and describe access policy in the card. D07 must never be repurposed as training data.

## Model repository

Add or validate, as applicable:
- README.md: comprehensive model card;
- config.json: verified architecture configuration (for merged/full checkpoint);
- generation_config.json;
- tokenizer_config.json and special_tokens_map.json;
- adapter_config.json for adapter-only publication;
- model.safetensors only for a complete merged model, not as a substitute for adapter weights;
- training_config.yaml and environment lock;
- evaluation_results.json;
- LICENSE, CITATION.cff and SECURITY.md.

State clearly whether the repository contains an adapter or full model. An adapter-only release must pin the base model and explain loading order. Publish merged, GGUF or other quantized versions only after compatibility tests and only if each has a clear distribution purpose.
