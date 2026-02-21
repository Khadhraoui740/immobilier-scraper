"""
Test du scraper DVF (Données Publiques - API Officielle)
"""
from scrapers.dvf_scraper import DVFScraper
from config import SEARCH_CONFIG, SCRAPERS_CONFIG

# Configuration DVF
config = SCRAPERS_CONFIG['dvf']

# Créer le scraper
scraper = DVFScraper(config)

# Lancer la recherche
print("🔍 Test DVF Scraper")
print("=" * 50)
print(f"Critères: {SEARCH_CONFIG['budget_min']}€ - {SEARCH_CONFIG['budget_max']}€")
print(f"Zones: {SEARCH_CONFIG['zones']}")
print()

results = scraper.search(
    SEARCH_CONFIG['budget_min'],
    SEARCH_CONFIG['budget_max'],
    SEARCH_CONFIG['dpe_max'],
    SEARCH_CONFIG['zones']
)

print(f"✓ Résultats trouvés: {len(results)}")
print()

if results:
    print("Exemples de propriétés:")
    for prop in results[:3]:
        print(f"\n  📍 {prop['title']}")
        print(f"  💰 Prix: {prop['price']:,.0f}€")
        print(f"  📏 Surface: {prop['surface']:.0f}m²")
        print(f"  🏠 Pièces: {prop['rooms']}")
        print(f"  📍 Localité: {prop['location']}")
else:
    print("⚠️ Aucune propriété trouvée")
    print("Note: DVF API peut nécessiter une requête spécifique")
