"""
Génération de visualisations pour rapport Power BI
Crée des graphiques à partir des données immobilier
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Configuration matplotlib
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Charger les données
df_properties = pd.read_csv('exports/proprietes_immobilier.csv')
df_communes = pd.read_csv('exports/analyse_communes.csv')

# Créer dossier pour les images
import os
os.makedirs('exports/visualisations', exist_ok=True)

print("Génération des visualisations...")
print()

# ============================================================================
# VIZ 1: TOP 10 COMMUNES - Budget 130k
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 6))

budget = 130000
top_communes = df_communes[df_communes['Prix Min'] <= budget].nsmallest(10, 'Prix Moyen')

colors = plt.cm.RdYlGn_r(np.linspace(0.3, 0.7, len(top_communes)))
bars = ax.barh(top_communes['Commune'], top_communes['Prix Moyen'], color=colors)

# Ajouter valeurs sur les barres
for i, (commune, prix) in enumerate(zip(top_communes['Commune'], top_communes['Prix Moyen'])):
    ax.text(prix + 1000, i, f"{prix:,.0f} EUR", va='center', fontsize=9)

ax.axvline(x=budget, color='red', linestyle='--', linewidth=2, label=f'Budget max: {budget:,} EUR')
ax.set_xlabel('Prix Moyen (EUR)', fontsize=11, fontweight='bold')
ax.set_title('TOP 10 Communes Accessibles avec Budget 130k EUR\n(Prix moyen et budget maximum)', 
             fontsize=13, fontweight='bold', pad=20)
ax.legend()
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('exports/visualisations/01_top10_communes_130k.png', dpi=300, bbox_inches='tight')
print("✓ Visualisation 1: TOP 10 communes créée")
plt.close()

# ============================================================================
# VIZ 2: MEILLEUR RAPPORT QUALITÉ/PRIX
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 7))

budget_communes = df_communes[df_communes['Prix Min'] <= budget]

scatter = ax.scatter(budget_communes['Prix Moyen'], 
                     budget_communes['Prix/m2'],
                     s=budget_communes['Nombre Annonces'] * 100,  # Taille = nb annonces
                     alpha=0.6,
                     c=budget_communes['Prix/m2'],
                     cmap='viridis',
                     edgecolors='black',
                     linewidth=1)

# Ajouter labels pour les meilleures communes
for idx, row in budget_communes.nsmallest(5, 'Prix/m2').iterrows():
    ax.annotate(row['Commune'], 
                (row['Prix Moyen'], row['Prix/m2']),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=9,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))

ax.set_xlabel('Prix Moyen (EUR)', fontsize=11, fontweight='bold')
ax.set_ylabel('Prix au m² (EUR/m²)', fontsize=11, fontweight='bold')
ax.set_title('Rapport Qualité-Prix par Commune\n(Taille = Nombre d\'annonces)', 
             fontsize=13, fontweight='bold', pad=20)

cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Prix/m²', fontsize=10)

ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('exports/visualisations/02_qualite_prix.png', dpi=300, bbox_inches='tight')
print("✓ Visualisation 2: Qualité-Prix créée")
plt.close()

# ============================================================================
# VIZ 3: DISTRIBUTION DES PRIX
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 6))

ax.hist(df_communes['Prix Moyen'], bins=15, color='steelblue', edgecolor='black', alpha=0.7)
ax.axvline(x=130000, color='red', linestyle='--', linewidth=2, label='Budget max: 130k EUR', )
ax.axvline(x=df_communes['Prix Moyen'].mean(), color='orange', linestyle='--', linewidth=2, 
           label=f'Moyenne: {df_communes["Prix Moyen"].mean():,.0f} EUR')

ax.set_xlabel('Prix Moyen (EUR)', fontsize=11, fontweight='bold')
ax.set_ylabel('Nombre de Communes', fontsize=11, fontweight='bold')
ax.set_title('Distribution des Prix Moyens par Commune', 
             fontsize=13, fontweight='bold', pad=20)
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('exports/visualisations/03_distribution_prix.png', dpi=300, bbox_inches='tight')
print("✓ Visualisation 3: Distribution des prix créée")
plt.close()

# ============================================================================
# VIZ 4: TOP 10 MEILLEUR RAPPORT QUALITÉ/PRIX
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 6))

top_ratio = df_communes[df_communes['Prix Min'] <= budget].nsmallest(10, 'Prix/m2')
colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(top_ratio)))

bars = ax.barh(top_ratio['Commune'], top_ratio['Prix/m2'], color=colors)

for i, (commune, ratio) in enumerate(zip(top_ratio['Commune'], top_ratio['Prix/m2'])):
    ax.text(ratio + 50, i, f"{ratio:,.0f} EUR/m²", va='center', fontsize=9)

ax.set_xlabel('Prix par m² (EUR/m²)', fontsize=11, fontweight='bold')
ax.set_title('TOP 10 Communes - Meilleur Rapport Qualité-Prix (€/m²)', 
             fontsize=13, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('exports/visualisations/04_top10_ratio_prix.png', dpi=300, bbox_inches='tight')
print("✓ Visualisation 4: TOP 10 ratio créée")
plt.close()

# ============================================================================
# VIZ 5: PRIX MIN-MAX PAR COMMUNE
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 8))

top_communes_full = df_communes[df_communes['Prix Min'] <= budget].nsmallest(12, 'Prix Moyen')
communes = top_communes_full['Commune'].values
prix_min = top_communes_full['Prix Min'].values
prix_max = top_communes_full['Prix Max'].values
prix_moy = top_communes_full['Prix Moyen'].values

x = np.arange(len(communes))
width = 0.25

bars1 = ax.bar(x - width, prix_min, width, label='Prix Min', alpha=0.8)
bars2 = ax.bar(x, prix_moy, width, label='Prix Moyen', alpha=0.8)
bars3 = ax.bar(x + width, prix_max, width, label='Prix Max', alpha=0.8)

ax.axhline(y=130000, color='red', linestyle='--', linewidth=2, label='Budget: 130k EUR')

ax.set_xlabel('Commune', fontsize=11, fontweight='bold')
ax.set_ylabel('Prix (EUR)', fontsize=11, fontweight='bold')
ax.set_title('Gamme de Prix par Commune (Min - Moyen - Max)', 
             fontsize=13, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(communes, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('exports/visualisations/05_prix_minmaxmoy.png', dpi=300, bbox_inches='tight')
print("✓ Visualisation 5: Prix Min-Max créée")
plt.close()

# ============================================================================
# VIZ 6: NOMBRE D'ANNONCES PAR COMMUNE
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 6))

annonces = df_communes.nlargest(15, 'Nombre Annonces')
colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(annonces)))

bars = ax.bar(annonces['Commune'], annonces['Nombre Annonces'], color=colors, edgecolor='black')

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_ylabel('Nombre d\'Annonces', fontsize=11, fontweight='bold')
ax.set_title('TOP 15 Communes - Nombre d\'Annonces', 
             fontsize=13, fontweight='bold', pad=20)
ax.set_xticklabels(annonces['Commune'], rotation=45, ha='right')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('exports/visualisations/06_nombre_annonces.png', dpi=300, bbox_inches='tight')
print("✓ Visualisation 6: Nombre annonces créée")
plt.close()

# ============================================================================
# VIZ 7: TABLEAU SYNTHÈSE
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 10))
ax.axis('tight')
ax.axis('off')

summary = df_communes[df_communes['Prix Min'] <= budget].head(15)[
    ['Commune', 'Nombre Annonces', 'Prix Moyen', 'Prix Min', 'Prix Max', 'Prix/m2']
].copy()

summary['Prix Moyen'] = summary['Prix Moyen'].apply(lambda x: f"{x:,.0f}")
summary['Prix Min'] = summary['Prix Min'].apply(lambda x: f"{x:,.0f}")
summary['Prix Max'] = summary['Prix Max'].apply(lambda x: f"{x:,.0f}")
summary['Prix/m2'] = summary['Prix/m2'].apply(lambda x: f"{x:,.0f}")

table = ax.table(cellText=summary.values, 
                colLabels=summary.columns,
                cellLoc='center',
                loc='center',
                colWidths=[0.25, 0.12, 0.12, 0.12, 0.12, 0.12])

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2)

# Style header
for i in range(len(summary.columns)):
    table[(0, i)].set_facecolor('#4472C4')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style alternating rows
for i in range(1, len(summary) + 1):
    for j in range(len(summary.columns)):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#E7E6E6')
        else:
            table[(i, j)].set_facecolor('#F2F2F2')

plt.title('Synthèse Détaillée - TOP 15 Communes (Budget 130k EUR)', 
          fontsize=13, fontweight='bold', pad=20)
plt.savefig('exports/visualisations/07_synthese_tableau.png', dpi=300, bbox_inches='tight')
print("✓ Visualisation 7: Synthèse tableau créée")
plt.close()

print()
print("=" * 80)
print("VISUALISATIONS GÉNÉRÉES")
print("=" * 80)
print("Dossier: exports/visualisations/")
print()
print("Fichiers créés:")
print("  1. 01_top10_communes_130k.png - Top 10 communes pour budget 130k")
print("  2. 02_qualite_prix.png - Analyse qualité-prix")
print("  3. 03_distribution_prix.png - Distribution des prix")
print("  4. 04_top10_ratio_prix.png - Meilleur rapport qualité-prix")
print("  5. 05_prix_minmaxmoy.png - Gamme de prix par commune")
print("  6. 06_nombre_annonces.png - Nombre d'annonces")
print("  7. 07_synthese_tableau.png - Tableau synthèse")
print()
