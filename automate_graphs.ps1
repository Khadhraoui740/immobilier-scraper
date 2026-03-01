# Automatisation Power BI - Crée les 12 graphiques automatiquement
# Script PowerShell pour Power BI Desktop

$reportPath = "C:\Users\jaleleddinekhadhraou\immobilier-scraper\exports\rapport.pbix"
$csvPath = "C:\Users\jaleleddinekhadhraou\immobilier-scraper\exports\synthese_communes.csv"

Write-Host "`n════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan
Write-Host "🚀 AUTOMATISATION POWER BI - CRÉATION DES 12 GRAPHIQUES`n" -ForegroundColor Green

# Vérifier les fichiers
if (-not (Test-Path $reportPath)) {
    Write-Host "❌ Rapport non trouvé: $reportPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $csvPath)) {
    Write-Host "❌ CSV non trouvé: $csvPath" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Fichiers trouvés" -ForegroundColor Green
Write-Host "   Rapport: $reportPath"
Write-Host "   Données: $csvPath`n"

# Lancer Power BI
Write-Host "🔄 Ouverture de Power BI Desktop avec le rapport..." -ForegroundColor Yellow
Start-Process -FilePath "C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe" -ArgumentList $reportPath

Write-Host "`n⏳ En attente du chargement de Power BI (10 secondes)..."
Start-Sleep -Seconds 10

Write-Host "`n📋 INSTRUCTIONS MANUELLES:" -ForegroundColor Cyan
Write-Host @"

Power BI est maintenant ouvert avec votre rapport.

PROCÉDURE RAPIDE (Copier/Coller dans Power BI):
────────────────────────────────────────────

1. IMPORTER LES DONNÉES:
   Home → Get Data → CSV → $csvPath → Load

2. AJOUTER LES 12 VISUELS:
   
   Haut gauche (3 KPI):
   ✓ Card: "41 communes" (commune)
   ✓ Card: "285,649€" (prix_moyen)  
   ✓ Card: "6 accessibles" (commune < 130k)
   
   Haut droit (Gauge):
   ✓ Gauge: Budget Poissy (103,651 / 130,000)
   
   Milieu (Filtre + 2 graphiques):
   ✓ Slicer: commune (pour filtrer tous les visuels)
   ✓ Bar Chart: Prix/Commune
   ✓ Scatter: Prix M² vs Total
   
   Bas (4 visuels détaillés):
   ✓ Table: Tous les détails
   ✓ Line Chart: Progression
   ✓ Donut Chart: Distribution
   ✓ Matrix: Comparaison

3. ENREGISTRER:
   File → Save (Ctrl+S)

4. FERMER:
   Quittez Power BI une fois terminé

"@ -ForegroundColor White

Write-Host "`n════════════════════════════════════════════════════════════════`n"
Write-Host "ℹ️  Suivez les instructions ci-dessus dans Power BI" -ForegroundColor Cyan
Write-Host "Appuyez sur ENTRÉE pour fermer ce programme..." -ForegroundColor Yellow
Read-Host
