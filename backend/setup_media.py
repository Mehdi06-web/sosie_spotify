import os
import random
import urllib.request
import tempfile
import sys
from urllib.error import URLError

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from django.core.files import File
from music.models import Song, Album, Artiste

# Sources libres de droits
MP3_URLS = [
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
]

IMAGE_URLS = [
    "https://picsum.photos/id/20/400/400",
    "https://picsum.photos/id/39/400/400",
    "https://picsum.photos/id/45/400/400",
    "https://picsum.photos/id/64/400/400",
    "https://picsum.photos/id/76/400/400",
    "https://picsum.photos/id/99/400/400",
    "https://picsum.photos/id/103/400/400"
]

def download_file(url, extension):
    """Télécharge un fichier temporairement et retourne l'objet File Django"""
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
        urllib.request.urlretrieve(url, temp_file.name)
        return temp_file.name
    except URLError as e:
        print(f"❌ Erreur de téléchargement pour {url}: {e}")
        return None

def main():
    print("🎵 Début du téléchargement des médias...")
    
    # 1. Mise à jour des Artistes
    artistes = Artiste.objects.all()
    print(f"Mise à jour de {artistes.count()} artistes...")
    for artiste in artistes:
        if not artiste.photo:
            img_path = download_file(random.choice(IMAGE_URLS), '.jpg')
            if img_path:
                with open(img_path, 'rb') as f:
                    artiste.photo.save(f'artiste_{artiste.id}.jpg', File(f), save=True)
                os.remove(img_path)

    # 2. Mise à jour des Albums
    albums = Album.objects.all()
    print(f"Mise à jour de {albums.count()} albums...")
    for album in albums:
        if not album.pochette:
            img_path = download_file(random.choice(IMAGE_URLS), '.jpg')
            if img_path:
                with open(img_path, 'rb') as f:
                    album.pochette.save(f'album_{album.id}.jpg', File(f), save=True)
                os.remove(img_path)

    # 3. Mise à jour des Chansons (Songs)
    songs = Song.objects.all()
    print(f"Mise à jour de {songs.count()} chansons...")
    for song in songs:
        if not song.fichier_audio:
            mp3_path = download_file(random.choice(MP3_URLS), '.mp3')
            if mp3_path:
                with open(mp3_path, 'rb') as f:
                    song.fichier_audio.save(f'song_{song.id}.mp3', File(f), save=True)
                os.remove(mp3_path)
                
    print("✅ Terminé ! Ton application Sosie Spotify a maintenant des vrais médias.")

if __name__ == '__main__':
    main()
