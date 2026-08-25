import json
from pathlib import Path

import numpy as np
import pandas as pd


BASE = Path(__file__).resolve().parents[1]
D = BASE / "data"
SCENARIOS = {"recuperacion_institucional", "continuidad_hibrida", "deriva_restrictiva"}


def test_secondary_aggregate_and_latent_center_are_distinct():
    overall = pd.read_csv(D / "overall_multilevel_2020_2025.csv")
    categories = pd.read_csv(D / "categories_multilevel_2020_2025.csv")
    row = overall[overall.year == 2025].iloc[0]
    assert row.data_status_peru == "secondary_reported_aggregate"
    assert np.isclose(row.peru_score, 5.88)
    assert set(categories[categories.year == 2025].data_status_peru) == {"modeled_latent_central"}
    assert np.isclose(categories[categories.year == 2025].peru_score.mean(), 5.88)


def test_anchor_ensemble_preserves_fixed_aggregate():
    ensemble = pd.read_csv(D / "peru_2025_anchor_ensemble.csv")
    config = json.loads((D / "model_config_v2_1.json").read_text(encoding="utf-8"))
    assert len(ensemble) == config["n_simulations"] == 10_000
    assert np.allclose(ensemble.overall_score, 5.88, atol=1e-12)
    numeric = ensemble.drop(columns=["sample_id", "overall_score", "data_status"])
    assert ((numeric >= 0) & (numeric <= 10)).all().all()


def test_anchor_summary_intervals_are_ordered():
    summary = pd.read_csv(D / "peru_2025_anchor_summary.csv")
    assert len(summary) == 5
    assert (summary.admissible_low <= summary.p10).all()
    assert (summary.p10 <= summary.p50).all()
    assert (summary.p50 <= summary.p90).all()
    assert (summary.p90 <= summary.admissible_high).all()


def test_parameter_matrix_complete_and_bounded():
    matrix = pd.read_csv(D / "parameter_elicitation_matrix.csv")
    assert len(matrix) == 30
    assert set(matrix.scenario_id) == SCENARIOS
    assert set(matrix.parameter) == {"shock_2026", "annual_structural_rate"}
    assert (matrix.plausible_low <= matrix.central).all()
    assert (matrix.central <= matrix.plausible_high).all()
    assert matrix.evidence_basis.str.len().gt(0).all()
    assert matrix.translation_rule.str.len().gt(20).all()


def test_source_priority_is_not_a_computational_weight():
    evidence = pd.read_csv(D / "post_election_evidence_2026.csv")
    assert "weight" not in evidence.columns
    assert "source_priority" in evidence.columns
    assert set(evidence.computational_use.astype(str).str.lower()) == {"false"}


def test_three_scenarios_and_ordering():
    summary = pd.read_csv(D / "scenario_summary_2030.csv").set_index("scenario_id")
    assert set(summary.index) == SCENARIOS
    assert (
        summary.loc["recuperacion_institucional", "score_2030"]
        > summary.loc["continuidad_hibrida", "score_2030"]
        > summary.loc["deriva_restrictiva", "score_2030"]
    )


def test_sensitivity_outputs_are_valid():
    bands = pd.read_csv(D / "scenario_sensitivity_bands.csv")
    assert len(bands) == 18
    assert bands.p10.le(bands.p50).all() and bands.p50.le(bands.p90).all()
    assert bands[["p10", "p50", "p90"]].ge(0).all().all()
    assert bands[["p10", "p50", "p90"]].le(10).all().all()
    assert bands.note.str.contains("not a confidence interval", regex=False).all()
    start = bands[bands.year == 2025]
    assert np.allclose(start[["p10", "p50", "p90"]], 5.88)


def test_trajectory_status_and_ranges():
    trajectories = pd.read_csv(D / "scenario_trajectories_2025_2030.csv")
    assert trajectories.overall_score.between(0, 10).all()
    assert set(trajectories[trajectories.year == 2025].data_status) == {"modeled_latent_central"}
    assert set(trajectories[trajectories.year > 2025].data_status) == {"simulated_scenario"}
