from django.contrib import admin
from .models import Playlist, PlaylistItem


class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 1


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('nom', 'utilisateur', 'est_publique', 'nb_chansons', 'date_creation')
    search_fields = ('nom', 'utilisateur__username')
    list_filter = ('est_publique',)
    inlines = [PlaylistItemInline]
