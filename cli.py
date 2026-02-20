"""
Interface CLI pour gérer le scraper immobilier
"""
import sys
import logging
from pathlib import Path
from tabulate import tabulate

# Ajouter le répertoire parent au chemin Python
sys.path.insert(0, str(Path(__file__).parent))

from logger import setup_logging
from database import Database
from scrapers.manager import ScraperManager
from notifier import EmailNotifier
from config import SEARCH_CONFIG, DPE_MAPPING, PROPERTY_STATUS

logger = setup_logging()


class ImmobilierCLI:
    """Interface CLI"""
    
    def __init__(self):
        self.db = Database()
        self.scraper_manager = ScraperManager()
        self.notifier = EmailNotifier()
    
    def cmd_scrape(self, args):
        """Commande: scrape [--source SOURCE]"""
        if args and args[0] in self.scraper_manager.scrapers:
            properties = self.scraper_manager.scrape_single(args[0])
        else:
            properties = self.scraper_manager.scrape_all()
        
        # Ajouter à la base
        for prop in properties:
            if not self.db.property_exists(prop.get('url')):
                self.db.add_property(prop)
        
        print(f"✓ {len(properties)} propriétés trouvées")
    
    def cmd_list(self, args):
        """Commande: list [--status STATUS] [--location LOCATION] [--limit LIMIT]"""
        filters = {}
        limit = 10
        
        i = 0
        while i < len(args):
            if args[i] == '--status' and i + 1 < len(args):
                filters['status'] = args[i + 1]
                i += 2
            elif args[i] == '--location' and i + 1 < len(args):
                filters['location'] = args[i + 1]
                i += 2
            elif args[i] == '--limit' and i + 1 < len(args):
                limit = int(args[i + 1])
                i += 2
            else:
                i += 1
        
        properties = self.db.get_properties(filters)[:limit]
        
        if not properties:
            print("Aucune propriété trouvée")
            return
        
        data = []
        for prop in properties:
            data.append([
                prop['id'][:8],
                prop['source'],
                prop['title'][:40],
                f"{prop['price']:,.0f} €",
                prop['dpe'] or 'N/A',
                prop['status']
            ])
        
        print(tabulate(data, headers=['ID', 'Source', 'Titre', 'Prix', 'DPE', 'Statut']))
    
    def cmd_stats(self, args):
        """Commande: stats"""
        stats = self.db.get_statistics()
        
        print("\n📊 STATISTIQUES")
        print(f"Total propriétés: {stats['total_properties']}")
        print(f"Prix moyen: {stats.get('avg_price', 0):,.0f} €")
        print(f"Prix min: {stats.get('min_price', 0):,} €")
        print(f"Prix max: {stats.get('max_price', 0):,} €")
        
        print("\nPar source:")
        for source, count in stats.get('by_source', {}).items():
            print(f"  {source}: {count}")
        
        print("\nPar statut:")
        for status, count in stats.get('by_status', {}).items():
            print(f"  {status}: {count}")
    
    def cmd_favorite(self, args):
        """Commande: favorite [--add ID | --list]"""
        if args and args[0] == '--add' and len(args) > 1:
            property_id = args[1]
            self.db.mark_as_favorite(property_id, True)
            print(f"✓ Propriété {property_id[:8]} ajoutée aux favoris")
        elif args and args[0] == '--list':
            properties = self.db.get_properties({'is_favorite': True})
            print(f"Favoris: {len(properties)} propriétés")
            for prop in properties:
                print(f"  - {prop['title']} ({prop['price']:,} €)")
        else:
            print("Usage: favorite --add ID | --list")
    
    def cmd_status(self, args):
        """Commande: status [--set ID STATUS] [--list]"""
        if args and args[0] == '--set' and len(args) > 2:
            property_id = args[1]
            status = args[2]
            self.db.update_property_status(property_id, status)
            print(f"✓ Statut de {property_id[:8]} mis à jour: {status}")
        elif args and args[0] == '--list':
            print("Statuts disponibles:")
            for status in PROPERTY_STATUS.values():
                print(f"  - {status}")
        else:
            print("Usage: status --set ID STATUS | --list")
    
    def cmd_email(self, args):
        """Commande: email --send [--new | --report]"""
        if args and args[0] == '--send':
            if len(args) > 1 and args[1] == '--new':
                new_props = self.db.get_new_properties(hours=24)
                self.notifier.send_alert(new_props)
                print("✓ Email envoyé avec les nouvelles propriétés")
            elif len(args) > 1 and args[1] == '--report':
                stats = self.db.get_statistics()
                self.notifier.send_daily_report(stats)
                print("✓ Rapport quotidien envoyé")
            else:
                print("Usage: email --send [--new | --report]")
        else:
            print("Usage: email --send [--new | --report]")
    
    def cmd_help(self, args):
        """Commande: help"""
        print("""
Commandes disponibles:
  scrape [--source SOURCE]  Effectuer un scraping (toutes sources ou une seule)
  list [options]            Lister les propriétés (--status, --location, --limit)
  stats                     Afficher les statistiques
  favorite [options]        Gérer les favoris (--add ID, --list)
  status [options]          Gérer les statuts (--set ID STATUS, --list)
  email [options]           Envoyer des emails (--send --new, --send --report)
  help                      Afficher cette aide
        """)
    
    def run(self, command, args):
        """Exécuter une commande"""
        commands = {
            'scrape': self.cmd_scrape,
            'list': self.cmd_list,
            'stats': self.cmd_stats,
            'favorite': self.cmd_favorite,
            'status': self.cmd_status,
            'email': self.cmd_email,
            'help': self.cmd_help
        }
        
        if command in commands:
            try:
                commands[command](args)
            except Exception as e:
                logger.error(f"Erreur: {e}")
                print(f"❌ Erreur: {e}")
        else:
            print(f"Commande inconnue: {command}")
            print("Tapez 'help' pour voir les commandes disponibles")


def main():
    """Fonction principale"""
    cli = ImmobilierCLI()
    
    if len(sys.argv) < 2:
        cli.cmd_help([])
        return
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    cli.run(command, args)


if __name__ == '__main__':
    main()
