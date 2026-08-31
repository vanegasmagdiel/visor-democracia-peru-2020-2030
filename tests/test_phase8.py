from pathlib import Path
import importlib.util


BASE = Path(__file__).resolve().parents[1]


def _module():
    path = BASE / "scripts" / "validate_phase8.py"
    spec = importlib.util.spec_from_file_location("validate_phase8", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_phase8_snapshot_is_consistent():
    result = _module().validate()
    assert result["status"] == "PASS", result["errors"]


def test_phase8_gate_is_open_for_phases_9_to_11():
    result = _module().validate()
    counts = result["verified_counts"]
    assert counts["reports_retrieved"] == 42
    assert counts["reports_assessed"] == 42
    assert counts["fulltext_excluded"] == 13
    assert counts["final_included"] == 29
    assert counts["not_retrieved"] == 30
