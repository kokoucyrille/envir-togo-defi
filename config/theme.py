"""Charte graphique de l'application.

La palette est analytique : chaque couleur porte une signification decisionnelle
et n'est jamais utilisee a des fins purement decoratives. L'identite generale de
l'interface (navigation, en-tete, accents) est construite autour du vert
institutionnel, en reference a l'environnement et aux ressources en eau.
"""

from __future__ import annotations

# Couleurs institutionnelles
COLOR_GREEN = "#1E7A46"       # institutionnel / environnement / situation favorable
COLOR_GREEN_DARK = "#12452A"  # vert fonce (fond menu, hover, degrades)
COLOR_GREEN_LIGHT = "#E8F3EC" # vert tres clair (fonds, survols legers)
COLOR_BLUE = "#1B6FA8"        # eau / infrastructures
COLOR_DARK_BLUE = "#0B2545"   # texte fort / fond header
COLOR_WHITE = "#FFFFFF"
COLOR_LIGHT_GREY = "#F4F6F8"
COLOR_GREY = "#8C8C8C"

# Couleurs du drapeau togolais, utilisees en filet discret (liseres, accents)
COLOR_FLAG_YELLOW = "#FFCE00"
COLOR_FLAG_RED = "#D21034"

# Palette analytique de priorite (reprise de l'EDA de reference)
PRIORITY_COLORS = {
    "Critique": "#B23A48",
    "Elevee": "#D98E04",
    "Moyenne": "#E4C580",
    "Surveillance": "#3A7D44",
}

# Palette analytique de risque (FRI) -- identique aux cartes officielles de l'EDA
FRI_COLORS = {
    "Tres faible": "#2E7D46",
    "Faible": "#8FBF6E",
    "Moyen": "#F2E28C",
    "Eleve": "#E8973B",
    "Tres eleve": "#B23A48",
}

# Palette source d'infrastructure
SOURCE_COLORS = {
    "COSO": COLOR_DARK_BLUE,
    "TdE": "#C9A961",
}

PLOTLY_TEMPLATE = "plotly_white"

