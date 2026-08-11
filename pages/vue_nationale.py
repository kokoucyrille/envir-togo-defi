"""Page 1 -- Vue nationale : cockpit principal du tableau de bord."""

from __future__ import annotations

import streamlit as st

from analytics.indicators import national_kpis
from analytics.priorities import get_top_n
from components.decision_cards import render_storytelling_block
from components.header import render_header
from components.kpi_cards import national_kpi_row
from components.maps import priority_map
from components.tables import render_priority_table
from config.settings import DISCLAIMER_FUNCTIONALITY
from utils.formatting import format_number, format_percent


def render(cantons_geo, cantons_table, top20, infrastructures) -> None:
    render_header()

    kpis = national_kpis(cantons_table, infrastructures)
    national_kpi_row(kpis)

    st.info(DISCLAIMER_FUNCTIONALITY, icon=None)

    st.markdown("### Carte nationale du Water Urgency Index")
    st.caption(
        "Chaque canton est colore selon son niveau de priorite d'intervention. "
        "Survolez un canton pour afficher son detail (population, FRI, RWI, WUI, couverture documentaire)."
    )
    st.plotly_chart(priority_map(cantons_geo), width="stretch")

    st.markdown("### Territoires les plus prioritaires")
    top10 = get_top_n(top20, 10)
    render_priority_table(top10, search_key="vn_top10", download_name="top10_zones_prioritaires.csv")

    st.markdown("### A retenir")
    render_storytelling_block(
        constat=(
            f"{format_number(kpis['n_cantons_critiques'])} cantons, soit "
            f"{format_percent(kpis['part_cantons_critiques'])} du territoire national, sont classes en "
            f"priorite Critique et concentrent {format_percent(kpis['part_population_critique'])} de la "
            f"population nationale estimee."
        ),
        interpretation=(
            "Ces cantons cumulent une population elevee, un risque d'inondation eleve et/ou une "
            "vulnerabilite economique marquee. La couverture documentaire en infrastructures reste "
            "partielle : elle ne couvre que les programmes COSO et TdE, et ne constitue pas un "
            "inventaire national exhaustif."
        ),
        implication=(
            "Une strategie d'intervention doit cibler en priorite ces territoires, en combinant "
            "verification terrain, rehabilitation et mesures de resilience selon le profil de chaque "
            "canton (voir la page Priorites et scenarios)."
        ),
    )
