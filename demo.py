"""
Démonstration et tests du système
"""
import sys
from pathlib import Path
import logging

# Ajouter le répertoire parent au chemin Python
sys.path.insert(0, str(Path(__file__).parent))

from logger import setup_logging
from database import Database
from scrapers.manager import ScraperManager
from analyzer import PropertyAnalyzer, generate_market_insight
from utils import PropertyUtils, DataProcessor, DateUtils

logger = setup_logging()


def demo_scraping():
    """Démo: Effectuer un scraping simple"""
    print("\n" + "=" * 60)
    print("DÉMO 1: Scraping Simple")
    print("=" * 60)
    
    try:
        manager = ScraperManager()
        
        print("\n🔍 Scraping en cours...")
        properties = manager.scrape_all()
        
        print(f"✓ {len(properties)} propriétés trouvées")
        
        if properties:
            print("\nPremière propriété:")
            prop = properties[0]
            print(f"  Titre: {prop.get('title')}")
            print(f"  Prix: {PropertyUtils.format_price(prop.get('price'))}")
            print(f"  Localisation: {prop.get('location')}")
            print(f"  Surface: {PropertyUtils.format_surface(prop.get('surface'))}")
            print(f"  Source: {prop.get('source')}")
    
    except Exception as e:
        logger.error(f"Erreur lors du scraping: {e}")


def demo_database():
    """Démo: Gestion de la base de données"""
    print("\n" + "=" * 60)
    print("DÉMO 2: Base de Données")
    print("=" * 60)
    
    try:
        db = Database()
        
        # Statistiques
        stats = db.get_statistics()
        print(f"\n📊 Statistiques globales:")
        print(f"  Total propriétés: {stats['total_properties']}")
        print(f"  Prix moyen: {PropertyUtils.format_price(stats.get('avg_price'))}")
        print(f"  Prix min/max: {PropertyUtils.format_price(stats.get('min_price'))} - "
              f"{PropertyUtils.format_price(stats.get('max_price'))}")
        
        # Par source
        if stats.get('by_source'):
            print(f"\n📍 Distribution par source:")
            for source, count in stats['by_source'].items():
                print(f"  {source}: {count}")
        
        # Propriétés récentes
        recent = db.get_new_properties(hours=24)
        if recent:
            print(f"\n🆕 Dernières annonces (24h): {len(recent)}")
    
    except Exception as e:
        logger.error(f"Erreur base de données: {e}")


def demo_analysis():
    """Démo: Analyse des données"""
    print("\n" + "=" * 60)
    print("DÉMO 3: Analyse des Données")
    print("=" * 60)
    
    try:
        analyzer = PropertyAnalyzer()
        
        # Résumé des 24 dernières heures
        summary = analyzer.get_summary_stats(24)
        print(f"\n📈 Résumé des 24 dernières heures:")
        print(f"  Nouvelles annonces: {summary['count']}")
        
        if summary.get('by_source'):
            print(f"  Par source: {summary['by_source']}")
        
        if summary.get('average_price'):
            print(f"  Prix moyen: {PropertyUtils.format_price(summary['average_price'])}")
        
        if summary.get('average_surface'):
            print(f"  Surface moyenne: {PropertyUtils.format_surface(summary['average_surface'])}")
        
        # Insights
        insights = generate_market_insight()
        if insights:
            print(f"\n💡 Insights de marché:")
            for insight in insights:
                print(f"  {insight}")
    
    except Exception as e:
        logger.error(f"Erreur analyse: {e}")


def demo_filtering():
    """Démo: Filtrage des propriétés"""
    print("\n" + "=" * 60)
    print("DÉMO 4: Filtrage et Tri")
    print("=" * 60)
    
    try:
        db = Database()
        
        # Exemple de filtrage
        filters = {
            'price_min': 200000,
            'price_max': 400000,
            'dpe_max': 'D'
        }
        
        properties = db.get_properties(filters)
        
        print(f"\n🔍 Propriétés filtrées (P: 200k-400k, DPE: ≤D)")
        print(f"  Résultats: {len(properties)} propriétés")
        
        if properties:
            # Afficher les 3 meilleures affaires
            valid = [p for p in properties if p.get('price') and p.get('surface')]
            if valid:
                sorted_props = sorted(valid, 
                                     key=lambda p: p.get('price', 0) / p.get('surface', 1))
                print(f"\n💎 Meilleures affaires (prix/m²):")
                for prop in sorted_props[:3]:
                    price_per_sqm = prop.get('price') / prop.get('surface')
                    print(f"  {prop['title'][:50]}")
                    print(f"    Prix: {PropertyUtils.format_price(prop.get('price'))}")
                    print(f"    {PropertyUtils.format_surface(prop.get('surface'))} "
                          f"({price_per_sqm:,.0f} €/m²)")
    
    except Exception as e:
        logger.error(f"Erreur filtrage: {e}")


def demo_export():
    """Démo: Export de données"""
    print("\n" + "=" * 60)
    print("DÉMO 5: Export de Données")
    print("=" * 60)
    
    try:
        db = Database()
        properties = db.get_properties()[:5]  # Limiter à 5 pour la démo
        
        if properties:
            # Export JSON
            export_file = Path(__file__).parent / 'logs' / 'demo_export.json'
            
            # Convertir les Row objects en dictionnaires
            props_list = [dict(p) for p in properties]
            success = DataProcessor.export_to_json(props_list, export_file)
            
            if success:
                print(f"\n✓ Données exportées en JSON: {export_file}")
                print(f"  Nombre de propriétés: {len(props_list)}")
        else:
            print("\nAucune propriété à exporter")
    
    except Exception as e:
        logger.error(f"Erreur export: {e}")


def run_all_demos():
    """Exécuter toutes les démos"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + "DÉMONSTRATION DU SYSTÈME DE SCRAPING IMMOBILIER".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    
    demos = [
        ("Scraping", demo_scraping),
        ("Base de Données", demo_database),
        ("Analyse", demo_analysis),
        ("Filtrage", demo_filtering),
        ("Export", demo_export),
    ]
    
    for name, demo_func in demos:
        try:
            response = input(f"\n▶ Exécuter démo '{name}'? (y/n) > ").lower()
            if response == 'y':
                demo_func()
        except KeyboardInterrupt:
            print("\n❌ Démo interrompue")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Démonstration terminée")
    print("=" * 60)


if __name__ == '__main__':
    try:
        run_all_demos()
    except KeyboardInterrupt:
        print("\n\n❌ Programme interrompu")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erreur: {e}", exc_info=True)
        sys.exit(1)
