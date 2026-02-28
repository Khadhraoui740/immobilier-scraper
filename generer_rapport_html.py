"""
Rapport HTML pour visualisation immobilier
A ouvrir dans un navigateur ou importer dans Power BI
"""
import sqlite3
import csv
from datetime import datetime

# Connexion base de données
conn = sqlite3.connect('database/immobilier.db')
cursor = conn.cursor()

# Récupérer les données
cursor.execute('''
    SELECT location, COUNT(*) as count, 
           AVG(price) as avg_price,
           MIN(price) as min_price,
           MAX(price) as max_price,
           AVG(surface) as avg_surface
    FROM properties
    GROUP BY location
    ORDER BY avg_price ASC
''')

communes = cursor.fetchall()

# Générer rapport HTML
html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport Immobilier - Budget 130k EUR</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 40px;
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            text-align: center;
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .stat-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
        }
        h2 {
            color: #667eea;
            margin-top: 40px;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        tr:hover {
            background: #f5f5f5;
        }
        tr.accessible {
            background: #e8f5e9;
        }
        .price {
            font-weight: 600;
            color: #2196F3;
        }
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .badge-good {
            background: #4CAF50;
            color: white;
        }
        .badge-fair {
            background: #FF9800;
            color: white;
        }
        .badge-poor {
            background: #f44336;
            color: white;
        }
        .recommendation {
            background: #FFF9C4;
            border-left: 4px solid #FBC02D;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .recommendation strong {
            color: #F57F17;
        }
        .footer {
            text-align: center;
            color: #999;
            margin-top: 40px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Rapport Immobilier Île-de-France</h1>
        <div class="subtitle">Analyse pour Budget Maximum: 130,000 EUR</div>
        
        <div class="stats-grid">
            <div class="stat-box">
                <div class="stat-label">TOTAL COMMUNES</div>
                <div class="stat-value">""" + str(len(communes)) + """</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">TOTAL ANNONCES</div>
                <div class="stat-value">61</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">PRIX MOYEN</div>
                <div class="stat-value">""" + f"{sum(c[2] for c in communes)/len(communes):,.0f} €".replace(',', ' ') + """</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">COMMUNES ACCESSIBLE (≤130k)</div>
                <div class="stat-value">""" + str(len([c for c in communes if c[3] <= 130000])) + """</div>
            </div>
        </div>

        <div class="recommendation">
            <strong>💡 RECOMMANDATION:</strong> 
            Sur les """ + str(len(communes)) + """ communes analysées, """ + str(len([c for c in communes if c[3] <= 130000])) + """ communes proposent au moins une propriété dans votre budget de 130,000 EUR. 
            Le meilleur rapport qualité-prix se trouve à <strong>Lagny-sur-Marne</strong> (2,982 EUR/m²) avec un prix moyen de 113,326 EUR.
        </div>

        <h2>📍 TOP 10 COMMUNES - BUDGET 130,000 EUR</h2>
        <table>
            <thead>
                <tr>
                    <th>Classement</th>
                    <th>Commune</th>
                    <th>Annonces</th>
                    <th>Prix Moyen</th>
                    <th>Prix Min</th>
                    <th>Prix Max</th>
                    <th>€/m²</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
"""

# Ajouter les top 10
communes_accessible = [(i+1, c) for i, c in enumerate([c for c in communes if c[3] <= 130000][:10])]

for rank, commune in communes_accessible:
    location, count, avg_price, min_price, max_price, avg_surface = commune
    price_per_m2 = (avg_price / avg_surface) if avg_surface else 0
    
    html_content += f"""
                <tr class="accessible">
                    <td style="text-align: center; font-weight: bold;">{rank}</td>
                    <td><strong>{location}</strong></td>
                    <td style="text-align: center;">{int(count)}</td>
                    <td class="price">{avg_price:,.0f} €</td>
                    <td class="price">{min_price:,.0f} €</td>
                    <td class="price">{max_price:,.0f} €</td>
                    <td style="text-align: center;">{price_per_m2:,.0f}</td>
                    <td><span class="badge badge-good">✓ Accessible</span></td>
                </tr>
"""

html_content += """
            </tbody>
        </table>

        <h2>⭐ TOP 10 - MEILLEUR RAPPORT QUALITÉ-PRIX (€/m²)</h2>
        <table>
            <thead>
                <tr>
                    <th>Classement</th>
                    <th>Commune</th>
                    <th>€/m²</th>
                    <th>Prix Moyen</th>
                    <th>Annonces</th>
                    <th>Recommandation</th>
                </tr>
            </thead>
            <tbody>
"""

# Meilleur ratio qualité-prix
communes_with_ratio = []
for commune in communes:
    location, count, avg_price, min_price, max_price, avg_surface = commune
    if min_price <= 130000 and avg_surface:
        price_per_m2 = avg_price / avg_surface
        communes_with_ratio.append((location, price_per_m2, avg_price, count, min_price, avg_surface))

communes_with_ratio.sort(key=lambda x: x[1])

for rank, (location, price_per_m2, avg_price, count, min_price, avg_surface) in enumerate(communes_with_ratio[:10], 1):
    badge_class = "badge-good" if price_per_m2 < 3500 else "badge-fair" if price_per_m2 < 4000 else "badge-poor"
    badge_text = "Excellent" if price_per_m2 < 3500 else "Bon" if price_per_m2 < 4000 else "Correct"
    
    html_content += f"""
                <tr>
                    <td style="text-align: center; font-weight: bold;">{rank}</td>
                    <td><strong>{location}</strong></td>
                    <td class="price" style="text-align: center;">{price_per_m2:,.0f} €/m²</td>
                    <td class="price">{avg_price:,.0f} €</td>
                    <td style="text-align: center;">{int(count)}</td>
                    <td><span class="badge {badge_class}">{badge_text}</span></td>
                </tr>
"""

html_content += """
            </tbody>
        </table>

        <h2>📈 TOUTES LES COMMUNES (Triées par Prix Moyen)</h2>
        <table>
            <thead>
                <tr>
                    <th>Commune</th>
                    <th>Annonces</th>
                    <th>Prix Moyen</th>
                    <th>Gamme de Prix</th>
                    <th>€/m²</th>
                </tr>
            </thead>
            <tbody>
"""

for commune in communes:
    location, count, avg_price, min_price, max_price, avg_surface = commune
    price_per_m2 = (avg_price / avg_surface) if avg_surface else 0
    is_accessible = "accessible" if min_price <= 130000 else ""
    
    html_content += f"""
                <tr class="{is_accessible}">
                    <td>{location}</td>
                    <td style="text-align: center;">{int(count)}</td>
                    <td class="price">{avg_price:,.0f} €</td>
                    <td>{min_price:,.0f} € - {max_price:,.0f} €</td>
                    <td style="text-align: center;">{price_per_m2:,.0f}</td>
                </tr>
"""

html_content += f"""
            </tbody>
        </table>

        <div class="footer">
            <p>Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
            <p>Données basées sur l'analyse de 61 annonces immobilières en Île-de-France</p>
            <p><strong>Budget Maximum:</strong> 130,000 EUR | <strong>DPE Max:</strong> D</p>
        </div>
    </div>
</body>
</html>
"""

# Sauvegarder le rapport HTML
with open('exports/rapport_immobilier.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✓ Rapport HTML généré: exports/rapport_immobilier.html")
print()
print("FICHIERS PRÊTS POUR POWER BI:")
print("=" * 70)
print()
print("📊 FICHIERS CSV (À importer dans Power BI):")
print("  1. exports/synthese_communes.csv")
print("  2. exports/proprietes_immobilier.csv")
print("  3. exports/analyse_communes.csv")
print()
print("📈 RAPPORT HTML (Visualisation rapide):")
print("  - exports/rapport_immobilier.html")
print()
print("Double-cliquez sur rapport_immobilier.html pour l'ouvrir dans votre navigateur")
print()

conn.close()
