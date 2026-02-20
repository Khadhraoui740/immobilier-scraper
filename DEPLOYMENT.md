# Scraping Immobilier - Guide de Déploiement

## 🚀 Déploiement Local

### Prérequis
- Python 3.8+
- pip
- Git

### Installation
```bash
# Cloner le repository
git clone https://github.com/jalel-khadhraoui/immobilier-scraper.git
cd immobilier-scraper

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Activer l'environnement (Linux/Mac)
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos paramètres
```

### Lancer l'application
```bash
python app.py
```

L'application est accessible à: http://localhost:5000

---

## 🐳 Déploiement Docker

### Avec Docker
```bash
# Construire l'image
docker build -t immobilier-scraper .

# Lancer le conteneur
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/database:/app/database \
  -e EMAIL_PASSWORD=your_password \
  --name immobilier-scraper \
  immobilier-scraper
```

### Avec Docker Compose
```bash
# Démarrer
docker-compose up -d

# Voir les logs
docker-compose logs -f web

# Arrêter
docker-compose down
```

---

## ☁️ Déploiement sur Heroku

### Prérequis
- Compte Heroku
- Heroku CLI installé

### Étapes
```bash
# Se connecter à Heroku
heroku login

# Créer une nouvelle application
heroku create immobilier-scraper

# Ajouter le fichier Procfile
echo "web: python app.py" > Procfile

# Configurer les variables d'environnement
heroku config:set EMAIL_PASSWORD=your_password
heroku config:set FLASK_ENV=production

# Déployer
git push heroku main

# Voir les logs
heroku logs --tail

# Arrêter les dynos si nécessaire
heroku ps:scale web=1
```

---

## 🖥️ Déploiement sur VPS (Ubuntu)

### Installation initiale
```bash
# Mettre à jour le système
sudo apt-get update && sudo apt-get upgrade -y

# Installer Python et pip
sudo apt-get install python3.11 python3.11-venv python3.11-dev -y

# Installer supervisor pour la gestion des processus
sudo apt-get install supervisor -y

# Cloner le repository
cd /home/username
git clone https://github.com/jalel-khadhraoui/immobilier-scraper.git
cd immobilier-scraper

# Créer l'environnement virtuel
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration Supervisor
```bash
# Créer le fichier de configuration
sudo nano /etc/supervisor/conf.d/immobilier-scraper.conf
```

**Contenu du fichier:**
```ini
[program:immobilier-scraper]
directory=/home/username/immobilier-scraper
command=/home/username/immobilier-scraper/venv/bin/python app.py
user=username
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/username/immobilier-scraper/logs/supervisor.log
environment=FLASK_ENV=production,EMAIL_PASSWORD=your_password
```

### Activation
```bash
# Recharger la configuration
sudo supervisorctl reread
sudo supervisorctl update

# Démarrer le service
sudo supervisorctl start immobilier-scraper

# Vérifier le statut
sudo supervisorctl status
```

### Configuration Nginx (Reverse Proxy)
```bash
# Créer la configuration Nginx
sudo nano /etc/nginx/sites-available/immobilier-scraper
```

**Contenu:**
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/immobilier-scraper /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL avec Let's Encrypt
```bash
# Installer certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Obtenir le certificat
sudo certbot --nginx -d example.com

# Renouvellement automatique
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## 📊 Sauvegarde et Restauration

### Sauvegarde automatique
```bash
# Cron job pour sauvegarder la BD tous les jours à 2h du matin
0 2 * * * /home/username/immobilier-scraper/backup.sh
```

**backup.sh:**
```bash
#!/bin/bash
BACKUP_DIR="/home/username/immobilier-scraper/database/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
cp /home/username/immobilier-scraper/database/immobilier.db "$BACKUP_DIR/immobilier_$TIMESTAMP.db"
# Supprimer les sauvegardes de plus de 30 jours
find "$BACKUP_DIR" -name "*.db" -mtime +30 -delete
```

### Restauration
```bash
python admin.py restore database/backups/immobilier_20240115_020000.db
```

---

## 📈 Monitoring

### Health Check
```bash
# Vérifier que l'application fonctionne
curl http://localhost:5000/

# Vérifier le statut de la BD
python -c "from database import Database; db = Database(); print(db.get_statistics())"
```

### Logs
```bash
# Voir les logs en temps réel
tail -f logs/app.log

# Voir les erreurs
tail -f logs/error.log

# Archiver les anciennes logs
gzip logs/app.*.log
```

### Alertes
Pour être notifié des erreurs:
1. Configurer les emails dans `.env`
2. Activer les notifications dans l'interface web
3. Les erreurs déclencheront automatiquement des emails

---

## 🔧 Variables d'environnement (.env)

```env
# Email
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_ADDRESS=khadhraoui.jalel@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Flask
FLASK_ENV=production
SECRET_KEY=your_secret_key

# Database
DATABASE_URL=sqlite:///database/immobilier.db

# Logging
LOG_LEVEL=INFO
```

---

## 🐛 Dépannage

### "Address already in use"
```bash
# Trouver le processus utilisant le port 5000
lsof -i :5000

# Tuer le processus
kill -9 <PID>
```

### Erreur de base de données
```bash
# Réinitialiser la base de données
python
>>> from database import Database
>>> db = Database()
>>> db.init_db()
>>> exit()
```

### Scrapers qui ne fonctionnent pas
1. Vérifier la connexion internet
2. Vérifier les logs: `tail -f logs/app.log`
3. Redémarrer l'application
4. Tester manuellement: `python main.py`

---

## 🔒 Sécurité

### Recommandations
1. ✅ Changer le SECRET_KEY à chaque déploiement
2. ✅ Utiliser HTTPS en production
3. ✅ Mettre à jour régulièrement les dépendances
4. ✅ Limiter l'accès à l'interface admin
5. ✅ Sauvegarder régulièrement la base de données
6. ✅ Monitorer les logs pour les anomalies

### Update des dépendances
```bash
# Vérifier les mises à jour disponibles
pip list --outdated

# Mettre à jour
pip install --upgrade -r requirements.txt
```

---

## 📞 Support

- **Email**: khadhraoui.jalel@gmail.com
- **GitHub**: https://github.com/jalel-khadhraoui/immobilier-scraper
- **Issues**: https://github.com/jalel-khadhraoui/immobilier-scraper/issues
