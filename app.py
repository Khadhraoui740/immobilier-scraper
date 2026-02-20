"""
Interface Web d'Administration pour le Scraping Immobilier
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import sys
from pathlib import Path
import os

# Ajouter le répertoire parent au chemin
sys.path.insert(0, str(Path(__file__).parent))

from logger import setup_logging
from database import Database
from scrapers.manager import ScraperManager
from analyzer import PropertyAnalyzer
from config import SEARCH_CONFIG, SCRAPERS_CONFIG
from datetime import datetime
import json

logger = setup_logging()

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

# Initialiser
db = Database()
scraper_manager = ScraperManager()
analyzer = PropertyAnalyzer()


# ============================================================================
# ROUTES - PAGES PRINCIPALES
# ============================================================================

@app.route('/')
def dashboard():
    """Page d'accueil - Dashboard"""
    try:
        stats = db.get_statistics() or {}
        summary = analyzer.get_summary_stats(24) or {}
        properties = db.get_new_properties(hours=24) or []
        
        # Valeurs par défaut si aucune propriété
        avg_price = stats.get('avg_price') or 0
        min_price = stats.get('min_price') or 0
        max_price = stats.get('max_price') or 0
        
        data = {
            'total_properties': stats.get('total_properties', 0),
            'avg_price': f"{int(avg_price):,.0f}" if avg_price else "0",
            'new_24h': len(properties) if properties else 0,
            'by_source': stats.get('by_source', {}),
            'by_status': stats.get('by_status', {}),
            'price_range': f"{int(min_price):,} - {int(max_price):,}" if (min_price or max_price) else "N/A"
        }
        
        return render_template('dashboard.html', **data)
    except Exception as e:
        logger.error(f"Erreur dashboard: {e}")
        return "Erreur serveur", 500


