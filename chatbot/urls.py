from django.urls import path
from . import views

urlpatterns = [
    path("chatbot-response/", views.chatbot_response, name="chatbot-response"),
]
