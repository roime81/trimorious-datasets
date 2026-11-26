#!/usr/bin/env python3
"""Read-only structural and quality audit for the Trimorious Hub datasets.

The report contains aggregate counts and hashes only. It does not emit record
text, mutate Hub repositories, or upload any files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from datasets import load_dataset

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "configs" / "dataset_registry.json"


def stable_hash(record: dict[str, Any]) -> str:
    payload = json.dumps(
        record, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def audit_split(dataset: Any, split_name: str, record_type: str) -> tuple[dict[str, Any], set[str]]:
    total = len(dataset)
    hashes: set[str] = set()
    duplicate_count = 0
    null_counts: Counter[str] = Counter()
    blank_counts: Counter[str] = Counter()
    role_counts: Counter[str] = Counter()
    invalid_message_records = 0
    records_without_user = 0
    records_without_assistant = 0
    empty_messages = 0
    malformed_ground_truth = 0
    message_count = 0
    message_content_chars = 0
    text_chars = 0
    source_counts: Counter[str] = Counter()
    invalid_examples: list[int] = []

    feature_names = list(dataset.features.keys())

    for index, raw_record in enumerate(dataset):
        record = dict(raw_record)
        record_hash = stable_hash(record)
        if record_hash in hashes:
            duplicate_count += 1
        else:
            hashes.add(record_hash)

        for field in feature_names:
            value = record.get(field)
            if value is None:
                null_counts[field] += 1
            elif isinstance(value, str) and not value.strip():
                blank_counts[field] += 1

        if record_type in {"chat_messages", "agentic_messages"}:
            messages = record.get("messages")
            if not isinstance(messages, list) or not messages:
                invalid_message_records += 1
                if len(invalid_examples) < 20:
                    invalid_examples.append(index)
                continue

            has_user = False
            has_assistant = False
            record_invalid = False
            for message in messages:
                message_count += 1
                if not isinstance(message, dict):
                    record_invalid = True
                    continue
                role = message.get("role")
                content = message.get("content")
                if not is_nonempty_string(role) or not isinstance(content, str):
                    record_invalid = True
                    continue
                role_counts[role.strip()] += 1
                message_content_chars += len(content)
                has_user = has_user or role.strip() == "user"
                has_assistant = has_assistant or role.strip() == "assistant"
                if not content.strip():
                    empty_messages += 1

            if not has_user:
                records_without_user += 1
            if not has_assistant:
                records_without_assistant += 1
            if record_invalid:
                invalid_message_records += 1
                if len(invalid_examples) < 20:
                    invalid_examples.append(index)

            if record_type == "agentic_messages":
                truth = record.get("ground_truth")
                if not is_nonempty_string(truth):
                    malformed_ground_truth += 1

        elif record_type == "knowledge_document":
            text = record.get("text")
            if isinstance(text, str):
                text_chars += len(text)
            source = record.get("source")
            if is_nonempty_string(source):
                source_counts[source.strip()] += 1

    report = {
        "split": split_name,
        "num_examples": total,
        "feature_names": feature_names,
        "feature_schema": str(dataset.features),
        "exact_duplicate_records": duplicate_count,
        "null_counts": dict(null_counts),
        "blank_string_counts": dict(blank_counts),
        "record_validation": {
            "invalid_message_records": invalid_message_records,
            "records_without_user_message": records_without_user,
            "records_without_assistant_message": records_without_assistant,
            "empty_message_contents": empty_messages,
            "malformed_ground_truth": malformed_ground_truth,
            "message_count": message_count,
            "message_role_counts": dict(role_counts),
            "message_content_characters": message_content_chars,
            "knowledge_text_characters": text_chars,
            "distinct_source_values": len(source_counts),
            "top_source_values": source_counts.most_common(20),
            "invalid_record_indices_sample": invalid_examples
        }
    }
    return report, hashes


def audit_dataset(entry: dict[str, Any], revision: str, cache_dir: str | None) -> dict[str, Any]:
    repo_id = entry["hub_repo"]
    logging.info("Loading %s (%s)", entry["id"], repo_id)
    dataset_dict = load_dataset(repo_id, revision=revision, cache_dir=cache_dir)

    split_reports: dict[str, Any] = {}
    split_hashes: dict[str, set[str]] = {}
    for split_name, split_data in dataset_dict.items():
        report, hashes = audit_split(split_data, split_name, entry["record_type"])
        split_reports[split_name] = report
        split_hashes[split_name] = hashes

    leakage: dict[str, int] = {}
    if "train" in split_hashes:
        for other_split, other_hashes in split_hashes.items():
            if other_split != "train":
                leakage[f"train_vs_{other_split}_exact_overlap"] = len(
                    split_hashes["train"].intersection(other_hashes)
                )

    return {
        "id": entry["id"],
        "name": entry["name"],
        "hub_repo": repo_id,
        "revision": revision,
        "record_type": entry["record_type"],
        "intended_use": entry.get("intended_use", []),
        "splits": split_reports,
        "exact_split_overlap": leakage
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--dataset", action="append", help="Dataset ID such as D01; repeat to select several.")
    parser.add_argument("--revision", default="main", help="Pinned Hub branch, tag or commit. Use a commit SHA for a release audit.")
    parser.add_argument("--cache-dir", default=None)
    parser.add_argument("--output", type=Path, default=ROOT / "reports" / "audit-latest.json")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level), format="%(levelname)s: %(message)s")

    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    entries = registry["datasets"]
    selected = set(args.dataset or [entry["id"] for entry in entries])
    unknown = selected.difference(entry["id"] for entry in entries)
    if unknown:
        raise SystemExit(f"Unknown dataset IDs: {sorted(unknown)}")

    results = []
    failures = []
    for entry in entries:
        if entry["id"] not in selected:
            continue
        try:
            results.append(audit_dataset(entry, args.revision, args.cache_dir))
        except Exception as exc:  # Preserve the rest of the audit if one source fails.
            logging.exception("Audit failed for %s", entry["id"])
            failures.append({"id": entry["id"], "hub_repo": entry["hub_repo"], "error": str(exc)})

    output = {
        "project": "Trimorious",
        "audit_version": "1.0.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "registry": str(args.registry),
        "hub_revision": args.revision,
        "read_only": True,
        "datasets": results,
        "failures": failures
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
