from django.urls import path
from . import views
from base import views as view



urlpatterns = [
    path('login/', views.login_view, name='login'),   
    path("logout", views.logout_view, name="logout"),
    path("register-user", views.registerUser, name="register-user"),
    path('profile/<int:user_id>/', views.artist_profile_view, name='artist-profile'),
    path('update-artist-profile/', views.update_artist_profile, name='update-artist-profile'), 
    
    path("activate/<str:uidb64>/<str:token>/", views.activate, name="activate"),
]