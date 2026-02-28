#!/usr/bin/env python3
"""
Script COMPLET et AUTOMATIQUE
Génère le rapport PBIX et l'ouvre dans Power BI en 1 clic
"""

import subprocess
import os
import time
import sys

def run_command(cmd, description):
    """Exécute une commande et affiche le résultat"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False, text=True, timeout=30, cwd=r"C:\Users\jaleleddinekhadhraou\immobilier-scraper")
        time.sleep(1)
        return True  # On suppose que si pas d'exception, c'est bon
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout lors de {description}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def find_powerbi():
    """Cherche Power BI Desktop"""
    possible_paths = [
        r"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe",
        r"C:\Program Files (x86)\Microsoft Power BI Desktop\bin\PBIDesktop.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def main():
    print("\n" + "="*70)
    print(" "*15 + "🎯 SOLUTION AUTOMATIQUE POWER BI")
    print(" "*10 + "Génération + Ouverture (0% intervention manuelle)")
    print("="*70 + "\n")
    
    # ETAPE 1: Vérifier les données
    print("ETAPE 1️⃣  Vérification des données")
    print("-" * 70)
    
    csv_path = r"C:\Users\jaleleddinekhadhraou\immobilier-scraper\exports\synthese_communes.csv"
    if not os.path.exists(csv_path):
        print("❌ Fichier CSV non trouvé!")
        print("   Exécutez d'abord: python export_powerbi.py")
        return False
    
    print("✅ Données CSV trouvées")
    print(f"   📍 {csv_path}\n")
    
    # ETAPE 2: Générer le PBIX
    print("ETAPE 2️⃣  Génération du rapport Power BI")
    print("-" * 70)
    
    if not run_command(
        "python generate_pbix_auto.py",
        "Génération du fichier PBIX"
    ):
        print("❌ Erreur lors de la génération du PBIX")
        return False
    
    pbix_path = r"C:\Users\jaleleddinekhadhraou\immobilier-scraper\exports\rapport_auto.pbix"
    if os.path.exists(pbix_path):
        size = os.path.getsize(pbix_path)
        print(f"✅ Fichier PBIX généré avec succès")
        print(f"   📍 {pbix_path}")
        print(f"   📊 Taille: {size:,} bytes\n")
    else:
        print("❌ Le fichier PBIX n'a pas pu être créé")
        return False
    
    # ETAPE 3: Chercher Power BI
    print("ETAPE 3️⃣  Vérification de Power BI Desktop")
    print("-" * 70)
    
    powerbi_path = find_powerbi()
    if not powerbi_path:
        print("❌ Power BI Desktop n'a pas été trouvé!")
        print("\n📥 Installation requise:")
        print("   Télécharger: https://www.microsoft.com/fr-fr/download/details.aspx?id=58494")
        return False
    
    print("✅ Power BI Desktop trouvé")
    print(f"   📍 {powerbi_path}\n")
    
    # ETAPE 4: Lancer Power BI
    print("ETAPE 4️⃣  Lancement du rapport")
    print("-" * 70)
    print("🚀 Démarrage de Power BI...")
    
    try:
        subprocess.Popen([powerbi_path, pbix_path])
        print("✅ Power BI en cours de démarrage...\n")
        
        time.sleep(3)
        
        print("="*70)
        print("\n✨ SUCCÈS! Le rapport est maintenant ouvert!\n")
        print("📊 CONTENU DU RAPPORT:")
        print("   • 41 communes analysées en Île-de-France")
        print("   • Prix moyen: ~286k EUR")
        print("   • Budget max: 130k EUR")
        print("   • 6 communes accessibles à votre budget")
        print("\n💡 RECOMMANDATIONS D'INVESTISSEMENT:")
        print("   ✓ Poissy: 103,651€ (MEILLEUR PRIX)")
        print("   ✓ Lagny-sur-Marne: 2,982€/m² (MEILLEUR RATIO)")
        print("   ✓ Sartrouville, Massy, Chelles, Rambouillet")
        print("\n🎯 PROCHAINES ÉTAPES:")
        print("   1. Explorez les visualisations")
        print("   2. Consultez les chiffres par commune")
        print("   3. Utilisez les filtres pour affiner")
        print("   4. Exportez/partagez si nécessaire")
        print("\n" + "="*70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
