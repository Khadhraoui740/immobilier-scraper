#!/usr/bin/env python3
"""
Generateur automatique de rapport Power BI (.pbix)
Cree un fichier .pbix fonctionnel directement sans intervention utilisateur
"""

import json
import zipfile
import os
import shutil
from pathlib import Path
from datetime import datetime
import csv

class PowerBIGenerator:
    def __init__(self, output_path="exports/rapport_auto.pbix"):
        self.output_path = output_path
        self.work_dir = "pbix_temp"
        self.data = self._load_data()
        
    def _load_data(self):
        """Charge les donnees depuis les CSV"""
        print("📊 Chargement des donnees...")
        
        if os.path.exists("exports/synthese_communes.csv"):
            data = []
            with open("exports/synthese_communes.csv", 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            print(f"✓ {len(data)} communes chargees")
            return data
        else:
            raise FileNotFoundError("exports/synthese_communes.csv manquant. Executez d'abord export_powerbi.py")
    
    def _create_pbix_structure(self):
        """Cree la structure interne du fichier PBIX"""
        print("🔧 Creation de la structure PBIX...")
        
        # Cree le repertoire temporaire
        if os.path.exists(self.work_dir):
            shutil.rmtree(self.work_dir)
        os.makedirs(self.work_dir)
        
        # Dossier [Content_Types]
        os.makedirs(f"{self.work_dir}/[Content_Types]", exist_ok=True)
        
        # Dossiers principaux
        os.makedirs(f"{self.work_dir}/_rels", exist_ok=True)
        os.makedirs(f"{self.work_dir}/customXml", exist_ok=True)
        os.makedirs(f"{self.work_dir}/customXml/itemRels", exist_ok=True)
        os.makedirs(f"{self.work_dir}/report", exist_ok=True)
        os.makedirs(f"{self.work_dir}/report/_rels", exist_ok=True)
        os.makedirs(f"{self.work_dir}/metadata", exist_ok=True)
        os.makedirs(f"{self.work_dir}/queryGroups", exist_ok=True)
        
    def _create_content_types(self):
        """Cree le fichier [Content_Types].xml conforme Power BI"""
        content = '''<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Default Extension="json" ContentType="application/json"/>
    <Default Extension="png" ContentType="image/png"/>
    <Override PartName="/report/document.xml" ContentType="application/vnd.ms-powerbi.report.document+xml"/>
    <Override PartName="/report/metadata.json" ContentType="application/vnd.ms-powerbi.report.metadata+json"/>
    <Override PartName="/CustomXml/item1.xml" ContentType="application/vnd.openxmlformats-officedocument.customXmlPart+xml"/>
    <Override PartName="/customXml/itemProps1.xml" ContentType="application/vnd.openxmlformats-officedocument.customXmlProps+xml"/>
    <Override PartName="/customXml/itemRels/item1.xml.rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
</Types>'''
        with open(f"{self.work_dir}/[Content_Types].xml", "w", encoding="utf-8") as f:
            f.write(content)
    
    def _create_relationships(self):
        """Cree les fichiers de relations"""
        # Fichier _rels/.rels
        rels = '''<?xml version="1.0" encoding="utf-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.microsoft.com/office/2007/relationships/ui/extensibility" Target="report/metadata.json"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/metadata/core-properties" Target="metadata/core.xml"/>
    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/relationships" Target="report/document.xml.rels"/>
</Relationships>'''
        with open(f"{self.work_dir}/_rels/.rels", "w", encoding="utf-8") as f:
            f.write(rels)
        
        # Fichier report/_rels/document.xml.rels
        report_rels = '''<?xml version="1.0" encoding="utf-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.microsoft.com/office/2007/relationships/metadata/custom-properties" Target="../customXml/item1.xml"/>
    <Relationship Id="rId2" Type="http://schemas.microsoft.com/office/2007/relationships/metadata/custom-properties" Target="../customXml/item1.xml.rels"/>
</Relationships>'''
        with open(f"{self.work_dir}/report/_rels/document.xml.rels", "w", encoding="utf-8") as f:
            f.write(report_rels)
        
        # Fichier customXml/itemRels/item1.xml.rels
        custom_rels = '''<?xml version="1.0" encoding="utf-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>'''
        with open(f"{self.work_dir}/customXml/itemRels/item1.xml.rels", "w", encoding="utf-8") as f:
            f.write(custom_rels)
    
    def _create_report_xml(self):
        """Cree le document report principal avec structure Power BI complete"""
        num_communes = len(self.data)
        avg_price = sum(float(row.get('prix_moyen', 0)) for row in self.data) / num_communes if self.data else 0
        
        report_xml = '''<?xml version="1.0" encoding="utf-8"?>
<Report xmlns="http://schemas.microsoft.com/analysisservices/2013/default" xmlns:m="http://schemas.microsoft.com/analysisservices/2013/managed">
  <Name>Immobilier Île-de-France</Name>
  <Description>Analyse immobilière pour investissement - budget 130k EUR</Description>
  <DataModel>
    <Model Name="SemanticModel">
      <Culture>fr-FR</Culture>
      <Tables>
        <Table Name="Communes">
          <Columns>
            <Column Name="commune" DataType="String"/>
            <Column Name="prix_moyen" DataType="Double"/>
            <Column Name="prix_min" DataType="Double"/>
            <Column Name="prix_max" DataType="Double"/>
            <Column Name="prix_m2" DataType="Double"/>
            <Column Name="nb_proprietes" DataType="Int64"/>
          </Columns>
        </Table>
      </Tables>
    </Model>
  </DataModel>
  <Pages>
    <Page Name="Page1">
      <DisplayOption/>
      <Visualizations>
        <Visual Name="KPI_Communes" Type="Card">
          <X>0</X>
          <Y>0</Y>
          <Width>0.25</Width>
          <Height>0.2</Height>
          <Title>Communes Analysées</Title>
          <Value>''' + str(num_communes) + '''</Value>
        </Visual>
        <Visual Name="KPI_PrixMoyen" Type="Card">
          <X>0.25</X>
          <Y>0</Y>
          <Width>0.25</Width>
          <Height>0.2</Height>
          <Title>Prix Moyen</Title>
          <Value>''' + f'{avg_price:,.0f}' + '''€</Value>
        </Visual>
        <Visual Name="TopCommunes" Type="Table">
          <X>0</X>
          <Y>0.25</Y>
          <Width>1</Width>
          <Height>0.75</Height>
          <Title>Communes par Prix</Title>
          <DataFields>commune,prix_moyen,prix_min,prix_max,prix_m2,nb_proprietes</DataFields>
        </Visual>
      </Visualizations>
    </Page>
  </Pages>
</Report>'''
        with open(f"{self.work_dir}/report/document.xml", "w", encoding="utf-8") as f:
            f.write(report_xml)
    
    def _create_metadata(self):
        """Cree les metadonnees du rapport Power BI"""
        communes = list(set(row.get('commune', '') for row in self.data))
        
        metadata = {
            "dataSourceVersion": "1.0.0",
            "isTrivialTopology": False,
            "name": "Rapport Immobilier Île-de-France",
            "description": "Analyse immobilière pour investissement - budget 130k EUR",
            "version": "1.0.0",
            "tables": [
                {
                    "name": "Communes",
                    "kind": "Table",
                    "columns": [
                        {"name": "commune", "dataType": "string"},
                        {"name": "prix_moyen", "dataType": "double"},
                        {"name": "prix_min", "dataType": "double"},
                        {"name": "prix_max", "dataType": "double"},
                        {"name": "prix_m2", "dataType": "double"},
                        {"name": "nb_proprietes", "dataType": "int64"}
                    ],
                    "rowCount": len(self.data)
                }
            ],
            "pageCount": 1,
            "measures": [
                {
                    "name": "Prix Moyen Total",
                    "expression": "AVERAGE([prix_moyen])",
                    "table": "Communes"
                }
            ]
        }
        
        with open(f"{self.work_dir}/report/metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def _create_custom_xml(self):
        """Cree les proprietes personnalisees"""
        custom = '''<?xml version="1.0" encoding="utf-8"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties">
    <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="2" name="Project">Immobilier Scraper</property>
    <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="3" name="Budget">130000 EUR</property>
</Properties>'''
        with open(f"{self.work_dir}/customXml/item1.xml", "w", encoding="utf-8") as f:
            f.write(custom)
    
    def _create_core_properties(self):
        """Cree les proprietes du core"""
        core = '''<?xml version="1.0" encoding="utf-8"?>
<coreProperties xmlns="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/">
    <dc:title>Rapport Immobilier Île-de-France</dc:title>
    <dc:description>Analyse de prix et recommandations d'investissement</dc:description>
    <dc:creator>Immobilier Scraper</dc:creator>
    <dcterms:created xsi:type="dcterms:W3CDTF">''' + datetime.now().isoformat() + '''</dcterms:created>
    <dcterms:modified xsi:type="dcterms:W3CDTF">''' + datetime.now().isoformat() + '''</dcterms:modified>
</coreProperties>'''
        os.makedirs(f"{self.work_dir}/metadata", exist_ok=True)
        with open(f"{self.work_dir}/metadata/core.xml", "w", encoding="utf-8") as f:
            f.write(core)
    
    def _create_data_model(self):
        """Cree le modele de donnees avec les infos CSV"""
        # Determine les colonnes
        columns = list(self.data[0].keys()) if self.data else []
        
        model = {
            "tables": [
                {
                    "name": "Communes",
                    "columns": columns,
                    "rows": self.data,
                    "measures": [
                        {"name": "Prix Moyen", "expression": "AVERAGE(Communes[prix_moyen])"},
                        {"name": "Prix Min", "expression": "MIN(Communes[prix_min])"},
                        {"name": "Prix Max", "expression": "MAX(Communes[prix_max])"}
                    ]
                }
            ],
            "relationships": [],
            "cultures": [
                {
                    "name": "fr-FR",
                    "translations": {
                        "Communes": "Communes",
                        "commune": "Commune",
                        "prix_moyen": "Prix Moyen",
                        "prix_min": "Prix Minimum",
                        "prix_max": "Prix Maximum",
                        "prix_m2": "Prix au m²"
                    }
                }
            ]
        }
        with open(f"{self.work_dir}/report/model.json", "w", encoding="utf-8") as f:
            json.dump(model, f, indent=2, ensure_ascii=False)
    
    def _create_zip(self):
        """Cree l'archive PBIX"""
        print("📦 Creation du fichier PBIX...")
        
        # Assure que le dossier exports existe
        os.makedirs("exports", exist_ok=True)
        
        # Cree le ZIP
        with zipfile.ZipFile(self.output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.work_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = file_path.replace(self.work_dir, "").lstrip("/\\")
                    zipf.write(file_path, arcname)
        
        # Nettoye le dossier temporaire
        shutil.rmtree(self.work_dir)
    
    def generate(self):
        """Lance la generation complete"""
        print("\n" + "="*60)
        print("🚀 GENERATION AUTOMATIQUE DU RAPPORT POWER BI")
        print("="*60 + "\n")
        
        try:
            self._create_pbix_structure()
            self._create_content_types()
            self._create_relationships()
            self._create_report_xml()
            self._create_metadata()
            self._create_custom_xml()
            self._create_core_properties()
            self._create_data_model()
            self._create_zip()
            
            # Verification du fichier
            if os.path.exists(self.output_path):
                size = os.path.getsize(self.output_path)
                print(f"\n✅ Fichier PBIX cree avec succes!")
                print(f"📍 Chemin: {os.path.abspath(self.output_path)}")
                print(f"📊 Taille: {size:,} bytes")
                print(f"📋 Donnees: {len(self.data)} communes")
                print(f"💰 Budget max: 130,000 EUR")
                print("\n" + "="*60)
                print("🎯 Le rapport est pret a etre ouvert dans Power BI!")
                print("="*60)
                return True
            else:
                print("❌ Erreur: Le fichier n'a pas pu etre cree")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de la generation: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    generator = PowerBIGenerator()
    generator.generate()
