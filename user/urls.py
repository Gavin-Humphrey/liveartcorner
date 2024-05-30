from django.urls import path
from . import views



urlpatterns = [
    path("register-user", views.registerUser, name="register-user"),
    path('profile/<int:user_id>/', views.artist_profile_view, name='artist-profile'),
    path('update-artist-profile/', views.update_artist_profile, name='update-artist-profile'), 
    path('artist-dashboard/<int:user_id>/', views.artist_dashboard, name='artist-dashboard'),
    path('manage-items/', views.manage_items, name='manage-items'),
    path('manage-availability/', views.manage_availability, name='manage-availability'),
    path('manage-calendar/', views.manage_calendar, name='manage-calendar'),
    path('upload-files/', views.upload_files, name='upload-files'),
]