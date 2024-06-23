#from django.contrib import admin
from django.urls import path

from . import views



urlpatterns = [
    path('add-to-wishlist/<int:item_id>/', views.add_to_wishlist, name='add-to-wishlist'),
    #path('', views.my_wishlist, name='view-wishlist'),
    path('wishlist/', views.my_wishlist, name='my-wishlist'),
    path('remove-from-wishlist/<int:item_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),
]