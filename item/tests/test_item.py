from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import CardItems, Item

from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image
from io import BytesIO

User = get_user_model()

class ItemViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.user.is_vetted_artist = True
        self.user.save()

        # Create a sample image
        image = Image.new('RGB', (100, 100))
        image_io = BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)
        image_file = SimpleUploadedFile("test_image.png", image_io.getvalue(), content_type="image/png")

        self.card = CardItems.objects.create(user=self.user)
        self.item = Item.objects.create(
            title='Test Item', description='Test Description', card=self.card, length=10, width=5, price=100, quantity=1, image=image_file,
        )

    def test_upload_item_view_post(self):
        self.client.force_login(self.user)
        url = reverse('upload-item')

        post_data = {
            'title': 'Test Item',
            'description': 'Test Description',
            'popularity': 5,
            'length': 10,
            'width': 5,
            'price': 100,
            'quantity': 1,
        }
        response = self.client.post(url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_item_details(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("item-detail", args=[self.item.id]))
        self.assertEqual(response.status_code, 200)

    def test_updates_item(self):
        self.client.force_login(self.user)
        updated_title = "Updated Item Title"
        updated_length = 15
        updated_width = 8
        updated_description = "Updated Description"
        updated_price = 200
        updated_quantity = 2

        # Create a sample updated image
        updated_image = Image.new('RGB', (150, 150))
        updated_image_io = BytesIO()
        updated_image.save(updated_image_io, format='PNG')
        updated_image_io.seek(0)
        updated_image_file = SimpleUploadedFile("updated_image.png", updated_image_io.getvalue(), content_type="image/png")

        # Verify initial state before update
        self.assertEqual(self.item.length, 10)
        self.assertEqual(self.item.width, 5)
        self.assertEqual(self.item.price, 100)
        
        # Test updating the item
        response = self.client.post(
            reverse("update-item", args=[self.item.id]),
            {
                "title": updated_title,
                "description": updated_description,
                "length": updated_length,
                "width": updated_width,
                "price": updated_price,
                "quantity": updated_quantity,
                "image": updated_image_file,
            },
            follow=True,
        )

        # Check if the form is present in the response context
        form = response.context.get('form')
        if form is not None:
            # Check for form errors in the response
            form_errors = form.errors
            self.assertFalse(form_errors, f"Form errors present: {form_errors}")

        # Check if the update was successful
        self.assertEqual(response.status_code, 200)

        # Fetch the updated item
        updated_item = Item.objects.get(id=self.item.id)

        # Detailed assertions to debug
        self.assertEqual(updated_item.title, updated_title)
        self.assertEqual(updated_item.description, updated_description)
        self.assertEqual(updated_item.length, updated_length)
        self.assertEqual(updated_item.width, updated_width)
        self.assertEqual(updated_item.price, updated_price)
        self.assertEqual(updated_item.quantity, updated_quantity)
