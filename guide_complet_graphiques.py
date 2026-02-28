#!/usr/bin/env python3
"""
Guide interactif pour ajouter TOUS les graphiques dans Power BI
Suit l'utilisateur étape par étape pour créer les visualisations complètes
"""

import time

def section(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def step(num, title):
    print(f"\n{'─'*80}")
    print(f"  ÉTAPE {num} - {title}")
    print(f"{'─'*80}\n")

def instructions(text):
    print(f"  📌 {text}")

def input_step():
    input("\n  ▶ Appuyez sur ENTRÉE quand c'est fait...")

def main():
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  📊 GUIDE COMPLET - AJOUTER TOUS LES GRAPHIQUES POWER BI".center(78) + "█")
    print("█" + "  8 Visualisations professionnelles".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    # ÉTAPE 1: Importer les données CSV
    step(1, "IMPORTER LES DONNÉES CSV")
    
    instructions("Ouvrez le rapport Power BI (rapport.pbix)")
    instructions("Menu en haut: Home → Get Data → CSV")
    instructions("Selectionnez: exports/synthese_communes.csv")
    instructions("Cliquez: Load")
    
    print("\n  ⚠️  IMPORTANT: Attendez le chargement complet des données")
    print("     Vous devriez voir 41 communes chargées")
    
    input_step()
    
    # ÉTAPE 2: KPI - Communes Count
    step(2, "KPI 1️⃣ - NOMBRE DE COMMUNES")
    
    instructions("Home → New Visual → Card")
    instructions("Drag 'commune' vers le champ de valeur")
    instructions("Positionnez en haut à gauche (1/4 écran)")
    instructions("Titre: 'Communes Analysées'")
    
    print("\n  💡 Résultat attendu: Affiche 41")
    input_step()
    
    # ÉTAPE 3: KPI - Prix Moyen
    step(3, "KPI 2️⃣ - PRIX MOYEN")
    
    instructions("Home → New Visual → Card")
    instructions("Drag 'prix_moyen' vers le champ de valeur")
    instructions("Créez une mesure: Sum(prix_moyen) / Count(commune)")
    instructions("Positionnez en haut à droite")
    instructions("Titre: 'Prix Moyen'")
    
    print("\n  💡 Résultat attendu: ≈ 285,649€")
    input_step()
    
    # ÉTAPE 4: Bar Chart - Prix par Commune
    step(4, "📊 GRAPHIQUE 1 - BARRES (Prix par Commune)")
    
    instructions("Home → New Visual → Column Chart")
    instructions("Axis: Drag 'commune'")
    instructions("Value: Drag 'prix_moyen'")
    instructions("Triez par Prix Moyen (décroissant)")
    instructions("Titre: 'Prix Moyen par Commune'")
    
    print("\n  💡 TOP communes visibles: Poissy, Lagny-sur-Marne, etc.")
    input_step()
    
    # ÉTAPE 5: Scatter Plot - Prix vs Surface  
    step(5, "🔵 GRAPHIQUE 2 - NUAGE DE POINTS (Prix vs M²)")
    
    instructions("Home → New Visual → Scatter Chart")
    instructions("X Axis: Drag 'prix_m2'")
    instructions("Y Axis: Drag 'prix_moyen'")
    instructions("Legend: Drag 'commune' (optionnel)")
    instructions("Titre: 'Analyse Prix au M² vs Prix Total'")
    
    print("\n  💡 Permet de voir le meilleur rapport qualité-prix")
    input_step()
    
    # ÉTAPE 6: Mapa/Tableau détaillé
    step(6, "📋 GRAPHIQUE 3 - TABLE (Détails Completes)")
    
    instructions("Home → New Visual → Table")
    instructions("Colonnes à ajouter:")
    instructions("  - commune")
    instructions("  - prix_moyen")
    instructions("  - prix_min")
    instructions("  - prix_max")
    instructions("  - prix_m2")
    instructions("Triez par prix_moyen (croissant)")
    instructions("Titre: 'Détail des Communes'")
    
    print("\n  💡 Affiche les 41 communes avec tous les détails")
    input_step()
    
    # ÉTAPE 7: Slicers - Filtres Interactifs
    step(7, "🔍 GRAPHIQUE 4 - SLICERS (Filtres Interactifs)")
    
    instructions("Home → New Visual → Slicer")
    instructions("Field: Drag 'commune'")
    instructions("Placez à gauche ou haut")
    instructions("Permet de filtrer toutes les visualisations")
    
    print("\n  💡 Sélectionnez une commune → Tous les graphiques se mettent à jour")
    input_step()
    
    # ÉTAPE 8: KPI - Communes Accessibles
    step(8, "KPI 3️⃣ - COMMUNES À BUDGET (≤130k)")
    
    instructions("Home → New Visual → Card")
    instructions("Créez une mesure: COUNTIF(communes où prix < 130000)")
    instructions("Positionnez en bas à gauche")
    instructions("Titre: 'Accessibles à 130k'")
    
    print("\n  💡 Résultat attendu: 6 communes")
    input_step()
    
    # ÉTAPE 9: Ligne/Area Chart - Progression Prix
    step(9, "📈 GRAPHIQUE 5 - COURBE (Evolution des Prix)")
    
    instructions("Home → New Visual → Line Chart")
    instructions("X Axis: Drag 'commune'")
    instructions("Y Axis: Drag 'prix_moyen'")
    instructions("Triez par prix_moyen")
    instructions("Titre: 'Classement des Communes par Prix'")
    
    print("\n  💡 Voir la progression visuelle des prix")
    input_step()
    
    # ÉTAPE 10: Donut Chart - Distribution Budget
    step(10, "🍩 GRAPHIQUE 6 - CAMEMBERT (Communes Accessibles)")
    
    instructions("Home → New Visual → Donut Chart")
    instructions("Legend: Drag 'commune' (communes < 130k)")
    instructions("Value: Drag 'prix_moyen'")
    instructions("Titre: '% des Communes Accessibles'")
    
    print("\n  💡 Voir la distribution des 6 communes accessibles")
    input_step()
    
    # ÉTAPE 11: Heatmap/Matrix
    step(11, "🔥 GRAPHIQUE 7 - MATRICE (Comparaison Détaillée)")
    
    instructions("Home → New Visual → Matrix")
    instructions("Rows: Drag 'commune'")
    instructions("Values: Drag 'prix_moyen', 'prix_min', 'prix_max', 'prix_m2'")
    instructions("Format conditionnel: Mettez en couleur (chaud/froid)")
    instructions("Titre: 'Matrice de Comparaison'")
    
    print("\n  💡 Vue d'ensemble avec code couleur")
    input_step()
    
    # ÉTAPE 12: Gauge - Indicateur Budget
    step(12, "⏸️ GRAPHIQUE 8 - JAUGE (% Budget Utilisé)")
    
    instructions("Home → New Visual → Gauge")
    instructions("Value: Drag 'prix_moyen' (pour Poissy: 103,651)")
    instructions("Target: 130,000 (votre budget max)")
    instructions("Titre: 'Utilisation du Budget (Poissy)'")
    
    print("\n  💡 Montre que Poissy = 79% de votre budget")
    input_step()
    
    # Finalisation
    section("📊 LAYOUT FINAL RECOMMANDÉ")
    
    print("""
    ┌─────────────────────────────────────────────────────────┐
    │  KPI 1        KPI 2        KPI 3        GAUGE           │
    │  Communes     Prix Moyen   Accessibles  Budget %         │
    ├─────────────────────────────────────────────────────────┤
    │   SLICER (communes filter)                              │
    ├─────────────────────────────────────────────────────────┤
    │  BAR CHART                    SCATTER PLOT              │
    │  (Prix par commune)           (Prix M² vs Total)        │
    ├─────────────────────────────────────────────────────────┤
    │  TABLE (tous les détails)                               │
    │  [commune] [prix_moyen] [prix_min] [prix_max] [prix_m2] │
    ├─────────────────────────────────────────────────────────┤
    │  LINE CHART        DONUT CHART      MATRIX             │
    │  (Progression)     (Distribution)    (Comparaison)      │
    └─────────────────────────────────────────────────────────┘
    """)
    
    # Enregistrer
    section("💾 ENREGISTRER LE RAPPORT")
    
    instructions("File → Save (ou Ctrl+S)")
    instructions("Nommez: 'Immobilier_Île-de-France_Complet'")
    instructions("Format: Power BI (.pbix)")
    
    print("\n  ✅ Tous les graphiques sauvegardés!")
    input_step()
    
    # Finale
    section("🎉 RAPPORT COMPLET!")
    
    print("""
    Votre rapport contient maintenant:
    
    ✅ 3 KPI cards (Communes, Prix, Accessibles)
    ✅ 1 Bar Chart (Prix par commune)
    ✅ 1 Scatter Plot (Prix M² vs Total)
    ✅ 1 Table (Détails complets)
    ✅ 1 Slicer (Filtres interactifs)
    ✅ 1 Line Chart (Progression)
    ✅ 1 Donut Chart (Distribution)
    ✅ 1 Gauge (Indicateur budget)
    ✅ 1 Matrix (Comparaison)
    
    TOTAL: 12 Visualisations professionnelles
    
    💡 Tous les graphiques sont INTERACTIFS et se sync automatiquement!
    """)
    
    print("\n" + "█"*80)
    print("█" + "  ✨ Rapport analytique complet créé avec succès!".center(78) + "█")
    print("█"*80 + "\n")

if __name__ == "__main__":
    main()
