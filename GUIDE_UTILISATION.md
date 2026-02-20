# 📖 GUIDE D'UTILISATION - Configuration et Scraping

## 🎯 Comment Utiliser le Système de Configuration

### 1️⃣ Access la Page de Configuration
```
http://localhost:5000/config
```

### 2️⃣ Modifier les Paramètres de Recherche

**Budget**
- Budget Minimum: Ex. 200,000€ → 300,000€
- Budget Maximum: Ex. 500,000€ → 700,000€

**Efficacité Énergétique (DPE)**
- Sélectionnez le DPE maximum accepté (A à G)
- G = inclut tous les biens (moins exigeant)
- A = seulement très efficaces (plus exigeant)

**Localisation**
- Cochez/décochez les zones de recherche
- Options: Paris, Hauts-de-Seine, Val-de-Marne, Essonne, Seine-et-Marne, Yvelines

**Surface**
- Surface Minimale (m²): Ex. 30 → 50

### 3️⃣ Sauvegarder la Configuration
```
Cliquez le bouton "Enregistrer la configuration"
```
✅ Les paramètres sont sauvegardés en `data/user_config.json`

---

## 🔄 Lancer le Scraping

### Option A: Via l'Interface Web
1. Allez sur http://localhost:5000/search
2. Cliquez "Scraper tout" ou sélectionnez une source
3. Les annonces s'ajoutent automatiquement

### Option B: Via Ligne de Commande
```bash
python scrape_live.py
```

### Option C: Scheduler Automatique
1. Allez sur http://localhost:5000/scheduler
2. Configurer l'intervalle de scraping (toutes les 2 heures, etc.)
3. Activer le scheduler

---

## 📊 Vérifier les Résultats

### Dashboard
```
http://localhost:5000
```
Affiche:
- Total d'annonces
- Prix moyen
- Nouvelles annonces (dernières 24h)
- Statistiques par source/statut

### Liste des Propriétés
```
http://localhost:5000/properties
```
- Tableau complet des annonces
- Filtrage par prix, DPE, location, statut
- Actions: marquer comme contacté, visité, etc.

### Statistiques Détaillées
```
http://localhost:5000/statistics
```
- Graphiques et analyses
- Prix min/max
- Répartition par source

---

## 🧪 Test Complet (End-to-End)

Pour valider que tout fonctionne:

```bash
# Exécuter le test complet
python test_config_end_to_end.py
```

Ce test:
1. ✅ Nettoie la BD
2. ✅ Scrape avec config originale
3. ✅ Modifie la configuration
4. ✅ Scrape avec nouvelle config
5. ✅ Valide que les résultats changent

---

## 📈 Flux Complete

```
┌─────────────────┐
│  Page Config    │  ← Modifiez les paramètres
│  /config        │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ user_config.json│  ← Sauvegardé automatiquement
│ data/           │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Scraping        │  ← Utilise les nouveaux paramètres
│ /api/scrape     │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Base de données │  ← 12 annonces (avec nouveaux filtres)
│ immobilier.db   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Dashboard       │  ← Statistiques mises à jour
│ /               │
└─────────────────┘
```

---

## 🔍 Dépannage

### Les résultats ne changent pas après modification

**Cause:** Scraping avec anciens paramètres

**Solution:**
1. Allez à `/config`
2. Vérifiez les paramètres affichés
3. Cliquez "Enregistrer la configuration"
4. Relancez le scraping

### Erreur "Configuration non trouvée"

**Solution:**
```bash
python test_config_end_to_end.py
```
Cela réinitialise les fichiers de config.

### Annonces dupliquées

**Solution:**
1. Allez à `/config`
2. Cliquez "Nettoyer doublons"
3. Relancez le scraping

---

## 📊 Exemple Complet

### Avant
```
Budget: 200,000€ - 500,000€
Premier scraping: 12 annonces
Prix moyen: 364,745€
```

### Modification
```
Budget: 300,000€ - 700,000€
```

### Après
```
Deuxième scraping: 12 annonces
Prix moyen: 560,851€ ⬆️
```

✅ **Les résultats changent bien!**

---

## 🎉 Système Opérationnel

Le système est **entièrement fonctionnel** et prêt pour:
- ✅ Configuration dynamique
- ✅ Scraping répétable
- ✅ Historique des annonces
- ✅ Notification par email
- ✅ Planification automatique

Commencez par la page `/config` et profitez! 🚀
