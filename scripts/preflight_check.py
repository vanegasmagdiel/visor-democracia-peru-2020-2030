#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys
BASE = Path(__file__).resolve().parents[1]
required = [
    "app.py", "README.md", "CITATION.cff", ".zenodo.json", "codemeta.json", "datacite.json",
    "ro-crate-metadata.json", "LICENSE", "LICENSE_POLICY.md", "THIRD_PARTY_NOTICES.md",
    "data/LICENSE.md",
    "data/overall_multilevel_2020_2025.csv", "data/categories_multilevel_2020_2025.csv",
    "data/data_status_registry.csv", "data/model_config_v2_1.json",
    "data/peru_2025_anchor_ensemble.csv", "data/peru_2025_anchor_summary.csv",
    "data/parameter_elicitation_matrix.csv", "data/scenario_sensitivity_by_category.csv",
    "data/scenario_parameter_samples_summary.csv",
    "data/scenario_summary_2030.csv", "data/scenario_trajectories_2025_2030.csv",
    "data/base_integral_democracia_2020_2030_v2.xlsx", "docs/index.html",
    "data/data_dictionary.csv", "docs/PROVENANCE.md", "docs/DECISION_LOG.md",
    "docs/AUDIT_CLOSURE_PHASES_1_7.md", "docs/OSF_COMPLEMENT.md",
    "docs/FASE_8_PRISMA.md", "docs/FASE_8_GATE.md",
    "docs/INFORME_METODOLOGICO_PRISMA_FASE_8_CIERRE_FULLTEXT.md",
    "docs/assets/figura_s1_prisma_fulltext_final.png",
    "data/prisma_phase8/phase8_manifest.json",
    "data/prisma_phase8/Libro_Analisis_PRISMA_Visor_Democracia_R4_3_5_Cierre_Fulltext.xlsx",
    "data/prisma_phase8/Bibliografia_Incluida_Visor_Democracia_Fulltext_Final_29.ris",
    "data/prisma_phase8/fulltext_decisions_72.csv",
    "data/prisma_phase8/fulltext_included_29.csv",
    "data/prisma_phase8/fulltext_excluded_13.csv",
    "data/prisma_phase8/fulltext_not_retrieved_30.csv",
    "data/prisma_phase8/evidence_integration_map_29.csv",
    "requirements-lock.txt", "runtime-lock.json",
    "RELEASE_INDEPENDENCE_POLICY.md", "RELEASE_GATE_STATUS.json",
    "PUBLICAR_VISOR_V2_1_0.bat", "scripts/publish_release.ps1",
    "scripts/secret_scan.py", "scripts/sync_public_data.py", "scripts/validate_phase8.py",
    "scripts/check_windows_publisher.py", "scripts/audit_release_independence.py",
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
try:
    with open(BASE/"data/model_config_v2_1.json", encoding="utf-8") as f:
        config=json.load(f)
    if config.get("model_version") != "2.1.0":
        errors.append("model_config_v2_1.json must declare model_version 2.1.0")
    with open(BASE/"data/peru_2025_anchor_ensemble.csv", encoding="utf-8", newline="") as f:
        anchors=list(csv.DictReader(f))
    if len(anchors) != int(config.get("n_simulations", 0)):
        errors.append("anchor ensemble row count differs from model configuration")
    if any(abs(float(row["overall_score"])-5.88)>1e-9 for row in anchors):
        errors.append("anchor ensemble does not preserve the fixed 2025 aggregate")
    with open(BASE/"data/parameter_elicitation_matrix.csv", encoding="utf-8", newline="") as f:
        params=list(csv.DictReader(f))
    if len(params) != 30:
        errors.append("parameter elicitation matrix must contain 30 rows")
    if any(float(row["plausible_low"]) > float(row["central"]) or float(row["central"]) > float(row["plausible_high"]) for row in params):
        errors.append("parameter range invariant failed")
    with open(BASE/"data/data_dictionary.csv", encoding="utf-8", newline="") as f:
        dictionary=list(csv.DictReader(f))
    if not dictionary or any(not row.get("description", "").strip() for row in dictionary):
        errors.append("data dictionary contains an empty description")
    if "PublishRelease" not in (BASE/"scripts/publish_release.ps1").read_text(encoding="utf-8"):
        errors.append("publisher lacks the explicit final-release gate")
    import importlib.util
    phase8_script = BASE/"scripts/validate_phase8.py"
    spec = importlib.util.spec_from_file_location("validate_phase8", phase8_script)
    phase8 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(phase8)
    phase8_result = phase8.validate()
    if phase8_result["status"] != "PASS":
        errors.extend(f"phase8: {item}" for item in phase8_result["errors"])
    publisher_script = BASE/"scripts/check_windows_publisher.py"
    publisher_spec = importlib.util.spec_from_file_location("check_windows_publisher", publisher_script)
    publisher_module = importlib.util.module_from_spec(publisher_spec)
    publisher_spec.loader.exec_module(publisher_module)
    errors.extend(f"publisher: {item}" for item in publisher_module.validate())
    independence_script = BASE/"scripts/audit_release_independence.py"
    independence_spec = importlib.util.spec_from_file_location("audit_release_independence", independence_script)
    independence_module = importlib.util.module_from_spec(independence_spec)
    independence_spec.loader.exec_module(independence_module)
    errors.extend(f"independence: {item}" for item in independence_module.audit())
except Exception as e:
    errors.append(f"v2.1.0 scientific preflight failed: {e}")
if errors:
    print("PREFLIGHT FAIL")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print("PREFLIGHT OK")
