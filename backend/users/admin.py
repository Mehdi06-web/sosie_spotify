from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Interface d'administration pour CustomUser"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_artiste', 'is_staff')
    list_filter = ('is_artiste', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    fieldsets = UserAdmin.fieldsets + (
        ('Profil Spotify', {
            'fields': ('bio', 'avatar', 'date_naissance', 'is_artiste')
        }),
    )
