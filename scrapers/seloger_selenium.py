"""
Scraper SeLoger avec Selenium - Simule un vrai navigateur
"""
import logging
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class SeLogerSeleniumScraper(BaseScraper):
    """Scraper SeLoger utilisant Selenium pour bypasser les blocages"""
    
    def __init__(self, config):
        super().__init__('SeLoger', config)
        self.headless = True  # Mode headless (sans interface)
    
    def _get_driver(self):
        """Créer un driver Chrome avec options pour éviter les blocages"""
        options = Options()
        
        if self.headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # Headers du navigateur
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        options.add_argument('accept-language=fr-FR,fr;q=0.9')
        
        # Éviter les détections de bot
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        return driver
    
    def search(self, budget_min, budget_max, dpe_max, zones):
        """Scraper avec Selenium"""
        logger.info(f"SeLoger Selenium: Recherche {budget_min}-{budget_max} EUR")
        
        properties = []
        driver = None
        
        try:
            driver = self._get_driver()
            
            # URL avec paramètres
            url = f"https://www.seloger.com/acheter/paris_75,hauts-de-seine_92,val-de-marne_94/achat/appartement,maison/?budgetMin={budget_min}&budgetMax={budget_max}"
            
            logger.info(f"Accès à: {url[:80]}...")
            driver.get(url)
            
            # Attendre le chargement initial
            time.sleep(5)
            
            # Scroll plusieurs fois pour charger plus de contenu
            for i in range(3):
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(2)
            
            # Récupérer le HTML
            page_source = driver.page_source
            
            # Parser avec BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Chercher tous les articles (conteneurs d'annonces)
            listings = soup.find_all('article')
            logger.info(f"Trouvé {len(listings)} annonces potentielles")
            
            for listing in listings[:30]:
                try:
                    # Prix
                    price_elem = listing.find('span', class_='price')
                    if not price_elem:
                        price_elem = listing.find(attrs={'data-testid': 'price'})
                    
                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        price = self._extract_price(price_text)
                        
                        if price and budget_min <= price <= budget_max:
                            # Titre
                            title_elem = listing.find('h2') or listing.find('a', class_='title')
                            title = title_elem.get_text(strip=True) if title_elem else "No title"
                            
                            # Location
                            location_elem = listing.find(attrs={'data-testid': 'location'})
                            if not location_elem:
                                location_elem = listing.find(class_='location')
                            location = location_elem.get_text(strip=True) if location_elem else "Non spécifiée"
                            
                            # URL
                            link_elem = listing.find('a')
                            link = link_elem.get('href', url) if link_elem else url
                            if link.startswith('/'):
                                link = 'https://www.seloger.com' + link
                            
                            # Surface
                            surface_str = listing.get_text()
                            surface_match = re.search(r'(\d+)\s*m²', surface_str)
                            surface = int(surface_match.group(1)) if surface_match else 50
                            
                            properties.append({
                                'id': f"seloger-{len(properties)}",
                                'source': 'SeLoger',
                                'title': title[:100],
                                'location': location[:100],
                                'price': price,
                                'surface': surface,
                                'rooms': 2,
                                'dpe': 'D',
                                'url': link,
                                'images': [],
                                'created_at': None
                            })
                            
                            logger.debug(f"Annonce: {title} - {price:,} EUR")
                    
                except Exception as e:
                    logger.debug(f"Erreur extraction: {e}")
                    continue
            
            logger.info(f"SeLoger Selenium: {len(properties)} propriétés extraites")
            
        except Exception as e:
            logger.error(f"Erreur Selenium SeLoger: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
        
        return properties
    
    def _extract_price(self, price_text):
        """Extraire le prix du texte"""
        try:
            # Supprimer les caractères non numériques sauf virgula/point
            price_str = ''.join(c for c in price_text if c.isdigit() or c in '.,')
            # Remplacer virgule par point
            price_str = price_str.replace(',', '.')
            # Prendre la première partie si plusieurs nombres
            price_str = price_str.split('.')[0]
            return int(price_str) if price_str else None
        except:
            return None
    
    def parse_property(self, property_html):
        """Non utilisé pour Selenium"""
        return None
