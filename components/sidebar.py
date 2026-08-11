"""Navigation laterale de l'application (cinq sections analytiques + page A propos)."""

from __future__ import annotations

import base64
import os

import streamlit as st

from config.settings import INSTITUTION_LINE_1, INSTITUTION_LINE_2, LOGO_PATH, PAGES


def _logo_base64() -> str | None:
    if not os.path.exists(LOGO_PATH):
        return None
    with open(LOGO_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def render_sidebar() -> str:
    
    with st.sidebar:
        logo_b64 = _logo_base64()
        logo_html = (
            f'<img src="data:image/png;base64,{logo_b64}" width="72" />' if logo_b64 else ""
        )
        st.markdown(
            f"""
            <div class="sidebar-brand">
                {logo_html}
                <p class="brand-title">{INSTITUTION_LINE_1}</p>
                <p class="brand-subtitle">{INSTITUTION_LINE_2}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<p class="sidebar-section-label">Navigation</p>', unsafe_allow_html=True)
        labels = [f"{i:02d}  {p}" for i, p in enumerate(PAGES, start=1)]
        selected_label = st.radio("Section", labels, label_visibility="collapsed")
        page = PAGES[labels.index(selected_label)]

        
    return page
