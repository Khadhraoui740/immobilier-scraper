#!/usr/bin/env python3
"""
Test du scenario exact de l'utilisateur
- BD vide au depart
- Changer config via page Web
- Scraper et verifier le dashboard
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import requests
import json
import time
from database import Database

BASE_URL = "http://localhost:5000"

def reset_database():
    """Viderla BD pour un test propre"""
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM properties')
    conn.commit()
    conn.close()
    print("[*] BD videe et prete pour le test")

def main():
    """Reproduire le scenario exact de l'utilisateur"""
    print("\n" + "="*70)
    print("TEST SCENARIO UTILISATEUR - CONFIG + SCRAPING + DASHBOARD")
    print("="*70)
    
    # ETAPE 1: Vider BD
    print("\n[ETAPE 1] Nettoyage Base de Donnees")
    print("-"*70)
    reset_database()
    
    # ETAPE 2: Configuration initiale
    print("\n[ETAPE 2] Verifier config initiale")
    print("-"*70)
    try:
        response = requests.get(f"{BASE_URL}/api/config/get")
        data = response.json()
        config = data.get('config', {})
        print(f"Config Initiale:")
        print(f"  Budget: {config.get('budget_min')} - {config.get('budget_max')} EUR")
        print(f"  DPE: {config.get('dpe_max')}")
        print(f"  Zones: {config.get('zones')}")
    except Exception as e:
        print(f"ERREUR: {e}")
        return
    
    # ETAPE 3: Scraper avec config initiale
    print("\n[ETAPE 3] Scraper avec config initiale")
    print("-"*70)
    try:
        response = requests.post(f"{BASE_URL}/api/scrape", json={'source': 'all'})
        data = response.json()
        print(f"Resultats: {data.get('total')} annonces trouvees")
        print(f"Nouvelles: {data.get('new')} ajoutees")
        
        response = requests.get(f"{BASE_URL}/api/stats")
        stats = response.json()
        print(f"Annonces en BD: {stats.get('total_properties', 'N/A')}")
        avg = stats.get('avg_price', 0)
        print(f"Prix moyen: {avg:,.0f} EUR")
    except Exception as e:
        print(f"ERREUR: {e}")
        return
    
    # ETAPE 4: Modifier la config (scenario de l'utilisateur)
    print("\n[ETAPE 4] Modifier Configuration COMME DANS LA PAGE WEB")
    print("-"*70)
    try:
        new_config = {
            'budget_min': 300000,  # Modifie
            'budget_max': 700000,  # Modifie
            'dpe_max': 'D',
            'surface_min': 30,
            'zones': ['Paris', 'Hauts-de-Seine', 'Val-de-Marne'],
            'email': 'khadhraoui.jalel@gmail.com',
            'report_time': '09:00',
            'email_notifications': True
        }
        
        response = requests.post(f"{BASE_URL}/api/config/save", json=new_config)
        data = response.json()
        
        if data.get('success'):
            print(f"NOUVELLE CONFIG:")
            print(f"  Budget: {new_config.get('budget_min')} - {new_config.get('budget_max')} EUR")
            print(f"  DPE: {new_config.get('dpe_max')}")
            print(f"  Message: {data.get('message')}")
        else:
            print(f"ERREUR sauvegarde: {data.get('error')}")
    except Exception as e:
        print(f"ERREUR: {e}")
        return
    
    # ETAPE 5: Verifier que la config est bien modifiee
    print("\n[ETAPE 5] Verifier que config est bien sauvegardee")
    print("-"*70)
    try:
        response = requests.get(f"{BASE_URL}/api/config/get")
        data = response.json()
        config = data.get('config', {})
        
        print(f"Config Chargee:")
        print(f"  Budget: {config.get('budget_min')} - {config.get('budget_max')} EUR")
        print(f"  Validation: Budget min == 300000? {config.get('budget_min') == 300000}")
        print(f"  Validation: Budget max == 700000? {config.get('budget_max') == 700000}")
    except Exception as e:
        print(f"ERREUR: {e}")
        return
    
    # ETAPE 6: Attendre et relancer le scraping
    print("\n[ETAPE 6] Lancer NOUVEAU scraping avec nouvelle config")
    print("-"*70)
    time.sleep(1)  # Petit delai pour s'assurer que config est appliquee
    
    try:
        response = requests.post(f"{BASE_URL}/api/scrape", json={'source': 'all'})
        data = response.json()
        print(f"Resultats: {data.get('total')} annonces trouvees")
        print(f"Nouvelles: {data.get('new')} ajoutees")
        print(f"Message: {data.get('message')}")
        
        if data.get('total') == 0:
            print("\n[ATTENTION] 0 annonces trouvees! C'est le BUG signale par l'utilisateur")
        else:
            print("\n[OK] Annonces trouvees avec nouvelle config")
    except Exception as e:
        print(f"ERREUR: {e}")
        return
    
    # ETAPE 7: Verifier le Dashboard
    print("\n[ETAPE 7] Verifier Dashboard apres scraping")
    print("-"*70)
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        stats = response.json()
        
        total = stats.get('total_properties', 'N/A')
        avg = stats.get('avg_price', 0)
        
        print(f"Dashboard Stats:")
        print(f"  Total annonces: {total}")
        print(f"  Prix moyen: {avg:,.0f} EUR")
        print(f"  Par source: {stats.get('by_source', {})}")
        print(f"  Par statut: {stats.get('by_status', {})}")
        
        print(f"\nDashboard Page: http://localhost:5000")
        print(f"Proprietes Page: http://localhost:5000/properties")
    except Exception as e:
        print(f"ERREUR: {e}")
        return
    
    # ETAPE 8: Validation complete
    print("\n[ETAPE 8] VALIDATION COMPLETE")
    print("-"*70)
    print("""
CHECKLIST:
  [*] Configuration modifiee via API
  [*] Config sauvegardee en user_config.json
  [*] Scraping lance avec nouvelle config
  [*] Annonces ajoutees en BD
  [*] Dashboard affiche les resultats
  
SI TOUS LES TESTS SONT OK:
  => LE SYSTEME FONCTIONNE CORRECTEMENT!
  
SI VOUS AVEZ 0 ANNONCES:
  => Vérifiez les logs pour les erreurs
  => Utilisez 'python scrape_live.py' en ligne de commande
  => Vérifiez que la config est bien sauvegardée
""")
    
    print("\n" + "="*70)
    print("TEST SCENARIO COMPLET TERMINE")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
