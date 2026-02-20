"""
Script de configuration initiale du système de scraping immobilier
"""
import os
import sys
import shutil
from pathlib import Path
from dotenv import load_dotenv

def setup_environment():
    """Configurer l'environnement"""
    base_dir = Path(__file__).parent
    
    # Créer le fichier .env s'il n'existe pas
    env_file = base_dir / '.env'
    env_example = base_dir / '.env.example'
    
    if not env_file.exists() and env_example.exists():
        print("📋 Création du fichier .env...")
        shutil.copy(env_example, env_file)
        print(f"✓ Fichier .env créé. Veuillez le configurer avec vos paramètres.")
        print(f"  Éditer: {env_file}")
    
    # Créer les répertoires nécessaires
    required_dirs = [
        base_dir / 'database' / 'backups',
        base_dir / 'logs'
    ]
    
    for dir_path in required_dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print("✓ Répertoires créés")
    
    # Vérifier les dépendances
    print("\n📦 Vérification des dépendances...")
    try:
        import requests
        import bs4
        import dotenv
        import apscheduler
        print("✓ Toutes les dépendances sont installées")
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("   Exécuter: pip install -r requirements.txt")
        return False
    
    return True


def check_configuration():
    """Vérifier la configuration"""
    print("\n⚙️ Vérification de la configuration...")
    
    load_dotenv()
    
    # Vérifier EMAIL_PASSWORD
    email_password = os.getenv('EMAIL_PASSWORD')
    if not email_password or email_password == 'votre_mot_de_passe_gmail_app':
        print("⚠️  EMAIL_PASSWORD non configuré")
        print("   Créer un mot de passe d'application Gmail:")
        print("   https://myaccount.google.com/apppasswords")
        print("   puis le configurer dans .env")
        return False
    
    print("✓ Configuration valide")
    return True


def init_database():
    """Initialiser la base de données"""
    print("\n💾 Initialisation de la base de données...")
    try:
        from database import Database
        db = Database()
        stats = db.get_statistics()
        print(f"✓ Base de données initialisée")
        print(f"  Total propriétés: {stats['total_properties']}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return False


def test_email():
    """Tester la connexion email"""
    print("\n📧 Test de la connexion email...")
    try:
        from notifier import EmailNotifier
        notifier = EmailNotifier()
        
        # Test simple d'envoi
        print("  Envoi d'un email de test...")
        # Envoyer un email minimal pour tester
        success = notifier.send_alert([{
            'title': 'Test - Système de scraping immobilier',
            'location': 'Test',
            'price': 300000,
            'surface': 100,
            'rooms': 3,
            'dpe': 'C',
            'url': 'https://example.com',
            'source': 'Test'
        }], 'Test de connexion')
        
        if success:
            print("✓ Email de test envoyé avec succès")
            return True
        else:
            print("❌ Erreur lors de l'envoi de l'email")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def main():
    """Fonction principale"""
    print("=" * 60)
    print("🏠 Configuration du système de scraping immobilier")
    print("=" * 60)
    
    # Étape 1: Configurer l'environnement
    if not setup_environment():
        return 1
    
    # Étape 2: Vérifier la configuration
    if not check_configuration():
        print("\n⚠️  Configuration incomplète. Veuillez éditer .env et relancer.")
        return 1
    
    # Étape 3: Initialiser la base de données
    if not init_database():
        return 1
    
    # Étape 4: Tester l'email
    print("\n🔧 Voulez-vous tester la connexion email? (y/n)")
    response = input("> ").lower()
    if response == 'y':
        if not test_email():
            print("⚠️  Email de test échoué. Vérifier vos paramètres.")
    
    print("\n" + "=" * 60)
    print("✅ Configuration complétée!")
    print("=" * 60)
    print("\nCommandes pour démarrer:")
    print("  • Scraping unique:    python main.py")
    print("  • Planificateur:       python scheduler.py")
    print("  • Interface CLI:       python cli.py help")
    print("\nPour plus d'informations: consulter README.md")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
