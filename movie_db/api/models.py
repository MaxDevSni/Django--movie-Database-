# api/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Uživatelský model
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)  # Správně hashované heslo
        user.is_admin = is_admin
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        return self.create_user(email, password, is_admin=True)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# Model pro osobu (herec/režisér)
class Person(models.Model):
    ROLE_CHOICES = [
        ('director', 'Director'),
        ('actor', 'Actor'),
    ]
    name = models.CharField(max_length=100)
    birthDate = models.DateField()
    country = models.CharField(max_length=100)
    biography = models.TextField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

# Model pro film
class Movie(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    director = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='directed_movies')  # Odkaz na režiséra
    actors = models.ManyToManyField(Person, related_name='acted_movies')  # Odkaz na herce
    isAvailable = models.BooleanField(default=True)
    genres = models.JSONField()  # Předpokládám, že toto je JSONField
    dateAdded = models.DateTimeField(auto_now_add=True)