#!/usr/bin/env python3
"""
Solution 2: Guide Interactif Étape-par-Étape
Crée un rapport Power BI en suivant des instructions claires

Pas de dépendances externes - 100% texte interactif
"""

import os

class PowerBIAutomator:
    """Guide interactif pour créer un rapport Power BI"""
    
    def __init__(self, csv_path="exports/synthese_communes.csv"):
        self.csv_path = csv_path
        self.step = 0
    
    def print_step(self, title, instructions):
        """Affiche une étape formatée"""
        self.step += 1
        print("\n" + "=" * 70)
        print(f"📌 ÉTAPE {self.step}: {title}")
        print("=" * 70)
        for line in instructions:
            print(f"  {line}")
        print()
    
    def next_step(self):
        """Pause avant prochaine étape"""
        input("  ➜ Appuyez sur Entrée quand c'est fait...")
        print()
    
    def import_csv_data(self):
        """Étape 1: Importe le CSV"""
        self.print_step("Importer les données CSV", [
            "1. Ouvrez Power BI Desktop",
            "2. Cliquez sur 'Obtenir les données' (en haut à gauche)",
            "3. Sélectionnez 'CSV'",
            f"4. Naviguez vers le fichier:",
            f"   {os.path.abspath(self.csv_path)}",
            "5. Cliquez sur 'Charger'",
            "6. Attendez que les données se chargent..."
        ])
        self.next_step()
    
    def create_kpi_communes(self):
        """Étape 2: Crée la première visualisation KPI"""
        self.print_step("Ajouter KPI - Communes Accessibles", [
            "OBJECTIF: Afficher le nombre de communes accessibles < 130k",
            "",
            "ACTIONS:",
            "1. Cliquez sur l'onglet 'Insérer' (ruban supérieur)",
            "2. Cliquez sur 'Cartes' → 'Nombre'",
            "3. Zone 'Valeur': Glissez 'Commune' depuis le panneau droit",
            "4. La carte affichera le nombre de communes",
            "5. Titre de la carte: 'Communes Accessibles < 130k'",
            "",
            "📌 CONSEIL: Placez-la en haut à gauche de votre page"
        ])
        self.next_step()
    
    def create_bar_chart(self):
        """Étape 3: Crée graphique à barres"""
        self.print_step("Ajouter Graphique à Barres - Top 10 Communes", [
            "OBJECTIF: Afficher les communes par prix moyen (ascending)",
            "",
            "ACTIONS:",
            "1. Insérer → Graphique à barres (Bar chart)",
            "2. Axe Y: Glissez 'Commune'",
            "3. Axe X: Glissez 'PrixMoyen'",
            "4. Cliquez sur PrixMoyen dans Valeurs → Tri croissant",
            "5. Titre: 'Top 10 Communes pour Budget 130k'",
            "6. (Optionnel) Filtrer: PrixMin <= 130000",
            "",
            "📌 RÉSULTAT: Les communes moins chères en bas, plus chères en haut"
        ])
        self.next_step()
    
    def create_scatter_chart(self):
        """Étape 4: Crée nuage de points"""
        self.print_step("Ajouter Nuage de Points - Qualité vs Prix", [
            "OBJECTIF: Voir la relation entre prix et qualité (€/m²)",
            "",
            "ACTIONS:",
            "1. Insérer → Nuage de points (Scatter chart)",
            "2. Axe X: Glissez 'PrixMoyen'",
            "3. Axe Y: Glissez 'PricePerm2' (€/m²)",
            "4. Légende: Glissez 'Commune'",
            "5. Taille de la bulle: Glissez 'Nombre'",
            "6. Titre: 'Relation Prix vs Quality'",
            "",
            "📌 RÉSULTAT: Identifier communes avec bon rapport prix/m²"
        ])
        self.next_step()
    
    def create_table(self):
        """Étape 5: Crée tableau"""
        self.print_step("Ajouter Tableau Synthèse", [
            "OBJECTIF: Afficher toutes les données en détail",
            "",
            "ACTIONS:",
            "1. Insérer → Tableau (Table)",
            "2. Ajouter colonnes (drag-drop du panneau droit):",
            "   - Commune",
            "   - Nombre",
            "   - PrixMoyen",
            "   - PrixMin",
            "   - PrixMax",
            "   - PricePerm2",
            "3. Tri: Par PrixMoyen (croissant)",
            "4. Titre: 'Synthèse détaillée'"
        ])
        self.next_step()
    
    def add_slicers(self):
        """Étape 6: Ajoute les filtres"""
        self.print_step("Ajouter Slicers (Filtres Interactifs)", [
            "OBJECTIF: Permettre de filtrer par commune dynamiquement",
            "",
            "ACTIONS:",
            "1. Insérer → Segment (Slicer)",
            "2. Glissez 'Commune' dans la slicer",
            "3. Positionnez à gauche (panel de filtrage)",
            "4. Cliquez sur chaque graphique → Format → Filtres",
            "5. Connectez le slicer à tous les graphiques",
            "",
            "📌 RÉSULTAT: Cliquez sur commune = tous les graphiques se mettent à jour"
        ])
        self.next_step()
    
    def set_theme(self):
        """Étape 7: Configure le thème"""
        self.print_step("Personnaliser le Thème et Couleurs", [
            "OBJECTIF: Rendre le rapport visuellement attrayant",
            "",
            "ACTIONS:",
            "1. Affichage → Thèmes (ruban supérieur)",
            "2. Sélectionnez un thème (ex: 'Bleu', 'Moderne')",
            "3. Pour plus de personnalisation:",
            "   Affichage → Thème → Gérer les thèmes",
            "4. Ou: Format → Couleurs de l'arrière-plan",
            "",
            "💡 CONSEIL: Thème bleu donne bon aspect professionnel"
        ])
        self.next_step()
    
    def export_report(self):
        """Étape 8: Exporte le rapport"""
        self.print_step("Enregistrer et Exporter le Rapport", [
            "OBJECTIF: Sauvegarder votre rapport Power BI",
            "",
            "ACTIONS:",
            "1. Fichier → Enregistrer sous (Ctrl+Shift+S)",
            "2. Nom du fichier: rapport_immobilier.pbix",
            "3. Emplacement: exports/",
            "4. Cliquez sur 'Enregistrer'",
            "",
            "✅ Votre rapport est maintenant sauvegardé!"
        ])
        self.next_step()
    
    def print_conclusion(self):
        """Affiche la conclusion"""
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 68 + "║")
        print("║" + "  ✅ RAPPORT TERMINÉ!".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("╚" + "═" * 68 + "╝")
        
        print("\n🎉 Bravo! Vous avez créé votre premier rapport Power BI!")
        print("\n📊 Votre rapport peut maintenant:")
        print("  • Être partagé avec des collègues")
        print("  • Être publié sur Power BI Service (cloud)")
        print("  • Recevoir de nouvelles pages")
        print("  • Utiliser des mesures DAX avancées")
        
        print("\n" + "─" * 70)
        print("💡 PROCHAINES ÉTAPES AVANCÉES:")
        print("─" * 70)
        
        print("\n1️⃣  AJOUTER DES MESURES DAX:")
        print("   • Créer des KPIs personnalisés")
        print("   • Calculer des évolutions année sur année")
        print("   • Agrégations personnalisées")
        
        print("\n2️⃣  CRÉER PLUS DE PAGES:")
        print("   • Page 'Vue Détaillée' par commune")
        print("   • Page 'Comparaison Communes'")
        print("   • Page 'Tendances de Marché'")
        
        print("\n3️⃣  PUBLIER SUR POWER BI SERVICE:")
        print("   • Fichier → Publier")
        print("   • Partager le lien avec collègues")
        print("   • Accès 24/7 via navigateur")
        
        print("\n" + "=" * 70)
        print("✨ Merci d'avoir utilisé ce guide!")
        print("=" * 70 + "\n")
    
    def run_guided_setup(self):
        """Lance l'assistant guidé complet"""
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 68 + "║")
        print("║" + "  🚀 ASSISTANT DE CRÉATION RAPPORT POWER BI".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("╚" + "═" * 68 + "╝")
        
        print("\n📋 PLAN DE CRÉATION:")
        print("  Cette formation guidée vous mènera à créer")
        print("  votre premier rapport Power BI professionnel.")
        print("\n  ⏱️  Temps estimé: 30-45 minutes")
        print("  📊 Fichier CSV: " + os.path.abspath(self.csv_path))
        print("\n💡 Comment ça fonctionne:")
        print("  1. Chaque ÉTAPE affiche les instructions précises")
        print("  2. Vous effectuez l'action dans Power BI Desktop")
        print("  3. Appuyez sur Entrée pour passer à la suivante")
        
        input("\n➜ Appuyez sur Entrée pour COMMENCER...\n")
        
        # Toutes les étapes
        self.import_csv_data()
        self.create_kpi_communes()
        self.create_bar_chart()
        self.create_scatter_chart()
        self.create_table()
        self.add_slicers()
        self.set_theme()
        self.export_report()
        
        # Conclusion
        self.print_conclusion()


if __name__ == "__main__":
    automator = PowerBIAutomator()
    automator.run_guided_setup()
