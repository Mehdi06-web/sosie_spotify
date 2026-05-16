# 🎓 Fiche de Révision : Soutenance Sosie Spotify

Cette fiche est ton "Cheat Sheet" pour ta soutenance. Elle contient les concepts clés, les questions probables et les emplacements exacts dans le code pour répondre aux questions de ta prof.

---

## 1. L'Architecture du Projet (Le "Big Picture")
Le projet est développé en **Python** avec le framework **Django**.
Django utilise l'architecture **MVT** (Modèle - Vue - Template) :
*   **Modèle (Model) :** Gère la base de données (SQLite). Définit comment les données sont stockées.
*   **Vue (View) :** Le cerveau du projet en Python. Traite la requête de l'utilisateur, interroge la base de données et renvoie la réponse.
*   **Template (Template) :** L'interface visuelle en HTML/CSS affichée à l'utilisateur.

Le code est divisé en plusieurs "Apps" pour rester propre :
*   `music` : Gère le catalogue (Artistes, Albums, Chansons) et la recherche.
*   `users` : Gère les comptes, l'inscription et la connexion.
*   `playlists` : Gère les favoris et playlists des utilisateurs.

---

## 2. Questions Fréquentes & "Montrez-moi dans le code"

### Q1. "Comment avez-vous créé la base de données pour les chansons ?"
*   **Ta réponse :** "J'ai utilisé les modèles de Django. J'ai créé des tables pour les Artistes, les Albums et les Chansons, en les reliant avec des clés étrangères (`ForeignKey`)."
*   📍 **Où le montrer :** Ouvre `backend/music/models.py`.
*   👉 **Ligne à pointer :** `class Song(models.Model):` (Montre comment `artiste` et `album` sont reliés).

### Q2. "Comment avez-vous géré les différentes pages pour afficher les listes ?"
*   **Ta réponse :** "Pour éviter de répéter du code, j'ai utilisé les Vues Génériques de Django, comme `ListView` pour l'affichage de listes et `DetailView` pour les pages spécifiques."
*   📍 **Où le montrer :** Ouvre `backend/music/views.py`.
*   👉 **Ligne à pointer :** `class MusicListView(ListView):` au début du fichier.

### Q3. "Comment fonctionne la recherche instantanée (l'autocomplete) ?"
*   **Ta réponse :** "J'utilise HTMX. Quand on tape dans la barre, le navigateur envoie discrètement une requête à Django. Django filtre la base de données avec `icontains` et renvoie directement un petit bout de HTML."
*   📍 **Où le montrer :** Ouvre `backend/music/views.py`.
*   👉 **Ligne à pointer :** Tout en bas : `class SearchSuggestionsView(View):`. Montre le code `Song.objects.filter(titre__icontains=query)`.

### Q4. "Comment faire pour que la musique continue quand on change de page ?"
*   **Ta réponse :** "C'est la magie d'HTMX ! Au lieu de faire des liens `href` classiques qui rechargent tout le navigateur, HTMX demande seulement le contenu de la nouvelle page au serveur et remplace uniquement le centre de l'écran. Le lecteur audio, qui est en bas, n'est jamais rechargé et continue de jouer."
*   📍 **Où le montrer :** C'est un concept général, mais tu peux mentionner le `base.html` dans `backend/templates/base/base.html` où le lecteur est fixe.

### Q5. "Où sont déclarées les adresses URL de votre site ?"
*   **Ta réponse :** "Elles sont dans les fichiers `urls.py` de chaque application. Ils relient une adresse (ex: `/search/`) à une 'Vue' Python."
*   📍 **Où le montrer :** Ouvre `backend/music/urls.py` ou `backend/users/urls.py`.
*   👉 **Ligne à pointer :** La liste `urlpatterns = [...]`.

### Q6. "Comment avez-vous rempli votre base avec de vraies musiques ?"
*   **Ta réponse :** "J'ai codé un script Python automatisé qui appelle une API externe (Deezer). Le script télécharge les infos, les mp3 et les pochettes, puis remplit la base de données tout seul."
*   📍 **Où le montrer :** Ouvre le fichier à la racine du backend comme `backend/seed_jul_sch.py`.

---

## 💡 Astuce de survie
Si elle te pointe un fichier au hasard, regarde son nom :
*   `models.py` = Base de données.
*   `views.py` = Logique Python (Cerveau).
*   `urls.py` = Routes Web (Adresses).
*   Un dossier `templates/` = L'affichage HTML.

Respire un bon coup, tu vas cartonner ! 🚀
