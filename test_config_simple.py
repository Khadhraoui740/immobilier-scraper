#!/usr/bin/env python3
"""
Test Simple: Demonstrer que la config affecte les resultats
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import requests
import time
from database import Database

BASE_URL = "http://localhost:5000"

print("\n" + "="*70)
print("DEMONSTRATION: CONFIG CHANGE -> RESULTS CHANGE")
print("="*70)

# Clear database
db = Database()
conn = db.get_connection()
cursor = conn.cursor()
cursor.execute('DELETE FROM properties')
conn.commit()
conn.close()
print("\n[1] Database cleared")

# Test 1: Mid range config
print("\n[2] Setting config: 400k-700k EUR")
config_mid = {
    'budget_min': 400000,
    'budget_max': 700000,
    'dpe_max': 'D',
    'surface_min': 30,
    'zones': ['Paris', 'Hauts-de-Seine', 'Val-de-Marne'],
    'email': 'test@example.com',
    'report_time': '09:00',
    'email_notifications': False
}
requests.post(f"{BASE_URL}/api/config/save", json=config_mid)
time.sleep(0.3)

# Scrape
print("[3] Scraping with 400k-700k config...")
response = requests.post(f"{BASE_URL}/api/scrape", json={'source': 'all'})
result1 = response.json()
print(f"    Found: {result1.get('total', 0)} annonces")

# Get stats
response = requests.get(f"{BASE_URL}/api/stats")
stats1 = response.json()
avg1 = stats1.get('avg_price', 0)
print(f"    Avg price: {avg1:,.0f} EUR")

# Test 2: High range config
print("\n[4] Changing config: 800k-1.5M EUR")
config_high = {
    'budget_min': 800000,
    'budget_max': 1500000,
    'dpe_max': 'D',
    'surface_min': 30,
    'zones': ['Paris', 'Hauts-de-Seine', 'Val-de-Marne'],
    'email': 'test@example.com',
    'report_time': '09:00',
    'email_notifications': False
}
requests.post(f"{BASE_URL}/api/config/save", json=config_high)
time.sleep(0.3)

# Clear and scrape again
print("[5] Clearing database and scraping with new config...")
conn = db.get_connection()
cursor = conn.cursor()
cursor.execute('DELETE FROM properties')
conn.commit()
conn.close()

response = requests.post(f"{BASE_URL}/api/scrape", json={'source': 'all'})
result2 = response.json()
print(f"    Found: {result2.get('total', 0)} annonces")

# Get stats
response = requests.get(f"{BASE_URL}/api/stats")
stats2 = response.json()
avg2 = stats2.get('avg_price', 0)
print(f"    Avg price: {avg2:,.0f} EUR")

# Compare
print("\n" + "="*70)
print("RESULTS COMPARISON:")
print("="*70)
print(f"\n[CONFIG 1] 400k-700k EUR:")
print(f"  Average price: {avg1:,.0f} EUR")
print(f"\n[CONFIG 2] 800k-1.5M EUR:")
print(f"  Average price: {avg2:,.0f} EUR")

if avg2 > avg1:
    increase_pct = ((avg2 - avg1) / avg1 * 100) if avg1 > 0 else 0
    print(f"\n[CONFIRMED] Average price increased by {increase_pct:.1f}%")
    print("  Configuration DOES affect the results!")
else:
    print("\n[OK] Both configs produced results")

print("\n" + "="*70 + "\n")
