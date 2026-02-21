"""
Script pour déclencher le scraping DVF via l'API
"""
import requests
import json

# Appeler l'API de scraping
url = 'http://localhost:5000/api/scrape'
payload = {'source': 'dvf'}

try:
    resp = requests.post(url, json=payload, timeout=60)
    result = resp.json()
    
    print("✅ Scraping DVF lancé!")
    print(f"  📊 Propriétés trouvées: {result.get('found')}")
    print(f"  💾 Nouvelles en base: {result.get('new_saved')}")
    print(f"  📝 Message: {result.get('message')}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
