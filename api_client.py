"""
API Client centralisé pour toutes les sources immobilières
Basé sur les APIs officielles + données publiques
"""
import logging
import os
import requests
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class APIClient:
    """Client API centralisé pour scraper via APIs officielles"""
    
    def __init__(self):
        # Charger les clés API depuis les variables d'environnement
        self.seloger_key = os.getenv('SELOGER_API_KEY')
        self.pap_key = os.getenv('PAP_API_KEY')
        self.leboncoin_key = os.getenv('LEBONCOIN_API_KEY')
        self.bienici_key = os.getenv('BIENICI_API_KEY')
        
        # URLs des APIs
        self.apis = {
            'seloger': {
                'url': 'https://api.seloger.com/v2/search',
                'key': self.seloger_key,
                'enabled': bool(self.seloger_key),
                'method': 'GET'
            },
            'pap': {
                'url': 'https://www.pap.fr/api/search',
                'key': self.pap_key,
                'enabled': bool(self.pap_key),
                'method': 'GET'
            },
            'leboncoin': {
                'url': 'https://api.leboncoin.fr/v2/finder/search',
                'key': self.leboncoin_key,
                'enabled': bool(self.leboncoin_key),
                'method': 'POST'
            },
            'bienici': {
                'url': 'https://api.bienici.com/search',
                'key': self.bienici_key,
                'enabled': bool(self.bienici_key),
                'method': 'GET'
            }
        }
    
    def search_seloger(self, budget_min: int, budget_max: int, zones: List[str]) -> List[Dict]:
        """Rechercher sur SeLoger via API"""
        if not self.apis['seloger']['enabled']:
            logger.warning("SeLoger API user credentialsn not configured")
            return []
        
        results = []
        headers = {'Authorization': f'Bearer {self.seloger_key}'}
        
        for zone in zones:
            try:
                params = {
                    'locations': zone,
                    'priceMin': budget_min,
                    'priceMax': budget_max,
                    'sortBy': 'relevance',
                    'pageSize': 50
                }
                
                r = requests.get(
                    self.apis['seloger']['url'],
                    params=params,
                    headers=headers,
                    timeout=10
                )
                
                if r.status_code == 200:
                    data = r.json()
                    properties = data.get('results', [])
                    logger.info(f"SeLoger: Found {len(properties)} properties in {zone}")
                    results.extend(self._normalize_seloger(properties))
                else:
                    logger.warning(f"SeLoger API error: {r.status_code}")
            
            except Exception as e:
                logger.error(f"SeLoger search error: {e}")
        
        return results
    
    def search_leboncoin(self, budget_min: int, budget_max: int, zones: List[str]) -> List[Dict]:
        """Rechercher sur LeBonCoin via API"""
        if not self.apis['leboncoin']['enabled']:
            logger.warning("LeBonCoin API credentials not configured")
            return []
        
        results = []
        headers = {'Authorization': f'Bearer {self.leboncoin_key}'}
        
        for zone in zones:
            try:
                payload = {
                    'search_query': {
                        'enums': {
                            'ad_type': ['offer'],
                            'category': ['real_estate'],
                            'location': [zone]
                        },
                        'filters': {
                            'price': {
                                'min': budget_min,
                                'max': budget_max
                            }
                        },
                        'limit': 50
                    }
                }
                
                r = requests.post(
                    self.apis['leboncoin']['url'],
                    json=payload,
                    headers=headers,
                    timeout=10
                )
                
                if r.status_code == 200:
                    data = r.json()
                    properties = data.get('results', [])
                    logger.info(f"LeBonCoin: Found {len(properties)} properties in {zone}")
                    results.extend(self._normalize_leboncoin(properties))
                else:
                    logger.warning(f"LeBonCoin API error: {r.status_code}")
            
            except Exception as e:
                logger.error(f"LeBonCoin search error: {e}")
        
        return results
    
    def search_pap(self, budget_min: int, budget_max: int, zones: List[str]) -> List[Dict]:
        """Rechercher sur PAP via API"""
        if not self.apis['pap']['enabled']:
            logger.warning("PAP API credentials not configured")
            return []
        
        results = []
        headers = {'Authorization': f'Bearer {self.pap_key}'}
        
        for zone in zones:
            try:
                params = {
                    'location': zone,
                    'priceMin': budget_min,
                    'priceMax': budget_max,
                    'limit': 50
                }
                
                r = requests.get(
                    self.apis['pap']['url'],
                    params=params,
                    headers=headers,
                    timeout=10
                )
                
                if r.status_code == 200:
                    data = r.json()
                    properties = data.get('listings', [])
                    logger.info(f"PAP: Found {len(properties)} properties in {zone}")
                    results.extend(self._normalize_pap(properties))
                else:
                    logger.warning(f"PAP API error: {r.status_code}")
            
            except Exception as e:
                logger.error(f"PAP search error: {e}")
        
        return results
    
    def search_bienici(self, budget_min: int, budget_max: int, zones: List[str]) -> List[Dict]:
        """Rechercher sur BienIci via API"""
        if not self.apis['bienici']['enabled']:
            logger.warning("BienIci API credentials not configured")
            return []
        
        results = []
        headers = {'Authorization': f'Bearer {self.bienici_key}'}
        
        for zone in zones:
            try:
                params = {
                    'location': zone,
                    'priceMin': budget_min,
                    'priceMax': budget_max,
                    'limit': 50
                }
                
                r = requests.get(
                    self.apis['bienici']['url'],
                    params=params,
                    headers=headers,
                    timeout=10
                )
                
                if r.status_code == 200:
                    data = r.json()
                    properties = data.get('results', [])
                    logger.info(f"BienIci: Found {len(properties)} properties in {zone}")
                    results.extend(self._normalize_bienici(properties))
                else:
                    logger.warning(f"BienIci API error: {r.status_code}")
            
            except Exception as e:
                logger.error(f"BienIci search error: {e}")
        
        return results
    
    # Normalization methods to convert API responses to standard format
    def _normalize_seloger(self, properties: List[Dict]) -> List[Dict]:
        """Normaliser les propriétés SeLoger"""
        results = []
        for prop in properties:
            try:
                result = {
                    'platform': 'SeLoger',
                    'source': 'SeLoger',
                    'id': f"seloger_{prop.get('id')}",
                    'title': prop.get('title', ''),
                    'url': prop.get('url', ''),
                    'price': float(prop.get('price', 0)),
                    'location': prop.get('location', ''),
                    'rooms': int(prop.get('rooms', 0)),
                    'surface': float(prop.get('surface', 0)),
                    'dpe': prop.get('dpe', ''),
                    'posted_date': prop.get('date', datetime.now().isoformat()),
                }
                results.append(result)
            except Exception as e:
                logger.warning(f"Error normalizing SeLoger property: {e}")
        return results
    
    def _normalize_leboncoin(self, properties: List[Dict]) -> List[Dict]:
        """Normaliser les propriétés LeBonCoin"""
        results = []
        for prop in properties:
            try:
                result = {
                    'platform': 'LeBonCoin',
                    'source': 'LeBonCoin',
                    'id': f"leboncoin_{prop.get('id')}",
                    'title': prop.get('title', ''),
                    'url': prop.get('url', ''),
                    'price': float(prop.get('price', 0)),
                    'location': prop.get('location', ''),
                    'rooms': int(prop.get('rooms', 0)),
                    'surface': float(prop.get('surface', 0)),
                    'dpe': prop.get('dpe', ''),
                    'posted_date': prop.get('date', datetime.now().isoformat()),
                }
                results.append(result)
            except Exception as e:
                logger.warning(f"Error normalizing LeBonCoin property: {e}")
        return results
    
    def _normalize_pap(self, properties: List[Dict]) -> List[Dict]:
        """Normaliser les propriétés PAP"""
        results = []
        for prop in properties:
            try:
                result = {
                    'platform': 'PAP',
                    'source': 'PAP',
                    'id': f"pap_{prop.get('id')}",
                    'title': prop.get('title', ''),
                    'url': prop.get('url', ''),
                    'price': float(prop.get('price', 0)),
                    'location': prop.get('location', ''),
                    'rooms': int(prop.get('rooms', 0)),
                    'surface': float(prop.get('surface', 0)),
                    'dpe': prop.get('dpe', ''),
                    'posted_date': prop.get('date', datetime.now().isoformat()),
                }
                results.append(result)
            except Exception as e:
                logger.warning(f"Error normalizing PAP property: {e}")
        return results
    
    def _normalize_bienici(self, properties: List[Dict]) -> List[Dict]:
        """Normaliser les propriétés BienIci"""
        results = []
        for prop in properties:
            try:
                result = {
                    'platform': 'BienIci',
                    'source': 'BienIci',
                    'id': f"bienici_{prop.get('id')}",
                    'title': prop.get('title', ''),
                    'url': prop.get('url', ''),
                    'price': float(prop.get('price', 0)),
                    'location': prop.get('location', ''),
                    'rooms': int(prop.get('rooms', 0)),
                    'surface': float(prop.get('surface', 0)),
                    'dpe': prop.get('dpe', ''),
                    'posted_date': prop.get('date', datetime.now().isoformat()),
                }
                results.append(result)
            except Exception as e:
                logger.warning(f"Error normalizing BienIci property: {e}")
        return results
    
    def get_status(self) -> Dict:
        """Retourner le statut des APIs configurées"""
        return {
            'seloger': self.apis['seloger']['enabled'],
            'pap': self.apis['pap']['enabled'],
            'leboncoin': self.apis['leboncoin']['enabled'],
            'bienici': self.apis['bienici']['enabled']
        }
