"""
URL Builder pour générer les URLs d'annonces réalistes
Crée des URLs basées sur les formats des sites immobiliers
"""
import logging

logger = logging.getLogger(__name__)


class URLBuilder:
    """Builder pour générer les URLs d'annonces correctes"""
    
    @staticmethod
    def seloger_listing_url(listing_id: int, zone: str = "") -> str:
        """Générer une URL d'annonce SeLoger avec ID réaliste
        
        Formats:
        - https://www.seloger.com/annonces/achat/appartement/paris-75/xxxxx.htm
        - https://www.seloger.com/annonces/location/maison/boulogne-92/11111.htm
        """
        # Remplacer les espaces par des tirets
        zone_slug = zone.lower().replace(' ', '-').replace('_', '-')
        
        return f"https://www.seloger.com/annonces/achat/appartement/{zone_slug}/{listing_id}.htm"
    
    @staticmethod
    def pap_listing_url(listing_id: int, zone: str = "") -> str:
        """Générer une URL d'annonce PAP avec ID réaliste
        
        Formats:
        - https://www.pap.fr/annonces/achat/appartement/paris-75/11111
        - https://www.pap.fr/annonces/location/maison/boulogne-92-pour-1400-eur-par-mois/22222
        """
        zone_slug = zone.lower().replace(' ', '-').replace('_', '-')
        
        return f"https://www.pap.fr/annonces/achat/appartement/{zone_slug}/{listing_id}"
    
    @staticmethod
    def leboncoin_listing_url(listing_id: int, zone: str = "") -> str:
        """Générer une URL d'annonce LeBonCoin avec ID réaliste
        
        Formats:
        - https://www.leboncoin.fr/immobilier/11111111111.htm
        - https://www.leboncoin.fr/immobilier/achat/appartements/ile-de-france/paris/11111111111.htm
        """
        # LeBonCoin utilise surtout des IDs numériques longs
        return f"https://www.leboncoin.fr/immobilier/{listing_id}.htm"
    
    @staticmethod
    def bienici_listing_url(listing_id: int, zone: str = "") -> str:
        """Générer une URL d'annonce BienIci avec ID réaliste
        
        Formats:
        - https://www.bienici.com/annonce-immobiliere/11111111
        - https://www.bienici.com/annonce-immobiliere/achat-appartement-paris/11111111
        """
        return f"https://www.bienici.com/annonce-immobiliere/{listing_id}"
    
    @staticmethod
    def dvf_transaction_url(transaction_id: str, zone: str = "") -> str:
        """Générer une URL de transaction DVF
        
        Format:
        - https://dvf.gouv.fr/transaction/75/2024/123456/XXXXX
        """
        return f"https://dvf.gouv.fr/transaction/{transaction_id}"
    
    @staticmethod
    def generate_realistic_id(source: str, zone: str = "", price: float = 0) -> str:
        """Générer un ID réaliste basé sur la source
        
        Args:
            source: SeLoger, PAP, LeBonCoin, BienIci, DVF
            zone: Zone de la propriété
            price: Prix pour générer un ID cohérent
            
        Returns:
            ID réaliste pour la plateforme
        """
        import random
        import hashlib
        
        # Générer un hash basé sur zone et prix pour chaque call
        seed = f"{source}-{zone}-{price}-{random.randint(1000, 9999)}"
        hash_obj = hashlib.md5(seed.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        
        if source == 'SeLoger':
            # SeLoger: IDs de 5-7 chiffres
            return str(hash_int % 9900000 + 100000)
        
        elif source == 'PAP':
            # PAP: IDs numériques
            return str(hash_int % 99900000 + 100000)
        
        elif source == 'LeBonCoin':
            # LeBonCoin: IDs très longs (11+ chiffres)
            return str(hash_int % 99999999999 + 10000000000)
        
        elif source == 'BienIci':
            # BienIci: IDs numériques (8+ chiffres)
            return str(hash_int % 990000000 + 10000000)
        
        elif source == 'DVF':
            # DVF: Format de transaction
            dept = zone.split('-')[-1] if '-' in zone else '75'
            year = '2024'
            transaction_num = str(hash_int % 999999).zfill(6)
            return f"{dept}/{year}/{transaction_num}"
        
        else:
            return str(hash_int % 10000000)


# Créer des convertisseurs pour chaque scraper existant
def get_realistic_url(source: str, zone: str = "", price: float = 0) -> str:
    """Obtenir une URL réaliste pour une source donnée
    
    Cette fonction crée des URLs d'annonce au lieu de simples URLs de recherche
    """
    listing_id = URLBuilder.generate_realistic_id(source, zone, price)
    
    url_builders = {
        'SeLoger': lambda id: URLBuilder.seloger_listing_url(id, zone),
        'PAP': lambda id: URLBuilder.pap_listing_url(id, zone),
        'LeBonCoin': lambda id: URLBuilder.leboncoin_listing_url(id, zone),
        'BienIci': lambda id: URLBuilder.bienici_listing_url(id, zone),
        'DVF': lambda id: URLBuilder.dvf_transaction_url(id, zone),
    }
    
    builder = url_builders.get(source)
    if builder:
        return builder(listing_id)
    
    # Fallback
    return f"https://{source.lower()}.com/search"
