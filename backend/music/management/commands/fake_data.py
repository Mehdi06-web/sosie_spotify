"""
Commande Django pour générer de fausses données musicales avec Faker.
Usage: python manage.py fake_data
"""
import random
from django.core.management.base import BaseCommand
from faker import Faker
from music.models import Genre, Artiste, Album, Song

fake = Faker('fr_FR')

GENRES = ['Pop', 'Rock', 'Jazz', 'Hip-Hop', 'Electronic', 'R&B', 'Classical', 'Reggae', 'Metal', 'Soul']

ARTISTES_CELEBRES = [
    'The Weeknd', 'Taylor Swift', 'Drake', 'Billie Eilish',
    'Ed Sheeran', 'Dua Lipa', 'Post Malone', 'Ariana Grande',
    'Harry Styles', 'Beyoncé', 'Rihanna', 'Bruno Mars',
]


class Command(BaseCommand):
    help = 'Génère de fausses données musicales pour Sosie Spotify'

    def add_arguments(self, parser):
        parser.add_argument('--artistes', type=int, default=10, help='Nombre d\'artistes')
        parser.add_argument('--albums', type=int, default=20, help='Nombre d\'albums')
        parser.add_argument('--songs', type=int, default=50, help='Nombre de chansons')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🎵 Génération des données musicales...'))

        # 1. Créer les genres
        self.stdout.write('  → Création des genres...')
        genres = []
        for nom_genre in GENRES:
            genre, created = Genre.objects.get_or_create(nom=nom_genre)
            genres.append(genre)
        self.stdout.write(self.style.SUCCESS(f'    ✅ {len(genres)} genres créés'))

        # 2. Créer les artistes
        self.stdout.write('  → Création des artistes...')
        artistes = []
        for nom in ARTISTES_CELEBRES[:options['artistes']]:
            artiste, created = Artiste.objects.get_or_create(
                nom=nom,
                defaults={
                    'bio': fake.paragraph(nb_sentences=3),
                    'pays': fake.country(),
                }
            )
            artistes.append(artiste)

        # Artistes supplémentaires avec Faker
        extra = options['artistes'] - len(ARTISTES_CELEBRES)
        for _ in range(max(0, extra)):
            artiste = Artiste.objects.create(
                nom=fake.name(),
                bio=fake.paragraph(nb_sentences=3),
                pays=fake.country(),
            )
            artistes.append(artiste)
        self.stdout.write(self.style.SUCCESS(f'    ✅ {len(artistes)} artistes créés'))

        # 3. Créer les albums
        self.stdout.write('  → Création des albums...')
        albums = []
        for _ in range(options['albums']):
            album = Album.objects.create(
                titre=fake.catch_phrase(),
                artiste=random.choice(artistes),
                annee_sortie=random.randint(2000, 2024),
            )
            albums.append(album)
        self.stdout.write(self.style.SUCCESS(f'    ✅ {len(albums)} albums créés'))

        # 4. Créer les chansons
        self.stdout.write('  → Création des chansons...')
        for _ in range(options['songs']):
            album = random.choice(albums)
            Song.objects.create(
                titre=fake.catch_phrase(),
                artiste=album.artiste,
                album=album,
                genre=random.choice(genres),
                duree=random.randint(120, 360),
                nb_ecoutes=random.randint(0, 1000000),
            )
        self.stdout.write(self.style.SUCCESS(f'    ✅ {options["songs"]} chansons créées'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🎉 Base de données peuplée avec succès !'))
        self.stdout.write(f'   Genres: {Genre.objects.count()}')
        self.stdout.write(f'   Artistes: {Artiste.objects.count()}')
        self.stdout.write(f'   Albums: {Album.objects.count()}')
        self.stdout.write(f'   Chansons: {Song.objects.count()}')
