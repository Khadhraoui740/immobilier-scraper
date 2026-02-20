#!/usr/bin/env python3
"""
Script pour ouvrir l'application dans le navigateur par défaut
"""

import webbrowser
import time
import sys
from pathlib import Path

# Ajouter le répertoire au chemin Python
sys.path.insert(0, str(Path(__file__).parent))

def show_menu():
    """Afficher le menu"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║        SCRAPING IMMOBILIER - Ouverture de l'Interface         ║
╚════════════════════════════════════════════════════════════════╝

Choisissez la page à ouvrir:

1. Dashboard (Accueil)
2. Propriétés
3. Recherche Avancée
4. Gestion des Sites
5. ⚙️ CONFIGURATION (Nouveau!)
6. Planificateur
7. Statistiques
8. Logs
9. GitHub Repository
0. Quitter

""")

def open_page(choice):
    """Ouvrir la page sélectionnée"""
    
    pages = {
        '1': ('http://localhost:5000/', 'Dashboard'),
        '2': ('http://localhost:5000/properties', 'Propriétés'),
        '3': ('http://localhost:5000/search', 'Recherche'),
        '4': ('http://localhost:5000/sites', 'Gestion des Sites'),
        '5': ('http://localhost:5000/config', 'Configuration ⚙️'),
        '6': ('http://localhost:5000/scheduler', 'Planificateur'),
        '7': ('http://localhost:5000/statistics', 'Statistiques'),
        '8': ('http://localhost:5000/logs', 'Logs'),
        '9': ('https://github.com/jalel-khadhraoui/immobilier-scraper', 'GitHub Repository'),
    }
    
    if choice in pages:
        url, name = pages[choice]
        print(f"\n🌐 Ouverture {name}...")
        print(f"   URL: {url}\n")
        webbrowser.open(url)
        return True
    elif choice == '0':
        print("Au revoir! 👋\n")
        return False
    else:
        print("❌ Choix invalide. Réessayez.\n")
        return True

def main():
    """Fonction principale"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║  Assurez-vous que l'application est lancée:                   ║
║  python app.py                                                 ║
║                                                                ║
║  L'application doit être accessible à:                         ║
║  http://localhost:5000                                         ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    import time
    time.sleep(2)
    
    while True:
        show_menu()
        choice = input("Entrez votre choix: ").strip()
        
        if not open_page(choice):
            break
        
        input("Appuyez sur Entrée pour continuer...")
        print("\n" * 2)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nArrêt du programme. Au revoir! 👋\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}\n")
        sys.exit(1)
