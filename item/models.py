from django.conf import settings
from django.db import models
from user.models import User
from PIL import Image
from io import BytesIO  #
from django.core.files.base import ContentFile  #
from cloudinary.models import CloudinaryField
import cloudinary.uploader


class CardItems(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Meta:
    app_label = "base"


class Item(models.Model):
    card = models.ForeignKey(CardItems, related_name="items", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    if settings.DEBUG:
        image = models.ImageField(upload_to="img")
    else:
        image = CloudinaryField("img")
    description = models.TextField(max_length=2555)
    popularity = models.IntegerField(default=0)
    length = models.DecimalField(
        max_digits=2, decimal_places=0, help_text="Length in centimeters"
    )
    width = models.DecimalField(
        max_digits=2, decimal_places=0, help_text="Width in centimeters"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=0)
    is_available = models.BooleanField(default=True)

    @property
    def user(self):
        return self.card.user

    def save(self, *args, **kwargs):
        if self.image and settings.DEBUG:
            if hasattr(self, "_original_image") and self.image.name != self._original_image:
                img = Image.open(self.image.path)
                img.save(self.image.path)
            self._original_image = self.image.name

        super().save(*args, **kwargs)
