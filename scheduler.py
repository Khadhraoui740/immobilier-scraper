"""
Planificateur de scraping automatisé
"""
import logging
import sys
from pathlib import Path
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

# Ajouter le répertoire parent au chemin Python
sys.path.insert(0, str(Path(__file__).parent))

from logger import setup_logging
from main import main as scrape_main
from config import SCHEDULER_CONFIG, NOTIFICATION_CONFIG
from database import Database
from notifier import EmailNotifier

logger = setup_logging()


class ImmobilierScheduler:
    """Planificateur pour le scraping automatisé"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.db = Database()
        
    def scraping_job(self):
        """Job de scraping"""
        logger.info(f"Job de scraping lancé - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        try:
            scrape_main()
        except Exception as e:
            logger.error(f"Erreur lors du job de scraping: {e}", exc_info=True)
    
    def daily_report_job(self):
        """Job de rapport quotidien"""
        logger.info(f"Job de rapport quotidien lancé - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        try:
            stats = self.db.get_statistics()
            notifier = EmailNotifier()
            
            # Obtenir les propriétés des dernières 24 heures
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM properties
                WHERE created_at >= datetime('now', '-1 day')
                ORDER BY created_at DESC
            ''')
            recent_properties = cursor.fetchall()
            
            notifier.send_daily_report(stats, recent_properties)
            logger.info("Rapport quotidien envoyé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du job de rapport: {e}", exc_info=True)
    
    def add_jobs(self):
        """Ajouter les jobs au planificateur"""
        # Job de scraping à intervalle régulier
        interval_hours = SCHEDULER_CONFIG['interval_hours']
        self.scheduler.add_job(
            self.scraping_job,
            IntervalTrigger(hours=interval_hours),
            id='immobilier_scraping',
            name=f'Scraping immobilier (toutes les {interval_hours} heures)',
            replace_existing=True
        )
        logger.info(f"Job scraping ajouté - intervalle: {interval_hours}h")
        
        # Job de rapport quotidien à 9h00
        send_time = NOTIFICATION_CONFIG['send_time']
        hour, minute = map(int, send_time.split(':'))
        self.scheduler.add_job(
            self.daily_report_job,
            CronTrigger(hour=hour, minute=minute),
            id='immobilier_daily_report',
            name=f'Rapport quotidien à {send_time}',
            replace_existing=True
        )
        logger.info(f"Job rapport quotidien ajouté - heure: {send_time}")
    
    def start(self):
        """Démarrer le planificateur"""
        self.add_jobs()
        self.scheduler.start()
        logger.info("Planificateur démarré")
        logger.info(f"Jobs actifs: {len(self.scheduler.get_jobs())}")
        
        try:
            # Garder le planificateur actif
            self.scheduler.start()
        except KeyboardInterrupt:
            logger.info("Arrêt du planificateur...")
            self.scheduler.shutdown()
            logger.info("Planificateur arrêté")


def main():
    """Fonction principale"""
    logger.info("=" * 80)
    logger.info(f"Démarrage du planificateur immobilier - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info("=" * 80)
    
    scheduler = ImmobilierScheduler()
    scheduler.start()


if __name__ == '__main__':
    main()
