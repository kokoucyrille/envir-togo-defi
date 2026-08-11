"""Cartes KPI standardisees (valeur, titre, contexte court)."""

from __future__ import annotations

import streamlit as st

from utils.formatting import format_number, format_percent


def render_kpi_row(kpis: list[tuple[str, str, str | None]]) -> None:
    """Affiche une rangee de cartes KPI. Chaque element est un tuple
    (titre, valeur formatee, contexte optionnel)."""
    cols = st.columns(len(kpis))
    for col, (title, value, context) in zip(cols, kpis):
        with col:
            st.metric(label=title, value=value, help=context)


def national_kpi_row(kpis: dict) -> None:
    """Rangee de KPI nationaux pour la vue nationale."""
    render_kpi_row([
        ("Cantons analyses", format_number(kpis["n_cantons"]), "Couverture nationale complete (5 regions)."),
        ("Population estimee", format_number(kpis["population_totale"]),
         "Population totale des 388 cantons (source : couche FRI)."),
        ("Cantons prioritaires (Critique)", format_number(kpis["n_cantons_critiques"]),
         f"{format_percent(kpis['part_cantons_critiques'])} des cantons du pays."),
        ("Population en zone Critique", format_number(kpis["population_critique"]),
         f"{format_percent(kpis['part_population_critique'])} de la population nationale."),
    ])
    render_kpi_row([
        ("Infrastructures documentees", format_number(kpis["n_infrastructures"]),
         f"{kpis['n_coso']} sous-projets COSO, {kpis['n_tde']} points TdE."),
        ("Infrastructures exposees", format_number(kpis["n_infra_exposees"]),
         "Situees dans un canton a risque d'inondation eleve ou tres eleve."),
        ("Population sans infra. documentee", format_percent(kpis["part_sans_infra"]),
         "Part de la population residant dans un canton sans infrastructure documentee."),
        ("Water Urgency Index moyen", f"{kpis['wui_moyen']:.3f}",
         "Indice composite national (0 = urgence faible, 1 = urgence forte)."),
    ])
