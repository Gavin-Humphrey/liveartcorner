from django.urls import path
from . import views
from base import views as view


urlpatterns = [
    path(
        "artist-dashboard/<int:user_id>/",
        views.artist_dashboard,
        name="artist-dashboard",
    ),
    path("manage-items/", views.manage_items, name="manage-items"),
    path("dashboard-orders/", views.artist_orders, name="dashboard-orders"),
    path(
        "manage-items-availability/",
        views.manage_items_availability,
        name="manage-items-availability",
    ),
    path(
        "create-artist-availability-calendar/",
        views.create_artist_availability_calendar,
        name="create-artist-availability-calendar",
    ),
    path(
        "update-artist-availability-calendar/<int:pk>/",
        views.update_artist_availability_calendar,
        name="update-artist-availability-calendar",
    ),
    path(
        "artist-availability-calendar/",
        views.artist_availability_calendar,
        name="artist-availability-calendar",
    ),
    path(
        "delete-artist-availability/<int:pk>/",
        views.delete_artist_availability,
        name="delete-artist-availability",
    ),
    path(
        "view-artist-bookings/", views.get_artist_bookings, name="view-artist-bookings"
    ),
    path("order-detail/<int:order_id>/", views.order_detail, name="order-detail"),
    path("upload-files/", views.upload_files, name="upload-files"),
]
