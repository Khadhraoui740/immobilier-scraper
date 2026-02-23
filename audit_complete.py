"""
AUDIT COMPLET DU SYSTEME IMMOBILIER-SCRAPER
============================================

Ce script fait un audit complet du code et de la fonctionnalité.
"""

import os
import json
import re
from pathlib import Path

print("=" * 100)
print("AUDIT COMPLET DU SYSTEME")
print("=" * 100)

audit_results = {
    'backend': {},
    'frontend': {},
    'database': {},
    'config': {},
    'issues': [],
    'warnings': []
}

# ============================================================================
# 1. AUDIT DU CODE BACKEND (app.py)
# ============================================================================
print("\n1. AUDIT CODE BACKEND (app.py)")
print("-" * 100)

app_py_path = 'app.py'
with open(app_py_path, encoding='utf-8', errors='ignore') as f:
    app_content = f.read()

# Verifier les imports necesaires
required_imports = ['Flask', 'requests', 'sqlite3', 'json', 'datetime']
for imp in required_imports:
    if imp in app_content:
        print(f"[OK] Import {imp} present")
        audit_results['backend'][f'import_{imp}'] = True
    else:
        print(f"[ERREUR] Import {imp} ABSENT")
        audit_results['issues'].append(f"Import {imp} manquant dans app.py")
        audit_results['backend'][f'import_{imp}'] = False

# Verifier les endpoints API
endpoints = [
    '/api/search',
    '/api/config/get',
    '/api/config/save',
    '/api/property/<property_id>',
    '/api/scrape'
]

for endpoint in endpoints:
    # Chercher le route
    if endpoint in app_content:
        print(f"[OK] Endpoint {endpoint} défini")
        audit_results['backend'][endpoint] = True
    else:
        print(f"[ERREUR] Endpoint {endpoint} ABSENT")
        audit_results['issues'].append(f"Endpoint {endpoint} manquant")
        audit_results['backend'][endpoint] = False

# Verifier load_user_config()
if 'def load_user_config' in app_content:
    print(f"[OK] Fonction load_user_config() définie")
    audit_results['backend']['load_user_config'] = True
    if 'load_user_config()' in app_content:
        print(f"[OK] load_user_config() appelée au démarrage")
        audit_results['backend']['load_user_config_called'] = True
    else:
        print(f"[AVERTISSEMENT] load_user_config() définie mais pas appelée au démarrage?")
        audit_results['warnings'].append("load_user_config() définie mais peut-être pas appelée au démarrage")
        audit_results['backend']['load_user_config_called'] = False
else:
    print(f"[ERREUR] Fonction load_user_config() ABSENT")
    audit_results['issues'].append("Fonction load_user_config() manquante")
    audit_results['backend']['load_user_config'] = False

# Verifier DPE_MAPPING
if 'DPE_MAPPING' in app_content or 'DPE_MAPPING' in open('config.py').read():
    print(f"[OK] DPE_MAPPING défini")
    audit_results['backend']['DPE_MAPPING'] = True
else:
    print(f"[ERREUR] DPE_MAPPING ABSENT")
    audit_results['issues'].append("DPE_MAPPING manquant")
    audit_results['backend']['DPE_MAPPING'] = False

# ============================================================================
# 2. AUDIT FRONTEND (JavaScript)
# ============================================================================
print("\n2. AUDIT CODE FRONTEND (main.js)")
print("-" * 100)

js_path = 'static/js/main.js'
with open(js_path, encoding='utf-8', errors='ignore') as f:
    js_content = f.read()

# Verifier les fonctions essentielles
required_functions = [
    'async function apiCall',
    'function showNotification',
    'async function doSearch',
    'function formatPrice'
]

for func in required_functions:
    if func in js_content:
        print(f"[OK] Fonction trouvée: {func}")
        audit_results['frontend'][func] = True
    else:
        print(f"[AVERTISSEMENT] Fonction non trouvée: {func}")
        audit_results['warnings'].append(f"Fonction {func} manquante dans main.js")
        audit_results['frontend'][func] = False

# ============================================================================
# 3. AUDIT DES TEMPLATES HTML
# ============================================================================
print("\n3. AUDIT DES TEMPLATES HTML")
print("-" * 100)

templates = {
    'config.html': [
        'budgetMin',
        'budgetMax',
        'dpeMax',
        'zone75',
        'saveConfig',
        'loadConfig',
        'ZONE_MAPPING'
    ],
    'search.html': [
        'doSearch',
        'location',
        'priceMin',
        'priceMax',
        'dpeMax'
    ],
    'properties.html': [
        'posted_date',
        'location'
    ],
    'property.html': [
        'posted_date',
        'location'
    ]
}

