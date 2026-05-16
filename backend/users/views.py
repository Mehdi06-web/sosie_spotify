from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import CustomUser


class LoginView(View):
    """Vue de connexion utilisateur"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('base:home')
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Veuillez remplir tous les champs.')
            return render(request, 'users/login.html', {'username': username})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue, {user.username} ! 🎵')
            next_url = request.GET.get('next', 'base:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
            return render(request, 'users/login.html', {'username': username})


class RegisterView(View):
    """Vue d'inscription d'un nouvel utilisateur"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('base:home')
        return render(request, 'users/register.html')

    def post(self, request):
        username   = request.POST.get('username', '').strip()
        email      = request.POST.get('email', '').strip()
        password1  = request.POST.get('password1', '')
        password2  = request.POST.get('password2', '')

        errors = {}

        # Validations
        if not username:
            errors['username'] = 'Le nom d\'utilisateur est requis.'
        elif CustomUser.objects.filter(username=username).exists():
            errors['username'] = 'Ce nom d\'utilisateur est déjà pris.'

        if not email:
            errors['email'] = 'L\'adresse email est requise.'
        elif CustomUser.objects.filter(email=email).exists():
            errors['email'] = 'Cette adresse email est déjà utilisée.'

        if not password1:
            errors['password1'] = 'Le mot de passe est requis.'
        elif len(password1) < 8:
            errors['password1'] = 'Le mot de passe doit contenir au moins 8 caractères.'

        if password1 != password2:
            errors['password2'] = 'Les mots de passe ne correspondent pas.'

        if errors:
            for msg in errors.values():
                messages.error(request, msg)
            return render(request, 'users/register.html', {
                'username': username,
                'email': email,
                'errors': errors,
            })

        # Créer l'utilisateur
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )
        login(request, user)
        messages.success(request, f'Compte créé avec succès ! Bienvenue {username} 🎉')
        return redirect('base:home')


class LogoutView(View):
    """Vue de déconnexion"""

    def post(self, request):
        logout(request)
        messages.info(request, 'Vous avez été déconnecté.')
        return redirect('base:home')

    def get(self, request):
        # Sécurité : logout uniquement en POST, mais on redirige quand même
        logout(request)
        return redirect('base:home')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    """Vue du profil utilisateur"""

    def get(self, request):
        user = request.user
        nb_likes = user.liked_songs.count()
        nb_ecoutes = user.history.count()
        
        return render(request, 'users/profile.html', {
            'user': user,
            'nb_likes': nb_likes,
            'nb_ecoutes': nb_ecoutes,
        })
