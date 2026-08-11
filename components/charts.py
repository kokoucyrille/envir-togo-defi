"""Graphiques Plotly reutilisables."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config.settings import FRI_CLASSES, PRIORITY_LEVELS
from config.theme import FRI_COLORS, PLOTLY_TEMPLATE, PRIORITY_COLORS, SOURCE_COLORS


def priority_bar_chart(distribution: pd.DataFrame) -> go.Figure:
    """Diagramme en barres du nombre de cantons par niveau de priorite."""
    df = distribution.reset_index().rename(columns={"index": "priorite"})
    fig = px.bar(
        df, x="priorite", y="cantons", color="priorite",
        color_discrete_map=PRIORITY_COLORS,
        category_orders={"priorite": PRIORITY_LEVELS},
        text="cantons",
        labels={"priorite": "Niveau de priorite", "cantons": "Nombre de cantons"},
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, height=380, margin=dict(t=20, b=10))
    return fig


def risk_distribution_chart(distribution: pd.DataFrame) -> go.Figure:
    """Diagramme en barres de la population par classe de risque FRI."""
    df = distribution.reset_index().rename(columns={"index": "classe_fri"})
    fig = px.bar(
        df, x="classe_fri", y="population", color="classe_fri",
        color_discrete_map=FRI_COLORS,
        category_orders={"classe_fri": FRI_CLASSES},
        labels={"classe_fri": "Classe de risque (FRI)", "population": "Population"},
        template=PLOTLY_TEMPLATE,
    )
    fig.update_layout(showlegend=False, height=380, margin=dict(t=20, b=10))
    return fig


def regional_population_chart(summary: pd.DataFrame) -> go.Figure:
    """Diagramme en barres horizontales de la population par region."""
    df = summary.reset_index().sort_values("population")
    fig = px.bar(
        df, x="population", y="region", orientation="h",
        text="part_population_pct",
        labels={"population": "Population", "region": "Region"},
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(texttemplate="%{text:.1f} %", textposition="outside", marker_color="#1B6FA8")
    fig.update_layout(height=320, margin=dict(t=20, b=10))
    return fig


def infrastructure_status_chart(infra_full: pd.DataFrame) -> go.Figure:
    """Diagramme en barres horizontales du statut d'avancement des sous-projets COSO."""
    order = [
        "Achevé 100.0%", "Réception technique 100.0%", "Réception provisoire 100.0%",
        "Réception définitive 100.0%", "Remise de l'ouvrage à la communauté 100.0%", "En cours",
    ]
    counts = infra_full["status"].value_counts().reindex(order).fillna(0).astype(int)
    df = counts.reset_index()
    df.columns = ["status", "count"]
    fig = px.bar(
        df, x="count", y="status", orientation="h",
        labels={"count": "Nombre de sous-projets", "status": "Statut administratif"},
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(marker_color="#0B2545")
    fig.update_layout(height=340, margin=dict(t=20, b=10))
    return fig


def coverage_by_region_chart(summary: pd.DataFrame) -> go.Figure:
    """Taux de couverture documentaire par region."""
    df = summary.reset_index().sort_values("taux_couverture_pct")
    fig = px.bar(
        df, x="taux_couverture_pct", y="region", orientation="h",
        labels={"taux_couverture_pct": "Taux de couverture documentaire (%)", "region": "Region"},
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(marker_color="#3A7D44")
    fig.update_layout(height=320, margin=dict(t=20, b=10))
    return fig


def risk_vulnerability_scatter(df: pd.DataFrame) -> go.Figure:
    """Nuage de points risque (FRI) x vulnerabilite economique (RWI), taille = population."""
    fig = px.scatter(
        df, x="rwi_min", y="FRI", size="population", color="priorite",
        color_discrete_map=PRIORITY_COLORS,
        category_orders={"priorite": PRIORITY_LEVELS},
        hover_name="canton",
        hover_data={"region": True, "population": ":,", "rwi_min": ":.2f", "FRI": ":.3f"},
        labels={"rwi_min": "Vulnerabilite economique (RWI min. -- plus bas = plus vulnerable)",
                "FRI": "Risque d'inondation (FRI)"},
        template=PLOTLY_TEMPLATE,
    )
    fig.update_layout(height=480, margin=dict(t=20, b=10))
    return fig


def scenario_comparison_chart(baseline: float, scenario_value: float, label: str) -> go.Figure:
    """Diagramme en barres comparant le WUI moyen actuel et simule pour un scenario."""
    df = pd.DataFrame({
        "Situation": ["Actuelle / Business as Usual", label],
        "WUI moyen": [baseline, scenario_value],
    })
    fig = px.bar(
        df, x="Situation", y="WUI moyen", color="Situation",
        color_discrete_sequence=["#8C8C8C", "#1B6FA8"],
        text="WUI moyen", template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
    fig.update_layout(showlegend=False, height=360, margin=dict(t=20, b=10))
    return fig


def source_split_chart(infra: pd.DataFrame) -> go.Figure:
    """Repartition des infrastructures documentees par source (COSO / TdE)."""
    counts = infra["source"].value_counts().reset_index()
    counts.columns = ["source", "count"]
    fig = px.pie(
        counts, names="source", values="count",
        color="source", color_discrete_map=SOURCE_COLORS,
        template=PLOTLY_TEMPLATE, hole=0.45,
    )
    fig.update_layout(height=320, margin=dict(t=20, b=10))
    return fig
