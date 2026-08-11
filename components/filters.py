"""Composants de filtrage reutilisables entre les pages.

Les filtres geographiques sont dependants (region -> prefecture -> commune -> canton) :
la selection d'une region restreint automatiquement les prefectures proposees, et ainsi
de suite, conformement au cahier des charges.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config.settings import PRIORITY_LEVELS, FRI_CLASSES


def geographic_filters(cantons: pd.DataFrame, key_prefix: str, show_canton: bool = True) -> dict:
    """Affiche des filtres region/prefecture/commune/(canton) en cascade et retourne
    la selection courante sous forme de dictionnaire."""
    columns = st.columns(4) if show_canton else st.columns(3)
    col1, col2, col3 = columns[0], columns[1], columns[2]

    with col1:
        region = st.selectbox(
            "Region", ["Toutes"] + sorted(cantons["region"].unique().tolist()),
            key=f"{key_prefix}_region",
        )
    scope = cantons if region == "Toutes" else cantons[cantons["region"] == region]

    with col2:
        prefecture = st.selectbox(
            "Prefecture", ["Toutes"] + sorted(scope["prefecture"].unique().tolist()),
            key=f"{key_prefix}_prefecture",
        )
    scope = scope if prefecture == "Toutes" else scope[scope["prefecture"] == prefecture]

    with col3:
        commune = st.selectbox(
            "Commune", ["Toutes"] + sorted(scope["commune"].unique().tolist()),
            key=f"{key_prefix}_commune",
        )
    scope = scope if commune == "Toutes" else scope[scope["commune"] == commune]

    canton = None
    if show_canton:
        with columns[3]:
            canton = st.selectbox(
                "Canton", ["Tous"] + sorted(scope["canton"].unique().tolist()),
                key=f"{key_prefix}_canton",
            )

    return {"region": region, "prefecture": prefecture, "commune": commune, "canton": canton}


def priority_filter(key_prefix: str) -> list[str]:
    """Filtre multi-selection sur le niveau de priorite (Water Urgency Index)."""
    return st.multiselect(
        "Niveau de priorite",
        PRIORITY_LEVELS,
        default=PRIORITY_LEVELS,
        key=f"{key_prefix}_priority",
    )


def risk_filter(key_prefix: str) -> list[str]:
    """Filtre multi-selection sur la classe de risque d'inondation (FRI)."""
    return st.multiselect(
        "Classe de risque (FRI)",
        FRI_CLASSES,
        default=FRI_CLASSES,
        key=f"{key_prefix}_risk",
    )


def infrastructure_filter(key_prefix: str) -> list[str]:
    """Filtre multi-selection sur la source d'infrastructure documentee."""
    return st.multiselect(
        "Source d'infrastructure",
        ["COSO", "TdE"],
        default=["COSO", "TdE"],
        key=f"{key_prefix}_source",
    )


def coverage_filter(key_prefix: str) -> str:
    """Filtre sur la couverture documentaire (canton avec/sans infrastructure documentee)."""
    return st.selectbox(
        "Couverture documentaire",
        ["Toutes", "Documentee", "Non documentee"],
        key=f"{key_prefix}_coverage",
    )
