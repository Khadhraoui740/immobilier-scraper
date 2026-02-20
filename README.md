# 🏠 Système Complet de Scraping Immobilier

Un système de scraping automatisé et avancé pour trouver des propriétés immobilières répondant à vos critères sur plusieurs plateformes françaises avec alertes email.

## ✨ Fonctionnalités

- **🔍 Scraping multi-plateforme**: SeLoger, PAP, LeBonCoin
- **📊 Base de données SQLite** : Stockage persistant et requêtes avancées
- **📧 Alertes email automatiques** : Notifications pour les nouvelles annonces
- **⏰ Planification automatique** : Scraping régulier et rapports quotidiens
- **💾 Historique complet** : Suivi des modifications de prix et statuts
- **🎯 Filtrage avancé** : Budget, DPE, localisation, surface, etc.
- **📱 CLI intuitive** : Gestion complète depuis la ligne de commande
- **📈 Statistiques détaillées** : Analyse des données scrapées

## 📋 Critères de Recherche

- **Budget** : 200 000 € - 500 000 €
- **Zones** : Paris (75), Hauts-de-Seine (92), Val-de-Marne (94)
- **DPE max** : D
- **Email de notification** : khadhraoui.jalel@gmail.com

## 🚀 Installation

### Prérequis

- Python 3.8+
- pip
- Un compte Gmail avec authentification par mot de passe d'application

### Étapes d'installation

1. **Cloner/créer le projet**
```bash
cd C:\Users\jaleleddinekhadhraou\immobilier-scraper
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
# Copier le fichier d'exemple
copy .env.example .env

# Éditer .env avec vos paramètres
# Particulièrement: EMAIL_PASSWORD (mot de passe d'application Gmail)
```

### Configuration Email Gmail

1. Activer l'authentification 2FA dans votre compte Google
2. Créer un mot de passe d'application: https://myaccount.google.com/apppasswords
3. Copier le mot de passe dans le fichier `.env` sous `EMAIL_PASSWORD`

## 📖 Utilisation

### Scraping Manuel

```bash
# Scraper toutes les plateformes
python main.py

# Scraper une plateforme spécifique
python cli.py scrape seloger
python cli.py scrape pap
python cli.py scrape leboncoin
```

### Planification Automatique

```bash
# Démarrer le planificateur (scraping toutes les 2 heures + rapport quotidien)
python scheduler.py
```

### Interface CLI

```bash
# Lister les propriétés
python cli.py list
python cli.py list --status disponible --limit 20

# Afficher les statistiques
python cli.py stats

# Gérer les favoris
python cli.py favorite --add <property_id>
python cli.py favorite --list

# Mettre à jour les statuts
python cli.py status --set <property_id> contacté
python cli.py status --list

# Envoyer des alertes
python cli.py email --send --new
python cli.py email --send --report

# Afficher l'aide
python cli.py help
```

## 📁 Structure du Projet

```
immobilier-scraper/
├── config.py                 # Configuration centralisée
├── logger.py                 # Gestion des logs
├── main.py                   # Script principal de scraping
├── scheduler.py              # Planificateur automatisé
├── cli.py                    # Interface en ligne de commande
├── requirements.txt          # Dépendances Python
├── .env.example              # Exemple de configuration
├── database/
│   ├── __init__.py
│   ├── db.py                 # Gestion de la base de données
│   ├── immobilier.db         # Base de données SQLite
│   └── backups/              # Sauvegardes de la BD
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py       # Classe de base abstraite
│   ├── seloger_scraper.py    # Scraper SeLoger
│   ├── pap_scraper.py        # Scraper PAP
│   ├── leboncoin_scraper.py  # Scraper LeBonCoin
│   └── manager.py            # Gestionnaire de scrapers
├── notifier/
│   ├── __init__.py
│   └── email_notifier.py     # Système d'alertes email
└── logs/
    └── immobilier-scraper.log
```

## 🗄️ Base de Données

### Tables principales

**properties** : Annonces immobilières
- id, source, url, title, location, price, surface, rooms, DPE, etc.

**property_history** : Historique des modifications
- Suivi des changements de prix et de statut

**searches** : Recherches sauvegardées
- Critères de recherche et résultats

**alerts** : Alertes envoyées
- Historique des notifications

## ⚙️ Configuration

### Modifier les critères de recherche

Éditer `config.py`:
```python
SEARCH_CONFIG = {
    'budget_min': 200000,
    'budget_max': 500000,
    'dpe_max': 'D',
    'zones': ['Paris', 'Hauts-de-Seine', 'Val-de-Marne']
}
```

### Modifier l'intervalle de scraping

Éditer `config.py`:
```python
SCHEDULER_CONFIG = {
    'interval_hours': 2,  # Scraper toutes les 2 heures
    'send_time': '09:00'  # Rapport quotidien à 9h
}
```

## 📊 Exemples de Données

Les données scrapées incluent:
- **Titre** : Titre de l'annonce
- **Prix** : Prix d'achat
- **Localisation** : Adresse complète
- **Surface** : Superficie en m²
- **Pièces/Chambres** : Nombre de pièces
- **DPE** : Performance énergétique (A-G)
- **GES** : Émissions de gaz à effet de serre
- **Images** : URLs des photos
- **Contact** : Informations du vendeur/agent
- **URL** : Lien vers l'annonce

## 📧 Format des Emails

Les alertes contiennent:
- Liste des propriétés correspondant aux critères
- Détails complets (prix, surface, DPE, lien)
- Synthèse visuelle avec code couleur DPE
- Horodatage et source de l'annonce

## 🔄 Tâches Planifiées

1. **Scraping régulier** (par défaut toutes les 2 heures)
   - Récupère les nouvelles annonces
   - Détecte les doublons
   - Envoie alertes pour les nouveautés

2. **Rapport quotidien** (par défaut à 09:00)
   - Statistiques globales
   - Distribution par source
   - Distribution par statut
   - Analysé des prix

## 🛠️ Dépannage

### Email non reçu
- Vérifier `EMAIL_PASSWORD` dans `.env`
- Vérifier que l'authentification 2FA est activée
- Vérifier les logs dans `logs/immobilier-scraper.log`

### Pas de données scrapées
- Vérifier la connexion Internet
- Vérifier que les URLs des plateformes sont à jour
- Consulter les logs pour les erreurs HTML

### Base de données corrompue
- Supprimer `database/immobilier.db`
- Relancer le script (recréera la BD)

## 📝 Statuts de Propriétés

- **disponible** : Annonce active
- **contacté** : Contact pris avec le vendeur
- **visité** : Visite effectuée
- **rejeté** : Propriété non correspond aux besoins
- **acheté** : Achat finalisé

## 📈 Améliorations Futures

- [ ] Support de zones géographiques personnalisées
- [ ] Scraping de l'évolution des prix
- [ ] Gestion des utilisateurs multiples
- [ ] Interface web
- [ ] Intégration Google Maps
- [ ] Support des SMS
- [ ] Machine Learning pour recommandations

## 📄 Licence

Ce projet est fourni à titre d'exemple éducatif.

## ⚖️ IMPORTANT - Respect des conditions d'utilisation

Ce scraper respecte les bonnes pratiques:
- Délais entre requêtes
- User-Agent approprié
- Pas de surcharge serveur
- Respect des robots.txt

Vérifier toujours les conditions d'utilisation des sites avant scraping.

---

**Créé** : Février 2026
**Email** : khadhraoui.jalel@gmail.com