for template, required_elements in templates.items():
    print(f"\nTemplate: {template}")
    template_path = f'templates/{template}'
    if os.path.exists(template_path):
        with open(template_path) as f:
            template_content = f.read()
        
        for element in required_elements:
            if element in template_content:
                print(f"  [OK] {element} present")
                audit_results['frontend'][f'{template}_{element}'] = True
            else:
                print(f"  [ERREUR] {element} ABSENT")
                audit_results['issues'].append(f"{element} manquant dans {template}")
                audit_results['frontend'][f'{template}_{element}'] = False
    else:
        print(f"  [ERREUR] Template {template} N'EXISTE PAS")
        audit_results['issues'].append(f"Template {template} manquant")

# ============================================================================
# 4. AUDIT DE LA CONFIGURATION
# ============================================================================
print("\n4. AUDIT DE LA CONFIGURATION")
print("-" * 100)

# Verifier fichiers de config
config_files = [
    'config.py',
    'data/user_config.json'
]

for config_file in config_files:
    if os.path.exists(config_file):
        print(f"[OK] Fichier {config_file} existe")
        audit_results['config'][config_file] = True
        
        if config_file == 'data/user_config.json':
            try:
                with open(config_file) as f:
                    config = json.load(f)
                required_keys = ['budget_min', 'budget_max', 'dpe_max', 'zones']
                for key in required_keys:
                    if key in config:
                        print(f"  [OK] Cle {key} presente: {config[key]}")
                    else:
                        print(f"  [ERREUR] Cle {key} manquante")
                        audit_results['issues'].append(f"Cle {key} manquante dans user_config.json")
            except json.JSONDecodeError:
                print(f"  [ERREUR] Fichier {config_file} n'est pas un JSON valide")
                audit_results['issues'].append(f"user_config.json invalide")
    else:
        print(f"[ERREUR] Fichier {config_file} N'EXISTE PAS")
        audit_results['issues'].append(f"Fichier {config_file} manquant")
        audit_results['config'][config_file] = False

# ============================================================================
# 5. AUDIT DE LA BASE DE DONNEES
# ============================================================================
print("\n5. AUDIT DE LA BASE DE DONNEES")
print("-" * 100)

import sqlite3

db_path = 'database/immobilier.db'
if os.path.exists(db_path):
    print(f"[OK] Fichier database existe")
    audit_results['database']['exists'] = True
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verifier table properties
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='properties'")
        if cursor.fetchone():
            print(f"[OK] Table 'properties' existe")
            audit_results['database']['properties_table'] = True
            
            # Verifier colonnes
            cursor.execute("PRAGMA table_info(properties)")
            columns = {row[1]: row[2] for row in cursor.fetchall()}
            
            required_columns = ['id', 'title', 'price', 'location', 'dpe', 'posted_date', 'source']
            for col in required_columns:
                if col in columns:
                    print(f"  [OK] Colonne {col} existe ({columns[col]})")
                    audit_results['database'][f'col_{col}'] = True
                else:
                    print(f"  [ERREUR] Colonne {col} ABSENT")
                    audit_results['issues'].append(f"Colonne {col} manquante dans table properties")
                    audit_results['database'][f'col_{col}'] = False
            
            # Compter les proprietes
            cursor.execute("SELECT COUNT(*) FROM properties")
            count = cursor.fetchone()[0]
            print(f"  [INFO] Total proprietes: {count}")
            audit_results['database']['count'] = count
        else:
            print(f"[ERREUR] Table 'properties' N'EXISTE PAS")
            audit_results['issues'].append("Table 'properties' manquante")
            audit_results['database']['properties_table'] = False
        
        conn.close()
    except Exception as e:
        print(f"[ERREUR] Impossible de lire la database: {e}")
        audit_results['issues'].append(f"Erreur lecture database: {e}")
else:
    print(f"[ERREUR] Fichier database N'EXISTE PAS")
    audit_results['issues'].append("Fichier database manquant")
    audit_results['database']['exists'] = False

# ============================================================================
# 6. RESUME
# ============================================================================
print("\n" + "=" * 100)
print("RESUME DE L'AUDIT")
print("=" * 100)

total_issues = len(audit_results['issues'])
total_warnings = len(audit_results['warnings'])

print(f"\nErreurs trouvees: {total_issues}")
for issue in audit_results['issues']:
    print(f"  - {issue}")

print(f"\nAvertissements: {total_warnings}")
for warning in audit_results['warnings']:
    print(f"  - {warning}")

if total_issues == 0:
    print("\n[SUCCES] Aucune erreur trouvee!")
else:
    print(f"\n[ATTENTION] {total_issues} erreur(s) a corriger")

# Sauvegarder les resultats
with open('audit_results.json', 'w') as f:
    json.dump(audit_results, f, indent=2, ensure_ascii=False)
    
print("\nResultats complets sauveg­ard­es dans audit_results.json")

print("\n" + "=" * 100)
print("FIN AUDIT")
print("=" * 100)
