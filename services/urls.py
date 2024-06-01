from django.urls import path
from . import views

urlpatterns = [
    path('add-service/', views.add_service, name='add-service'),
    path('services-list/', views.service_list, name='services-list'),
    path("update-service/<int:service_id>/", views.update_service, name="update-service"),
    path("delete-service/<int:service_id>/", views.delete_service, name="delete-service"),
]