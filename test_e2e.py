"""
Test de bout en bout complet - Vérifier tous les endpoints et pages
"""
import requests
import json
from database.db import Database
from config import SEARCH_CONFIG, SCRAPERS_CONFIG

print("=" * 60)
print("🧪 TEST DE BOUT EN BOUT - VÉRIFICATION COMPLÈTE")
print("=" * 60)

# ============================================================================
# 1. VÉRIFIER LA BASE DE DONNÉES
# ============================================================================
print("\n1️⃣  VÉRIFICATION BASE DE DONNÉES")
print("-" * 60)

db = Database()
conn = db.get_connection()
c = conn.cursor()

# Total propriétés
c.execute('SELECT COUNT(*) FROM properties')
total = c.fetchone()[0]
print(f"   📊 Total propriétés en BD: {total}")

# Par source
c.execute('SELECT source, COUNT(*) as cnt FROM properties GROUP BY source')
print(f"   📍 Par source:")
for src, cnt in c.fetchall():
    print(f"      • {src}: {cnt}")

# Exemples
c.execute('SELECT id, title, price, location FROM properties LIMIT 3')
print(f"\n   📋 Exemples:")
for id, title, price, location in c.fetchall():
    print(f"      • {title} - {price:,.0f}€ ({location})")

conn.close()

# ============================================================================
# 2. VÉRIFIER LES ENDPOINTS DE L'API
# ============================================================================
print("\n\n2️⃣  VÉRIFICATION ENDPOINTS API")
print("-" * 60)

base_url = 'http://localhost:5000'

endpoints = [
    ('GET', '/', 'Page d\'accueil (Dashboard)'),
    ('GET', '/properties', 'Page Propriétés'),
    ('GET', '/dashboard', 'Dashboard'),
    ('POST', '/api/search', 'API Recherche (JSON)'),
    ('GET', '/api/stats', 'API Statistiques (JSON)'),
]

for method, endpoint, desc in endpoints:
    try:
        if method == 'GET':
            resp = requests.get(f'{base_url}{endpoint}', timeout=5)
        status_emoji = '✅' if resp.status_code == 200 else '❌'
        print(f"   {status_emoji} {endpoint:25} ({resp.status_code}) - {desc}")
        
        # Pour les APIs JSON, ajouter infos supplémentaires
        if resp.status_code == 200 and endpoint.startswith('/api'):
            try:
                if method == 'GET':
                    data = resp.json()
                    if isinstance(data, dict) and 'total' in data:
                        print(f"      → Total: {data.get('total')}, Prix moyen: {data.get('avg_price')}")
                elif method == 'POST':
                    # Pour /api/search on poste des filtres simples
                    data = resp.json()
                    if data.get('success'):
                        print(f"      → Propriétés retournées: {data.get('count')}")
            except:
                pass
    except Exception as e:
        print(f"   ❌ {endpoint:25} - Erreur: {str(e)[:40]}")

# ============================================================================
# 3. VÉRIFIER LES CONTENUS DES PAGES
# ============================================================================
print("\n\n3️⃣  VÉRIFICATION CONTENU HTML")
print("-" * 60)

# Dashboard
try:
    resp = requests.get(f'{base_url}/', timeout=5)
    if 'propriét' in resp.text.lower():
        # Chercher le nombre d'annonces dans le dashboard
        import re
        matches = re.findall(r'(\d+)\s*(annonce|propriét|result)', resp.text.lower())
        props_count = None
        for match in matches:
            if match[0].isdigit():
                try:
                    num = int(match[0])
                    if 50 > num > 0:  # Nombre plausible
                        props_count = num
                        break
                except:
                    pass
        
        if props_count:
            print(f"   ✅ Dashboard: {props_count} propriétés trouvées dans le HTML")
        else:
            print(f"   ⚠️  Dashboard: Contenu détecté mais nombre pas trouvé")
    else:
        # Chercher "44" ou tout nombre
        import re
        all_numbers = re.findall(r'\d+', resp.text)
        print(f"   📟 Dashboard: Nombres trouvés: {set(all_numbers)}")
except Exception as e:
    print(f"   ❌ Dashboard: Erreur {e}")

# Page Propriétés
try:
    resp = requests.get(f'{base_url}/properties', timeout=5)
    if '<table' in resp.text or 'property' in resp.text.lower():
        import re
        # Chercher les lignes de propriétés
        matches = re.findall(r'<tr|<div class="property|class=".*property', resp.text.lower())
        print(f"   ✅ Propriétés: Page chargée ({len(matches)} éléments property détectés)")
    else:
        print(f"   ⚠️  Propriétés: Page chargée mais structure différente")
except Exception as e:
    print(f"   ❌ Propriétés: Erreur {e}")

# ============================================================================
# 4. VÉRIFIER L'API JSON DIRECTEMENT
# ============================================================================
print("\n\n4️⃣  VÉRIFICATION API JSON DÉTAILLÉE")
print("-" * 60)

try:
    # Tester /api/search avec filtres vides
    resp = requests.post(f'{base_url}/api/search', json={}, timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        if data.get('success'):
            print(f"   ✅ /api/search retourne {data.get('count')} propriétés (limitées à 50)")
            if data.get('properties'):
                prop = data['properties'][0]
                print(f"\n   🔍 Exemple: title={prop.get('title')}, price={prop.get('price')}, source={prop.get('source')}")
        else:
            print(f"   ⚠️ /api/search: success=False")
    else:
        print(f"   ❌ /api/search retourna {resp.status_code}")
except Exception as e:
    print(f"   ❌ Erreur parsing JSON: {e}")

# ============================================================================
# 5. TESTER UN SCRAPING COMPLET
# ============================================================================
print("\n\n5️⃣  TEST SCRAPING COMPLET")
print("-" * 60)

try:
    resp = requests.post(
        f'{base_url}/api/scrape',
        json={'source': 'all'},
        timeout=60
    )
    if resp.status_code == 200:
        result = resp.json()
        print(f"   ✅ Scraping lancé")
        print(f"   📊 Message: {result.get('message')}")
        
        # Recompter après scraping
        conn = db.get_connection()
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM properties')
        new_total = c.fetchone()[0]
        conn.close()
        
        print(f"   📈 Avant: {total} → Après: {new_total} ({new_total - total:+d})")
    else:
        print(f"   ❌ Scraping retourna {resp.status_code}")
except Exception as e:
    print(f"   ❌ Erreur scraping: {e}")

# ============================================================================
# RÉSUMÉ
# ============================================================================
print("\n" + "=" * 60)
print("📌 RÉSUMÉ")
print("=" * 60)
print("""
✅ Si vous voyez:
  • BD: 44+ propriétés
  • Dashboard: Nombre affiché
  • Propriétés: Liste visible
  • API: Données JSON correctes
  → Tout fonctionne! ✨

❌ Si problème:
  • BD OK, Dashboard OK, mais Propriétés vide
    → Bug dans le template properties.html
  
  • API retourne 0 propriétés
    → Problème dans app.py /api/properties
    
  • Dashboard affiche un nombre différent de la BD
    → Problème dans le calcul des statistiques
""")
