from django.db import models
from django.conf import settings
from music.models import Song

class LikedSong(models.Model):
    """Titres likés par un utilisateur"""
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='liked_songs'
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Titre liké"
        verbose_name_plural = "Titres likés"
        unique_together = ('utilisateur', 'song')
        ordering = ['-date_ajout']

    def __str__(self):
        return f"{self.utilisateur.username} aime {self.song.titre}"


class History(models.Model):
    """Historique d'écoute d'un utilisateur"""
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='history'
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE
    )
    date_ecoute = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historique d'écoute"
        verbose_name_plural = "Historiques d'écoutes"
        ordering = ['-date_ecoute']

    def __str__(self):
        return f"{self.utilisateur.username} a écouté {self.song.titre}"
