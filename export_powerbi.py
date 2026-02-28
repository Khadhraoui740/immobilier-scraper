"""
Export des données immobilier pour Power BI
Génère des fichiers CSV et synthèse d'analyse
"""
import sqlite3
import csv
from datetime import datetime
from collections import defaultdict

# Connexion à la base de données
conn = sqlite3.connect('database/immobilier.db')
cursor = conn.cursor()

print("=" * 80)
print("EXPORT DONNÉES IMMOBILIER POUR POWER BI")
print("=" * 80)
print()

# 1. Récupérer toutes les propriétés
cursor.execute('''
    SELECT id, source, location, price, surface, rooms, dpe, posted_date, url
    FROM properties
    ORDER BY location, price
''')

properties = cursor.fetchall()
print(f"Total propriétés en base: {len(properties)}")

# 2. Exporter en CSV
csv_filename = 'exports/proprietes_immobilier.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Source', 'Commune', 'Prix', 'Surface', 'Pieces', 'DPE', 'Date Publie', 'URL'])
    for prop in properties:
        writer.writerow(prop)

print(f"Export CSV: {csv_filename}")
print()

# 3. Analyse par commune
communes_data = defaultdict(lambda: {'count': 0, 'prices': [], 'surfaces': []})

for prop in properties:
    id_, source, location, price, surface, rooms, dpe, posted_date, url = prop
    if price and location:
        communes_data[location]['count'] += 1
        communes_data[location]['prices'].append(price)
        if surface:
            communes_data[location]['surfaces'].append(surface)

# Calcul statistiques par commune
commune_stats = []
for commune, data in sorted(communes_data.items()):
    if data['prices']:
        avg_price = sum(data['prices']) / len(data['prices'])
        min_price = min(data['prices'])
        max_price = max(data['prices'])
        avg_surface = sum(data['surfaces']) / len(data['surfaces']) if data['surfaces'] else 0
        price_per_m2 = avg_price / avg_surface if avg_surface > 0 else 0
        
        commune_stats.append({
            'commune': commune,
            'count': data['count'],
            'avg_price': avg_price,
            'min_price': min_price,
            'max_price': max_price,
            'avg_surface': avg_surface,
            'price_per_m2': price_per_m2
        })

# Trier par prix moyen
commune_stats_sorted = sorted(commune_stats, key=lambda x: x['avg_price'])

# 4. Exporter analyse communes
stats_filename = 'exports/analyse_communes.csv'
with open(stats_filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Commune', 'Nombre Annonces', 'Prix Moyen', 'Prix Min', 'Prix Max', 'Surface Moy', 'Prix/m2'])
    for stat in commune_stats_sorted:
        writer.writerow([
            stat['commune'],
            stat['count'],
            f"{stat['avg_price']:.0f}",
            f"{stat['min_price']:.0f}",
            f"{stat['max_price']:.0f}",
            f"{stat['avg_surface']:.1f}",
            f"{stat['price_per_m2']:.0f}"
        ])

print(f"Export Analyse: {stats_filename}")
print()

# 5. Top 10 communes pour budget 130k
budget = 130000
print(f"TOP 10 COMMUNES POUR BUDGET DE {budget:,} EUR:")
print("-" * 80)

best_communes = [s for s in commune_stats_sorted if s['min_price'] <= budget][:10]

for i, stat in enumerate(best_communes, 1):
    print(f"{i:2}. {stat['commune']:<25} | Prix moy: {stat['avg_price']:>9,.0f} EUR | ({stat['count']} annonces)")

print()

# 6. Top 10 par rapport qualité/prix (prix/m2)
print("TOP 10 COMMUNES - MEILLEUR RAPPORT QUALITE/PRIX (€/m2):")
print("-" * 80)

best_value = sorted([s for s in commune_stats if s['min_price'] <= budget], 
                     key=lambda x: x['price_per_m2'])[:10]

for i, stat in enumerate(best_value, 1):
    print(f"{i:2}. {stat['commune']:<25} | {stat['price_per_m2']:>6,.0f} EUR/m2 | Prix moy: {stat['avg_price']:>9,.0f} EUR")

print()

# 7. Créer fichier synthèse pour Power BI
summary_filename = 'exports/synthese_communes.csv'
with open(summary_filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Rang', 'Commune', 'Count', 'AvgPrice', 'MinPrice', 'MaxPrice', 'AvgSurface', 'PricePerm2', 'BudgetFit'])
    
    for rank, stat in enumerate(commune_stats_sorted, 1):
        budget_fit = 1 if stat['min_price'] <= budget else 0
        writer.writerow([
            rank,
            stat['commune'],
            stat['count'],
            stat['avg_price'],
            stat['min_price'],
            stat['max_price'],
            stat['avg_surface'],
            stat['price_per_m2'],
            budget_fit
        ])

print(f"Export Synthese: {summary_filename}")
print()

print("=" * 80)
print("FICHIERS GENERÉS - PRETS POUR POWER BI:")
print("=" * 80)
print(f"  1. {csv_filename}")
print(f"  2. {stats_filename}")
print(f"  3. {summary_filename}")
print()
print("Importer ces fichiers CSV dans Power BI Desktop pour créer vos visualisations!")
print()

conn.close()
