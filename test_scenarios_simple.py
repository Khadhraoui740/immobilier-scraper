#!/usr/bin/env python3
"""Test complet - Tous les scenarios"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database import Database
from scrapers.manager import ScraperManager
from logger import setup_logging
from config import SEARCH_CONFIG
import json

logger = setup_logging()

def clean_database():
    """Nettoy la BD"""
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM properties')
    conn.commit()
    conn.close()
    return db

def test_all():
    """Executer tous les tests"""
    print("\n" + "="*70)
    print("TEST COMPLET - TOUS LES SCENARIOS")
    print("="*70)
    
    # SCENARIO 1
    print("\n[S1] Configuration par defaut (200k-500k EUR)")
    print("-"*70)
    clean_database()
    db = Database()
    manager = ScraperManager()
    
    print(f"Budget: {SEARCH_CONFIG.get('budget_min')}-{SEARCH_CONFIG.get('budget_max')} EUR")
    
    results_1 = manager.scrape_all(
        budget_min=SEARCH_CONFIG.get('budget_min'),
        budget_max=SEARCH_CONFIG.get('budget_max'),
        dpe_max=SEARCH_CONFIG.get('dpe_max'),
        zones=SEARCH_CONFIG.get('zones')
    )
    
    print(f"Resultats: {len(results_1)} annonces")
    saved = 0
    for prop in results_1:
        try:
            db.add_property(prop)
            saved += 1
        except:
            pass
    
    print(f"Sauvegardees: {saved}")
    stats_1 = db.get_statistics()
    print(f"Prix moyen: {stats_1.get('avg_price', 0):,.0f} EUR")
    print(f"Total BD: {stats_1.get('total_properties', 0)}")
    
    # SCENARIO 2
    print("\n[S2] Configuration modifiee (300k-700k EUR)")
    print("-"*70)
    clean_database()
    db = Database()
    
    print(f"Avant: 200k-500k EUR")
    SEARCH_CONFIG['budget_min'] = 300000
    SEARCH_CONFIG['budget_max'] = 700000
    print(f"Apres: {SEARCH_CONFIG['budget_min']}-{SEARCH_CONFIG['budget_max']} EUR")
    
    # Sauvegarder config
    config_file = Path(__file__).parent / 'data' / 'user_config.json'
    config_file.parent.mkdir(exist_ok=True)
    with open(config_file, 'w') as f:
        json.dump({
            'budget_min': SEARCH_CONFIG['budget_min'],
            'budget_max': SEARCH_CONFIG['budget_max'],
            'dpe_max': SEARCH_CONFIG.get('dpe_max'),
            'zones': SEARCH_CONFIG.get('zones')
        }, f, indent=2)
    print(f"Config sauvegardee")
    
    results_2 = manager.scrape_all(
        budget_min=SEARCH_CONFIG.get('budget_min'),
        budget_max=SEARCH_CONFIG.get('budget_max'),
        dpe_max=SEARCH_CONFIG.get('dpe_max'),
        zones=SEARCH_CONFIG.get('zones')
    )
    
    print(f"Resultats: {len(results_2)} annonces")
    saved = 0
    for prop in results_2:
        try:
            db.add_property(prop)
            saved += 1
        except:
            pass
    
    print(f"Sauvegardees: {saved}")
    stats_2 = db.get_statistics()
    print(f"Prix moyen: {stats_2.get('avg_price', 0):,.0f} EUR")
    print(f"Total BD: {stats_2.get('total_properties', 0)}")
    
    # SCENARIO 3
    print("\n[S3] Ajout sans suppression (300k-700k EUR)")
    print("-"*70)
    print(f"Avant: {stats_2.get('total_properties', 0)} annonces")
    
    results_3 = manager.scrape_all(
        budget_min=SEARCH_CONFIG.get('budget_min'),
        budget_max=SEARCH_CONFIG.get('budget_max'),
        dpe_max=SEARCH_CONFIG.get('dpe_max'),
        zones=SEARCH_CONFIG.get('zones')
    )
    
    saved = 0
    for prop in results_3:
        if not db.property_exists(prop.get('url')):
            db.add_property(prop)
            saved += 1
    
    print(f"Nouvelles annonces: {saved}")
    stats_3 = db.get_statistics()
    print(f"Apres: {stats_3.get('total_properties', 0)} annonces")
    print(f"Augmentation: +{stats_3.get('total_properties', 0) - stats_2.get('total_properties', 0)}")
    
    # SCENARIO 4
    print("\n[S4] Filtre tres strict (600k-800k EUR)")
    print("-"*70)
    clean_database()
    db = Database()
    
    print(f"Budget: 600k-800k EUR (plage tres haute)")
    
    results_4 = manager.scrape_all(
        budget_min=600000,
        budget_max=800000,
        dpe_max='D',
        zones=['Paris']
    )
    
    print(f"Resultats: {len(results_4)} annonces")
    saved = 0
    for prop in results_4:
        try:
            db.add_property(prop)
            saved += 1
        except:
            pass
    
    print(f"Sauvegardees: {saved}")
    stats_4 = db.get_statistics()
    print(f"Total BD: {stats_4.get('total_properties', 0)}")
    if stats_4.get('total_properties', 0) > 0:
        print(f"Prix moyen: {stats_4.get('avg_price', 0):,.0f} EUR")
    
    # SCENARIO 5
    print("\n[S5] Filtre tres large (50k-2M EUR)")
    print("-"*70)
    clean_database()
    db = Database()
    
    print(f"Budget: 50k-2M EUR (tous les prix)")
    
    results_5 = manager.scrape_all(
        budget_min=50000,
        budget_max=2000000,
        dpe_max='G',
        zones=['Paris', 'Hauts-de-Seine', 'Val-de-Marne', 'Essonne', 'Seine-et-Marne', 'Yvelines']
    )
    
    print(f"Resultats: {len(results_5)} annonces")
    saved = 0
    for prop in results_5:
        try:
            db.add_property(prop)
            saved += 1
        except:
            pass
    
    print(f"Sauvegardees: {saved}")
    stats_5 = db.get_statistics()
    print(f"Total BD: {stats_5.get('total_properties', 0)}")
    if stats_5.get('total_properties', 0) > 0:
        print(f"Prix moyen: {stats_5.get('avg_price', 0):,.0f} EUR")
        props = db.get_properties()
        prices = [p['price'] for p in props if p['price']]
        if prices:
            print(f"Prix min-max: {min(prices):,.0f} - {max(prices):,.0f} EUR")
    
    # RESUME
    print("\n" + "="*70)
    print("RESUME FINAL")
    print("="*70)
    print(f"\n[S1] 200k-500k:  {stats_1.get('total_properties', 0)} annonces, prix moyen {stats_1.get('avg_price', 0):,.0f} EUR")
    print(f"[S2] 300k-700k:  {stats_2.get('total_properties', 0)} annonces, prix moyen {stats_2.get('avg_price', 0):,.0f} EUR")
    print(f"[S3] Ajout mode: avant {stats_2.get('total_properties', 0)} -> apres {stats_3.get('total_properties', 0)}")
    print(f"[S4] 600k-800k:  {stats_4.get('total_properties', 0)} annonces")
    print(f"[S5] 50k-2M:     {stats_5.get('total_properties', 0)} annonces")
    
    print("\n" + "="*70)
    print("TOUS LES TESTS COMPLETES!")
    print("="*70 + "\n")

if __name__ == '__main__':
    test_all()
