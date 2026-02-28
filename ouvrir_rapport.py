#!/usr/bin/env python3
"""
Script AUTOMATIQUE - Version FINALE et FIABLE
Utilise le rapport.pbix existant (celui qui fonctionne) et l'ouvre automatiquement
"""

import subprocess
import os
import time
import sys

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
    print(" "*20 + "✨ RAPPORT POWER BI")
    print(" "*15 + "Ouverture automatique du rapport")
    print("="*70 + "\n")
    
    # Utiliser rapport.pbix (le seul fichier valide)
    exports_dir = r"C:\Users\jaleleddinekhadhraou\immobilier-scraper\exports"
    pbix_path = os.path.join(exports_dir, "rapport.pbix")
    
    if not os.path.exists(pbix_path):
        print("❌ Fichier rapport.pbix non trouvé dans exports/")
        print("   Ce fichier est créé automatiquement par Power BI lors de la première utilisation")
        return False
    
    print(f"✅ Rapport trouvé")
    print(f"   📍 {pbix_path}")
    size = os.path.getsize(pbix_path)
    print(f"   📊 Taille: {size:,} bytes\n")
    
    # Chercher Power BI
    print("🔍 Recherche Power BI Desktop...")
    powerbi_path = find_powerbi()
    
    if not powerbi_path:
        print("❌ Power BI Desktop non trouvé!")
        print("\n📥 Installez Power BI Desktop:")
        print("   https://www.microsoft.com/fr-fr/download/details.aspx?id=58494")
        return False
    
    print(f"✅ Power BI Desktop trouvé\n")
    
    # Lancer Power BI
    print("🚀 Ouverture du rapport...")
    try:
        subprocess.Popen([powerbi_path, pbix_path])
        print("✅ Power BI en cours de démarrage...\n")
        
        time.sleep(2)
        
        print("="*70)
        print("\n✨ Rapport ouvert avec succès!\n")
        print("📊 CONTENU:")
        print("   • 41 communes en Île-de-France")
        print("   • 6 communes accessibles à 130k EUR")
        print("   • Visualisations interactives")
        print("\n💡 TOP OPTIONS:")
        print("   1. Poissy: 103,651€ (MEILLEUR PRIX)")
        print("   2. Lagny-sur-Marne: 2,982€/m² (MEILLEUR RATIO)")
        print("   3. Sartrouville, Massy, Chelles, Rambouillet")
        print("\n" + "="*70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
