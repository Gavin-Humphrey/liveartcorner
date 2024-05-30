from django.db import models
from django.contrib.auth.models import AbstractUser#, Group, Permission 
from django.conf import settings
from .managers import CustomUserManager




class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    username = models.CharField(max_length=150, default="")
    is_artist = models.BooleanField(default=False) 
    is_vetted_artist = models.BooleanField(default=False) 

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return f"{settings.STATIC_URL}img/avatar.svg"


    def __str__(self):
        return self.name if self.name else self.email
    


class ArtistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='artist_profile_pics', blank=True)
    portfolio_url = models.URLField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    artistic_medium = models.CharField(max_length=100, blank=True)
    experience_education = models.TextField(blank=True)

    def __str__(self):
        return self.user.name if self.user.name else self.user.email