"""Recommandations strategiques structurees, reprises et adaptees de l'EDA de reference
(section 27 du notebook). Chaque recommandation reste tracable a un resultat calcule
dans l'analyse source."""

from __future__ import annotations

STRATEGIC_RECOMMENDATIONS = [
    {
        "titre": "Combler la lacune de donnees sur la fonctionnalite des ouvrages",
        "probleme": (
            "Aucun champ de statut operationnel n'est disponible dans les donnees fournies, "
            "alors que le schema source de la Togolaise des Eaux en prevoit un."
        ),
        "territoire": "National",
        "action": (
            "Activer la collecte et la publication reguliere du champ de fonctionnalite deja "
            "prevu dans le schema de donnees TdE, et l'etendre aux ouvrages COSO en exploitation."
        ),
        "justification": "100 % des 218 sous-projets COSO et 67 points TdE sont depourvus de statut operationnel exploitable.",
        "impact": "Rend possible, pour la premiere fois, le calcul d'un taux de fonctionnalite national.",
        "kpi": "Taux de couverture du champ fonctionnalite dans les bases sectorielles.",
        "horizon": "Court terme (0-2 ans)",
    },
    {
        "titre": "Corriger la geolocalisation des sous-projets COSO",
        "probleme": "33,5 % des sous-projets COSO presentent des coordonnees de remplissage (0, 0) ou une geometrie manquante.",
        "territoire": "Regions Centrale, Kara, Savanes",
        "action": "Campagne de correction des coordonnees GPS a partir des fiches de localisation existantes, avec verification terrain pour les cas ambigus.",
        "justification": "Le taux de jointure spatiale fiable passerait de 38 % a un niveau proche de 100 % apres correction.",
        "impact": "Fiabilisation des cartes utilisees pour le pilotage et la communication institutionnelle.",
        "kpi": "Part de sous-projets avec coordonnees valides dans la plage geographique du Togo.",
        "horizon": "Court terme (0-2 ans)",
    },
    {
        "titre": "Etendre la couverture documentaire en region Plateaux",
        "probleme": "La region Plateaux, qui porte pres d'un cinquieme de la population nationale, n'apparait que dans un seul point d'infrastructure documente.",
        "territoire": "Region Plateaux",
        "action": "Lancer un recensement terrain des ouvrages hydrauliques existants dans les cantons a forte population de la region, avant toute decision d'extension.",
        "justification": "0,9 % des cantons de la region disposent d'une infrastructure documentee, contre 50,7 % en Savanes.",
        "impact": "Amelioration de la fiabilite des futures priorisations pour environ 1,67 million d'habitants.",
        "kpi": "Nombre de cantons de Plateaux dotes d'un inventaire d'ouvrages verifie.",
        "horizon": "Court a moyen terme (0-3 ans)",
    },
    {
        "titre": "Prioriser la resilience dans les cantons cotiers a risque tres eleve",
        "probleme": "Les cantons classes en risque tres eleve portent une population cumulee significative et concentrent l'essentiel des points TdE exposes.",
        "territoire": "Cantons du Grand Lome en zone cotiere",
        "action": "Etudes hydrauliques locales et mesures de protection ou de surelevation des ouvrages TdE deja identifies comme exposes.",
        "justification": "46,3 % des points TdE se situent en zone a risque eleve ou tres eleve.",
        "impact": "Reduction simulee de 5,3 % du WUI moyen des cantons critiques sous le seul levier de resilience.",
        "kpi": "Nombre d'infrastructures TdE protegees rapporte au nombre total d'infrastructures TdE exposees.",
        "horizon": "Moyen terme (3-5 ans)",
    },
    {
        "titre": "Deployer une strategie integree sur les cantons prioritaires Critique",
        "probleme": "46 % de la population nationale reside dans les 39 cantons cumulant les facteurs defavorables.",
        "territoire": "39 cantons de priorite Critique",
        "action": "Deploiement combine de rehabilitation, d'extension de la couverture documentaire et de mesures de resilience.",
        "justification": "Le scenario integre simule une reduction moyenne du WUI de 20,5 % et fait repasser 26 des 39 cantons sous le seuil critique.",
        "impact": "Jusqu'a 1,2 million de personnes concernees par une amelioration significative du score d'urgence, sous hypotheses documentees.",
        "kpi": "Nombre de cantons en priorite Critique ; WUI moyen national.",
        "horizon": "Moyen a long terme (3-10 ans)",
    },
]


DECISION_MATRIX = [
    {
        "situation": "Population elevee et infrastructure non documentee",
        "action": "Verification terrain puis extension si deficit confirme",
    },
    {
        "situation": "Population elevee et risque d'inondation eleve",
        "action": "Rehabilitation et protection des ouvrages existants",
    },
    {
        "situation": "Risque d'inondation eleve et vulnerabilite economique elevee",
        "action": "Resilience prioritaire (drainage, protection, surelevation)",
    },
    {
        "situation": "Vulnerabilite economique elevee sans risque d'inondation majeur",
        "action": "Extension prioritaire a cout maitrise",
    },
    {
        "situation": "Couverture documentaire faible en region entiere",
        "action": "Recensement terrain avant toute decision d'investissement",
    },
    {
        "situation": "Risque eleve avec infrastructure documentee existante",
        "action": "Prevention et maintenance preventive",
    },
    {
        "situation": "Situation favorable (WUI en Surveillance)",
        "action": "Maintenance courante et suivi standard",
    },
]
