from django.urls import path
from . import views
from base.views import home


urlpatterns = [
    path("", home, name="home"),
    # path("login/", views.loginPage, name="login"),
    # path("logout", views.logout_view, name="logout"),
    # path("register-user", views.registerUser, name="register-user"),
    path("contact", views.contact, name="contact"),
]
