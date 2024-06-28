import stripe
import logging
from django.conf import settings
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from .models import Booking, Service
from user.models import ArtistAvailability


logger = logging.getLogger(__name__)


class BookingCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        try:
            total_cost = request.POST.get("total_cost")
            service_id = kwargs.get("service_id")
            availability_slot_id = request.POST.get("availability_slot")
            service = Service.objects.get(pk=service_id)
            availability_slot = ArtistAvailability.objects.get(pk=availability_slot_id)

            description = (
                f"Service ID: #{service_id}\n"
                f"Date: {availability_slot.date}\n"
                f"Time: {availability_slot.start_time} - {availability_slot.end_time}"
            )

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": service.name,
                                "description": description,
                            },
                            "unit_amount": int(float(total_cost) * 100),
                        },
                        "quantity": 1,
                    }
                ],
                metadata={
                    "service_id": service_id,
                    "availability_slot_id": availability_slot_id,
                    "date": availability_slot.date,
                    "start_time": availability_slot.start_time,
                    "end_time": availability_slot.end_time,
                },
                mode="payment",
                success_url=settings.PAYMENT_SUCCESS_URL,
                cancel_url=settings.PAYMENT_CANCEL_URL,
            )
            return redirect(checkout_session.url)
        except Exception as e:
            logger.error("Error creating Stripe checkout session: %s", e)
            return HttpResponse("Error creating Stripe checkout session", status=500)


class SuccessView(TemplateView):
    template_name = "services/success.html"


class CancelView(TemplateView):
    template_name = "services/cancel.html"


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        logger.info(f"Webhook received: {event['type']}")
    except ValueError as e:
        # Invalid payload
        logger.error("Invalid payload", exc_info=True)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error("Invalid signature", exc_info=True)
        return HttpResponse(status=400)
    except Exception as e:
        # Handle any other exceptions
        logger.error("Error processing webhook", exc_info=True)
        return HttpResponse(status=400)

    return HttpResponse(status=200)


def handle_payment_intent_succeeded(payment_intent):
    booking_id = payment_intent["metadata"]["booking_id"]
    booking = get_object_or_404(Booking, id=booking_id)
    booking.booking_status = "PAID"  # Updated status to 'PAID'
    booking.save()  # Save the changes


def payment_status_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.booking_status == "PAID":
        context = {
            "payment_status": "success",
        }
    else:
        context = {
            "payment_status": "cancel",
        }
    return render(request, "services/booking_payment_status.html", context)
