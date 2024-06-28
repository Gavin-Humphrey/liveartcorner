from django.db import models
from user.models import User
from item.models import Item
from cart.models import DeliveryMethod, DiscountCode


class DeliveryInfo(models.Model):
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)


class Order(models.Model):
    # Associate orders with a user (authenticated) or a guest user (unauthenticated)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    # Add a field to indicate the order type (e.g., 'guest', 'authenticated')
    order_type = models.CharField(max_length=20)
    items = models.ManyToManyField(Item, through="OrderItem")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_method = models.ForeignKey(
        DeliveryMethod, on_delete=models.SET_NULL, null=True
    )
    order_status = models.CharField(max_length=50, default="Pending")
    delivery_info = models.OneToOneField(
        DeliveryInfo, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.email if self.user else 'Guest'}"


class GuestUser(models.Model):
    # Define a special user account for unauthenticated users (guest users)
    is_guest = True

    def __str__(self):
        return "Guest User"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_code = models.ForeignKey(
        DiscountCode, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.quantity} x {self.item.title} ({self.order.user.email})"

    def get_total_cost(self):
        return self.quantity * self.item.price
