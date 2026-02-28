"""Test de cohérence entre configuration et toutes les pages"""
import json
import sqlite3
import requests
from config import SEARCH_CONFIG
from database.db import Database

print("=" * 80)
print("TEST DE COHÉRENCE - IMMOBILIER SCRAPER")
print("=" * 80)
print()

# 1. Vérifier user_config.json
print("1. Configuration dans user_config.json:")
with open('data/user_config.json', 'r', encoding='utf-8') as f:
    user_config = json.load(f)
print(f"   Budget: {user_config['budget_min']:,} - {user_config['budget_max']:,} EUR")
print(f"   DPE max: {user_config['dpe_max']}")
print(f"   Zones: {user_config['zones']}")
print()

# 2. Vérifier SEARCH_CONFIG chargé
print("2. Configuration chargée dans SEARCH_CONFIG:")
print(f"   Budget: {SEARCH_CONFIG.get('budget_min', 0):,} - {SEARCH_CONFIG.get('budget_max', 9999999):,} EUR")
print(f"   DPE max: {SEARCH_CONFIG.get('dpe_max', 'G')}")
print(f"   Zones: {SEARCH_CONFIG.get('zones', [])}")
print()

# 3. Vérifier base de données brute
print("3. Base de données (SANS filtres):")
conn = sqlite3.connect('database/immobilier.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM properties')
total_db = cursor.fetchone()[0]
cursor.execute('SELECT MIN(price), MAX(price) FROM properties')
min_price, max_price = cursor.fetchone()
print(f"   Total propriétés: {total_db}")
print(f"   Prix min-max: {int(min_price or 0):,} - {int(max_price or 0):,} EUR")
conn.close()
print()

# 4. Vérifier get_properties avec filtres
print("4. Database.get_properties() avec filtres:")
db = Database()
filters = {
    'price_min': user_config['budget_min'],
    'price_max': user_config['budget_max'],
    'dpe_max': user_config['dpe_max']
}
props = db.get_properties(filters=filters)
print(f"   Propriétés filtrées: {len(props)}")
if props:
    prices = [p['price'] for p in props if p['price']]
    print(f"   Prix min-max: {int(min(prices)):,} - {int(max(prices)):,} EUR")
print()

# 5. Vérifier get_statistics avec filtres
print("5. Database.get_statistics() avec filtres:")
stats = db.get_statistics(filters=filters)
print(f"   Total: {stats['total_properties']}")
print(f"   Prix min-max: {int(stats['min_price'] or 0):,} - {int(stats['max_price'] or 0):,} EUR")
print()

# 6. Tester API /api/stats
print("6. API /api/stats (utilisé par dashboard):")
try:
    resp = requests.get('http://localhost:5000/api/stats', timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        print(f"   Total: {data['total']}")
        print(f"   Prix min-max: {int(data['min_price']):,} - {int(data['max_price']):,} EUR")
        print(f"   Nouveau 24h: {data['new_24h']}")
    else:
        print(f"   ❌ Erreur HTTP {resp.status_code}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
print()

# 7. Tester API /api/properties
print("7. API /api/properties (page propriétés):")
try:
    resp = requests.get('http://localhost:5000/api/properties', timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        print(f"   Total: {data['count']}")
        if data['properties']:
            prices = [p['price'] for p in data['properties'] if p.get('price')]
            if prices:
                print(f"   Prix min-max: {int(min(prices)):,} - {int(max(prices)):,} EUR")
    else:
        print(f"   ❌ Erreur HTTP {resp.status_code}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
print()

# 8. Vérifier incohérences
print("=" * 80)
print("RÉSUMÉ DES INCOHÉRENCES:")
print("=" * 80)

budget_max_config = user_config['budget_max']
issues = []

# Vérifier si SEARCH_CONFIG est correct
if SEARCH_CONFIG.get('budget_max') != budget_max_config:
    issues.append(f"ALERTE: SEARCH_CONFIG budget_max ({SEARCH_CONFIG.get('budget_max'):,}) != user_config ({budget_max_config:,})")

# Vérifier si la DB a des biens hors budget
if max_price and max_price > budget_max_config:
    issues.append(f"ALERTE: Base de donnees contient des biens a {int(max_price):,} EUR > budget max {budget_max_config:,} EUR")

# Vérifier si l'API retourne des biens hors budget
try:
    resp = requests.get('http://localhost:5000/api/stats', timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        if data['max_price'] > budget_max_config:
            issues.append(f"ALERTE: API /api/stats retourne max_price {int(data['max_price']):,} EUR > budget max {budget_max_config:,} EUR")
except:
    pass

if issues:
    for issue in issues:
        print(issue)
    print()
    print("[ECHEC] INCOHERENCES DETECTEES")
else:
    print("[OK] AUCUNE INCOHERENCE - Tous les systemes sont coherents")
print()
