from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.views import APIView

from .models import Person, Movie, User
from .serializers import PersonSerializer, MovieSerializer, UserSerializer, UserRegistrationSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MovieCreateView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class PersonListCreateView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class DirectorListView(APIView):
    def get(self, request):
        limit = request.GET.get('limit')  # Získání parametru limit
        directors = Person.objects.filter(role='director')

        # Použijeme limit, pokud je zadán a je platný
        if limit:
            try:
                limit = int(limit)
                directors = directors[:limit]
            except ValueError:
                return Response({"error": "Limit must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PersonSerializer(directors, many=True)
        return Response(serializer.data)



class ActorListView(APIView):
    def get(self, request):
        limit = request.GET.get('limit')  # Získání parametru limit
        actors = Person.objects.filter(role='actor')

        # Použijeme limit, pokud je zadán a je platný
        if limit:
            try:
                limit = int(limit)
                actors = actors[:limit]
            except ValueError:
                return Response({"error": "Limit must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PersonSerializer(actors, many=True)
        return Response(serializer.data)

class PersonDetailView(APIView):
    # GET požadavek pro ziskani detailu cloveka
    def get(self, request, pk):
        try:
            person = Person.objects.get(pk=pk)
            serializer = PersonSerializer(person)
            return Response(serializer.data)
        except Person.DoesNotExist:
            return Response({"error": "Person not found."}, status=status.HTTP_404_NOT_FOUND)

    # PUT požadavek pro úpravu člověka
    def put(self, request, pk):
        try:
            person = Person.objects.get(pk=pk)  # Najdi osobu podle ID
            serializer = PersonSerializer(person, data=request.data)  # Předáme nová data do serializeru

            if serializer.is_valid():  # Zkontroluj, zda jsou data validní
                serializer.save()  # Ulož nová data
                return Response(serializer.data)  # Vrať aktualizované data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Pokud není validní, vrať chybu
        except Person.DoesNotExist:
            return Response({"error": "Person not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            person = Person.objects.get(pk=pk)
            person_data = {
                "_id": str(person.id),
                "name": person.name,
                "birthDate": person.birthDate,
                "country": person.country,
                "biography": person.biography,
                "role": person.role,
                "__v": person.__v,  # Zde můžeš přizpůsobit podle tvé implementace
            }
            person.delete()  # Odstranění osoby
            return Response(person_data, status=status.HTTP_200_OK)  # Vrať odstraněná data
        except Person.DoesNotExist:
            return Response({"error": "Person not found."}, status=status.HTTP_404_NOT_FOUND)


class MovieListView(APIView):
    def get(self, request):
        # Získání filtrů z query parametrů
        director_id = request.GET.get('directorID')
        actor_id = request.GET.get('actorID')
        genre = request.GET.get('genre')
        from_year = request.GET.get('fromYear')
        to_year = request.GET.get('toYear')
        limit = request.GET.get('limit', 10)  # výchozí limit 10

        # Získání všech filmů
        movies = Movie.objects.all()

        # Aplikace filtrů
        if director_id:
            movies = movies.filter(director_id=director_id)
        if actor_id:
            movies = movies.filter(actors__id=actor_id)  # ManyToManyField
        if genre:
            movies = movies.filter(genres__contains=[genre])  # JSONField
        if from_year:
            movies = movies.filter(year__gte=int(from_year))
        if to_year:
            movies = movies.filter(year__lte=int(to_year))

        # Omezit počet výsledků
        movies = movies[:int(limit)]

        # Serializace dat
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieDetailView(APIView):
    def get(self, request, movie_id):
        try:
            # Získání filmu podle ID
            movie = Movie.objects.get(id=movie_id)

            # Získání režiséra a herců
            director = {
                "_id": str(movie.director.id),
                "name": movie.director.name
            }
            actors = [
                {
                    "_id": str(actor.id),
                    "name": actor.name
                } for actor in movie.actors.all()
            ]

            # Serializace dat
            movie_data = {
                "_id": str(movie.id),
                "name": movie.name,
                "year": movie.year,
                "directorID": str(movie.director.id),
                "actorIDs": [str(actor.id) for actor in movie.actors.all()],
                "genres": movie.genres,
                "isAvailable": movie.isAvailable,
                "dateAdded": movie.dateAdded.isoformat(),
                "__v": movie.__v,
                "director": director,
                "actors": actors
            }

            return Response(movie_data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({"detail": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)




class MovieUpdateView(APIView):
    def put(self, request, movie_id):
        try:
            # Získání filmu podle ID
            movie = Movie.objects.get(id=movie_id)

            # Načtení dat z požadavku
            data = request.data

            # Aktualizace filmu
            movie.name = data.get("name", movie.name)
            movie.year = data.get("year", movie.year)
            movie.isAvailable = data.get("isAvailable", movie.isAvailable)
            movie.genres = data.get("genres", movie.genres)

            # Zpracování režiséra
            director_id = data.get("directorID")
            if director_id:
                try:
                    movie.director = Person.objects.get(id=director_id)
                except Person.DoesNotExist:
                    return Response({"detail": "Director not found."}, status=status.HTTP_404_NOT_FOUND)

            # Zpracování herců
            actor_ids = data.get("actorIDs", [])
            movie.actors.clear()  # Odstraní předchozí herce
            for actor_id in actor_ids:
                try:
                    actor = Person.objects.get(id=actor_id)
                    movie.actors.add(actor)
                except Person.DoesNotExist:
                    return Response({"detail": f"Actor with ID {actor_id} not found."}, status=status.HTTP_404_NOT_FOUND)

            # Uložení změn do databáze
            movie.save()

            # Příprava odpovědi
            movie_data = {
                "_id": str(movie.id),
                "name": movie.name,
                "year": movie.year,
                "directorID": str(movie.director.id),
                "actorIDs": [str(actor.id) for actor in movie.actors.all()],
                "genres": movie.genres,
                "isAvailable": movie.isAvailable,
                "dateAdded": movie.dateAdded.isoformat(),
                "__v": movie.__v,
            }

            return Response(movie_data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({"detail": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)



class MovieDeleteView(APIView):
    def delete(self, request, movie_id):
        try:
            # Získání filmu podle ID
            movie = Movie.objects.get(id=movie_id)

            # Uložení dat pro odpověď
            movie_data = {
                "_id": str(movie.id),
                "name": movie.name,
                "year": movie.year,
                "directorID": str(movie.director.id),
                "actorIDs": [str(actor.id) for actor in movie.actors.all()],
                "genres": movie.genres,
                "isAvailable": movie.isAvailable,
                "dateAdded": movie.dateAdded.isoformat(),
                "__v": movie.__v,
            }

            # Odstranění filmu
            movie.delete()

            # Vrátí odstraněný film jako odpověď
            return Response(movie_data, status=status.HTTP_200_OK)

        except Movie.DoesNotExist:
            return Response({"detail": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)



GENRES = [
    "sci-fi",
    "adventure",
    "action",
    "romantic",
    "animated",
    "comedy"
]

class GenreListView(APIView):
    def get(self, request):
        return Response(GENRES, status=status.HTTP_200_OK)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "email": user.email,
                "isAdmin": user.is_admin,
                "_id": str(user.id),
                "__v": 0
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)