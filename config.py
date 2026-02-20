"""
Configuration centralisée du système de scraping immobilier
"""
import os
from pathlib import Path

# Répertoire de base
BASE_DIR = Path(__file__).parent

# Configuration des critères de recherche
SEARCH_CONFIG = {
    'budget_min': 200000,
    'budget_max': 500000,
    'dpe_max': 'D',  # Maximum D
    'zones': ['Paris', 'Hauts-de-Seine', 'Val-de-Marne'],
    'zones_codes': {
        'Paris': '75',
        'Hauts-de-Seine': '92',
        'Val-de-Marne': '94'
    }
}

# Configuration Email
EMAIL_CONFIG = {
    'email': 'khadhraoui.jalel@gmail.com',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'from_email': 'immobilier-scraper@noreply.com',
    # Remarque: Utiliser une variable d'environnement pour le mot de passe
    # Créer un fichier .env avec EMAIL_PASSWORD=votre_mot_de_passe_app
}

# Configuration Base de Données
DATABASE_CONFIG = {
    'path': BASE_DIR / 'database' / 'immobilier.db',
    'backup_dir': BASE_DIR / 'database' / 'backups'
}

# Configuration des scrapers
SCRAPERS_CONFIG = {
    'seloger': {
        'name': 'SeLoger',
        'url': 'https://www.seloger.com/acheter/',
        'enabled': True,
        'timeout': 30,
        'delay_between_requests': 2,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
    },
    'pap': {
        'name': 'PAP',
        'url': 'https://www.pap.fr/immobilier/annonces/',
        'enabled': True,
        'timeout': 30,
        'delay_between_requests': 2,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.google.com/'
        }
    },
    'leboncoin': {
        'name': 'LeBonCoin',
        'url': 'https://www.leboncoin.fr/immobilier/offres/',
        'enabled': True,
        'timeout': 30,
        'delay_between_requests': 3,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.google.com/'
        }
    },
    'bienici': {
        'name': 'BienIci',
        'url': 'https://www.bienici.com/annonces/achat/',
        'enabled': False,
        'timeout': 30,
        'delay_between_requests': 3,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.google.com/'
        }
    }
}

# Configuration Logging
LOG_CONFIG = {
    'log_dir': BASE_DIR / 'logs',
    'log_level': 'INFO',
    'max_log_size': '10MB'
}

# Configuration Planification
SCHEDULER_CONFIG = {
    'interval_hours': 2,  # Scraper tous les 2 heures
    'max_workers': 3,      # Nombre de workers parallèles
    'retry_failed_after_minutes': 30
}

# Mappings DPE
DPE_MAPPING = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6
}

# Statut des annonces
PROPERTY_STATUS = {
    'AVAILABLE': 'disponible',
    'CONTACTED': 'contacté',
    'VISITED': 'visité',
    'DECLINED': 'rejeté',
    'PURCHASED': 'acheté'
}

# Seuils de notification
NOTIFICATION_CONFIG = {
    'min_new_properties': 1,  # Notifier si au moins 1 nouvelle annonce
    'batch_email': True,       # Envoyer les annonces par lot
    'send_time': '09:00'       # Heure d'envoi quotidienne
}
