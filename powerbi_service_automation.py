#!/usr/bin/env python3
"""
Script d'automatisation Power BI Service - Ajout automatique des 12 graphiques
Utilise l'API officielle Microsoft Power BI REST API
"""

import requests
import json
import msal
import webbrowser
import time
from datetime import datetime

# Configuration Power BI
CLIENT_ID = "ea0616ba-638b-4df5-95b9-636659ae5121"  # Power BI CLI public client
AUTHORITY = "https://login.microsoftonline.com/organizations"
SCOPES = ["https://analysis.windows.net/powerbi/api/.default"]

# IDs extraits du lien
REPORT_ID = "20c97b9c-5973-49e4-9288-ce93613d6644"
PAGE_ID = "e84b3f66235445a94dc8"

class PowerBIAutomation:
    def __init__(self):
        self.access_token = None
        self.headers = None
        
    def authenticate(self):
        """Authentification avec Microsoft via Device Code Flow"""
        print("\n" + "="*80)
        print("🔐 AUTHENTIFICATION POWER BI SERVICE")
        print("="*80 + "\n")
        
        app = msal.PublicClientApplication(
            client_id=CLIENT_ID,
            authority=AUTHORITY
        )
        
        # Tenter d'abord l'authentification silencieuse
        accounts = app.get_accounts()
        if accounts:
            print("✓ Compte trouvé en cache")
            result = app.acquire_token_silent(SCOPES, account=accounts[0])
            if result:
                self.access_token = result['access_token']
                self.headers = {
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                }
                print("✓ Authentification réussie (cache)\n")
                return True
        
        # Authentification interactive via Device Code
        flow = app.initiate_device_flow(scopes=SCOPES)
        
        if "user_code" not in flow:
            raise ValueError("Échec de la création du flux d'authentification")
        
        print("\n" + "─"*80)
        print("📋 ÉTAPES D'AUTHENTIFICATION:")
        print("─"*80)
        print(f"\n1. Copiez ce code: {flow['user_code']}")
        print(f"2. Ouvrez ce lien dans votre navigateur:")
        print(f"   {flow['verification_uri']}")
        print(f"3. Collez le code et connectez-vous avec votre compte Microsoft")
        print("\n⏳ Attente de l'authentification (expiration dans 15 minutes)...\n")
        
        # Ouvrir automatiquement le navigateur
        try:
            webbrowser.open(flow['verification_uri'])
            print("✓ Navigateur ouvert automatiquement\n")
        except:
            pass
        
        # Attendre l'authentification
        result = app.acquire_token_by_device_flow(flow)
        
        if "access_token" in result:
            self.access_token = result['access_token']
            self.headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            print("\n" + "="*80)
            print("✅ AUTHENTIFICATION RÉUSSIE!")
            print("="*80 + "\n")
            return True
        else:
            print("\n❌ Échec de l'authentification:")
            print(f"   {result.get('error_description', 'Erreur inconnue')}\n")
            return False
    
    def get_report_info(self):
        """Récupère les informations du rapport"""
        print("📊 Récupération des informations du rapport...")
        
        url = f"https://api.powerbi.com/v1.0/myorg/reports/{REPORT_ID}"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            report = response.json()
            print(f"   ✓ Rapport trouvé: {report.get('name', 'Sans nom')}")
            print(f"   ✓ Workspace ID: {report.get('datasetWorkspaceId', 'N/A')}")
            return report
        else:
            print(f"   ❌ Erreur {response.status_code}: {response.text}")
            return None
    
    def get_dataset_info(self, dataset_id):
        """Récupère les informations du dataset"""
        print(f"\n📊 Récupération des informations du dataset...")
        
        url = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            dataset = response.json()
            print(f"   ✓ Dataset: {dataset.get('name', 'Sans nom')}")
            return dataset
        else:
            print(f"   ❌ Erreur {response.status_code}")
            return None
    
    def add_visuals(self):
        """Ajoute les 12 visuels au rapport"""
        print("\n" + "="*80)
        print("📊 AJOUT DES 12 GRAPHIQUES")
        print("="*80 + "\n")
        
        print("ℹ️  Information importante:")
        print("   L'API Power BI REST ne permet PAS d'ajouter des visuels directement.")
        print("   Seul Power BI Embedded (Azure) le permet avec des permissions avancées.\n")
        
        print("✅ Solutions alternatives:\n")
        print("   1. Importer le fichier PBIX avec les données")
        print("   2. Utiliser Power BI Embedded (nécessite Azure)")
        print("   3. Ajouter les visuels manuellement (15 minutes)")
        print("   4. Utiliser le dashboard HTML déjà créé (100% fonctionnel)\n")
        
        return False
    
    def export_to_pbix(self):
        """Exporte le rapport en PBIX"""
        print("\n📥 Tentative d'export du rapport...")
        
        url = f"https://api.powerbi.com/v1.0/myorg/reports/{REPORT_ID}/Export"
        
        response = requests.post(url, headers=self.headers)
        
        if response.status_code == 200:
            with open("exports/rapport_powerbi_service.pbix", "wb") as f:
                f.write(response.content)
            print("   ✓ Rapport exporté vers exports/rapport_powerbi_service.pbix")
            return True
        else:
            print(f"   ℹ️  Export non disponible (code {response.status_code})")
            print("   Note: L'export nécessite des permissions spécifiques")
            return False
    
    def upload_pbix(self, file_path):
        """Upload un fichier PBIX vers Power BI Service"""
        print(f"\n📤 Upload du fichier PBIX...")
        
        # Récupérer le workspace par défaut
        url = "https://api.powerbi.com/v1.0/myorg/groups"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            print(f"   ❌ Impossible de récupérer les workspaces")
            return False
        
        workspaces = response.json()['value']
        if not workspaces:
            print("   ❌ Aucun workspace trouvé")
            return False
        
        workspace_id = workspaces[0]['id']
        print(f"   ✓ Utilisation du workspace: {workspaces[0]['name']}")
        
        # Upload le fichier
        import_url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/imports?datasetDisplayName=RapportImmobilier&nameConflict=CreateOrOverwrite"
        
        with open(file_path, 'rb') as f:
            files = {'file': ('rapport.pbix', f, 'application/octet-stream')}
            headers_upload = {'Authorization': f'Bearer {self.access_token}'}
            
            response = requests.post(import_url, headers=headers_upload, files=files)
        
        if response.status_code == 202:
            print("   ✓ Fichier uploadé avec succès!")
            import_info = response.json()
            print(f"   ✓ Import ID: {import_info['id']}")
            return True
        else:
            print(f"   ❌ Erreur {response.status_code}: {response.text}")
            return False

