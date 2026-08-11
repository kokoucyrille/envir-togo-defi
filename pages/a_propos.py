"""Page complementaire -- A propos, methodologie, qualite des donnees et limites."""

from __future__ import annotations

import streamlit as st

from components.header import render_header
from config.settings import (
    AUTHOR_BIO,
    AUTHOR_EMAIL,
    AUTHOR_GITHUB,
    AUTHOR_LINKEDIN,
    AUTHOR_NAME,
    AUTHOR_PHONE,
    AUTHOR_TITLE,
    AUTHOR_WHATSAPP,
    DATA_DICTIONARY_CSV,
)


def render(data_dictionary) -> None:
    render_header(
        page_title="A propos et methodologie",
        page_subtitle="Sources, qualite des donnees, limites et contact",
    )

    st.markdown("### Sources")
    st.markdown(
        "- Indice de risque d'inondation (FRI) par canton -- Togo AI Lab, fevrier 2026 (couverture nationale, 388 cantons).\n"
        "- Sous-projets d'hydraulique rurale du programme COSO, finance par la Banque mondiale.\n"
        "- Points de forages et chateaux d'eau geres par la Togolaise des Eaux (TdE).\n"
        "- Recensement demographique 2010 (donnee de contexte, non utilisee pour le calcul du WUI)."
    )

    st.markdown("### Qualite des donnees")
    with st.expander("Consulter le data dictionary consolide"):
        st.dataframe(data_dictionary, width="stretch", hide_index=True)

    st.markdown("### Limites methodologiques")
    with st.expander("Consulter les limites de l'etude", expanded=True):
        st.markdown(
            "- Aucune source ne renseigne le statut de fonctionnalite operationnelle des ouvrages, "
            "bien que le schema de la TdE prevoie un champ correspondant non transmis dans l'extrait "
            "disponible. Aucun taux de fonctionnalite n'est donc calcule ni affiche.\n"
            "- Les sous-projets COSO et les points TdE couvrent des perimetres geographiques partiels "
            "et non recoupes ; leur absence dans un canton ne signifie pas l'absence physique "
            "d'infrastructure.\n"
            "- 33,5 % des sous-projets COSO presentent une geometrie manquante ou des coordonnees de "
            "remplissage (0, 0) ; une jointure combinee (spatiale puis attributaire) a ete utilisee "
            "pour rattacher 83,5 % des sous-projets a un canton.\n"
            "- Le recensement demographique mobilise date de 2010, tandis que la couche FRI integre "
            "une population modelisee plus recente ; les deux sources n'ont pas ete reconciliees.\n"
            "- Les scenarios prospectifs sont des simulations parametriques a hypotheses explicites, "
            "non des previsions calibrees sur des donnees d'impact observees.\n"
            "- Les correlations statistiques presentees dans l'EDA de reference ne demontrent aucune "
            "relation causale."
        )

    st.markdown("### A propos de l'application")
    st.markdown(
        f"""
        **{AUTHOR_NAME}**
        {AUTHOR_TITLE}

        {AUTHOR_BIO}

        Email : [{AUTHOR_EMAIL}](mailto:{AUTHOR_EMAIL})
        Telephone : {AUTHOR_PHONE}
        WhatsApp : {AUTHOR_WHATSAPP}
        LinkedIn : [{AUTHOR_LINKEDIN}]({AUTHOR_LINKEDIN})
        GitHub : [{AUTHOR_GITHUB}]({AUTHOR_GITHUB})
        """
    )
