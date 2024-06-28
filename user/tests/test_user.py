from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import ArtistProfile
from django.core import mail
from ..tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


User = get_user_model()


class UserTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register-user")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.profile_url = lambda user_id: reverse("artist-profile", args=[user_id])
        self.update_profile_url = reverse("update-artist-profile")
        self.user_data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "phone_number": "1234567890",
            "street_address": "123 Test St",
            "city": "Test City",
            "postal_code": "12345",
            "country": "Test Country",
        }
        self.user = User.objects.create_user(
            name="Test User",
            email="testuser@example.com",
            password="testpassword123",
            is_active=True,
        )
        self.artist_profile = ArtistProfile.objects.create(
            user=self.user,
            bio="Test bio",
            portfolio_url="http://testportfolio.com",
            phone_number="1234567890",
            location="Test Location",
            artistic_medium="Test Medium",
            experience_education="Test Experience",
        )

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 200)
        # self.assertRedirects(response, self.login_url)
        # Optionally, check for email verification functionality if applicable
        self.assertEqual(len(mail.outbox), 0)

    def test_account_activation(self):
        user = User.objects.create_user(
            name="New User",
            email="newuser@example.com",
            password="newpassword123",
            is_active=False,
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_url = reverse("activate", args=[uid, token])
        response = self.client.get(activation_url)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_login_view(self):
        response = self.client.post(
            self.login_url,
            {"username": "testuser@example.com", "password": "testpassword123"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_logout_view(self):
        self.client.login(username="testuser@example.com", password="testpassword123")
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_artist_profile_view(self):
        self.client.login(username="testuser@example.com", password="testpassword123")
        response = self.client.get(
            reverse("artist-profile", kwargs={"user_id": self.user.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/user_profile.html")
        # Adjust this to check for the correct profile data
        # self.assertContains(response, 'Test bio')  # Ensure 'Test bio' is present in the response content

    def test_update_artist_profile(self):
        self.client.login(username="testuser@example.com", password="testpassword123")
        response = self.client.post(
            self.update_profile_url,
            {
                "bio": "Updated bio",
                "phone_number": "0987654321",
                "location": "Updated Location",
                "artistic_medium": "Updated Medium",
                "experience_education": "Updated Experience",
            },
        )

        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, self.profile_url(self.user.id))
        self.artist_profile.refresh_from_db()
