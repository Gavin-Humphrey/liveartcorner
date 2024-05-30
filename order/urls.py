from django.urls import path
from .views import process_delivery, process_checkout # pre_checkout_summary,
from .process_payment import (CheckoutSessionView, SuccessView, CancelView, payment_status_view, my_webhook_view)  


urlpatterns = [ 
    path('process-delivery/', process_delivery, name='process-delivery'), 
    #path('pre-checkout-summary/', pre_checkout_summary, name='pre-checkout-summary'), 
    path("process-checkout/", process_checkout, name="process-checkout"),
    path('order/webhook/stripe/', my_webhook_view, name='webhook-stripe'),
    path('payment-status/<int:order_id>/', payment_status_view, name='payment-status'),
    #path('create-checkout-session/', CheckoutSessionView.as_view(), name='create-checkout-session'),
    path('create-checkout-session/<int:order_id>/', CheckoutSessionView.as_view(), name='create-checkout-session'),


    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),
]
