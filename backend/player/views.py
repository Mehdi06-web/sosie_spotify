from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import LikedSong, History
from music.models import Song

class RecordPlayView(View):
    """Enregistre une écoute (incrémente le compteur et ajoute à l'historique)"""
    def post(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        
        # Incrémenter le compteur global
        song.nb_ecoutes += 1
        song.save(update_fields=['nb_ecoutes'])
        
        # Ajouter à l'historique si connecté
        if request.user.is_authenticated:
            History.objects.create(utilisateur=request.user, song=song)
            
        return JsonResponse({'status': 'ok', 'nb_ecoutes': song.nb_ecoutes})


@method_decorator(login_required, name='dispatch')
class ToggleLikeView(View):
    """Like ou Dislike une chanson"""
    def post(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        liked_song, created = LikedSong.objects.get_or_create(
            utilisateur=request.user,
            song=song
        )
        
        if not created:
            # Si ça existait déjà, on le supprime (unlike)
            liked_song.delete()
            is_liked = False
        else:
            is_liked = True
            
        return JsonResponse({'status': 'ok', 'is_liked': is_liked})


@method_decorator(login_required, name='dispatch')
class LikedSongsListView(ListView):
    """Affiche la liste des titres likés"""
    model = LikedSong
    template_name = 'player/liked_songs.html'
    context_object_name = 'liked_songs'
    
    def get_queryset(self):
        return LikedSong.objects.filter(
            utilisateur=self.request.user
        ).select_related('song', 'song__artiste', 'song__album', 'song__genre')
