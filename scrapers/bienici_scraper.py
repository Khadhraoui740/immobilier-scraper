"""
Scraper pour BienIci
"""

import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime
import re

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class BienIciScraper(BaseScraper):
    """Scraper pour le site BienIci"""
    
    def __init__(self, config=None):
        super().__init__("BienIci", config if config else {
            'url': 'https://www.bienici.com',
            'timeout': 30,
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        })
        self.base_url = "https://www.bienici.com"
    
    def search(self, budget_min, budget_max, dpe_max, zones):
        """Effectuer une recherche sur BienIci"""
        results = []
        
        for zone in zones:
            try:
                # URL de recherche simplifiée
                url = self._build_search_url(zone, budget_min, budget_max, dpe_max)
                html = self.fetch_page(url)
                
                if not html:
                    continue
                
                soup = BeautifulSoup(html, 'html.parser')
                
                # Chercher les annonces (sélecteur générique)
                properties = soup.find_all('div', class_=re.compile(r'annonce|ad|card', re.I))
                
                for prop in properties[:20]:  # Limiter à 20 par zone
                    property_data = self.parse_property(prop)
                    if property_data and self._is_valid_property(property_data, dpe_max):
                        results.append(property_data)
                
            except Exception as e:
                logger.warning(f"Erreur lors du scraping BienIci pour {zone}: {e}")
                continue
        
        return results
    
    def parse_property(self, element):
        """Parser une annonce BienIci"""
        try:
            # Extraction simplifiée
            title_elem = element.find(['h2', 'h3', 'a'])
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # URL
            url_elem = element.find('a', href=True)
            url = url_elem['href'] if url_elem else ""
            if url and not url.startswith('http'):
                url = self.base_url + url
            
            # Prix
            price = None
            price_text = element.get_text()
            price_match = re.search(r'(\d+(?:\s\d{3})*)\s*€', price_text)
            if price_match:
                price = int(price_match.group(1).replace(' ', ''))
            
            # Surface
            surface = None
            surface_match = re.search(r'(\d+)\s*m[²2]', price_text)
            if surface_match:
                surface = int(surface_match.group(1))
            
            # DPE
            dpe = self._extract_dpe_from_text(price_text)
            
            if not price:
                return None
            
            return {
                'title': title,
                'url': url,
                'price': price,
                'surface': surface,
                'dpe': dpe,
                'source': 'BienIci',
                'description': title,
                'scrape_date': datetime.now().isoformat(),
                'status': 'disponible'
            }
        
        except Exception as e:
            logger.debug(f"Erreur extraction propriété: {e}")
            return None
    
    def _build_search_url(self, zone, budget_min, budget_max, dpe_max):
        """Construire l'URL de recherche"""
        # URL simplifiée - peut être améliorée
        return f"{self.base_url}/annonces/achat/?loc={zone}&prixMax={budget_max}"
    
    def _extract_dpe_from_text(self, text):
        """Extraire le DPE du texte"""
        match = re.search(r'[A-G]', text)
        return match.group() if match else "N/A"
    
    def _is_valid_property(self, prop, dpe_max):
        """Vérifier si la propriété est valide"""
        if not prop.get('price'):
            return False
        
        dpe = prop.get('dpe', 'G')
        if dpe != "N/A":
            dpe_order = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
            if dpe_order.get(dpe.upper(), 7) > dpe_order.get(dpe_max.upper(), 4):
                return False
        
        return True
