# api/urls.py
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, MovieViewSet, PersonListCreateView, PersonDetailView, DirectorListView, \
    ActorListView, MovieCreateView, MovieListView, MovieDetailView, MovieUpdateView, MovieDeleteView, GenreListView, \
    RegisterView, LoginView, LogoutView, CurrentUserView

router = DefaultRouter()
router.register(r'people', PersonViewSet)
router.register(r'movies', MovieViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),

    path('people/', PersonListCreateView.as_view(), name='person-list-create'),
    path('people/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),
    path('people/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),  # PUT požadavek bude směřován sem
    path('directors/', DirectorListView.as_view(), name='director-list'),
    path('actors/', ActorListView.as_view(), name='actor-list'),  # Nová URL pro herce
    path('people/<str:pk>/', PersonDetailView.as_view(), name='person-detail'),

    path('movies/', MovieCreateView.as_view(), name='movie-create'),  # Cesta pro vytváření filmu
    path('api/movies/', MovieListView.as_view(), name='movie-list'),
    path('api/movies/<str:movie_id>/', MovieDetailView.as_view(), name='movie-detail'),
    path('api/movies/<str:movie_id>/', MovieUpdateView.as_view(), name='movie-update'),
    path('api/movies/<str:movie_id>/', MovieDeleteView.as_view(), name='movie-delete'),

    path('genres/', GenreListView.as_view(), name='genre-list'),  # Odkazuje na URL

    path('user/', RegisterView.as_view(), name='register'),
    path('auth/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),  # Nová URL pro odhlášení
    path('auth/me/', CurrentUserView.as_view(), name='current-user'),  # Nová URL pro aktuálního uživatele

]


