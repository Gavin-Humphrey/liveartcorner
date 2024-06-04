import stripe
import logging
from django.conf import settings
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from .models import Order, OrderItem
from item.models import CardItems

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)

class CheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def post(self, request, *args, **kwargs):
        total_cost = request.POST.get('total_cost')
        order_id = request.POST.get('order_id')
        order = Order.objects.get(pk=order_id)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Total Order',
                            'description': f'Order ID: #{order_id}',
                        },
                        'unit_amount': int(float(order.total_cost) * 100),
                    },
                    'quantity': 1,
                }],
            metadata={"product_id": order_id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return redirect(checkout_session.url)
        


class SuccessView(TemplateView):
    template_name = "order/success.html"

class CancelView(TemplateView):
    template_name = "order/cancel.html"


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
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

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        logger.info(f"Checkout session completed: {session}")
        handle_checkout_session(session)
    else:
        logger.warning(f"Unhandled event type: {event['type']}")

    return HttpResponse(status=200)



def handle_checkout_session(session):
    order_id = session.get('metadata', {}).get('order_id')
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
            # Update order status
            order.order_status = 'completed'
            order.save()
            # Deduct items from each user's CardItem
            for order_item in order.orderitem_set.all():
                item = order_item.item
                item_quantity = order_item.quantity
                seller = item.card.user  # Each item has a seller (owner)
                seller_card_item, created = CardItems.objects.get_or_create(user=seller)
                # Deduct the quantity from the seller's CardItem
                if seller_card_item:
                    if item in seller_card_item.items.all():
                        seller_item = seller_card_item.items.get(id=item.id)
                        seller_item.quantity -= item_quantity
                        seller_item.save()
            logger.info(f"Order {order_id} marked as completed and items deducted from sellers' CardItems")
        except Order.DoesNotExist:
            logger.error(f"Order with ID {order_id} does not exist")
        except CardItems.DoesNotExist:
            logger.error(f"CardItems not found for one of the sellers")
    else:
        logger.error("Order ID not found in session metadata")


def handle_payment_intent_succeeded(payment_intent):
    order_id = payment_intent['metadata']['order_id']
    order = get_object_or_404(Order, id=order_id)
    order.order_status = 'PAID'  # Updated status to 'PAID'
    order.save()  # Save the changes



def payment_status_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.order_status == 'PAID':
        context = {
            "payment_status": "success",
        }
    else:
        context = {
            "payment_status": "cancel",
        }
    return render(request, "order/payment_status.html", context)



def handle_successful_payment(order):
    # Retrieve order items
    order_items = OrderItem.objects.filter(order=order)
    
    # Deduct items from inventory
    for order_item in order_items:
        item = order_item.item
        quantity_purchased = order_item.quantity
        item.quantity -= quantity_purchased
        item.save()
