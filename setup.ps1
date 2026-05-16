# ============================================================
#   SOSIE SPOTIFY - Script de configuration automatique
#   Atelier 1 : Mise en oeuvre du projet Django
# ============================================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   SOSIE SPOTIFY - Setup de l'environnement" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Etape 1 : Autoriser les scripts PowerShell
Write-Host "[1/7] Configuration des permissions PowerShell..." -ForegroundColor Yellow
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
Write-Host "     OK" -ForegroundColor Green

# Etape 2 : Installer virtualenv
Write-Host "[2/7] Installation de virtualenv..." -ForegroundColor Yellow
pip install virtualenv
Write-Host "     OK" -ForegroundColor Green

# Etape 3 : Creer l'environnement virtuel
Write-Host "[3/7] Creation de l'environnement virtuel..." -ForegroundColor Yellow
virtualenv venv
Write-Host "     OK" -ForegroundColor Green

# Etape 4 : Activer l'environnement virtuel
Write-Host "[4/7] Activation de l'environnement virtuel..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "     OK" -ForegroundColor Green

# Etape 5 : Installer Django et dependances
Write-Host "[5/7] Installation de Django et dependances..." -ForegroundColor Yellow
pip install django pillow mutagen django-crispy-forms
Write-Host "     OK" -ForegroundColor Green

# Etape 6 : Creer le projet Django 'backend'
Write-Host "[6/7] Creation du projet Django 'backend'..." -ForegroundColor Yellow
django-admin startproject backend
Write-Host "     OK" -ForegroundColor Green

# Etape 7 : Creer les applications Django
Write-Host "[7/7] Creation des applications Django..." -ForegroundColor Yellow
Set-Location backend
python manage.py startapp base
python manage.py startapp music
python manage.py startapp users
python manage.py startapp playlists
python manage.py startapp player
Set-Location ..
Write-Host "     OK" -ForegroundColor Green

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "   Setup termine avec succes !" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Structure creee :" -ForegroundColor Cyan
Write-Host "  sosie_spotify/" -ForegroundColor White
Write-Host "  ├── venv/              (environnement virtuel)" -ForegroundColor Gray
Write-Host "  └── backend/           (projet Django)" -ForegroundColor White
Write-Host "      ├── backend/       (configuration)" -ForegroundColor Gray
Write-Host "      ├── base/          (layout commun, navbar)" -ForegroundColor Gray
Write-Host "      ├── music/         (chansons, albums, artistes)" -ForegroundColor Gray
Write-Host "      ├── users/         (authentification)" -ForegroundColor Gray
Write-Host "      ├── playlists/     (gestion des playlists)" -ForegroundColor Gray
Write-Host "      └── player/        (lecteur, historique)" -ForegroundColor Gray
Write-Host ""
Write-Host "Prochaine etape : cd backend && python manage.py runserver" -ForegroundColor Yellow
