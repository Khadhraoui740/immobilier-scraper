"""
Scraper pour LeBonCoin
"""
import logging
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class LeBonCoinScraper(BaseScraper):
    """Scraper pour LeBonCoin"""
    
    def __init__(self, config):
        super().__init__('LeBonCoin', config)
        self.base_url = config['url']
    
    def search(self, budget_min, budget_max, dpe_max, zones):
        """Effectuer une recherche sur LeBonCoin"""
        results = []
        
        try:
            # Construire l'URL de recherche
            url = self._build_search_url(budget_min, budget_max, zones)
            html = self.fetch_page(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            # Trouver toutes les annonces
            properties = soup.find_all('a', class_='_2MWPK')
            
            for prop in properties:
                property_data = self.parse_property(prop)
                if property_data and self._is_valid_property(property_data, budget_min, budget_max):
                    results.append(property_data)
            
            logger.info(f"LeBonCoin: {len(properties)} annonces trouvées")
        
        except Exception as e:
            logger.error(f"Erreur lors du scraping de LeBonCoin: {e}")
        
        return results
    
    def parse_property(self, property_html):
        """Parser une annonce LeBonCoin"""
        try:
            property_data = {
                'source': 'LeBonCoin',
                'title': '',
                'location': '',
                'price': None,
                'url': '',
                'surface': None,
                'rooms': None,
                'images': []
            }
            
            # URL
            url = property_html.get('href', '')
            if url:
                if not url.startswith('http'):
                    url = 'https://www.leboncoin.fr' + url
                property_data['url'] = url
                property_data['id'] = self.get_property_id(url)
            
            # Titre
            title_elem = property_html.find('h3', class_='_3Z9-o')
            if title_elem:
                property_data['title'] = title_elem.get_text(strip=True)
            
            # Localisation
            location_elem = property_html.find('p', class_='_5Fhx7')
            if location_elem:
                property_data['location'] = self.normalize_location(
                    location_elem.get_text(strip=True)
                )
            
            # Prix
            price_elem = property_html.find('p', class_='_2XwNB')
            if price_elem:
                property_data['price'] = self.parse_price(price_elem.get_text())
            
            # Caractéristiques
            features_elem = property_html.find('p', class_='_1GoHT')
            if features_elem:
                features_text = features_elem.get_text()
                # Parser BIEN-description
                if 'm²' in features_text:
                    try:
                        surface_str = features_text.split('m²')[0].split()[-1]
                        property_data['surface'] = self.parse_surface(surface_str + 'm²')
                    except:
                        pass
            
            # Images
            img_elem = property_html.find('img')
            if img_elem and img_elem.get('src'):
                property_data['images'] = [img_elem.get('src')]
            
            return property_data if property_data.get('url') else None
        
        except Exception as e:
            logger.error(f"Erreur lors du parsing de l'annonce LeBonCoin: {e}")
            return None
    
    def _build_search_url(self, budget_min, budget_max, zones):
        """Construire l'URL de recherche pour LeBonCoin"""
        return (f"{self.base_url}immobilier/ventes/"
                f"?rb=&priceMin={budget_min}&priceMax={budget_max}")
    
    def _is_valid_property(self, property_data, budget_min, budget_max):
        """Valider une annonce"""
        price = property_data.get('price')
        if not price:
            return False
        
        return budget_min <= price <= budget_max
