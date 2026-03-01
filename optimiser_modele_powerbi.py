#!/usr/bin/env python3
"""
Optimisation du modèle Power BI Desktop
Crée un rapport avec modélisation optimale, relations et mesures DAX
"""

import zipfile
import json
import os
import shutil
from datetime import datetime

# Chemins
RAPPORT_SOURCE = "exports/rapport.pbix"
RAPPORT_OPTIMISE = "exports/rapport_optimise.pbix"
CSV_COMMUNES = "exports/synthese_communes.csv"
CSV_PROPRIETES = "exports/proprietes_immobilier.csv"

# Mesures DAX professionnelles
MESURES_DAX = [
    {
        "name": "Total Annonces",
        "expression": "COUNTROWS(Proprietes)",
        "format": "#,##0"
    },
    {
        "name": "Prix Moyen",
        "expression": "AVERAGE(Proprietes[Prix])",
        "format": "#,##0 €"
    },
    {
        "name": "Prix Minimum",
        "expression": "MIN(Proprietes[Prix])",
        "format": "#,##0 €"
    },
    {
        "name": "Prix Maximum",
        "expression": "MAX(Proprietes[Prix])",
        "format": "#,##0 €"
    },
    {
        "name": "Surface Moyenne",
        "expression": "AVERAGE(Proprietes[Surface])",
        "format": "#,##0.0 m²"
    },
    {
        "name": "Prix/m² Moyen",
        "expression": "DIVIDE([Prix Moyen], [Surface Moyenne], 0)",
        "format": "#,##0 €/m²"
    },
    {
        "name": "Communes Accessibles",
        "expression": "CALCULATE(DISTINCTCOUNT(Communes[Commune]), Communes[BudgetFit] = 1)",
        "format": "#,##0"
    },
    {
        "name": "% Budget Accessible",
        "expression": "DIVIDE([Communes Accessibles], DISTINCTCOUNT(Communes[Commune]), 0)",
        "format": "0.0%"
    },
    {
        "name": "Rentabilité",
        "expression": "DIVIDE(1000 * 12, [Prix/m² Moyen], 0) * 100",
        "format": "0.00%",
        "description": "Estimation loyer 1000€/mois"
    },
    {
        "name": "Budget Restant",
        "expression": "130000 - [Prix Moyen]",
        "format": "#,##0 €"
    }
]

# Relations entre tables
RELATIONS = [
    {
        "from_table": "Proprietes",
        "from_column": "Commune",
        "to_table": "Communes",
        "to_column": "Commune",
        "cardinality": "Many-One",
        "cross_filter": "Single"
    }
]

def print_header(text):
    """Affiche un en-tête formaté"""
    print("\n" + "="*80)
    print(f" {text}")
    print("="*80 + "\n")

def copier_pbix_base():
    """Copie le PBIX source vers la version optimisée"""
    print("📋 Copie du fichier PBIX source...")
    
    if not os.path.exists(RAPPORT_SOURCE):
        print(f"❌ Fichier source introuvable: {RAPPORT_SOURCE}")
        return False
    
    # Copier le fichier
    shutil.copy2(RAPPORT_SOURCE, RAPPORT_OPTIMISE)
    
    taille = os.path.getsize(RAPPORT_OPTIMISE)
    print(f"✓ Fichier copié: {taille:,} bytes")
    return True

def ajouter_mesures_dax():
    """Ajoute les mesures DAX dans un fichier séparé pour import manuel"""
    print("\n📊 Génération des mesures DAX...")
    
    dax_script = "-- Mesures DAX pour Power BI Desktop\n"
    dax_script += f"-- Générées automatiquement le {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    
    for i, mesure in enumerate(MESURES_DAX, 1):
        dax_script += f"-- Mesure {i}: {mesure['name']}\n"
        if 'description' in mesure:
            dax_script += f"-- {mesure['description']}\n"
        dax_script += f"{mesure['name']} = {mesure['expression']}\n"
        dax_script += f"-- Format: {mesure['format']}\n\n"
    
    # Relations
    dax_script += "\n-- RELATIONS À CRÉER :\n"
    for rel in RELATIONS:
        dax_script += f"-- {rel['from_table']}[{rel['from_column']}] → {rel['to_table']}[{rel['to_column']}]  "
        dax_script += f"(Cardinalité: {rel['cardinality']})\n"
    
    # Sauvegarder
    dax_file = "exports/mesures_dax.txt"
    with open(dax_file, 'w', encoding='utf-8') as f:
        f.write(dax_script)
    
    print(f"✓ {len(MESURES_DAX)} mesures DAX générées")
    print(f"✓ Fichier créé: {dax_file}")
    return dax_file

