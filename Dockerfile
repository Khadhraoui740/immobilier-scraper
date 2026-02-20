FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Créer les répertoires nécessaires
RUN mkdir -p logs database data

# Variables d'environnement
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Port
EXPOSE 5000

# Commande de démarrage
CMD ["python", "app.py"]
