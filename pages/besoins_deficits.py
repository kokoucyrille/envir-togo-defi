"""Page 3 -- Besoins et deficits : pression demographique et couverture documentaire."""

from __future__ import annotations

import streamlit as st

from components.decision_cards import render_storytelling_block
from components.filters import coverage_filter, geographic_filters
from components.header import render_header
from components.maps import coverage_map, population_map
from components.tables import render_priority_table
from config.settings import DISCLAIMER_NO_INFRA
from data.preprocessing import filter_cantons
from utils.formatting import format_number, format_percent


def render(cantons_geo, cantons_table) -> None:
    render_header(
        page_title="Besoins et deficits documentaires",
        page_subtitle="Pression demographique et couverture documentaire des infrastructures",
    )

    st.markdown(
        f'<div class="alert-methodo">{DISCLAIMER_NO_INFRA}</div>',
        unsafe_allow_html=True,
    )

    population_sans_infra = cantons_table.loc[~cantons_table["infrastructure_documentee"], "population"].sum()
    part = 100 * population_sans_infra / cantons_table["population"].sum()
    c1, c2 = st.columns(2)
    c1.metric("Population sans infrastructure documentee", format_number(population_sans_infra))
    c2.metric("Part de la population nationale", format_percent(part))

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Population par canton")
        st.plotly_chart(population_map(cantons_geo), width="stretch")
    with col_b:
        st.markdown("#### Couverture documentaire")
        st.plotly_chart(coverage_map(cantons_geo), width="stretch")

    st.markdown("#### Filtres")
    geo = geographic_filters(cantons_table, key_prefix="besoins", show_canton=False)
    coverage = coverage_filter(key_prefix="besoins")

    filtered = filter_cantons(
        cantons_table, region=geo["region"], prefecture=geo["prefecture"], commune=geo["commune"],
        infrastructure_documentee=coverage,
    )

    st.markdown("#### Territoires par population et couverture documentaire")
    sort_choice = st.radio("Trier par", ["Population", "Water Urgency Index"], horizontal=True, key="besoins_sort")
    sort_col = "population" if sort_choice == "Population" else "WUI"
    display = filtered.sort_values(sort_col, ascending=False).rename(columns={
        "canton": "Canton", "commune": "Commune", "prefecture": "Prefecture", "region": "Region",
        "population": "Population", "FRI": "FRI", "rwi_min": "RWI min", "WUI": "WUI",
        "infrastructure_documentee": "Infra. documentee", "priorite": "Priorite",
    })[["Canton", "Commune", "Prefecture", "Region", "Population", "FRI", "RWI min",
        "Infra. documentee", "WUI", "Priorite"]]
    render_priority_table(display, search_key="besoins_table", download_name="besoins_deficits.csv")

    render_storytelling_block(
        constat=(
            "La population togolaise est fortement concentree en region Maritime, qui porte pres de "
            "44 % de la population nationale estimee sur moins d'un cinquieme des cantons du pays."
        ),
        interpretation=(
            "Une population elevee combinee a une absence d'infrastructure documentee signale un "
            "territoire ou une verification prioritaire est justifiee, sans pour autant confirmer "
            "un deficit physique reel."
        ),
        implication=(
            "Les cantons combinant forte population et couverture documentaire absente constituent "
            "une cible naturelle pour un recensement terrain avant toute decision d'investissement."
        ),
    )
