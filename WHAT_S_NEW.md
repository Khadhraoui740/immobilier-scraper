## 🎉 CONFIGURATION ET GITHUB - MISE EN PLACE COMPLÈTE!

Vous pouvez maintenant:
1. ✅ Configurer les paramètres (prix, DPE, zones)
2. ✅ Voir le lien vers le repository GitHub
3. ✅ Accéder facilement à toutes les pages

---

## 🚀 LANCER L'APPLICATION

### Méthode 1: Interface Web Simple (RECOMMANDÉ)
```bash
# Terminal 1: Lancer l'app
cd C:\Users\jaleleddinekhadhraou\immobilier-scraper
python app.py

# Terminal 2: Ouvrir le menu
python open_browser.py
```

### Méthode 2: Directe
```bash
python app.py
# Puis aller à: http://localhost:5000/config
```

### Méthode 3: Docker
```bash
docker-compose up -d
# http://localhost:5000/config
```

---

## 📍 PAGE DE CONFIGURATION

### Lien Direct
```
http://localhost:5000/config
```

### Menu de Navigation
1. Cliquez sur **⚙️ Config** dans la barre
2. Voilà!

---

## 🌐 LIEN GITHUB

### Depuis l'Interface Web
**Footer** → Cliquez sur **GitHub Repository**

### URL Directe
```
https://github.com/jalel-khadhraoui/immobilier-scraper
```

---

## ⚙️ CONFIGURER LES PARAMÈTRES

### 1. Critères de Recherche
Modifiez:
- **Budget min/max:** 200k - 500k € (par défaut)
- **DPE max:** A à D (par défaut: D)
- **Surface min:** 30m² (par défaut)

### 2. Zones Géographiques
Cochez les zones à inclure:
- ✅ Paris 75
- ✅ Hauts-de-Seine 92
- ✅ Val-de-Marne 94
- + 3 autres zones disponibles

### 3. Email & Notifications
- Email de réception
- Mot de passe Gmail (app password)
- Heure du rapport quotidien
- Activer/Désactiver notifications

### 4. Cliquez "Enregistrer la configuration"
- Sauvegarde dans `data/user_config.json`
- Utilisé automatiquement pour les scrapes futurs!

---

## 📊 STATISTIQUES

### Database
- **Propriétés stockées:** Affichage en temps réel
- **Dernier scraping:** Timestamp
- **Actions:**
  - 🔧 Optimiser BD
  - 🗑️ Nettoyer doublons
  - 🔴 Réinitialiser (danger!)

---

## 📧 TESTER L'EMAIL
# Option 1: Menu interactif
python open_browser.py

# Option 2: Direct
python app.py
# Puis: http://localhost:5000/config

# Option 3: Docker
docker-compose up -d
1. Remplissez les paramètres email
2. Bouton: **"Envoyer un email de test"**
3. Vérifiez votre boîte

### Obtenir un mot de passe Gmail:
https://myaccount.google.com/apppasswords

---

## 🔗 REPOSITORY GITHUB

### Informations Complètes
```
Nom: immobilier-scraper
Propriétaire: jalel-khadhraoui
URL: https://github.com/jalel-khadhraoui/immobilier-scraper
Branche: master → main (À migrer)
```

### Documentation GitHub
- ✅ README principal
- ✅ Quick Start
- ✅ Guides complets
- ✅ API Documentation
- ✅ Deployment Guide

### À Faire
- [ ] Organiser depuis GitHub Web
- [ ] Ajouter des GitHub Actions
- [ ] Créer des releases
- [ ] Ajouter des issues templates

---

## 📱 UTILISATION COMPLÈTE

### Workflow Typique:

**Jour 1:**
```
1. Aller à /config
2. Définir budget (200k-600k)
3. Choisir zones (Paris, 92, 94)
4. Fixer DPE max (C)
5. Configurer email
6. Clicker "Enregistrer"
```

**Jour 2+:**
```
1. Dashboard → Scraper Maintenant
2. Voir les annonces filtrées
3. Modifier les statuts
4. Analyser les statistiques
5. Recevoir rapports email
```

---

## 🛠️ COMMANDES RAPIDES

### Ouvrir la page Config
```bash
python open_browser.py
# Puis sélectionner option 5
```

### Scraper depuis CLI
```bash
python main.py scrape seloger
```

### Voir les logs
```bash
tail -f logs/immobilier-scraper.log
```

### Réinitialiser DB
```bash
python admin.py reset_db
```

---

## 📚 FICHIERS IMPORTANTS

| Fichier | Rôle |
|---------|------|
| `app.py` | Application Flask principale |
| `config.py` | Configuration centrale |
| `templates/config.html` | Page configuration |
| `data/user_config.json` | Votre config sauvegardée |
| `Dockerfile` | Image Docker |

---

## ✨ NOUVEAUTÉS AJOUTÉES

### Commit 4 (Actuel)
```
✅ Page /config complète
✅ Endpoints API pour config
✅ Lien GitHub visible
✅ Documentation complète
✅ Script open_browser.py
```

### Commits Précédents
```
1. Initial commit: Base du projet
2. Documentation + Docker
3. Guides + Résumé projet
```

---

## 🎯 RÉSUMÉ RAPIDE

**Avant:** Scripts CLI uniquement
**Maintenant:** Interface web complète avec configuration!

**Pages Disponibles:**
- Dashboard (stats)
- Propriétés (list)
- Recherche (advanced)
- Sites (gestion)
- **Config ⚙️ (NOUVEAU)**
- Scheduler (auto)
- Statistics (charts)
- Logs (debug)
- **GitHub link**

---

## 🚀 COMMENCER

### 1. Lancer l'app
```bash
python app.py
```

### 2. Ouvrir le menu
```bash
python open_browser.py
```

### 3. Aller à Configuration
```
Option 5: ⚙️ Configuration
```

### 4. Configurer vos paramètres!

---

## 📞 SUPPORT

- **Interface:** http://localhost:5000/config
- **GitHub:** https://github.com/jalel-khadhraoui/immobilier-scraper
- **Email:** khadhraoui.jalel@gmail.com
- **Issues:** GitHub Issues

---

**Status: ✅ PRÊT À UTILISER!**

Tous les systèmes sont opérationnels.
Configuration personnalisable via web.
GitHub accessible depuis l'app.

**Bon scraping! 🎉**