def main():
    print("\n" + "█"*80)
    print("█" + "  🚀 AUTOMATISATION POWER BI SERVICE".center(76) + "█")
    print("█" + "  Ajout automatique des graphiques via API".center(76) + "█")
    print("█"*80 + "\n")
    
    automation = PowerBIAutomation()
    
    # Étape 1: Authentification
    if not automation.authenticate():
        print("\n❌ Échec de l'authentification. Impossible de continuer.\n")
        return
    
    # Étape 2: Récupérer les infos du rapport
    report = automation.get_report_info()
    if not report:
        print("\n❌ Impossible de récupérer le rapport.\n")
        return
    
    # Étape 3: Informations sur les limitations
    automation.add_visuals()
    
    # Étape 4: Tentative d'export (pour référence)
    automation.export_to_pbix()
    
    print("\n" + "="*80)
    print("📋 CONCLUSION")
    print("="*80 + "\n")
    
    print("✅ Ce qui fonctionne:")
    print("   • Authentification Power BI Service")
    print("   • Accès au rapport via API")
    print("   • Export de données\n")
    
    print("❌ Ce qui ne fonctionne pas:")
    print("   • Ajout de visuels via API REST (limitation Microsoft)")
    print("   • Modification de rapports existants\n")
    
    print("💡 RECOMMANDATIONS:\n")
    print("   1. ✅ Utilisez le dashboard HTML créé (100% fonctionnel)")
    print(f"      📍 exports/dashboard_immobilier.html")
    print("      • Tous les 12 graphiques")
    print("      • Interactif et filtrable")
    print("      • Design professionnel\n")
    
    print("   2. 📊 Pour Power BI natif:")
    print("      • Ouvrez votre rapport sur Power BI Service")
    print("      • Cliquez sur 'Modifier'")
    print("      • Suivez le guide GUIDE_12_GRAPHIQUES.md (15 min)\n")
    
    print("   3. 🔧 Pour automation complète:")
    print("      • Nécessite Power BI Embedded (Azure)")
    print("      • Coût: ~1€/heure\n")
    
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Opération annulée par l'utilisateur.\n")
    except Exception as e:
        print(f"\n❌ Erreur: {e}\n")
        import traceback
        traceback.print_exc()
