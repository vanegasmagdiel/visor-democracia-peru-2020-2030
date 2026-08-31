"""Build the final PRISMA-style flow for the auxiliary support-literature search.

The figure deliberately says "documents" rather than "studies": this is an
original article and the structured search supplies contextual and
methodological support; it is not the primary study design.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "figura_s1_prisma_fulltext_final"


def box(ax, xy, width, height, title, body, *, green=False):
    edge = "#1f6b32" if green else "#17212b"
    face = "#f3f8f3" if green else "#ffffff"
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.014",
        linewidth=1.9,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(patch)
    x, y = xy
    ax.text(x + 0.025, y + height - 0.025, title, fontsize=10.2, weight="bold", va="top", linespacing=1.05)
    body_offset = 0.065 if "\n" not in title else 0.085
    ax.text(x + 0.025, y + height - body_offset, body, fontsize=8.8, va="top", linespacing=1.10)


def arrow(ax, start, end):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=13,
            linewidth=1.7,
            color="#17212b",
            shrinkA=0,
            shrinkB=0,
        )
    )


def main():
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.958, "PRISMA 2020 — CIERRE DE TEXTO COMPLETO", ha="center", fontsize=18, weight="bold")
    ax.text(
        0.5,
        0.934,
        "Búsqueda estructurada de literatura de soporte para un artículo original",
        ha="center",
        fontsize=11.5,
        color="#4b4b4b",
    )

    left_x, right_x, width, height = 0.08, 0.56, 0.40, 0.12
    ys = [0.77, 0.61, 0.45, 0.29]

    box(ax, (left_x, ys[0]), width, height, "Registros identificados", "Bases de datos (n = 767)\nRegistros (n = 0)")
    box(ax, (right_x, ys[0]), width, height, "Eliminados antes del cribado", "Duplicados (n = 116)\nOtras razones de compuerta (n = 3)")
    box(ax, (left_x, ys[1]), width, height, "Registros cribados", "n = 648")
    box(ax, (right_x, ys[1]), width, height, "Excluidos por título/resumen", "n = 576")
    box(ax, (left_x, ys[2]), width, height, "Informes buscados", "n = 72")
    box(ax, (right_x, ys[2]), width, height, "Informes no recuperados", "n = 30")
    box(ax, (left_x, ys[3]), width, height, "Informes evaluados\na texto completo", "n = 42")
    box(
        ax,
        (right_x, ys[3]),
        width,
        height,
        "Excluidos tras texto completo",
        "n = 13\nSin aporte directo: 8 · constructo: 2\ntransferibilidad: 2 · temporalidad: 1",
    )
    box(
        ax,
        (left_x, 0.12),
        width,
        height,
        "Documentos incluidos\nen el corpus de soporte",
        "n = 29",
        green=True,
    )

    for y in ys:
        arrow(ax, (left_x + width, y + height / 2), (right_x, y + height / 2))
    arrow(ax, (left_x + width / 2, ys[0]), (left_x + width / 2, ys[1] + height))
    arrow(ax, (left_x + width / 2, ys[1]), (left_x + width / 2, ys[2] + height))
    arrow(ax, (left_x + width / 2, ys[2]), (left_x + width / 2, ys[3] + height))
    arrow(ax, (left_x + width / 2, ys[3]), (left_x + width / 2, 0.12 + height))

    note = (
        "Nota. PRISMA se usa para documentar la obtención y selección de literatura de soporte. "
        "El diseño principal continúa siendo un análisis longitudinal descriptivo con escenarios "
        "exploratorios; no es una revisión sistemática."
    )
    ax.text(0.08, 0.075, note, fontsize=8.3, color="#404040", va="top", wrap=True)
    ax.text(0.08, 0.026, "Fuente: elaboración propia a partir del registro de decisiones de la fase 8.", fontsize=7.8, color="#555555")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT.with_suffix(".png"), dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(OUT.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
    fig.savefig(OUT.with_suffix(".svg"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
