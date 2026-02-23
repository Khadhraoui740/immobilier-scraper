"""
URL Builder pour générer les URLs fonctionnelles vers les sites immobiliers
Crée des URLs de recherche réelles qui fonctionnent
"""
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)


# Mapping des départements vers codes postaux
DEPT_TO_CODE = {
    'Paris': '75',
    'Hauts-de-Seine': '92',
    'Val-de-Marne': '94',
    'Essonne': '91',
    'Seine-et-Marne': '77',
    'Yvelines': '78'
}


class URLBuilder:
    """Builder pour générer les URLs de recherche fonctionnelles"""
    
    @staticmethod
    def seloger_search_url(zone: str = "", price_max: int = 150000) -> str:
        """Générer une URL de recherche SeLoger fonctionnelle
        
        Format:
        - https://www.seloger.com/immobilier/achat/immo-paris-75/
        """
        # Obtenir le code département
        dept_code = DEPT_TO_CODE.get(zone, '75')
        zone_slug = zone.lower().replace(' ', '-').replace('_', '-')
        
        return f"https://www.seloger.com/immobilier/achat/immo-{zone_slug}-{dept_code}/"
    
    @staticmethod
    def pap_search_url(zone: str = "", price_max: int = 150000) -> str:
        """Générer une URL de recherche PAP fonctionnelle
        
        Format:
        - https://www.pap.fr/annonce/vente-appartement-paris-75
        """
        dept_code = DEPT_TO_CODE.get(zone, '75')
        zone_slug = zone.lower().replace(' ', '-').replace('_', '-')
        
        return f"https://www.pap.fr/annonce/vente-appartement-{zone_slug}-{dept_code}"
    
    @staticmethod
    def leboncoin_search_url(zone: str = "", price_max: int = 150000) -> str:
        """Générer une URL de recherche LeBonCoin fonctionnelle
        
        Format:
        - https://www.leboncoin.fr/recherche?category=9&locations=Paris_75000
        """
        dept_code = DEPT_TO_CODE.get(zone, '75')
        zone_param = quote(f"{zone}_{dept_code}000")
        
        return f"https://www.leboncoin.fr/recherche?category=9&locations={zone_param}"
    
    @staticmethod
    def bienici_search_url(zone: str = "", price_max: int = 150000) -> str:
        """Générer une URL de recherche BienIci fonctionnelle
        
        Format:
        - https://www.bienici.com/recherche/achat/paris-75000
        """
        dept_code = DEPT_TO_CODE.get(zone, '75')
        zone_slug = zone.lower().replace(' ', '-').replace('_', '-')
        
        return f"https://www.bienici.com/recherche/achat/{zone_slug}-{dept_code}000"
    
    @staticmethod
    def dvf_transaction_url(zone: str = "") -> str:
        """Générer une URL vers les données DVF
        
        Format:
        - https://app.dvf.etalab.gouv.fr/
        """
        return "https://app.dvf.etalab.gouv.fr/"


# Créer des convertisseurs pour chaque scraper existant
def get_realistic_url(source: str, zone: str = "", price: float = 0) -> str:
    """Obtenir une URL de recherche fonctionnelle pour une source donnée
    
    Cette fonction crée des URLs de recherche qui fonctionnent vraiment
    
    Args:
        source: SeLoger, PAP, LeBonCoin, BienIci, DVF
        zone: Zone/département de la propriété
        price: Prix pour la recherche
        
    Returns:
        URL de recherche fonctionnelle
    """
    price_max = int(price * 1.5) if price else 150000
    
    url_builders = {
        'SeLoger': lambda: URLBuilder.seloger_search_url(zone, price_max),
        'PAP': lambda: URLBuilder.pap_search_url(zone, price_max),
        'LeBonCoin': lambda: URLBuilder.leboncoin_search_url(zone, price_max),
        'BienIci': lambda: URLBuilder.bienici_search_url(zone, price_max),
        'DVF': lambda: URLBuilder.dvf_transaction_url(zone),
    }
    
    builder = url_builders.get(source)
    if builder:
        return builder()
    
    # Fallback
    return f"https://www.{source.lower()}.com"
