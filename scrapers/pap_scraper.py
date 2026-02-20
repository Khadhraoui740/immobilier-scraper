"""
Scraper pour PAP (De Particulier À Particulier)
"""
import logging
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class PAPScraper(BaseScraper):
    """Scraper pour PAP"""
    
    def __init__(self, config):
        super().__init__('PAP', config)
        self.base_url = config['url']
    
    def search(self, budget_min, budget_max, dpe_max, zones):
        """Effectuer une recherche sur PAP"""
        results = []
        
        try:
            # PAP utilise une seule URL pour toutes les zones
            url = self._build_search_url(budget_min, budget_max, zones)
            html = self.fetch_page(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            # Trouver toutes les annonces
            properties = soup.find_all('a', class_='itemAds')
            
            for prop in properties:
                property_data = self.parse_property(prop)
                if property_data and self._is_valid_property(property_data, dpe_max, zones):
                    results.append(property_data)
            
            logger.info(f"PAP: {len(properties)} annonces trouvées")
        
        except Exception as e:
            logger.error(f"Erreur lors du scraping de PAP: {e}")
        
        return results
    
    def parse_property(self, property_html):
        """Parser une annonce PAP"""
        try:
            property_data = {
                'source': 'PAP',
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
            if not url.startswith('http'):
                url = 'https://www.pap.fr' + url
            property_data['url'] = url
            property_data['id'] = self.get_property_id(url)
            
            # Titre et localisation
            title_elem = property_html.find('h2', class_='itemTitle')
            if title_elem:
                property_data['title'] = title_elem.get_text(strip=True)
            
            location_elem = property_html.find('p', class_='itemLocation')
            if location_elem:
                property_data['location'] = self.normalize_location(
                    location_elem.get_text(strip=True)
                )
            
            # Prix
            price_elem = property_html.find('span', class_='itemPrice')
            if price_elem:
                property_data['price'] = self.parse_price(price_elem.get_text())
            
            # Caractéristiques
            features = property_html.find('p', class_='itemFeatures')
            if features:
                features_text = features.get_text()
                # Parser superficie
                if 'm²' in features_text:
                    try:
                        surface_str = features_text.split('m²')[0].split()[-1]
                        property_data['surface'] = self.parse_surface(surface_str + 'm²')
                    except:
                        pass
                # Parser pièces
                if 'pièce' in features_text.lower():
                    try:
                        rooms_str = features_text.split('pièce')[0].split()[-1]
                        property_data['rooms'] = float(rooms_str)
                    except:
                        pass
            
            # Image principale
            img_elem = property_html.find('img', class_='itemImage')
            if img_elem and img_elem.get('src'):
                property_data['images'] = [img_elem.get('src')]
            
            return property_data if property_data.get('url') else None
        
        except Exception as e:
            logger.error(f"Erreur lors du parsing de l'annonce PAP: {e}")
            return None
    
    def _build_search_url(self, budget_min, budget_max, zones):
        """Construire l'URL de recherche pour PAP"""
        zone_params = ','.join(zones)
        return (f"{self.base_url}acheter/bien-immobilier/"
                f"{zone_params}?"
                f"budget_min={budget_min}&budget_max={budget_max}")
    
    def _is_valid_property(self, property_data, dpe_max, zones):
        """Valider une annonce"""
        if not property_data.get('price'):
            return False
        
        # Vérifier que la localisation est dans les zones demandées
        location = property_data.get('location', '').upper()
        if not any(zone.upper() in location for zone in zones):
            return False
        
        return True
