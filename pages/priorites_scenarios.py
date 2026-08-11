"""Page 5 -- Priorites et scenarios : de la priorisation a l'action (page centrale)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from analytics.priorities import explain_priority_factors, get_canton_profile, recommend_action
from analytics.recommendations import DECISION_MATRIX, STRATEGIC_RECOMMENDATIONS
from analytics.scenarios import scenario_impact_summary
from components.charts import scenario_comparison_chart
from components.decision_cards import render_recommendation_card, render_territory_profile
from components.filters import geographic_filters, priority_filter
from components.header import render_header
from components.tables import render_priority_table
from config.settings import DISCLAIMER_SCENARIOS, SCENARIOS, WUI_SENSITIVITY_NOTE
from data.preprocessing import filter_cantons
from utils.formatting import format_number, format_percent


def _section_a(cantons_table: pd.DataFrame) -> None:
    st.markdown("### A. Water Urgency Index -- exploration territoriale")
    st.caption(WUI_SENSITIVITY_NOTE)

    geo = geographic_filters(cantons_table, key_prefix="pr_wui")
    priorities = priority_filter(key_prefix="pr_wui")

    filtered = filter_cantons(
        cantons_table, region=geo["region"], prefecture=geo["prefecture"], commune=geo["commune"],
        canton=geo["canton"], priorite=priorities,
    )
    display = filtered.sort_values("WUI", ascending=False).rename(columns={
        "canton": "Canton", "commune": "Commune", "prefecture": "Prefecture", "region": "Region",
        "population": "Population", "FRI": "FRI", "rwi_min": "RWI min",
        "infrastructure_documentee": "Infra. documentee", "WUI": "WUI", "priorite": "Priorite",
    })[["Canton", "Commune", "Prefecture", "Region", "Population", "FRI", "RWI min",
        "Infra. documentee", "WUI", "Priorite"]]
    render_priority_table(display, search_key="pr_wui_table", download_name="water_urgency_index.csv")
    return geo["canton"]


def _section_b(top20: pd.DataFrame) -> None:
    st.markdown("### B. Top 20 des territoires prioritaires")
    render_priority_table(top20, search_key="pr_top20", download_name="top20_zones_prioritaires.csv")


def _section_c(cantons_table: pd.DataFrame, preselected_canton: str | None) -> None:
    st.markdown("### C. Profil territorial")
    canton_list = sorted(cantons_table["canton"].unique().tolist())
    default_index = 0
    if preselected_canton and preselected_canton in canton_list:
        default_index = canton_list.index(preselected_canton) + 1
    selection = st.selectbox("Selectionner un canton", ["-- Choisir --"] + canton_list, index=default_index)

    if selection == "-- Choisir --":
        st.caption("Selectionnez un canton pour afficher sa fiche decisionnelle.")
        return

    profile = get_canton_profile(cantons_table, selection)
    if profile is None:
        st.warning("Canton introuvable.")
        return

    factors = explain_priority_factors(profile, cantons_table)
    recommendation = recommend_action(profile, cantons_table)
    render_territory_profile(profile, factors, recommendation)


def _section_d() -> None:
    st.markdown("### D. Matrice de decision")
    df = pd.DataFrame(DECISION_MATRIX).rename(columns={"situation": "Situation observee", "action": "Intervention potentielle"})
    st.dataframe(df, width="stretch", hide_index=True)


def _section_e(cantons_table: pd.DataFrame) -> None:
    st.markdown("### E. Scenarios prospectifs (simulation)")
    st.markdown(f'<div class="alert-methodo">{DISCLAIMER_SCENARIOS}</div>', unsafe_allow_html=True)

    scenario_keys = [k for k in SCENARIOS if k != "S0"]
    labels = {k: SCENARIOS[k]["label"] for k in scenario_keys}
    choice = st.selectbox("Scenario a comparer au statu quo", scenario_keys, format_func=lambda k: labels[k])
    params = SCENARIOS[choice]
    st.caption(params["description"])

    result = scenario_impact_summary(cantons_table, params, scope="critique")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Territoires cibles (priorite Critique)", format_number(result["territoires_cibles"]))
    c2.metric("Population ciblee", format_number(result["population_ciblee"]))
    c3.metric("Reduction moyenne du WUI simulee", format_percent(result["reduction_wui_pct"]))
    c4.metric("Cantons repassant sous le seuil critique", format_number(result["cantons_sous_seuil_critique"]))

    st.plotly_chart(
        scenario_comparison_chart(result["wui_moyen_actuel"], result["wui_moyen_simule"], labels[choice]),
        width="stretch",
    )

    comparison = pd.DataFrame([
        {"Indicateur": "WUI moyen (cantons critiques)",
         "Situation actuelle / BAU": result["wui_moyen_actuel"],
         "Scenario simule": result["wui_moyen_simule"]},
        {"Indicateur": "Cantons en priorite Critique",
         "Situation actuelle / BAU": result["territoires_cibles"],
         "Scenario simule": result["territoires_cibles"] - result["cantons_sous_seuil_critique"]},
        {"Indicateur": "Population en zone Critique",
         "Situation actuelle / BAU": result["population_ciblee"],
         "Scenario simule": result["population_ciblee"] - result["population_beneficiaire_potentielle"]},
    ])
    st.dataframe(comparison, width="stretch", hide_index=True)


def render(cantons_table: pd.DataFrame, top20: pd.DataFrame) -> None:
    render_header(
        page_title="Priorites et scenarios",
        page_subtitle="De la priorisation territoriale a la decision d'intervention",
    )

    selected_canton = _section_a(cantons_table)
    st.markdown("---")
    _section_b(top20)
    st.markdown("---")
    _section_c(cantons_table, selected_canton)
    st.markdown("---")
    _section_d()
    st.markdown("---")
    _section_e(cantons_table)
    st.markdown("---")

    st.markdown("### Recommandations strategiques")
    for rec in STRATEGIC_RECOMMENDATIONS:
        render_recommendation_card(rec)
