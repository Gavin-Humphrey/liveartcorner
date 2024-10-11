from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from item.models import Item, CardItems
from ..models import Cart, CartItem, DeliveryMethod

User = get_user_model()


class CartViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass"
        )

        # Create a CardItems instance associated with the user
        self.card_items = CardItems.objects.create(user=self.user)

        # Create a test item
        self.item = Item.objects.create(
            title="Test Item",
            quantity=10,
            price=20.0,
            length=5,
            width=5,
            card=self.card_items,
        )

    def test_view_cart_anonymous(self):
        response = self.client.get(reverse("view-cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/cart.html")

    def test_view_cart_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("view-cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/cart.html")

    def test_remove_from_cart_authenticated(self):
        self.client.force_login(self.user)
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, item=self.item)

        response = self.client.post(
            reverse("remove-from-cart", kwargs={"item_id": self.item.pk})
        )
        self.assertEqual(response.status_code, 302)  # Assuming a redirect after removal
        self.assertFalse(
            CartItem.objects.filter(id=cart_item.id).exists()
        )  # Check item is removed

    def test_add_to_cart_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("add-to-cart", kwargs={"item_id": self.item.pk})
        )
        self.assertEqual(response.status_code, 302)
        cart = Cart.objects.get(user=self.user)
        self.assertTrue(CartItem.objects.filter(cart=cart, item=self.item).exists())

    def test_add_to_cart_anonymous(self):
        response = self.client.post(
            reverse("add-to-cart", kwargs={"item_id": self.item.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_add_existing_item_to_cart_authenticated(self):
        self.client.force_login(self.user)
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, item=self.item)  # Add item first

        response = self.client.post(
            reverse("add-to-cart", kwargs={"item_id": self.item.pk}),
            data={"confirm": True},
        )
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertEqual(
            CartItem.objects.filter(item=self.item, cart__user=self.user).count(), 2
        )  # Item count should be 2

    def test_update_cart_item_delivery_method_authenticated(self):
        self.client.force_login(self.user)
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, item=self.item)

        # Create a delivery method
        delivery_method = DeliveryMethod.objects.create(method="Standard", cost=5.0)

        # Ensure that the cart item has a delivery method to update
        response = self.client.post(
            reverse("update-cart"),
            {
                "cart_item_id": cart_item.id,
                "selected_delivery_method_id": delivery_method.id,
            },
        )

        # Expecting a redirect to another page
        self.assertEqual(
            response.status_code, 302
        )  # Changed to 302 if redirection is expected
        cart_item.refresh_from_db()
        self.assertEqual(
            cart_item.delivery_method.id, delivery_method.id
        )  # Verify if the delivery method is set

    def test_view_cart_empty_message(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("view-cart"))
        self.assertContains(
            response, "Your cart is empty."
        )  # Ensure empty message is shown

    def test_view_cart_warning_if_delivery_method_not_selected(self):
        self.client.force_login(self.user)
        cart = Cart.objects.create(user=self.user)

        # Create a test item with an associated image
        item_with_image = Item.objects.create(
            title="Test Item with Image",
            quantity=0,
            price=20.0,
            length=5,
            width=5,
            card=self.card_items,
            image="path/to/image.jpg",
        )

        cart_item = CartItem.objects.create(cart=cart, item=item_with_image)

        response = self.client.get(reverse("view-cart"))
        self.assertContains(
            response,
            "Please select a delivery method for all items before proceeding to checkout.",
        )  # Check warning message

    def test_add_to_cart_invalid_item(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("add-to-cart", kwargs={"item_id": 999})
        )  # Non-existing item
        self.assertEqual(response.status_code, 404)  # Should return a 404 status

    def test_update_cart_item_invalid_id(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("update-cart"), {"cart_item_id": 999}
        )  # Non-existing cart item
        self.assertEqual(response.status_code, 302)  # Should redirect
