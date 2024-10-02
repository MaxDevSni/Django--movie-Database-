# api/urls.py
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, MovieViewSet, UserViewSet, PersonListCreateView, PersonDetailView, DirectorListView, \
    ActorListView, MovieCreateView, MovieListView, MovieDetailView, MovieUpdateView, MovieDeleteView, GenreListView, \
    UserRegistrationView

router = DefaultRouter()
router.register(r'people', PersonViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('people/', PersonListCreateView.as_view(), name='person-list-create'),
    path('people/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),
    path('directors/', DirectorListView.as_view(), name='director-list'),
    path('actors/', ActorListView.as_view(), name='actor-list'),  # Nová URL pro herce
    path('people/<str:pk>/', PersonDetailView.as_view(), name='person-detail'),
    path('movies/', MovieCreateView.as_view(), name='movie-create'),  # Nová cesta pro vytvoření filmu
    path('api/movies/', MovieListView.as_view(), name='movie-list'),
    path('api/movies/<str:movie_id>/', MovieDetailView.as_view(), name='movie-detail'),
    path('api/movies/<str:movie_id>/', MovieUpdateView.as_view(), name='movie-update'),
    path('api/movies/<str:movie_id>/', MovieDeleteView.as_view(), name='movie-delete'),
    path('api/genres/', GenreListView.as_view(), name='genre-list'),
    path('api/user/', UserRegistrationView.as_view(), name='user-registration'),


]


