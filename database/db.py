"""
Gestion de la base de données SQLite pour les annonces immobilières
"""
import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from config import DATABASE_CONFIG, DPE_MAPPING, PROPERTY_STATUS

logger = logging.getLogger(__name__)


class Database:
    """Classe pour gérer la base de données"""
    
    def __init__(self):
        self.db_path = DATABASE_CONFIG['path']
        self.backup_dir = DATABASE_CONFIG['backup_dir']
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """Obtenir une connexion à la base de données"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            logger.error(f"Erreur de connexion à la base de données: {e}")
            raise
    
    def init_database(self):
        """Initialiser les tables de la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Table des annonces
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS properties (
                    id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    url TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    location TEXT NOT NULL,
                    price REAL NOT NULL,
                    price_per_sqm REAL,
                    surface REAL,
                    rooms REAL,
                    bedrooms REAL,
                    bathrooms REAL,
                    floor TEXT,
                    building_year INTEGER,
                    property_type TEXT,
                    description TEXT,
                    dpe TEXT,
                    dpe_value INTEGER,
                    ges TEXT,
                    ges_value INTEGER,
                    images TEXT,
                    contact_name TEXT,
                    contact_phone TEXT,
                    contact_email TEXT,
                    posted_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'disponible',
                    notes TEXT,
                    is_favorite BOOLEAN DEFAULT 0,
                    viewed BOOLEAN DEFAULT 0
                )
            ''')
            
            # Table d'historique
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS property_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    property_id TEXT NOT NULL,
                    old_price REAL,
                    new_price REAL,
                    status_change TEXT,
                    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (property_id) REFERENCES properties(id)
                )
            ''')
            
            # Table des recherches
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS searches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    criteria TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_executed TIMESTAMP,
                    results_count INTEGER DEFAULT 0
                )
            ''')
            
            # Table des alertes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_email TEXT NOT NULL,
                    search_id INTEGER NOT NULL,
                    property_id TEXT,
                    alert_type TEXT,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_sent BOOLEAN DEFAULT 0,
                    FOREIGN KEY (search_id) REFERENCES searches(id),
                    FOREIGN KEY (property_id) REFERENCES properties(id)
                )
            ''')
            
            # Créer les index
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON properties(source)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON properties(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_price ON properties(price)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_dpe ON properties(dpe)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_location ON properties(location)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON properties(created_at)')
            
            conn.commit()
            logger.info("Base de données initialisée avec succès")
        except sqlite3.Error as e:
            logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def add_property(self, property_data):
        """Ajouter une annonce à la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO properties 
                (id, source, url, title, location, price, price_per_sqm, surface,
                 rooms, bedrooms, bathrooms, floor, building_year, property_type,
                 description, dpe, dpe_value, ges, ges_value, images,
                 contact_name, contact_phone, contact_email, posted_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?)
            ''', (
                property_data.get('id'),
                property_data.get('source'),
                property_data.get('url'),
                property_data.get('title'),
                property_data.get('location'),
                property_data.get('price'),
                property_data.get('price_per_sqm'),
                property_data.get('surface'),
                property_data.get('rooms'),
                property_data.get('bedrooms'),
                property_data.get('bathrooms'),
                property_data.get('floor'),
                property_data.get('building_year'),
                property_data.get('property_type'),
                property_data.get('description'),
                property_data.get('dpe'),
                DPE_MAPPING.get(property_data.get('dpe'), 6),
                property_data.get('ges'),
                property_data.get('ges_value'),
                property_data.get('images'),
                property_data.get('contact_name'),
                property_data.get('contact_phone'),
                property_data.get('contact_email'),
                property_data.get('posted_date')
            ))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Erreur lors de l'ajout de la propriété: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def get_properties(self, filters=None):
        """Récupérer les annonces filtrées"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM properties WHERE 1=1'
        params = []
        
        if filters:
            if filters.get('price_min'):
                query += ' AND price >= ?'
                params.append(filters['price_min'])
            if filters.get('price_max'):
                query += ' AND price <= ?'
                params.append(filters['price_max'])
            if filters.get('dpe_max'):
                dpe_value = DPE_MAPPING[filters['dpe_max']]
                query += ' AND dpe_value <= ?'
                params.append(dpe_value)
            if filters.get('location'):
                query += ' AND location LIKE ?'
                params.append(f"%{filters['location']}%")
            if filters.get('status'):
                query += ' AND status = ?'
                params.append(filters['status'])
        
        query += ' ORDER BY created_at DESC'
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def update_property_status(self, property_id, status, notes=None):
        """Mettre à jour le statut d'une annonce"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE properties 
                SET status = ?, updated_at = CURRENT_TIMESTAMP, notes = ?
                WHERE id = ?
            ''', (status, notes, property_id))
            
            # Enregistrer dans l'historique
            cursor.execute('''
                INSERT INTO property_history (property_id, status_change, changed_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (property_id, status))
            
            conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Erreur lors de la mise à jour du statut: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def mark_as_favorite(self, property_id, is_favorite=True):
        """Marquer une annonce comme favorite"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE properties 
                SET is_favorite = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (is_favorite, property_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Erreur lors de la mise à jour favorite: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_new_properties(self, hours=2):
        """Récupérer les annonces récentes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM properties
            WHERE created_at >= datetime('now', '-' || ? || ' hours')
            ORDER BY created_at DESC
        ''', (hours,))
        
        return cursor.fetchall()
    
    def property_exists(self, url):
        """Vérifier si une annonce existe déjà"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM properties WHERE url = ?', (url,))
        return cursor.fetchone() is not None
    
    def get_statistics(self):
        """Récupérer les statistiques de la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total des annonces
        cursor.execute('SELECT COUNT(*) FROM properties')
        stats['total_properties'] = cursor.fetchone()[0]
        
        # Par source
        cursor.execute('SELECT source, COUNT(*) FROM properties GROUP BY source')
        stats['by_source'] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Par statut
        cursor.execute('SELECT status, COUNT(*) FROM properties GROUP BY status')
        stats['by_status'] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Moyenne des prix
        cursor.execute('SELECT AVG(price) FROM properties')
        stats['avg_price'] = cursor.fetchone()[0]
        
        # Prix min/max
        cursor.execute('SELECT MIN(price), MAX(price) FROM properties')
        min_price, max_price = cursor.fetchone()
        stats['min_price'] = min_price
        stats['max_price'] = max_price
        
        return stats
