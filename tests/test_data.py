"""Tests du chargement et de la validation des donnees."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.settings import CANTONS_CSV, COSO_CSV, TDE_CSV, TOP20_CSV
from data.validators import validate_cantons, validate_top20


def test_cantons_csv_exists_and_loads():
    df = pd.read_csv(CANTONS_CSV)
    assert len(df) == 388
    assert "WUI" in df.columns
    assert "priorite" in df.columns


def test_top20_csv_exists_and_loads():
    df = pd.read_csv(TOP20_CSV)
    assert len(df) == 20


def test_infrastructure_csv_load():
    coso = pd.read_csv(COSO_CSV)
    tde = pd.read_csv(TDE_CSV)
    assert len(coso) > 0
    assert len(tde) > 0
    assert "latitude" in coso.columns and "longitude" in coso.columns


def test_validate_cantons_passes_on_reference_data():
    df = pd.read_csv(CANTONS_CSV)
    issues = validate_cantons(df)
    assert issues == []


def test_validate_top20_passes_on_reference_data():
    df = pd.read_csv(TOP20_CSV)
    issues = validate_top20(df)
    assert issues == []


def test_validate_cantons_detects_missing_region():
    df = pd.read_csv(CANTONS_CSV)
    broken = df[df["region"] != "Plateaux"]
    issues = validate_cantons(broken)
    assert any("Regions manquantes" in i for i in issues)
