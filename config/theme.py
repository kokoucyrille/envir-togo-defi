"""Charte graphique de l'application.

La palette est analytique : chaque couleur porte une signification decisionnelle
et n'est jamais utilisee a des fins purement decoratives.

Mise a jour : sidebar vert institutionnel, logo en en-tete, navigation repensee.
"""

from __future__ import annotations

# Couleurs institutionnelles
COLOR_GREEN        = "#1E7A46"   # vert institutionnel Togo / situation favorable
COLOR_GREEN_DARK   = "#155C34"   # vert fonce -- hover sidebar, fond actif
COLOR_GREEN_LIGHT  = "#E8F5EE"   # vert tres pale -- fond hover elements inactifs
COLOR_BLUE         = "#1B6FA8"   # eau / infrastructures
COLOR_DARK_BLUE    = "#0B2545"   # texte fort / bandeau header
COLOR_WHITE        = "#FFFFFF"
COLOR_LIGHT_GREY   = "#F4F6F8"
COLOR_GREY         = "#8C8C8C"
COLOR_GOLD         = "#C9A961"   # accent institutionnel (etoile du drapeau)

# Palette analytique de priorite (reprise de l'EDA de reference)
PRIORITY_COLORS = {
    "Critique":     "#B23A48",
    "Elevee":       "#D98E04",
    "Moyenne":      "#E4C580",
    "Surveillance": "#3A7D44",
}

# Palette analytique de risque (FRI) -- identique aux cartes officielles de l'EDA
FRI_COLORS = {
    "Tres faible": "#2E7D46",
    "Faible":      "#8FBF6E",
    "Moyen":       "#F2E28C",
    "Eleve":       "#E8973B",
    "Tres eleve":  "#B23A48",
}

# Palette source d'infrastructure
SOURCE_COLORS = {
    "COSO": COLOR_DARK_BLUE,
    "TdE":  COLOR_GOLD,
}

PLOTLY_TEMPLATE = "plotly_white"

