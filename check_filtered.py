import sqlite3

conn = sqlite3.connect('database/immobilier.db')
cursor = conn.cursor()

# DPE_MAPPING depuis database/db.py
DPE_MAPPING = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}

cursor.execute('''
    SELECT location, price, dpe 
    FROM properties 
    WHERE price >= 50000 AND price <= 150000 AND dpe_value <= ?
    ORDER BY price
''', (DPE_MAPPING['D'],))

results = cursor.fetchall()
print(f'Propriétés 50k-150k avec DPE ≤ D: {len(results)}\n')
for loc, price, dpe in results:
    print(f'  {loc}: {price:,.0f} EUR (DPE {dpe})')
