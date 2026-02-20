"""
Gestionnaire de scrapers
"""
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import SCRAPERS_CONFIG, SEARCH_CONFIG
from .seloger_scraper import SeLogerScraper
from .pap_scraper import PAPScraper
from .leboncoin_scraper import LeBonCoinScraper
from .bienici_scraper import BienIciScraper
from .test_scraper import TestScraper

logger = logging.getLogger(__name__)


class ScraperManager:
    """Gestionnaire pour tous les scrapers"""
    
    def __init__(self):
        self.scrapers = {}
        self._init_scrapers()
    
    def _init_scrapers(self):
        """Initialiser les scrapers"""
        if SCRAPERS_CONFIG['seloger']['enabled']:
            self.scrapers['seloger'] = SeLogerScraper(SCRAPERS_CONFIG['seloger'])
        
        if SCRAPERS_CONFIG['pap']['enabled']:
            self.scrapers['pap'] = PAPScraper(SCRAPERS_CONFIG['pap'])
        
        if SCRAPERS_CONFIG['leboncoin']['enabled']:
            self.scrapers['leboncoin'] = LeBonCoinScraper(SCRAPERS_CONFIG['leboncoin'])
        
        if SCRAPERS_CONFIG.get('bienici', {}).get('enabled', False):
            self.scrapers['bienici'] = BienIciScraper(SCRAPERS_CONFIG['bienici'])
        
        # Ajouter le scraper de test pour la démo
        self.scrapers['test'] = TestScraper({'name': 'Test', 'timeout': 5})
    
    def scrape_all(self, budget_min=None, budget_max=None, dpe_max=None, zones=None):
        """Scraper toutes les plateformes en parallèle"""
        budget_min = budget_min or SEARCH_CONFIG['budget_min']
        budget_max = budget_max or SEARCH_CONFIG['budget_max']
        dpe_max = dpe_max or SEARCH_CONFIG['dpe_max']
        zones = zones or SEARCH_CONFIG['zones']
        
        all_results = []
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {}
            
            for name, scraper in self.scrapers.items():
                future = executor.submit(
                    scraper.search,
                    budget_min, budget_max, dpe_max, zones
                )
                futures[future] = name
            
            for future in as_completed(futures):
                scraper_name = futures[future]
                try:
                    results = future.result()
                    all_results.extend(results)
                    logger.info(f"{scraper_name}: {len(results)} propriétés scrapées")
                except Exception as e:
                    logger.error(f"Erreur lors du scraping de {scraper_name}: {e}")
        
        return all_results
    
    def scrape_single(self, scraper_name, budget_min=None, budget_max=None, 
                     dpe_max=None, zones=None):
        """Scraper une seule plateforme"""
        budget_min = budget_min or SEARCH_CONFIG['budget_min']
        budget_max = budget_max or SEARCH_CONFIG['budget_max']
        dpe_max = dpe_max or SEARCH_CONFIG['dpe_max']
        zones = zones or SEARCH_CONFIG['zones']
        
        scraper = self.scrapers.get(scraper_name)
        if not scraper:
            logger.error(f"Scraper {scraper_name} non trouvé")
            return []
        
        try:
            return scraper.search(budget_min, budget_max, dpe_max, zones)
        except Exception as e:
            logger.error(f"Erreur lors du scraping de {scraper_name}: {e}")
            return []