def generer_guide_optimisation():
    """Génère un guide pas-à-pas pour optimiser le modèle"""
    guide = """
████████████████████████████████████████████████████████████████████████████████
█                    GUIDE D'OPTIMISATION POWER BI                           █
█                   Modèle de données professionnel                          █
████████████████████████████████████████████████████████████████████████████████

📋 ÉTAPE 1 : OUVRIR LE RAPPORT
────────────────────────────────────────────────────────────────────────────────
1. Ouvrir Power BI Desktop
2. Fichier → Ouvrir → rapport_optimise.pbix
3. Attendre le chargement complet

📊 ÉTAPE 2 : VÉRIFIER LES DONNÉES
────────────────────────────────────────────────────────────────────────────────
1. Cliquer sur l'onglet "Données" (icône tableau)
2. Vérifier les tables :
   ✓ Proprietes (63 lignes) - Détails des annonces
   ✓ Communes (41 lignes) - Synthèse par commune

🔗 ÉTAPE 3 : CRÉER LA RELATION
────────────────────────────────────────────────────────────────────────────────
1. Onglet "Modèle" (icône 3 carrés reliés)
2. Glisser-déposer :
   Proprietes[Commune] → Communes[Commune]
3. Configuration :
   • Cardinalité : Plusieurs à un (*)→(1)
   • Direction du filtre croisé : Unique
   • Activer cette relation : ✓
4. Cliquer "OK"

📐 ÉTAPE 4 : AJOUTER LES MESURES DAX
────────────────────────────────────────────────────────────────────────────────

Cliquer sur "Nouvelle mesure" et copier-coller chaque mesure :

1️⃣  Total Annonces = COUNTROWS(Proprietes)
    Format : Nombre entier

2️⃣  Prix Moyen = AVERAGE(Proprietes[Prix])
    Format : Devise (€)

3️⃣  Prix Minimum = MIN(Proprietes[Prix])
    Format : Devise (€)

4️⃣  Prix Maximum = MAX(Proprietes[Prix])
    Format : Devise (€)

5️⃣  Surface Moyenne = AVERAGE(Proprietes[Surface])
    Format : Décimal, 1 chiffre

6️⃣  Prix/m² Moyen = DIVIDE([Prix Moyen], [Surface Moyenne], 0)
    Format : Nombre entier

7️⃣  Communes Accessibles = CALCULATE(DISTINCTCOUNT(Communes[Commune]), Communes[BudgetFit] = 1)
    Format : Nombre entier

8️⃣  % Budget Accessible = DIVIDE([Communes Accessibles], DISTINCTCOUNT(Communes[Commune]), 0)
    Format : Pourcentage, 1 décimale

9️⃣  Rentabilité = DIVIDE(1000 * 12, [Prix/m² Moyen], 0) * 100
    Format : Pourcentage, 2 décimales
    Description : Si loyer = 1000€/mois

🔟 Budget Restant = 130000 - [Prix Moyen]
    Format : Devise (€)

⚙️  ÉTAPE 5 : OPTIMISER LES TYPES DE DONNÉES
────────────────────────────────────────────────────────────────────────────────

Table Proprietes :
• Prix → Devise fixe (€)
• Surface → Nombre décimal
• Pieces → Nombre entier
• Date Publie → Date/Heure
• URL → URL Web
• DPE → Texte

Table Communes :
• Count → Nombre entier
• AvgPrice, MinPrice, MaxPrice → Devise fixe (€)
• AvgSurface → Nombre décimal
• PricePerm2 → Nombre décimal
• BudgetFit → Nombre entier (0/1)

📊 ÉTAPE 6 : CRÉER LES HIÉRARCHIES
────────────────────────────────────────────────────────────────────────────────

Hiérarchie Géographique :
1. Table Communes → Clic droit sur "Commune"
2. "Créer une hiérarchie"
3. Nom : "Hiérarchie Géographique"

Hiérarchie Temporelle :
1. Table Proprietes → Clic droit sur "Date Publie"
2. "Créer une hiérarchie"
3. Ajouter : Année → Trimestre → Mois → Jour

🎨 ÉTAPE 7 : FORMATER LES COLONNES
────────────────────────────────────────────────────────────────────────────────

Prix (toutes tables) :
• Format : € French (France)
• Séparateur de milliers : espace
• Sans décimales

Surface :
• Format : Décimal
• 1 décimale
• Suffixe : " m²"

Prix/m² :
• Format : Décimal
• Sans décimales
• Suffixe : " €/m²"

⚡ ÉTAPE 8 : OPTIMISER LES PERFORMANCES
────────────────────────────────────────────────────────────────────────────────

1. Colonnes inutilisées :
   • Cacher les colonnes techniques (ID, Rang)
   
2. Trier les tables :
   • Communes : Trier par AvgPrice (ascendant)
   • Proprietes : Trier par Date Publie (descendant)

3. Catégories de données :
   • Communes[Commune] → Ville
   • Proprietes[URL] → URL Web
   • Proprietes[Date Publie] → Date

✅ ÉTAPE 9 : VALIDER LE MODÈLE
────────────────────────────────────────────────────────────────────────────────

1. Onglet "Modèle" :
   ✓ Relation visible entre les tables
   ✓ Ligne connectant Commune → Commune

2. Onglet "Données" :
   ✓ 10 mesures visibles dans le volet "Champs"
   ✓ Icônes Σ à côté de chaque mesure

3. Test :
   • Créer un visuel "Carte"
   • Glisser la mesure "Prix Moyen"
   • Valeur attendue : ~283 486 €

💾 ÉTAPE 10 : SAUVEGARDER
────────────────────────────────────────────────────────────────────────────────

1. Fichier → Enregistrer sous
2. Nom : rapport_optimise_final.pbix
3. ✓ Modèle de données optimisé prêt !

════════════════════════════════════════════════════════════════════════════════
⏱️  TEMPS ESTIMÉ : 10-15 minutes
🎯 RÉSULTAT : Modèle professionnel avec 10 mesures DAX et relations optimales
════════════════════════════════════════════════════════════════════════════════

💡 CONSEIL PRO :
Après ces étapes, vous pouvez créer les 12 graphiques recommandés dans le
fichier GUIDE_12_GRAPHIQUES.md. Le modèle optimisé rendra la création des
visuels beaucoup plus rapide et intuitive !

"""
    
    guide_file = "exports/GUIDE_OPTIMISATION_MODELE.txt"
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print(f"\n✓ Guide créé: {guide_file}")
    return guide_file

