"""Validations legeres executees au chargement des donnees.

Ces controles ne recalculent aucune analyse : ils verifient uniquement que les
fichiers exportes par l'EDA de reference conservent la forme attendue, afin de
detecter rapidement une incoherence entre l'analyse source et l'application.
"""

from __future__ import annotations

import pandas as pd

EXPECTED_CANTON_COUNT = 388
EXPECTED_REGIONS = {"Maritime", "Plateaux", "Savanes", "Kara", "Centrale"}
EXPECTED_PRIORITY_LEVELS = {"Critique", "Elevee", "Moyenne", "Surveillance"}


def validate_cantons(df: pd.DataFrame) -> list[str]:
    """Retourne la liste des anomalies detectees sur la table des cantons. Une liste
    vide signifie que les controles sont passes avec succes."""
    issues: list[str] = []

    if len(df) != EXPECTED_CANTON_COUNT:
        issues.append(f"Nombre de cantons inattendu : {len(df)} (attendu {EXPECTED_CANTON_COUNT}).")

    missing_regions = EXPECTED_REGIONS - set(df["region"].unique())
    if missing_regions:
        issues.append(f"Regions manquantes : {sorted(missing_regions)}.")

    unexpected_priorities = set(df["priorite"].unique()) - EXPECTED_PRIORITY_LEVELS
    if unexpected_priorities:
        issues.append(f"Niveaux de priorite inattendus : {sorted(unexpected_priorities)}.")

    if df["WUI"].isna().any():
        issues.append("Des valeurs manquantes ont ete detectees dans le Water Urgency Index.")

    if not df["WUI"].between(0, 1).all():
        issues.append("Certaines valeurs de WUI sont hors de la plage attendue [0, 1].")

    if not df["FRI"].between(0, 1).all():
        issues.append("Certaines valeurs de FRI sont hors de la plage attendue [0, 1].")

    if (df["population"] < 0).any():
        issues.append("Des valeurs de population negatives ont ete detectees.")

    return issues


def validate_top20(df: pd.DataFrame) -> list[str]:
    """Verifie la coherence minimale du classement des 20 cantons prioritaires."""
    issues: list[str] = []
    if len(df) != 20:
        issues.append(f"Le classement prioritaire contient {len(df)} lignes (attendu 20).")
    required_cols = {"Canton", "Region", "Population", "FRI", "WUI", "Priorite"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        issues.append(f"Colonnes manquantes dans le Top 20 : {sorted(missing_cols)}.")
    return issues
