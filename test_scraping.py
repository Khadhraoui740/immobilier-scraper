#!/usr/bin/env python3
"""Test rapide du scraping"""
import sys
from config import SEARCH_CONFIG
from scrapers.manager import ScraperManager

# Tester avec critères élargis
print("Test scraping avec critères élargis...")
manager = ScraperManager()

results = manager.scrape_all(
    budget_min=150000,
    budget_max=600000,
    dpe_max='G',
    zones=['Paris', 'Hauts-de-Seine', 'Val-de-Marne']
)

print(f"\nTotal annonces trouvées: {len(results)}")
for prop in results[:5]:
    print(f"- {prop.get('title', 'N/A')} - {prop.get('price', 'N/A')}€")
