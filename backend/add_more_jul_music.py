import os
import json
import urllib.request
import urllib.parse
import tempfile
import django

# Initialisation de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.files import File
from music.models import Song, Album, Artiste, Genre

def download_file(url, extension):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
        with urllib.request.urlopen(req) as response, open(temp_file.name, 'wb') as out_file:
            out_file.write(response.read())
        return temp_file.name
    except Exception as e:
        print(f"❌ Erreur téléchargement {url}: {e}")
        return None

def fetch_itunes_songs(artist_name, limit=50):
    print(f"🔍 Recherche de musiques pour {artist_name} sur iTunes API...")
    url = f"https://itunes.apple.com/search?term={urllib.parse.quote(artist_name)}&entity=song&limit={limit}&country=FR"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('results', [])
    except Exception as e:
        print(f"❌ Erreur API iTunes: {e}")
        return []

def main():
    rap, _ = Genre.objects.get_or_create(nom="Rap Français")
    nom_artiste = "Jul"
    
    # Récupérer ou créer l'artiste
    artiste_obj, _ = Artiste.objects.get_or_create(nom=nom_artiste, pays="France")
    
    # Récupérer les données depuis iTunes
    results = fetch_itunes_songs(nom_artiste, limit=50)
    
    added_count = 0
    
    for track in results:
        # Eviter les faux positifs (par ex, Juliet, etc.)
        if track.get('artistName', '').lower() != nom_artiste.lower() and nom_artiste.lower() not in track.get('artistName', '').lower():
            continue
            
        titre = track.get('trackName')
        album_name = track.get('collectionName')
        preview_url = track.get('previewUrl')
        cover_url = track.get('artworkUrl100', '').replace('100x100bb', '600x600bb') # HD cover
        
        if not preview_url:
            continue
            
        # Vérifier si la chanson existe déjà
        if Song.objects.filter(titre=titre, artiste=artiste_obj).exists():
            continue
            
        # Gérer l'album
        album_obj = None
        if album_name:
            album_obj, created = Album.objects.get_or_create(
                titre=album_name,
                artiste=artiste_obj
            )
            # Ajouter la pochette à l'album si nouveau
            if created and cover_url:
                print(f"  🖼️ Téléchargement pochette album: {album_name}")
                cover_path = download_file(cover_url, '.jpg')
                if cover_path:
                    with open(cover_path, 'rb') as f:
                        album_obj.pochette.save(f"{album_name[:20].replace(' ', '_')}.jpg", File(f), save=True)
                    os.remove(cover_path)
        
        # Mettre à jour la photo de l'artiste s'il n'en a pas encore
        if not artiste_obj.photo and cover_url:
            print(f"  📸 Ajout photo artiste {nom_artiste}")
            cover_path = download_file(cover_url, '.jpg')
            if cover_path:
                with open(cover_path, 'rb') as f:
                    artiste_obj.photo.save(f"{nom_artiste.replace(' ', '_')}.jpg", File(f), save=True)
                os.remove(cover_path)

        # Créer la chanson
        print(f"  🎶 Ajout de la chanson : {titre}")
        song = Song.objects.create(
            titre=titre,
            artiste=artiste_obj,
            album=album_obj,
            genre=rap,
            duree=30 # Les previews iTunes font 30 secondes
        )
        
        # Télécharger le fichier audio M4A/MP3
        audio_path = download_file(preview_url, '.m4a')
        if audio_path:
            with open(audio_path, 'rb') as f:
                song.fichier_audio.save(f"{titre[:20].replace(' ', '_')}.m4a", File(f), save=True)
            os.remove(audio_path)
            
        # Si pas d'album, on met la pochette sur la chanson
        if not album_obj and cover_url:
            cover_path = download_file(cover_url, '.jpg')
            if cover_path:
                with open(cover_path, 'rb') as f:
                    song.pochette.save(f"{titre[:20].replace(' ', '_')}.jpg", File(f), save=True)
                os.remove(cover_path)
                
        added_count += 1

    print(f"\n✅ C'EST PRÊT ! {added_count} nouvelles chansons de Jul ont été importées avec succès.")

if __name__ == '__main__':
    main()
