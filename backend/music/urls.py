from django.urls import path
from .views import MusicListView, SongDetailView, ArtisteListView, ArtisteDetailView, AlbumListView, AlbumDetailView, SearchView, SearchSuggestionsView

app_name = 'music'

urlpatterns = [
    path('', MusicListView.as_view(), name='music_list'),
    path('search/', SearchView.as_view(), name='search'),
    path('search/suggestions/', SearchSuggestionsView.as_view(), name='search_suggestions'),
    path('song/<int:pk>/', SongDetailView.as_view(), name='song_detail'),
    path('artistes/', ArtisteListView.as_view(), name='artiste_list'),
    path('artiste/<int:pk>/', ArtisteDetailView.as_view(), name='artiste_detail'),
    path('albums/', AlbumListView.as_view(), name='album_list'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),
]
