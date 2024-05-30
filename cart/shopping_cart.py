from django.shortcuts import get_object_or_404
from .models import CartItem
from item.models import Item
from decimal import Decimal
from .models import DeliveryMethod, DiscountCode, Cart

from django.http import Http404



class CartHandler:
    def __init__(self, request):
        self.request = request
        self.user = request.user if request.user.is_authenticated else None
        if self.user:
            # Fetch or create the user's shopping cart
            self.cart, created = Cart.objects.get_or_create(user=self.user)
            # Fetch cart items associated with the user's shopping cart
            self.cart_items = CartItem.objects.filter(cart=self.cart)
        else:
            # Anonymous user
            if 'cart' in request.session:
                cart_id = request.session['cart']
                try:
                    self.cart = Cart.objects.get(pk=cart_id)
                except Cart.DoesNotExist:
                    self.cart = Cart.objects.create()
                    request.session['cart'] = self.cart.pk
            else:
                self.cart = Cart.objects.create()
                request.session['cart'] = self.cart.pk
            self.cart_items = CartItem.objects.filter(cart=self.cart)

    def add_to_cart(self, item, quantity):
        cart_item, created = CartItem.objects.get_or_create(cart=self.cart, item=item)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

    def remove_item(self, item_id):
        item_id = str(item_id)
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
        items = []
        for cart_item in self.cart_items:
            items.append({
                'item': cart_item.item,
                'quantity': cart_item.quantity,
                'id': cart_item.item.id  #  using item ID here
            })
        return items
    
  
    def get_cart_items_count(self):
        return sum(cart_item.quantity for cart_item in self.cart_items)


    def calculate_sub_total(self):
        # Ensure iteration over the correct attribute: self.cart_items
        sub_total = sum(item.item.price * item.quantity for item in self.cart_items)
        return sub_total
    

    def choose_delivery(self, selected_delivery_method_id):
        try:
            delivery_method = get_object_or_404(DeliveryMethod, id=selected_delivery_method_id)
            print("Chosen Delivery Method:", delivery_method)  # Debug print statement
            return delivery_method
        except Http404 as e:
            print("Error retrieving delivery method:", e)  # Debug print statement
            return None


    def add_discount(self, discount_code):
        try:
            # Retrieve the discount code based on the provided ID
            discount_code_obj = get_object_or_404(DiscountCode, code=discount_code)
            # Return the value of the discount code
            return discount_code_obj
        except DiscountCode.DoesNotExist:
            return Decimal('0.00') 
    
    def calculate_total_with_delivery(self, selected_delivery_method_id, discount_code_id):
        sub_total = self.calculate_sub_total()
        delivery_method = get_object_or_404(DeliveryMethod, id=selected_delivery_method_id)
        delivery_cost = delivery_method.cost
        total_cost = sub_total + delivery_cost
 
        if discount_code_id:
            try:
                discount_code = get_object_or_404(DiscountCode, code=discount_code_id)
                discount_code_value = discount_code.value
                total_cost -= discount_code_value
            except Exception as e:
                # If any exception occurs, return the specific error message
                return "Invalid code: Discount code not found"
        return total_cost
    


    def clear_cart(self):
        # Delete all cart items associated with the current user session
        self.cart_items.delete()

