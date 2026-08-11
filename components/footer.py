"""Pied de page discret, affiche sur chaque page."""

from __future__ import annotations

import streamlit as st

from config.settings import APP_TITLE, AUTHOR_NAME, AUTHOR_TITLE


def render_footer() -> None:
    st.markdown(
        f"""
        <div class="app-footer">
            {APP_TITLE}<br>
            Application d'aide a la decision<br>
            {AUTHOR_NAME} -- {AUTHOR_TITLE}
        </div>
        """,
        unsafe_allow_html=True,
    )
