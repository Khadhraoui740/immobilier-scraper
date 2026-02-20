#!/usr/bin/env python3
"""
Test de bout en bout - Modification config et validation des résultats
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database import Database
from scrapers.manager import ScraperManager
from logger import setup_logging
from config import SEARCH_CONFIG
import json

logger = setup_logging()

def print_header(text):
    print("\n" + "="*60)
    print(f"🔹 {text}")
    print("="*60)

def test_end_to_end():
    """Test complet de bout en bout"""
    db = Database()
    manager = ScraperManager()
    
    # ÉTAPE 1: Afficher config initiale
    print_header("ÉTAPE 1: Configuration Initiale")
    print(f"Budget: {SEARCH_CONFIG.get('budget_min')}€ - {SEARCH_CONFIG.get('budget_max')}€")
    print(f"DPE Max: {SEARCH_CONFIG.get('dpe_max')}")
    print(f"Zones: {SEARCH_CONFIG.get('zones')}")
    
    # ÉTAPE 2: Vider la BD pour test propre
    print_header("ÉTAPE 2: Nettoyage de la Base de Données")
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM properties')
    old_count = cursor.fetchone()[0]
    print(f"Annonces avant: {old_count}")
    
    cursor.execute('DELETE FROM properties')
    conn.commit()
    cursor.execute('SELECT COUNT(*) FROM properties')
    new_count = cursor.fetchone()[0]
    print(f"Annonces après nettoyage: {new_count}")
    
    # ÉTAPE 3: PREMIÈRE scrape avec config originale
    print_header("ÉTAPE 3: Scraping avec Config Originale")
    print(f"Budget: 200k-500k€")
    results_1 = manager.scrape_all(
        budget_min=200000,
        budget_max=500000,
        dpe_max='D',
        zones=['Paris', 'Hauts-de-Seine', 'Val-de-Marne']
    )
    
    print(f"✅ {len(results_1)} annonces trouvées")
    if results_1:
        print(f"   Prix: {results_1[0].get('price')}€ - {results_1[-1].get('price')}€")
        prix_moyens_1 = [p.get('price') for p in results_1 if p.get('price')]
        if prix_moyens_1:
            avg_1 = sum(prix_moyens_1) / len(prix_moyens_1)
            print(f"   Prix moyen: {avg_1:,.0f}€")
    
    # Sauvegarder en BD
    saved_count_1 = 0
    for prop in results_1:
        try:
            db.add_property(prop)
            saved_count_1 += 1
        except:
            pass
    print(f"   Sauvegardées: {saved_count_1}")
    
    # ÉTAPE 4: Modifier la configuration
    print_header("ÉTAPE 4: Modification de la Configuration")
    print("Nouvelle config: 300k-700k€")
    
    SEARCH_CONFIG['budget_min'] = 300000
    SEARCH_CONFIG['budget_max'] = 700000
    
    # Sauvegarder en fichier aussi
    config_file = Path(__file__).parent / 'data' / 'user_config.json'
    config_file.parent.mkdir(exist_ok=True)
    
    user_config = {
        'budget_min': 300000,
        'budget_max': 700000,
        'dpe_max': 'D',
        'surface_min': 30,
        'zones': ['Paris', 'Hauts-de-Seine', 'Val-de-Marne'],
        'email': 'khadhraoui.jalel@gmail.com',
        'report_time': '09:00',
        'email_notifications': True
    }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(user_config, f, ensure_ascii=False, indent=2)
    print(f"✅ Configuration sauvegardée: {config_file}")
    
    # ÉTAPE 5: DEUXIÈME scrape avec nouvelle config
    print_header("ÉTAPE 5: Scraping avec Nouvelle Configuration")
    print(f"Budget: 300k-700k€")
    results_2 = manager.scrape_all(
        budget_min=300000,
        budget_max=700000,
        dpe_max='D',
        zones=['Paris', 'Hauts-de-Seine', 'Val-de-Marne']
    )
    
    print(f"✅ {len(results_2)} annonces trouvées")
    if results_2:
        print(f"   Prix: {results_2[0].get('price')}€ - {results_2[-1].get('price')}€")
        prix_moyens_2 = [p.get('price') for p in results_2 if p.get('price')]
        if prix_moyens_2:
            avg_2 = sum(prix_moyens_2) / len(prix_moyens_2)
            print(f"   Prix moyen: {avg_2:,.0f}€")
    
    # Sauvegarder en BD
    saved_count_2 = 0
    for prop in results_2:
        try:
            db.add_property(prop)
            saved_count_2 += 1
        except:
            pass
    print(f"   Sauvegardées: {saved_count_2}")
    
    # ÉTAPE 6: Validation des résultats
    print_header("ÉTAPE 6: Validation dans la Base de Données")
    stats = db.get_statistics()
    
    print(f"Total annonces: {stats.get('total_properties', 0)}")
    print(f"Prix moyen: {stats.get('avg_price', 0):,.0f}€")
    print(f"Min: {stats.get('min_price', 0):,.0f}€")
    print(f"Max: {stats.get('max_price', 0):,.0f}€")
    print(f"Par source: {stats.get('by_source', {})}")
    
    # ÉTAPE 7: Résumé comparatif
    print_header("ÉTAPE 7: Résumé Comparatif")
    print(f"Config 1 (200k-500k€): {len(results_1)} annonces")
    print(f"Config 2 (300k-700k€): {len(results_2)} annonces")
    print(f"Différence: {len(results_2) - len(results_1)}")
    print(f"\n✅ Total en BD: {stats.get('total_properties', 0)} annonces")
    
    # ÉTAPE 8: Vérifier les prix
    print_header("ÉTAPE 8: Analyse des Prix")
    props = db.get_properties()
    if props:
        prices = [p['price'] for p in props if p['price']]
        if prices:
            print(f"Prix min trouvé: {min(prices):,.0f}€")
            print(f"Prix max trouvé: {max(prices):,.0f}€")
            print(f"Tous les prix sont entre 200k et 700k: {all(200000 <= p <= 700000 for p in prices)}")

if __name__ == '__main__':
    test_end_to_end()
    print("\n✨ Test terminé!")
