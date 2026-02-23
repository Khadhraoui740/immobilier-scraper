#!/usr/bin/env python3
"""
Script de scraping rapide pour générer des propriétés avec de vraies communes
"""
import sys
import json
from pathlib import Path
from scrapers.manager import ScraperManager
from database.db import Database
from config import SEARCH_CONFIG

def load_user_config():
    """Charger la configuration utilisateur"""
    config_file = Path(__file__).parent / 'data' / 'user_config.json'
    try:
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            
            # Mettre à jour SEARCH_CONFIG
            if 'budget_min' in user_config:
                SEARCH_CONFIG['budget_min'] = user_config['budget_min']
            if 'budget_max' in user_config:
                SEARCH_CONFIG['budget_max'] = user_config['budget_max']
            if 'dpe_max' in user_config:
                SEARCH_CONFIG['dpe_max'] = user_config['dpe_max']
            if 'zones' in user_config:
                SEARCH_CONFIG['zones'] = user_config['zones']
    except Exception as e:
        print(f"Erreur lors du chargement de la config: {e}")
    
    return SEARCH_CONFIG

def main():
    print("="*80)
    print("SCRAPING AVEC COMMUNES REELLES")
    print("="*80)
    print()
    
    # Charger la config
    config = load_user_config()
    print(f"Budget: {config['budget_min']} - {config['budget_max']} EUR")
    print(f"DPE max: {config['dpe_max']}")
    print(f"Zones: {', '.join(config['zones'])}")
    print()
    
    # Initialiser le manager et la base
    manager = ScraperManager()
    db = Database()
    
    # Lancer la recherche
    print("Lancement du scraping...")
    results = manager.scrape_all(
        budget_min=config['budget_min'],
        budget_max=config['budget_max'],
        dpe_max=config['dpe_max'],
        zones=config['zones']
    )
    
    print(f"\nResultats: {len(results)} proprietes trouvees")
    print()
    
    # Sauvegarder dans la base
    saved = 0
    for prop in results:
        if db.add_property(prop):
            saved += 1
            location = prop.get('location', 'N/A')
            department = prop.get('department', 'N/A')
            price = prop.get('price', 0)
            print(f"  + {prop['source']}: {location} ({department}) - {price:,.0f} EUR")
    
    print()
    print("="*80)
    print(f"TERMINE: {saved}/{len(results)} proprietes sauvegardees")
    print("="*80)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
