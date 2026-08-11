"""En-tete institutionnel affiche en haut de chaque page."""

from __future__ import annotations

import base64
import os

import streamlit as st

from config.settings import (
    APP_SUBTITLE,
    APP_TITLE,
    INSTITUTION_LINE_1,
    INSTITUTION_LINE_2,
    LOGO_PATH,
)


def _logo_base64() -> str | None:
    if not os.path.exists(LOGO_PATH):
        return None
    with open(LOGO_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def render_header(page_title: str | None = None, page_subtitle: str | None = None) -> None:
    """Affiche le bandeau institutionnel. Le logo n'est affiche que s'il est present
    dans assets/logo/images.png ; aucune image de substitution n'est generee."""
    logo_b64 = _logo_base64()
    logo_html = (
        f'<img class="header-logo" src="data:image/png;base64,{logo_b64}" />' if logo_b64 else ""
    )

    title = page_title or APP_TITLE
    subtitle = page_subtitle or APP_SUBTITLE
    st.markdown(
        f"""
        <div class="institution-header">
            <div class="institution-header-row">
                {logo_html}
                <div>
                    <p class="line1">{INSTITUTION_LINE_1}</p>
                    <p class="line2">{INSTITUTION_LINE_2}</p>
                    <p class="title">{title}</p>
                    <p class="subtitle">{subtitle}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
