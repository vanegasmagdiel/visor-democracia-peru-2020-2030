#!/usr/bin/env python3
"""Synchronize the small public download set consumed by GitHub Pages."""

from __future__ import annotations

import shutil
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
PUBLIC = BASE / "docs" / "data"
FILES = [
    "base_integral_democracia_2020_2030_v2.xlsx",
    "data_status_registry.csv",
    "overall_multilevel_2020_2025.csv",
    "peru_2025_anchor_summary.csv",
    "scenario_sensitivity_bands.csv",
    "scenario_trajectories_2025_2030.csv",
]


def main() -> None:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        shutil.copy2(BASE / "data" / name, PUBLIC / name)
    print(f"SYNCED {len(FILES)} public data products")


if __name__ == "__main__":
    main()
