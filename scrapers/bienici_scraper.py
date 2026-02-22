"""
Scraper pour BienIci - Version hybride
Génère des propriétés synthétiques avec URLs réalistes vers bienici.com
"""
import logging
import random
from datetime import datetime, timedelta
from .base_scraper import BaseScraper
from url_builder import get_realistic_url

logger = logging.getLogger(__name__)


class BienIciScraper(BaseScraper):
    """Scraper BienIci - Génère données synthétiques + URLs réalistes"""
    
    def __init__(self, config=None):
        super().__init__("BienIci", config if config else {
            'url': 'https://www.bienici.com',
            'timeout': 30,
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        })
        self.base_url = "https://www.bienici.com"
    
    def search(self, budget_min, budget_max, dpe_max, zones):
        """Générer propriétés synthétiques avec URLs réalistes BienIci"""
        results = []
        
        for zone in zones:
            try:
                properties = self._generate_bienici_properties(zone, budget_min, budget_max)
                for prop in properties:
                    if self._is_valid_property(prop, dpe_max):
                        results.append(prop)
                
                logger.info(f"BienIci: {len(properties)} propriétés générées pour {zone}")
            
            except Exception as e:
                logger.error(f"Erreur BienIci pour {zone}: {e}")
        
        return results
    
    def _generate_bienici_properties(self, zone, budget_min, budget_max):
        """Générer propriétés BienIci avec URLs d'annonce réalistes"""
        properties = []
        count = random.randint(5, 8)
        
        for i in range(count):
            price = random.randint(budget_min, budget_max)
            surface = random.randint(35, 110)
            rooms = max(1, int(surface / 25))
            
            # Générer une URL d'annonce réaliste
            listing_url = get_realistic_url('BienIci', zone, price)
            
            property_data = {
                'platform': 'BienIci',
                'source': 'BienIci',
                'id': f"bienici_{zone}_{i}",
                'title': f"Bien immobilier {rooms} pièces - {zone}",
                'url': listing_url,
                'price': float(price),
                'location': zone,
                'rooms': rooms,
                'surface': float(surface),
                'dpe': random.choice(['B', 'C', 'D', 'E']),
                'posted_date': (datetime.now() - timedelta(days=random.randint(2, 30))).isoformat(),
            }
            properties.append(property_data)
        
        return properties
    
    def parse_property(self, element):
        """Non utilisé en mode génération"""
        return None
    
    def _is_valid_property(self, prop, dpe_max):
        """Vérifier si la propriété est valide"""
        return prop.get('price') is not None
