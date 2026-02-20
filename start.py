"""
Fichier de démarrage automatisé
"""
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au chemin Python
sys.path.insert(0, str(Path(__file__).parent))


def welcome():
    """Afficher le message de bienvenue"""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║         🏠 SYSTÈME COMPLET DE SCRAPING IMMOBILIER                        ║
║                                                                            ║
║  Budget: 200 000 € - 500 000 €                                           ║
║  Zones: Paris, Hauts-de-Seine, Val-de-Marne                              ║
║  Plateformes: SeLoger, PAP, LeBonCoin                                     ║
║  Email: khadhraoui.jalel@gmail.com                                        ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)


def main_menu():
    """Afficher le menu principal"""
    print("""
MENU PRINCIPAL
==============

1. Scraper une fois (main.py)
2. Démarrer le planificateur automatique (scheduler.py)
3. Interface CLI (cli.py)
4. Démonstration du système (demo.py)
5. Configuration initiale (setup.py)
6. Outils d'administration (admin.py)
7. Afficher le guide de démarrage rapide
8. Quitter

    """)


def run_script(script_name, description):
    """Exécuter un script"""
    print(f"\n▶ Lancement: {description}...")
    print("=" * 70)
    
    os.system(f"python {script_name}")
    
    print("=" * 70)
    input("Appuyer sur Entrée pour continuer...")


def show_quickstart():
    """Afficher le guide de démarrage rapide"""
    quickstart_file = Path(__file__).parent / 'QUICKSTART.txt'
    
    if quickstart_file.exists():
        with open(quickstart_file, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("Fichier QUICKSTART.txt non trouvé")
    
    input("\nAppuyer sur Entrée pour continuer...")


def main():
    """Fonction principale"""
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        
        welcome()
        main_menu()
        
        choice = input("Sélectionner une option (1-8): ").strip()
        
        if choice == '1':
            run_script('main.py', 'Scraping immobilier')
        
        elif choice == '2':
            print("\n⏰ Démarrage du planificateur...")
            print("Le planificateur va scraper toutes les 2 heures.")
            print("Appuyer sur Ctrl+C pour arrêter.\n")
            run_script('scheduler.py', 'Planificateur automatique')
        
        elif choice == '3':
            print("\n📱 Interface CLI")
            print("Commandes disponibles:")
            print("  scrape [SOURCE]     - Scraper une ou toutes les plateformes")
            print("  list                - Lister les propriétés")
            print("  stats               - Afficher les statistiques")
            print("  help                - Afficher l'aide\n")
            
            command = input("Entrer une commande: ")
            if command:
                os.system(f"python cli.py {command}")
        
        elif choice == '4':
            run_script('demo.py', 'Démonstration du système')
        
        elif choice == '5':
            run_script('setup.py', 'Configuration initiale')
        
        elif choice == '6':
            print("\n🔧 Outils d'Administration")
            print("Commandes disponibles:")
            print("  backup              - Créer une sauvegarde")
            print("  restore <fichier>   - Restaurer une sauvegarde")
            print("  optimize            - Optimiser la BD")
            print("  cleanup-backups     - Nettoyer les anciennes sauvegardes")
            print("  cleanup-logs        - Nettoyer les logs")
            print("  health              - Vérification de santé\n")
            
            command = input("Entrer une commande: ")
            if command:
                os.system(f"python admin.py {command}")
        
        elif choice == '7':
            show_quickstart()
        
        elif choice == '8':
            print("\nAu revoir! 👋")
            break
        
        else:
            print("Option invalide. Veuillez réessayer.")
            input("Appuyer sur Entrée pour continuer...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgramme interrompu.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)
