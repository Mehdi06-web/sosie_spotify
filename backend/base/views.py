from django.views import View
from django.shortcuts import render
from music.models import Song


class HomeView(View):
    """Vue principale de la page d'accueil Sosie Spotify"""

    def get(self, request):
        top_songs = Song.objects.select_related('artiste', 'album', 'genre').order_by('-nb_ecoutes')[:4]
        
        context = {
            'titre': 'Sosie Spotify',
            'message': 'Bienvenue sur Sosie Spotify 🎵',
            'top_songs': top_songs,
        }
        return render(request, 'base/home.html', context)
