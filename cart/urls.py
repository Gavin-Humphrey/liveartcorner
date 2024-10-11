from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from cart import views


urlpatterns = [
    path("add-to-cart/<int:item_id>/", views.add_to_cart, name="add-to-cart"),
    path("view-cart/", views.view_cart, name="view-cart"),
    path(
        "remove-from-cart/<int:item_id>/",
        views.remove_from_cart,
        name="remove-from-cart",
    ),
    # path("update-item-quantity/<int:item_id>/",views.update_item_quantity,name="update-item-quantity",),
    path(
        "update-cart/",
        views.update_cart,
        name="update-cart",
    ),
]
