"""Page 2 -- Infrastructures : couverture des ouvrages documentes (COSO + TdE)."""

from __future__ import annotations

import streamlit as st

from components.charts import infrastructure_status_chart, source_split_chart
from components.decision_cards import render_storytelling_block
from components.filters import geographic_filters, infrastructure_filter
from components.header import render_header
from components.maps import infrastructure_points_map
from components.tables import render_infrastructure_table
from config.settings import DISCLAIMER_COVERAGE
from data.preprocessing import filter_infrastructures


def render(cantons_geo, infrastructures, infra_full_coso) -> None:
    render_header(
        page_title="Infrastructures hydrauliques documentees",
        page_subtitle="Couverture des sous-projets COSO et des points Togolaise des Eaux (TdE)",
    )

    st.markdown(
        f'<div class="alert-methodo">{DISCLAIMER_COVERAGE}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("#### Filtres")
    geo = geographic_filters(infrastructures, key_prefix="infra", show_canton=False)
    source = infrastructure_filter(key_prefix="infra")

    filtered = filter_infrastructures(
        infrastructures, region=geo["region"], prefecture=geo["prefecture"],
        commune=geo["commune"], source=source,
    )

    col_map, col_side = st.columns([3, 1])
    with col_map:
        st.markdown("#### Localisation des infrastructures documentees")
        st.plotly_chart(infrastructure_points_map(cantons_geo, filtered), width="stretch")
    with col_side:
        st.markdown("#### Repartition par source")
        st.plotly_chart(source_split_chart(filtered) if len(filtered) else source_split_chart(infrastructures),
                         width="stretch")

    st.markdown("#### Etat d'avancement administratif des sous-projets COSO")
    st.caption(
        "Cet indicateur mesure l'avancement du cycle de vie administratif des sous-projets "
        "(reception, remise a la communaute) et ne constitue pas une mesure de fonctionnalite "
        "operationnelle actuelle."
    )
    st.plotly_chart(infrastructure_status_chart(infra_full_coso), width="stretch")

    st.markdown("#### Tableau des infrastructures documentees")
    render_infrastructure_table(filtered, search_key="infra_table", download_name="infrastructures_filtrees.csv")

    render_storytelling_block(
        constat=(
            "Les sous-projets COSO couvrent principalement les regions Centrale, Kara et Savanes, "
            "tandis que les points TdE sont concentres dans la region Maritime."
        ),
        interpretation=(
            "Ces deux sources ne se recouvrent pas geographiquement et ne documentent, ensemble, "
            "qu'une partie du territoire national."
        ),
        implication=(
            "Toute lecture d'un canton sans infrastructure visible sur la carte doit etre "
            "interpretee comme une absence de documentation, non comme une absence physique "
            "d'ouvrage."
        ),
    )
