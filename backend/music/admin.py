from django.contrib import admin
from .models import Genre, Artiste, Album, Song


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)


@admin.register(Artiste)
class ArtisteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'pays', 'date_creation')
    search_fields = ('nom', 'pays')
    list_filter = ('pays',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('titre', 'artiste', 'annee_sortie')
    search_fields = ('titre', 'artiste__nom')
    list_filter = ('annee_sortie', 'artiste')


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('titre', 'artiste', 'album', 'genre', 'duree', 'nb_ecoutes', 'date_ajout')
    search_fields = ('titre', 'artiste__nom', 'album__titre')
    list_filter = ('genre', 'artiste', 'album')
    readonly_fields = ('nb_ecoutes', 'date_ajout')
