# 📋 Guide d'Installation Complet

## 🎯 Objectif du Système

Un système complet et automatisé pour scraper les annonces immobilières sur 3 plateformes avec:
- **Budget**: 200 000 € - 500 000 €
- **Zones**: Paris, Hauts-de-Seine, Val-de-Marne
- **DPE max**: D
- **Alertes email** automatiques vers khadhraoui.jalel@gmail.com

## 📁 Structure Complète du Projet

```
immobilier-scraper/
├── SCRIPTS PRINCIPAUX
├── main.py                 # Scraping unique
├── scheduler.py            # Scraping automatisé
├── cli.py                  # Interface CLI
├── demo.py                 # Démonstration
├── setup.py                # Configuration
├── admin.py                # Administration
├── start.py                # Menu interactif
│
├── CONFIGURATION
├── config.py               # Configuration
├── logger.py               # Logs
├── utils.py                # Utilitaires
├── analyzer.py             # Analyse
│
├── MODULES
├── database/ (db.py)       # Base de données
├── scrapers/ (3 scrapers)  # SeLoger, PAP, LeBonCoin
├── notifier/ (email)       # Alertes
│
├── DOCUMENTATION
├── README.md               # Doc complète
├── INSTALLATION.md         # Ce fichier
├── QUICKSTART.txt          # Démarrage rapide
├── ROADMAP.txt             # Améliorations
│
└── FICHIERS SYSTÈME
├── requirements.txt        # Dépendances
├── .env.example            # Config exemple
└── .gitignore              # Fichiers ignorés
```

## 🚀 Installation Étape par Étape

### Étape 1: Prérequis

- Python 3.8+ installé
- Vérify: `python --version`

### Étape 2: Environnement Virtuel

```bash
cd C:\Users\jaleleddinekhadhraou\immobilier-scraper
python -m venv venv
venv\Scripts\activate
```

### Étape 3: Dépendances

```bash
pip install -r requirements.txt
```

### Étape 4: Configuration Email

1. Créer un mot de passe d'application Gmail: https://myaccount.google.com/apppasswords
2. Copier `.env.example` vers `.env`
3. Ajouter le mot de passe dans `EMAIL_PASSWORD`

### Étape 5: Démarrage

```bash
python setup.py  # Configuration initiale
python start.py  # Menu interactif
```

## 📊 Structure de la Base de Données

**Tables**:
- `properties`: Annonces (30+ colonnes)
- `property_history`: Historique des modifications
- `searches`: Recherches sauvegardées
- `alerts`: Alertes envoyées

**Taille initiale**: ~10MB par 10,000 propriétés

## 🎬 Commandes Principales

| Commande | Description |
|----------|-------------|
| `python main.py` | Scraping unique |
| `python scheduler.py` | Scraping automatique |
| `python cli.py list` | Voir les propriétés |
| `python cli.py stats` | Statistiques |
| `python demo.py` | Démonstration |
| `python admin.py backup` | Sauvegarder la BD |
| `python start.py` | Menu interactif |

## ✨ Utilisation Rapide

```bash
# 1. Installation (première fois uniquement)
python setup.py

# 2. Scraper et recevoir une alerte
python main.py

# 3. Voir les résultats
python cli.py list

# 4. Lancer le scraping automatique
python scheduler.py
```

## 🔧 Personnalisation

Éditer `config.py` pour:
- Budget min/max
- Zones de recherche
- DPE maximum
- Intervalle de scraping
- Heure des rapports

## 📧 Tests Email

```bash
python cli.py email --send --new
```

## 💾 Sauvegardes

```bash
python admin.py backup        # Créer une sauvegarde
python admin.py restore <file> # Restaurer
python admin.py cleanup-backups # Nettoyer
```

## 📈 Statistiques

```bash
python cli.py stats
```

## ⚠️ Dépannage

| Problème | Solution |
|----------|----------|
| Email non reçu | Vérifier MESSAGE_PASSWORD dans .env |
| Pas de données | Vérifier connexion Internet |
| BD corrompue | Supprimer database/immobilier.db |

## 📚 Documentation Complète

- `README.md`: Guide complet
- `QUICKSTART.txt`: Démarrage rapide
- `ROADMAP.txt`: Futures améliorations
- Logs: `logs/immobilier-scraper.log`

## 🎓 Exemples

```bash
# Lister les 20 meilleures annonces
python cli.py list --limit 20

# Marquer comme visité
python cli.py status --set <ID> visité

# Ajouter aux favoris
python cli.py favorite --add <ID>

# Générer un rapport
python cli.py email --send --report
```

## ✅ Vérification

```bash
python admin.py health  # Vérification de santé complète
```

## 🎉 Vous êtes Prêt!

```bash
python start.py  # Démarrer le menu interactif
```

---

**Créé**: Février 2026  
**Contact**: khadhraoui.jalel@gmail.com  
**Répertoire**: C:\Users\jaleleddinekhadhraou\immobilier-scraper
