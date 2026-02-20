"""
Scraper de base abstraite pour les différentes plateformes
"""
import logging
from abc import ABC, abstractmethod
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from retrying import retry

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Classe de base abstraite pour les scrapers"""
    
    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(config.get('headers', {}))
    
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def fetch_page(self, url, params=None):
        """Récupérer le contenu d'une page avec retry"""
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.config.get('timeout', 30)
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la récupération de {url}: {e}")
            raise
    
    @abstractmethod
    def search(self, budget_min, budget_max, dpe_max, zones):
        """Effectuer une recherche - à implémenter dans les sous-classes"""
        pass
    
    @abstractmethod
    def parse_property(self, property_html):
        """Parser une annonce - à implémenter dans les sous-classes"""
        pass
    
    def parse_price(self, price_str):
        """Parser un prix depuis une chaîne de caractères"""
        if not price_str:
            return None
        try:
            return float(price_str.replace('€', '').replace(' ', '').split(',')[0])
        except (ValueError, AttributeError):
            return None
    
    def parse_surface(self, surface_str):
        """Parser une surface depuis une chaîne de caractères"""
        if not surface_str:
            return None
        try:
            return float(surface_str.replace('m²', '').replace(' ', '').replace(',', '.'))
        except (ValueError, AttributeError):
            return None
    
    def normalize_location(self, location):
        """Normaliser une localisation"""
        return location.strip().title()
    
    def get_property_id(self, url):
        """Générer un ID unique pour une propriété"""
        import hashlib
        return hashlib.md5(f"{self.name}-{url}".encode()).hexdigest()
