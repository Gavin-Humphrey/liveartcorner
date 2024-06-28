from django.contrib import admin
from .models import CardItems, Item


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    fields = [
        "title",
        "description",
        "length",
        "width",
        "price",
        "quantity",
        "image",
        "popularity",
    ]
    readonly_fields = [
        "title",
        "description",
        "length",
        "width",
        "price",
        "quantity",
        "image",
        "popularity",
    ]


admin.site.register(Item)


class CardItemsAdmin(admin.ModelAdmin):
    readonly_fields = ("user",)
    inlines = [ItemInline]


admin.site.register(CardItems, CardItemsAdmin)
