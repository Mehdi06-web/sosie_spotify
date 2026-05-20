import os
import random
import re
from django.conf import settings
from django.core.management.base import BaseCommand
from music.models import Song, Album, Artiste


class Command(BaseCommand):
    help = 'Assigne des fichiers audio et des pochettes existants aux chansons et albums'

    ARTIST_NAMES = [
        'Jul', 'SCH', 'SDM', 'Ninho', 'Gazo',
        'PLK', 'Naps', 'Lomepal', 'Damso', 'Booba'
    ]

    KEYWORD_ARTISTS = {
        'jul': 'Jul',
        'sch': 'SCH',
        'sdm': 'SDM',
        'ninho': 'Ninho',
        'gazo': 'Gazo',
        'plk': 'PLK',
        'naps': 'Naps',
        'lomepal': 'Lomepal',
        'damso': 'Damso',
        'booba': 'Booba',
    }

    def handle(self, *args, **options):
        songs_dir = os.path.join(settings.MEDIA_ROOT, 'songs')
        cover_dir = os.path.join(songs_dir, 'pochettes')

        if not os.path.isdir(songs_dir):
            self.stderr.write(self.style.ERROR(f"Le dossier media n'existe pas: {songs_dir}"))
            return
        if not os.path.isdir(cover_dir):
            self.stderr.write(self.style.ERROR(f"Le dossier de pochettes n'existe pas: {cover_dir}"))
            return

        audio_files = sorted([
            f for f in os.listdir(songs_dir)
            if os.path.isfile(os.path.join(songs_dir, f))
            and f.lower().endswith(('.mp3', '.m4a', '.wav', '.ogg'))
        ])
        cover_files = sorted([
            f for f in os.listdir(cover_dir)
            if os.path.isfile(os.path.join(cover_dir, f))
            and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
        ])

        if not audio_files:
            self.stderr.write(self.style.ERROR('Aucun fichier audio trouvé dans media/songs/'))
            return
        if not cover_files:
            self.stderr.write(self.style.ERROR('Aucune pochette trouvée dans media/songs/pochettes/'))
            return

        self._ensure_artistes()
        artists = {art.nom.lower(): art for art in Artiste.objects.all()}
        songs = list(Song.objects.all().order_by('id'))
        albums = list(Album.objects.all().order_by('id'))

        self._assign_audio_and_titles(songs, audio_files, artists)
        self._assign_album_covers(albums, cover_files)

        self.stdout.write(self.style.SUCCESS('Mise à jour des fichiers médias terminée.'))

    def _ensure_artistes(self):
        artistes = list(Artiste.objects.all().order_by('id'))
        for index, name in enumerate(self.ARTIST_NAMES):
            if index < len(artistes):
                artiste = artistes[index]
                artiste.nom = name
                artiste.bio = artiste.bio or 'Artiste de rap français.'
                artiste.pays = 'France'
                artiste.save(update_fields=['nom', 'bio', 'pays'])
            else:
                Artiste.objects.create(
                    nom=name,
                    bio='Artiste de rap français.',
                    pays='France',
                )

    def _clean_title(self, filename):
        title = os.path.splitext(filename)[0]
        title = title.replace('_', ' ')
        title = re.sub(r'\s+', ' ', title).strip()
        title = re.sub(r'(?i)( clip officiel| clip| official| audio| audio officiel| version| live| lyrics| video)$', '', title)
        title = re.sub(r'(?i)feat\.?\s+[^-]+', '', title)
        title = re.sub(r'(?i)ft\.?\s+[^-]+', '', title)
        title = re.sub(r'(?i)\s+-\s+$', '', title)
        title = re.sub(r'(?i)^(jul|sch|sdm|ninho|gazo|plk|naps|lomepal|damso|booba)\s*[-_]+\s*', '', title)
        return title.strip()

    def _find_artist(self, filename, artists):
        base = filename.lower()
        for keyword, name in self.KEYWORD_ARTISTS.items():
            if keyword in base and name.lower() in artists:
                return artists[name.lower()]
        return random.choice(list(artists.values()))

    def _assign_audio_and_titles(self, songs, audio_files, artists):
        if not songs:
            self.stdout.write('Aucune chanson en base à mettre à jour.')
            return

        if len(audio_files) < len(songs):
            self.stdout.write(self.style.WARNING(
                'Il y a moins de fichiers audio que de chansons. Les premières chansons seront mises à jour en priorité.'
            ))

        self.stdout.write(f"Assignation de fichiers audio réels pour {len(songs)} chansons...")
        for index, song in enumerate(songs):
            if index >= len(audio_files):
                break
            filename = audio_files[index]
            song.fichier_audio = os.path.join('songs', filename)
            song.titre = self._clean_title(filename)
            assigned_artist = self._find_artist(filename, artists)
            song.artiste = assigned_artist
            song.save(update_fields=['fichier_audio', 'titre', 'artiste'])

        self.stdout.write(self.style.SUCCESS('Fichiers audio réels assignés.'))

    def _assign_album_covers(self, albums, cover_files):
        if not albums:
            self.stdout.write('Aucun album en base à mettre à jour.')
            return

        self.stdout.write(f"Assignation de pochettes aux {len(albums)} albums...")
        for index, album in enumerate(albums):
            cover_filename = cover_files[index % len(cover_files)]
            album.pochette = os.path.join('songs', 'pochettes', cover_filename)
            album.save(update_fields=['pochette'])

        self.stdout.write(self.style.SUCCESS('Pochettes assignées aux albums.'))
