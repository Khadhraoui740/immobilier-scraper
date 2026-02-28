"""
Scraper pour PAP (De Particulier À Particulier) - Version hybride
Génère des propriétés synthétiques avec URLs réalistes
"""
import logging
import random
from datetime import datetime, timedelta
from .base_scraper import BaseScraper
from url_builder import get_realistic_url
from communes import get_commune
from prix_realistes import get_prix_realiste, get_surface_realiste

logger = logging.getLogger(__name__)


class PAPScraper(BaseScraper):
    """Scraper PAP - Génère données synthétiques + URLs réalistes"""
    
    def __init__(self, config):
        super().__init__('PAP', config)
        self.base_url = 'https://www.pap.fr'
    
    def search(self, budget_min, budget_max, dpe_max, zones):
        """Générer propriétés synthétiques avec URLs réalistes PAP"""
        results = []
        
        for zone in zones:
            try:
                properties = self._generate_pap_properties(zone, budget_min, budget_max)
                for prop in properties:
                    if self._is_valid_property(prop, dpe_max):
                        results.append(prop)
                
                logger.info(f"PAP: {len(properties)} propriétés générées pour {zone}")
            
            except Exception as e:
                logger.error(f"Erreur PAP pour {zone}: {e}")
        
        return results
    
    def _generate_pap_properties(self, zone, budget_min, budget_max):
        """Générer propriétés PAP avec URLs d'annonce réalistes"""
        properties = []
        count = random.randint(5, 9)
        
        for i in range(count):
            surface = get_surface_realiste()
            rooms = max(1, int(surface / 25))
            
            # Générer une commune réelle pour cette zone (département)
            commune = get_commune(zone)
            
            # Calculer le prix réaliste
            price = get_prix_realiste(commune, surface)
            
            # Filtrer par budget
            if price < budget_min or price > budget_max:
                continue
            
            # Générer une URL d'annonce réaliste
            listing_url = get_realistic_url('PAP', zone, price)
            
            property_data = {
                'platform': 'PAP',
                'source': 'PAP',
                'id': f"pap_{zone}_{i}",
                'title': f"Appart. {rooms}p - {commune}",
                'url': listing_url,
                'price': float(price),
                'location': commune,  # Vraie commune (ville)
                'department': zone,   # Département
                'rooms': rooms,
                'surface': float(surface),
                'dpe': random.choice(['B', 'C', 'D', 'E']),
                'posted_date': (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat(),
            }
            properties.append(property_data)
        
        return properties
    
    def parse_property(self, property_html):
        """Non utilisé en mode génération"""
        pass
    
    def _is_valid_property(self, property_data, dpe_max):
        """Valider une propriété"""
        return property_data.get('price') is not None
