#!/usr/bin/env python3
"""
Ouvre automatiquement le rapport PBIX dans Power BI Desktop
"""

import subprocess
import os
import time
import sys

def find_powerbi():
    """Cherche Power BI Desktop sur la machine"""
    possible_paths = [
        r"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe",
        r"C:\Program Files (x86)\Microsoft Power BI Desktop\bin\PBIDesktop.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def main():
    print("\n" + "="*60)
    print("📖 OUVERTURE DU RAPPORT POWER BI")
    print("="*60 + "\n")
    
    # Cherche le fichier PBIX
    pbix_path = r"C:\Users\jaleleddinekhadhraou\immobilier-scraper\exports\rapport_auto.pbix"
    
    if not os.path.exists(pbix_path):
        print(f"❌ Fichier non trouve: {pbix_path}")
        print("   Executez d'abord: python generate_pbix_auto.py")
        return False
    
    print(f"✓ Fichier PBIX trouve")
    print(f"  📍 {pbix_path}")
    
    # Cherche Power BI
    print("\n🔍 Recherche de Power BI Desktop...")
    powerbi_path = find_powerbi()
    
    if not powerbi_path:
        print("❌ Power BI Desktop n'a pas ete trouve!")
        print("\n📥 Installation requise:")
        print("   1. Telecharger: https://www.microsoft.com/fr-fr/download/details.aspx?id=58494")
        print("   2. Installer normalement")
        print("   3. Relancer ce script")
        return False
    
    print(f"✓ Power BI Desktop trouve")
    print(f"  📍 {powerbi_path}")
    
    # Lance Power BI
    print("\n🚀 Demarrage de Power BI...")
    try:
        subprocess.Popen([powerbi_path, pbix_path])
        print("✅ Power BI en demarrage...")
        print("\n💡 Le rapport va s'ouvrir dans quelques secondes...")
        print("   - Les donnees sont deja chargees")
        print("   - Vous pouvez consulter les visualisations")
        print("   - Cliquez sur 'Enregistrer' si vous voulez faire des modifications\n")
        
        time.sleep(3)
        print("="*60)
        print("✨ Rapport ouvert! Vous pouvez commencer a l'analyser.")
        print("="*60 + "\n")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
