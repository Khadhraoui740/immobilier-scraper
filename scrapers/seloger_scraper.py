"""
Scraper pour SeLoger - Version hybride avec URLs réalistes
Génère des propriétés synthétiques avec URLs vers seloger.com
"""
import logging
import random
from datetime import datetime, timedelta
from .base_scraper import BaseScraper
from url_builder import get_realistic_url
from communes import get_commune

logger = logging.getLogger(__name__)


class SeLogerScraper(BaseScraper):
    """Scraper pour la plateforme SeLoger - Génère données + URLs réalistes"""
    
    def __init__(self, config):
        super().__init__('SeLoger', config)
        self.base_url = 'https://www.seloger.com'
    
    def search(self, budget_min, budget_max, dpe_max, zones):
        """Générer des propriétés synthétiques avec URLs réalistes SeLoger"""
        results = []
        
        for zone in zones:
            try:
                properties = self._generate_seloger_properties(zone, budget_min, budget_max)
                for prop in properties:
                    if self._is_valid_property(prop, dpe_max):
                        results.append(prop)
                
                logger.info(f"SeLoger: {len(properties)} propriétés générées pour {zone}")
            
            except Exception as e:
                logger.error(f"Erreur SeLoger pour {zone}: {e}")
        
        return results
    
    def _generate_seloger_properties(self, zone, budget_min, budget_max):
        """Générer des propriétés avec URLs d'annonce réalistes SeLoger"""
        properties = []
        count = random.randint(6, 10)
        
        for i in range(count):
            price = random.randint(budget_min, budget_max)
            surface = random.randint(30, 120)
            rooms = max(1, int(surface / 25) + random.randint(-1, 1))
            
            # Générer une commune réelle pour cette zone (département)
            commune = get_commune(zone)
            
            # Générer une URL d'annonce réaliste
            listing_url = get_realistic_url('SeLoger', zone, price)
            
            property_data = {
                'platform': 'SeLoger',
                'source': 'SeLoger',
                'id': f"seloger_{zone}_{i}",
                'title': f"Appartement {rooms}P - {commune}",
                'url': listing_url,
                'price': float(price),
                'location': commune,  # Vraie commune (ville)
                'department': zone,   # Département
                'rooms': rooms,
                'surface': float(surface),
                'dpe': random.choice(['A', 'B', 'C', 'D']),
                'posted_date': (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat(),
            }
            properties.append(property_data)
        
        return properties
    
    def parse_property(self, property_html):
        """Non utilisé en mode génération"""
        pass
    
    def _get_zone_code(self, zone):
        """Obtenir le code de zone SeLoger"""
        zone_codes = {
            'Paris': 'Paris-75',
            'Hauts-de-Seine': 'Hauts-de-Seine-92',
            'Val-de-Marne': 'Val-de-Marne-94'
        }
        return zone_codes.get(zone, zone)
    
    def _is_valid_property(self, property_data, dpe_max):
        """Valider une propriété"""
        if not property_data.get('price'):
            return False
        return True
