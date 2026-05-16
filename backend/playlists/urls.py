from django.urls import path
from .views import (
    PlaylistListView,
    PlaylistDetailView,
    PlaylistCreateView,
    PlaylistAddSongView,
    PlaylistRemoveSongView,
    PlaylistDeleteView,
    LibraryView,
)

app_name = 'playlists'

urlpatterns = [
    path('',                              PlaylistListView.as_view(),       name='playlist_list'),
    path('create/',                       PlaylistCreateView.as_view(),     name='playlist_create'),
    path('<int:pk>/',                     PlaylistDetailView.as_view(),     name='playlist_detail'),
    path('<int:pk>/add-song/',            PlaylistAddSongView.as_view(),    name='playlist_add_song'),
    path('<int:pk>/remove/<int:item_pk>/',PlaylistRemoveSongView.as_view(), name='playlist_remove_song'),
    path('<int:pk>/delete/',              PlaylistDeleteView.as_view(),     name='playlist_delete'),
    path('library/',                      LibraryView.as_view(),            name='library'),
]
