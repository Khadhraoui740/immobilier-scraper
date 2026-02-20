# Scraping Immobilier - Système complet d'annonces en ligne

Bienvenue sur le **système de scraping immobilier** - une application web Python complète pour rechercher, suivre et analyser les propriétés immobilières en Île-de-France.

## 🌐 GitHub Repository

**Repository:** https://github.com/jalel-khadhraoui/immobilier-scraper  
**Branch Principal:** main  
**Dernière mise à jour:** 20 février 2026

### Cloner le projet

```bash
git clone https://github.com/jalel-khadhraoui/immobilier-scraper.git
cd immobilier-scraper
```

---

## 🚀 Démarrage Rapide

### Installation (2 minutes)

**Option 1: Python Local**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

**Option 2: Docker**
```bash
docker-compose up -d
```

Puis ouvrir: **http://localhost:5000**

---

## 📦 Fonctionnalités

✅ **Scraping Multi-Plateformes**
- SeLoger
- PAP
- LeBonCoin
- BienIci ✨

✅ **Interface Web Complète**
- Dashboard en temps réel
- Recherche avancée avec filtres
- Gestion des propriétés
- Configuration personnalisée
- Planification automatique
- Statistiques détaillées
- Logs en direct

✅ **Base de Données SQLite**
- Historique complet
- Filtrage personnalisé
- Statistiques intégrées

✅ **Email & Notifications**
- Alertes quotidiennes
- Templates HTML
- SMTP Gmail intégré

✅ **DevOps Ready**
- Docker & Docker Compose
- Support Heroku
- VPS avec Nginx

---

## 📋 Configuration Recommandée

**Paramètres par défaut:**
- Budget: 200k - 500k €
- DPE: A à D
- Zones: Paris (75), Hauts-de-Seine (92), Val-de-Marne (94)

Modifier dans: **Interface Web → ⚙️ Configuration**

---

## 📚 Documentation

| Document | Contenu |
|----------|---------|
| [QUICK_START.md](QUICK_START.md) | Démarrage en 2 minutes |
| [WEB_INTERFACE_GUIDE.md](WEB_INTERFACE_GUIDE.md) | Guide complet interface |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Endpoints API REST |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production & DevOps |

---

## 🎯 Pages Disponibles

- **`/`** - Dashboard principal
- **`/properties`** - Liste des propriétés
- **`/search`** - Recherche avancée
- **`/sites`** - Gestion des scrapers
- **`/config`** - Configuration système ⚙️
- **`/scheduler`** - Planification
- **`/statistics`** - Statistiques
- **`/logs`** - Visualiseur logs

---

## 📊 Architectures

```
immobilier-scraper/
├── app.py                  # Application Flask
├── config.py              # Configuration centrale
├── database/              # Gestion SQLite
├── scrapers/              # 4 scrapers (SeLoger, PAP, LeBonCoin, BienIci)
├── templates/             # 10 pages HTML/Jinja2
├── static/                # CSS, JavaScript
├── notifier/              # Système d'emails
└── docs/                  # Documentation
```

---

## 💻 Technologie

- **Backend:** Flask 2.3.3
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite
- **Scraping:** BeautifulSoup4, Selenium
- **Scheduling:** APScheduler
- **Email:** SMTP Gmail
- **DevOps:** Docker, Docker Compose

---

## 🔒 Sécurité

✅ Pas de stockage de mots de passe  
✅ Variables d'environnement  
✅ CORS sécurisé  
✅ Injection SQL prévenue  
✅ HTTPS ready  

---

## 📈 Performances

- ⚡ Scraping parallèle (3 workers)
- 🎯 ~2min pour scraper 4 sites
- 📊 Statistiques en temps réel
- 💾 BD optimisée et indexée

---

## 🛠️ Maintenance

```bash
# Lancer les tests
pytest tests/

# Optimiser la BD
python admin.py optimize

# Sauvegarder
python admin.py backup

# Nettoyer les doublons
python admin.py cleanup
```

---

## 📞 Support & Contribution

### Issues & Bugs

Signaler les bugs sur: [GitHub Issues](https://github.com/jalel-khadhraoui/immobilier-scraper/issues)

### Pull Requests

Les contributions sont les bienvenues! Voir [CONTRIBUTING.md](CONTRIBUTING.md)

### Contact

**Email:** khadhraoui.jalel@gmail.com  
**GitHub:** [@jalel-khadhraoui](https://github.com/jalel-khadhraoui)

---

## 📜 Licence

Ce projet est fourni à titre d'exemple. Adaptation libre pour usage personnel.

---

## 🙏 Remerciements

Développé avec **❤️** pour simplifier la recherche immobilière.

---

## 📈 Statistiques du Projet

- 54 fichiers
- 6,500+ lignes de code  
- 10 pages web
- 4 scrapers immobiliers
- 20+ endpoints API
- Documentation complète
- Production-ready

---

**Bon scraping! 🚀**

Visitez: **http://localhost:5000**
