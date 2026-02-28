#!/usr/bin/env python3
"""
Script Launcher Automatisé Power BI
Lance Power BI Desktop + guide interactif simultané
"""

import subprocess
import os
import time
import sys
from pathlib import Path

class PowerBILauncher:
    """Lance Power BI et guide l'utilisateur en parallèle"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.csv_path = self.project_root / "exports" / "synthese_communes.csv"
        self.powerbi_exe = r"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe"
        
    def check_powerbi_installed(self):
        """Vérifie si Power BI Desktop est installé"""
        if not os.path.exists(self.powerbi_exe):
            print("❌ Power BI Desktop n'est pas installé!")
            print("📥 Téléchargez-le: https://powerbi.microsoft.com/fr-fr/desktop/")
            return False
        return True
    
    def check_csv_exists(self):
        """Vérifie que le fichier CSV existe"""
        if not self.csv_path.exists():
            print("❌ Fichier CSV non trouvé!")
            print(f"📁 Chemin attendu: {self.csv_path}")
            return False
        return True
    
    def launch_powerbi(self):
        """Lance Power BI Desktop"""
        try:
            print("\n🚀 Lancement de Power BI Desktop...")
            subprocess.Popen([self.powerbi_exe])
            print("✅ Power BI Desktop lancé!")
            print("⏳ Attendez 10-15 secondes que l'application se charge...")
            time.sleep(12)
            return True
        except Exception as e:
            print(f"❌ Erreur au lancement: {e}")
            return False
    
    def display_banner(self):
        """Affiche le bandeau de démarrage"""
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 68 + "║")
        print("║" + "  🚀 LAUNCHER AUTOMATISÉ - POWER BI DESKTOP".center(68) + "║")
        print("║" + "  + Guide Interactif en Temps Réel".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("╚" + "═" * 68 + "╝")
    
    def display_step_1_import(self):
        """Étape 1: Importer le CSV"""
        print("\n" + "=" * 70)
        print("📌 ÉTAPE 1: IMPORTER LES DONNÉES CSV")
        print("=" * 70)
        print(f"\n📁 Fichier CSV à importer:")
        print(f"   {self.csv_path}")
        print(f"\n📋 Colonnes disponibles:")
        print("   • Commune")
        print("   • Nombre (count)")
        print("   • PrixMoyen")
        print("   • PrixMin")
        print("   • PrixMax")
        print("   • AvgSurface")
        print("   • PricePerm2 (€/m²)")
        
        print("\n🎯 ACTIONS À FAIRE DANS POWER BI:")
        print("  1. Cliquez sur 'Obtenir les données' (haut gauche)")
        print("  2. Sélectionnez 'CSV'")
        print(f"  3. Naviguez vers: {self.csv_path}")
        print("  4. Cliquez sur 'Charger'")
        print("  5. Attendez que les données apparaissent à droite")
        
        print("\n⏳ Vous avez 2 minutes pour compléter cette étape...")
        input("\n➜ Appuyez sur Entrée quand le CSV est chargé...")
        
        print("✅ Excellent! Passons à l'étape suivante.\n")
    
    def display_step_2_kpi(self):
        """Étape 2: Ajouter KPI"""
        print("=" * 70)
        print("📌 ÉTAPE 2: CRÉER KPI - COMMUNES ACCESSIBLES")
        print("=" * 70)
        print("\n🎯 OBJECTIF: Afficher le nombre de communes < 130k EUR")
        
        print("\n🔧 ACTIONS DANS POWER BI:")
        print("  1. Cliquez sur 'Insérer' (ruban supérieur)")
        print("  2. Cliquez sur 'Cartes' → 'Nombre'")
        print("  3. Une nouvelle visualisation apparaît")
        print("  4. Dans le panneau droit, glissez 'Commune' → Zone 'Valeur'")
        print("  5. La carte affichera le nombre: 30 (communes)")
        print("\n💄 PERSONNALISATION:")
        print("  • Titre: 'Communes Accessibles < 130k'")
        print("  • Position: Haut gauche de la page")
        
        input("\n➜ Appuyez sur Entrée quand le KPI est créé...")
        print("✅ Bravo! Continuons.\n")
    
    def display_step_3_bar_chart(self):
        """Étape 3: Graphique à barres"""
        print("=" * 70)
        print("📌 ÉTAPE 3: CRÉER GRAPHIQUE À BARRES - TOP 10")
        print("=" * 70)
        print("\n🎯 OBJECTIF: Afficher communes par prix moyen (moins chers d'abord)")
        
        print("\n🔧 ACTIONS DANS POWER BI:")
        print("  1. Insérer → 'Graphique à barres'")
        print("  2. Glissez 'Commune' vers 'Axe'")
        print("  3. Glissez 'PrixMoyen' vers 'Valeur'")
        print("  4. Dans 'Valeur': Cliquez sur 'PrixMoyen' → 'Trier croissant'")
        print("  5. Titre: 'Top 10 Communes pour Budget 130k'")
        
        print("\n📊 RÉSULTAT ATTENDU:")
        print("  • Commune la moins chère: Poissy (103,651€)")
        print("  • Plus chère: Rambouillet (126,992€)")
        
        input("\n➜ Appuyez sur Entrée quand le graphique est prêt...")
        print("✅ Parfait! Continuons.\n")
    
    def display_step_4_scatter(self):
        """Étape 4: Nuage de points"""
        print("=" * 70)
        print("📌 ÉTAPE 4: CRÉER NUAGE DE POINTS - QUALITÉ vs PRIX")
        print("=" * 70)
        print("\n🎯 OBJECTIF: Voir relation entre prix total et prix/m²")
        
        print("\n🔧 ACTIONS DANS POWER BI:")
        print("  1. Insérer → 'Nuage de points'")
        print("  2. Axe X: Glissez 'PrixMoyen'")
        print("  3. Axe Y: Glissez 'PricePerm2' (€/m²)")
        print("  4. Légende: Glissez 'Commune'")
        print("  5. Taille de bulle: Glissez 'Nombre'")
        print("  6. Titre: 'Relation Prix vs Quality'")
        
        print("\n💡 INTERPRÉTATION:")
        print("  • Communes en bas-gauche = bon marché, bonne qualité ✅")
        print("  • Lagny-sur-Marne: 2,982€/m² (meilleur ratio)")
        
        input("\n➜ Appuyez sur Entrée quand le scatter plot est créé...")
        print("✅ Excellent! Continuons.\n")
    
    def display_step_5_table(self):
        """Étape 5: Tableau"""
        print("=" * 70)
        print("📌 ÉTAPE 5: CRÉER TABLEAU SYNTHÈSE")
        print("=" * 70)
        print("\n🎯 OBJECTIF: Afficher toutes les données en détail")
        
        print("\n🔧 ACTIONS DANS POWER BI:")
        print("  1. Insérer → 'Tableau'")
        print("  2. Glissez depuis le panneau droit:")
        print("     • Commune")
        print("     • Nombre")
        print("     • PrixMoyen")
        print("     • PrixMin")
        print("     • PrixMax")
        print("     • PricePerm2")
        print("  3. Cliquez sur 'PrixMoyen' → Tri croissant")
        print("  4. Titre: 'Synthèse détaillée'")
        
        input("\n➜ Appuyez sur Entrée quand le tableau est complet...")
        print("✅ Parfait! Continuons.\n")
    
    def display_step_6_slicers(self):
        """Étape 6: Slicers"""
        print("=" * 70)
        print("📌 ÉTAPE 6: AJOUTER FILTRES INTERACTIFS (SLICERS)")
        print("=" * 70)
        print("\n🎯 OBJECTIF: Permettre de filtrer par commune dynamiquement")
        
        print("\n🔧 ACTIONS DANS POWER BI:")
        print("  1. Insérer → 'Segment' (Slicer)")
        print("  2. Glissez 'Commune' dans le champ")
        print("  3. Positionnez à gauche (zone de filtrage)")
        print("  4. Cliquez sur chaque graphique → Format → Filtres")
        print("  5. Activez 'Commune' comme filtre pour tous")
        
        print("\n✨ RÉSULTAT:")
        print("  • Cliquez sur une commune → Tous les graphiques se mettent à jour!")
        print("  • Vous pouvez sélectionner plusieurs communes")
        
        input("\n➜ Appuyez sur Entrée quand les slicers sont branchés...")
        print("✅ Excellent! Continuons.\n")
    
    def display_step_7_theme(self):
        """Étape 7: Thème"""
        print("=" * 70)
        print("📌 ÉTAPE 7: PERSONNALISER LE THÈME ET LES COULEURS")
        print("=" * 70)
        print("\n🎯 OBJECTIF: Rendre le rapport visuellement attrayant")
        
        print("\n🔧 ACTIONS DANS POWER BI:")
        print("  (Optionnel mais recommandé)")
        print("  1. Affichage → 'Thèmes' (ruban supérieur)")
        print("  2. Sélectionnez un thème (ex: 'Bleu', 'Moderne')")
        print("  3. Pour personnalisation avancée:")
        print("     → Affichage → Thème → Gérer les thèmes")
        
        print("\n🎨 CONSEILS:")
        print("  • Thème bleu = aspect professionnel")
        print("  • Contraste élevé = meilleure lisibilité")
        
        input("\n➜ Appuyez sur Entrée après personnalisation...")
        print("✅ Bravo! Dernière étape.\n")
    
    def display_step_8_save(self):
        """Étape 8: Sauvegarde"""
        print("=" * 70)
        print("📌 ÉTAPE 8: ENREGISTRER LE RAPPORT")
        print("=" * 70)
        print("\n🎯 OBJECTIF: Sauvegarder votre rapport Power BI")
        
        print("\n🔧 ACTIONS DANS POWER BI:")
        print("  1. Fichier → 'Enregistrer sous' (Ctrl+Shift+S)")
        print("  2. Nom: rapport_immobilier.pbix")
        print(f"  3. Emplacement: {self.project_root / 'exports'}")
        print("  4. Cliquez sur 'Enregistrer'")
        
        print("\n✅ SUCCÈS!")
        print("  Votre rapport est maintenant .pbix (Power BI format)")
        
        input("\n➜ Appuyez sur Entrée après sauvegarde...")
        print("✅ Parfait! Rapport terminé.\n")
    
    def display_conclusion(self):
        """Affiche la conclusion"""
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 68 + "║")
        print("║" + "  🎉 RAPPORT POWER BI CRÉÉ AVEC SUCCÈS!".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("╚" + "═" * 68 + "╝")
        
        print("\n✨ RÉSUMÉ DE VOTRE RAPPORT:")
        print("  • 8 étapes complétées")
        print("  • 1 KPI (communes accessibles)")
        print("  • 1 Graphique à barres (top 10)")
        print("  • 1 Nuage de points (qualité/prix)")
        print("  • 1 Tableau synthèse (30 communes)")
        print("  • 1 Filtre interactif (slicer)")
        print("  • 1 Thème personnalisé")
        
        print("\n📊 DONNÉES CLÉS:")
        print("  ✓ 30 communes analysées")
        print("  ✓ 61 propriétés scrappées")
        print("  ✓ 6 communes accessibles ≤ 130k EUR")
        print("  ✓ Lagny-sur-Marne: Meilleur ratio (2,982€/m²)")
        
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("  1. Partager le rapport avec des collègues")
        print("  2. Publier sur Power BI Service (cloud)")
        print("     Fichier → Publier")
        print("  3. Ajouter des mesures DAX avancées")
        print("  4. Créer des pages détaillées par commune")
        
        print("\n" + "=" * 70)
        print("✨ Merci d'avoir suivi ce guide!")
        print("=" * 70 + "\n")
    
    def run_full_launcher(self):
        """Lance le processus complet"""
        # Vérifications
        self.display_banner()
        
        if not self.check_powerbi_installed():
            return
        
        if not self.check_csv_exists():
            return
        
        print("\n✅ Tous les fichiers requis sont présents!")
        print(f"✅ Power BI Desktop détecté: {self.powerbi_exe}")
        print(f"✅ Fichier CSV détecté: {self.csv_path}")
        
        input("\n➜ Appuyez sur Entrée pour lancer Power BI Desktop...\n")
        
        # Lancer Power BI
        if not self.launch_powerbi():
            return
        
        # Afficher les étapes guidées
        try:
            self.display_step_1_import()
            self.display_step_2_kpi()
            self.display_step_3_bar_chart()
            self.display_step_4_scatter()
            self.display_step_5_table()
            self.display_step_6_slicers()
            self.display_step_7_theme()
            self.display_step_8_save()
            self.display_conclusion()
        except KeyboardInterrupt:
            print("\n\n⚠️  Guide interrompu par l'utilisateur")
            print("✅ Power BI Desktop reste ouvert")
            print("💡 Vous pouvez continuer manuellement ou relancer ce script")


if __name__ == "__main__":
    launcher = PowerBILauncher()
    launcher.run_full_launcher()
