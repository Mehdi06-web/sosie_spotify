from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from .models import Playlist, PlaylistItem
from music.models import Song


class PlaylistListView(View):
    """Liste des playlists publiques + playlists de l'utilisateur connecté"""

    def get(self, request):
        # Playlists publiques
        playlists_publiques = Playlist.objects.filter(
            est_publique=True
        ).select_related('utilisateur').order_by('-date_creation')

        # Playlists de l'utilisateur connecté
        mes_playlists = []
        if request.user.is_authenticated:
            mes_playlists = Playlist.objects.filter(
                utilisateur=request.user
            ).order_by('-date_creation')

        return render(request, 'playlists/playlist_list.html', {
            'playlists_publiques': playlists_publiques,
            'mes_playlists': mes_playlists,
        })


class PlaylistDetailView(View):
    """Détail d'une playlist avec ses chansons"""

    def get(self, request, pk):
        playlist = get_object_or_404(Playlist, pk=pk)

        # Vérification accès : publique ou propriétaire
        if not playlist.est_publique and playlist.utilisateur != request.user:
            messages.error(request, 'Cette playlist est privée.')
            return redirect('playlists:playlist_list')

        items = playlist.items.select_related('song', 'song__artiste', 'song__genre').order_by('ordre', 'date_ajout')

        # Chansons disponibles à ajouter (pour le formulaire)
        songs_disponibles = None
        if request.user == playlist.utilisateur:
            # Exclure les chansons déjà dans la playlist
            songs_dans_playlist = playlist.items.values_list('song_id', flat=True)
            songs_disponibles = Song.objects.exclude(
                id__in=songs_dans_playlist
            ).select_related('artiste')[:50]

        return render(request, 'playlists/playlist_detail.html', {
            'playlist': playlist,
            'items': items,
            'songs_disponibles': songs_disponibles,
        })


@method_decorator(login_required, name='dispatch')
class PlaylistCreateView(View):
    """Créer une nouvelle playlist"""

    def get(self, request):
        return render(request, 'playlists/playlist_create.html')

    def post(self, request):
        nom         = request.POST.get('nom', '').strip()
        description = request.POST.get('description', '').strip()
        est_publique = request.POST.get('est_publique') == 'on'

        if not nom:
            messages.error(request, 'Le nom de la playlist est requis.')
            return render(request, 'playlists/playlist_create.html', {
                'nom': nom,
                'description': description,
            })

        playlist = Playlist.objects.create(
            nom=nom,
            description=description,
            utilisateur=request.user,
            est_publique=est_publique,
        )
        messages.success(request, f'Playlist « {nom} » créée avec succès ! 🎵')
        return redirect('playlists:playlist_detail', pk=playlist.pk)


@method_decorator(login_required, name='dispatch')
class PlaylistAddSongView(View):
    """Ajouter une chanson à une playlist"""

    def post(self, request, pk):
        playlist = get_object_or_404(Playlist, pk=pk, utilisateur=request.user)
        song_id  = request.POST.get('song_id')

        if not song_id:
            messages.error(request, 'Chanson introuvable.')
            return redirect('playlists:playlist_detail', pk=pk)

        song = get_object_or_404(Song, pk=song_id)

        # Calculer le prochain ordre
        dernier_ordre = playlist.items.count()

        item, created = PlaylistItem.objects.get_or_create(
            playlist=playlist,
            song=song,
            defaults={'ordre': dernier_ordre + 1}
        )

        if created:
            messages.success(request, f'« {song.titre} » ajouté à la playlist !')
        else:
            messages.info(request, f'« {song.titre} » est déjà dans cette playlist.')

        return redirect('playlists:playlist_detail', pk=pk)


@method_decorator(login_required, name='dispatch')
class PlaylistRemoveSongView(View):
    """Retirer une chanson d'une playlist"""

    def post(self, request, pk, item_pk):
        playlist = get_object_or_404(Playlist, pk=pk, utilisateur=request.user)
        item     = get_object_or_404(PlaylistItem, pk=item_pk, playlist=playlist)
        titre    = item.song.titre
        item.delete()
        messages.success(request, f'« {titre} » retiré de la playlist.')
        return redirect('playlists:playlist_detail', pk=pk)


@method_decorator(login_required, name='dispatch')
class PlaylistDeleteView(View):
    """Supprimer une playlist"""

    def post(self, request, pk):
        playlist = get_object_or_404(Playlist, pk=pk, utilisateur=request.user)
        nom = playlist.nom
        playlist.delete()
        messages.success(request, f'Playlist « {nom} » supprimée.')
        return redirect('playlists:playlist_list')


@method_decorator(login_required, name='dispatch')
class LibraryView(View):
    """Ma Bibliothèque (Playlists + stats)"""
    def get(self, request):
        mes_playlists = Playlist.objects.filter(utilisateur=request.user).order_by('-date_creation')
        nb_likes = request.user.liked_songs.count()
        return render(request, 'playlists/library.html', {
            'mes_playlists': mes_playlists,
            'nb_likes': nb_likes
        })
