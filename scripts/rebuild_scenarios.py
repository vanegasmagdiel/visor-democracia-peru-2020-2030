#!/usr/bin/env python3
"""Rebuild deterministic scenario trajectories and Monte Carlo sensitivity bands.

This script intentionally does NOT regenerate the XLSX workbook; the workbook is a
release artifact. It reproduces the computational scenario layer from the auditable
CSV inputs in data/.
"""
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
D = BASE / "data"
SEED = 20260819
N = 10_000
DECAY = {2027: 1.0, 2028: 0.9, 2029: 0.8, 2030: 0.7}

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


def main() -> None:
    calibration = pd.read_csv(D / "peru_2025_category_calibration_audit.csv")
    anchor = calibration.set_index("category_full")["peru_2025_modeled_anchor"].reindex(CATS).astype(float)
    assert abs(anchor.mean() - 5.88) < 1e-12

    coeff = pd.read_csv(D / "scenario_coefficients.csv")
    meta = pd.read_csv(D / "scenario_summary_2030.csv").set_index("scenario_id")
    scenario_ids = list(meta.index)

    rows = []
    for sid in scenario_ids:
        c = coeff[coeff.scenario_id == sid].set_index("category_full").reindex(CATS)
        shock = c["shock_2026"].to_numpy(float)
        growth = c["annual_structural_rate"].to_numpy(float)
        current = anchor.to_numpy(float).copy()
        vals = {ES[k]: round(float(v), 3) for k, v in zip(CATS, current)}
        rows.append({"scenario_id": sid, "scenario_name": meta.loc[sid, "scenario_name"], "year": 2025,
                     **vals, "overall_score": round(float(current.mean()), 3),
                     "phase": "anchor_observed_overall_modeled_categories", "regime_type": regime(float(current.mean()))})
        current = np.clip(current + shock, 0, 10)
        vals = {ES[k]: round(float(v), 3) for k, v in zip(CATS, current)}
        rows.append({"scenario_id": sid, "scenario_name": meta.loc[sid, "scenario_name"], "year": 2026,
                     **vals, "overall_score": round(float(current.mean()), 3),
                     "phase": "post_election_shock", "regime_type": regime(float(current.mean()))})
        for year, decay in DECAY.items():
            current = np.clip(current + growth * decay, 0, 10)
            vals = {ES[k]: round(float(v), 3) for k, v in zip(CATS, current)}
            rows.append({"scenario_id": sid, "scenario_name": meta.loc[sid, "scenario_name"], "year": year,
                         **vals, "overall_score": round(float(current.mean()), 3),
                         "phase": "structural_projection", "regime_type": regime(float(current.mean()))})
    proj = pd.DataFrame(rows)
    proj.to_csv(D / "scenario_trajectories_2025_2030.csv", index=False)

    cats = pd.read_csv(D / "categories_multilevel_2020_2025.csv")
    hist = cats[cats.year <= 2024].pivot(index="year", columns="category_full", values="peru_score").reindex(columns=CATS)
    sigma = (hist.diff().dropna().std(ddof=1) * 0.25).clip(lower=0.04, upper=0.20)
    rng = np.random.default_rng(SEED)
    sigma_mult = {"recuperacion_institucional": 0.80, "continuidad_hibrida": 1.00, "deriva_restrictiva": 1.25}
    bands = []
    for sid in scenario_ids:
        c = coeff[coeff.scenario_id == sid].set_index("category_full").reindex(CATS)
        shock = c["shock_2026"].to_numpy(float)
        growth = c["annual_structural_rate"].to_numpy(float)
        arr = np.tile(anchor.to_numpy(float), (N, 1))
        ov = arr.mean(axis=1)
        bands.append([sid, 2025, *np.quantile(ov, [0.10, 0.50, 0.90]), N])
        arr = np.clip(arr + shock + rng.normal(0, sigma.to_numpy() * sigma_mult[sid], size=(N, 5)), 0, 10)
        ov = arr.mean(axis=1)
        bands.append([sid, 2026, *np.quantile(ov, [0.10, 0.50, 0.90]), N])
        for year, decay in DECAY.items():
            arr = np.clip(arr + growth * decay + rng.normal(0, sigma.to_numpy() * sigma_mult[sid] * 0.85, size=(N, 5)), 0, 10)
            ov = arr.mean(axis=1)
            bands.append([sid, year, *np.quantile(ov, [0.10, 0.50, 0.90]), N])
    b = pd.DataFrame(bands, columns=["scenario_id", "year", "p10", "p50", "p90", "n_sim"])
    b[["p10", "p50", "p90"]] = b[["p10", "p50", "p90"]].round(3)
    b["note"] = "Sensitivity envelope from 10,000 Monte Carlo paths using 25% of historical annual category volatility (floored/capped); not a statistical confidence interval."
    b.to_csv(D / "scenario_sensitivity_bands.csv", index=False)

    summary = pd.read_csv(D / "scenario_summary_2030.csv")
    for i, row in summary.iterrows():
        sid = row.scenario_id
        summary.loc[i, "score_2026"] = float(proj[(proj.scenario_id == sid) & (proj.year == 2026)].overall_score.iloc[0])
        s2030 = float(proj[(proj.scenario_id == sid) & (proj.year == 2030)].overall_score.iloc[0])
        summary.loc[i, "score_2030"] = s2030
        summary.loc[i, "regime_2030"] = regime(s2030)
    summary.to_csv(D / "scenario_summary_2030.csv", index=False)
    print("Rebuilt trajectories, sensitivity bands and 2030 summary.")


if __name__ == "__main__":
    main()
