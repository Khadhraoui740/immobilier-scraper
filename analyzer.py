"""
Analyse et rapports des propriétés
"""
import logging
from datetime import datetime, timedelta
from pathlib import Path
import json

from database import Database
from utils import PropertyUtils, DataProcessor, DateUtils

logger = logging.getLogger(__name__)


class PropertyAnalyzer:
    """Analyseur de propriétés"""
    
    def __init__(self):
        self.db = Database()
    
    def analyze_property(self, property_data):
        """Analyser une propriété"""
        analysis = {
            'id': property_data.get('id'),
            'title': property_data.get('title'),
            'price': property_data.get('price'),
            'surface': property_data.get('surface'),
            'location': property_data.get('location'),
            'dpe': property_data.get('dpe'),
        }
        
        # Calculer le prix au m²
        if property_data.get('price') and property_data.get('surface'):
            analysis['price_per_sqm'] = PropertyUtils.calculate_price_per_sqm(
                property_data.get('price'),
                property_data.get('surface')
            )
        
        # Déterminer si c'est une bonne affaire
        if analysis.get('price_per_sqm'):
            analysis['is_good_deal'] = PropertyUtils.is_good_deal(
                property_data.get('price'),
                property_data.get('surface'),
                property_data.get('location', 'Paris')
            )
        
        return analysis
    
    def get_summary_stats(self, time_period_hours=24):
        """Obtenir un résumé des statistiques"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Propriétés récentes
        cursor.execute('''
            SELECT * FROM properties
            WHERE created_at >= datetime('now', '-' || ? || ' hours')
            ORDER BY created_at DESC
        ''', (time_period_hours,))
        
        recent_properties = cursor.fetchall()
        
        stats = {
            'period': f'{time_period_hours}h',
            'count': len(recent_properties),
            'by_source': {},
            'average_price': None,
            'price_range': None,
            'average_surface': None,
            'average_rooms': None
        }
        
        if recent_properties:
            # Par source
            from collections import Counter
            sources = Counter(p['source'] for p in recent_properties)
            stats['by_source'] = dict(sources)
            
            # Prix
            prices = [p['price'] for p in recent_properties if p['price']]
            if prices:
                stats['average_price'] = sum(prices) / len(prices)
                stats['price_range'] = (min(prices), max(prices))
            
            # Surface
            surfaces = [p['surface'] for p in recent_properties if p['surface']]
            if surfaces:
                stats['average_surface'] = sum(surfaces) / len(surfaces)
            
            # Pièces
            rooms_list = [p['rooms'] for p in recent_properties if p['rooms']]
            if rooms_list:
                stats['average_rooms'] = sum(rooms_list) / len(rooms_list)
        
        return stats
    
    def get_market_report(self):
        """Générer un rapport de marché complet"""
        db_stats = self.db.get_statistics()
        summary = self.get_summary_stats(24)
        
        report = {
            'generated_at': DateUtils.get_formatted_datetime(),
            'global_statistics': db_stats,
            'last_24h_summary': summary,
            'analysis': {}
        }
        
        # Analyser les tendances
        if db_stats.get('avg_price'):
            report['analysis']['average_price_formatted'] = PropertyUtils.format_price(
                db_stats['avg_price']
            )
        
        if summary.get('count') > 0:
            report['analysis']['new_listings_24h'] = summary['count']
        
        return report
    
    def export_report(self, filepath: Path, report_format='json'):
        """Exporter un rapport"""
        report = self.get_market_report()
        
        try:
            if report_format == 'json':
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(report, f, ensure_ascii=False, indent=2, default=str)
            
            logger.info(f"Rapport exporté vers {filepath}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'export du rapport: {e}")
            return False


class PropertyComparator:
    """Comparateur de propriétés"""
    
    @staticmethod
    def compare_properties(props_list):
        """Comparer plusieurs propriétés"""
        if not props_list:
            return {}
        
        comparison = {
            'count': len(props_list),
            'price': {
                'min': min(p.get('price', float('inf')) for p in props_list),
                'max': max(p.get('price', 0) for p in props_list),
                'avg': sum(p.get('price', 0) for p in props_list) / len(props_list)
            },
            'surface': {
                'min': min(p.get('surface', float('inf')) for p in props_list if p.get('surface')),
                'max': max(p.get('surface', 0) for p in props_list if p.get('surface')),
            },
            'best_value': None,
            'most_expensive': None,
            'largest': None
        }
        
        # Meilleure rapport prix/surface
        valid_props = [p for p in props_list if p.get('price') and p.get('surface')]
        if valid_props:
            best = min(valid_props, 
                      key=lambda p: p.get('price', 0) / p.get('surface', 1))
            comparison['best_value'] = best['id']
        
        # Plus cher
        most_expensive = max(props_list, key=lambda p: p.get('price', 0))
        comparison['most_expensive'] = most_expensive['id']
        
        # Plus grand
        largest = max(props_list, key=lambda p: p.get('surface', 0))
        comparison['largest'] = largest['id']
        
        return comparison


def generate_market_insight():
    """Générer des insights sur le marché"""
    analyzer = PropertyAnalyzer()
    report = analyzer.get_market_report()
    
    insights = []
    
    # Insight 1: Nombre d'annonces
    if report['last_24h_summary'].get('count') > 0:
        insights.append(
            f"🆕 {report['last_24h_summary']['count']} nouvelle(s) annonce(s) "
            f"dans les dernières 24h"
        )
    
    # Insight 2: Prix moyen
    if report['global_statistics'].get('avg_price'):
        avg_price = PropertyUtils.format_price(report['global_statistics']['avg_price'])
        insights.append(f"💰 Prix moyen en base: {avg_price}")
    
    # Insight 3: Tendance par source
    if report['last_24h_summary'].get('by_source'):
        top_source = max(
            report['last_24h_summary']['by_source'].items(),
            key=lambda x: x[1]
        )
        insights.append(
            f"📍 {top_source[0]} en tête avec {top_source[1]} annonces"
        )
    
    return insights
