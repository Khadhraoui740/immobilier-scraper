"""
Module principal du système de scraping immobilier
"""

__version__ = "1.0.0"
__author__ = "Jalel Khadhraoui"
__email__ = "khadhraoui.jalel@gmail.com"

from config import SEARCH_CONFIG, SCRAPERS_CONFIG, DATABASE_CONFIG
from database import Database
from scrapers.manager import ScraperManager
from notifier import EmailNotifier
from analyzer import PropertyAnalyzer

__all__ = [
    'Database',
    'ScraperManager',
    'EmailNotifier',
    'PropertyAnalyzer',
    'SEARCH_CONFIG',
    'SCRAPERS_CONFIG',
    'DATABASE_CONFIG'
]
