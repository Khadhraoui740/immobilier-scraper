#!/usr/bin/env python3
"""
Script de scraping complet - Remplit la base de données avec les annonces
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database import Database
from scrapers.manager import ScraperManager
from logger import setup_logging
from datetime import datetime

logger = setup_logging()

def scrape_and_save():
    """Scraper et sauvegarder en base"""
    print("=" * 60)
    print("🚀 SCRAPING EN COURS...")
    print("=" * 60)
    
    db = Database()
    manager = ScraperManager()
    
    # Lancer le scraping avec critères larges
    print("\n📥 Récupération des annonces...")
    results = manager.scrape_all(
        budget_min=100000,
        budget_max=800000,
        dpe_max='G',
        zones=['Paris', 'Hauts-de-Seine', 'Val-de-Marne']
    )
    
    print(f"\n✅ {len(results)} annonces trouvées!")
    
    # Sauvegarder en base de données
    if results:
        print("\n💾 Sauvegarde en base de données...")
        saved_count = 0
        for prop in results:
            try:
                db.add_property(prop)
                saved_count += 1
            except Exception as e:
                logger.debug(f"Propriété déjà existante ou erreur: {e}")
        
        print(f"✅ {saved_count} annonces sauvegardées!")
    
    # Afficher statistiques
    stats = db.get_statistics()
    print("\n" + "=" * 60)
    print("📊 STATISTIQUES")
    print("=" * 60)
    print(f"Total annonces: {stats.get('total_properties', 0)}")
    avg_price = stats.get('avg_price') or 0
    print(f"Prix moyen: {avg_price:,.0f}€")
    print(f"Par source: {stats.get('by_source', {})}")
    print(f"Par statut: {stats.get('by_status', {})}")
    print("=" * 60)
    print("\n✨ Scraping terminé! Les annonces sont maintenant visibles dans l'interface.")

if __name__ == '__main__':
    scrape_and_save()
