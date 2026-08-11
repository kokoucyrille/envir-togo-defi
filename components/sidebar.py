"""Navigation laterale de l'application.

Sidebar fond vert institutionnel avec :
  - logo centre sur fond blanc
  - titre de section en lettres capitales discretes
  - items de navigation au style bouton (item actif blanc/vert fonce, inactifs blancs transparents)
  - note methodologique en bas
"""

from __future__ import annotations

import os

import streamlit as st

from config.settings import LOGO_PATH, PAGES

# Icones associees a chaque section (emoji minimaliste)
_PAGE_ICONS: dict[str, str] = {
    "Vue nationale":              "🗺️",
    "Infrastructures":            "🔧",
    "Besoins et deficits":        "💧",
    "Risques":                    "⚠️",
    "Priorites et scenarios":     "📊",
    "A propos et methodologie":   "ℹ️",
}


def render_sidebar() -> str:
    """Affiche la navigation laterale et retourne la page selectionnee."""
    with st.sidebar:
        # Logo centre sur fond blanc (cadre clair)
        if os.path.exists(LOGO_PATH):
            st.image(str(LOGO_PATH), use_container_width=True)
        else:
            st.markdown(
                "<p style='color:rgba(255,255,255,0.6);font-size:0.75rem;"
                "text-align:center;padding:0.5rem 0;'>Logo institutionnel</p>",
                unsafe_allow_html=True,
            )

        st.markdown("### Navigation")

        # Radio avec libelles enrichis d'icones
        labeled_pages = [f"{_PAGE_ICONS.get(p, '•')}  {p}" for p in PAGES]
        selected_label = st.radio(
            "Section",
            labeled_pages,
            label_visibility="collapsed",
        )

        # Retrouver le nom de page original (sans icone)
        idx = labeled_pages.index(selected_label)
        page = PAGES[idx]

        st.markdown("---")
        st.caption(
            "Les analyses presentees sont issues de EDA_Eau_Togo.ipynb. "
            "Aucun indicateur n'est recalcule avec des hypotheses differentes de celles "
            "documentees dans l'etude de reference."
        )

    return page
