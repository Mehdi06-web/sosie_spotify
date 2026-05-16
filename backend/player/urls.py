from django.urls import path
from .views import RecordPlayView, ToggleLikeView, LikedSongsListView

app_name = 'player'

urlpatterns = [
    path('record/<int:song_id>/', RecordPlayView.as_view(), name='record_play'),
    path('like/<int:song_id>/', ToggleLikeView.as_view(), name='toggle_like'),
    path('liked-songs/', LikedSongsListView.as_view(), name='liked_songs'),
]
