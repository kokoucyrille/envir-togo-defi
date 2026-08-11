"""Tests des fonctions de priorisation, d'explication et de scenarios."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analytics.priorities import explain_priority_factors, get_canton_profile, recommend_action
from analytics.scenarios import prepare_normalized_components, scenario_impact_summary
from config.settings import CANTONS_CSV, SCENARIOS


def _cantons() -> pd.DataFrame:
    return pd.read_csv(CANTONS_CSV)


def test_get_canton_profile_returns_none_for_unknown_canton():
    cantons = _cantons()
    assert get_canton_profile(cantons, "Canton Inexistant XYZ") is None


def test_get_canton_profile_returns_row_for_known_canton():
    cantons = _cantons()
    known = cantons.iloc[0]["canton"]
    profile = get_canton_profile(cantons, known)
    assert profile is not None
    assert profile["canton"] == known


def test_explain_priority_factors_returns_non_empty_list():
    cantons = _cantons()
    top_canton = cantons.sort_values("WUI", ascending=False).iloc[0]
    factors = explain_priority_factors(top_canton, cantons)
    assert len(factors) > 0


def test_recommend_action_returns_expected_keys():
    cantons = _cantons()
    profile = cantons.iloc[0]
    rec = recommend_action(profile, cantons)
    assert {"situation", "action", "horizon"} <= set(rec.keys())


def test_scenario_impact_summary_s0_has_no_effect():
    cantons = _cantons()
    result = scenario_impact_summary(cantons, SCENARIOS["S0"], scope="critique")
    assert result["reduction_wui_pct"] == 0.0


def test_scenario_impact_summary_s4_reduces_wui():
    cantons = _cantons()
    result = scenario_impact_summary(cantons, SCENARIOS["S4"], scope="critique")
    assert result["reduction_wui_pct"] > 0
    assert result["wui_moyen_simule"] < result["wui_moyen_actuel"]


def test_prepare_normalized_components_bounds():
    cantons = _cantons()
    prepared = prepare_normalized_components(cantons)
    for col in ["n_pop", "n_fri", "n_vuln_eco"]:
        assert prepared[col].min() >= 0
        assert prepared[col].max() <= 1
