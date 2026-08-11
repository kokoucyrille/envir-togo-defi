"""Fonctions de formatage d'affichage (nombres, pourcentages)."""

from __future__ import annotations


def format_number(value: float, decimals: int = 0) -> str:
    """Formate un nombre avec espace comme separateur de milliers (convention francophone)."""
    if value is None:
        return "-"
    text = f"{value:,.{decimals}f}"
    return text.replace(",", " ")


def format_population(value: float) -> str:
    return format_number(value, decimals=0)


def format_percent(value: float, decimals: int = 1) -> str:
    if value is None:
        return "-"
    return f"{value:.{decimals}f} %"


def format_index(value: float, decimals: int = 3) -> str:
    if value is None:
        return "-"
    return f"{value:.{decimals}f}"
