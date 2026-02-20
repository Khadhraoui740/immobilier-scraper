# API Documentation - Scraping Immobilier

## Base URL
```
http://localhost:5000
```

---

## 📑 Table des Matières

1. [Scraping](#scraping)
2. [Recherche](#recherche)
3. [Propriétés](#propriétés)
4. [Sites/Scrapers](#sitesscrapers)
5. [Planificateur](#planificateur)
6. [Statistiques](#statistiques)
7. [Alertes](#alertes)
8. [Codes d'erreur](#codes-derreur)

---

## Scraping

### Lancer un scraping
**Endpoint:** `POST /api/scrape`

**Description:** Lance le scraping immédiat sur les sources spécifiées

**Body:**
```json
{
  "source": "all"
}
```

**Parameters:**
- `source` (string): `all`, `seloger`, `pap`, `leboncoin`, ou `bienici`

**Response (200):**
```json
{
  "success": true,
  "message": "Scraping lancé avec succès",
  "source": "all",
  "count": 25,
  "new": 8,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"source": "seloger"}'
```

---

## Recherche

### Recherche avancée
**Endpoint:** `POST /api/search`

**Description:** Recherche les propriétés avec filtres

**Body:**
```json
{
  "price_min": 200000,
  "price_max": 500000,
  "dpe_max": "D",
  "location": "75",
  "status": "disponible"
}
```

**Parameters:**
- `price_min` (integer, optional): Prix minimum
- `price_max` (integer, optional): Prix maximum
- `dpe_max` (string, optional): DPE max (A-G)
- `location` (string, optional): Code postal ou zone
- `status` (string, optional): Statut (disponible, contacté, visité, rejeté, acheté)

**Response (200):**
```json
{
  "success": true,
  "count": 15,
  "properties": [
    {
      "id": 1,
      "title": "Appartement 2 pièces",
      "price": 350000,
      "surface": 55,
      "rooms": 2,
      "dpe": "C",
      "source": "SeLoger",
      "location": "75001",
      "url": "https://...",
      "status": "disponible",
      "scrape_date": "2024-01-15T10:30:45"
    }
  ]
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "price_max": 500000,
    "dpe_max": "D",
    "location": "75"
  }'
```

---

## Propriétés

### Obtenir une propriété
**Endpoint:** `GET /api/property/<id>`

**Response (200):**
```json
{
  "success": true,
  "property": {
    "id": 1,
    "title": "Appartement 2 pièces",
    "price": 350000,
    "surface": 55,
    "rooms": 2,
    "dpe": "C",
    "source": "SeLoger",
    "location": "75001",
    "url": "https://...",
    "status": "disponible",
    "description": "Belle vue, proximité métro...",
    "image_url": "https://...",
    "scrape_date": "2024-01-15T10:30:45",
    "created_at": "2024-01-15T10:30:45",
    "updated_at": "2024-01-15T10:30:45"
  }
}
```

### Mettre à jour une propriété
**Endpoint:** `POST /api/property/<id>`

**Body:**
```json
{
  "status": "visité",
  "notes": "À revoir"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Propriété mise à jour",
  "property": {...}
}
```

### Supprimer une propriété
**Endpoint:** `DELETE /api/property/<id>`

**Response (200):**
```json
{
  "success": true,
  "message": "Propriété supprimée"
}
```

---

## Sites/Scrapers

### Lister les sites
**Endpoint:** `GET /api/sites`

**Response (200):**
```json
{
  "success": true,
  "sites": [
    {
      "id": "seloger",
      "name": "SeLoger",
      "url": "https://www.seloger.com/acheter/",
      "enabled": true,
      "timeout": 30,
      "last_run": "2024-01-15T10:30:45",
      "properties_count": 125
    },
    {
      "id": "bienici",
      "name": "BienIci",
      "url": "https://www.bienici.com/annonces/achat/",
      "enabled": true,
      "timeout": 30,
      "last_run": "2024-01-15T09:30:45",
      "properties_count": 89
    }
  ]
}
```

### Activer/Désactiver un site
**Endpoint:** `PUT /api/sites/<id>`

**Body:**
```json
{
  "enabled": false
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "SeLoger a été désactivé"
}
```

### Ajouter un nouveau site
**Endpoint:** `POST /api/sites/new`

**Body:**
```json
{
  "id": "immoweb",
  "name": "ImmoWeb",
  "url": "https://www.immoweb.be/en/search",
  "timeout": 30,
  "enabled": true
}
```

**Parameters:**
- `id` (string, required): Identifiant unique
- `name` (string, required): Nom du site
- `url` (string, required): URL de base
- `timeout` (integer, optional): Timeout en secondes (défaut: 30)
- `enabled` (boolean, optional): Activé par défaut (défaut: true)

**Response (201):**
```json
{
  "success": true,
  "message": "Site 'ImmoWeb' ajouté avec succès",
  "site": {
    "id": "immoweb",
    "name": "ImmoWeb",
    "url": "https://www.immoweb.be/en/search",
    "enabled": true,
    "timeout": 30
  }
}
```

---

## Planificateur

### Obtenir l'état du planificateur
**Endpoint:** `GET /api/scheduler/status`

**Response (200):**
```json
{
  "running": true,
  "last_run": "2024-01-15T08:30:45",
  "next_run": "2024-01-15T12:30:45",
  "interval_hours": 2,
  "total_runs": 45,
  "history": [
    {
      "timestamp": "2024-01-15T08:30:45",
      "duration_seconds": 125,
      "properties_found": 8,
      "success": true
    }
  ]
}
```

### Démarrer le planificateur
**Endpoint:** `POST /api/scheduler/start`

**Response (200):**
```json
{
  "success": true,
  "message": "Planificateur démarré",
  "next_run": "2024-01-15T12:30:45"
}
```

### Arrêter le planificateur
**Endpoint:** `POST /api/scheduler/stop`

**Response (200):**
```json
{
  "success": true,
  "message": "Planificateur arrêté"
}
```

### Mettre à jour la configuration du planificateur
**Endpoint:** `PUT /api/scheduler/config`

**Body:**
```json
{
  "interval_hours": 4,
  "report_time": "09:00",
  "notifications_enabled": true
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Configuration mise à jour",
  "config": {...}
}
```

---

## Statistiques

### Obtenir les statistiques
**Endpoint:** `GET /api/stats`

**Response (200):**
```json
{
  "success": true,
  "stats": {
    "total_properties": 425,
    "new_today": 8,
    "new_this_week": 42,
    "by_source": {
      "SeLoger": 125,
      "PAP": 95,
      "LeBonCoin": 110,
      "BienIci": 95
    },
    "by_status": {
      "disponible": 350,
      "contacté": 45,
      "visité": 25,
      "rejeté": 5
    },
    "by_dpe": {
      "A": 15,
      "B": 45,
      "C": 125,
      "D": 142,
      "E": 73,
      "F": 20,
      "G": 5
    },
    "price_stats": {
      "min": 150000,
      "max": 750000,
      "average": 380000,
      "median": 350000
    },
    "last_update": "2024-01-15T10:30:45"
  }
}
```

---

## Alertes

### Tester les notifications email
**Endpoint:** `POST /api/alerts/test`

**Response (200):**
```json
{
  "success": true,
  "message": "Email de test envoyé à khadhraoui.jalel@gmail.com",
  "timestamp": "2024-01-15T10:30:45"
}
```

### Configurer les alertes
**Endpoint:** `PUT /api/alerts/config`

**Body:**
```json
{
  "email": "user@example.com",
  "min_new_properties": 1,
  "daily_report": true,
  "report_time": "09:00"
}
```

---

## Codes d'erreur

### Success (2xx)
- **200 OK**: Requête réussie
- **201 Created**: Ressource créée
- **204 No Content**: Requête réussie, pas de contenu

### Client Errors (4xx)
- **400 Bad Request**: Paramètres invalides
- **404 Not Found**: Ressource non trouvée
- **409 Conflict**: Conflit (e.g., site déjà existant)

### Server Errors (5xx)
- **500 Internal Server Error**: Erreur serveur
- **503 Service Unavailable**: Service indisponible

### Format d'erreur
```json
{
  "success": false,
  "error": "Description de l'erreur",
  "details": "Détails supplémentaires",
  "timestamp": "2024-01-15T10:30:45"
}
```

---

## Authentification

Actuellement, l'API est ouverte. Pour une version de production:
- Ajouter une authentification JWT
- Implémenter des rôles d'utilisateur
- Limiter les taux de requête

---

## Versions

- **Version actuelle**: 1.0.0
- **Date de création**: 2024-01-15
- **Maintenu par**: Jalel Khadhraoui

---

## Exemples de scripts

### Python - Requests
```python
import requests
import json

BASE_URL = "http://localhost:5000"

# Lancer un scraping
response = requests.post(
    f"{BASE_URL}/api/scrape",
    json={"source": "all"}
)
print(response.json())

# Rechercher des propriétés
response = requests.post(
    f"{BASE_URL}/api/search",
    json={
        "price_max": 500000,
        "dpe_max": "D"
    }
)
print(f"Trouvé {response.json()['count']} propriétés")
```

### JavaScript - Fetch
```javascript
// Lancer un scraping
fetch('http://localhost:5000/api/scrape', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({source: 'all'})
})
.then(r => r.json())
.then(data => console.log(data));

// Rechercher
fetch('http://localhost:5000/api/search', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    price_max: 500000,
    dpe_max: 'D'
  })
})
.then(r => r.json())
.then(data => console.log(data.properties));
```

### cURL
```bash
# Scraper tous les sites
curl -X POST http://localhost:5000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"source": "all"}'

# Rechercher avec filtres
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "price_max": 500000,
    "dpe_max": "D",
    "location": "75"
  }'
```