def generer_script_power_query():
    """Génère un script Power Query M pour les transformations"""
    
    m_script = """
// ═══════════════════════════════════════════════════════════════════════════
// SCRIPT POWER QUERY M - OPTIMISATION DES DONNÉES
// ═══════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────
// TABLE : Proprietes (Source : proprietes_immobilier.csv)
// ───────────────────────────────────────────────────────────────────────────

let
    Source = Csv.Document(File.Contents("proprietes_immobilier.csv"),
        [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    
    // Promouvoir les en-têtes
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    
    // Changer les types
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders,{
        {"ID", type text},
        {"Source", type text},
        {"Commune", type text},
        {"Prix", Currency.Type},
        {"Surface", type number},
        {"Pieces", Int64.Type},
        {"DPE", type text},
        {"Date Publie", type datetime},
        {"URL", type text}
    }),
    
    // Ajouter des colonnes calculées
    AddPrixM2 = Table.AddColumn(ChangeTypes, "Prix/m²", 
        each [Prix] / [Surface], Currency.Type),
    
    AddMoisPubli = Table.AddColumn(AddPrixM2, "Mois Publication",
        each Date.MonthName([Date Publie]), type text),
    
    // Filtrer les valeurs nulles
    FilterNull = Table.SelectRows(AddMoisPubli, 
        each [Prix] <> null and [Surface] <> null),
    
    // Trier par date descendant
    SortByDate = Table.Sort(FilterNull,{{"Date Publie", Order.Descending}})
in
    SortByDate


// ───────────────────────────────────────────────────────────────────────────
// TABLE : Communes (Source : synthese_communes.csv)
// ───────────────────────────────────────────────────────────────────────────

let
    Source = Csv.Document(File.Contents("synthese_communes.csv"),
        [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    
    // Promouvoir les en-têtes
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    
    // Changer les types
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders,{
        {"Rang", Int64.Type},
        {"Commune", type text},
        {"Count", Int64.Type},
        {"AvgPrice", Currency.Type},
        {"MinPrice", Currency.Type},
        {"MaxPrice", Currency.Type},
        {"AvgSurface", type number},
        {"PricePerm2", type number},
        {"BudgetFit", Int64.Type}
    }),
    
    // Ajouter colonne Accessible
    AddAccessible = Table.AddColumn(ChangeTypes, "Accessible", 
        each if [BudgetFit] = 1 then "Oui" else "Non", type text),
    
    // Ajouter catégorie de prix
    AddCategorie = Table.AddColumn(AddAccessible, "Catégorie Prix",
        each if [AvgPrice] <= 130000 then "Accessible"
             else if [AvgPrice] <= 200000 then "Moyen"
             else "Élevé", type text),
    
    // Trier par prix moyen
    SortByPrice = Table.Sort(AddCategorie,{{"AvgPrice", Order.Ascending}})
in
    SortByPrice


// ═══════════════════════════════════════════════════════════════════════════
// INSTRUCTIONS D'APPLICATION :
// ═══════════════════════════════════════════════════════════════════════════
//
// 1. Dans Power BI Desktop, aller dans "Transformer les données"
// 2. Pour chaque table (Proprietes, Communes) :
//    • Clic droit sur la requête → Éditeur avancé
//    • Remplacer tout le code par le script correspondant ci-dessus
//    • Modifier le chemin du fichier CSV (ligne "File.Contents")
//    • Cliquer "Terminé"
// 3. Cliquer "Fermer et appliquer"
//
// ═══════════════════════════════════════════════════════════════════════════
"""
    
    m_file = "exports/script_power_query.txt"
    with open(m_file, 'w', encoding='utf-8') as f:
        f.write(m_script)
    
    print(f"✓ Script Power Query M créé: {m_file}")
    return m_file

