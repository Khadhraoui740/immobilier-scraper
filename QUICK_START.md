# 🚀 Démarrage Rapide - 2 minutes

## Windows

```powershell
# 1. Ouvrir PowerShell dans le dossier du projet

# 2. Créer l'environnement virtuel
python -m venv venv

# 3. Activer l'environnement
.\venv\Scripts\activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer l'application
python app.py
```

Puis ouvrir: **http://localhost:5000**

---

## Linux / Mac

```bash
# 1. Entrer dans le dossier
cd immobilier-scraper

# 2. Créer l'environnement virtuel
python3 -m venv venv

# 3. Activer l'environnement
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer l'application
python app.py
```

Puis ouvrir: **http://localhost:5000**

---

## Docker (Encore plus rapide)

```bash
# 1. Construire l'image
docker build -t immobilier-scraper .

# 2. Lancer le conteneur
docker run -d -p 5000:5000 --name app immobilier-scraper

# 3. Voir les logs
docker logs -f app
```

Puis ouvrir: **http://localhost:5000**

---

## Docker Compose (Le plus simple)

```bash
# 1. Lancer tout d'un coup
docker-compose up -d

# 2. Voir les logs
docker-compose logs -f web
```

Puis ouvrir: **http://localhost:5000**

---

## Interface Web

### Dashboard
- 📊 Voir les statistiques
- 🔄 Lancer le scraping
- 📧 Tester l'email

### Propriétés
- 🏠 Voir toutes les annonces
- 🔍 Filtrer par prix, DPE, etc.
- ✏️ Mettre à jour le statut

### Sites
- 🌐 Ajouter des nouveaux sites
- ✅ Activer/Désactiver des scrapers
- 🧪 Tester les connexions

### Planificateur
- ⏰ Configurer le scraping auto
- 📅 Définir les horaires
- 📋 Voir l'historique

### Recherche Avancée
- 💰 Budget: 200k-500k€
- 🏘️ Zones: Paris, 92, 94
- 🔤 DPE: A à D

---

## Configuration (Optionnel)

Éditer `.env`:
```
EMAIL_PASSWORD=votre_mot_de_passe_gmail
FLASK_ENV=production
```

Pour Gmail: [Obtenir un mot de passe d'application](https://myaccount.google.com/apppasswords)

---

## Arrêter l'application

```bash
# Appuyer sur Ctrl+C dans le terminal
```

Ou si avec Docker:
```bash
docker stop app
docker rm app
```

Ou si avec Docker Compose:
```bash
docker-compose down
```

---

## 📚 Fichiers utiles

| Fichier | Description |
|---------|-------------|
| `app.py` | Application Flask principale |
| `config.py` | Configuration centralisée |
| `main.py` | Scraping CLI |
| `WEB_INTERFACE_GUIDE.md` | Guide complet de l'interface |
| `API_DOCUMENTATION.md` | Documentation de l'API REST |
| `DEPLOYMENT.md` | Guide de déploiement en production |

---

## 🆘 Aide

**Port 5000 déjà utilisé?**
```powershell
netstat -ano | findstr :5000               # Windows
kill -9 $(lsof -t -i :5000)                # Mac/Linux
```

**Erreur de dépendances?**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Base de données corrompue?**
```bash
rm database/immobilier.db
python app.py  # Elle se créera automatiquement
```

---

✅ **C'est tout! Vous êtes prêt à scraper!** 🎉
