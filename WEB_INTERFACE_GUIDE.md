# Guide d'utilisation - Interface Web d'Administration

## Démarrage

### 1. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 2. Configuration de l'environnement
Copier `.env.example` en `.env` et remplir avec vos paramètres :
```bash
cp .env.example .env
```

### 3. Lancer l'application
```bash
python app.py
```

L'interface est accessible à : **http://localhost:5000**

---

## Fonctionnalités de l'Interface

### 📊 Dashboard (Accueil)
- **Vue d'ensemble** : Statistiques principales (total propriétés, nouvelles, par source)
- **Actions rapides** :
  - 🔄 **Scraper Maintenant** : Lance le scraping sur tous les sites
  - 📧 **Tester Email** : Envoie un email de test
  - ⏰ **Démarrer Planificateur** : Lance le scraping automatique

### 🏠 Propriétés
- **Liste des propriétés** avec filtres
- **Informations** : Prix, surface, DPE, source, date
- **Édition** : Mettre à jour le statut de chaque propriété
- **Statuts** : disponible, contacté, visité, rejeté, acheté

### 🔍 Recherche Avancée
Filtrer les propriétés par :
- 💰 **Prix** : plage min/max
- 🏘️ **Localisation** : zones/codes postaux
- 📋 **DPE** : A à G
- ⏱️ **Statut** : disponible, contacté, etc.

### 📍 Gestion des Sites
- **Voir les scrapers actifs** (SeLoger, PAP, LeBonCoin, BienIci)
- **Activer/Désactiver** des scrapers
- **Ajouter un nouveau site** :
  - ID unique
  - Nom du site
  - URL de base
  - Timeout (en secondes)
- **Tester** chaque site

### ⏰ Planificateur
Configure le scraping automatique :
- **Intervalle** : Scraper toutes les X heures (défaut: 2h)
- **Rapport quotidien** : Heure d'envoi du rapport (défaut: 09:00)
- **Notifications** : Actif/Désactif
- **Historique** : Voir les exécutions précédentes

### 📈 Statistiques
- **Distribution par source** : SeLoger, PAP, LeBonCoin, BienIci
- **Distribution par statut** : Disponible, contacté, visité, etc.
- **Tableaux** avec compteurs et pourcentages

### 📋 Logs
- **Visualisation** en temps réel
- **Auto-refresh** automatique
- **Download** des logs complets
- **Filtrage** par type

---

## Points d'API

L'interface utilise une API REST pour communiquer avec le backend:

### Scraping
```
POST /api/scrape
Body: { "source": "all" | "seloger" | "pap" | "leboncoin" | "bienici" }
```

### Recherche
```
POST /api/search
Body: {
  "price_min": 200000,
  "price_max": 500000,
  "dpe_max": "D",
  "location": "75",
  "status": "disponible"
}
```

### Propriétés
```
GET /api/property/{id}
POST /api/property/{id}
Body: { "status": "nouveau_statut" }
```

### Sites
```
GET /api/sites                      # Liste les sites
PUT /api/sites/{id}                 # Activer/Désactiver
Body: { "enabled": true/false }
POST /api/sites/new                 # Ajouter un site
Body: { "id": "...", "name": "...", "url": "...", "timeout": 30 }
```

### Planificateur
```
POST /api/scheduler/start           # Démarrer
POST /api/scheduler/stop            # Arrêter
GET /api/scheduler/status           # État actuel
```

### Statistiques
```
GET /api/stats                      # Toutes les stats
```

---

## Configuration avancée

### Filtres de recherche
Modifiez `config.py` pour changer les critères par défaut:

```python
SEARCH_CONFIG = {
    'budget_min': 200000,
    'budget_max': 500000,
    'dpe_max': 'D',
    'zones': ['Paris', 'Hauts-de-Seine', 'Val-de-Marne']
}
```

### Scheduler
```python
SCHEDULER_CONFIG = {
    'interval_hours': 2,        # Intervalle en heures
    'max_workers': 3,           # Scrapers parallèles
    'retry_failed_after_minutes': 30
}
```

### Email
```python
EMAIL_CONFIG = {
    'email': 'khadhraoui.jalel@gmail.com',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}
```

---

## Ajouter un nouveau scraper

### 1. Créer le scraper (e.g., `scrapers/newsite_scraper.py`)
```python
from .base_scraper import BaseScraper

class NewSiteScraper(BaseScraper):
    def __init__(self, config=None):
        super().__init__("NewSite", config)
    
    def scrape(self, filters):
        # Votre logique de scraping
        pass
```

### 2. Ajouter à `config.py`
```python
SCRAPERS_CONFIG = {
    'newsite': {
        'name': 'NewSite',
        'url': 'https://...',
        'enabled': True,
        'timeout': 30
    }
}
```

### 3. Importer dans `scrapers/manager.py`
```python
from .newsite_scraper import NewSiteScraper

# Dans _init_scrapers():
if SCRAPERS_CONFIG['newsite']['enabled']:
    self.scrapers['newsite'] = NewSiteScraper(SCRAPERS_CONFIG['newsite'])
```

### 4. Utiliser l'interface pour l'activer
L'interface web détectera automatiquement le nouveau scraper!

---

## Dépannage

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Port 5000 déjà utilisé"
Modifier dans `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Emails ne s'envoient pas
1. Vérifier les identifiants dans `.env`
2. Pour Gmail : utiliser un [mot de passe d'application](https://myaccount.google.com/apppasswords)
3. Vérifier les logs

### Scrapers trop lent
Augmenter le timeout dans la configuration des sites

---

## Architecture

```
immobilier-scraper/
├── app.py                  # Application Flask
├── config.py               # Configuration centralisée
├── database/db.py          # Gestion SQLite
├── scrapers/               # Modules de scraping
│   ├── manager.py          # Gestionnaire parallèle
│   ├── bienici_scraper.py  # ✨ Nouveau
│   └── ...
├── templates/              # Templates HTML/Jinja2
├── static/                 # CSS et JavaScript
└── requirements.txt        # Dépendances
```

---

## Support

Email: khadhraoui.jalel@gmail.com
