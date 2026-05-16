@echo off
chcp 65001 > nul
echo ============================================
echo    SOSIE SPOTIFY - Installation Django
echo ============================================
echo.

cd /d "C:\Users\mehdi\Desktop\sosie_spotify"
echo Repertoire courant: %CD%
echo.

echo [ETAPE 1] Verification de Python...
python --version
if errorlevel 1 (
    echo ERREUR: Python non trouve !
    pause
    exit /b 1
)

echo [ETAPE 2] Installation de pip virtualenv...
python -m pip install virtualenv
if errorlevel 1 (
    echo ERREUR: pip a echoue !
    pause
    exit /b 1
)

echo [ETAPE 3] Creation de l environnement virtuel...
python -m virtualenv venv
if errorlevel 1 (
    echo ERREUR: virtualenv a echoue !
    pause
    exit /b 1
)
echo Venv cree avec succes!

echo [ETAPE 4] Activation du venv et installation de Django...
call venv\Scripts\activate.bat
python -m pip install django pillow mutagen
if errorlevel 1 (
    echo ERREUR: Installation Django a echoue !
    pause
    exit /b 1
)

echo [ETAPE 5] Creation du projet Django...
python -m django startproject backend
if errorlevel 1 (
    echo ERREUR: Creation du projet a echoue !
    pause
    exit /b 1
)

echo [ETAPE 6] Creation des applications...
cd backend
python manage.py startapp base
python manage.py startapp music
python manage.py startapp users
python manage.py startapp playlists
python manage.py startapp player
cd ..

echo.
echo ============================================
echo    SUCCES ! Projet cree !
echo ============================================
echo.
echo Pour lancer :
echo   cd backend
echo   python manage.py runserver
echo.
pause
