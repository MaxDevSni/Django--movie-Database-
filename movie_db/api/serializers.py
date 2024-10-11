# api/serializers.py
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import Person


# Person serializer
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

from rest_framework import serializers
from .models import Movie


# Movie serializer
class MovieSerializer(serializers.ModelSerializer):
    director = serializers.PrimaryKeyRelatedField(queryset=Person.objects.filter(role="director"))  # Použijte 'director' místo 'directorID'
    actors = serializers.PrimaryKeyRelatedField(queryset=Person.objects.filter(role="actor"), many=True)  # Použijte 'actors' místo 'actorIDs'

    class Meta:
        model = Movie
        fields = ['id', 'name', 'year', 'director', 'actors', 'isAvailable', 'genres', 'dateAdded']  # Odpovídající pole

    def create(self, validated_data):
        director = validated_data.pop('director')  # Změňte na 'director'
        actors = validated_data.pop('actors')  # Změňte na 'actors'

        # Vytvoření filmu
        movie = Movie.objects.create(director=director, **validated_data)

        # Přidání herců
        movie.actors.set(actors)
        movie.save()

        return movie





# User serializer
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'is_admin', '_id']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()