from django.urls import path
from . import views
from .process_booking_payment import (
    BookingCheckoutSessionView,
    my_webhook_view,
    payment_status_view,
)


urlpatterns = [
    path("add-service/", views.add_service, name="add-service"),
    path("services-list/", views.service_list, name="services-list"),
    path(
        "update-service/<int:service_id>/", views.update_service, name="update-service"
    ),
    path(
        "delete-service/<int:service_id>/", views.delete_service, name="delete-service"
    ),
    # path('service-booking/<int:service_id>/', views.book_service, name='service-booking'),
    path(
        "create-booking-checkout-session/<int:service_id>/",
        BookingCheckoutSessionView.as_view(),
        name="create-booking-checkout-session",
    ),
    path("services/webhook/stripe/", my_webhook_view, name="webhook-stripe"),
    path(
        "payment-status/<int:booking_id>/", payment_status_view, name="payment-status"
    ),
    path(
        "service-booking/<int:service_id>/",
        views.service_booking,
        name="service-booking",
    ),
    path(
        "booking-summary/<int:service_id>/<int:booking_id>/",
        views.booking_summary,
        name="booking-summary",
    ),
]
