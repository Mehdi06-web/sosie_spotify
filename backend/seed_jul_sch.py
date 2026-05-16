import os
import django
import urllib.request
import tempfile

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

def main():
    print("🧹 Nettoyage de la base de données...")
    Song.objects.all().delete()
    Album.objects.all().delete()
    Artiste.objects.all().delete()
    Genre.objects.all().delete()

    print("🎵 Création des genres...")
    rap, _ = Genre.objects.get_or_create(nom="Rap Français")
    
    print("🎤 Création des artistes (Jul, SCH)...")
    jul = Artiste.objects.create(nom="Jul", pays="France", bio="Le J, c'est le S.")
    sch = Artiste.objects.create(nom="SCH", pays="France", bio="Le S, JVLIVS.")

    print("📸 Ajout des photos d'artistes...")
    # Utilisation des images locales générées
    jul_img_path = r"C:\Users\mehdi\.gemini\antigravity\brain\8f71850b-7dbb-4f01-bb2a-233025ff1a21\jul_photo_1778288360254.png"
    sch_img_path = r"C:\Users\mehdi\.gemini\antigravity\brain\8f71850b-7dbb-4f01-bb2a-233025ff1a21\sch_photo_1778288381401.png"

    if os.path.exists(jul_img_path):
        with open(jul_img_path, 'rb') as f:
            jul.photo.save('jul.png', File(f), save=True)
            
    if os.path.exists(sch_img_path):
        with open(sch_img_path, 'rb') as f:
            sch.photo.save('sch.png', File(f), save=True)

    print("💿 Création des albums...")
    album_jul = Album.objects.create(titre="Demain ça ira", artiste=jul, annee_sortie=2021)
    album_sch = Album.objects.create(titre="JVLIVS II", artiste=sch, annee_sortie=2021)
    album_bande = Album.objects.create(titre="13 Organisé", artiste=jul, annee_sortie=2020)

    print("🖼️ Ajout des pochettes d'albums...")
    cover_13_path = r"C:\Users\mehdi\.gemini\antigravity\brain\8f71850b-7dbb-4f01-bb2a-233025ff1a21\album_13_1778288393742.png"
    cover_jul_path = r"C:\Users\mehdi\.gemini\antigravity\brain\8f71850b-7dbb-4f01-bb2a-233025ff1a21\album_jul_1778288409302.png"
    cover_sch_path = r"C:\Users\mehdi\.gemini\antigravity\brain\8f71850b-7dbb-4f01-bb2a-233025ff1a21\album_sch_1778288423990.png"

    if os.path.exists(cover_13_path):
        with open(cover_13_path, 'rb') as f:
            album_bande.pochette.save('13_organise.png', File(f), save=True)

    if os.path.exists(cover_jul_path):
        with open(cover_jul_path, 'rb') as f:
            album_jul.pochette.save('demain_ca_ira.png', File(f), save=True)

    if os.path.exists(cover_sch_path):
        with open(cover_sch_path, 'rb') as f:
            album_sch.pochette.save('jvlivs_2.png', File(f), save=True)

    print("🎶 Création des morceaux...")
    mp3_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

    songs_data = [
        {"titre": "Bande Organisée", "artiste": jul, "album": album_bande, "genre": rap, "duree": 357},
        {"titre": "Pic et Pic, Alcool et Drame", "artiste": jul, "album": album_jul, "genre": rap, "duree": 210},
        {"titre": "JCVD", "artiste": jul, "album": None, "genre": rap, "duree": 195},
        {"titre": "Marché Noir", "artiste": sch, "album": album_sch, "genre": rap, "duree": 204},
        {"titre": "Loup Noir", "artiste": sch, "album": album_sch, "genre": rap, "duree": 230},
        {"titre": "Fade Up", "artiste": sch, "album": None, "genre": rap, "duree": 180},
    ]

    for data in songs_data:
        song = Song.objects.create(**data)
        print(f"Téléchargement audio pour {song.titre}...")
        path = download_file(mp3_url, '.mp3')
        if path:
            with open(path, 'rb') as f:
                song.fichier_audio.save(f"{song.titre.replace(' ', '_')}.mp3", File(f), save=True)
            os.remove(path)
            
        # Si le morceau n'a pas d'album, on lui met la pochette générique (même que l'album Jul pour l'exemple)
        if not song.album:
            if os.path.exists(cover_jul_path):
                with open(cover_jul_path, 'rb') as f:
                    song.pochette.save(f"pochette_{song.titre.replace(' ', '_')}.png", File(f), save=True)

    print("✅ Base de données mise à jour avec Jul et SCH !")

if __name__ == '__main__':
    main()
