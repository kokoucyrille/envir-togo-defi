"""Point d'entree de l'application Streamlit.

Ce fichier se limite a la configuration Streamlit, au chargement des donnees en cache,
a la navigation et a l'orchestration des pages. Toute la logique d'affichage vit dans
``pages/`` et ``components/`` ; toute la logique analytique vit dans ``analytics/``.
"""

from __future__ import annotations

import streamlit as st

from components.footer import render_footer
from components.sidebar import render_sidebar
from config.settings import APP_TITLE
from config.theme import CUSTOM_CSS
from data.loader import (
    load_cantons_geo,
    load_cantons_table,
    load_data_dictionary,
    load_infrastructures,
    load_infrastructures_full_coso,
    load_top20,
)
from data.validators import validate_cantons, validate_top20

st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def main() -> None:
    cantons_geo = load_cantons_geo()
    cantons_table = load_cantons_table()
    top20 = load_top20()
    data_dictionary = load_data_dictionary()
    infrastructures = load_infrastructures()
    infra_full_coso = load_infrastructures_full_coso()

    issues = validate_cantons(cantons_table) + validate_top20(top20)
    if issues:
        with st.sidebar:
            st.error("Anomalies detectees dans les donnees chargees :\n\n" + "\n".join(f"- {i}" for i in issues))

    page = render_sidebar()

    

    render_footer()


if __name__ == "__main__":
    main()
