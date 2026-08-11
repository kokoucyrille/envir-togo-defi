"""Test de lancement complet de l'application (toutes les pages, sans exception)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from streamlit.testing.v1 import AppTest

APP_PATH = str(Path(__file__).resolve().parent.parent / "app.py")

PAGES = [
    "Vue nationale",
    "Infrastructures",
    "Besoins et deficits",
    "Risques",
    "Priorites et scenarios",
    "A propos et methodologie",
]


def test_app_launches_without_exception():
    at = AppTest.from_file(APP_PATH, default_timeout=90)
    at.run()
    assert len(at.exception) == 0


def test_all_pages_render_without_exception():
    for page in PAGES:
        at = AppTest.from_file(APP_PATH, default_timeout=90)
        at.run()
        at.sidebar.radio[0].set_value(page).run()
        assert len(at.exception) == 0, f"Exception sur la page {page} : {at.exception}"
