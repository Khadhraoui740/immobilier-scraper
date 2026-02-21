"""
Health check endpoint and utility for monitoring application readiness.
Use this to detect when the app is ready for tests.
"""
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class HealthStatus:
    """Simple health status tracker"""
    
    def __init__(self):
        self.database_ok = False
        self.api_ok = False
        self.scrapers_ok = False
        self.last_check = None
    
    def to_dict(self):
        return {
            'status': 'healthy' if self.is_healthy() else 'unhealthy',
            'database': 'ok' if self.database_ok else 'error',
            'api': 'ok' if self.api_ok else 'error',
            'scrapers': 'ok' if self.scrapers_ok else 'error',
            'timestamp': self.last_check
        }
    
    def is_healthy(self):
        return self.database_ok and self.api_ok


health_status = HealthStatus()


def check_health(db, scraper_manager):
    """Perform health check on application components"""
    try:
        # Check database
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM properties')
            conn.close()
            health_status.database_ok = True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            health_status.database_ok = False
        
        # Check scrapers
        try:
            if scraper_manager and len(scraper_manager.scrapers) > 0:
                health_status.scrapers_ok = True
            else:
                health_status.scrapers_ok = False
        except Exception as e:
            logger.error(f"Scraper health check failed: {e}")
            health_status.scrapers_ok = False
        
        # API is ok if we're running
        health_status.api_ok = True
        health_status.last_check = datetime.now().isoformat()
        
        return health_status.to_dict()
    
    except Exception as e:
        logger.error(f"Health check error: {e}")
        health_status.last_check = datetime.now().isoformat()
        return health_status.to_dict()
