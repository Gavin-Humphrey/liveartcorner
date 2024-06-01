from django.db import models
from user.models import User

class Service(models.Model):
    artist = models.ForeignKey(User, related_name='services', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
