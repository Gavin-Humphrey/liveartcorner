# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from item.models import Item, CardItems
# from ..models import Cart, CartItem

# User = get_user_model()

# class CartViewsTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(username='testuser', email='test@example.com')
#         self.card_items = CardItems.objects.create(user=self.user)
#         self.item = Item.objects.create(title='Test Item', quantity=10, price=20.0, length=5, width=5, card=self.card_items)

#     def test_view_cart_anonymous(self):
#         response = self.client.get(reverse('cart:view_cart'))
#         self.assertEqual(response.status_code, 200)
#         # Add assertions for anonymous users accessing the cart view

#     def test_view_cart_authenticated(self):
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('cart:view_cart'))
#         self.assertEqual(response.status_code, 200)
#         # Add assertions for authenticated users accessing the cart view

#     def test_remove_from_cart_authenticated(self):
#         self.client.force_login(self.user)
#         cart = Cart.objects.create(user=self.user)
#         cart_item = CartItem.objects.create(cart=cart, item=self.item, quantity=1)
#         # Add assertions for removing items from the cart for authenticated users

#     def test_remove_from_cart_anonymous(self):
#         response = self.client.post(reverse('cart:remove_from_cart'), {'item_id': self.item.pk})
#         self.assertEqual(response.status_code, 302)
#         # Add assertions for removing items from the cart for anonymous users

#     def test_add_to_cart_authenticated(self):
#         self.client.force_login(self.user)
#         response = self.client.post(reverse('cart:add_to_cart'), {'item_id': self.item.pk})
#         self.assertEqual(response.status_code, 302)
#         # Add assertions for adding items to the cart for authenticated users

#     def test_add_to_cart_anonymous(self):
#         response = self.client.post(reverse('cart:add_to_cart'), {'item_id': self.item.pk})
#         self.assertEqual(response.status_code, 302)
#         # Add assertions for adding items to the cart for anonymous users


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from item.models import Item, CardItems
from ..models import Cart, CartItem

User = get_user_model()

class CartViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.card_items = CardItems.objects.create(user=self.user)
        self.item = Item.objects.create(title='Test Item', quantity=10, price=20.0, length=5, width=5, card=self.card_items)

    def test_view_cart_anonymous(self):
        response = self.client.get(reverse('view-cart'))
        self.assertEqual(response.status_code, 200)
        # Add assertions for anonymous users accessing the cart view

    def test_view_cart_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('view-cart'))
        self.assertEqual(response.status_code, 200)
        # Add assertions for authenticated users accessing the cart view

    def test_remove_from_cart_authenticated(self):
        self.client.force_login(self.user)
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, item=self.item, quantity=1)
        # Add assertions for removing items from the cart for authenticated users


    ###### TEST ANONYMOUS USER REMOVE ITEM LATER    


    def test_add_to_cart_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('add-to-cart', kwargs={'item_id': self.item.pk}))
        self.assertEqual(response.status_code, 302)
        # Add assertions for adding items to the cart for authenticated users

    def test_add_to_cart_anonymous(self):
        response = self.client.post(reverse('add-to-cart', kwargs={'item_id': self.item.pk}))
        self.assertEqual(response.status_code, 302)
        # Add assertions for adding items to the cart for anonymous users

