"""Parametres globaux de l'application : chemins, seuils et constantes analytiques.

Toutes les valeurs numeriques ici reprises (seuils FRI, ponderations du Water Urgency
Index, quantiles de priorite) proviennent directement du notebook de reference
``EDA_Eau_Togo.ipynb`` et ne doivent pas etre modifiees sans mettre a jour l'analyse
source correspondante.
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Chemins
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "geodata"
ASSETS_DIR = BASE_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "logo" / "images.png"

CANTONS_GEOJSON = DATA_DIR / "cantons_wui.geojson"
CANTONS_CSV = DATA_DIR / "cantons_water_urgency_index.csv"
TOP20_CSV = DATA_DIR / "top20_zones_prioritaires.csv"
DATA_DICTIONARY_CSV = DATA_DIR / "data_dictionary.csv"
COSO_CSV = DATA_DIR / "infrastructures_coso.csv"
COSO_ALL_CSV = DATA_DIR / "infrastructures_coso_all.csv"
TDE_CSV = DATA_DIR / "infrastructures_tde.csv"

# ---------------------------------------------------------------------------
# Identite institutionnelle
# ---------------------------------------------------------------------------
APP_TITLE = "Diagnostic et priorisation des interventions hydrauliques au Togo"
APP_SUBTITLE = "Tableau de bord d'aide a la decision territoriale"
INSTITUTION_LINE_1 = "REPUBLIQUE TOGOLAISE"
INSTITUTION_LINE_2 = "Ministere de l'Efficacite du Service Public et de la Transformation Numerique"

AUTHOR_NAME = "DAYO Kokou Cyrille"
AUTHOR_TITLE = "Ingenieur de Travaux Informatiques"
AUTHOR_BIO = (
    "Passionne par la Data Science, le developpement d'applications decisionnelles, "
    "l'intelligence artificielle et la transformation numerique."
)
AUTHOR_EMAIL = "cyridayo@gmail.com"
AUTHOR_PHONE = "+228 90 51 59 28"
AUTHOR_WHATSAPP = "+228 90 51 59 28"
AUTHOR_LINKEDIN = "https://www.linkedin.com/in/dkc023/"
AUTHOR_GITHUB = "https://github.com/kokoucyrille/"

# ---------------------------------------------------------------------------
# Navigation (5 sections, conformement au cahier des charges)
# ---------------------------------------------------------------------------
PAGES = [
    ''
]

# ---------------------------------------------------------------------------
# Seuils du FRI (repris de la legende officielle des cartes -- section 12 de l'EDA)
# ---------------------------------------------------------------------------
FRI_CLASSES = ["Tres faible", "Faible", "Moyen", "Eleve", "Tres eleve"]
FRI_THRESHOLDS = {
    "Tres faible": (0.0, 0.10),
    "Faible": (0.10, 0.17),
    "Moyen": (0.17, 0.29),
    "Eleve": (0.29, 0.44),
    "Tres eleve": (0.44, 1.01),
}

# ---------------------------------------------------------------------------
# Water Urgency Index -- ponderation de reference (section 14 de l'EDA)
# Reutilisee uniquement pour rejouer les scenarios de simulation ; le score
# WUI affiche dans l'application est toujours celui calcule dans le notebook
# et charge depuis cantons_water_urgency_index.csv, jamais recalcule avec de
# nouvelles ponderations.
# ---------------------------------------------------------------------------
WUI_WEIGHTS = {
    "population": 0.35,
    "fri": 0.35,
    "vulnerabilite_eco": 0.20,
    "couverture_documentaire": 0.10,
}
WUI_SENSITIVITY_NOTE = (
    "Le classement des 20 cantons les plus urgents reste stable a 70 % au minimum "
    "(14 a 20 cantons communs sur 20) face a quatre jeux de ponderation alternatifs "
    "testes dans l'EDA de reference, y compris des ponderations extremes centrees sur "
    "une seule dimension."
)

PRIORITY_LEVELS = ["Critique", "Elevee", "Moyenne", "Surveillance"]

# ---------------------------------------------------------------------------
# Scenarios prospectifs (section 18 de l'EDA) -- parametres de simulation
# ---------------------------------------------------------------------------
SCENARIOS = {
    "S0": {
        "label": "S0 -- Statu quo (Business as Usual)",
        "description": "Poursuite des tendances observees, sans intervention nouvelle.",
        "reduction_fri": 0.0,
        "reduction_vuln": 0.0,
        "ajout_couverture": 0.0,
    },
    "S1": {
        "label": "S1 -- Rehabilitation ciblee",
        "description": (
            "Hypothese : reduction de 20 % de la vulnerabilite economique percue des "
            "cantons critiques via l'amelioration de services de base associes."
        ),
        "reduction_fri": 0.0,
        "reduction_vuln": 0.20,
        "ajout_couverture": 0.0,
    },
    "S2": {
        "label": "S2 -- Extension de la couverture documentee",
        "description": (
            "Hypothese : 50 % des cantons critiques sans infrastructure documentee "
            "recoivent un ouvrage verifie."
        ),
        "reduction_fri": 0.0,
        "reduction_vuln": 0.0,
        "ajout_couverture": 0.50,
    },
    "S3": {
        "label": "S3 -- Resilience face au risque",
        "description": (
            "Hypothese : reduction de 15 % du risque effectif d'inondation via des "
            "mesures de drainage et de protection."
        ),
        "reduction_fri": 0.15,
        "reduction_vuln": 0.0,
        "ajout_couverture": 0.0,
    },
    "S4": {
        "label": "S4 -- Strategie integree",
        "description": "Cumul des leviers de rehabilitation, d'extension et de resilience (S1 + S2 + S3).",
        "reduction_fri": 0.15,
        "reduction_vuln": 0.20,
        "ajout_couverture": 0.50,
    },
}

# ---------------------------------------------------------------------------
# Messages methodologiques a rappeler systematiquement dans l'interface
# ---------------------------------------------------------------------------
DISCLAIMER_COVERAGE = (
    "Les infrastructures presentees correspondent aux sources documentees disponibles "
    "dans l'etude (programme COSO et points TdE) et ne constituent pas un inventaire "
    "national exhaustif."
)
DISCLAIMER_NO_INFRA = (
    "Une infrastructure non documentee ne signifie pas qu'elle n'existe pas "
    "physiquement. Une verification terrain est necessaire avant toute decision "
    "d'investissement."
)
DISCLAIMER_SCENARIOS = (
    "Les resultats des scenarios sont des simulations sous hypotheses explicites. "
    "Ils ne constituent pas des previsions certaines ni des engagements de resultats."
)
DISCLAIMER_FUNCTIONALITY = (
    "Aucune donnee de statut operationnel (fonctionnalite) n'est disponible dans les "
    "sources fournies. Aucun taux de fonctionnalite n'est donc affiche ni estime."
)
