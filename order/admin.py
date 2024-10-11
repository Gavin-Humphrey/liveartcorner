from django.contrib import admin
from .models import GuestUser, Order, OrderItem


admin.site.register(GuestUser)


class GuestUser(admin.TabularInline):
    model = GuestUser
    extra = 0
    fields = [
        "is_user",
    ]
    readonly_fields = [
        "is_user",
    ]


class OrderAdmin(admin.ModelAdmin):
    model = Order
    extra = 0
    readonly_fields = [
        "user",
        "order_type",
        "items",
        "total_cost",
        # "delivery_method",  # Assuming no discount_code field
        "order_status",
        "id",
        "created_at",
        "updated_at",
    ]
    list_display = [
        "user",
        "order_type",
        "total_cost",
        # "delivery_method",  # Assuming no discount_code field
        "order_status",
        "id",
        "created_at",
        "updated_at",
    ]


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    extra = 0
    readonly_fields = [
        "order",
        "item",
        "delivery_method",
        "discount_code",
        "item_total_cost",
    ]
    list_display = [
        "order",
        "item",
        "delivery_method",
        "discount_code",
        "item_total_cost",
    ]


admin.site.register(OrderItem, OrderItemAdmin)
