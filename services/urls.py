from django.urls import path
from . import views

urlpatterns = [
    path('add-service/', views.add_service, name='add-service'),
    path('services-list/', views.service_list, name='services-list'),
]