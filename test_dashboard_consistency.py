from database.db import Database
from config import SEARCH_CONFIG

db = Database()

# Appliquer les mêmes filtres que le dashboard et /properties
filters = {
    'price_min': SEARCH_CONFIG.get('budget_min', 0),
    'price_max': SEARCH_CONFIG.get('budget_max', 9999999),
    'dpe_max': SEARCH_CONFIG.get('dpe_max', 'G')
}

# Récupérer les statistiques avec filtres
stats = db.get_statistics(filters=filters)

# Récupérer les propriétés avec filtres
props = db.get_properties(filters=filters)

print(f"Configuration:")
print(f"  Budget: {filters['price_min']:,} - {filters['price_max']:,} EUR")
print(f"  DPE max: {filters['dpe_max']}")
print()
print(f"Dashboard (avec filtres):")
print(f"  Total propriétés: {stats['total_properties']}")
print(f"  Prix moyen: {int(stats['avg_price'] or 0):,} EUR")
print(f"  Prix min-max: {int(stats['min_price'] or 0):,} - {int(stats['max_price'] or 0):,} EUR")
print()
print(f"Page /properties (avec filtres):")
print(f"  Total propriétés: {len(props)}")
print()
print(f"✅ Les chiffres correspondent!" if stats['total_properties'] == len(props) else f"❌ Incohérence: {stats['total_properties']} vs {len(props)}")
