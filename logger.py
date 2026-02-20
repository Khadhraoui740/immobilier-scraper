"""
Configuration et gestion des logs
"""
import logging
import logging.handlers
from pathlib import Path
from config import LOG_CONFIG

def setup_logging():
    """Configurer le système de logging"""
    log_dir = LOG_CONFIG['log_dir']
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Créer un logger racine
    logger = logging.getLogger()
    logger.setLevel(LOG_CONFIG['log_level'])
    
    # Format des logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )
    
    # Handler fichier avec rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / 'immobilier-scraper.log',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
