"""
GUIDE COMPLET - RAPPORT POWER BI IMMOBILIER
============================================

ÉTAPE 1: IMPORTER LES DONNÉES DANS POWER BI DESKTOP
----------------------------------------------------

1. Ouvrir Power BI Desktop
2. Cliquer sur "Obtenir les données" > "CSV"
3. Sélectionner le fichier: exports/synthese_communes.csv
4. Cliquer "Charger"
5. Répéter pour: exports/proprietes_immobilier.csv

ÉTAPE 2: CRÉER LES VISUALISATIONS RECOMMANDÉES
-----------------------------------------------

VISUALISATION 1: TOP 10 COMMUNES (Budget 130k)
- Type: Graphique à barres horizontales
- Axe Y: Commune (filtré pour min_price <= 130000)
- Axe X: AvgPrice
- Titre: "Top 10 communes accessibles avec budget 130k EUR"
- Couleur: Dégradé Prix

VISUALISATION 2: MEILLEUR RAPPORT QUALITÉ/PRIX
- Type: Graphique en nuage de points
- X: AvgPrice
- Y: PricePerm2
- Taille: Count (nombre d'annonces)
- Légende: Commune
- Titre: "Rapport Qualité-Prix par Commune"

VISUALISATION 3: ÉVOLUTION PRIX PAR COMMUNE
- Type: Tableau
- Colonnes: Commune, Count, AvgPrice, MinPrice, MaxPrice, PricePerm2
- Tri: Par AvgPrice croissant
- Format: Nombre à 0 décimales pour les prix

VISUALISATION 4: KPI - COMMUNES ACCESSIBLES
- Type: Carte (nombre)
- Mesure: COUNTIF(BudgetFit=1)
- Titre: "Communes accessibles < 130k EUR"

VISUALISATION 5: DISTRIBUTION PRIX
- Type: Histogramme
- Valeurs: AvgPrice
- Compartiments: 10
- Titre: "Distribution des prix moyens"

VISUALISATION 6: MATRICE - SYNTHÈSE
- Lignes: Commune
- Valeurs: Count, AvgPrice, PricePerm2
- Titre: "Synthèse détaillée par commune"

ÉTAPE 3: AJOUTER DES FILTRES
-----------------------------

Créer un filtre sur:
- Budget (slider 50k à 500k EUR) pour filtrer dynamiquement
- Type de commune (filtre par commune)
- Prix/m2 (pour comparer qualité-prix)

ÉTAPE 4: CRÉER LE RAPPORT FINAL
-------------------------------

Organiser en sections:
1. Page "Vue Générale"
   - KPI communes accessibles
   - Top 10 communes
   - Distribution prix

2. Page "Analyse Détaillée"
   - Nuage de points Qualité-Prix
   - Tableau synthèse

3. Page "Données Brutes"
   - Toutes les annonces individuelles

FICHIERS À UTILISER:
-------------------
✓ exports/synthese_communes.csv - Données agrégées par commune
✓ exports/proprietes_immobilier.csv - Toutes les annonces
"""

print(__doc__)

# Créer aussi un fichier d'aide au calcul des mesures
print("\n" + "=" * 80)
print("MESURES DAX À CRÉER DANS POWER BI")
print("=" * 80)

dax_measures = """
-- Total propriétés
TotalProperties = COUNTA(proprietes_immobilier[ID])

-- Communes accessibles avec budget 130k
CommaunesAccessibles = COUNTIF(synthese_communes[MinPrice],"<=130000")

-- Prix moyen tous biens
PrixMoyenGeneral = AVERAGE(proprietes_immobilier[Prix])

-- Prix minimum global
PrixMin = MIN(proprietes_immobilier[Prix])

-- Prix maximum global  
PrixMax = MAX(proprietes_immobilier[Prix])

-- Meilleur ratio qualité/prix
MeilleurRatioPrix = MIN(synthese_communes[PricePerm2])
"""

print(dax_measures)
