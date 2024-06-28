from django.contrib import admin
from .models import WishList, WishListItem


class WishListAdmin(admin.ModelAdmin):
    model = WishList
    extra = 0
    fields = [
        "user",
        "id",
    ]
    list_display = [
        "user",
        "id",
    ]


admin.site.register(WishList, WishListAdmin)


class WishListItemAdmin(admin.ModelAdmin):
    model = WishListItem
    extra = 0
    fields = ["wishlist", "item", "id"]
    list_display = ["wishlist", "item", "id"]  #### CHECK THIS OUT LATER


admin.site.register(WishListItem, WishListItemAdmin)
