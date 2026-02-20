"""
Scraper avec Selenium pour bypasser les protections
"""
import logging
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    logger.warning("Selenium non installé. Pour utiliser les scrapers web, installer: pip install selenium webdriver-manager")
    SELENIUM_AVAILABLE = False


class SeleniumSeLogerScraper(BaseScraper):
    """Scraper SeLoger utilisant Selenium pour contourner les blocages"""
    
    def __init__(self, config):
        super().__init__('SeLoger-Selenium', config)
        self.base_url = config['url']
        self.driver = None
    
    def _init_driver(self):
        """Initialiser le driver Selenium"""
        if not SELENIUM_AVAILABLE:
            logger.error("Selenium n'est pas disponible")
            return False
        
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            return True
        except Exception as e:
            logger.error(f"Erreur initialisation Chrome: {e}")
            return False
    
    def search(self, budget_min, budget_max, dpe_max, zones):
        """Scraper SeLoger avec Selenium"""
        if not self._init_driver():
            return []
        
        results = []
        try:
            # URL complète SeLoger
            url = f"{self.base_url}?budgetMin={budget_min}&budgetMax={budget_max}"
            logger.info(f"Scraping: {url}")
            
            self.driver.get(url)
            # Attendre que les annonces se chargent
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "se_listing"))
            )
            
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Parser les annonces
            properties = soup.find_all('article', class_='se_listing')
            logger.info(f"SeLoger-Selenium: {len(properties)} annonces trouvées")
            
            for prop in properties:
                try:
                    property_data = self.parse_property(prop)
                    if property_data and self._is_valid_property(property_data, dpe_max):
                        results.append(property_data)
                except Exception as e:
                    logger.debug(f"Erreur parsing: {e}")
            
            return results
        
        except Exception as e:
            logger.error(f"Erreur scraping SeLoger: {e}")
            return []
        finally:
            if self.driver:
                self.driver.quit()
    
    def parse_property(self, property_html):
        """Parser une annonce SeLoger"""
        try:
            property_data = {
                'source': 'SeLoger',
                'title': '',
                'location': '',
                'price': None,
                'url': '',
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
            
            # Location
            location_elem = property_html.find('p', class_='se_listing-location')
            if location_elem:
                property_data['location'] = self.normalize_location(
                    location_elem.get_text(strip=True)
                )
            
            return property_data if property_data.get('url') else None
        except Exception as e:
            logger.debug(f"Erreur parsing: {e}")
            return None
    
    def _is_valid_property(self, property_data, dpe_max):
        """Valider une annonce"""
        return bool(property_data.get('price') and property_data.get('url'))
