"""Chargement des jeux de donnees analytiques.

Toutes les fonctions de ce module sont decorees avec ``st.cache_data`` afin de
n'executer la lecture et la preparation des donnees qu'une seule fois par session,
conformement a l'exigence de performance du cahier des charges.
"""

from __future__ import annotations

import geopandas as gpd
import pandas as pd
import streamlit as st

from config.settings import (
    CANTONS_CSV,
    CANTONS_GEOJSON,
    COSO_ALL_CSV,
    COSO_CSV,
    DATA_DICTIONARY_CSV,
    TDE_CSV,
    TOP20_CSV,
)


@st.cache_data(show_spinner=False)
def load_cantons_geo() -> gpd.GeoDataFrame:
    """Charge les 388 cantons avec leurs attributs analytiques (FRI, RWI, WUI, priorite)
    et leur geometrie, tels que calcules dans EDA_Eau_Togo.ipynb."""
    gdf = gpd.read_file(CANTONS_GEOJSON)
    gdf["population"] = gdf["population"].astype(int)
    return gdf


@st.cache_data(show_spinner=False)
def load_cantons_table() -> pd.DataFrame:
    """Charge la table plate (sans geometrie) des 388 cantons, pour les tableaux et filtres."""
    df = pd.read_csv(CANTONS_CSV)
    return df


@st.cache_data(show_spinner=False)
def load_top20() -> pd.DataFrame:
    """Charge le classement de reference des 20 cantons les plus prioritaires."""
    return pd.read_csv(TOP20_CSV)


@st.cache_data(show_spinner=False)
def load_data_dictionary() -> pd.DataFrame:
    """Charge le data dictionary consolide produit par l'EDA de reference."""
    return pd.read_csv(DATA_DICTIONARY_CSV)


@st.cache_data(show_spinner=False)
def load_infrastructures() -> pd.DataFrame:
    """Charge et concatene les infrastructures documentees cartographiables (COSO + TdE)."""
    coso = pd.read_csv(COSO_CSV)
    tde = pd.read_csv(TDE_CSV)
    common_cols = ["title", "type", "region", "prefecture", "commune", "canton",
                   "latitude", "longitude", "source"]
    coso_c = coso[common_cols].copy()
    coso_c["status"] = coso["status"]
    tde_c = tde[common_cols].copy()
    tde_c["status"] = "Non renseigne"
    combined = pd.concat([coso_c, tde_c], ignore_index=True)
    return combined


@st.cache_data(show_spinner=False)
def load_infrastructures_full_coso() -> pd.DataFrame:
    """Charge l'integralite des sous-projets COSO rattaches a un canton (avec ou sans
    coordonnees GPS valides), utile pour les tableaux et agregations non cartographiques."""
    return pd.read_csv(COSO_ALL_CSV)


@st.cache_data(show_spinner=False)
def get_geographic_hierarchy(cantons: pd.DataFrame) -> dict:
    """Construit la hierarchie region -> prefecture -> commune -> canton pour alimenter
    des filtres en cascade."""
    hierarchy: dict = {}
    for region, g_region in cantons.groupby("region"):
        hierarchy[region] = {}
        for prefecture, g_pref in g_region.groupby("prefecture"):
            hierarchy[region][prefecture] = {}
            for commune, g_comm in g_pref.groupby("commune"):
                hierarchy[region][prefecture][commune] = sorted(g_comm["canton"].unique().tolist())
    return hierarchy
