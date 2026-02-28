# 📊 GUIDE COMPLET - 12 GRAPHIQUES POWER BI

## 🎯 OBJECTIF
Créer un rapport Power BI complet avec **12 visualisations** interactives pour analyser les communes d'Île-de-France.

---

## 📋 ÉTAPES À SUIVRE

### ✅ ÉTAPE 1️⃣  - IMPORTER LES DONNÉES CSV

```
Home → Get Data → CSV
Choisir: exports/synthese_communes.csv
Cliquer: Load
```

**Vérification:** Vous devez voir 41 communes chargées

---

### ✅ ÉTAPE 2️⃣  - KPI 1: NOMBRE DE COMMUNES

**Type:** Card  
**Chemin:** Home → New Visual → Card  
**Configuration:**
- Drag 'commune' → Value field
- Titre: "Communes Analysées"
- Position: Haut gauche

**Résultat attendu:** 41

---

### ✅ ÉTAPE 3️⃣  - KPI 2: PRIX MOYEN

**Type:** Card  
**Chemin:** Home → New Visual → Card  
**Configuration:**
- Drag 'prix_moyen' → Value field  
- Format: Devise EUR
- Titre: "Prix Moyen"
- Position: Haut centre

**Résultat attendu:** ≈ 285,649€

---

### ✅ ÉTAPE 4️⃣  - BAR CHART: Prix par Commune

**Type:** Column Chart  
**Chemin:** Home → New Visual → Column Chart  
**Configuration:**
- Axis: Drag 'commune'
- Value: Drag 'prix_moyen'
- Sort: By prix_moyen (desc)
- Titre: "Prix Moyen par Commune"
- Position: Moitié gauche

**Résultat attendu:** Poissy en #1, Lagny-sur-Marne en #2

---

### ✅ ÉTAPE 5️⃣  - SCATTER PLOT: Prix M² vs Total

**Type:** Scatter Chart  
**Chemin:** Home → New Visual → Scatter  
**Configuration:**
- X Axis: Drag 'prix_m2'
- Y Axis: Drag 'prix_moyen'
- Details: Drag 'commune'
- Titre: "Analyse Prix au M² vs Prix Total"
- Position: Moitié droite

**Résultat attendu:** Nuage de points montrant la corrélation

---

### ✅ ÉTAPE 6️⃣  - TABLE: Détails Complets

**Type:** Table  
**Chemin:** Home → New Visual → Table  
**Configuration:**
- Colonnes:
  - commune
  - prix_moyen
  - prix_min
  - prix_max
  - prix_m2
- Sort: By prix_moyen (asc)
- Titre: "Détail des Communes"

**Résultat attendu:** 41 lignes avec tous les détails

---

### ✅ ÉTAPE 7️⃣  - SLICER: Filtre Interactif

**Type:** Slicer  
**Chemin:** Home → New Visual → Slicer  
**Configuration:**
- Field: Drag 'commune'
- Style: List ou Dropdown
- Position: Haut (au-dessus des graphiques)

**Effet:** Cliquez une commune → Tous les graphiques se mettent à jour!

---

### ✅ ÉTAPE 8️⃣  - KPI 3: Communes Accessibles

**Type:** Card  
**Chemin:** Home → New Visual → Card  
**Configuration:**
- Drag 'commune' → Value
- Appliquez un filtre: prix_moyen <= 130000
- Titre: "Communes ≤ 130k"
- Position: Haut droit

**Résultat attendu:** 6

---

### ✅ ÉTAPE 9️⃣  - LINE CHART: Progression des Prix

**Type:** Line Chart  
**Chemin:** Home → New Visual → Line  
**Configuration:**
- X Axis: Drag 'commune'
- Y Axis: Drag 'prix_moyen'
- Sort: By prix_moyen
- Titre: "Classement des Communes"

**Résultat attendu:** Courbe ascendante montrant l'augmentation des prix

---

### ✅ ÉTAPE 1️⃣0️⃣  - DONUT CHART: Distribution Budget

**Type:** Donut Chart  
**Chemin:** Home → New Visual → Donut  
**Configuration:**
- Legend: Drag 'commune' (filter < 130k)
- Value: Drag 'prix_moyen'
- Titre: "Distribution Communes Accessibles"

**Résultat attendu:** 6 communes visibles, leurs parts de budget

---

### ✅ ÉTAPE 1️⃣1️⃣  - MATRIX: Comparaison Détaillée

**Type:** Matrix/Heatmap  
**Chemin:** Home → New Visual → Matrix  
**Configuration:**
- Rows: Drag 'commune'
- Values: 
  - prix_moyen
  - prix_min
  - prix_max
  - prix_m2
- Format conditionnel: Activez (rouge=cher, vert=bon marché)
- Titre: "Matrice de Comparaison"

**Résultat attendu:** Vue d'ensemble avec code couleur

---

### ✅ ÉTAPE 1️⃣2️⃣  - GAUGE: Indicateur Budget

**Type:** Gauge  
**Chemin:** Home → New Visual → Gauge  
**Configuration:**
- Value: 103651 (prix Poissy)
- Target: 130000 (votre budget)
- Titre: "Utilisation Budget (Poissy)"

**Résultat attendu:** Jauge montrant 79% d'utilisation

---

## 📐 LAYOUT RECOMMANDÉ

```
┌────────────────────────────────────────────────────────┐
│  KPI 1      KPI 2         KPI 3       GAUGE          │
│  (41)     (285k€)        (6)         (79%)            │
├────────────────────────────────────────────────────────┤
│          ▼ SLICER: Sélectionnez une commune ▼         │
├────────────────────────────────────────────────────────┤
│  BAR CHART              │  SCATTER PLOT              │
│  (Prix/Commune)         │  (Prix M² vs Total)        │
├────────────────────────────────────────────────────────┤
│  TABLE - Détails Complets (41 communes)              │
├────────────────────────────────────────────────────────┤
│  LINE CHART     DONUT CHART    MATRIX                 │
│  (Progression)  (Distribution)  (Comparaison)         │
└────────────────────────────────────────────────────────┘
```

---

## 💾 ENREGISTREMENT

Quand tous les graphiques sont prêts:

```
File → Save (Ctrl+S)
OU
File → Export as PDF/Image
```

---

## 🎯 VÉRIFICATION FINALE

✅ 3 KPI cards (totaux)  
✅ 1 Bar Chart (prix)  
✅ 1 Scatter Plot (analyse)  
✅ 1 Table (détails)  
✅ 1 Slicer (filtre)  
✅ 1 Line Chart (progression)  
✅ 1 Donut Chart (distribution)  
✅ 1 Gauge (budget)  
✅ 1 Matrix (comparaison)  

**TOTAL: 12 Visualisations interactives!**

---

## 💡 ASTUCES POWER BI

### Lier les graphiques
- Tous les graphiques sont **automatiquement liés** si vous utilisez le même Field
- Cliquez une commune dans le Slicer → Tous se mettent à jour

### Format personnalisé
- Right-click sur visual → Format
- Couleurs, polices, tailles d'étiquettes

### Drill-down
- Double-cliquez un graphique pour zoomer

### Actualiser les données
- File → Options → Data source → Refresh

---

## 📞 SUPPORT

Si un graphique ne fonctionne pas:
1. Vérifiez que les données CSV sont chargées (`Home → Edit Queries`)
2. Vérifiez que les colonnes sont du bon type (numeric, text, etc.)
3. Supprimez le visuel et recommencez

---

**C'est tout! Vous avez un rapport analytique professionnel complètement fonctionnel! 🎉**