def main():
    print_header("🚀 OPTIMISATION DU MODÈLE POWER BI DESKTOP")
    
    print("Ce script va créer un modèle de données professionnel avec :\n")
    print("   ✓ Relations entre tables optimisées")
    print("   ✓ 10 mesures DAX professionnelles")
    print("   ✓ Hiérarchies géographiques et temporelles")
    print("   ✓ Types de données optimisés")
    print("   ✓ Scripts Power Query M")
    print("   ✓ Guide pas-à-pas détaillé")
    
    # Copier le PBIX
    if not copier_pbix_base():
        return
    
    # Générer les fichiers d'optimisation
    dax_file = ajouter_mesures_dax()
    m_file = generer_script_power_query()
    guide_file = generer_guide_optimisation()
    
    # Résumé
    print_header("✅ OPTIMISATION TERMINÉE")
    
    print("📁 Fichiers créés :\n")
    print(f"   1. {RAPPORT_OPTIMISE}")
    print(f"      → Rapport Power BI de base (prêt pour optimisation)")
    print(f"\n   2. {dax_file}")
    print(f"      → {len(MESURES_DAX)} mesures DAX à copier-coller")
    print(f"\n   3. {m_file}")
    print(f"      → Scripts Power Query M pour transformations")
    print(f"\n   4. {guide_file}")
    print(f"      → Guide complet d'optimisation (10-15 min)")
    
    print("\n" + "─"*80)
    print("📋 PROCHAINES ÉTAPES :\n")
    print("   1. Ouvrir rapport_optimise.pbix dans Power BI Desktop")
    print("   2. Suivre le guide GUIDE_OPTIMISATION_MODELE.txt")
    print("   3. Créer la relation entre Proprietes et Communes")
    print("   4. Ajouter les 10 mesures DAX (copier-coller)")
    print("   5. Optionnel : Appliquer les scripts Power Query M")
    print("   6. Créer les 12 graphiques (GUIDE_12_GRAPHIQUES.md)")
    print("\n⏱️  Temps total estimé : 15-20 minutes")
    print("🎯 Résultat : Modèle de données professionnel et optimisé")
    print("─"*80 + "\n")
    
    # Ouvrir le guide
    print("🚀 Ouverture du guide d'optimisation...")
    os.system(f'start notepad "{guide_file}"')
    
    print("\n✨ Prêt pour l'optimisation ! Suivez le guide.")

if __name__ == "__main__":
    main()