@app.route('/properties')
def properties():
    """Page des propriétés"""
    page = request.args.get('page', 1, type=int)
    limit = 20
    offset = (page - 1) * limit
    
    props = db.get_properties()
    total = len(props)
    props = props[offset:offset + limit]
    
    # Convertir Row objects en dictionnaires
    properties_list = []
    for p in props:
        properties_list.append({
            'id': p['id'],
            'title': p['title'],
            'price': f"{p['price']:,} €" if p['price'] else 'N/A',
            'location': p['location'],
            'source': p['source'],
            'dpe': p['dpe'] or 'N/A',
            'status': p['status'],
            'url': p['url']
        })
    
    return render_template('properties.html', 
                         properties=properties_list,
                         page=page,
                         total=total,
                         pages=(total + limit - 1) // limit)


@app.route('/search')
def search():
    """Page de recherche"""
    scrapers = list(SCRAPERS_CONFIG.keys())
    return render_template('search.html', scrapers=scrapers)


@app.route('/scheduler')
def scheduler_page():
    """Page du planificateur"""
    from config import SCHEDULER_CONFIG, NOTIFICATION_CONFIG
    
    return render_template('scheduler.html',
                         interval=SCHEDULER_CONFIG['interval_hours'],
                         send_time=NOTIFICATION_CONFIG['send_time'])


@app.route('/sites')
def sites():
    """Page de gestion des sites"""
    scrapers = []
    for name, config in SCRAPERS_CONFIG.items():
        scrapers.append({
            'id': name,
            'name': config.get('name', name),
            'enabled': config.get('enabled', False),
            'url': config.get('url', ''),
            'timeout': config.get('timeout', 30)
        })
    
    return render_template('sites.html', scrapers=scrapers)


@app.route('/statistics')
def statistics():
    """Page des statistiques"""
    stats = db.get_statistics()
    return render_template('statistics.html', stats=stats)


@app.route('/config')
def config_page():
    """Page de configuration"""
    return render_template('config.html')


@app.route('/logs')
def logs():
    """Page des logs"""
    log_file = Path(__file__).parent / 'logs' / 'immobilier-scraper.log'
    
    logs_content = []
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            # Afficher les 100 dernières lignes
            logs_content = lines[-100:]
    
    return render_template('logs.html', logs=logs_content)


# ============================================================================
# API - SCRAPING
# ============================================================================

@app.route('/api/scrape', methods=['POST'])
def api_scrape():
    """Lancer un scraping avec les paramètres de configuration"""
    try:
        data = request.json
        source = data.get('source', 'all')
        
        # Utiliser les paramètres de configuration actuels
        budget_min = SEARCH_CONFIG.get('budget_min', 200000)
        budget_max = SEARCH_CONFIG.get('budget_max', 500000)
        dpe_max = SEARCH_CONFIG.get('dpe_max', 'D')
        zones = SEARCH_CONFIG.get('zones', ['Paris', 'Hauts-de-Seine', 'Val-de-Marne'])
        
        logger.info(f"🔍 Scraping avec paramètres: {budget_min}€-{budget_max}€, DPE<={dpe_max}, zones={zones}")
        
        if source == 'all':
            properties = scraper_manager.scrape_all(
                budget_min=budget_min,
                budget_max=budget_max,
                dpe_max=dpe_max,
                zones=zones
            )
        else:
            properties = scraper_manager.scrape_single(
                source,
                budget_min=budget_min,
                budget_max=budget_max,
                dpe_max=dpe_max,
                zones=zones
            )
        
        # Ajouter à la base
        new_count = 0
        for prop in properties:
            if not db.property_exists(prop.get('url')):
                db.add_property(prop)
                new_count += 1
        
        return jsonify({
            'success': True,
            'total': len(properties),
            'new': new_count,
            'message': f'{new_count} nouvelle(s) propriété(s) trouvée(s)'
        })
    
    except Exception as e:
        logger.error(f"Erreur scraping: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/search', methods=['POST'])
def api_search():
    """Recherche avancée"""
    try:
        filters = request.json
        
        db_filters = {
            'price_min': filters.get('price_min'),
            'price_max': filters.get('price_max'),
            'dpe_max': filters.get('dpe_max'),
            'location': filters.get('location'),
            'status': filters.get('status')
        }
        
        properties = db.get_properties(db_filters)
        
        props_list = []
        for p in properties[:50]:  # Limiter à 50
            props_list.append({
                'id': p['id'],
                'title': p['title'][:60],
                'price': p['price'],
                'location': p['location'],
                'dpe': p['dpe'],
                'surface': p['surface'],
                'source': p['source']
            })
        
        return jsonify({
            'success': True,
            'count': len(properties),
            'properties': props_list
        })
    
    except Exception as e:
        logger.error(f"Erreur recherche: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/property/<property_id>', methods=['GET', 'POST'])
def api_property(property_id):
    """Détails d'une propriété"""
    try:
        if request.method == 'GET':
            # Récupérer les détails
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM properties WHERE id = ?', (property_id,))
            prop = cursor.fetchone()
            conn.close()
            
            if prop:
                return jsonify({
                    'success': True,
                    'property': dict(prop)
                })
            else:
                return jsonify({'success': False, 'error': 'Non trouvé'}), 404
        
        else:  # POST
            # Mettre à jour
            data = request.json
            status = data.get('status')
            notes = data.get('notes')
            
            db.update_property_status(property_id, status, notes)
            
            return jsonify({'success': True})
    
    except Exception as e:
        logger.error(f"Erreur propriété: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# API - SITES/SCRAPERS
# ============================================================================

@app.route('/api/sites', methods=['GET'])
def api_get_sites():
    """Liste des sites configurés"""
    sites = []
    for name, config in SCRAPERS_CONFIG.items():
        sites.append({
            'id': name,
            'name': config.get('name', name),
            'enabled': config.get('enabled', False),
            'url': config.get('url', '')
        })
    
    return jsonify(sites)


@app.route('/api/sites/<site_id>', methods=['PUT'])
def api_update_site(site_id):
    """Activer/désactiver un site"""
    try:
        data = request.json
        
        if site_id in SCRAPERS_CONFIG:
            SCRAPERS_CONFIG[site_id]['enabled'] = data.get('enabled', False)
            
            # Sauvegarder la config
            # Note: Dans une vraie app, on sauvegarderait dans la BD
            
            return jsonify({
                'success': True,
                'message': f'{SCRAPERS_CONFIG[site_id].get("name")} '
                          f'{"activé" if data.get("enabled") else "désactivé"}'
            })
        else:
            return jsonify({'success': False, 'error': 'Site non trouvé'}), 404
    
    except Exception as e:
        logger.error(f"Erreur update site: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/sites/new', methods=['POST'])
def api_add_site():
    """Ajouter un nouveau site"""
    try:
        data = request.json
        
        site_id = data.get('id', 'new_scraper')
        
        new_scraper_config = {
            'name': data.get('name'),
            'url': data.get('url'),
            'enabled': data.get('enabled', True),
            'timeout': data.get('timeout', 30),
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
        
        SCRAPERS_CONFIG[site_id] = new_scraper_config
        
        # Sauvegarder dans un fichier JSON
        config_file = Path(__file__).parent / 'data' / 'custom_sites.json'
        config_file.parent.mkdir(exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(dict(SCRAPERS_CONFIG), f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'message': f'Site {data.get("name")} ajouté avec succès'
        })
    
    except Exception as e:
        logger.error(f"Erreur add site: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# API - PLANIFICATEUR
# ============================================================================

@app.route('/api/scheduler/status', methods=['GET'])
def api_scheduler_status():
    """État du planificateur"""
    return jsonify({
        'running': True,  # À implémenter avec état réel
        'last_run': 'Maintenant',
        'next_run': '12:00',
        'frequency': '2h'
    })


@app.route('/api/scheduler/start', methods=['POST'])
def api_scheduler_start():
    """Démarrer le planificateur"""
    try:
        return jsonify({
            'success': True,
            'message': 'Planificateur démarré'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/scheduler/stop', methods=['POST'])
def api_scheduler_stop():
    """Arrêter le planificateur"""
    try:
        return jsonify({
            'success': True,
            'message': 'Planificateur arrêté'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# API - STATISTIQUES
# ============================================================================

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Statistiques"""
    try:
        stats = db.get_statistics()
        summary = analyzer.get_summary_stats(24)
        
        return jsonify({
            'total': stats.get('total_properties', 0),
            'avg_price': stats.get('avg_price', 0),
            'min_price': stats.get('min_price', 0),
            'max_price': stats.get('max_price', 0),
            'by_source': stats.get('by_source', {}),
            'by_status': stats.get('by_status', {}),
            'new_24h': summary.get('count', 0)
        })
    except Exception as e:
        logger.error(f"Erreur stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# API - ALERTES EMAIL
# ============================================================================

@app.route('/api/alerts/test', methods=['POST'])
def api_test_alert():
    """Test d'alerte email"""
    try:
        from notifier import EmailNotifier
        
        # Récupérer les propriétés récentes
        props = db.get_new_properties(hours=24)
        
        if not props:
            return jsonify({
                'success': False,
                'error': 'Aucune propriété récente'
            })
        
        # Convertir Row en dict
        props_list = [dict(p) for p in props[:5]]
        
        notifier = EmailNotifier()
        success = notifier.send_alert(props_list, 'Test depuis l\'interface')
        
        return jsonify({
            'success': success,
            'message': 'Email de test envoyé' if success else 'Erreur lors de l\'envoi'
        })
    except Exception as e:
        logger.error(f"Erreur test alert: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# API - CONFIGURATION
# ============================================================================

@app.route('/api/config/get', methods=['GET'])
def api_get_config():
    """Récupérer la configuration actuelle"""
    try:
        config = {
            'budget_min': SEARCH_CONFIG.get('budget_min', 200000),
            'budget_max': SEARCH_CONFIG.get('budget_max', 500000),
            'dpe_max': SEARCH_CONFIG.get('dpe_max', 'D'),
            'surface_min': 30,
            'zones': SEARCH_CONFIG.get('zones', ['Paris', 'Hauts-de-Seine', 'Val-de-Marne']),
            'email': 'khadhraoui.jalel@gmail.com',
            'report_time': '09:00',
            'email_notifications': True
        }
        
        return jsonify({
            'success': True,
            'config': config
        })
    except Exception as e:
        logger.error(f"Erreur get config: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/config/save', methods=['POST'])
def api_save_config():
    """Sauvegarder la configuration"""
    try:
        data = request.json
        
        SEARCH_CONFIG['budget_min'] = data.get('budget_min', 200000)
        SEARCH_CONFIG['budget_max'] = data.get('budget_max', 500000)
        SEARCH_CONFIG['dpe_max'] = data.get('dpe_max', 'D')
        SEARCH_CONFIG['zones'] = data.get('zones', [])
        
        config_file = Path(__file__).parent / 'data' / 'user_config.json'
        config_file.parent.mkdir(exist_ok=True)
        
        user_config = {
            'budget_min': data.get('budget_min'),
            'budget_max': data.get('budget_max'),
            'dpe_max': data.get('dpe_max'),
            'surface_min': data.get('surface_min'),
            'zones': data.get('zones'),
            'email': data.get('email'),
            'report_time': data.get('report_time'),
            'email_notifications': data.get('email_notifications')
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(user_config, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'Configuration enregistrée avec succès'
        })
    except Exception as e:
        logger.error(f"Erreur save config: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/db/optimize', methods=['POST'])
def api_db_optimize():
    """Optimiser la base de données"""
    try:
        db.optimize()
        return jsonify({
            'success': True,
            'message': 'Base de données optimisée'
        })
    except Exception as e:
        logger.error(f"Erreur optimize db: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/db/cleanup', methods=['POST'])
def api_db_cleanup():
    """Nettoyer les doublons"""
    try:
        removed = db.cleanup_duplicates()
        return jsonify({
            'success': True,
            'message': f'{removed} doublon(s) supprimé(s)'
        })
    except Exception as e:
        logger.error(f"Erreur cleanup db: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/db/reset', methods=['POST'])
def api_db_reset():
    """Réinitialiser la base de données"""
    try:
        db.reset()
        return jsonify({
            'success': True,
            'message': 'Base de données réinitialisée'
        })
    except Exception as e:
        logger.error(f"Erreur reset db: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# GESTION DES ERREURS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Page 404"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Erreur serveur"""
    logger.error(f"Erreur serveur: {error}")
    return render_template('500.html'), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                   INTERFACE WEB D'ADMINISTRATION                          ║
║                                                                            ║
║  🌐 Accessible à: http://localhost:5000                                  ║
║                                                                            ║
║  ✓ Dashboard du scraping                                                  ║
║  ✓ Gestion des propriétés                                                ║
║  ✓ Recherche avancée                                                     ║
║  ✓ Configuration des sites                                               ║
║  ✓ Planificateur de tâches                                               ║
║  ✓ Statistiques en temps réel                                            ║
║  ✓ Gestion des alertes                                                   ║
║                                                                            ║
║  Appuyer sur Ctrl+C pour arrêter                                         ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
