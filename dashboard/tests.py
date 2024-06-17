from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from base.models import CardItems, Item
from user.models import ArtistAvailability
from services.models import Booking
from order.models import OrderItem

User = get_user_model()

class ArtistDashboardViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testartist', password='password', is_artist=True)
        self.url = reverse('artist-dashboard', kwargs={'user_id': self.user.id})
        self.client.force_login(self.user)

    def test_artist_dashboard_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/artist_dashboard.html')
        self.assertIn('availabilities', response.context)
        self.assertIn('bookings', response.context)
        self.assertIn('items', response.context)
        self.assertIn('items_count', response.context)

class ManageItemsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testartist', password='password', is_artist=True)
        self.url = reverse('manage-items')
        self.client.force_login(self.user)

    def test_manage_items_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'item/manage_items.html')
        self.assertIn('items', response.context)

class ManageItemsAvailabilityViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testartist', password='password', is_artist=True)
        self.url = reverse('manage-availability')
        self.client.force_login(self.user)

    def test_manage_items_availability_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'item/manage_availability.html')
        self.assertIn('items', response.context)


