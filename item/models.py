from django.db import models
from user.models import User
from PIL import Image





class CardItems(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
class Meta:
        app_label = 'base'



class Item(models.Model):
    card = models.ForeignKey(CardItems, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='img')
    description = models.TextField(max_length=2555)
    popularity = models.IntegerField(default=5)
    length = models.DecimalField(max_digits=2, decimal_places=0, help_text="Length in centimeters")
    width = models.DecimalField(max_digits=2, decimal_places=0, help_text="Width in centimeters")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=0)


    @property
    def user(self):
        return self.card.user
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the model instance first

        if self.image:
            # Open the uploaded image using Pillow
            img = Image.open(self.image.path)
            # Get the current aspect ratio
            aspect_ratio = img.width / img.height

            # Set the target width and height for resizing
            target_width = 300
            target_height = int(target_width / aspect_ratio)

            # Resize the image while maintaining aspect ratio
            resized_img = img.resize((target_width, target_height))

            # Save the resized image back to the model
            img_format = img.format
            img_path = self.image.path
            resized_img.save(img_path, format=img_format)
