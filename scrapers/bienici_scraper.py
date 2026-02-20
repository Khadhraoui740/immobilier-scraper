"""
Scraper pour BienIci
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import cloudscraper
import re

from .base_scraper import BaseScraper


class BienIciScraper(BaseScraper):
    """Scraper pour le site BienIci"""
    
    def __init__(self, config=None):
        super().__init__("BienIci", config)
        self.base_url = "https://www.bienici.com"
        self.scraper = cloudscraper.create_scraper()
    
    def build_url(self, filters):
        """Construit l'URL de recherche avec les filtres"""
        url_params = []
        
        # Prix
        if filters.get('price_max'):
            url_params.append(f"prixMax={filters['price_max']}")
        
        # Surface
        if filters.get('surface_min'):
            url_params.append(f"surfaceMin={filters['surface_min']}")
        
        # Localisation
        if filters.get('location'):
            # BienIci prend des codes postaux
            location = filters['location'].replace(' ', '%20')
            url_params.append(f"loc={location}")
        
        # DPE
        if filters.get('dpe_max'):
            dpe_codes = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5', 'F': '6', 'G': '7'}
            dpe_code = dpe_codes.get(filters['dpe_max'].upper(), '4')
            url_params.append(f"dpeMax={dpe_code}")
        
        # Type de bien
        url_params.append("type=1")  # 1 = Maisons et appartements
        url_params.append("tri=0")   # Tri par défaut
        
        url = f"{self.base_url}/annonces/achat/?" + "&".join(url_params)
        return url
    
    def scrape(self, filters):
        """Scrape les annonces BienIci"""
        try:
            url = self.build_url(filters)
            self.logger.info(f"Scraping BienIci: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = self.scraper.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            return self._parse_html(response.text, filters)
        
        except Exception as e:
            self.logger.error(f"Erreur scraping BienIci: {str(e)}")
            return []
    
    def _parse_html(self, html, filters):
        """Parse le HTML BienIci"""
        properties = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Trouver les cartes d'annonces
            cards = soup.find_all('div', class_=re.compile(r'annonce-card|ad-card|announce'))
            
            if not cards:
                # Fallback: chercher par d'autres sélecteurs
                cards = soup.find_all('a', {'href': re.compile(r'/annonces/achat/')})
            
            for card in cards:
                try:
                    prop = self._extract_property(card, filters)
                    if prop:
                        properties.append(prop)
                
                except Exception as e:
                    self.logger.debug(f"Erreur extraction propriété: {str(e)}")
                    continue
            
            self.logger.info(f"BienIci: {len(properties)} propriétés trouvées")
            return properties
        
        except Exception as e:
            self.logger.error(f"Erreur parse HTML: {str(e)}")
            return []
    
    def _extract_property(self, element, filters):
        """Extrait les infos d'une propriété"""
        try:
            # Titre/URL
            title_elem = element.find('h2') or element.find('span', class_=re.compile(r'title'))
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # URL
            url_elem = element.find('a', href=True)
            if url_elem:
                url = url_elem['href']
                if not url.startswith('http'):
                    url = self.base_url + url
            else:
                url = ""
            
            # Prix
            price_elem = element.find(class_=re.compile(r'price|prix'))
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price = int(re.search(r'\d+', price_text.replace(' ', '')).group())
            else:
                price = None
            
            # Surface
            surface_elem = element.find(class_=re.compile(r'surface|area'))
            if surface_elem:
                surface_text = surface_elem.get_text(strip=True)
                surface = int(re.search(r'\d+', surface_text).group())
            else:
                surface = None
            
            # Pièces/chambres
            rooms = None
            pieces_elem = element.find(class_=re.compile(r'rooms|pieces|chambres'))
            if pieces_elem:
                pieces_text = pieces_elem.get_text(strip=True)
                rooms = int(re.search(r'\d+', pieces_text).group())
            
            # DPE
            dpe = self._extract_dpe(element)
            
            # Filtrer par critères
            if not self._apply_filters(price, surface, dpe, filters):
                return None
            
            # Créer l'objet propriété
            property_data = {
                'title': title,
                'url': url,
                'price': price,
                'surface': surface,
                'rooms': rooms,
                'dpe': dpe,
                'source': 'BienIci',
                'image_url': self._extract_image(element),
                'description': self._extract_description(element),
                'location': filters.get('location', ''),
                'scrape_date': datetime.now().isoformat(),
                'available': True,
                'status': 'disponible'
            }
            
            return property_data
        
        except Exception as e:
            self.logger.debug(f"Erreur extraction propriété: {str(e)}")
            return None
    
    def _extract_dpe(self, element):
        """Extrait le DPE"""
        dpe_elem = element.find(class_=re.compile(r'dpe|energy'))
        if dpe_elem:
            dpe_text = dpe_elem.get_text(strip=True)
            match = re.search(r'[A-G]', dpe_text)
            if match:
                return match.group()
        return "N/A"
    
    def _extract_image(self, element):
        """Extrait l'URL de l'image"""
        img_elem = element.find('img')
        if img_elem:
            return img_elem.get('src', '')
        return ""
    
    def _extract_description(self, element):
        """Extrait la description"""
        desc_elem = element.find(class_=re.compile(r'description|desc'))
        if desc_elem:
            return desc_elem.get_text(strip=True)[:250]
        return ""
    
    def _apply_filters(self, price, surface, dpe, filters):
        """Applique les filtres"""
        if price:
            if filters.get('price_max') and price > filters['price_max']:
                return False
            if filters.get('price_min') and price < filters['price_min']:
                return False
        
        if dpe and dpe != "N/A":
            dpe_max = filters.get('dpe_max', 'G')
            dpe_order = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
            if dpe_order.get(dpe, 7) > dpe_order.get(dpe_max.upper(), 4):
                return False
        
        return True
