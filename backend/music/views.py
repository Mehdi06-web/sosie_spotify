from django.views.generic import ListView, DetailView
from django.views import View
from django.shortcuts import render
from .models import Song, Artiste, Album, Genre


class MusicListView(ListView):
    """Vue générique pour afficher la liste des chansons"""
    model = Song
    template_name = 'music/music_list.html'
    context_object_name = 'songs'
    paginate_by = 20

    def get_queryset(self):
        queryset = Song.objects.select_related('artiste', 'album', 'genre').all()
        # Filtrage par genre
        genre_id = self.request.GET.get('genre')
        if genre_id:
            queryset = queryset.filter(genre_id=genre_id)
        # Recherche
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(titre__icontains=search) | \
                       queryset.filter(artiste__nom__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = 'Catalogue Musical'
        context['genres'] = Genre.objects.all()
        context['genre_actif'] = self.request.GET.get('genre', '')
        context['search'] = self.request.GET.get('q', '')
        return context


class SongDetailView(DetailView):
    """Vue générique pour afficher les détails d'une chanson"""
    model = Song
    template_name = 'music/song_detail.html'
    context_object_name = 'song'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        song = self.get_object()
        # Chansons similaires du même artiste
        context['songs_similaires'] = Song.objects.filter(
            artiste=song.artiste
        ).exclude(pk=song.pk)[:5]
        return context


class ArtisteListView(ListView):
    """Vue pour afficher la liste des artistes"""
    model = Artiste
    template_name = 'music/artiste_list.html'
    context_object_name = 'artistes'


class ArtisteDetailView(DetailView):
    """Vue pour afficher les détails d'un artiste"""
    model = Artiste
    template_name = 'music/artiste_detail.html'
    context_object_name = 'artiste'


class AlbumListView(ListView):
    """Vue pour afficher la liste des albums"""
    model = Album
    template_name = 'music/album_list.html'
    context_object_name = 'albums'


class AlbumDetailView(DetailView):
    """Vue pour afficher les détails d'un album"""
    model = Album
    template_name = 'music/album_detail.html'
    context_object_name = 'album'


class SearchView(View):
    """Vue pour la recherche globale (chansons, artistes, albums)"""
    def get(self, request):
        query = request.GET.get('q', '')
        songs = []
        artistes = []
        albums = []
        
        if query:
            songs = Song.objects.filter(titre__icontains=query).select_related('artiste', 'album', 'genre')[:12]
            artistes = Artiste.objects.filter(nom__icontains=query)[:6]
            albums = Album.objects.filter(titre__icontains=query).select_related('artiste')[:6]
            
        return render(request, 'music/search.html', {
            'query': query,
            'songs': songs,
            'artistes': artistes,
            'albums': albums,
        })


class SearchSuggestionsView(View):
    """Vue pour l'autocomplete HTMX de la recherche"""
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if len(query) < 2:
            return render(request, 'music/search_suggestions.html', {'query': query})
            
        songs = Song.objects.filter(titre__icontains=query).select_related('artiste', 'album')[:4]
        artistes = Artiste.objects.filter(nom__icontains=query)[:3]
        
        return render(request, 'music/search_suggestions.html', {
            'query': query,
            'songs': songs,
            'artistes': artistes,
        })
