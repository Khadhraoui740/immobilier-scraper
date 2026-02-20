"""
Initialiser le package scrapers
"""
from .base_scraper import BaseScraper
from .seloger_scraper import SeLogerScraper
from .pap_scraper import PAPScraper
from .leboncoin_scraper import LeBonCoinScraper
from .manager import ScraperManager

__all__ = [
    'BaseScraper',
    'SeLogerScraper',
    'PAPScraper',
    'LeBonCoinScraper',
    'ScraperManager'
]
