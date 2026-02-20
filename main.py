"""
Script principal de scraping immobilier
"""
import logging
import sys
from datetime import datetime
from pathlib import Path

# Ajouter le répertoire parent au chemin Python
sys.path.insert(0, str(Path(__file__).parent))

from logger import setup_logging
from database import Database
from scrapers.manager import ScraperManager
from notifier import EmailNotifier
from config import SEARCH_CONFIG

# Configurer les logs
logger = setup_logging()


def main():
    """Fonction principale"""
    logger.info("=" * 80)
    logger.info(f"Démarrage du scraping immobilier - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info("=" * 80)
    
    try:
        # Initialiser la base de données
        logger.info("Initialisation de la base de données...")
        db = Database()
        
        # Initialiser les scrapers
        logger.info("Initialisation des scrapers...")
        manager = ScraperManager()
        
        # Effectuer le scraping
        logger.info(f"Scraping en cours avec les critères:")
        logger.info(f"  - Budget: {SEARCH_CONFIG['budget_min']:,} € - {SEARCH_CONFIG['budget_max']:,} €")
        logger.info(f"  - Zones: {', '.join(SEARCH_CONFIG['zones'])}")
        logger.info(f"  - DPE max: {SEARCH_CONFIG['dpe_max']}")
        
        properties = manager.scrape_all()
        logger.info(f"Total: {len(properties)} propriétés scrapées")
        
        # Ajouter à la base de données
        new_count = 0
        duplicate_count = 0
        
        for prop in properties:
            if db.property_exists(prop.get('url')):
                duplicate_count += 1
                logger.debug(f"Annonce déjà en base: {prop.get('title')}")
            else:
                db.add_property(prop)
                new_count += 1
                logger.debug(f"Annonce ajoutée: {prop.get('title')} - {prop.get('price')} €")
        
        logger.info(f"Résultats:")
        logger.info(f"  - Nouvelles annonces: {new_count}")
        logger.info(f"  - Doublons: {duplicate_count}")
        
        # Envoyer les alertes pour les nouvelles annonces
        if new_count > 0:
            logger.info(f"Envoi des alertes pour {new_count} nouvelles propriétés...")
            notifier = EmailNotifier()
            new_properties = [p for p in properties if not db.property_exists(p.get('url'))]
            
            if notifier.send_alert(new_properties):
                logger.info("Alerte email envoyée avec succès")
            else:
                logger.warning("Erreur lors de l'envoi de l'alerte email")
        else:
            logger.info("Aucune nouvelle annonce à notifier")
        
        # Afficher les statistiques
        stats = db.get_statistics()
        logger.info(f"Statistiques de la base de données:")
        logger.info(f"  - Total propriétés: {stats['total_properties']}")
        logger.info(f"  - Prix moyen: {stats.get('avg_price', 0):,.0f} €")
        logger.info(f"  - Prix min/max: {stats.get('min_price', 0):,} € - {stats.get('max_price', 0):,} €")
        
        logger.info("=" * 80)
        logger.info(f"Scraping complété - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        logger.info("=" * 80)
        
        return 0
    
    except Exception as e:
        logger.error(f"Erreur lors du scraping: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
