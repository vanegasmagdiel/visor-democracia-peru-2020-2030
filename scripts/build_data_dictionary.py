#!/usr/bin/env python3
"""Regenerate the field-level dictionary for every public CSV data product."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
OUTPUT = DATA / "data_dictionary.csv"

DESCRIPTIONS = {
    "scenario_id": "Stable machine-readable scenario identifier.",
    "scenario_name": "Human-readable scenario name.",
    "year": "Calendar or analytical year.",
    "peru_score": "Peru score on the 0–10 Democracy Index scale; interpret with its data-status field.",
    "latin_america_score": "Latin America and Caribbean aggregate on the 0–10 scale.",
    "world_score": "World aggregate on the 0–10 scale.",
    "overall_score": "Arithmetic mean of the five dimensional values on the 0–10 scale.",
    "data_status": "Controlled epistemic-status identifier from data_status_registry.csv.",
    "data_status_peru": "Epistemic status of the Peru value.",
    "data_status_latam": "Epistemic status of the Latin America value.",
    "data_status_world": "Epistemic status of the world value.",
    "sample_id": "Deterministic simulation-row identifier.",
    "p10": "10th percentile of the stated sensitivity distribution.",
    "p50": "Median of the stated sensitivity distribution.",
    "p90": "90th percentile of the stated sensitivity distribution.",
    "n_sim": "Number of Monte Carlo sensitivity draws.",
    "central": "Central structured analytical judgement for the parameter.",
    "plausible_low": "Lower plausible bound used by the triangular parameter distribution.",
    "plausible_high": "Upper plausible bound used by the triangular parameter distribution.",
    "evidence_basis": "Semicolon-separated evidence identifiers supporting the judgement.",
    "translation_rule": "Explicit rule translating qualitative evidence into a bounded parameter judgement.",
    "source_priority": "Categorical source-priority label; never a numeric model weight.",
    "computational_use": "Whether the evidence record is directly used as a numeric coefficient.",
    "overall_constraint": "Fixed 2025 aggregate that every latent dimensional vector must preserve.",
    "interpretation": "Mandatory interpretive limitation for the value or distribution.",
    "uncertainty_layers": "Uncertainty components jointly propagated in the sensitivity exercise.",
    "note": "Interpretive note, including limits on probabilistic claims.",
    "parameter_status": "Epistemic classification of the parameter.",
    "decision_author": "Person responsible for the documented analytical judgement.",
    "decision_date": "ISO date of the analytical judgement.",
    "url": "Source URL.",
    "formula": "Human-readable model formula.",
    "formula_id": "Stable formula identifier.",
    "status_id": "Stable controlled-vocabulary identifier.",
    "definition": "Definition of the controlled data status.",
    "allowed_use": "Permitted interpretation and citation use.",
}


def describe(field: str) -> str:
    if field in DESCRIPTIONS:
        return DESCRIPTIONS[field]
    if field.endswith("_score"):
        return "Score on the 0–10 Democracy Index scale."
    if field.startswith("source_"):
        return "Bibliographic source and location for the corresponding value."
    if field.startswith("peru_minus_") or field == "latam_minus_world":
        return "Arithmetic score difference between the named geographies."
    if field.endswith("pct_change_vs_2020"):
        return "Percentage change relative to the 2020 baseline."
    if field in {"Proceso electoral y pluralismo", "Funcionamiento del gobierno", "Participación política", "Cultura política", "Libertades civiles"}:
        return "Dimensional score on the 0–10 scale; interpret with data_status."
    return field.replace("_", " ").capitalize() + "."


def main() -> None:
    rows: list[dict[str, str]] = []
    for path in sorted(DATA.glob("*.csv")):
        if path.name == OUTPUT.name:
            continue
        frame = pd.read_csv(path, nrows=200)
        for field, dtype in frame.dtypes.items():
            rows.append(
                {
                    "file": path.name,
                    "field": field,
                    "dtype": str(dtype),
                    "description": describe(field),
                }
            )
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["file", "field", "dtype", "description"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"WROTE {OUTPUT.relative_to(BASE)} ({len(rows)} fields)")


if __name__ == "__main__":
    main()
