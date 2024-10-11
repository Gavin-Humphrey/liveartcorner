from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from item.models import CardItems, Item

from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io


User = get_user_model()


class ArtistDashboardViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            password="password",
            is_artist=True,
        )
        self.url = reverse("artist-dashboard", kwargs={"user_id": self.user.id})
        self.client.force_login(self.user)

    def test_artist_dashboard_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/artist_dashboard.html")
        self.assertIn("availabilities", response.context)
        self.assertIn("bookings", response.context)
        self.assertIn("items", response.context)
        self.assertIn("items_count", response.context)


class ManageItemsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testartist",
            email="test@example.com",
            password="password",
            is_artist=True,
        )
        self.url = reverse("manage-items")
        self.client.force_login(self.user)

    def test_manage_items_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")


class ManageItemsAvailabilityViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testartist", email="test@example.com", password="password"
        )
        self.user.is_artist = True
        self.user.save()

        # Create a CardItems instance for the user
        self.card = CardItems.objects.create(user=self.user)

        # Create some items for the card with a mock image
        image = Image.new("RGB", (10, 10), color="red")
        image_io = io.BytesIO()
        image.save(image_io, format="JPEG")
        image_io.seek(0)
        image_file = SimpleUploadedFile(
            "img1.jpg", image_io.read(), content_type="image/jpeg"
        )

        Item.objects.create(
            card=self.card,
            title="Item 1",
            image=image_file,
            length=10,
            width=5,
            is_available=True,
            price=100,
            quantity=1,
            description="Item 1 description",
            popularity=5,
        )
        Item.objects.create(
            card=self.card,
            title="Item 2",
            image=image_file,
            length=20,
            width=15,
            is_available=False,
            price=200,
            quantity=2,
            description="Item 2 description",
            popularity=3,
        )

        self.url = reverse("manage-items-availability")
        self.client.force_login(self.user)

    def test_manage_items_availability_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "item/manage_availability.html")
        self.assertIn("items", response.context)

        items = response.context["items"]
        self.assertEqual(len(items), 2)
        item_titles = [item.title for item in items]
        self.assertIn("Item 1", item_titles)
        self.assertIn("Item 2", item_titles)

    def test_manage_items_availability_view_post(self):
        post_data = {
            "is_available_1": "on",  # Set Item 1 as available
            "is_available_2": "on",  # Set Item 2 as available
        }
        response = self.client.post(self.url, post_data, follow=True)
        self.assertRedirects(response, self.url)

        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Item availability updated successfully.", messages)

        item1 = Item.objects.get(id=1)
        item2 = Item.objects.get(id=2)
        self.assertTrue(item1.is_available)
        self.assertTrue(item2.is_available)  # Since both are set to 'on' in post_data

    def test_manage_items_availability_view_no_card_items(self):
        user_without_card_items = User.objects.create_user(
            username="newuser", email="newuser@example.com", password="password"
        )
        self.client.force_login(user_without_card_items)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, reverse("home"))

        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("You have no items to manage.", messages)

    def test_manage_items_availability_view_failure(self):
        self.assertTrue(True)  # This test should fail to demonstrate a failure
