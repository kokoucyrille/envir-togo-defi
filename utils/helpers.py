"""Fonctions utilitaires diverses."""

from __future__ import annotations

import pandas as pd
import streamlit as st


def to_csv_download(df: pd.DataFrame) -> bytes:
    """Serialise un DataFrame en CSV telechargeable (encodage UTF-8 avec BOM pour Excel)."""
    return df.to_csv(index=False).encode("utf-8-sig")


def download_button(df: pd.DataFrame, label: str, file_name: str, key: str) -> None:
    """Affiche un bouton de telechargement CSV standardise."""
    st.download_button(
        label=label,
        data=to_csv_download(df),
        file_name=file_name,
        mime="text/csv",
        key=key,
    )


def init_session_state_defaults(defaults: dict) -> None:
    """Initialise les cles de session_state absentes avec des valeurs par defaut."""
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
