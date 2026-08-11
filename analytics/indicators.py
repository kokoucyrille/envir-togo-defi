"""Calcul des KPI nationaux et territoriaux affiches dans le tableau de bord.

Ces fonctions agregent des colonnes deja produites par l'EDA de reference ; elles
n'introduisent aucun nouvel indicateur qui ne serait pas deja calculable a partir des
donnees disponibles.
"""

from __future__ import annotations

import pandas as pd


def national_kpis(cantons: pd.DataFrame, infrastructures: pd.DataFrame) -> dict:
    """Calcule le socle de KPI nationaux presente sur la vue nationale."""
    critique = cantons[cantons["priorite"] == "Critique"]
    exposed_classes = {"Eleve", "Tres eleve"}

    return {
        "n_cantons": int(len(cantons)),
        "n_regions": int(cantons["region"].nunique()),
        "n_prefectures": int(cantons["prefecture"].nunique()),
        "population_totale": int(cantons["population"].sum()),
        "n_cantons_critiques": int(len(critique)),
        "part_cantons_critiques": float(len(critique) / len(cantons) * 100),
        "population_critique": int(critique["population"].sum()),
        "part_population_critique": float(critique["population"].sum() / cantons["population"].sum() * 100),
        "n_infrastructures": int(len(infrastructures)),
        "n_coso": int((infrastructures["source"] == "COSO").sum()),
        "n_tde": int((infrastructures["source"] == "TdE").sum()),
        "n_infra_exposees": int(
            infrastructures["canton"].isin(
                cantons.loc[cantons["classe_fri"].isin(exposed_classes), "canton"]
            ).sum()
        ),
        "wui_moyen": float(cantons["WUI"].mean()),
        "part_sans_infra": float(
            cantons.loc[~cantons["infrastructure_documentee"], "population"].sum()
            / cantons["population"].sum()
            * 100
        ),
        "population_sans_infra": int(cantons.loc[~cantons["infrastructure_documentee"], "population"].sum()),
    }


def regional_summary(cantons: pd.DataFrame) -> pd.DataFrame:
    """Synthese population, FRI moyen et couverture documentaire par region."""
    summary = cantons.groupby("region").agg(
        cantons=("canton", "count"),
        population=("population", "sum"),
        fri_moyen=("FRI", "mean"),
        wui_moyen=("WUI", "mean"),
        cantons_couverts=("infrastructure_documentee", "sum"),
    )
    summary["taux_couverture_pct"] = (summary["cantons_couverts"] / summary["cantons"] * 100).round(1)
    summary["part_population_pct"] = (summary["population"] / summary["population"].sum() * 100).round(1)
    summary["fri_moyen"] = summary["fri_moyen"].round(3)
    summary["wui_moyen"] = summary["wui_moyen"].round(3)
    return summary.sort_values("population", ascending=False)


def priority_distribution(cantons: pd.DataFrame) -> pd.DataFrame:
    """Repartition des cantons et de la population par niveau de priorite."""
    from config.settings import PRIORITY_LEVELS

    summary = cantons.groupby("priorite").agg(
        cantons=("canton", "count"),
        population=("population", "sum"),
    ).reindex(PRIORITY_LEVELS)
    summary["part_population_pct"] = (summary["population"] / cantons["population"].sum() * 100).round(1)
    summary["part_cantons_pct"] = (summary["cantons"] / len(cantons) * 100).round(1)
    return summary
