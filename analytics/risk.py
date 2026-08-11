"""Analyses relatives au risque d'inondation (FRI) et a l'exposition des infrastructures."""

from __future__ import annotations

import pandas as pd


def risk_distribution(cantons: pd.DataFrame) -> pd.DataFrame:
    """Repartition des cantons et de la population par classe de risque FRI."""
    from config.settings import FRI_CLASSES

    summary = cantons.groupby("classe_fri").agg(
        cantons=("canton", "count"),
        population=("population", "sum"),
    ).reindex(FRI_CLASSES)
    summary["part_cantons_pct"] = (summary["cantons"] / len(cantons) * 100).round(1)
    summary["part_population_pct"] = (summary["population"] / cantons["population"].sum() * 100).round(1)
    return summary


def exposed_infrastructures(infrastructures: pd.DataFrame, cantons: pd.DataFrame) -> pd.DataFrame:
    """Retourne les infrastructures documentees situees dans un canton a risque eleve
    ou tres eleve, avec le detail du canton associe."""
    exposed_cantons = cantons.loc[cantons["classe_fri"].isin(["Eleve", "Tres eleve"]), "canton"]
    out = infrastructures[infrastructures["canton"].isin(exposed_cantons)].copy()
    fri_lookup = cantons.set_index("canton")[["FRI", "classe_fri"]]
    out = out.join(fri_lookup, on="canton")
    return out.sort_values("FRI", ascending=False)


def exposure_rate_by_source(infrastructures: pd.DataFrame, cantons: pd.DataFrame) -> pd.DataFrame:
    """Taux d'exposition au risque eleve/tres eleve, par source d'infrastructure."""
    exposed_cantons = set(cantons.loc[cantons["classe_fri"].isin(["Eleve", "Tres eleve"]), "canton"])
    rows = []
    for source, g in infrastructures.groupby("source"):
        n_total = len(g)
        n_exposed = g["canton"].isin(exposed_cantons).sum()
        rows.append({
            "Source": source,
            "Total documente": n_total,
            "Situees en zone a risque eleve/tres eleve": int(n_exposed),
            "Taux d'exposition (%)": round(100 * n_exposed / n_total, 1) if n_total else 0.0,
        })
    return pd.DataFrame(rows)


def risk_vulnerability_matrix(cantons: pd.DataFrame) -> pd.DataFrame:
    """Classe chaque canton dans une matrice risque (FRI) x vulnerabilite economique
    (RWI), selon des seuils de mediane, pour la visualisation croisee de la page Risques."""
    out = cantons.copy()
    med_fri = out["FRI"].median()
    med_rwi = out["rwi_min"].median()
    out["quadrant_risque"] = ((out["FRI"] >= med_fri).map({True: "FRI eleve", False: "FRI faible"}))
    out["quadrant_vulnerabilite"] = (
        (out["rwi_min"] <= med_rwi).map({True: "Vulnerabilite elevee", False: "Vulnerabilite faible"})
    )
    return out
