from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Service, ArtistAvailability
from datetime import datetime, timedelta

User = get_user_model()


class YourTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )
        self.artist = User.objects.create_user(
            username="artistuser", email="artist@example.com", password="password"
        )

        # Create ArtistAvailability instances for the artist
        self.availability_with_booking = ArtistAvailability.objects.create(
            artist=self.artist,
            date=datetime.now().date(),
            start_time=(datetime.now() + timedelta(hours=1)).time(),
            end_time=(datetime.now() + timedelta(hours=2)).time(),
            booked=False,
        )

        self.availability_without_booking = ArtistAvailability.objects.create(
            artist=self.artist,
            date=datetime.now().date(),
            start_time=(datetime.now() + timedelta(hours=3)).time(),
            end_time=(datetime.now() + timedelta(hours=4)).time(),
            booked=False,
        )

        self.service_with_availability = Service.objects.create(
            name="Service with Availability",
            artist=self.artist,
            price=50.00,  # Adjust the price according to your model definition
        )

        self.service_without_availability = Service.objects.create(
            name="Service without Availability",
            artist=self.artist,
            price=60.00,  # Adjust the price according to your model definition
        )

    def test_service_booking_with_availability(self):
        # Simulate authentication
        self.client.force_login(self.user)

        # Attempt to book the service with availability
        response = self.client.post(
            reverse("service-booking", args=[self.service_with_availability.id]),
            {"availability_slot": self.availability_with_booking.pk},  # Use pk directly
        )

        # Check that the response status code is as expected
        self.assertEqual(response.status_code, 302)  # Assuming successful redirect

        # Optionally, check that the availability slot is now booked
        self.availability_with_booking.refresh_from_db()
        self.assertTrue(self.availability_with_booking.booked)

    def test_service_booking_without_availability(self):
        # Simulate authentication
        self.client.force_login(self.user)

        # Attempt to book the service without availability
        response = self.client.post(
            reverse("service-booking", args=[self.service_without_availability.id]),
            {
                "selected_slot_id": self.availability_without_booking.pk  # Use pk directly
            },
        )

        # Check that the response status code is as expected (404 or other appropriate error)
        self.assertEqual(
            response.status_code, 404
        )  # Adjust as per your application's response

    def test_add_service(self):
        # Simulate authentication
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("add-service"),
            {
                "name": "New Service",
                "artist": self.user.id,
                "price": 60.00,  # Example price
            },
        )
        self.assertEqual(response.status_code, 200)  # Adjust status code as needed

    def test_delete_service(self):
        # Simulate authentication
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("delete-service", args=[self.service_with_availability.id])
        )
        self.assertEqual(response.status_code, 302)  # Adjust status code as needed

    def test_update_service(self):
        # Simulate authentication
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("update-service", args=[self.service_with_availability.id]),
            {
                "name": "Updated Service",
                "artist": self.user.id,
                "price": 70.00,  # Example price
            },
        )
        self.assertEqual(response.status_code, 200)  # Adjust status code as needed
