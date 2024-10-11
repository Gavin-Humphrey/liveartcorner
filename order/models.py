from django.db import models
from user.models import User
from item.models import Item
from cart.models import CartItem, DeliveryMethod, DiscountCode


class DeliveryInfo(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.full_name}, {self.email}, {self.address}, {self.city}, {self.postcode}, {self.country}, {self.phone_number}"


class Order(models.Model):
    # Associate orders with a user (authenticated) or a guest user (unauthenticated)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    # Add a field to indicate the order type (e.g., 'guest', 'authenticated')
    order_type = models.CharField(max_length=20)
    items = models.ManyToManyField(Item, through="OrderItem")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=50, default="Pending")
    delivery_info = models.OneToOneField(
        DeliveryInfo, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order N° {self.pk} - {self.user.email if self.user else 'Guest'}"


class GuestUser(models.Model):
    # Define a special user account for unauthenticated users (guest users)
    is_guest = True

    def __str__(self):
        return "Guest User"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    delivery_method = models.ForeignKey(
        DeliveryMethod, null=True, on_delete=models.SET_NULL
    )  # Store delivery method
    discount_code = models.ForeignKey(
        DiscountCode, null=True, blank=True, on_delete=models.SET_NULL
    )  # Store discount code
    item_total_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )  # Store total cost of the item in the order

    def __str__(self):
        if self.item:
            return f"{self.item.title} - Total Cost: ${self.item_total_cost:.2f} (Order ID: {self.order.id})"
        return f"OrderItem #{self.id} (No associated Item)"

    def get_cart_item(self):
        return self.cart_item
