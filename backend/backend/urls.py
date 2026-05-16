"""
URL configuration for backend project (Sosie Spotify).
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),              # Page d'accueil
    path('music/', include('music.urls')),       # Catalogue musical
    path('users/', include('users.urls')),       # Authentification
    path('playlists/', include('playlists.urls')), # Playlists
    path('player/', include('player.urls')),     # Player (Likes, Historique)
    path('serviceworker.js', TemplateView.as_view(template_name='serviceworker.js', content_type='application/javascript'), name='serviceworker'),
]

# Servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
