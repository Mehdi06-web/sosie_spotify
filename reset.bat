@echo off
chcp 65001 > nul
echo ============================================
echo   RESET MIGRATIONS - Sosie Spotify
echo ============================================
echo.

cd /d "C:\Users\mehdi\Desktop\sosie_spotify\backend"

echo [1] Arret de tous les processus Python...
taskkill /F /IM python.exe /T > nul 2>&1
echo     OK

echo [2] Suppression de la base de donnees...
if exist db.sqlite3 del /F /Q db.sqlite3
echo     OK

echo [3] Suppression des anciennes migrations...
for %%a in (users music playlists player base) do (
    if exist %%a\migrations (
        del /F /Q %%a\migrations\0*.py > nul 2>&1
    )
)
echo     OK

echo [4] Creation des migrations...
call ..\venv\Scripts\activate.bat
python manage.py makemigrations users
python manage.py makemigrations music
python manage.py makemigrations playlists
python manage.py makemigrations player
python manage.py makemigrations
echo     OK

echo [5] Application des migrations...
python manage.py migrate
echo     OK

echo.
echo ============================================
echo   SUCCES ! Base de donnees prete !
echo ============================================
echo.
echo Prochaines etapes :
echo   1. python manage.py createsuperuser
echo   2. python manage.py fake_data
echo   3. python manage.py runserver
echo.
pause
