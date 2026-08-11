"""Acces aux resultats de priorisation territoriale (Water Urgency Index).

Le WUI et le niveau de priorite ne sont jamais recalcules ici : ils sont lus tels
quels depuis les fichiers produits par EDA_Eau_Togo.ipynb, conformement a la consigne
de ne pas reponderer arbitrairement l'indice dans l'application.
"""

from __future__ import annotations

import pandas as pd


def get_top_n(top20: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Retourne les n premiers territoires du classement de reference."""
    return top20.head(n)


def get_canton_profile(cantons: pd.DataFrame, canton_name: str) -> pd.Series | None:
    """Retourne la ligne complete d'un canton donne, ou None si introuvable."""
    match = cantons[cantons["canton"] == canton_name]
    if match.empty:
        return None
    return match.iloc[0]


def explain_priority_factors(profile: pd.Series, cantons: pd.DataFrame) -> list[str]:
    """Construit la liste des facteurs contributifs explicatifs du niveau de priorite
    d'un canton, par comparaison a la distribution nationale (quartiles)."""
    factors: list[str] = []

    q75_pop = cantons["population"].quantile(0.75)
    q75_fri = cantons["FRI"].quantile(0.75)
    q25_rwi = cantons["rwi_min"].quantile(0.25)

    if profile["population"] >= q75_pop:
        factors.append(
            f"Population elevee ({profile['population']:,.0f} habitants), superieure au 3e quartile national."
        )
    if profile["FRI"] >= q75_fri:
        factors.append(
            f"Risque d'inondation eleve (FRI = {profile['FRI']:.3f}), superieur au 3e quartile national."
        )
    if profile["rwi_min"] <= q25_rwi:
        factors.append(
            f"Vulnerabilite economique marquee (RWI = {profile['rwi_min']:.2f}), "
            "inferieure au 1er quartile national."
        )
    if not profile["infrastructure_documentee"]:
        factors.append("Aucune infrastructure documentee (COSO ou TdE) recensee dans ce canton.")

    if not factors:
        factors.append("Aucun facteur ne depasse les seuils de quartile national retenus dans l'EDA.")

    return factors


def recommend_action(profile: pd.Series, cantons: pd.DataFrame) -> dict:
    """Applique la matrice de decision de l'EDA de reference (section 25) au profil
    d'un canton pour proposer une action coherente avec les facteurs identifies."""
    q75_pop = cantons["population"].quantile(0.75)
    pop_high = profile["population"] >= q75_pop
    fri_high = profile["FRI"] >= 0.29  # seuil "Eleve" repris de l'EDA
    no_infra = not profile["infrastructure_documentee"]
    vuln_high = profile["rwi_min"] <= 0

    if no_infra and fri_high:
        return {
            "situation": "Absence d'infrastructure documentee et risque d'inondation eleve",
            "action": "Verification terrain prioritaire, puis mesures de resilience si un deficit est confirme",
            "horizon": "Court terme (0-2 ans)",
        }
    if pop_high and no_infra:
        return {
            "situation": "Population elevee et infrastructure non documentee dans les sources disponibles",
            "action": "Verification terrain puis extension de la couverture si le deficit est confirme",
            "horizon": "Court a moyen terme (0-3 ans)",
        }
    if pop_high and fri_high:
        return {
            "situation": "Population elevee et risque d'inondation eleve",
            "action": "Rehabilitation et protection des infrastructures existantes",
            "horizon": "Moyen terme (3-5 ans)",
        }
    if fri_high and vuln_high:
        return {
            "situation": "Risque d'inondation eleve et vulnerabilite economique marquee",
            "action": "Mesures de resilience (drainage, protection, surelevation des ouvrages)",
            "horizon": "Moyen terme (3-5 ans)",
        }
    if vuln_high:
        return {
            "situation": "Vulnerabilite economique marquee sans risque d'inondation majeur",
            "action": "Extension prioritaire a cout maitrise",
            "horizon": "Moyen terme (3-5 ans)",
        }
    if no_infra:
        return {
            "situation": "Couverture documentaire faible",
            "action": "Recensement terrain avant toute decision d'investissement",
            "horizon": "Court terme (0-2 ans)",
        }
    return {
        "situation": "Situation relativement favorable au regard des facteurs disponibles",
        "action": "Maintenance courante et suivi standard",
        "horizon": "Continu",
    }
