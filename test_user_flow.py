"""
Simulation de l'interaction utilisateur sur /config
"""
import requests
import json
import time

print("=" * 100)
print("SIMULATION DE L'INTERACTION UTILISATEUR")
print("=" * 100)

# 1. L'utilisateur accede a /config et loadConfig() est appelee
print("\n1. PAGE /config CHARGEE -> loadConfig() appelee")
print("-" * 100)

response = requests.get('http://localhost:5000/api/config/get')
api_config = response.json()['config']
print(f"loadConfig() retourne:")
print(f"  budget_min: {api_config['budget_min']}")
print(f"  budget_max: {api_config['budget_max']}")
print(f"  zones: {api_config['zones']}")

# Les zones dans le formulaire doivent etre cochees si elles sont dans zones
print(f"\nZones qui devraient etre cochees:")
if api_config['zones']:
    for zone in api_config['zones']:
        print(f"  - {zone}")
else:
    print(f"  AUCUNE (zones est vide!)")

# 2. L'utilisateur change les valeurs
print("\n2. UTILISATEUR CHANGE LES VALEURS")
print("-" * 100)

print(f"L'utilisateur change:")
print(f"  budget_min: {api_config['budget_min']} -> 50000")
print(f"  budget_max: {api_config['budget_max']} -> 200000")
print(f"  zones: {api_config['zones']} -> ['Paris', 'Hauts-de-Seine', 'Val-de-Marne', 'Essonne', 'Seine-et-Marne', 'Yvelines']")

# Simuler les codes postaux coches:
# Si les zones dans la config sont vides, les checkboxes du HTML sont CHECKED par defaut
# Donc les zones cochees par defaut seraient 75, 92, 94 (Paris, Hauts-de-Seine, Val-de-Marne)
# Mais si l'utilisateur coche AUSSI 91, 77, 78, il enverrait tous les 6

postal_codes = {
    '75': 'Paris',
    '92': 'Hauts-de-Seine',
    '94': 'Val-de-Marne',
    '91': 'Essonne',
    '77': 'Seine-et-Marne',
    '78': 'Yvelines'
}

# Simuler: l'utilisateur coche TOUTES les zones
checked_postcodes = list(postal_codes.keys())
print(f"\nZones cochees (codes postaux): {checked_postcodes}")

# Convertir en zone names (comme saveConfig() le ferait)
zones_to_send = [postal_codes[code] for code in checked_postcodes]
print(f"Zones converties en noms: {zones_to_send}")

# 3. Sauvegarder
print("\n3. UTILISATEUR CLIQUE 'Enregistrer'")
print("-" * 100)

new_config = {
    "budget_min": 50000,
    "budget_max": 200000,
    "dpe_max": "D",
    "surface_min": 30,
    "email": "khadhraoui.jalel@gmail.com",
    "email_password": "",
    "report_time": "09:00",
    "email_notifications": True,
    "zones": zones_to_send
}

print(f"saveConfig() envoie:")
print(json.dumps(new_config, indent=2, ensure_ascii=False))

response = requests.post('http://localhost:5000/api/config/save', json=new_config)
print(f"\nReponse API: {response.json()}")

# 4. Verifier la sauvegarde
print("\n4. VERIFICATION DE LA SAUVEGARDE")
print("-" * 100)
time.sleep(0.5)

response = requests.get('http://localhost:5000/api/config/get')
saved_config = response.json()['config']
print(f"Config sauvegardee:")
print(f"  budget_min: {saved_config['budget_min']}")
print(f"  budget_max: {saved_config['budget_max']}")
print(f"  zones: {saved_config['zones']}")

# 5. Verifier que la recherche retourne les bons resultats
print("\n5. VERIFIER LA RECHERCHE")
print("-" * 100)

response = requests.post('http://localhost:5000/api/search', json={
    'price_min': saved_config['budget_min'],
    'price_max': saved_config['budget_max'],
    'dpe_max': saved_config['dpe_max']
})
result = response.json()
count = result.get('count', 0)
print(f"Recherche avec config: {count} resultats")

if count > 0:
    print(f"\nPremier resultat:")
    p = result['properties'][0]
    print(f"  Titre: {p['title']}")
    print(f"  Prix: {p['price']} EUR")
    print(f"  Commune: {p['location']}")
    print(f"  DPE: {p['dpe']}")
    print(f"  Date: {p['posted_date']}")
    
    print("\n[OK] TOUT FONCTIONNE!")
else:
    print(f"\n[ERREUR] Aucun resultat?")

print("\n" + "=" * 100)
print("FIN TEST")
print("=" * 100)
