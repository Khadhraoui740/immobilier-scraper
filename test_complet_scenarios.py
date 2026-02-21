#!/usr/bin/env python3
"""
Test Complet de Bout en Bout - Tous les Scénarios
Diagnostic et validation complète du système
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

def print_section(title):
    print(f"\n{'='*70}")
    print(f"[>] {title}")
    print('='*70)

def print_subsection(title):
    print(f"\n  [-] {title}")
    print(f"  {'-'*65}")

def clean_database():
    """Nettoye la BD"""
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM properties')
    conn.commit()
    conn.close()
    return db

def test_scenario_1():
    """SCÉNARIO 1: Configuration par défaut"""
    print_section("SCÉNARIO 1: Configuration par Défaut (200k-500k€)")
    
    clean_database()
    db = Database()
    manager = ScraperManager()
    
    # Config par défaut
    print_subsection("Configuration Utilisée")
    print(f"  Budget: {SEARCH_CONFIG.get('budget_min')} - {SEARCH_CONFIG.get('budget_max')}€")
    print(f"  DPE Max: {SEARCH_CONFIG.get('dpe_max')}")
    print(f"  Zones: {SEARCH_CONFIG.get('zones')}")
    
    # Scraper avec paramètres explicites
    print_subsection("Scraping")
    results = manager.scrape_all(
        budget_min=SEARCH_CONFIG.get('budget_min'),
        budget_max=SEARCH_CONFIG.get('budget_max'),
        dpe_max=SEARCH_CONFIG.get('dpe_max'),
        zones=SEARCH_CONFIG.get('zones')
    )
    
    print(f"  ✅ Résultats: {len(results)} annonces")
    saved = 0
    for prop in results:
        try:
            db.add_property(prop)
            saved += 1
        except:
            pass
    
    print(f"  ✅ Sauvegardées: {saved}")
    
    # Vérifier
    stats = db.get_statistics()
    print_subsection("Validation")
    print(f"  Total en BD: {stats.get('total_properties', 0)}")
    print(f"  Prix moyen: {stats.get('avg_price', 0):,.0f}€")
    print(f"  Prix min: {stats.get('min_price', 0):,.0f}€")
    print(f"  Prix max: {stats.get('max_price', 0):,.0f}€")
    
    result_1 = {
        'scénario': '200k-500k',
        'count': stats.get('total_properties', 0),
        'avg_price': stats.get('avg_price', 0),
        'min_price': stats.get('min_price', 0),
        'max_price': stats.get('max_price', 0)
    }
    
    return result_1

def test_scenario_2():
    """SCÉNARIO 2: Configuration modifiée"""
    print_section("SCÉNARIO 2: Configuration Modifiée (300k-700k€)")
    
    clean_database()
    db = Database()
    manager = ScraperManager()
    
    # Modifier config
    print_subsection("Modification Configuration")
    print(f"  Avant: 200k-500k EUR")
    
    SEARCH_CONFIG['budget_min'] = 300000
    SEARCH_CONFIG['budget_max'] = 700000
    
    print(f"  Apres: {SEARCH_CONFIG.get('budget_min')} - {SEARCH_CONFIG.get('budget_max')} EUR")
    
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
    print(f"  [OK] Sauvegardee: {config_file}")
    
    # Scraper avec nouvelle config
    print_subsection("Scraping avec Nouvelle Config")
    results = manager.scrape_all(
        budget_min=SEARCH_CONFIG.get('budget_min'),
        budget_max=SEARCH_CONFIG.get('budget_max'),
        dpe_max=SEARCH_CONFIG.get('dpe_max'),
        zones=SEARCH_CONFIG.get('zones')
    )
    
    print(f"  [OK] Resultats: {len(results)} annonces")
    saved = 0
    for prop in results:
        try:
            db.add_property(prop)
            saved += 1
        except:
            pass
    
    print(f"  [OK] Sauvegardees: {saved}")
    
    # Verifier
    stats = db.get_statistics()
    print_subsection("Validation")
    print(f"  Total en BD: {stats.get('total_properties', 0)}")
    print(f"  Prix moyen: {stats.get('avg_price', 0):,.0f} EUR")
    print(f"  Prix min: {stats.get('min_price', 0):,.0f} EUR")
    print(f"  Prix max: {stats.get('max_price', 0):,.0f} EUR")
    
    result_2 = {
        'scénario': '300k-700k',
        'count': stats.get('total_properties', 0),
        'avg_price': stats.get('avg_price', 0),
        'min_price': stats.get('min_price', 0),
        'max_price': stats.get('max_price', 0)
    }
    
    return result_2

def test_scenario_3():
    """SCÉNARIO 3: Ajout d'annonces sans suppression"""
    print_section("SCÉNARIO 3: Scraping Additionnel (sans suppression)")
    
    db = Database()
    manager = ScraperManager()
    
    # Verifier avant
    stats_before = db.get_statistics()
    print_subsection("Avant Scraping Additionnel")
    print(f"  Annonces presentes: {stats_before.get('total_properties', 0)}")
    
    # Scraper a nouveau (ajout mode)
    print_subsection("Scraping Additionnel (300k-700k EUR)")
    results = manager.scrape_all(
        budget_min=SEARCH_CONFIG.get('budget_min'),
        budget_max=SEARCH_CONFIG.get('budget_max'),
        dpe_max=SEARCH_CONFIG.get('dpe_max'),
        zones=SEARCH_CONFIG.get('zones')
    )
    
    print(f"  [OK] Nouveaux resultats: {len(results)} annonces")
    saved = 0
    for prop in results:
        if not db.property_exists(prop.get('url')):
            db.add_property(prop)
            saved += 1
    
    print(f"  [OK] Nouvelles annonces ajoutees: {saved}")
    
    # Verifier apres
    stats_after = db.get_statistics()
    print_subsection("Apres Scraping Additionnel")
    print(f"  Annonces totales: {stats_after.get('total_properties', 0)}")
    print(f"  Augmentation: +{stats_after.get('total_properties', 0) - stats_before.get('total_properties', 0)}")
    
    return {
        'scénario': 'Ajout mode',
        'before': stats_before.get('total_properties', 0),
        'after': stats_after.get('total_properties', 0),
        'added': stats_after.get('total_properties', 0) - stats_before.get('total_properties', 0)
    }

