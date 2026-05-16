from django.db import models
from django.conf import settings
from music.models import Song


class Playlist(models.Model):
    """Playlist créée par un utilisateur"""
    nom = models.CharField(max_length=200, verbose_name="Nom de la playlist")
    description = models.TextField(blank=True, null=True)
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='playlists',
        verbose_name="Utilisateur"
    )
    est_publique = models.BooleanField(default=True, verbose_name="Publique")
    pochette = models.ImageField(
        upload_to='playlists/',
        blank=True,
        null=True,
        verbose_name="Image"
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Playlist"
        verbose_name_plural = "Playlists"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.nom} ({self.utilisateur.username})"

    def nb_chansons(self):
        return self.items.count()


class PlaylistItem(models.Model):
    """Chanson ajoutée à une playlist"""
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Playlist"
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='playlist_items',
        verbose_name="Chanson"
    )
    ordre = models.IntegerField(default=0, verbose_name="Ordre")
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Item de Playlist"
        verbose_name_plural = "Items de Playlist"
        ordering = ['ordre', 'date_ajout']
        unique_together = ('playlist', 'song')

    def __str__(self):
        return f"{self.playlist.nom} → {self.song.titre}"
