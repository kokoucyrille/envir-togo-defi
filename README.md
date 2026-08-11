# Diagnostic et priorisation des interventions hydrauliques au Togo

Application Streamlit d'aide a la decision territoriale sur les infrastructures
hydrauliques et le risque d'inondation au Togo. Ce tableau de bord transforme les
resultats de l'etude analytique `EDA_Eau_Togo.ipynb` en un outil interactif destine a
des decideurs publics non specialistes de la donnee.

## Contexte et problematique

Le Togo dispose de donnees ouvertes ou institutionnelles sur ses infrastructures
hydrauliques, mais leur repartition territoriale, leur couverture et leur adequation
avec les besoins des populations restent difficiles a apprehender sans un outil de
synthese. Cette application repond a la question centrale :

> Ou faut-il intervenir en priorite, pourquoi, quelle action faut-il privilegier et
> quel impact peut-on raisonnablement attendre ?

## Objectifs

- Presenter un diagnostic national clair en moins de deux minutes de lecture.
- Cartographier le risque d'inondation, la pression demographique et la couverture
  documentaire en infrastructures.
- Identifier et expliquer les territoires prioritaires a partir du Water Urgency
  Index calcule dans l'EDA de reference.
- Simuler l'impact potentiel de scenarios d'intervention, sous hypotheses explicites.
- Fournir des recommandations operationnelles tracables aux resultats analytiques.

## Fonctionnalites

- **Vue nationale** : KPI nationaux, carte du Water Urgency Index, Top 10 des
  territoires prioritaires, message decisionnel de synthese.
- **Infrastructures** : carte interactive des sous-projets COSO et des points TdE,
  filtres geographiques en cascade, tableau telechargeable, avertissement
  methodologique sur la couverture partielle des sources.
- **Besoins et deficits** : carte de la population et de la couverture documentaire,
  tableau triable par population ou par WUI.
- **Risques** : carte du FRI par canton avec superposition optionnelle des
  infrastructures documentees, matrice risque x vulnerabilite economique, taux
  d'exposition des infrastructures par source.
- **Priorites et scenarios** : exploration du WUI par territoire, Top 20, fiche de
  profil territorial (facteurs contributifs et recommandation), matrice de decision,
  simulation comparative de quatre scenarios prospectifs.
- **A propos et methodologie** : sources, data dictionary, limites de l'etude,
  contact.

## Architecture

```
eau_togo_dashboard/
├── app.py                     # Point d'entree : configuration, navigation, orchestration
├── pages/                     # Logique d'affichage de chaque section
├── components/                # Composants visuels reutilisables (header, cartes, tableaux...)
├── analytics/                 # Calculs analytiques (KPI, priorites, risque, scenarios, recommandations)
├── data/                      # Chargement, validation et filtrage des donnees
│   └── geodata/                 # Fichiers de donnees exportes depuis l'EDA de reference
├── config/                    # Parametres, seuils, ponderations et charte graphique
├── utils/                     # Fonctions utilitaires (formatage, telechargement)
├── assets/logo/                # Emplacement du logo institutionnel (images.png, non fourni)
├── tests/                     # Tests automatises (donnees, indicateurs, priorites, lancement)
├── requirements.txt
└── README.md
```

## Methodologie

Toutes les valeurs affichees (population, FRI, RWI, Water Urgency Index, niveau de
priorite, resultats du Top 20) sont lues directement depuis les fichiers produits par
`EDA_Eau_Togo.ipynb` et ne sont jamais recalculees avec des hypotheses differentes.
Les seules operations effectuees par l'application sont :

- des filtres (region, prefecture, commune, canton, priorite, classe de risque,
  source) ;
- une simulation parametrique des scenarios prospectifs, qui reproduit exactement la
  methode et la ponderation de reference documentees dans l'EDA (section 18) ;
- des agregations simples (sommes, moyennes) a des fins d'affichage.

## Donnees

Les fichiers de `data/geodata/` sont extraits et derives de l'etude `EDA_Eau_Togo.ipynb` :

| Fichier | Contenu |
|---|---|
| `cantons_wui.geojson` | 388 cantons avec geometrie, FRI, RWI, WUI et niveau de priorite |
| `cantons_water_urgency_index.csv` | Version tabulaire du fichier precedent |
| `top20_zones_prioritaires.csv` | Classement de reference des 20 cantons les plus prioritaires |
| `infrastructures_coso.csv` | Sous-projets COSO cartographiables (coordonnees valides) |
| `infrastructures_coso_all.csv` | Ensemble des sous-projets COSO rattaches a un canton |
| `infrastructures_tde.csv` | Points de forages et chateaux d'eau de la Togolaise des Eaux |
| `data_dictionary.csv` | Dictionnaire de donnees consolide de l'EDA de reference |

## Limites analytiques a connaitre

- Aucune source ne renseigne le statut de fonctionnalite operationnelle des ouvrages :
  aucun taux de fonctionnalite n'est calcule ni affiche dans l'application.
- Les infrastructures documentees (COSO, TdE) ne constituent pas un inventaire
  national exhaustif ; leur absence dans un canton ne signifie pas l'absence physique
  d'ouvrage.
- La couverture documentaire est un proxy documentaire, pondere a hauteur de 10 %
  seulement dans le Water Urgency Index.
- Les scenarios prospectifs sont des simulations parametriques sous hypotheses
  explicites, non des previsions garanties.
- Les correlations presentees dans l'EDA de reference ne demontrent aucune relation
  causale.

Le detail complet des limites est disponible dans la page "A propos et
methodologie" de l'application.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement

```bash
streamlit run app.py
```

L'application est accessible par defaut sur `http://localhost:8501`.

## Tests

```bash
pytest tests/ -v
```

Les tests couvrent le chargement des donnees, leur validation, le calcul des KPI, la
logique de priorisation et de recommandation, la simulation des scenarios, ainsi que
le lancement complet de l'application (toutes les pages, via `streamlit.testing.v1.AppTest`).

## Technologies

- [Streamlit](https://streamlit.io) -- interface et navigation
- [Plotly](https://plotly.com/python/) -- cartographie interactive (MapLibre) et
  graphiques
- [GeoPandas](https://geopandas.org) -- manipulation des donnees geospatiales
- [pandas](https://pandas.pydata.org) -- manipulation des donnees tabulaires
- [pytest](https://pytest.org) -- tests automatises

## Identite visuelle

Le logo institutionnel (`images.png`) n'a pas ete fourni avec les fichiers source de
ce projet. L'emplacement `assets/logo/images.png` est prevu et pris en charge par
`components/header.py` et `components/sidebar.py` : deposer le fichier a cet
emplacement suffit a l'afficher automatiquement, sans aucune modification de code.
En son absence, l'en-tete institutionnel s'affiche en mode texte seul (Republique
togolaise / Ministere de l'Efficacite du Service Public et de la Transformation
Numerique).

## Limites de perimetre de cette livraison

Le fichier `final.zip` mentionne dans le cahier des charges original n'a pas ete
fourni dans cette conversation : cette application a ete construite a partir des
livrables directement disponibles (notebook EDA et exports CSV de reference), qui en
constituent le contenu attendu.

## Auteur

**DAYO Kokou Cyrille**
Ingenieur de Travaux Informatiques

Passionne par la Data Science, le developpement d'applications decisionnelles,
l'intelligence artificielle et la transformation numerique.

- Email : cyridayo@gmail.com
- Telephone / WhatsApp : +228 90 51 59 28
- LinkedIn : https://www.linkedin.com/in/dkc023/
- GitHub : https://github.com/kokoucyrille/
