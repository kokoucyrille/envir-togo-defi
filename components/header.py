"""En-tete institutionnel affiche en haut de chaque page."""

from __future__ import annotations

import os

import streamlit as st

from config.settings import (
    APP_SUBTITLE,
    APP_TITLE,
    INSTITUTION_LINE_1,
    INSTITUTION_LINE_2,
    LOGO_PATH,
)


def render_header(page_title: str | None = None, page_subtitle: str | None = None) -> None:
    """Affiche le bandeau institutionnel. Le logo n'est affiche que s'il est present
    dans assets/logo/images.png ; aucune image de substitution n'est generee."""
    col_logo, col_text = st.columns([1, 6], gap="medium")

    with col_logo:
        if os.path.exists(LOGO_PATH):
            st.image(str(LOGO_PATH), width="stretch")

    with col_text:
        title = page_title or APP_TITLE
        subtitle = page_subtitle or APP_SUBTITLE
        st.markdown(
            f"""
            <div class="institution-header">
                <p class="line1">{INSTITUTION_LINE_1}</p>
                <p class="line2">{INSTITUTION_LINE_2}</p>
                <p class="title">{title}</p>
                <p class="subtitle">{subtitle}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
