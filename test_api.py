"""
Tester l'API pour vérifier les propriétés DVF chargées
"""
import requests
import json

# Endpoints à tester
endpoints = [
    ('/', 'GET', 'Page d\'accueil'),
    ('/dashboard', 'GET', 'Dashboard'),
    ('/properties', 'GET', 'Liste propriétés'),
]

print("🧪 Test des Endpoints")
print("=" * 50)

for endpoint, method, desc in endpoints:
    try:
        resp = requests.get(f'http://localhost:5000{endpoint}', timeout=3)
        status = '✅' if resp.status_code == 200 else '❌'
        print(f"{status} {endpoint} ({resp.status_code}) - {desc}")
    except Exception as e:
        print(f"❌ {endpoint} - Erreur: {e}")

print("\n📊 Vérifier le contenu de la base de données")
print("=" * 50)

# Connexion directe à la base pour vérifier
try:
    from database.db import Database
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Compter les propriétés
    cursor.execute('SELECT COUNT(*) FROM properties')
    count = cursor.fetchone()[0]
    print(f"📈 Propriétés dans la BD: {count}")
    
    # Afficher les 3 premières
    cursor.execute('SELECT platform, title, price, rooms FROM properties LIMIT 3')
    rows = cursor.fetchall()
    
    if rows:
        print("\n📍 Exemples:")
        for row in rows:
            platform, title, price, rooms = row
            print(f"  • {platform}: {title} ({rooms}P) - {price:,.0f}€")
    else:
        print("⚠️ Aucune propriété en base de données")
    
    conn.close()
except Exception as e:
    print(f"Erreur BD: {e}")
