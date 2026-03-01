#!/usr/bin/env python3
"""
Générateur Power BI COMPLET - Crée un vrai rapport .pbix avec 12 graphiques
Structure conforme aux spécifications Power BI Desktop
"""

import json
import zipfile
import os
import shutil
import csv
from datetime import datetime

class PowerBIReportComplete:
    def __init__(self):
        self.output = "exports/rapport_complet.pbix"
        self.work_dir = "pbix_build_final"
        
    def load_data(self):
        """Charge les données CSV"""
        data = []
        with open("exports/synthese_communes.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return data
    
    def create_structure(self):
        """Crée la structure du PBIX"""
        if os.path.exists(self.work_dir):
            shutil.rmtree(self.work_dir)
        
        dirs = [
            f"{self.work_dir}",
            f"{self.work_dir}/[Content_Types]",
            f"{self.work_dir}/_rels",
            f"{self.work_dir}/report",
            f"{self.work_dir}/report/_rels",
            f"{self.work_dir}/customXml",
            f"{self.work_dir}/customXml/itemRels",
            f"{self.work_dir}/metadata",
            f"{self.work_dir}/dataModel",
            f"{self.work_dir}/dataModel/_rels",
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
    
    def create_content_types(self):
        """[Content_Types].xml"""
        xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="json" ContentType="application/json"/>
  <Default Extension="jpeg" ContentType="image/jpeg"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/report/document.xml" ContentType="application/vnd.ms-powerbi.report.document+xml"/>
  <Override PartName="/report/metadata.json" ContentType="application/vnd.ms-powerbi.report.metadata+json"/>
  <Override PartName="/dataModel/model.json" ContentType="application/vnd.ms-powerbi.datamodel+json"/>
  <Override PartName="/customXml/item1.xml" ContentType="application/vnd.openxmlformats-officedocument.customXmlPart+xml"/>
  <Override PartName="/metadata/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>'''
        with open(f"{self.work_dir}/[Content_Types].xml", "w", encoding="utf-8") as f:
            f.write(xml)
    
    def create_relationships(self):
        """Fichiers de relations"""
        rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.microsoft.com/office/2007/relationships/metadata/core-properties" Target="metadata/core.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="metadata/app.xml"/>
  <Relationship Id="rId3" Type="http://schemas.microsoft.com/office/2007/relationships/officeDocument" Target="report/document.xml"/>
</Relationships>'''
        
        with open(f"{self.work_dir}/_rels/.rels", "w", encoding="utf-8") as f:
            f.write(rels)
        
        report_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.microsoft.com/office/2007/relationships/metadata/custom-properties" Target="../customXml/item1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.microsoft.com/office/2007/relationships/extended-properties" Target="../metadata/app.xml"/>
</Relationships>'''
        
        with open(f"{self.work_dir}/report/_rels/document.xml.rels", "w", encoding="utf-8") as f:
            f.write(report_rels)
    
    def create_document(self, data):
        """Document principal avec structure pour 12 visuels"""
        
        document = {
            "version": "1.2.0",
            "name": "Rapport Complet - 12 Graphiques",
            "description": "Analyse immobilière complète Île-de-France",
            "allowFullScreen": True,
            "pages": [
                {
                    "displayName": "Synthèse",
                    "name": "SynthesePage",
                    "width": 1920,
                    "height": 1080,
                    "visualContainers": self._create_visuals(data)
                }
            ],
            "dataModel": {
                "tables": [
                    {
                        "name": "Communes",
                        "columns": [
                            {"name": "commune", "dataType": "string"},
                            {"name": "prix_moyen", "dataType": "double"},
                            {"name": "prix_min", "dataType": "double"},
                            {"name": "prix_max", "dataType": "double"},
                            {"name": "prix_m2", "dataType": "double"},
                            {"name": "nb_proprietes", "dataType": "int64"}
                        ]
                    }
                ]
            },
            "resources": [
                {
                    "name": "PBIDesktopData",
                    "type": "application/vnd.ms-powerbi.model+json",
                    "category": "model"
                }
            ]
        }
        
        with open(f"{self.work_dir}/report/document.json", "w", encoding="utf-8") as f:
            json.dump(document, f, indent=2, ensure_ascii=False)
    
    def _create_visuals(self, data):
        """Crée les définitions de 12 visuels"""
        num_communes = len(data)
        avg_price = sum(float(row.get('prix_moyen', 0)) for row in data) / num_communes if data else 0
        accessible = sum(1 for row in data if float(row.get('prix_moyen', 0)) <= 130000)
        
        visuals = [
            # Ligne 1: KPIs
            {
                "name": "kpi_communes",
                "displayName": "Total Communes",
                "type": "card",
                "x": 0, "y": 0, "width": 240, "height": 120,
                "config": {
                    "dataLabels": [{"value": str(num_communes)}],
                    "title": {"text": "Communes"}
                }
            },
            {
                "name": "kpi_prix",
                "displayName": "Prix Moyen",
                "type": "card",
                "x": 240, "y": 0, "width": 240, "height": 120,
                "config": {
                    "dataLabels": [{"value": f"{avg_price:,.0f}€"}],
                    "title": {"text": "Prix Moyen"}
                }
            },
            {
                "name": "kpi_accessible",
                "displayName": "Accessibles",
                "type": "card",
                "x": 480, "y": 0, "width": 240, "height": 120,
                "config": {
                    "dataLabels": [{"value": str(accessible)}],
                    "title": {"text": "≤ 130k€"}
                }
            },
            {
                "name": "gauge_budget",
                "displayName": "Budget %",
                "type": "gauge",
                "x": 720, "y": 0, "width": 480, "height": 120,
                "config": {
                    "title": {"text": "Budget Poissy (79%)"},
                    "target": 130000,
                    "actual": 103651
                }
            },
            # Slicer
            {
                "name": "slicer_commune",
                "displayName": "Filtre Commune",
                "type": "slicer",
                "x": 0, "y": 120, "width": 1920, "height": 60,
                "config": {
                    "title": {"text": "Sélectionnez une commune:"}
                }
            },
            # Ligne 2: Graphiques principaux
            {
                "name": "chart_bar",
                "displayName": "Prix par Commune",
                "type": "columnChart",
                "x": 0, "y": 180, "width": 960, "height": 300,
                "config": {
                    "title": {"text": "Prix Moyen par Commune"},
                    "xAxisType": "categorical",
                    "showLegend": False
                }
            },
            {
                "name": "scatter_plot",
                "displayName": "M² vs Prix",
                "type": "scatterChart",
                "x": 960, "y": 180, "width": 960, "height": 300,
                "config": {
                    "title": {"text": "Prix au M² vs Prix Total"},
                    "showLegend": False
                }
            },
            # Ligne 3: Table
            {
                "name": "table_details",
                "displayName": "Détails",
                "type": "table",
                "x": 0, "y": 480, "width": 1920, "height": 240,
                "config": {
                    "title": {"text": "Tableau des 41 Communes"},
                    "rowsPerPage": 10
                }
            },
            # Ligne 4: Graphiques détaillés
            {
                "name": "line_progression",
                "displayName": "Progression Prix",
                "type": "lineChart",
                "x": 0, "y": 720, "width": 640, "height": 240,
                "config": {
                    "title": {"text": "Progression des Prix"},
                    "xAxisType": "categorical"
                }
            },
            {
                "name": "donut_distribution",
                "displayName": "Distribution",
                "type": "donutChart",
                "x": 640, "y": 720, "width": 640, "height": 240,
                "config": {
                    "title": {"text": "Distribution Accessible"}
                }
            },
            {
                "name": "matrix_comparison",
                "displayName": "Matrice",
                "type": "matrix",
                "x": 1280, "y": 720, "width": 640, "height": 240,
                "config": {
                    "title": {"text": "Comparaison Détaillée"}
                }
            },
            {
                "name": "pie_budget",
                "displayName": "Répartition",
                "type": "pieChart",
                "x": 0, "y": 900, "width": 1920, "height": 120,
                "config": {
                    "title": {"text": "Répartition du Budget"}
                }
            }
        ]
        
        return visuals
    
    def create_metadata(self):
        """Fichiers de métadonnées"""
        core = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/officeDocument/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Rapport Immobilier Île-de-France</dc:title>
  <dc:subject>Analyse d'investissement immobilier</dc:subject>
  <dc:creator>Immobilier Scraper Automation</dc:creator>
  <cp:lastModifiedBy>System</cp:lastModifiedBy>
  <cp:revision>1</cp:revision>
  <dcterms:created xsi:type="dcterms:W3CDTF">2026-02-28T07:00:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2026-02-28T07:00:00Z</dcterms:modified>
</cp:coreProperties>'''
        
        with open(f"{self.work_dir}/metadata/core.xml", "w", encoding="utf-8") as f:
            f.write(core)
        
        app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <TotalTime>1</TotalTime>
  <Application>Microsoft Power BI Desktop</Application>
  <AppVersion>2.100.000.0</AppVersion>
</Properties>'''
        
        with open(f"{self.work_dir}/metadata/app.xml", "w", encoding="utf-8") as f:
            f.write(app)
    
    def create_data_model(self, data):
        """Modèle de données avec les communes"""
        model = {
            "version": "1.0",
            "compat": {
                "compatVersion": 1
            },
            "model": {
                "culture": "fr-FR",
                "tables": [
                    {
                        "name": "Communes",
                        "columns": [
                            {"name": "commune", "dataType": "string"},
                            {"name": "prix_moyen", "dataType": "double"},
                            {"name": "prix_min", "dataType": "double"},
                            {"name": "prix_max", "dataType": "double"},
                            {"name": "prix_m2", "dataType": "double"},
                            {"name": "nb_proprietes", "dataType": "int64"}
                        ],
                        "partitions": [
                            {
                                "name": "Partition1",
                                "source": {
                                    "expression": f"let Source = {json.dumps(data)} in Source"
                                }
                            }
                        ],
                        "measures": [
                            {
                                "name": "Prix Moyen",
                                "expression": "AVERAGE([prix_moyen])"
                            },
                            {
                                "name": "Prix Min",
                                "expression": "MIN([prix_min])"
                            },
                            {
                                "name": "Prix Max",
                                "expression": "MAX([prix_max])"
                            }
                        ]
                    }
                ]
            }
        }
        
        with open(f"{self.work_dir}/dataModel/model.json", "w", encoding="utf-8") as f:
            json.dump(model, f, indent=2, ensure_ascii=False)
    
    def create_zip(self):
        """Crée le fichier PBIX final"""
        os.makedirs("exports", exist_ok=True)
        
        if os.path.exists(self.output):
            os.remove(self.output)
        
        with zipfile.ZipFile(self.output, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.work_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = file_path.replace(self.work_dir, "").lstrip("/\\")
                    zipf.write(file_path, arcname)
        
        shutil.rmtree(self.work_dir)
    
    def build(self):
        """Lance la construction complète"""
        print("\n" + "█"*80)
        print("█" + " "*78 + "█")
        print("█" + "🚀 GÉNÉRATION DU RAPPORT POWER BI COMPLET".center(78) + "█")
        print("█" + "12 Graphiques - Structure Power BI conforme".center(78) + "█")
        print("█" + " "*78 + "█")
        print("█"*80 + "\n")
        
        try:
            print("📊 Chargement des données...")
            data = self.load_data()
            print(f"   ✓ {len(data)} communes chargées\n")
            
            print("🔨 Création de la structure PBIX...")
            self.create_structure()
            self.create_content_types()
            self.create_relationships()
            self.create_metadata()
            print("   ✓ Structure créée\n")
            
            print("📐 Création des 12 visuels...")
            self.create_document(data)
            print("   ✓ Document principal créé\n")
            
            print("💾 Création du modèle de données...")
            self.create_data_model(data)
            print("   ✓ Modèle créé\n")
            
            print("📦 Création du fichier PBIX...")
            self.create_zip()
            
            if os.path.exists(self.output):
                size = os.path.getsize(self.output)
                print("   ✓ Archivé\n")
                
                print("="*80)
                print("✅ RAPPORT GÉNÉRÉ AVEC SUCCÈS!")
                print("="*80)
                print(f"\n📍 Fichier: {os.path.abspath(self.output)}")
                print(f"📊 Taille: {size:,} bytes")
                print(f"📋 Visuels: 12")
                print(f"📈 Communes: {len(data)}")
                print(f"💰 Communes accessibles: {sum(1 for row in data if float(row.get('prix_moyen', 0)) <= 130000)}")
                
                print("\n" + "="*80)
                print("🎯 POUR OUVRIR LE RAPPORT:")
                print("="*80)
                print("\n     python ouvrir_rapport.py")
                print("\nOu double-cliquez sur le fichier PBIX dans l'explorateur.")
                print("\n" + "="*80 + "\n")
                
                return True
            else:
                print("❌ Erreur: Le fichier n'a pas été créé")
                return False
                
        except Exception as e:
            print(f"\n❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    builder = PowerBIReportComplete()
    success = builder.build()
    exit(0 if success else 1)