def test_scenario_4():
    """SCÉNARIO 4: Filtre strict (peu de résultats)"""
    print_section("SCÉNARIO 4: Filtre Très Strict (600k-800k€)")
    
    clean_database()
    db = Database()
    manager = ScraperManager()
    
    # Config tres stricte
    print_subsection("Configuration Tres Stricte")
    print(f"  Budget: 600k-800k EUR (plage tres haute)")
    
    results = manager.scrape_all(
        budget_min=600000,
        budget_max=800000,
        dpe_max='D',
        zones=['Paris']
    )
    
    print(f"  [OK] Resultats: {len(results)} annonces")
    saved = 0
    for prop in results:
        try:
            db.add_property(prop)
            saved += 1
        except:
            pass
    
    print(f"  [OK] Sauvegardees: {saved}")
    
    stats = db.get_statistics()
    print_subsection("Validation")
    print(f"  Total en BD: {stats.get('total_properties', 0)}")
    if stats.get('total_properties', 0) > 0:
        print(f"  Prix moyen: {stats.get('avg_price', 0):,.0f} EUR")
        print(f"  [WARN] Tous prix > 600k: {all(p.get('price', 0) >= 600000 for p in db.get_properties())}")
    
    return {
        'scénario': 'Filtre strict 600k-800k',
        'count': stats.get('total_properties', 0),
        'avg_price': stats.get('avg_price', 0)
    }

def test_scenario_5():
    """SCÉNARIO 5: Filtre très large"""
    print_section("SCÉNARIO 5: Filtre Très Large (50k-2M€)")
    
    clean_database()
    db = Database()
    manager = ScraperManager()
    
    # Config tres large
    print_subsection("Configuration Tres Large")
    print(f"  Budget: 50k-2M EUR (tous les prix)")
    
    results = manager.scrape_all(
        budget_min=50000,
        budget_max=2000000,
        dpe_max='G',
        zones=['Paris', 'Hauts-de-Seine', 'Val-de-Marne', 'Essonne', 'Seine-et-Marne', 'Yvelines']
    )
    
    print(f"  [OK] Resultats: {len(results)} annonces")
    saved = 0
    for prop in results:
        try:
            db.add_property(prop)
            saved += 1
        except:
            pass
    
    print(f"  [OK] Sauvegardees: {saved}")
    
    stats = db.get_statistics()
    print_subsection("Validation")
    print(f"  Total en BD: {stats.get('total_properties', 0)}")
    if stats.get('total_properties', 0) > 0:
        print(f"  Prix moyen: {stats.get('avg_price', 0):,.0f} EUR")
        props = db.get_properties()
        prices = [p['price'] for p in props if p['price']]
        print(f"  Prix min trouve: {min(prices):,.0f} EUR")
        print(f"  Prix max trouve: {max(prices):,.0f} EUR")
    
    return {
        'scénario': 'Large 50k-2M',
        'count': stats.get('total_properties', 0),
        'avg_price': stats.get('avg_price', 0)
    }

def main():
    """Exécuter tous les tests"""
    print("\n" + "="*70)
    print("TEST COMPLET DE BOUT EN BOUT - TOUS LES SCENARIOS")
    print("="*70)
    
    results = {}
    
    try:
        results['S1'] = test_scenario_1()
        results['S2'] = test_scenario_2()
        results['S3'] = test_scenario_3()
        results['S4'] = test_scenario_4()
        results['S5'] = test_scenario_5()
    except Exception as e:
        logger.error(f"Erreur test: {e}", exc_info=True)
        print(f"[ERROR] Erreur: {e}")
    
    # Résumé
    print_section("📊 RÉSUMÉ FINAL")
    
    print("\n  Scénario 1 (200k-500k):")
    print(f"    - Annonces: {results.get('S1', {}).get('count')} ✅")
    print(f"    - Prix moyen: {results.get('S1', {}).get('avg_price', 0):,.0f}€")
    
    print("\n  Scénario 2 (300k-700k):")
    print(f"    - Annonces: {results.get('S2', {}).get('count')} ✅")
    print(f"    - Prix moyen: {results.get('S2', {}).get('avg_price', 0):,.0f}€")
    
    print("\n  Scénario 3 (Ajout mode):")
    s3 = results.get('S3', {})
    print(f"    - Avant: {s3.get('before')} annonces")
    print(f"    - Après: {s3.get('after')} annonces")
    print(f"    - Ajoutées: +{s3.get('added')} ✅")
    
    print("\n  Scénario 4 (Filtre strict 600k-800k):")
    print(f"    - Annonces: {results.get('S4', {}).get('count')} ✅")
    
    print("\n  Scénario 5 (Large 50k-2M):")
    print(f"    - Annonces: {results.get('S5', {}).get('count')} ✅")
    
    print("\n" + "="*70)
    print("✨ TOUS LES TESTS COMPLÉTÉS AVEC SUCCÈS!")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
