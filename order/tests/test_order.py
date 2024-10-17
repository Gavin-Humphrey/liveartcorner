from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from cart.models import DeliveryMethod
from ..order import create_order
from ..models import Order


from ..models import (
    GuestUser,
)


User = get_user_model()


class OrderProcessTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass"
        )

        # Create a delivery method
        self.delivery_method = DeliveryMethod.objects.create(
            method="Standard Delivery", cost=5.00
        )

    def test_process_delivery_get(self):
        # Test delivery page access as an anonymous user
        response = self.client.get(reverse("process-delivery"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order/process_delivery.html")

    def test_process_delivery_post_authenticated(self):
        self.client.login(username="testuser", password="testpass")

        # Set up session data for delivery method, cost, etc.
        self.client.session["chosen_delivery_method"] = self.delivery_method.id
        self.client.session["delivery_cost"] = 10
        self.client.session["discount_value"] = "0"

        delivery_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "address": "456 Elm St",
            "city": "Anywhere",
            "postal_code": "67890",
        }

        response = self.client.post(reverse("process-delivery"), data=delivery_data)

        # Check for the correct response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order/process_delivery.html")

    def test_process_checkout_post_anonymous(self):
        # Attempt to post checkout data as an anonymous user
        order_data = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "address": "123 Test St",
            "city": "Test City",
            "postcode": "12345",
            "country": "Testland",
            "phone_number": "1234567890",
        }

        response = self.client.post(reverse("process-checkout"), data=order_data)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(
            response, "/login/?next=/process-checkout/"
        )  # Redirects to login

    def test_process_checkout_post_authenticated(self):
        self.client.login(username="testuser", password="testpass")

        # Set up the necessary session data
        self.client.session["chosen_delivery_method"] = self.delivery_method.id
        self.client.session["delivery_cost"] = 10
        self.client.session["discount_value"] = "20"  # Discount used for this test

        # Submit the form with order data
        delivery_data = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "address": "123 Main St",
            "city": "Somewhere",
            "postcode": "12345",
            "country": "Testland",
            "phone_number": "1234567890",
        }

        response = self.client.post(reverse("process-checkout"), data=delivery_data)

        # Check the response for the expected success
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order/checkout.html")

    def test_process_checkout_post_anonymous(self):
        # Attempt to post checkout data as an anonymous user
        order_data = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "address": "123 Test St",
            "city": "Test City",
            "postcode": "12345",
            "country": "Testland",
            "phone_number": "1234567890",
        }

        # Set up the necessary session data for the anonymous user
        self.client.session["chosen_delivery_method"] = self.delivery_method.id
        self.client.session["delivery_cost"] = 10
        self.client.session["discount_value"] = "0"  # No discount for this test

        response = self.client.post(reverse("process-checkout"), data=order_data)

        # Check the response to ensure it processes correctly for an anonymous user
        self.assertEqual(response.status_code, 200)  # Expecting a 200 OK
        self.assertTemplateUsed(response, "order/checkout.html")

    def test_create_order_authenticated(self):
        # Test order creation as an authenticated user
        self.client.login(username="testuser", password="testpass")

        delivery_data = {
            "full_name": "Dave",
            "email": "dave@example.com",
            "address": "101 First St",
            "city": "First City",
            "postcode": "11111",
            "country": "Firstland",
            "phone_number": "8889990000",
            "total_cost": 200.00,
        }
        order = create_order(self.user, delivery_data)  # Pass the user object
        self.assertIsInstance(order, Order)
        self.assertEqual(order.user, self.user)  # Check the order's user
        self.assertEqual(order.total_cost, 200.00)

    def test_create_order_anonymous(self):
        # Create a guest user object
        guest_user = GuestUser.objects.create()

        order_data = {
            "full_name": "Anonymous User",
            # No email field since we are using GuestUser
            "address": "123 Anonymous St",
            "city": "Nowhere",
            "postcode": "00000",
            "country": "Nowhere",
            "phone_number": "9876543210",
        }

        # Set up the necessary session data for the anonymous user
        self.client.session["chosen_delivery_method"] = self.delivery_method.id
        self.client.session["delivery_cost"] = 10
        self.client.session["discount_value"] = "0"

        response = self.client.post(reverse("process-checkout"), data=order_data)

        # Check for a successful response
        self.assertEqual(response.status_code, 200)  # Expecting a 200 OK
        self.assertTemplateUsed(response, "order/checkout.html")
