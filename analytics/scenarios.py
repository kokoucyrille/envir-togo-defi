"""Simulation parametrique des scenarios prospectifs.

Cette logique reproduit exactement la methode de simulation documentee dans
EDA_Eau_Togo.ipynb (section 18) : les composantes normalisees du Water Urgency Index
sont recalculees sous hypotheses explicites, avec la ponderation de reference
(config.settings.WUI_WEIGHTS), afin d'illustrer un effet potentiel et non une
prevision. Le WUI observe (colonne ``WUI`` des donnees chargees) n'est jamais modifie :
seule une copie de travail est utilisee pour la simulation.
"""

from __future__ import annotations

import pandas as pd

from config.settings import WUI_WEIGHTS


def _normalize(series: pd.Series) -> pd.Series:
    return (series - series.min()) / (series.max() - series.min())


def prepare_normalized_components(cantons: pd.DataFrame) -> pd.DataFrame:
    """Recalcule les composantes normalisees necessaires a la simulation, a partir des
    seules colonnes d'origine (population, FRI, RWI, couverture documentaire). Le score
    WUI de reference n'est pas modifie par cette preparation."""
    out = cantons.copy()
    out["n_pop"] = _normalize(out["population"])
    out["n_fri"] = _normalize(out["FRI"])
    out["n_vuln_eco"] = _normalize(-out["rwi_min"])
    out["n_sans_infra"] = (~out["infrastructure_documentee"]).astype(float)
    return out


def simulate_scenario(
    cantons_prepared: pd.DataFrame,
    reduction_fri: float = 0.0,
    reduction_vuln: float = 0.0,
    ajout_couverture: float = 0.0,
) -> pd.DataFrame:
    """Applique les parametres d'un scenario aux composantes normalisees et retourne
    une copie des donnees enrichie d'un WUI simule (colonne ``WUI_sim``)."""
    d = cantons_prepared.copy()
    d["n_fri_sim"] = (d["n_fri"] * (1 - reduction_fri)).clip(lower=0)
    d["n_vuln_eco_sim"] = (d["n_vuln_eco"] * (1 - reduction_vuln)).clip(lower=0)
    d["n_sans_infra_sim"] = (d["n_sans_infra"] * (1 - ajout_couverture)).clip(lower=0)
    d["WUI_sim"] = (
        d["n_pop"] * WUI_WEIGHTS["population"]
        + d["n_fri_sim"] * WUI_WEIGHTS["fri"]
        + d["n_vuln_eco_sim"] * WUI_WEIGHTS["vulnerabilite_eco"]
        + d["n_sans_infra_sim"] * WUI_WEIGHTS["couverture_documentaire"]
    )
    return d


def scenario_impact_summary(
    cantons: pd.DataFrame,
    scenario_params: dict,
    scope: str = "critique",
) -> dict:
    """Simule un scenario et retourne un resume d'impact comparable a celui de l'EDA de
    reference. Les composantes normalisees sont calculees sur l'ensemble des 388 cantons
    (comme dans le notebook source) avant de restreindre l'affichage au perimetre demande,
    afin que le WUI de reference et le WUI simule restent sur la meme echelle."""
    prepared_national = prepare_normalized_components(cantons)
    simulated_national = simulate_scenario(
        prepared_national,
        reduction_fri=scenario_params["reduction_fri"],
        reduction_vuln=scenario_params["reduction_vuln"],
        ajout_couverture=scenario_params["ajout_couverture"],
    )

    scope_df = simulated_national[simulated_national["priorite"] == "Critique"] if scope == "critique" else simulated_national

    wui_actuel_moyen = scope_df["WUI"].mean()
    wui_simule_moyen = scope_df["WUI_sim"].mean()
    reduction_pct = 100 * (1 - wui_simule_moyen / wui_actuel_moyen) if wui_actuel_moyen else 0.0

    seuil_critique = cantons["WUI"].quantile(0.90)
    n_sortis = int((scope_df["WUI_sim"] < seuil_critique).sum())
    population_beneficiaire = int(scope_df.loc[scope_df["WUI_sim"] < seuil_critique, "population"].sum())

    return {
        "territoires_cibles": int(len(scope_df)),
        "population_ciblee": int(scope_df["population"].sum()),
        "wui_moyen_actuel": round(float(wui_actuel_moyen), 3),
        "wui_moyen_simule": round(float(wui_simule_moyen), 3),
        "reduction_wui_pct": round(float(reduction_pct), 1),
        "cantons_sous_seuil_critique": n_sortis,
        "population_beneficiaire_potentielle": population_beneficiaire,
        "detail": scope_df,
    }
