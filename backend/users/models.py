from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Modèle utilisateur personnalisé pour Sosie Spotify"""

    bio = models.TextField(blank=True, null=True, verbose_name="Biographie")
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Photo de profil"
    )
    date_naissance = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de naissance"
    )
    is_artiste = models.BooleanField(
        default=False,
        verbose_name="Est un artiste"
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.username} ({self.email})"
