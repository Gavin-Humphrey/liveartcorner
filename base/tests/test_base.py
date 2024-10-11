from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django_secure_contact_form.forms import ContactForm

from django.test import TestCase
from django.urls import reverse
from django.core import mail
from unittest.mock import patch

User = get_user_model()


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("home")
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password"
        )

    def test_home_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/home.html")
        self.assertIn("card_items", response.context)
        self.assertIn("cart_items_count", response.context)
        self.assertIn("wishlist_items_count", response.context)
        self.assertIn("popular_items", response.context)


class ContactViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("contact")
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password"
        )

    def test_contact_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/contact.html")
        self.assertIsInstance(response.context["form"], ContactForm)

    def test_contact_view_post_valid(self):
        data = {
            "firstname": "John",
            "lastname": "Doe",
            "email": "john.doe@example.com",
            "subject": "Test Subject",
            "message": "Test Message",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/thank_you.html")
        self.assertContains(response, "John")

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Contact Form Submission - Test Subject", mail.outbox[0].subject)
        self.assertIn("Firstame: John", mail.outbox[0].body)
        self.assertIn("Lastname: Doe", mail.outbox[0].body)
        self.assertIn("Email: john.doe@example.com", mail.outbox[0].body)
        self.assertIn("Subject: Test Subject", mail.outbox[0].body)
        self.assertIn("Message: Test Message", mail.outbox[0].body)


class ContactViewTestCase(TestCase):

    @patch(
        "captcha.fields.CaptchaField.clean"
    )  # Mock the clean method of the CaptchaField
    def test_contact_view_post_valid(self, mock_captcha):
        # Mock the CAPTCHA response to always be valid
        mock_captcha.return_value = True

        # Send a POST request with valid data
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Test User",
                "email": "test@example.com",
                "subject": "Test Subject",
                "message": "Test Message",
                "captcha": "valid_captcha_response",  # Simulating a valid CAPTCHA response
            },
        )

        # Assert that the correct template is used after form submission
        self.assertTemplateUsed(response, "base/thank_you.html")

        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check how the email body is formatted
        email_body = mail.outbox[0].body

        # Adjust this line based on how your email is structured
        self.assertIn("Full Name: Test User", email_body)
        self.assertIn("Email: test@example.com", email_body)
        self.assertIn("Subject: Test Subject", email_body)
        self.assertIn("Message: Test Message", email_body)
