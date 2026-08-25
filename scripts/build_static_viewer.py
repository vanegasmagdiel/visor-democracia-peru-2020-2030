#!/usr/bin/env python3
"""Build the self-contained GitHub Pages viewer from v2.1.0 CSV outputs."""

from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.offline import get_plotlyjs


BASE = Path(__file__).resolve().parents[1]
D = BASE / "data"
OUT = BASE / "docs" / "index.html"
COLORS = {
    "recuperacion_institucional": "#26734d",
    "continuidad_hibrida": "#24518a",
    "deriva_restrictiva": "#a93232",
}
FILLS = {
    "recuperacion_institucional": "rgba(38,115,77,0.14)",
    "continuidad_hibrida": "rgba(36,81,138,0.14)",
    "deriva_restrictiva": "rgba(169,50,50,0.14)",
}


def chart_html(fig: go.Figure, div_id: str) -> str:
    return fig.to_html(full_html=False, include_plotlyjs=False, div_id=div_id, config={"responsive": True})


def history_chart(overall: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for col, name, color in (
        ("peru_score", "Perú", "#24518a"),
        ("latin_america_score", "América Latina y el Caribe", "#2f7d50"),
        ("world_score", "Mundo", "#a66b18"),
    ):
        fig.add_trace(go.Scatter(x=overall.year, y=overall[col], mode="lines+markers", name=name, line={"width": 3, "color": color}, marker={"size": 8}))
    fig.add_hline(y=6, line_dash="dot", line_color="#6b7280", annotation_text="Umbral 6,0")
    fig.update_layout(template="plotly_white", height=460, margin={"l": 55, "r": 25, "t": 25, "b": 50}, yaxis={"range": [4.8, 6.8], "title": "Puntaje 0–10"}, xaxis_title="Año", legend={"orientation": "h", "y": 1.08})
    return fig


def anchor_chart(anchor: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=anchor.category_es, y=anchor.peru_2024_official_source_observed, mode="markers", name="2024 observado", marker={"size": 13, "color": "#24518a", "symbol": "circle"}))
    fig.add_trace(go.Scatter(x=anchor.category_es, y=anchor.p50, mode="markers", name="2025 ancla latente", marker={"size": 14, "color": "#a66b18", "symbol": "diamond-open", "line": {"width": 3}}, error_y={"type": "data", "symmetric": False, "array": anchor.p90-anchor.p50, "arrayminus": anchor.p50-anchor.p10, "color": "#a66b18", "thickness": 2}))
    fig.update_layout(template="plotly_white", height=480, margin={"l": 50, "r": 25, "t": 25, "b": 120}, yaxis={"range": [0, 10], "title": "Puntaje 0–10"}, legend={"orientation": "h", "y": 1.08})
    return fig


