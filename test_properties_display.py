#!/usr/bin/env python3
"""Test pour vérifier que les propriétés affichent location et posted_date"""

import sys
from database.db import Database

def test_properties_route():
    """Vérifie que les données de properties incluent location et posted_date"""
    print("=" * 80)
    print("TEST: Données de la route /properties")
    print("=" * 80)
    
    db = Database()
    props = db.get_properties()
    
    if not props:
        print("❌ ERREUR: Aucune propriété dans la base de données")
        return False
    
    # Simuler ce que fait la route /properties
    properties_list = []
    for p in props[:5]:  # Tester les 5 premières
        prop_dict = {
            'id': p['id'],
            'title': p['title'],
            'price': f"{p['price']:,} €" if p['price'] else 'N/A',
            'location': p['location'],
            'source': p['source'],
            'dpe': p['dpe'] or 'N/A',
            'status': p['status'],
            'url': p['url'],
            'posted_date': p['posted_date']
        }
        properties_list.append(prop_dict)
        
        print(f"\n📄 Propriété ID {prop_dict['id']}:")
        print(f"   Titre: {prop_dict['title'][:50]}...")
        print(f"   📍 Location: {prop_dict['location']}")
        print(f"   📅 Date: {prop_dict['posted_date']}")
        print(f"   💰 Prix: {prop_dict['price']}")
        print(f"   🏷️  DPE: {prop_dict['dpe']}")
    
    # Vérifier que tous ont location et posted_date
    missing_location = [p for p in properties_list if not p['location']]
    missing_date = [p for p in properties_list if not p['posted_date']]
    
    print("\n" + "=" * 80)
    print("📊 RÉSULTAT:")
    print("=" * 80)
    print(f"Total testé: {len(properties_list)}")
    print(f"Sans location: {len(missing_location)}")
    print(f"Sans posted_date: {len(missing_date)}")
    
    if missing_location:
        print("\n❌ ÉCHOUÉ: Des propriétés n'ont pas de location")
        return False
    
    if missing_date:
        print("\n❌ ÉCHOUÉ: Des propriétés n'ont pas de posted_date")
        return False
    
    print("\n✅ SUCCÈS: Toutes les propriétés ont location et posted_date")
    return True


if __name__ == '__main__':
    success = test_properties_route()
    sys.exit(0 if success else 1)
