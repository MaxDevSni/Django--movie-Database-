# api/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Person, Movie, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'is_admin']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'year', 'director', 'actors', 'genres', 'isAvailable', 'dateAdded']


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        # Vytvoření uživatele s heslem
        user = User.objects.create_user(**validated_data)
        return user