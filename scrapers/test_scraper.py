"""
Scraper de test pour démonstration
"""
import logging
from .base_scraper import BaseScraper
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)


class TestScraper(BaseScraper):
    """Scraper de test avec données fictives"""
    
    def __init__(self, config):
        super().__init__('TestScraper', config)
    
    def search(self, budget_min, budget_max, dpe_max, zones):
        """Retourner des données de test"""
        logger.info("Scraper Test: Génération de données de test")
        
        properties = []
        titles = [
            "Appartement 2 pièces avec balcon",
            "Maison indépendante 4 pièces",
            "Studio rénové proche métro",
            "T3 lumineux Ile-de-France",
            "Penthouse moderne avec vue",
            "Duplex contemporain",
            "Loft spacieux Paris",
            "Villa familiale 5 pièces"
        ]
        
        locations = ['Paris 15', 'Boulogne', 'Vanves', 'Neuilly', 'Saint-Denis', 'Levallois']
        dpe_values = ['A', 'B', 'C', 'D', 'E', 'F']
        
        for i in range(12):
            price = random.randint(int(budget_min), int(budget_max))
            surface = random.randint(30, 150)
            
            properties.append({
                'id': f"test-{i}",
                'source': 'TestScraper',
                'title': random.choice(titles),
                'location': random.choice(locations),
                'price': price,
                'surface': surface,
                'rooms': random.randint(1, 5),
                'dpe': random.choice(dpe_values),
                'url': f'https://test.fr/property/{i}',
                'images': [],
                'created_at': (datetime.now() - timedelta(hours=random.randint(0, 24))).isoformat()
            })
        
        logger.info(f"TestScraper: {len(properties)} propriétés générées")
        return properties
    
    def parse_property(self, property_html):
        """Non utilisé pour le scraper de test"""
        return None
