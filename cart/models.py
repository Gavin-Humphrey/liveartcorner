from django.db import models
from item.models import Item
from user.models import User




class DeliveryMethod(models.Model):
    method = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2) 


class DiscountCode(models.Model):
    code = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField(blank=True, null=True)  # Optional expiration date
    active = models.BooleanField(default=True)  # Track active/inactive status


    def __str__(self):
        return self.code 
    

  
class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.name}"
        else:
            return "Guest Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)