CUSTOM_CSS = f"""
<style>
    /* ------------------------------------------------------------------ */
    /* Reset Streamlit chrome                                              */
    /* ------------------------------------------------------------------ */
    #MainMenu  {{visibility: hidden;}}
    footer     {{visibility: hidden;}}

    .block-container {{
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}

    /* ------------------------------------------------------------------ */
    /* SIDEBAR -- fond vert institutionnel                                 */
    /* ------------------------------------------------------------------ */
    section[data-testid="stSidebar"] {{
        background-color: {COLOR_GREEN};
        border-right: 3px solid {COLOR_GREEN_DARK};
    }}

    /* Logo dans la sidebar */
    section[data-testid="stSidebar"] img {{
        display: block;
        margin: 0 auto 0.5rem auto;
        padding: 0.8rem 0.6rem 0.4rem 0.6rem;
        background: {COLOR_WHITE};
        border-radius: 8px;
        width: 80% !important;
    }}

    /* Titre de navigation */
    section[data-testid="stSidebar"] h3 {{
        color: {COLOR_WHITE} !important;
        font-size: 0.70rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        margin: 0.8rem 0 0.4rem 0 !important;
        opacity: 0.80;
    }}

    /* Label du radio group (cache) */
    section[data-testid="stSidebar"] .stRadio > label {{
        color: {COLOR_WHITE} !important;
    }}

    /* Items de navigation (radio buttons) */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
        color: {COLOR_WHITE} !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        padding: 0.45rem 0.8rem !important;
        border-radius: 6px !important;
        margin-bottom: 0.15rem !important;
        transition: background 0.15s ease !important;
        cursor: pointer !important;
    }}

    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {{
        background-color: {COLOR_GREEN_DARK} !important;
    }}

    /* Item actif (selectionne) */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {{
        background-color: {COLOR_WHITE} !important;
        color: {COLOR_GREEN_DARK} !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.18) !important;
    }}

    /* Cacher les boutons radio natifs -- on garde juste le texte */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] input[type="radio"] {{
        display: none !important;
    }}

    /* Separateur sidebar */
    section[data-testid="stSidebar"] hr {{
        border-color: rgba(255,255,255,0.25) !important;
        margin: 0.8rem 0 !important;
    }}

    /* Caption / note methodologique sidebar */
    section[data-testid="stSidebar"] .stCaptionContainer,
    section[data-testid="stSidebar"] small,
    section[data-testid="stSidebar"] caption {{
        color: rgba(255,255,255,0.72) !important;
        font-size: 0.73rem !important;
        line-height: 1.45 !important;
    }}

    /* Scrollbar sidebar verte */
    section[data-testid="stSidebar"]::-webkit-scrollbar {{
        width: 4px;
    }}
    section[data-testid="stSidebar"]::-webkit-scrollbar-track {{
        background: {COLOR_GREEN_DARK};
    }}
    section[data-testid="stSidebar"]::-webkit-scrollbar-thumb {{
        background: rgba(255,255,255,0.35);
        border-radius: 4px;
    }}

    /* ------------------------------------------------------------------ */
    /* EN-TETE INSTITUTIONNEL                                              */
    /* ------------------------------------------------------------------ */
    .institution-header {{
        background: linear-gradient(135deg, {COLOR_DARK_BLUE} 0%, #143060 100%);
        color: {COLOR_WHITE};
        padding: 1.1rem 1.6rem;
        border-radius: 8px;
        margin-bottom: 1.2rem;
        border-left: 5px solid {COLOR_GREEN};
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    }}
    .institution-header .line1 {{
        font-size: 0.74rem;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        opacity: 0.80;
        margin: 0;
    }}
    .institution-header .line2 {{
        font-size: 0.78rem;
        opacity: 0.85;
        margin: 0 0 0.5rem 0;
    }}
    .institution-header .title {{
        font-size: 1.30rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.3;
    }}
    .institution-header .subtitle {{
        font-size: 0.88rem;
        opacity: 0.88;
        margin: 0.18rem 0 0 0;
        font-style: italic;
    }}

    /* ------------------------------------------------------------------ */
    /* CARTES KPI                                                          */
    /* ------------------------------------------------------------------ */
    div[data-testid="stMetric"] {{
        background-color: {COLOR_WHITE};
        border: 1px solid #DDE3EB;
        border-left: 4px solid {COLOR_GREEN};
        border-radius: 8px;
        padding: 0.75rem 1rem 0.55rem 1rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }}
    div[data-testid="stMetricLabel"] {{
        font-size: 0.79rem;
        color: {COLOR_GREY};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    div[data-testid="stMetricValue"] {{
        color: {COLOR_DARK_BLUE};
        font-weight: 700;
    }}

    /* ------------------------------------------------------------------ */
    /* BLOCS DECISION / ALERTE                                             */
    /* ------------------------------------------------------------------ */
    .decision-block {{
        background-color: {COLOR_LIGHT_GREY};
        border-radius: 8px;
        padding: 1rem 1.2rem;
        border-left: 4px solid {COLOR_GREEN};
        margin-bottom: 0.8rem;
    }}
    .decision-block h4 {{
        margin-top: 0;
        margin-bottom: 0.4rem;
        font-size: 0.95rem;
        color: {COLOR_DARK_BLUE};
    }}

    .alert-methodo {{
        background-color: #FFF6E5;
        border-left: 4px solid #D98E04;
        border-radius: 6px;
        padding: 0.7rem 1rem;
        font-size: 0.88rem;
        margin: 0.6rem 0 1rem 0;
        color: #5A4200;
    }}

    /* ------------------------------------------------------------------ */
    /* BADGES PRIORITE                                                     */
    /* ------------------------------------------------------------------ */
    .priority-badge {{
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        color: white;
    }}

    /* ------------------------------------------------------------------ */
    /* PIED DE PAGE                                                        */
    /* ------------------------------------------------------------------ */
    .app-footer {{
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 2px solid {COLOR_GREEN};
        font-size: 0.78rem;
        color: {COLOR_GREY};
        text-align: center;
    }}
    .app-footer strong {{
        color: {COLOR_GREEN};
    }}

    /* ------------------------------------------------------------------ */
    /* TITRES DE SECTIONS                                                  */
    /* ------------------------------------------------------------------ */
    h2, h3 {{
        color: {COLOR_DARK_BLUE};
    }}
    h2 {{
        border-bottom: 2px solid {COLOR_GREEN};
        padding-bottom: 0.3rem;
    }}
</style>
"""


def priority_badge_html(priority: str) -> str:
    """Retourne un badge HTML colore pour un niveau de priorite donne."""
    color = PRIORITY_COLORS.get(priority, "#8C8C8C")
    return f'<span class="priority-badge" style="background-color:{color};">{priority}</span>'
