# 🎵 Sosie Spotify - Application de Musique Django

Une application de streaming musical inspirée de Spotify, développée avec Python Django.

## 📁 Structure du Projet

```
sosie_spotify/
├── venv/                    # Environnement virtuel Python
├── backend/                 # Projet Django principal
│   ├── backend/             # Configuration Django
│   │   ├── settings.py      # Paramètres du projet
│   │   ├── urls.py          # URLs principales
│   │   └── wsgi.py
│   ├── base/                # App centrale (layout, navbar, footer)
│   ├── music/               # App musique (chansons, albums, artistes)
│   ├── users/               # App utilisateurs (auth, profils)
│   ├── playlists/           # App playlists
│   ├── player/              # App lecteur audio
│   └── manage.py
└── setup.ps1                # Script d'installation automatique
```

## 🚀 Installation

### 1. Lancer le script de setup
```powershell
.\setup.ps1
```

### 2. Activer l'environnement virtuel (à chaque session)
```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Lancer le serveur de développement
```powershell
cd backend
python manage.py runserver
```

Accéder à : http://127.0.0.1:8000

## 📦 Applications Django

| Application | Description |
|-------------|-------------|
| `base` | Layout principal, navbar, footer, composants communs |
| `music` | Chansons, albums, artistes, genres |
| `users` | Authentification, profils utilisateurs |
| `playlists` | Création et gestion des playlists |
| `player` | Lecteur audio, historique d'écoute |

## 🛠️ Technologies

- **Backend**: Python 3.x, Django 4.x
- **Base de données**: SQLite (développement)
- **Frontend**: HTML5, CSS3, JavaScript
- **Médias**: Pillow (images), Mutagen (métadonnées audio)
