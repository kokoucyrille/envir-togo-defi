"""Tableaux interactifs standardises (tri, recherche, mise en evidence, telechargement)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config.theme import PRIORITY_COLORS
from utils.helpers import download_button


def _highlight_priority(row: pd.Series) -> list[str]:
    color = PRIORITY_COLORS.get(row.get("Priorite", ""), None)
    if color is None:
        return [""] * len(row)
    return [f"background-color: {color}22"] * len(row)


def render_priority_table(df: pd.DataFrame, search_key: str, download_name: str) -> None:
    """Affiche un tableau de territoires avec recherche par nom de canton, mise en
    evidence du niveau de priorite et telechargement CSV."""
    search = st.text_input("Rechercher un canton", key=f"{search_key}_search", placeholder="Nom du canton...")
    view = df
    if search:
        col = "Canton" if "Canton" in df.columns else "canton"
        view = df[df[col].str.contains(search, case=False, na=False)]

    if "Priorite" in view.columns:
        styled = view.style.apply(_highlight_priority, axis=1)
        st.dataframe(styled, width="stretch", hide_index=True)
    else:
        st.dataframe(view, width="stretch", hide_index=True)

    download_button(view, "Telecharger ce tableau (CSV)", download_name, key=f"{search_key}_dl")


def render_infrastructure_table(df: pd.DataFrame, search_key: str, download_name: str) -> None:
    """Affiche le tableau des infrastructures documentees filtrees, avec recherche et export."""
    search = st.text_input(
        "Rechercher un ouvrage", key=f"{search_key}_search", placeholder="Nom de l'ouvrage ou du canton..."
    )
    view = df
    if search:
        mask = df["title"].str.contains(search, case=False, na=False) | df["canton"].str.contains(
            search, case=False, na=False
        )
        view = df[mask]

    display_cols = [c for c in ["title", "type", "source", "status", "region", "prefecture", "commune", "canton"]
                     if c in view.columns]
    st.dataframe(view[display_cols], width="stretch", hide_index=True)
    download_button(view[display_cols], "Telecharger ce tableau (CSV)", download_name, key=f"{search_key}_dl")
