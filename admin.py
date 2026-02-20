"""
Outils d'administration et de maintenance
"""
import os
import logging
import sqlite3
import shutil
from pathlib import Path
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent))

from config import DATABASE_CONFIG
from logger import setup_logging

logger = setup_logging()


class DatabaseMaintenance:
    """Maintenance de la base de données"""
    
    def __init__(self):
        self.db_path = DATABASE_CONFIG['path']
        self.backup_dir = DATABASE_CONFIG['backup_dir']
    
    def backup_database(self, name=None):
        """Créer une sauvegarde de la base de données"""
        try:
            if not self.db_path.exists():
                logger.warning("Base de données non trouvée")
                return False
            
            if not name:
                name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            
            backup_file = self.backup_dir / name
            shutil.copy2(self.db_path, backup_file)
            
            logger.info(f"Sauvegarde créée: {backup_file}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {e}")
            return False
    
    def restore_database(self, backup_file):
        """Restaurer une sauvegarde"""
        try:
            backup_path = Path(backup_file)
            
            if not backup_path.exists():
                logger.error(f"Fichier de sauvegarde non trouvé: {backup_file}")
                return False
            
            # Créer une sauvegarde de la BD actuelle
            self.backup_database("backup_before_restore.db")
            
            # Restaurer
            shutil.copy2(backup_path, self.db_path)
            
            logger.info(f"Base de données restaurée depuis: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la restauration: {e}")
            return False
    
    def optimize_database(self):
        """Optimiser la base de données"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # VACUUM: réorganise la BD et réduit sa taille
            cursor.execute("VACUUM")
            
            # ANALYZE: met à jour les statistiques
            cursor.execute("ANALYZE")
            
            conn.commit()
            conn.close()
            
            logger.info("Base de données optimisée")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'optimisation: {e}")
            return False
    
    def get_database_size(self):
        """Obtenir la taille de la base de données"""
        if not self.db_path.exists():
            return None
        
        size_bytes = self.db_path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        return size_mb
    
    def cleanup_old_backups(self, keep_recent=5):
        """Supprimer les anciennes sauvegardes"""
        try:
            backups = sorted(self.backup_dir.glob('backup_*.db'), 
                           key=lambda p: p.stat().st_mtime, 
                           reverse=True)
            
            deleted = 0
            for backup in backups[keep_recent:]:
                backup.unlink()
                deleted += 1
                logger.info(f"Sauvegarde supprimée: {backup.name}")
            
            logger.info(f"Nettoyage: {deleted} sauvegarde(s) supprimée(s)")
            return deleted
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage: {e}")
            return 0
    
    def get_database_stats(self):
        """Obtenir les statistiques de la base de données"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Nombre de tables
            cursor.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table'"
            )
            table_count = cursor.fetchone()[0]
            
            # Taille
            size_mb = self.get_database_size()
            
            # Date de dernière modification
            mtime = datetime.fromtimestamp(self.db_path.stat().st_mtime)
            
            conn.close()
            
            return {
                'tables': table_count,
                'size_mb': size_mb,
                'last_modified': mtime.strftime('%d/%m/%Y %H:%M:%S')
            }
        except Exception as e:
            logger.error(f"Erreur: {e}")
            return None
    
    def delete_old_records(self, days=90):
        """Supprimer les anciens enregistrements"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Supprimer les propriétés détectées comme inactives depuis X jours
            cursor.execute('''
                DELETE FROM properties 
                WHERE created_at < datetime('now', '-' || ? || ' days')
                AND status IN ('rejeté', 'acheté')
            ''', (days,))
            
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            
            logger.info(f"Suppression: {deleted} ancien(s) enregistrement(s)")
            return deleted
        except Exception as e:
            logger.error(f"Erreur: {e}")
            return 0


class LogMaintenance:
    """Maintenance des logs"""
    
    @staticmethod
    def cleanup_old_logs(max_size_mb=50):
        """Nettoyer les vieux fichiers de log"""
        try:
            from config import LOG_CONFIG
            
            log_dir = LOG_CONFIG['log_dir']
            log_file = log_dir / 'immobilier-scraper.log'
            
            if log_file.exists():
                size_mb = log_file.stat().st_size / (1024 * 1024)
                
                if size_mb > max_size_mb:
                    # Créer une archive
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    archive_name = f"immobilier-scraper_{timestamp}.log.bak"
                    archive_file = log_dir / archive_name
                    
                    shutil.move(str(log_file), str(archive_file))
                    logger.info(f"Fichier log archivé: {archive_name}")
                    
                    return True
        except Exception as e:
            logger.error(f"Erreur nettoyage logs: {e}")
        
        return False


class HealthCheck:
    """Vérification santé du système"""
    
    @staticmethod
    def run_health_check():
        """Exécuter une vérification complète"""
        print("\n🏥 VÉRIFICATION DE SANTÉ DU SYSTÈME")
        print("=" * 60)
        
        checks = {
            '✓': [],
            '⚠': [],
            '❌': []
        }
        
        # Vérifier l'existence de la BD
        db_path = DATABASE_CONFIG['path']
        if db_path.exists():
            checks['✓'].append(f"Base de données existante ({db_path})")
        else:
            checks['⚠'].append("Base de données non trouvée")
        
        # Vérifier l'existence des répertoires
        required_dirs = [
            DATABASE_CONFIG['path'].parent / 'backups',
            Path(__file__).parent / 'logs'
        ]
        
        for dir_path in required_dirs:
            if dir_path.exists():
                checks['✓'].append(f"Répertoire: {dir_path.name}")
            else:
                checks['⚠'].append(f"Répertoire manquant: {dir_path.name}")
        
        # Vérifier la configuration .env
        env_file = Path(__file__).parent / '.env'
        if env_file.exists():
            checks['✓'].append(".env configuré")
            
            # Vérifier EMAIL_PASSWORD
            from dotenv import load_dotenv
            load_dotenv()
            if not os.getenv('EMAIL_PASSWORD'):
                checks['⚠'].append("EMAIL_PASSWORD non défini dans .env")
        else:
            checks['❌'].append(".env non trouvé")
        
        # Afficher les résultats
        for status, items in checks.items():
            if items:
                print(f"\n{status}:")
                for item in items:
                    print(f"  {item}")
        
        print("\n" + "=" * 60)
        
        # Résumé
        if not checks['❌']:
            print("✅ Système en bon état")
            return True
        else:
            print("❌ Problèmes détectés")
            return False


def admin_cli():
    """Interface CLI pour l'administration"""
    if len(sys.argv) < 2:
        print("""
Commandes d'administration:
  backup              Créer une sauvegarde
  restore <fichier>   Restaurer une sauvegarde
  optimize            Optimiser la BD
  cleanup-backups     Nettoyer les anciennes sauvegardes
  cleanup-logs        Nettoyer les logs
  health              Vérification de santé
  help                Afficher cette aide
        """)
        return
    
    command = sys.argv[1]
    maintenance = DatabaseMaintenance()
    
    if command == 'backup':
        if maintenance.backup_database():
            print("✓ Sauvegarde créée")
        else:
            print("❌ Erreur lors de la sauvegarde")
    
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("Usage: restore <fichier>")
        elif maintenance.restore_database(sys.argv[2]):
            print("✓ Sauvegarde restaurée")
        else:
            print("❌ Erreur lors de la restauration")
    
    elif command == 'optimize':
        if maintenance.optimize_database():
            print("✓ Base de données optimisée")
        else:
            print("❌ Erreur lors de l'optimisation")
    
    elif command == 'cleanup-backups':
        count = maintenance.cleanup_old_backups()
        print(f"✓ {count} sauvegarde(s) supprimée(s)")
    
    elif command == 'cleanup-logs':
        if LogMaintenance.cleanup_old_logs():
            print("✓ Logs nettoyés")
        else:
            print("Logs OK")
    
    elif command == 'health':
        HealthCheck.run_health_check()
    
    elif command == 'help':
        print("""
Commandes d'administration:
  backup              Créer une sauvegarde de la BD
  restore <fichier>   Restaurer une sauvegarde
  optimize            Optimiser la BD (VACUUM/ANALYZE)
  cleanup-backups     Supprimer les anciennes sauvegardes
  cleanup-logs        Nettoyer les fichiers logs
  health              Vérification de santé du système
  help                Afficher l'aide
        """)
    
    else:
        print(f"Commande inconnue: {command}")


if __name__ == '__main__':
    admin_cli()
