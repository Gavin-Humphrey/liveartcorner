from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class CheckoutProcessTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )

    def test_checkout_process(self):
        # Log in the user
        self.client.login(username="testuser", password="password")

        # Make a GET request to the process-checkout URL
        response = self.client.get(reverse("process-checkout"))

        # Assert that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Assert that the response is redirected to the process-checkout URL
        self.assertRedirects(response, reverse("process-delivery"))

    def test_checkout_process_logged_in_user(self):
        # Log in the user
        self.client.login(username="testuser", password="password")

        # Make a GET request to the process-checkout URL
        response = self.client.get(reverse("process-checkout"))

        # Assert that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Assert that the response is redirected to the process-delivery URL
        self.assertRedirects(response, reverse("process-delivery"))

    def test_checkout_process_anonymous_user(self):
        # Make a GET request to the process-checkout URL without logging in
        response = self.client.get(reverse("process-checkout"))

        # Assert that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Assert that the response is redirected to the process-delivery URL
        self.assertRedirects(response, reverse("process-delivery"))
