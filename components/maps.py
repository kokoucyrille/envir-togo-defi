"""Cartes interactives (Plotly / Mapbox open-street-map, sans cle API requise)."""

from __future__ import annotations

import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config.theme import FRI_COLORS, PRIORITY_COLORS, SOURCE_COLORS

_TOGO_CENTER = {"lat": 8.6, "lon": 1.0}


def _base_choropleth(gdf: gpd.GeoDataFrame, color_col: str, color_map: dict, hover_data: dict,
                      legend_title: str) -> go.Figure:
    geojson = gdf.__geo_interface__
    fig = px.choropleth_map(
        gdf,
        geojson=geojson,
        locations=gdf.index,
        color=color_col,
        color_discrete_map=color_map,
        hover_data=hover_data,
        map_style="carto-positron",
        center=_TOGO_CENTER,
        zoom=6.1,
        opacity=0.82,
        labels={color_col: legend_title},
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(title=legend_title, orientation="v", yanchor="top", y=0.98, xanchor="left", x=0.01),
        height=560,
    )
    return fig


def priority_map(gdf: gpd.GeoDataFrame) -> go.Figure:
    """Carte nationale du Water Urgency Index, coloree par niveau de priorite."""
    return _base_choropleth(
        gdf,
        color_col="priorite",
        color_map=PRIORITY_COLORS,
        hover_data={
            "canton": True, "region": True, "prefecture": True, "population": ":,",
            "FRI": ":.3f", "rwi_min": ":.2f", "WUI": ":.3f",
            "infrastructure_documentee": True,
        },
        legend_title="Niveau de priorite",
    )


def fri_map(gdf: gpd.GeoDataFrame) -> go.Figure:
    """Carte nationale du risque d'inondation (FRI) par canton."""
    return _base_choropleth(
        gdf,
        color_col="classe_fri",
        color_map=FRI_COLORS,
        hover_data={
            "canton": True, "region": True, "population": ":,", "FRI": ":.3f",
        },
        legend_title="Classe de risque",
    )


def coverage_map(gdf: gpd.GeoDataFrame) -> go.Figure:
    """Carte de la couverture documentaire en infrastructures, par canton."""
    coverage_labels = gdf["infrastructure_documentee"].map({
        True: "Documentee", False: "Non documentee dans les sources disponibles",
    })
    gdf = gdf.assign(couverture=coverage_labels)
    return _base_choropleth(
        gdf,
        color_col="couverture",
        color_map={
            "Documentee": "#3A7D44",
            "Non documentee dans les sources disponibles": "#D9D9D9",
        },
        hover_data={"canton": True, "region": True, "population": ":,"},
        legend_title="Couverture documentaire",
    )


def population_map(gdf: gpd.GeoDataFrame) -> go.Figure:
    """Carte choroplethe continue de la population par canton."""
    geojson = gdf.__geo_interface__
    fig = px.choropleth_map(
        gdf,
        geojson=geojson,
        locations=gdf.index,
        color="population",
        color_continuous_scale="Blues",
        hover_data={"canton": True, "region": True, "population": ":,"},
        map_style="carto-positron",
        center=_TOGO_CENTER,
        zoom=6.1,
        opacity=0.85,
        labels={"population": "Population"},
    )
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=560)
    return fig


def infrastructure_points_map(gdf: gpd.GeoDataFrame, infra: pd.DataFrame) -> go.Figure:
    """Carte des infrastructures documentees (COSO / TdE) superposees a un fond cantonal neutre."""
    geojson = gdf.__geo_interface__
    fig = px.choropleth_map(
        gdf,
        geojson=geojson,
        locations=gdf.index,
        color_discrete_sequence=["#EDEDED"],
        hover_data={"canton": True, "region": True},
        map_style="carto-positron",
        center=_TOGO_CENTER,
        zoom=6.1,
        opacity=0.5,
    )
    fig.update_traces(showlegend=False)

    for source, g in infra.groupby("source"):
        fig.add_trace(go.Scattermap(
            lat=g["latitude"], lon=g["longitude"],
            mode="markers",
            marker=dict(size=8, color=SOURCE_COLORS.get(source, "#333333")),
            name=source,
            text=g["title"] + " (" + g["canton"].fillna("canton non identifie") + ")",
            hoverinfo="text",
        ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=560,
        legend=dict(title="Source", orientation="v", yanchor="top", y=0.98, xanchor="left", x=0.01),
    )
    return fig


def risk_infrastructure_overlay_map(gdf: gpd.GeoDataFrame, infra: pd.DataFrame) -> go.Figure:
    """Carte du FRI par canton avec superposition des infrastructures documentees."""
    fig = fri_map(gdf)
    for source, g in infra.groupby("source"):
        fig.add_trace(go.Scattermap(
            lat=g["latitude"], lon=g["longitude"],
            mode="markers",
            marker=dict(size=7, color="black", symbol="circle" if source == "COSO" else "circle"),
            name=f"{source} (documente)",
            text=g["title"],
            hoverinfo="text",
        ))
    return fig
