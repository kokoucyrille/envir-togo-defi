"""Tests des calculs d'indicateurs nationaux et regionaux."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analytics.indicators import national_kpis, priority_distribution, regional_summary
from config.settings import CANTONS_CSV, COSO_CSV, TDE_CSV


def _load_infrastructures() -> pd.DataFrame:
    coso = pd.read_csv(COSO_CSV)
    tde = pd.read_csv(TDE_CSV)
    coso_c = coso[["title", "type", "region", "prefecture", "commune", "canton", "latitude", "longitude"]].copy()
    coso_c["source"] = "COSO"
    tde_c = tde[["title", "type", "region", "prefecture", "commune", "canton", "latitude", "longitude"]].copy()
    tde_c["source"] = "TdE"
    return pd.concat([coso_c, tde_c], ignore_index=True)


def test_national_kpis_counts_match_reference():
    cantons = pd.read_csv(CANTONS_CSV)
    infra = _load_infrastructures()
    kpis = national_kpis(cantons, infra)

    assert kpis["n_cantons"] == 388
    assert kpis["n_cantons_critiques"] == 39
    assert kpis["n_regions"] == 5
    assert round(kpis["part_population_critique"], 0) == 46


def test_regional_summary_sums_to_total_population():
    cantons = pd.read_csv(CANTONS_CSV)
    summary = regional_summary(cantons)
    assert abs(summary["population"].sum() - cantons["population"].sum()) < 1


def test_priority_distribution_sums_to_total_cantons():
    cantons = pd.read_csv(CANTONS_CSV)
    dist = priority_distribution(cantons)
    assert dist["cantons"].sum() == len(cantons)
    assert dist.loc["Critique", "cantons"] == 39
