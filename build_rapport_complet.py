#!/usr/bin/env python3
"""
Générateur de rapport Power BI COMPLET avec 12 visuels
Crée un fichier .pbix préconfiguré avec tous les graphiques
"""

import json
import zipfile
import os
import shutil
import uuid
from datetime import datetime

class PowerBIReportBuilder:
    def __init__(self, output_path="exports/rapport_complet.pbix"):
        self.output_path = output_path
        self.work_dir = "pbix_build"
        
    def _load_csv_data(self):
        """Charge les données CSV"""
        data = []
        csv_path = "exports/synthese_communes.csv"
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"{csv_path} manquant")
        
        import csv
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        return data
    
    def _create_directory_structure(self):
        """Crée la structure des dossiers"""
        if os.path.exists(self.work_dir):
            shutil.rmtree(self.work_dir)
        
        os.makedirs(f"{self.work_dir}/[Content_Types]", exist_ok=True)
        os.makedirs(f"{self.work_dir}/_rels", exist_ok=True)
        os.makedirs(f"{self.work_dir}/report", exist_ok=True)
        os.makedirs(f"{self.work_dir}/report/_rels", exist_ok=True)
        os.makedirs(f"{self.work_dir}/customXml", exist_ok=True)
        os.makedirs(f"{self.work_dir}/metadata", exist_ok=True)
    
    def _create_content_types(self):
        """Fichier [Content_Types].xml"""
        content = '''<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Default Extension="json" ContentType="application/json"/>
    <Override PartName="/report/document.xml" ContentType="application/vnd.ms-powerbi.report.document+xml"/>
    <Override PartName="/report/metadata.json" ContentType="application/json"/>
    <Override PartName="/customXml/item1.xml" ContentType="application/vnd.openxmlformats-officedocument.customXmlPart+xml"/>
</Types>'''
        with open(f"{self.work_dir}/[Content_Types].xml", "w", encoding="utf-8") as f:
            f.write(content)
    
    def _create_relationships(self):
        """Fichiers .rels"""
        rels = '''<?xml version="1.0" encoding="utf-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.microsoft.com/office/2007/relationships/metadata/core-properties" Target="metadata/core.xml"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="metadata/app.xml"/>
</Relationships>'''
        with open(f"{self.work_dir}/_rels/.rels", "w", encoding="utf-8") as f:
            f.write(rels)
        
        report_rels = '''<?xml version="1.0" encoding="utf-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>'''
        with open(f"{self.work_dir}/report/_rels/document.xml.rels", "w", encoding="utf-8") as f:
            f.write(report_rels)
    
    def _create_document(self, data):
        """Crée le document principal avec les 12 visuels"""
        
        num_communes = len(data)
        avg_price = sum(float(row.get('prix_moyen', 0)) for row in data) / num_communes if data else 0
        accessible = sum(1 for row in data if float(row.get('prix_moyen', 0)) <= 130000)
        
        document = {
            "version": "1.2.0",
            "name": "Rapport Complet Immobilier",
            "description": "Analyse 12 visualisations",
            "dataModel": {
                "tables": [{
                    "name": "Communes",
                    "columns": [
                        {"name": "commune", "dataType": "string"},
                        {"name": "prix_moyen", "dataType": "double"},
                        {"name": "prix_min", "dataType": "double"},
                        {"name": "prix_max", "dataType": "double"},
                        {"name": "prix_m2", "dataType": "double"},
                        {"name": "nb_proprietes", "dataType": "int64"}
                    ],
                    "rows": data
                }]
            },
            "pages": [{
                "name": "Page1",
                "displayName": "Rapport Complet",
                "width": 1920,
                "height": 1080,
                "visuals": self._generate_12_visuals(num_communes, avg_price, accessible)
            }],
            "config": {
                "theme": "default",
                "locale": "fr-FR"
            }
        }
        
        with open(f"{self.work_dir}/report/document.json", "w", encoding="utf-8") as f:
            json.dump(document, f, indent=2, ensure_ascii=False)
    
    def _generate_12_visuals(self, num_communes, avg_price, accessible):
        """Génère les définitions des 12 visuels"""
        return [
            {
                "name": "kpi_communes",
                "type": "card",
                "x": 0, "y": 0, "width": 0.2, "height": 0.15,
                "title": "Communes Analysées",
                "value": num_communes,
                "format": "number"
            },
            {
                "name": "kpi_prix",
                "type": "card",
                "x": 0.2, "y": 0, "width": 0.2, "height": 0.15,
                "title": "Prix Moyen",
                "value": f"{avg_price:,.0f}€",
                "format": "currency"
            },
            {
                "name": "kpi_accessibles",
                "type": "card",
                "x": 0.4, "y": 0, "width": 0.2, "height": 0.15,
                "title": "Accessibles ≤130k",
                "value": accessible,
                "format": "number"
            },
            {
                "name": "gauge_budget",
                "type": "gauge",
                "x": 0.6, "y": 0, "width": 0.4, "height": 0.15,
                "title": "Budget Poissy",
                "min": 0, "max": 130000, "value": 103651
            },
            {
                "name": "slicer_commune",
                "type": "slicer",
                "x": 0, "y": 0.15, "width": 1, "height": 0.08,
                "title": "Commune",
                "field": "commune"
            },
            {
                "name": "chart_bar",
                "type": "columnChart",
                "x": 0, "y": 0.23, "width": 0.5, "height": 0.3,
                "title": "Prix par Commune",
                "xAxis": "commune",
                "yAxis": "prix_moyen"
            },
            {
                "name": "scatter_plot",
                "type": "scatterChart",
                "x": 0.5, "y": 0.23, "width": 0.5, "height": 0.3,
                "title": "Prix M² vs Total",
                "xAxis": "prix_m2",
                "yAxis": "prix_moyen"
            },
            {
                "name": "table_details",
                "type": "table",
                "x": 0, "y": 0.53, "width": 1, "height": 0.25,
                "title": "Détail des Communes",
                "columns": ["commune", "prix_moyen", "prix_min", "prix_max", "prix_m2"]
            },
            {
                "name": "line_chart",
                "type": "lineChart",
                "x": 0, "y": 0.78, "width": 0.33, "height": 0.22,
                "title": "Progression Prix",
                "xAxis": "commune",
                "yAxis": "prix_moyen"
            },
            {
                "name": "donut_chart",
                "type": "donutChart",
                "x": 0.33, "y": 0.78, "width": 0.33, "height": 0.22,
                "title": "Distribution Accessibles",
                "field": "commune",
                "value": "prix_moyen"
            },
            {
                "name": "matrix_compare",
                "type": "matrix",
                "x": 0.66, "y": 0.78, "width": 0.34, "height": 0.22,
                "title": "Comparaison Détaillée",
                "rows": "commune",
                "values": ["prix_moyen", "prix_m2"]
            },
            {
                "name": "pie_chart",
                "type": "pieChart",
                "x": 0, "y": 0.5, "width": 1, "height": 0.3,
                "title": "Répartition Budget",
                "field": "commune",
                "value": "prix_moyen"
            }
        ]
    
    def _create_metadata(self):
        """Crée les métadonnées"""
        core = '''<?xml version="1.0" encoding="utf-8"?>
<coreProperties xmlns="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Rapport Immobilier - 12 Visualisations</dc:title>
    <dc:creator>Immobilier Scraper</dc:creator>
    <dc:subject>Île-de-France Investment Analysis</dc:subject>
</coreProperties>'''
        
        with open(f"{self.work_dir}/metadata/core.xml", "w", encoding="utf-8") as f:
            f.write(core)
    
    def _create_zip(self):
        """Crée le fichier ZIP final"""
        os.makedirs("exports", exist_ok=True)
        
        with zipfile.ZipFile(self.output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.work_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = file_path.replace(self.work_dir, "").lstrip("/\\")
                    zipf.write(file_path, arcname)
        
        shutil.rmtree(self.work_dir)
    
    def build(self):
        """Lance la construction complète"""
        print("\n" + "="*80)
        print("🚀 GÉNÉRATION DU RAPPORT POWER BI COMPLET (12 VISUELS)")
        print("="*80 + "\n")
        
        try:
            print("📊 Chargement des données...")
            data = self._load_csv_data()
            print(f"   ✓ {len(data)} communes chargées\n")
            
            print("🔨 Création de la structure...")
            self._create_directory_structure()
            self._create_content_types()
            self._create_relationships()
            self._create_metadata()
            print("   ✓ Structure créée\n")
            
            print("📐 Création des 12 visuels...")
            self._create_document(data)
            print("   ✓ Visuels définis\n")
            
            print("📦 Création du fichier PBIX...")
            self._create_zip()
            print("   ✓ Fichier généré\n")
            
            if os.path.exists(self.output_path):
                size = os.path.getsize(self.output_path)
                print("="*80)
                print("✅ RAPPORT GÉNÉRÉ AVEC SUCCÈS!")
                print("="*80)
                print(f"\n📍 Fichier: {os.path.abspath(self.output_path)}")
                print(f"📊 Taille: {size:,} bytes")
                print(f"📋 Visuels: 12")
                print(f"📈 Communes: {len(data)}")
                print(f"💰 Budget: 130,000€")
                print("\n" + "="*80)
                print("Pour ouvrir le rapport:")
                print("   python ouvrir_rapport.py")
                print("="*80 + "\n")
                return True
            else:
                print("❌ Erreur: Le fichier n'a pas été créé")
                return False
                
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    builder = PowerBIReportBuilder()
    success = builder.build()
    exit(0 if success else 1)
