#!/usr/bin/env python3
"""Rebuild the v2.1.0 scenario layer and epistemic sensitivity outputs.

The model keeps Peru's 2025 aggregate fixed at 5.88 while representing its
unpublished dimensional composition as an ensemble. Scenario parameters are
bounded structured analytical judgements, not statistically estimated effects.
The same random draws are reused across scenarios for comparability.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


BASE = Path(__file__).resolve().parents[1]
D = BASE / "data"
CATS = [
    "Electoral process and pluralism",
    "Functioning of government",
    "Political participation",
    "Political culture",
    "Civil liberties",
]
ES = {
    "Electoral process and pluralism": "Proceso electoral y pluralismo",
    "Functioning of government": "Funcionamiento del gobierno",
    "Political participation": "Participación política",
    "Political culture": "Cultura política",
    "Civil liberties": "Libertades civiles",
}


def regime(score: float) -> str:
    if score <= 4:
        return "Authoritarian regime"
    if score <= 6:
        return "Hybrid regime"
    if score <= 8:
        return "Flawed democracy"
    return "Full democracy"


def triangular_ppf(u: np.ndarray, left: np.ndarray, mode: np.ndarray, right: np.ndarray) -> np.ndarray:
    """Inverse CDF of a triangular distribution with broadcastable arrays."""
    width = right - left
    c = np.divide(mode - left, width, out=np.full_like(width, 0.5, dtype=float), where=width > 0)
    left_branch = left + np.sqrt(u * width * (mode - left))
    right_branch = right - np.sqrt((1.0 - u) * width * (right - mode))
    return np.where(u < c, left_branch, right_branch)


def historical_matrix() -> pd.DataFrame:
    cats = pd.read_csv(D / "categories_multilevel_2020_2025.csv")
    return (
        cats[cats.year <= 2024]
        .pivot(index="year", columns="category_full", values="peru_score")
        .reindex(columns=CATS)
        .astype(float)
    )


def build_anchor_ensemble(config: dict, rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    audit = pd.read_csv(D / "peru_2025_category_calibration_audit.csv")
    central = audit.set_index("category_full")["peru_2025_modeled_anchor"].reindex(CATS).astype(float)
    target = float(config["overall_2025"])
    if not np.isclose(central.mean(), target, atol=1e-12):
        raise ValueError("The documented central anchor does not average to the 2025 aggregate.")

    hist = historical_matrix()
    rule = config["anchor_uncertainty"]
    sigma = (hist.diff().dropna().std(ddof=1) * float(rule["historical_volatility_multiplier"])).clip(
        lower=float(rule["sigma_floor"]), upper=float(rule["sigma_cap"])
    )
    bounds = float(rule["bound_sigma_multiplier"])
    lower = np.maximum(0.0, central.to_numpy() - bounds * sigma.to_numpy())
    upper = np.minimum(10.0, central.to_numpy() + bounds * sigma.to_numpy())
    n = int(config["n_simulations"])

    accepted: list[np.ndarray] = []
    accepted_count = 0
    while accepted_count < n:
        batch_n = max(2000, (n - accepted_count) * 2)
        raw = rng.normal(0.0, sigma.to_numpy(), size=(batch_n, len(CATS)))
        raw -= raw.mean(axis=1, keepdims=True)
        candidate = central.to_numpy() + raw
        keep = ((candidate >= lower) & (candidate <= upper)).all(axis=1)
        if keep.any():
            block = candidate[keep]
            accepted.append(block)
            accepted_count += len(block)
    arr = np.vstack(accepted)[:n]
    if not np.allclose(arr.mean(axis=1), target, atol=1e-12):
        raise AssertionError("Anchor ensemble does not preserve the fixed 2025 aggregate.")

    ensemble = pd.DataFrame(arr, columns=[ES[c] for c in CATS])
    ensemble.insert(0, "sample_id", np.arange(1, n + 1))
    ensemble["overall_score"] = arr.mean(axis=1)
    ensemble["data_status"] = "modeled_latent_ensemble"

    summary_rows = []
    hist_2024 = hist.loc[2024]
    for i, cat in enumerate(CATS):
        q10, q50, q90 = np.quantile(arr[:, i], [0.10, 0.50, 0.90])
        summary_rows.append(
            {
                "category_full": cat,
                "category_es": ES[cat],
                "peru_2024_official_source_observed": round(float(hist_2024[cat]), 4),
                "central_anchor_2025": round(float(central[cat]), 4),
                "anchor_sigma": round(float(sigma[cat]), 4),
                "admissible_low": round(float(lower[i]), 4),
                "p10": round(float(q10), 4),
                "p50": round(float(q50), 4),
                "p90": round(float(q90), 4),
                "admissible_high": round(float(upper[i]), 4),
                "overall_constraint": target,
                "data_status": "modeled_latent_ensemble",
                "interpretation": "Uncertainty in dimensional composition; not an official EIU Peru sub-score.",
            }
        )
    return ensemble, pd.DataFrame(summary_rows)


def parameter_arrays(matrix: pd.DataFrame, scenario_id: str, parameter: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rows = (
        matrix[(matrix.scenario_id == scenario_id) & (matrix.parameter == parameter)]
        .set_index("category_full")
        .reindex(CATS)
    )
    if rows[["central", "plausible_low", "plausible_high"]].isna().any().any():
        raise ValueError(f"Incomplete parameter matrix for {scenario_id}/{parameter}")
    return (
        rows["plausible_low"].to_numpy(float),
        rows["central"].to_numpy(float),
        rows["plausible_high"].to_numpy(float),
    )


def build_outputs(config: dict, ensemble: pd.DataFrame) -> None:
    n = int(config["n_simulations"])
    seed = int(config["seed"])
    rng = np.random.default_rng(seed + 1)
    parameter_matrix = pd.read_csv(D / "parameter_elicitation_matrix.csv")
    scenario_meta = pd.read_csv(D / "scenario_summary_2030.csv").set_index("scenario_id")
    scenario_ids = list(scenario_meta.index)
    decay = {int(year): float(value) for year, value in config["decay"].items()}
    anchor_arr = ensemble[[ES[c] for c in CATS]].to_numpy(float)

    # Common random numbers improve cross-scenario comparability.
    u_shock = rng.random((n, len(CATS)))
    u_rate = rng.random((n, len(CATS)))
    u_scale = rng.random(n)
    u_rho = rng.random(n)
    years_noise = [2026, *decay.keys()]
    common_z = {year: rng.normal(size=(n, 1)) for year in years_noise}
    idio_z = {year: rng.normal(size=(n, len(CATS))) for year in years_noise}

    scale_cfg = config["structural_rate_scale"]
    rate_scale = triangular_ppf(
        u_scale,
        np.full(n, float(scale_cfg["low"])),
        np.full(n, float(scale_cfg["mode"])),
        np.full(n, float(scale_cfg["high"])),
    )
    residual_cfg = config["residual_uncertainty"]
    rho = triangular_ppf(
        u_rho,
        np.full(n, float(residual_cfg["rho_low"])),
        np.full(n, float(residual_cfg["rho_mode"])),
        np.full(n, float(residual_cfg["rho_high"])),
    )
    hist = historical_matrix()
    residual_sigma = (
        hist.diff().dropna().std(ddof=1) * float(residual_cfg["historical_volatility_multiplier"])
    ).clip(lower=float(residual_cfg["sigma_floor"]), upper=float(residual_cfg["sigma_cap"]))

    def residual(year: int) -> np.ndarray:
        correlated = np.sqrt(rho)[:, None] * common_z[year] + np.sqrt(1.0 - rho)[:, None] * idio_z[year]
        return correlated * residual_sigma.to_numpy()[None, :]

    deterministic_rows = []
    band_rows = []
    category_band_rows = []
    parameter_summary_rows = []
    central_anchor = (
        pd.read_csv(D / "peru_2025_category_calibration_audit.csv")
        .set_index("category_full")["peru_2025_modeled_anchor"]
        .reindex(CATS)
        .to_numpy(float)
    )

    for sid in scenario_ids:
        shock_low, shock_central, shock_high = parameter_arrays(parameter_matrix, sid, "shock_2026")
        rate_low, rate_central, rate_high = parameter_arrays(parameter_matrix, sid, "annual_structural_rate")
        shock_draws = triangular_ppf(u_shock, shock_low, shock_central, shock_high)
        rate_draws = triangular_ppf(u_rate, rate_low, rate_central, rate_high)

        for parameter, draws in (("shock_2026", shock_draws), ("annual_structural_rate", rate_draws)):
            for i, cat in enumerate(CATS):
                q10, q50, q90 = np.quantile(draws[:, i], [0.10, 0.50, 0.90])
                parameter_summary_rows.append(
                    {
                        "scenario_id": sid,
                        "category_full": cat,
                        "category_es": ES[cat],
                        "parameter": parameter,
                        "p10": round(float(q10), 5),
                        "p50": round(float(q50), 5),
                        "p90": round(float(q90), 5),
                        "n_sim": n,
                    }
                )

        current_c = central_anchor.copy()
        central_by_year = {2025: current_c.copy()}
        current_c = np.clip(current_c + shock_central, 0, 10)
        central_by_year[2026] = current_c.copy()
        for year, decay_value in decay.items():
            current_c = np.clip(current_c + rate_central * decay_value, 0, 10)
            central_by_year[year] = current_c.copy()

        for year, values in central_by_year.items():
            deterministic_rows.append(
                {
                    "scenario_id": sid,
                    "scenario_name": scenario_meta.loc[sid, "scenario_name"],
                    "year": year,
                    **{ES[cat]: round(float(value), 3) for cat, value in zip(CATS, values)},
                    "overall_score": round(float(values.mean()), 3),
                    "phase": "modeled_latent_central" if year == 2025 else ("post_election_shock" if year == 2026 else "structural_projection"),
                    "data_status": "modeled_latent_central" if year == 2025 else "simulated_scenario",
                    "regime_type": regime(float(values.mean())),
                }
            )

        current = anchor_arr.copy()
        simulation_by_year = {2025: current.copy()}
        current = np.clip(current + shock_draws + residual(2026), 0, 10)
        simulation_by_year[2026] = current.copy()
        for year, decay_value in decay.items():
            current = np.clip(
                current + rate_draws * decay_value * rate_scale[:, None] + residual(year), 0, 10
            )
            simulation_by_year[year] = current.copy()

        for year, values in simulation_by_year.items():
            overall = values.mean(axis=1)
            q10, q50, q90 = np.quantile(overall, [0.10, 0.50, 0.90])
            band_rows.append(
                {
                    "scenario_id": sid,
                    "year": year,
                    "p10": round(float(q10), 3),
                    "p50": round(float(q50), 3),
                    "p90": round(float(q90), 3),
                    "n_sim": n,
                    "uncertainty_layers": "2025 dimensional composition; bounded scenario parameters; structural-rate scale; correlated residual perturbation",
                    "note": "Sensitivity envelope; not a confidence interval and not a scenario-occurrence probability.",
                }
            )
            for i, cat in enumerate(CATS):
                cq10, cq50, cq90 = np.quantile(values[:, i], [0.10, 0.50, 0.90])
                category_band_rows.append(
                    {
                        "scenario_id": sid,
                        "year": year,
                        "category_full": cat,
                        "category_es": ES[cat],
                        "p10": round(float(cq10), 3),
                        "p50": round(float(cq50), 3),
                        "p90": round(float(cq90), 3),
                        "n_sim": n,
                    }
                )

    trajectories = pd.DataFrame(deterministic_rows)
    bands = pd.DataFrame(band_rows)
    category_bands = pd.DataFrame(category_band_rows)
    parameter_summary = pd.DataFrame(parameter_summary_rows)
    trajectories.to_csv(D / "scenario_trajectories_2025_2030.csv", index=False)
    bands.to_csv(D / "scenario_sensitivity_bands.csv", index=False)
    category_bands.to_csv(D / "scenario_sensitivity_by_category.csv", index=False)
    parameter_summary.to_csv(D / "scenario_parameter_samples_summary.csv", index=False)

    summary = scenario_meta.reset_index()
    for i, row in summary.iterrows():
        sid = row.scenario_id
        central_2026 = trajectories[(trajectories.scenario_id == sid) & (trajectories.year == 2026)].iloc[0]
        central_2030 = trajectories[(trajectories.scenario_id == sid) & (trajectories.year == 2030)].iloc[0]
        band_2030 = bands[(bands.scenario_id == sid) & (bands.year == 2030)].iloc[0]
        summary.loc[i, "score_2026"] = central_2026.overall_score
        summary.loc[i, "score_2030"] = central_2030.overall_score
        summary.loc[i, "p10_2030"] = band_2030.p10
        summary.loc[i, "p50_2030"] = band_2030.p50
        summary.loc[i, "p90_2030"] = band_2030.p90
        summary.loc[i, "regime_2030"] = regime(float(central_2030.overall_score))
        summary.loc[i, "classification_basis"] = "central deterministic trajectory"
    summary.to_csv(D / "scenario_summary_2030.csv", index=False)


def write_compatibility_coefficients() -> None:
    matrix = pd.read_csv(D / "parameter_elicitation_matrix.csv")
    pivot = matrix.pivot_table(
        index=["scenario_id", "scenario_name", "category_full", "category_es"],
        columns="parameter",
        values="central",
        aggfunc="first",
    ).reset_index()
    evidence = (
        matrix.groupby(["scenario_id", "category_full"], as_index=False)["evidence_basis"]
        .agg(lambda values: ";".join(dict.fromkeys(";".join(values).split(";"))))
    )
    pivot = pivot.merge(evidence, on=["scenario_id", "category_full"], how="left")
    pivot.to_csv(D / "scenario_coefficients.csv", index=False)


def main() -> None:
    config = json.loads((D / "model_config_v2_1.json").read_text(encoding="utf-8"))
    rng = np.random.default_rng(int(config["seed"]))
    ensemble, anchor_summary = build_anchor_ensemble(config, rng)
    ensemble.to_csv(D / "peru_2025_anchor_ensemble.csv", index=False)
    anchor_summary.to_csv(D / "peru_2025_anchor_summary.csv", index=False)
    build_outputs(config, ensemble)
    write_compatibility_coefficients()
    print("Rebuilt v2.1.0 anchors, trajectories and sensitivity outputs.")


if __name__ == "__main__":
    main()
