from django.test import TestCase
from django.contrib.auth import get_user_model
from item.models import Item, CardItems
from wishlist.models import WishList, WishListItem
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO

User = get_user_model()

class WishListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client.login(email='test@example.com', password='password')

        self.card_item = CardItems.objects.create(user=self.user)

        # Create an in-memory image file
        image = Image.new('RGB', (100, 100))
        image_file = BytesIO()
        image.save(image_file, 'JPEG')
        image_file.seek(0)
        uploaded_image = SimpleUploadedFile('test.jpg', image_file.read(), content_type='image/jpeg')

        self.item = Item.objects.create(
            card=self.card_item,
            title="Test Item",
            image=uploaded_image,
            description="Test description",
            length=10,
            width=10,
            price=100,
            quantity=1
        )

        self.wishlist = WishList.objects.create(user=self.user)
        self.wishlist_item = WishListItem.objects.create(wishlist=self.wishlist, item=self.item)

    def test_add_to_wishlist_authenticated_user(self):
        # Make sure the item is in the wishlist_items related manager of the WishList instance
        wishlist_items = [wishlist_item.item for wishlist_item in self.wishlist.wishlist_items.all()]
        self.assertIn(self.item, wishlist_items)

    def test_remove_from_wishlist_authenticated_user(self):
        # Remove the item from the wishlist_items related manager
        self.wishlist_item.delete()
        wishlist_items = [wishlist_item.item for wishlist_item in self.wishlist.wishlist_items.all()]
        self.assertNotIn(self.item, wishlist_items)

    def test_view_wishlist_authenticated_user(self):
        # Test viewing the wishlist page for authenticated users
        response = self.client.get('/wishlist/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.title)

    def test_view_wishlist_unauthenticated_user(self):
        # Test viewing the wishlist page for unauthenticated users
        self.client.logout()
        response = self.client.get('/wishlist/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
