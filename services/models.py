from django.db import models
from user.models import User, ArtistAvailability

class Service(models.Model):
    artist = models.ForeignKey(User, related_name='services', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Customer who booked
    availability = models.ForeignKey(ArtistAvailability, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Service being booked (optional)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - Booking for {self.availability} ({self.service})"
    


