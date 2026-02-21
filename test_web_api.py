#!/usr/bin/env python3
"""
Test complet de l'interface web - Tous les endpoints
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_endpoints():
    """Test tous les endpoints"""
    print("\n" + "="*70)
    print("TEST D'INTEGRATION WEB - TOUS LES ENDPOINTS")
    print("="*70)
    
    # Test 1: Dashboard
    print("\n[1] Test Dashboard")
    print("-"*70)
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Titre contient 'Dashboard': {'Dashboard' in response.text or 'dashboard' in response.text}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    # Test 2: Properties
    print("\n[2] Test Page Proprietes")
    print("-"*70)
    try:
        response = requests.get(f"{BASE_URL}/properties")
        print(f"Status: {response.status_code}")
        print(f"Contient 'properties': {'properties' in response.text.lower()}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    # Test 3: Search
    print("\n[3] Test Page Recherche")
    print("-"*70)
    try:
        response = requests.get(f"{BASE_URL}/search")
        print(f"Status: {response.status_code}")
        print(f"Contient 'search': {'search' in response.text.lower()}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    # Test 4: Config
    print("\n[4] Test Page Configuration")
    print("-"*70)
    try:
        response = requests.get(f"{BASE_URL}/config")
        print(f"Status: {response.status_code}")
        print(f"Contient 'config': {'config' in response.text.lower()}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    # Test 5: API Stats
    print("\n[5] Test API /api/stats")
    print("-"*70)
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Annonces: {data.get('total_properties', 'N/A')}")
        print(f"Prix moyen: {data.get('avg_price', 'N/A')}")
        print(f"Par source: {data.get('by_source', {})}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    # Test 6: API Get Config
    print("\n[6] Test API /api/config/get")
    print("-"*70)
    try:
        response = requests.get(f"{BASE_URL}/api/config/get")
        print(f"Status: {response.status_code}")
        data = response.json()
        if data.get('success'):
            config = data.get('config', {})
            print(f"Budget min: {config.get('budget_min')} EUR")
            print(f"Budget max: {config.get('budget_max')} EUR")
            print(f"DPE max: {config.get('dpe_max')}")
            print(f"Zones: {config.get('zones')}")
        else:
            print(f"ERREUR: {data.get('error')}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    # Test 7: Modification config
    print("\n[7] Test API /api/config/save (modification)")
    print("-"*70)
    try:
        new_config = {
            'budget_min': 350000,
            'budget_max': 750000,
            'dpe_max': 'E',
            'surface_min': 40,
            'zones': ['Paris', 'Hauts-de-Seine'],
            'email': 'test@example.com',
            'report_time': '10:00',
            'email_notifications': True
        }
        response = requests.post(f"{BASE_URL}/api/config/save", json=new_config)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Message: {data.get('message')}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    # Test 8: Verification config modifiee
    print("\n[8] Verification config apres modification")
    print("-"*70)
    try:
        response = requests.get(f"{BASE_URL}/api/config/get")
        data = response.json()
        config = data.get('config', {})
        print(f"Budget min: {config.get('budget_min')} EUR (attendu: 350000)")
        print(f"Budget max: {config.get('budget_max')} EUR (attendu: 750000)")
        print(f"Zones: {config.get('zones')} (attendu: ['Paris', 'Hauts-de-Seine'])")
        
        # Valider
        assert config.get('budget_min') == 350000, "Budget min incorrect!"
        assert config.get('budget_max') == 750000, "Budget max incorrect!"
        print("   VALIDATION: OK")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    # Test 9: Scraping via API
    print("\n[9] Test API /api/scrape (avec nouvelle config)")
    print("-"*70)
    try:
        response = requests.post(f"{BASE_URL}/api/scrape", json={'source': 'all'})
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Total trouvees: {data.get('total')}")
        print(f"Nouvelles: {data.get('new')}")
        print(f"Message: {data.get('message')}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    # Test 10: Verifier stats apres scraping
    print("\n[10] Verification stats apres scraping")
    print("-"*70)
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        data = response.json()
        print(f"Total annonces: {data.get('total_properties', 'N/A')}")
        print(f"Prix moyen: {data.get('avg_price', 'N/A'):,.0f} EUR")
        print(f"Prix min: {data.get('min_price', 'N/A'):,.0f} EUR")
        print(f"Prix max: {data.get('max_price', 'N/A'):,.0f} EUR")
        print(f"Par source: {data.get('by_source', {})}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    # Test 11: Recherche avancee
    print("\n[11] Test API /api/search (recherche avancee)")
    print("-"*70)
    try:
        search_filters = {
            'price_min': 300000,
            'price_max': 600000,
            'dpe_max': 'D'
        }
        response = requests.post(f"{BASE_URL}/api/search", json=search_filters)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Resultats trouves: {len(data) if isinstance(data, list) else 'N/A'}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    # Test 12: Logs
    print("\n[12] Test Page Logs")
    print("-"*70)
    try:
        response = requests.get(f"{BASE_URL}/logs")
        print(f"Status: {response.status_code}")
        print(f"Contient logs: {'logs' in response.text.lower()}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    # Cleanup
    print("\n[13] Restaurer config originale")
    print("-"*70)
    try:
        original_config = {
            'budget_min': 200000,
            'budget_max': 500000,
            'dpe_max': 'D',
            'surface_min': 30,
            'zones': ['Paris', 'Hauts-de-Seine', 'Val-de-Marne'],
            'email': 'khadhraoui.jalel@gmail.com',
            'report_time': '09:00',
            'email_notifications': True
        }
        response = requests.post(f"{BASE_URL}/api/config/save", json=original_config)
        print(f"Config restauree: {response.json().get('success')}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    print("\n" + "="*70)
    print("TESTS D'INTEGRATION COMPLETS!")
    print("="*70 + "\n")

if __name__ == '__main__':
    print("\nAttendre que le serveur Web soit pret...")
    print("Assurez-vous que Flask fonctionne sur http://localhost:5000")
    time.sleep(2)
    
    test_endpoints()
