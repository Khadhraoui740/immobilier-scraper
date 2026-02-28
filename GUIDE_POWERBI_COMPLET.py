"""
GUIDE COMPLET - RAPPORT POWER BI IMMOBILIER
============================================

ÉTAPE 1: ACCÉDER À VOS DONNÉES
==============================

Tous les fichiers nécessaires sont générés dans: exports/

📊 FICHIERS CRÉÉS:
  
  1. rapport_immobilier.html
     └─ Rapport Web interactif à 130,000 EUR
     └─ Ouvrir directement avec votre navigateur
     └─ Contient: Top 10 communes, meilleur ratio qualité-prix, synthèse
  
  2. synthese_communes.csv
     └─ Données agrégées par commune
     └─ Colonnes: Commune, Count, AvgPrice, MinPrice, MaxPrice, AvgSurface, PricePerm2
     └─ Pour importer dans Power BI
  
  3. proprietes_immobilier.csv
     └─ Toutes les 61 annonces individuelles
     └─ Colonnes: ID, Source, Commune, Prix, Surface, Pieces, DPE, DatePublie, URL
  
  4. analyse_communes.csv  
     └─ Analyse détaillée par commune
     └─ Format: Commune, Nombre Annonces, Prix Moyen, Prix Min, Prix Max, Surface Moy, Prix/m2


ÉTAPE 2: IMPORTER DANS POWER BI DESKTOP
========================================

A. Ouvrir Power BI Desktop

B. Nouvelle source de données:
   1. Cliquer "Obtenir les données" en haut à gauche
   2. Sélectionner "CSV"
   3. Naviguer vers: exports/synthese_communes.csv
   4. Cliquer "Charger"

C. Ajouter une deuxième table (optionnel):
   1. Requête > Nouvelles sources > CSV
   2. Sélectionner: exports/proprietes_immobilier.csv
   3. Charger

D. Transformer les données (si nécessaire):
   1. Convertir colonnes numériques (AvgPrice, MinPrice etc.) en Decimal
   2. Définir les relations si vous avez 2 tables


ÉTAPE 3: CRÉER LES VISUALISATIONS
==================================

PAGE 1 - VUE GÉNÉRALE
─────────────────────

VIZ 1: KPI - Communes Accessibles
  Type: Nombre (Cartes)
  Mesure: COUNTIF(Commune, "MinPrice <= 130000")
  Titre: "Communes Accessibles < 130k"

VIZ 2: KPI - Prix Moyen
  Type: Nombre
  Mesure: AVERAGE(AvgPrice)
  Format: Devise EUR

VIZ 3: TOP 10 Communes
  Type: Graphique à barres horizontales (Sorted)
  Axe: AvgPrice (filtré MinPrice <= 130000)
  Légende/Axe Y: Commune
  Tri: AvgPrice croissant
  Titre: "Top 10 Communes pour Budget 130k"

VIZ 4: Meilleur Ratio Qualité-Prix  
  Type: Graphique à barres horizontales
  Axe: PricePerm2 (€/m²)
  Légende: Commune
  Tri: PricePerm2 croissant
  Titre: "Top 10 Meilleur €/m²"


PAGE 2 - ANALYSE DÉTAILLÉE
──────────────────────────

VIZ 5: Distribution des Prix
  Type: Histogramme
  Valeurs: AvgPrice
  Titre: "Distribution des prix moyens par commune"

VIZ 6: Nuage de Points - Qualité/Prix
  Type: Scatter
  X: AvgPrice
  Y: PricePerm2
  Taille: Count
  Légende: Commune
  Titre: "Relation Price vs Quality"

VIZ 7: Tableau Synthèse
  Type: Tableau
  Colonnes: Commune, Count, AvgPrice, MinPrice, MaxPrice, PricePerm2
  Tri: AvgPrice
  Titre: "Synthèse détaillée"


PAGE 3 - DONNÉES BRUTES
──────────────────────

VIZ 8: Table Propriétés
  Type: Tableau
  Colonnes: Commune, Prix, Surface, Pieces, DPE, Source, DatePublie
  Filtres: Ajouter slicers pour Commune, DPE, Source


ÉTAPE 4: AJOUTER DES FILTRES (Slicers)
=======================================

Ajouter des slicers pour dynamique:
  ✓ Commune (multi-sélection)
  ✓ DPE (A, B, C, D)
  ✓ Plage de Prix (slider)
  ✓ Source (BienIci, LeBonCoin, PAP, SeLoger)


ÉTAPE 5: MESURES DAX RECOMMANDÉES
==================================

Créer dans Power BI > Mesures:

-- Communes accessibles
CommaunesAccessibles = 
  COUNTIF(synthese_communes[MinPrice], "<=130000")

-- Prix moyen
PrixMoyenGlobal = 
  AVERAGE(synthese_communes[AvgPrice])

-- Meilleur ratio
MeilleurRatio = 
  MIN(synthese_communes[PricePerm2])

-- Total annonces
TotalAnnonces = 
  COUNTA(proprietes_immobilier[ID])

-- Économie vs budget
EconomieTotal = 
  130000 * [CommaunesAccessibles] - SUMIF(synthese_communes[MinPrice], "<=130000", synthese_communes[MinPrice])


ÉTAPE 6: EXPORTER LE RAPPORT
=============================

Après création:
  1. Fichier > Enregistrer sous: rapport_immobilier.pbix
  2. Partager > Publier (optionnel)
  3. Exporter en PDF: Fichier > Exporter en PDF


RÉSULTATS ATTENDUS
===================

Après implémentation complète, vous devrez voir:

✓ 6 communes accessibles au budget 130k EUR
✓ Prix moyen des communes: ~113,000 EUR
✓ Meilleur rapport qualité-prix: Lagny-sur-Marne (2,982 €/m²)
✓ Top communes abordables: Poissy, Lagny-sur-Marne, Sartrouville, Massy, Chelles, Rambouillet
✓ Distribution de prix uniforme (102k - 127k EUR pour communes accessibles)


INFOS SUPPLÉMENTAIRES
=====================

Budget: 130,000 EUR
Zones: Île-de-France
Communes: 30+
Annonces: 61 (4 sources: LeBonCoin, Seloger, PAP, BienIci)
Date analyse: 28/02/2026

Pour questions ou modifications:
  - Modifier budget dans export_powerbi.py: budget = 130000
  - Regénérer exports: python export_powerbi.py
  - Rafraîchir Power BI: Accueil > Actualiser
"""

print(__doc__)

# Ouvrir le fichier rapport_immobilier.html
import webbrowser
import os

rapport_path = os.path.abspath('exports/rapport_immobilier.html')
print(f"\n✓ Rapport disponible à: {rapport_path}")
print("\nOuverture automatique du rapport HTML...")
try:
    webbrowser.open(f'file://{rapport_path}')
    print("✓ Rapport ouvert dans le navigateur")
except:
    print(f"⚠ Ouvrez manuellement: {rapport_path}")
