"""
Scraper pour SeLoger
"""
import logging
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class SeLogerScraper(BaseScraper):
    """Scraper pour la plateforme SeLoger"""
    
    def __init__(self, config):
        super().__init__('SeLoger', config)
        self.base_url = config['url']
    
    def search(self, budget_min, budget_max, dpe_max, zones):
        """Effectuer une recherche sur SeLoger"""
        results = []
        
        for zone in zones:
            zone_code = self._get_zone_code(zone)
            if not zone_code:
                continue
            
            try:
                # Construire l'URL de recherche
                url = self._build_search_url(zone_code, budget_min, budget_max)
                html = self.fetch_page(url)
                soup = BeautifulSoup(html, 'html.parser')
                
                # Trouver toutes les annonces
                properties = soup.find_all('article', class_='se_listing')
                
                for prop in properties:
                    property_data = self.parse_property(prop)
                    if property_data and self._is_valid_property(property_data, dpe_max):
                        results.append(property_data)
                
                logger.info(f"SeLoger: {len(properties)} annonces trouvées pour {zone}")
            
            except Exception as e:
                logger.error(f"Erreur lors du scraping de SeLoger pour {zone}: {e}")
        
        return results
    
    def parse_property(self, property_html):
        """Parser une annonce SeLoger"""
        try:
            property_data = {
                'source': 'SeLoger',
                'title': '',
                'location': '',
                'price': None,
                'url': '',
                'images': []
            }
            
            # Titre et URL
            title_elem = property_html.find('a', class_='se_listing-title')
            if title_elem:
                property_data['title'] = title_elem.get_text(strip=True)
                property_data['url'] = title_elem.get('href', '')
                property_data['id'] = self.get_property_id(property_data['url'])
            
            # Prix
            price_elem = property_html.find('span', class_='se_listing-price')
            if price_elem:
                property_data['price'] = self.parse_price(price_elem.get_text())
            
            # Localisation
            location_elem = property_html.find('p', class_='se_listing-location')
            if location_elem:
                property_data['location'] = self.normalize_location(
                    location_elem.get_text(strip=True)
                )
            
            # Surface
            surface_elem = property_html.find('span', class_='se_listing-surface')
            if surface_elem:
                property_data['surface'] = self.parse_surface(
                    surface_elem.get_text()
                )
            
            # Chambres
            rooms_elem = property_html.find('span', class_='se_listing-rooms')
            if rooms_elem:
                try:
                    property_data['rooms'] = float(rooms_elem.get_text().split()[0])
                except:
                    pass
            
            # DPE
            dpe_elem = property_html.find('span', class_='se_listing-dpe')
            if dpe_elem:
                property_data['dpe'] = dpe_elem.get_text(strip=True)
            
            # Images
            img_elems = property_html.find_all('img', class_='se_listing-img')
            property_data['images'] = [img.get('src') for img in img_elems if img.get('src')]
            
            return property_data if property_data.get('url') else None
        
        except Exception as e:
            logger.error(f"Erreur lors du parsing de l'annonce SeLoger: {e}")
            return None
    
    def _build_search_url(self, zone_code, budget_min, budget_max):
        """Construire l'URL de recherche"""
        # SeLoger moderne - utiliser l'API ou page directe
        return (f"{self.base_url}?search=true&programs=1&new=0&"
                f"budgetMin={budget_min}&budgetMax={budget_max}&"
                f"qsVersion=1.0&multiline=0&"
                f"places=[\"Ile-de-France\"]")
    
    def _get_zone_code(self, zone):
        """Obtenir le code de zone"""
        zone_codes = {
            'Paris': 'paris_75',
            'Hauts-de-Seine': 'hauts-de-seine_92',
            'Val-de-Marne': 'val-de-marne_94'
        }
        return zone_codes.get(zone)
    
    def _is_valid_property(self, property_data, dpe_max):
        """Valider une annonce"""
        if not property_data.get('price'):
            return False
        
        if property_data.get('dpe') and property_data.get('dpe') > dpe_max:
            return False
        
        return True
