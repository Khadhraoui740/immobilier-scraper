"""
DVF Scraper - Utilise les données publiques de DVF
Base de données officielle gratuite du gouvernement français
"""
import logging
import requests
from datetime import datetime, timedelta
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class DVFOpenDataScraper(BaseScraper):
    """Scraper utilisant les données publiques DVF (data.gouv.fr)"""
    
    def __init__(self, config):
        super().__init__('DVF Open Data', config)
        self.base_url = 'https://data.opendatasoft.com/api/v2/catalog/datasets'
        self.dvf_dataset = 'dvf-data/records'
    
    def search(self, budget_min, budget_max, dpe_max, zones):
        """Rechercher les données DVF publiques"""
        results = []
        
        for zone in zones:
            try:
                properties = self._search_dvf_zone(zone, budget_min, budget_max)
                
                for prop in properties:
                    if self._is_valid_property(prop, dpe_max):
                        results.append(prop)
                
                logger.info(f"DVF Open Data: {len(properties)} records found for {zone}")
            
            except Exception as e:
                logger.error(f"Erreur DVF pour {zone}: {e}")
        
        return results
    
    def _search_dvf_zone(self, zone, budget_min, budget_max):
        """Rechercher les transactions DVF pour une zone donnée"""
        properties = []
        
        try:
            # Requête vers l'API OpenData Soft (DVF)
            url = f"https://data.opendatasoft.com/api/v2/catalog/datasets/{self.dvf_dataset}/records"
            
            # Filtres de recherche
            filters = f"valeur_fonciere >= {budget_min} AND valeur_fonciere <= {budget_max} AND commune_name ILIKE '{zone}'"
            
            params = {
                'limit': 100,
                'offset': 0,
                'where': filters,
                'order_by': 'date_mutation desc'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                records = data.get('records', [])
                
                for record in records:
                    prop = self._convert_dvf_record(record, zone, budget_min, budget_max)
                    if prop:
                        properties.append(prop)
            
            else:
                logger.warning(f"DVF API returned {response.status_code}")
        
        except Exception as e:
            logger.error(f"DVF API error: {e}")
        
        return properties
    
    def _convert_dvf_record(self, record, zone, budget_min, budget_max):
        """Convertir un enregistrement DVF en propriété standardisée"""
        try:
            fields = record.get('record', {})
            
            price = float(fields.get('valeur_fonciere', 0))
            if not (budget_min <= price <= budget_max):
                return None
            
            # Extraire les surfaces
            surface = fields.get('surface_terrain', 0) or fields.get('surface_reelle_bati', 0)
            if not surface:
                surface = 70  # Default si pas de surface
            
            surface = float(surface) if surface else 70
            
            # Estimer le nombre de pièces basé sur la surface
            rooms = max(1, int(surface / 25))
            
            property_data = {
                'platform': 'DVF Open Data',
                'source': 'DVF',
                'id': f"dvf_{fields.get('id_mutation', hash(str(fields)))}",
                'title': f"{fields.get('type_local', 'Propriété')} - {zone}",
                'url': f"https://dvf.gouv.fr/transaction/{fields.get('id_mutation', '')}",
                'price': price,
                'location': zone,
                'rooms': rooms,
                'surface': surface,
                'dpe': 'D',  # DVF n'a pas d'info DPE
                'posted_date': fields.get('date_mutation', datetime.now().isoformat()),
                'property_type': fields.get('type_local', 'Unknown'),
                'address': fields.get('adresse_numero', '') + ' ' + fields.get('adresse_nom_voie', ''),
                'description': f"Transaction DVF certifiée\nPrix: {price}EUR\nDate: {fields.get('date_mutation', 'N/A')}"
            }
            
            return property_data
        
        except Exception as e:
            logger.warning(f"Error converting DVF record: {e}")
            return None
    
    def parse_property(self, property_data):
        """Non utilisé"""
        pass
    
    def _is_valid_property(self, property_data, dpe_max):
        """Valider une propriété"""
        return property_data.get('price', 0) > 0 and property_data.get('surface', 0) > 0
