"""Fonctions de filtrage reutilisables sur la table des cantons et des infrastructures.

Ce module ne recalcule aucun indicateur : il applique uniquement des filtres sur des
resultats deja produits par l'EDA de reference.
"""

from __future__ import annotations

import pandas as pd


def filter_cantons(
    df: pd.DataFrame,
    region: str | None = None,
    prefecture: str | None = None,
    commune: str | None = None,
    canton: str | None = None,
    priorite: list[str] | None = None,
    classe_fri: list[str] | None = None,
    infrastructure_documentee: str | None = None,
) -> pd.DataFrame:
    """Applique en cascade les filtres geographiques et analytiques disponibles."""
    out = df
    if region and region != "Toutes":
        out = out[out["region"] == region]
    if prefecture and prefecture != "Toutes":
        out = out[out["prefecture"] == prefecture]
    if commune and commune != "Toutes":
        out = out[out["commune"] == commune]
    if canton and canton != "Tous":
        out = out[out["canton"] == canton]
    if priorite:
        out = out[out["priorite"].isin(priorite)]
    if classe_fri:
        out = out[out["classe_fri"].isin(classe_fri)]
    if infrastructure_documentee and infrastructure_documentee != "Toutes":
        target = infrastructure_documentee == "Documentee"
        out = out[out["infrastructure_documentee"] == target]
    return out


def filter_infrastructures(
    df: pd.DataFrame,
    region: str | None = None,
    prefecture: str | None = None,
    commune: str | None = None,
    source: list[str] | None = None,
) -> pd.DataFrame:
    """Applique les filtres geographiques et de source aux infrastructures documentees."""
    out = df
    if region and region != "Toutes":
        out = out[out["region"] == region]
    if prefecture and prefecture != "Toutes":
        out = out[out["prefecture"] == prefecture]
    if commune and commune != "Toutes":
        out = out[out["commune"] == commune]
    if source:
        out = out[out["source"].isin(source)]
    return out


def options_or_all(values: pd.Series, all_label: str) -> list[str]:
    """Construit une liste d'options triees prefixee par un libelle 'tous/toutes'."""
    return [all_label] + sorted(values.dropna().unique().tolist())
