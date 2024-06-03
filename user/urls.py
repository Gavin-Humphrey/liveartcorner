from django.urls import path
from . import views



urlpatterns = [
    path("register-user", views.registerUser, name="register-user"),
    path('profile/<int:user_id>/', views.artist_profile_view, name='artist-profile'),
    path('update-artist-profile/', views.update_artist_profile, name='update-artist-profile'), 
    path('artist-dashboard/<int:user_id>/', views.artist_dashboard, name='artist-dashboard'),
    path('manage-items/', views.manage_items, name='manage-items'),
    path('manage-availability/', views.manage_availability, name='manage-availability'),

    path('create-artist-availability-calendar/', views.create_artist_availability_calendar, name='create-artist-availability-calendar'),
    path('update-artist-availability-calendar/<int:pk>/', views.update_artist_availability_calendar, name='update-artist-availability-calendar'),
    path('artist-availability-calendar/', views.artist_availability_calendar, name='artist-availability-calendar'),
    path("delete-artist-availability/<int:pk>/", views.delete_artist_availability, name="delete-artist-availability"),
    path('upload-files/', views.upload_files, name='upload-files'),
]