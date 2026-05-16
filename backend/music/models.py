from django.db import models


class Genre(models.Model):
    """Genre musical (Pop, Rock, Jazz, etc.)"""
    nom = models.CharField(max_length=100, unique=True, verbose_name="Genre")
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Artiste(models.Model):
    """Artiste ou groupe musical"""
    nom = models.CharField(max_length=200, verbose_name="Nom de l'artiste")
    bio = models.TextField(blank=True, null=True, verbose_name="Biographie")
    photo = models.ImageField(
        upload_to='artistes/',
        blank=True,
        null=True,
        verbose_name="Photo"
    )
    pays = models.CharField(max_length=100, blank=True, null=True, verbose_name="Pays")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Artiste"
        verbose_name_plural = "Artistes"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Album(models.Model):
    """Album musical"""
    titre = models.CharField(max_length=200, verbose_name="Titre de l'album")
    artiste = models.ForeignKey(
        Artiste,
        on_delete=models.CASCADE,
        related_name='albums',
        verbose_name="Artiste"
    )
    pochette = models.ImageField(
        upload_to='albums/',
        blank=True,
        null=True,
        verbose_name="Pochette"
    )
    annee_sortie = models.IntegerField(verbose_name="Année de sortie", blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Albums"
        ordering = ['-annee_sortie']

    def __str__(self):
        return f"{self.titre} - {self.artiste.nom}"


class Song(models.Model):
    """Chanson / Morceau de musique"""
    titre = models.CharField(max_length=200, verbose_name="Titre")
    artiste = models.ForeignKey(
        Artiste,
        on_delete=models.CASCADE,
        related_name='songs',
        verbose_name="Artiste"
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='songs',
        verbose_name="Album"
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='songs',
        verbose_name="Genre"
    )
    fichier_audio = models.FileField(
        upload_to='songs/',
        blank=True,
        null=True,
        verbose_name="Fichier audio (MP3)"
    )
    pochette = models.ImageField(
        upload_to='songs/pochettes/',
        blank=True,
        null=True,
        verbose_name="Pochette de la chanson"
    )
    duree = models.IntegerField(
        default=0,
        verbose_name="Durée (secondes)"
    )
    nb_ecoutes = models.IntegerField(default=0, verbose_name="Nombre d'écoutes")
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")

    class Meta:
        verbose_name = "Chanson"
        verbose_name_plural = "Chansons"
        ordering = ['-date_ajout']

    def __str__(self):
        return f"{self.titre} - {self.artiste.nom}"

    def get_duree_formatee(self):
        """Retourne la durée au format MM:SS"""
        minutes = self.duree // 60
        secondes = self.duree % 60
        return f"{minutes}:{secondes:02d}"
