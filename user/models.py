from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .managers import CustomUserManager
import datetime
from datetime import timedelta



class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    username = models.CharField(max_length=150, default="")
    is_artist = models.BooleanField(default=False) 
    is_vetted_artist = models.BooleanField(default=False) 
    phone_number = models.CharField(max_length=15, blank=True, default='') #
    street_address = models.CharField(max_length=255, blank=True, default='') #
    city = models.CharField(max_length=100, blank=True, default='') #
    postal_code = models.CharField(max_length=20, blank=True, default='') #
    country = models.CharField(max_length=100, blank=True, default='') #

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'phone_number', 'street_address', 'city', 'postal_code', 'country'] #
    #REQUIRED_FIELDS = []

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
    


class ArtistAvailability(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    booked = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.artist} - Available on {self.date} from {self.start_time} to {self.end_time}"
