from django.contrib import admin
from .models import Cart, CartItem, DeliveryMethod, DiscountCode #CartItem 




#admin.site.register(CartItem)


class CartAdmin(admin.ModelAdmin):
    model = Cart
    extra = 0
    fields = ['user',]
    readonly_fields = ['user',]
admin.site.register(Cart, CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    model = CartItem
    extra = 0
    fields = ['user',]
    list_display = ['id', 'cart', 'item', 'quantity']
admin.site.register(CartItem, CartItemAdmin)

# class CartItem(admin.TabularInline):
#     model = CartItem
#     extra = 0
#     fields = ['item', 'quantity',]
#     readonly_fields = ['item', 'quantity',]

class DiscountCodeAdmin(admin.ModelAdmin):
    model = DiscountCode
    extra = 0
    #readonly_fields = ['code', 'value', 'expiration_date', 'active']
    list_display = ['code', 'value', 'expiration_date', 'active']
admin.site.register(DiscountCode, DiscountCodeAdmin)

class DeliveryMethodAdmin(admin.ModelAdmin):
    model = DeliveryMethod
    extra = 0
    #readonly_fields = ['method', 'id', 'cost',]
    list_display = ['method',  'cost',]

admin.site.register(DeliveryMethod, DeliveryMethodAdmin)