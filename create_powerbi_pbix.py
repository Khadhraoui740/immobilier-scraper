#!/usr/bin/env python3
"""
Solution 1: Créer un rapport Power BI (.pbix) directement en Python
Utilise: python-pptx (alternative) + génération de structure PBIX

Note: Power BI Desktop .pbix est un format ZIP propriétaire.
Cette approche crée une structure minimale que Power BI peut lire.
"""

import json
import sqlite3
import os
import zipfile
from datetime import datetime
from pathlib import Path

class PowerBIPBIXGenerator:
    """Génère une base .pbix que vous pouvez ouvrir dans Power BI Desktop"""
    
    def __init__(self, db_path="database/immobilier.db", output_path="exports"):
        self.db_path = db_path
        self.output_path = output_path
        self.temp_dir = os.path.join(output_path, ".pbix_temp")
        
    def extract_data(self):
        """Extrait les données SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Récupère les communes avec stats
        cursor.execute("""
            SELECT 
                commune,
                COUNT(*) as nombre,
                ROUND(AVG(price), 0) as prix_moyen,
                MIN(price) as prix_min,
                MAX(price) as prix_max
            FROM properties
            GROUP BY commune
            ORDER BY prix_moyen ASC
        """)
        
        data = cursor.fetchall()
        conn.close()
        
        return [{
            "Commune": row[0],
            "Nombre": row[1],
            "PrixMoyen": row[2],
            "PrixMin": row[3],
            "PrixMax": row[4]
        } for row in data]
    
    def create_pbix_structure(self, data):
        """Crée la structure minimale .pbix"""
        
        # Crée le répertoire temporaire
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # 1. Crée le fichier DataModelSchema.json
        schema = {
            "version": "1.0",
            "dataModel": {
                "tables": [{
                    "name": "Communes",
                    "columns": [
                        {"name": "Commune", "dataType": "string"},
                        {"name": "Nombre", "dataType": "int64"},
                        {"name": "PrixMoyen", "dataType": "int64"},
                        {"name": "PrixMin", "dataType": "int64"},
                        {"name": "PrixMax", "dataType": "int64"}
                    ],
                    "rows": data
                }]
            }
        }
        
        schema_path = os.path.join(self.temp_dir, "DataModelSchema.json")
        with open(schema_path, 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=2)
        
        # 2. Crée le fichier Report.json (rapport vide, prêt à éditer)
        report = {
            "version": "1.0.0",
            "config": {
                "hasUsingDefaultBindingUI": True
            },
            "sections": [{
                "name": "ReportSection1",
                "displayName": "Vue Générale",
                "visualContainers": []  # Vous allez ajouter les visuels
            }]
        }
        
        report_path = os.path.join(self.temp_dir, "Report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        # 3. Crée metadata.json
        metadata = {
            "name": "Rapport Immobilier",
            "description": "Analyse des communes Île-de-France - Budget 130k EUR",
            "created": datetime.now().isoformat(),
            "author": "Scraper Immobilier"
        }
        
        metadata_path = os.path.join(self.temp_dir, "metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
    
    def create_zip_pbix(self):
        """Crée le fichier .pbix (ZIP avec structure)"""
        pbix_path = os.path.join(self.output_path, "rapport_immobilier.pbix")
        
        with zipfile.ZipFile(pbix_path, 'w', zipfile.ZIP_DEFLATED) as pbix:
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.temp_dir)
                    pbix.write(file_path, arcname)
        
        return pbix_path
    
    def cleanup(self):
        """Nettoie les fichiers temporaires"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def generate(self):
        """Génère le .pbix complet"""
        print("📊 Génération du fichier Power BI (.pbix)...")
        
        data = self.extract_data()
        print(f"✓ {len(data)} communes extraites")
        
        self.create_pbix_structure(data)
        print("✓ Structure PBIX créée")
        
        pbix_path = self.create_zip_pbix()
        print(f"✓ Fichier créé: {pbix_path}")
        
        self.cleanup()
        print("\n📌 Prochaine étape:")
        print("1. Ouvrez Power BI Desktop")
        print("2. Ouvrez le fichier: " + pbix_path)
        print("3. Les données sont prêtes, vous pouvez créer les visuels")
        
        return pbix_path


if __name__ == "__main__":
    generator = PowerBIPBIXGenerator()
    generator.generate()
