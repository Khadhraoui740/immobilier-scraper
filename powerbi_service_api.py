#!/usr/bin/env python3
"""
Solution 3: Power BI Service API (Cloud)
Crée un rapport Power BI via l'API REST Microsoft

Installation: pip install msal requests
"""

import json
import requests
from datetime import datetime

class PowerBIServiceAPI:
    """Connecte à Power BI Service pour créer des rapports"""
    
    def __init__(self, tenant_id=None, client_id=None, username=None, password=None):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.username = username
        self.password = password
        self.token = None
        self.api_url = "https://api.powerbi.com/v1.0/myorg"
        
    def authenticate(self):
        """S'authentifie auprès de Power BI Service"""
        print("🔐 Authentification Power BI Service...")
        
        if not all([self.tenant_id, self.client_id, self.username, self.password]):
            print("❌ Informations d'authentification manquantes")
            print("\n📌 Pour utiliser cette solution:")
            print("  1. Inscrivez-vous gratuitement: https://powerbi.microsoft.com")
            print("  2. Enregistrez une app: https://dev.powerbi.com/apps")
            print("  3. Récupérez:")
            print("     - Tenant ID (Azure AD)")
            print("     - Client ID (App ID)")
            print("     - Votre email Microsoft")
            print("     - Votre mot de passe")
            return False
        
        try:
            from msal import PublicClientApplication
            
            app = PublicClientApplication(
                self.client_id,
                authority=f"https://login.microsoftonline.com/{self.tenant_id}"
            )
            
            result = app.acquire_token_by_username_password(
                self.username,
                self.password,
                scopes=["https://analysis.windows.net/powerbi/api/.default"]
            )
            
            if "access_token" in result:
                self.token = result["access_token"]
                print("✅ Authentification réussie!")
                return True
            else:
                print("❌ Erreur:", result.get("error_description"))
                return False
                
        except ImportError:
            print("❌ msal non installé: pip install msal")
            return False
    
    def create_workspace(self, name="Immobilier Analysis"):
        """Crée un nouvel espace de travail"""
        if not self.token:
            print("❌ Non authentifié. Appelez authenticate() d'abord")
            return None
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Vérifier si l'espace existe déjà
        response = requests.get(
            f"{self.api_url}/groups",
            headers=headers
        )
        
        if response.status_code == 200:
            groups = response.json()["value"]
            for group in groups:
                if group["name"] == name:
                    print(f"✅ Espace existant trouvé: {name}")
                    return group["id"]
        
        # Créer nouvel espace
        data = {"name": name}
        response = requests.post(
            f"{self.api_url}/groups",
            headers=headers,
            json=data
        )
        
        if response.status_code == 201:
            workspace_id = response.json()["id"]
            print(f"✅ Espace créé: {name}")
            return workspace_id
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    
    def upload_dataset(self, workspace_id, csv_path, dataset_name="Communes"):
        """Upload un dataset"""
        if not self.token:
            print("❌ Non authentifié")
            return None
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Lire le CSV et le préparer
        with open(csv_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        files = {
            'file': (dataset_name + '.csv', content)
        }
        
        response = requests.post(
            f"{self.api_url}/groups/{workspace_id}/imports?datasetDisplayName={dataset_name}&importConflictHandlerOverride=CreateOrOverwrite",
            headers=headers,
            files=files
        )
        
        if response.status_code == 200:
            print(f"✅ Dataset uploadé: {dataset_name}")
            return response.json()["id"]
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    
    def get_cloudification_status(self):
        """Affiche l'état de configuration Power BI Service"""
        print("\n" + "=" * 60)
        print("☁️  POWER BI SERVICE (Cloud) - CONFIGURATION")
        print("=" * 60)
        print("\n✅ AVANTAGES:")
        print("  • Accessible partout (pas besoin de Power BI Desktop)")
        print("  • Partageable facilement avec les collègues")
        print("  • Version cloud = toujours à jour")
        print("  • Gratuit jusqu'à 10 GB")
        print("\n⚠️  AVANT DE COMMENCER:")
        print("  1. Créez un compte Microsoft (gratuit)")
        print("  2. Inscrivez-vous à Power BI: https://powerbi.microsoft.com")
        print("  3. Téléchargez Power BI Desktop (gratuit)")
        print("  4. Dans Desktop: Fichier → Publier → Sélectionnez workspace")
        print("\n📍 PLAN D'ACTION:")
        print("  Phase 1: Créer rapport auprès Power BI Desktop (méthode 2)")
        print("  Phase 2: Publier vers Power BI Service (cloud)")
        print("  Phase 3: Inviter collègues à consulter le rapport")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("📊 POWER BI SERVICE API - SETUP")
    print("=" * 60)
    
    api = PowerBIServiceAPI()
    api.get_cloudification_status()
    
    print("\n" + "=" * 60)
    print("💡 RECOMMANDATION POUR VOUS:")
    print("=" * 60)
    print("\nÉtape 1: Utilisez la Méthode 2 (Automation Guide)")
    print("  → Crée le rapport dans Power BI Desktop")
    print("\nÉtape 2: Publiez dans Power BI Service")
    print("  → Depuis Desktop: Fichier → Publier")
    print("\nÉtape 3: Partagez le lien à vos collègues")
    print("  → Pas besoin de Power BI Desktop chez eux!")
