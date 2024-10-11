from django.shortcuts import get_object_or_404
from .models import CartItem
from decimal import Decimal
from .models import DeliveryMethod, DiscountCode, Cart
import logging

logger = logging.getLogger(__name__)


class CartHandler:
    def __init__(self, request):
        self.request = request
        self.user = request.user if request.user.is_authenticated else None
        if self.user:
            self.cart, created = Cart.objects.get_or_create(user=self.user)
            self.cart_items = CartItem.objects.filter(cart=self.cart)
        else:
            if "cart" in request.session:
                cart_id = request.session["cart"]
                try:
                    self.cart = Cart.objects.get(pk=cart_id)
                except Cart.DoesNotExist:
                    self.cart = Cart.objects.create()
                    request.session["cart"] = self.cart.pk
            else:
                self.cart = Cart.objects.create()
                request.session["cart"] = self.cart.pk
            self.cart_items = CartItem.objects.filter(cart=self.cart)

    def add_to_cart(self, item):
        cart_item = CartItem.objects.create(cart=self.cart, item=item)
        cart_item.save()

    def remove_item(self, item_id):
        # Using `item_id` here to remove the correct item
        cart_item = get_object_or_404(CartItem, cart=self.cart, item_id=item_id)
        cart_item.delete()

    def update_quantity(self, item_id, quantity):
        item_id = str(item_id)
        cart_item = get_object_or_404(CartItem, cart=self.cart, item_id=item_id)
        cart_item.quantity = quantity
        cart_item.save()

    def save(self):
        self.session.modified = True

    def get_cart_items(self):
        return self.cart_items

    def get_cart_items_count(self):
        return len(self.cart_items)

    def update_cart_item(
        self, cart_item_id, selected_delivery_method_id, discount_code
    ):
        # Find the cart item by referencing CartItem.id directly
        cart_item = self.cart_items.filter(
            id=cart_item_id
        ).first()  # Use CartItem.id instead of item_id

        if not cart_item:
            raise CartItem.DoesNotExist(
                f"CartItem with ID {cart_item_id} does not exist."
            )

        # Update delivery method for the specific cart item
        if selected_delivery_method_id:
            delivery_method = DeliveryMethod.objects.get(id=selected_delivery_method_id)
            cart_item.delivery_method = delivery_method

        # Apply discount code logic (if applicable)
        if discount_code:
            discount_code_obj = DiscountCode.objects.filter(
                code=discount_code, active=True
            ).first()
            if discount_code_obj:
                cart_item.discount_code = discount_code_obj  # Link discount code object
            else:
                raise ValueError("Invalid discount code.")

        cart_item.save()  # Save the changes for this cart item

    def get_cart_item_by_id(self, item_id):
        try:
            return CartItem.objects.get(id=item_id)
        except CartItem.DoesNotExist:
            return None

    def choose_delivery(self, selected_delivery_method_id):
        if selected_delivery_method_id:
            try:
                delivery_method = DeliveryMethod.objects.get(
                    id=selected_delivery_method_id
                )
                return delivery_method
            except DeliveryMethod.DoesNotExist:
                # print(f"Delivery method with ID {selected_delivery_method_id} does not exist.")
                return None
        else:
            # print("No delivery method ID provided.")
            return None

    def add_discount(self, discount_code):
        try:
            # Retrieve the discount code based on the provided code
            discount_code_obj = DiscountCode.objects.get(code=discount_code)
            return discount_code_obj.value
        except DiscountCode.DoesNotExist:
            return Decimal("0.00")  # No discount if code does not exist

    def calculate_item_sub_total(self, item_id):
        item_id = str(item_id)
        cart_item = get_object_or_404(CartItem, cart=self.cart, item_id=item_id)
        item_sub_total = cart_item.item.price
        return item_sub_total

    def calculate_item_total_cost(self, cart_item):
        item = cart_item.item
        item_sub_total = item.price
        delivery_cost = 0

        # Add delivery cost for this specific item
        if cart_item.delivery_method:
            delivery_cost = cart_item.delivery_method.cost

        # Start with the item subtotal plus delivery
        item_total_cost = item_sub_total + delivery_cost

        # Apply discount, if available for this item
        if cart_item.discount_code:
            discount_value = cart_item.discount_code.value
            item_total_cost -= discount_value

        return max(item_total_cost, 0)

    def calculate_sub_total(self):
        # Iteration over the self.cart_items attribute.
        sub_total = sum(item.item.price for item in self.cart_items)
        return sub_total

    def calculate_cart_total_cost(self):
        cart_total_cost = 0
        for cart_item in self.cart_items:
            item_total_cost = self.calculate_item_total_cost(cart_item)
            if isinstance(item_total_cost, str):
                return item_total_cost  # Return the error message if any
            cart_total_cost += item_total_cost
        return cart_total_cost

    def clear_cart(self):
        # Delete all cart items associated with the current user session
        self.cart_items.delete()