def scenario_chart(bands: pd.DataFrame, summary: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    names = summary.set_index("scenario_id").scenario_name.to_dict()
    for sid, name in names.items():
        d = bands[bands.scenario_id == sid].sort_values("year")
        fig.add_trace(go.Scatter(x=list(d.year)+list(d.year[::-1]), y=list(d.p90)+list(d.p10[::-1]), fill="toself", fillcolor=FILLS[sid], line={"color": "rgba(255,255,255,0)"}, hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(x=d.year, y=d.p50, mode="lines+markers", name=name, line={"width": 3, "color": COLORS[sid]}, marker={"size": 8}, hovertemplate=f"<b>{escape(name)}</b><br>Año: %{{x}}<br>p50: %{{y:.2f}}<extra></extra>"))
    fig.add_hline(y=6, line_dash="dot", line_color="#6b7280", annotation_text="Umbral 6,0")
    fig.update_layout(template="plotly_white", height=510, margin={"l": 55, "r": 25, "t": 25, "b": 55}, yaxis={"range": [4.9, 6.6], "title": "Puntaje 0–10"}, xaxis_title="Año", legend={"orientation": "h", "y": 1.15})
    return fig


def main() -> None:
    overall = pd.read_csv(D / "overall_multilevel_2020_2025.csv")
    anchor = pd.read_csv(D / "peru_2025_anchor_summary.csv")
    bands = pd.read_csv(D / "scenario_sensitivity_bands.csv")
    summary = pd.read_csv(D / "scenario_summary_2030.csv")
    latest = overall.iloc[-1]

    summary_rows = "".join(
        f"<tr><td>{escape(row.scenario_name)}</td><td>{row.score_2030:.3f}</td><td>{row.p10_2030:.3f}–{row.p90_2030:.3f}</td><td>{escape(row.regime_2030)}</td></tr>"
        for _, row in summary.iterrows()
    )
    html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Visor Democracia Perú 2020–2030 · v2.1.0</title>
<script>{get_plotlyjs()}</script>
<style>
:root{{--bg:#f2f6fb;--card:#fff;--line:#dbe4ee;--ink:#14253a;--muted:#63758a;--accent:#173f70}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font-family:Segoe UI,Arial,sans-serif}}
.wrap{{max-width:1440px;margin:auto;padding:28px}} .hero{{background:linear-gradient(135deg,#173f70,#356caa);color:white;border-radius:24px;padding:34px 38px}}
.hero h1{{font-size:2rem;margin:0 0 10px}} .hero p{{max-width:1100px;line-height:1.55;margin:0;color:#eef5fc}}
.meta{{font-size:.82rem;margin-top:14px;color:#dbeafe}} .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:18px 0}}
.kpi,.card{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px 20px}} .kpi .label{{color:var(--muted);font-size:.84rem}} .kpi .value{{font-size:1.5rem;font-weight:800}}
.card{{margin-bottom:18px}} .card h2{{font-size:1.15rem;margin:0 0 4px}} .note{{color:var(--muted);font-size:.9rem;line-height:1.5}}
.warn{{background:#fff7df;border:1px solid #ead59a;border-radius:14px;padding:13px 15px;margin:12px 0;line-height:1.5}}
table{{width:100%;border-collapse:collapse;margin-top:12px}} th,td{{padding:10px;border-bottom:1px solid var(--line);text-align:left}} th{{background:#1f2937;color:white}}
.footer{{font-size:.82rem;color:var(--muted);text-align:right;padding:12px 0}} a{{color:#24518a}} @media(max-width:900px){{.grid{{grid-template-columns:repeat(2,1fr)}}}} @media(max-width:560px){{.grid{{grid-template-columns:1fr}}.wrap{{padding:14px}}}}
</style></head><body><main class="wrap">
<section class="hero"><h1>Visor Integrado de Democracia del Perú 2020–2030</h1><p>Serie agregada 2020–2025 y tres escenarios exploratorios 2026–2030. La versión 2.1.0 distingue observación oficial, agregado reportado secundariamente, ancla dimensional latente y simulación.</p><div class="meta">Candidato científico v2.1.0 · corte de evidencia: 17-08-2026 · 10 000 simulaciones por escenario</div></section>
<section class="grid"><div class="kpi"><div class="label">Perú 2025</div><div class="value">{latest.peru_score:.2f}</div><div class="note">agregado reportado secundariamente</div></div><div class="kpi"><div class="label">Cambio 2024→2025</div><div class="value">+{latest.peru_score-overall.iloc[-2].peru_score:.2f}</div></div><div class="kpi"><div class="label">América Latina y Caribe</div><div class="value">{latest.latin_america_score:.2f}</div></div><div class="kpi"><div class="label">Mundo</div><div class="value">{latest.world_score:.2f}</div></div></section>
<section class="card"><h2>Trayectoria agregada</h2><div class="note">Los valores 2020–2024 proceden de ediciones EIU; el agregado peruano 2025 tiene estatus de reporte secundario.</div>{chart_html(history_chart(overall),'history')}</section>
<section class="card"><h2>Ancla dimensional de 2025</h2><div class="note">p50 y p10–p90 del conjunto de composiciones compatibles con el total 5,88. No son subpuntajes oficiales EIU.</div>{chart_html(anchor_chart(anchor),'anchor')}</section>
<section class="card"><h2>Escenarios 2026–2030</h2><div class="note">Línea = p50; franja = p10–p90. Son envolventes de sensibilidad, no intervalos de confianza ni probabilidades de escenario.</div>{chart_html(scenario_chart(bands,summary),'scenarios')}<table><thead><tr><th>Escenario</th><th>Central 2030</th><th>p10–p90</th><th>Clasificación de la central</th></tr></thead><tbody>{summary_rows}</tbody></table></section>
<div class="warn"><strong>Alcance:</strong> el visor mide calidad democrática mediante las dimensiones del <em>Democracy Index</em>. “Funcionamiento del gobierno” no se interpreta como medición directa de capacidad estatal. Los parámetros prospectivos son juicios analíticos estructurados y auditables.</div>
<footer class="footer">Magdiel Torres Vanegas · <a href="https://orcid.org/0000-0002-7913-214X">ORCID</a> · <a href="https://doi.org/10.5281/zenodo.22080540">DOI conceptual</a> · <a href="https://github.com/vanegasmagdiel/visor-democracia-peru-2020-2030">Repositorio</a></footer>
</main></body></html>"""
    html = "\n".join(line.rstrip() for line in html.splitlines()) + "\n"
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(BASE)}")


if __name__ == "__main__":
    main()