CUSTOM_CSS = f"""
<style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    .block-container {{
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}

    /* ------------------------------------------------------------------ */
    /* Bandeau institutionnel (en-tete de page)                           */
    /* ------------------------------------------------------------------ */
    .institution-header {{
        background: linear-gradient(120deg, {COLOR_GREEN_DARK} 0%, {COLOR_GREEN} 100%);
        color: {COLOR_WHITE};
        padding: 1.1rem 1.6rem;
        border-radius: 10px;
        margin-bottom: 1.2rem;
        border-left: 5px solid {COLOR_FLAG_YELLOW};
        box-shadow: 0 2px 10px rgba(18, 69, 42, 0.18);
    }}
    .institution-header-row {{
        display: flex;
        align-items: center;
        gap: 1.1rem;
    }}
    .institution-header .header-logo {{
        width: 58px;
        height: 58px;
        border-radius: 50%;
        background-color: {COLOR_WHITE};
        padding: 4px;
        box-shadow: 0 0 0 2px {COLOR_FLAG_YELLOW};
        flex-shrink: 0;
    }}
    .institution-header .line1 {{
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        opacity: 0.9;
        margin: 0;
        font-weight: 600;
    }}
    .institution-header .line2 {{
        font-size: 0.78rem;
        opacity: 0.85;
        margin: 0 0 0.5rem 0;
    }}
    .institution-header .title {{
        font-size: 1.35rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.3;
    }}
    .institution-header .subtitle {{
        font-size: 0.92rem;
        opacity: 0.92;
        margin: 0.15rem 0 0 0;
    }}

    div[data-testid="stMetric"] {{
        background-color: {COLOR_LIGHT_GREY};
        border: 1px solid #E4E7EB;
        border-left: 4px solid {COLOR_BLUE};
        border-radius: 6px;
        padding: 0.7rem 0.9rem 0.5rem 0.9rem;
    }}
    div[data-testid="stMetricLabel"] {{
        font-size: 0.80rem;
        color: {COLOR_GREY};
    }}

    .decision-block {{
        background-color: {COLOR_GREEN_LIGHT};
        border-radius: 8px;
        padding: 1rem 1.2rem;
        border-left: 4px solid {COLOR_GREEN};
        margin-bottom: 0.8rem;
    }}
    .decision-block h4 {{
        margin-top: 0;
        margin-bottom: 0.4rem;
        font-size: 0.95rem;
        color: {COLOR_GREEN_DARK};
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

    .priority-badge {{
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        color: white;
    }}

    .app-footer {{
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid #E4E7EB;
        font-size: 0.78rem;
        color: {COLOR_GREY};
        text-align: center;
    }}

    /* ------------------------------------------------------------------ */
    /* Barre laterale generale                                            */
    /* ------------------------------------------------------------------ */
    section[data-testid="stSidebar"] {{
        background-color: {COLOR_WHITE};
        border-right: 1px solid #E4E7EB;
    }}
    section[data-testid="stSidebar"] > div:first-child {{
        padding-top: 0.6rem;
    }}

    /* Bloc logo + identite, en tete de la sidebar */
    .sidebar-brand {{
        background: linear-gradient(160deg, {COLOR_GREEN_DARK} 0%, {COLOR_GREEN} 100%);
        border-radius: 12px;
        padding: 1rem 1rem 0.9rem 1rem;
        margin-bottom: 1.1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(18, 69, 42, 0.20);
    }}
    .sidebar-brand img {{
        border-radius: 50%;
        background-color: {COLOR_WHITE};
        padding: 4px;
        box-shadow: 0 0 0 2px {COLOR_FLAG_YELLOW};
    }}
    .sidebar-brand .brand-title {{
        color: {COLOR_WHITE};
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin: 0.6rem 0 0.1rem 0;
    }}
    .sidebar-brand .brand-subtitle {{
        color: rgba(255,255,255,0.85);
        font-size: 0.70rem;
        margin: 0;
        line-height: 1.3;
    }}

    .sidebar-section-label {{
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        color: {COLOR_GREY};
        text-transform: uppercase;
        margin: 0.2rem 0 0.5rem 0.2rem;
    }}

    /* ------------------------------------------------------------------ */
    /* Menu de navigation (st.radio transforme en menu vertical)          */
    /* ------------------------------------------------------------------ */
    section[data-testid="stSidebar"] div[role="radiogroup"] {{
        gap: 0.3rem;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label {{
        display: flex;
        align-items: center;
        width: 100%;
        padding: 0.62rem 0.85rem;
        margin: 0 0 0.05rem 0;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.15s ease, color 0.15s ease, transform 0.1s ease;
        border: 1px solid transparent;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background-color: {COLOR_GREEN_LIGHT};
        border-color: rgba(30, 122, 70, 0.25);
    }}
    /* Masque le rond de selection natif du radio */
    section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {{
        display: none;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {{
        font-size: 0.90rem;
        font-weight: 500;
        color: #1F2A24;
        margin: 0;
    }}
    /* Element actif du menu */
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
        background-color: {COLOR_GREEN};
        border-color: {COLOR_GREEN};
        box-shadow: 0 2px 6px rgba(30, 122, 70, 0.30);
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) div[data-testid="stMarkdownContainer"] p {{
        color: {COLOR_WHITE};
        font-weight: 700;
    }}

    section[data-testid="stSidebar"] hr {{
        border-color: #E4E7EB;
        margin: 1rem 0;
    }}
    section[data-testid="stSidebar"] .stCaption, section[data-testid="stSidebar"] small {{
        color: {COLOR_GREY};
    }}

    /* ------------------------------------------------------------------ */
    /* Widgets de filtrage (selectbox / multiselect) en accent vert       */
    /* ------------------------------------------------------------------ */
    div[data-baseweb="select"] > div {{
        border-color: #D8E3DC !important;
    }}
    div[data-baseweb="select"] > div:hover {{
        border-color: {COLOR_GREEN} !important;
    }}
    div[data-baseweb="tag"] {{
        background-color: {COLOR_GREEN} !important;
    }}

    /* Onglets */
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {COLOR_GREEN_DARK} !important;
        border-bottom-color: {COLOR_GREEN} !important;
    }}
    div[data-baseweb="tab-highlight"] {{
        background-color: {COLOR_GREEN} !important;
    }}

    /* Boutons */
    .stButton > button, .stDownloadButton > button {{
        border-color: {COLOR_GREEN};
        color: {COLOR_GREEN_DARK};
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        border-color: {COLOR_GREEN};
        background-color: {COLOR_GREEN_LIGHT};
        color: {COLOR_GREEN_DARK};
    }}
</style>
"""


def priority_badge_html(priority: str) -> str:
    """Retourne un badge HTML colore pour un niveau de priorite donne."""
    color = PRIORITY_COLORS.get(priority, "#8C8C8C")
    return f'<span class="priority-badge" style="background-color:{color};">{priority}</span>'
