"""
Test complet du flux de configuration
"""
import requests
import json
import sqlite3
from pathlib import Path

print("=" * 100)
print("TEST COMPLET DU FLUX DE CONFIGURATION")
print("=" * 100)

# 1. Verifier l'etat actuel de la config
print("\n1. ETAT ACTUEL DE LA CONFIG")
print("-" * 100)

# Fichier
config_file = Path('data/user_config.json')
if config_file.exists():
    with open(config_file) as f:
        file_config = json.load(f)
    print(f"Fichier user_config.json:")
    print(f"  budget_min: {file_config.get('budget_min')}")
    print(f"  budget_max: {file_config.get('budget_max')}")
    print(f"  zones: {file_config.get('zones')}")
    print(f"  dpe_max: {file_config.get('dpe_max')}")
else:
    print("Fichier user_config.json: N'EXISTE PAS")

# Serveur
print(f"\nServeur (API /api/config/get):")
response = requests.get('http://localhost:5000/api/config/get')
if response.status_code == 200:
    api_config = response.json()['config']
    print(f"  budget_min: {api_config.get('budget_min')}")
    print(f"  budget_max: {api_config.get('budget_max')}")
    print(f"  zones: {api_config.get('zones')}")
    print(f"  dpe_max: {api_config.get('dpe_max')}")
else:
    print(f"  ERREUR: {response.status_code}")

# 2. Test de changement de config
print("\n2. TEST DE CHANGEMENT DE CONFIG")
print("-" * 100)

new_config = {
    "budget_min": 100000,
    "budget_max": 300000,
    "dpe_max": "D",
    "surface_min": 30,
    "email": "test@test.com",
    "email_password": "",
    "report_time": "09:00",
    "email_notifications": True,
    "zones": ["Paris", "Hauts-de-Seine", "Val-de-Marne"]
}

print(f"Envoi config: {json.dumps(new_config, indent=2, ensure_ascii=False)}")
response = requests.post('http://localhost:5000/api/config/save', json=new_config)
print(f"Response: {response.json()}")

# 3. Verifier que la config a ete SAUVEGARDEE
print("\n3. VERIFICATION APRES SAUVEGARDE")
print("-" * 100)

# Fichier
with open('data/user_config.json') as f:
    saved_config = json.load(f)
print(f"Fichier user_config.json apres sauvegarde:")
print(f"  budget_min: {saved_config.get('budget_min')}")
print(f"  budget_max: {saved_config.get('budget_max')}")
print(f"  zones: {saved_config.get('zones')}")

# Serveur
response = requests.get('http://localhost:5000/api/config/get')
api_config = response.json()['config']
print(f"\nServeur apres sauvegarde:")
print(f"  budget_min: {api_config.get('budget_min')}")
print(f"  budget_max: {api_config.get('budget_max')}")
print(f"  zones: {api_config.get('zones')}")

# 4. Verifier que la recherche fonctionne avec les bonnes zones
print("\n4. TEST DE RECHERCHE AVEC CONFIG")
print("-" * 100)

response = requests.post('http://localhost:5000/api/search', json={
    'price_min': 100000,
    'price_max': 300000,
    'dpe_max': 'D'
})
result = response.json()
print(f"Recherche (100k-300k, DPE D): {result.get('count')} resultats")

if result.get('properties'):
    # Verifier les communes retournees
    locations = set()
    for p in result['properties'][:10]:
        locations.add(p['location'])
    print(f"Communes trouvees: {locations}")

# 5. Tous les champs sont la?
print("\n5. VERIFICATION DES CHAMPS")
print("-" * 100)

if result.get('properties') and len(result['properties']) > 0:
    p = result['properties'][0]
    required_fields = ['id', 'title', 'price', 'location', 'dpe', 'posted_date']
    print(f"Champs dans la reponse: {list(p.keys())}")
    
    missing = [f for f in required_fields if f not in p]
    if missing:
        print(f"CHAMPS MANQUANTS: {missing}")
    else:
        print(f"[OK] Tous les champs requis presents")
        
    # Afficher le premier resultat
    print(f"\nPremier resultat:")
    for k, v in p.items():
        print(f"  {k}: {v}")

print("\n" + "=" * 100)
print("FIN TEST")
print("=" * 100)
