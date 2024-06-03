from django.db import models
from user.models import User
from item.models import Item





class WishList(models.Model):
    user = models.OneToOneField(User, related_name='wishlist', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

class WishListItem(models.Model):
    wishlist = models.ForeignKey(WishList, related_name='wishlist_items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='wishlist_item', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item.title} in {self.wishlist.user.username}'s Wishlist"
    



