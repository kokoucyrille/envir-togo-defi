"""Blocs de storytelling decisionnel (Constat / Interpretation / Implication) et fiches
de recommandation (Probleme -> Action -> Impact -> KPI -> Horizon)."""

from __future__ import annotations

import streamlit as st

from config.theme import priority_badge_html


def render_storytelling_block(constat: str, interpretation: str, implication: str) -> None:
    """Affiche un bloc structure Constat / Interpretation / Implication."""
    st.markdown(
        f"""
        <div class="decision-block">
            <h4>Ce que montrent les donnees</h4>
            <p>{constat}</p>
            <h4>Pourquoi c'est important</h4>
            <p>{interpretation}</p>
            <h4>Pour la decision</h4>
            <p>{implication}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendation_card(rec: dict) -> None:
    """Affiche une fiche de recommandation strategique complete."""
    with st.container(border=True):
        st.markdown(f"#### {rec['titre']}")
        st.markdown(f"**Territoire concerne :** {rec['territoire']}")
        st.markdown(f"**Probleme identifie :** {rec['probleme']}")
        st.markdown(f"**Action proposee :** {rec['action']}")
        st.markdown(f"**Justification quantitative :** {rec['justification']}")
        st.markdown(f"**Impact potentiel :** {rec['impact']}")
        st.markdown(f"**KPI de suivi :** {rec['kpi']}")
        st.markdown(f"**Horizon :** {rec['horizon']}")


def render_territory_profile(profile, factors: list[str], recommendation: dict) -> None:
    """Affiche la fiche decisionnelle d'un canton selectionne."""
    from utils.formatting import format_number, format_index

    badge = priority_badge_html(profile["priorite"])
    st.markdown(f"### {profile['canton']} &nbsp; {badge}", unsafe_allow_html=True)
    st.caption(f"{profile['commune']}, {profile['prefecture']}, region {profile['region']}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Population", format_number(profile["population"]))
    c2.metric("Risque d'inondation (FRI)", format_index(profile["FRI"]))
    c3.metric("Vulnerabilite (RWI min.)", f"{profile['rwi_min']:.2f}")
    c4.metric("Water Urgency Index", format_index(profile["WUI"]))

    st.markdown("**Pourquoi ce territoire est-il classe a ce niveau de priorite ?**")
    for f in factors:
        st.markdown(f"- {f}")

    st.markdown("**Quelle intervention envisager ?**")
    st.markdown(
        f"""
        <div class="decision-block">
            <p><strong>Situation :</strong> {recommendation['situation']}</p>
            <p><strong>Action potentielle :</strong> {recommendation['action']}</p>
            <p><strong>Horizon indicatif :</strong> {recommendation['horizon']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
