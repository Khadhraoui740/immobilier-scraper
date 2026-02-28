from database.db import Database
from config import SEARCH_CONFIG

db = Database()

# Appliquer les mêmes filtres que app.py
filters = {
    'price_min': SEARCH_CONFIG.get('budget_min', 0),
    'price_max': SEARCH_CONFIG.get('budget_max', 9999999),
    'dpe_max': SEARCH_CONFIG.get('dpe_max', 'G')
}

props = db.get_properties(filters=filters)

# Filtrer par zones
zones = SEARCH_CONFIG.get('zones', [])
if zones:
    filtered_props = []
    for p in props:
        location = p['location'] or ''
        if any(zone in location for zone in zones):
            filtered_props.append(p)
    props = filtered_props

print(f"Configuration:")
print(f"  Budget: {filters['price_min']:,} - {filters['price_max']:,} EUR")
print(f"  DPE max: {filters['dpe_max']}")
print(f"  Zones: {zones}")
print(f"\nRésultat: {len(props)} propriétés filtrées")

if props:
    print(f"\nExemples (5 premiers):")
    for p in props[:5]:
        print(f"  - {p['location']}: {p['price']:,} EUR - DPE {p['dpe']}")
