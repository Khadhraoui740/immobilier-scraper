"""
Scraper pour LeBonCoin - Version hybride
Génère des propriétés synthétiques avec URLs réalistes vers leboncoin.fr
"""
import logging
import random
from datetime import datetime, timedelta
from .base_scraper import BaseScraper
from url_builder import get_realistic_url

logger = logging.getLogger(__name__)


class LeBonCoinScraper(BaseScraper):
    """Scraper LeBonCoin - Génère données synthétiques + URLs réalistes"""
    
    def __init__(self, config):
        super().__init__('LeBonCoin', config)
        self.base_url = 'https://www.leboncoin.fr'
    
    def search(self, budget_min, budget_max, dpe_max, zones):
        """Générer propriétés synthétiques avec URLs réalistes LeBonCoin"""
        results = []
        
        for zone in zones:
            try:
                properties = self._generate_leboncoin_properties(zone, budget_min, budget_max)
                for prop in properties:
                    if self._is_valid_property(prop, dpe_max):
                        results.append(prop)
                
                logger.info(f"LeBonCoin: {len(properties)} propriétés générées pour {zone}")
            
            except Exception as e:
                logger.error(f"Erreur LeBonCoin pour {zone}: {e}")
        
        return results
    
    def _generate_leboncoin_properties(self, zone, budget_min, budget_max):
        """Générer propriétés LeBonCoin avec URLs d'annonce réalistes"""
        properties = []
        count = random.randint(6, 10)
        
        for i in range(count):
            price = random.randint(budget_min, budget_max)
            surface = random.randint(35, 110)
            rooms = max(1, int(surface / 25))
            
            # Générer une URL d'annonce réaliste
            listing_url = get_realistic_url('LeBonCoin', zone, price)
            
            property_data = {
                'platform': 'LeBonCoin',
                'source': 'LeBonCoin',
                'id': f"lbc_{zone}_{i}",
                'title': f"Appartement {rooms} pièces - {zone}",
                'url': listing_url,
                'price': float(price),
                'location': zone,
                'rooms': rooms,
                'surface': float(surface),
                'dpe': random.choice(['B', 'C', 'D', 'E']),
                'posted_date': (datetime.now() - timedelta(days=random.randint(2, 35))).isoformat(),
            }
            properties.append(property_data)
        
        return properties
    
    def parse_property(self, property_html):
        """Non utilisé en mode génération"""
        pass
    
    def _is_valid_property(self, property_data, dpe_max):
        """Valider une propriété"""
        return property_data.get('price') is not None
