"""Page 4 -- Risques : exposition au risque d'inondation (FRI)."""

from __future__ import annotations

import streamlit as st

from analytics.risk import (
    exposed_infrastructures,
    exposure_rate_by_source,
    risk_distribution,
    risk_vulnerability_matrix,
)
from components.charts import risk_distribution_chart, risk_vulnerability_scatter
from components.decision_cards import render_storytelling_block
from components.header import render_header
from components.maps import risk_infrastructure_overlay_map
from utils.formatting import format_percent


def render(cantons_geo, cantons_table, infrastructures) -> None:
    render_header(
        page_title="Risques d'inondation",
        page_subtitle="Exposition territoriale et infrastructures documentees en zone a risque",
    )

    show_overlay = st.toggle("Afficher les infrastructures documentees sur la carte du risque", value=True)
    st.markdown("#### Indice de risque d'inondation (FRI) par canton")
    if show_overlay:
        st.plotly_chart(risk_infrastructure_overlay_map(cantons_geo, infrastructures), width="stretch")
    else:
        from components.maps import fri_map
        st.plotly_chart(fri_map(cantons_geo), width="stretch")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Population par classe de risque")
        st.plotly_chart(risk_distribution_chart(risk_distribution(cantons_table)), width="stretch")
    with col_b:
        st.markdown("#### Exposition des infrastructures documentees par source")
        st.dataframe(exposure_rate_by_source(infrastructures, cantons_table), width="stretch", hide_index=True)

    st.markdown("#### Matrice risque x vulnerabilite economique")
    st.caption(
        "Chaque point represente un canton. La taille du point est proportionnelle a la population ; "
        "la couleur indique le niveau de priorite issu du Water Urgency Index."
    )
    matrix_df = risk_vulnerability_matrix(cantons_table)
    st.plotly_chart(risk_vulnerability_scatter(matrix_df), width="stretch")

    st.markdown("#### Infrastructures documentees en zone a risque eleve ou tres eleve")
    exposed = exposed_infrastructures(infrastructures, cantons_table)
    st.dataframe(
        exposed[["title", "type", "source", "canton", "region", "FRI", "classe_fri"]],
        width="stretch", hide_index=True,
    )

    n_exposed_tde = int(((infrastructures["source"] == "TdE") & infrastructures["canton"].isin(
        cantons_table.loc[cantons_table["classe_fri"].isin(["Eleve", "Tres eleve"]), "canton"]
    )).sum())
    n_tde = int((infrastructures["source"] == "TdE").sum())
    part_tde = 100 * n_exposed_tde / n_tde if n_tde else 0.0

    render_storytelling_block(
        constat=(
            f"{format_percent(part_tde)} des points TdE documentes se situent dans un canton classe a "
            "risque d'inondation eleve ou tres eleve, contre une part negligeable des sous-projets COSO."
        ),
        interpretation=(
            "Cet ecart resulte de la repartition geographique des deux sources : le programme COSO "
            "intervient en zones rurales du nord et du centre, structurellement moins exposees, tandis "
            "que les points TdE sont concentres sur le littoral, plus expose."
        ),
        implication=(
            "Les infrastructures TdE situees en zone a risque eleve constituent une cible naturelle "
            "pour des mesures de resilience (protection, surelevation), a instruire par une etude "
            "hydraulique locale."
        ),
    )
