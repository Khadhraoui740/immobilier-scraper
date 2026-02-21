# Configuration des APIs Immobilières

## Vue d'ensemble

Le système a été restructuré pour fonctionner avec les **APIs officielles** des sites immobiliers plutôt que du scraping synthétique.

### Mode de fonctionnement actuel:
1. **DVF Open Data** ✅ Actif - Données publiques gratuites certifiées
2. **APIs SeLoger, PAP, LeBonCoin, BienIci** - À configurer avec vos clés

## Configuration des APIs

### 1. Obtenir les clés API

#### **LeBonCoin**
```
URL: https://developer.leboncoin.fr/
Documentation: https://developers.leboncoin.fr/docs
Démarches:
1. Créer un compte développeur
2. Demander accès à l'API immobilier
3. Générer une clé API
4. Ajouter dans .env: LEBONCOIN_API_KEY=votre_cle
```

#### **PAP** (De Particulier À Particulier)
```
URL: https://www.pap.fr/api
Documentation: https://www.pap.fr/api/documentation
Démarches:
1. Contacter PAP pour accès développeur
2. Obtenir une clé API
3. Ajouter dans .env: PAP_API_KEY=votre_cle
```

#### **SeLoger**
```
URL: https://api.seloger.com
Documentation: https://api.seloger.com/docs
Démarches:
1. Créer compte développeur SeLoger
2. Faire une demande d'accès API
3. Obtenir une clé API
4. Ajouter dans .env: SELOGER_API_KEY=votre_cle
```

#### **BienIci**
```
URL: https://api.bienici.com
Documentation: https://developers.bienici.com
Démarches:
1. Créer compte développeur
2. Demander accès à l'API
3. Obtenir une clé API
4. Ajouter dans .env: BIENICI_API_KEY=votre_cle
```

### 2. Configurer le fichier `.env`

Créer ou modifier le fichier `.env` à la racine du projet:

```env
# API Keys (optionnel - remplir avec vos clés si disponibles)
SELOGER_API_KEY=your_key_here
PAP_API_KEY=your_key_here
LEBONCOIN_API_KEY=your_key_here
BIENICI_API_KEY=your_key_here

# Mode de scraping (options: api, hybrid, fallback)
# - api: Utiliser uniquement les APIs
# - hybrid: APIs + fallback sur DVF si API échoue
# - fallback: Utiliser DVF comme source principale
SCRAPE_MODE=hybrid

# Email
EMAIL_PASSWORD=your_email_password

# Database
DATABASE_URL=sqlite:///database/immobilier.db
```

### 3. Redémarrer l'application

```bash
python app.py
```

## Architecture du système

```
┌─────────────────────────────────────┐
│ Application Immobilier Scraper      │
└────────────────┬────────────────────┘
                 │
        ┌────────▼────────┐
        │ API Orchestrator│
        └────────┬────────┘
                 │
    ┌────────────┼────────────┬──────────────┐
    │            │            │              │
    ▼            ▼            ▼              ▼
┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│SeLoger  │ │LeBonCoin │ │   PAP    │ │ BienIci  │
│ API     │ │   API    │ │   API    │ │   API    │
│ (if key)│ │  (if key)│ │ (if key) │ │ (if key) │
└─────────┘ └──────────┘ └──────────┘ └──────────┘

Fallback si pas de clés API:
    │
    ▼
┌──────────────────────┐
│  DVF Open Data       │
│  (Données publiques) │
│  (Toujours actif)    │
└──────────────────────┘
```

## États des APIs

```bash
# Vérifier les APIs disponibles
curl http://localhost:5000/api/status
```

Résultat attendu:
```json
{
  "seloger": false,      // true si clé configurée
  "pap": false,          // true si clé configurée
  "leboncoin": false,    // true si clé configurée
  "bienici": false,      // true si clé configurée
  "dvf_opendata": true   // Toujours vrai - source de fallback gratuite
}
```

## Mode de scraping

### Mode `fallback` (Recommandé)
- Utilise DVF Open Data (gratuit, public)
- Ajoute les APIs officielles dès que les clés sont configurées
- Pas de dépendances externes

### Mode `hybrid`
- Tente les APIs en premier
- Fallback sur DVF si l'API échoue
- Nécessite des clés API pour un meilleur résultat

### Mode `api`
- Utilise uniquement les APIs
- Nécessite les clés API pour chaque site
- Meilleure couverture et fraîcheur des données

## Avantages de cette approche

✅ **Légal**: Utilise des APIs officielles
✅ **Fiable**: Sources certifiées (gouvernement pour DVF)
✅ **Rapide**: APIs au lieu du web scraping
✅ **Flexible**: Fonctionne sans clés API (utilise DVF)
✅ **Extensible**: Ajouter les clés API quand disponibles
✅ **Sécurisé**: Pas de scraping de sites
✅ **À jour**: Données actualisées en temps réel

## Prochaines étapes

1. Demander les clés API aux sites (processus peut prendre quelques jours)
2. Ajouter les clés au fichier `.env`
3. Changez `SCRAPE_MODE=api` une fois toutes les clés disponibles
4. Le système est maintenant production-ready!

## Dépannage

**"API not configured for SeLoger"**
→ Ajouter `SELOGER_API_KEY=...` au `.env`

**"DVF data is stale"**
→ Les données publiques DVF sont mises à jour régulièrement
→ Ajouter les clés API pour les données real-time

**"API returned 403 Forbidden"**
→ Clé API invalide ou API rejette les requests
→ Vérifier les headers de la request
→ Consulter la documentation de l'API
