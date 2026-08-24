#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys
BASE = Path(__file__).resolve().parents[1]
required = [
    "app.py", "README.md", "CITATION.cff", ".zenodo.json", "codemeta.json", "datacite.json",
    "ro-crate-metadata.json", "LICENSE", "LICENSE_POLICY.md", "THIRD_PARTY_NOTICES.md",
    "data/LICENSE.md",
    "data/overall_multilevel_2020_2025.csv", "data/categories_multilevel_2020_2025.csv",
    "data/scenario_summary_2030.csv", "data/scenario_trajectories_2025_2030.csv",
    "data/base_integral_democracia_2020_2030_v2.xlsx", "docs/index.html",
]
errors=[]
for item in required:
    p=BASE/item
    if not p.exists() or p.stat().st_size == 0:
        errors.append(f"missing/empty: {item}")
if not (BASE/"docs/.nojekyll").is_file():
    errors.append("missing: docs/.nojekyll")
with open(BASE/"data/scenario_summary_2030.csv", encoding="utf-8", newline="") as f:
    rows=list(csv.DictReader(f))
if len(rows)!=3:
    errors.append("scenario_summary_2030.csv must contain exactly 3 rows")
try:
    vals={r["scenario_id"]:float(r["score_2030"]) for r in rows}
    if not (vals["recuperacion_institucional"] > vals["continuidad_hibrida"] > vals["deriva_restrictiva"]):
        errors.append("2030 scenario ordering invariant failed")
except Exception as e:
    errors.append(f"scenario parsing failed: {e}")
if errors:
    print("PREFLIGHT FAIL")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print("PREFLIGHT OK")
