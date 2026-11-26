from __future__ import annotations

import ast
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def test_registry_contains_d01_to_d10_once():
    registry = load_json("configs/dataset_registry.json")
    ids = [item["id"] for item in registry["datasets"]]
    assert ids == [f"D{i:02d}" for i in range(1, 11)]
    assert len(ids) == len(set(ids))


def test_existing_datasets_have_current_sources_and_record_types():
    registry = load_json("configs/dataset_registry.json")
    existing = [item for item in registry["datasets"] if item.get("status") == "existing_baseline"]
    assert [item["id"] for item in existing] == ["D01", "D02", "D03", "D04"]
    for item in existing:
        assert item.get("hub_repo")
        assert item.get("github_mirror")
        assert item.get("record_type")
        assert (ROOT / item["current_schema"]).is_file()
        assert (ROOT / item["target_schema"]).is_file()


def test_proposed_datasets_are_not_misrepresented_as_created():
    registry = load_json("configs/dataset_registry.json")
    proposed = [item for item in registry["datasets"] if item.get("status") == "proposed"]
    assert [item["id"] for item in proposed] == ["D05", "D06", "D07", "D08", "D09", "D10"]
    for item in proposed:
        assert item.get("hub_repo") is None
        assert item.get("github_mirror") is None
        assert (ROOT / item["target_schema"]).is_file()


def test_all_current_and_target_schemas_are_valid_json_schema():
    registry = load_json("configs/dataset_registry.json")
    schema_paths = set()
    for item in registry["datasets"]:
        schema_paths.add(item.get("current_schema"))
        schema_paths.add(item.get("target_schema"))
    schema_paths.discard(None)

    for relative_path in schema_paths:
        schema = load_json(relative_path)
        Draft202012Validator.check_schema(schema)


def test_d07_is_explicitly_evaluation_only():
    registry = load_json("configs/dataset_registry.json")
    d07 = next(item for item in registry["datasets"] if item["id"] == "D07")
    assert d07["intended_use"] == ["held_out_evaluation_only"]
    schema = load_json(d07["target_schema"])
    split_policy = schema["properties"]["split_policy"]
    assert split_policy["properties"]["training_allowed"]["const"] is False


def test_audit_script_parses_and_defaults_to_existing_datasets():
    path = ROOT / "scripts" / "audit_datasets.py"
    ast.parse(path.read_text(encoding="utf-8"))
    content = path.read_text(encoding="utf-8")
    assert 'entry.get("status") == "existing_baseline"' in content
    assert 'selected = set(args.dataset or existing_ids)' in content
