"""
Utilitaires et fonctions communes
"""
import logging
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class PropertyUtils:
    """Utilitaires pour les propriétés immobilières"""
    
    @staticmethod
    def calculate_price_per_sqm(price: float, surface: float) -> float:
        """Calculer le prix au m²"""
        if not price or not surface or surface == 0:
            return None
        return price / surface
    
    @staticmethod
    def format_price(price: float) -> str:
        """Formater une prix"""
        if not price:
            return "N/A"
        return f"{price:,.0f} €"
    
    @staticmethod
    def format_surface(surface: float) -> str:
        """Formater une surface"""
        if not surface:
            return "N/A"
        return f"{surface:.0f} m²"
    
    @staticmethod
    def calculate_dpe_rating(price_per_sqm: float) -> str:
        """Suggérer un DPE basé sur le prix/m²"""
        if not price_per_sqm:
            return None
        
        if price_per_sqm < 3000:
            return "G"
        elif price_per_sqm < 4000:
            return "F"
        elif price_per_sqm < 5000:
            return "E"
        elif price_per_sqm < 6000:
            return "D"
        elif price_per_sqm < 7000:
            return "C"
        else:
            return "A"
    
    @staticmethod
    def is_good_deal(price: float, surface: float, zone: str) -> bool:
        """Déterminer si c'est une bonne affaire"""
        if not price or not surface:
            return False
        
        price_per_sqm = price / surface
        
        # Seuils par zone (estimé)
        thresholds = {
            'Paris': 8000,
            'Hauts-de-Seine': 6000,
            'Val-de-Marne': 5000
        }
        
        threshold = thresholds.get(zone, 6000)
        return price_per_sqm < threshold * 0.8  # 20% en dessous du seuil


class DataProcessor:
    """Traitement des données"""
    
    @staticmethod
    def deduplicate_properties(properties: List[Dict]) -> List[Dict]:
        """Supprimer les doublons basés sur l'URL"""
        seen = set()
        deduplicated = []
        
        for prop in properties:
            url = prop.get('url')
            if url and url not in seen:
                seen.add(url)
                deduplicated.append(prop)
        
        return deduplicated
    
    @staticmethod
    def sort_properties(properties: List[Dict], field: str = 'price', 
                       ascending: bool = True) -> List[Dict]:
        """Trier les propriétés"""
        try:
            return sorted(
                properties,
                key=lambda x: x.get(field, 0),
                reverse=not ascending
            )
        except Exception as e:
            logger.error(f"Erreur lors du tri: {e}")
            return properties
    
    @staticmethod
    def filter_properties(properties: List[Dict], **filters) -> List[Dict]:
        """Filtrer les propriétés"""
        filtered = properties
        
        if 'price_min' in filters and filters['price_min']:
            filtered = [p for p in filtered if p.get('price', 0) >= filters['price_min']]
        
        if 'price_max' in filters and filters['price_max']:
            filtered = [p for p in filtered if p.get('price', 0) <= filters['price_max']]
        
        if 'dpe_max' in filters and filters['dpe_max']:
            dpe_values = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}
            max_value = dpe_values.get(filters['dpe_max'], 6)
            filtered = [p for p in filtered 
                       if dpe_values.get(p.get('dpe'), 6) <= max_value]
        
        if 'min_surface' in filters and filters['min_surface']:
            filtered = [p for p in filtered if p.get('surface', 0) >= filters['min_surface']]
        
        if 'location' in filters and filters['location']:
            location = filters['location'].lower()
            filtered = [p for p in filtered 
                       if location in p.get('location', '').lower()]
        
        return filtered
    
    @staticmethod
    def export_to_json(properties: List[Dict], filepath: Path) -> bool:
        """Exporter les propriétés en JSON"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(properties, f, ensure_ascii=False, indent=2, default=str)
            logger.info(f"Propriétés exportées vers {filepath}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'export: {e}")
            return False
    
    @staticmethod
    def export_to_csv(properties: List[Dict], filepath: Path) -> bool:
        """Exporter les propriétés en CSV"""
        import csv
        try:
            if not properties:
                return False
            
            fields = list(properties[0].keys())
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                writer.writerows(properties)
            
            logger.info(f"Propriétés exportées vers {filepath}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'export CSV: {e}")
            return False


class HashUtils:
    """Utilitaires pour le hachage"""
    
    @staticmethod
    def hash_string(s: str) -> str:
        """Hacher une chaîne de caractères"""
        return hashlib.md5(s.encode()).hexdigest()
    
    @staticmethod
    def hash_property(property_data: Dict) -> str:
        """Créer un hash pour une propriété"""
        # Utiliser l'URL comme base
        url = property_data.get('url', '')
        source = property_data.get('source', '')
        return HashUtils.hash_string(f"{source}-{url}")


class DateUtils:
    """Utilitaires pour les dates"""
    
    @staticmethod
    def get_timestamp() -> str:
        """Obtenir un timestamp"""
        return datetime.now().isoformat()
    
    @staticmethod
    def get_formatted_date() -> str:
        """Obtenir une date formatée"""
        return datetime.now().strftime('%d/%m/%Y')
    
    @staticmethod
    def get_formatted_datetime() -> str:
        """Obtenir une date/heure formatée"""
        return datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    @staticmethod
    def hours_since(datetime_str: str) -> float:
        """Calculer les heures écoulées"""
        try:
            dt = datetime.fromisoformat(datetime_str)
            return (datetime.now() - dt).total_seconds() / 3600
        except:
            return None
