from django.shortcuts import render, redirect
from base.forms import DeliveryInfoForm
from .models import OrderItem
from cart.shopping_cart import CartHandler
from .order import create_order
from cart.models import DeliveryMethod
import logging

logger = logging.getLogger(__name__)


def process_delivery(request, order_id=None, context=None):
    cart = CartHandler(request)

    if context is None:
        context = {}

    chosen_delivery_method = request.POST.get("chosen_delivery_method")
    delivery_cost = request.POST.get("delivery_cost")
    discount_value = request.POST.get("discount_value", "0")

    # Calculate the total cost using existing logic
    cart_sub_total = cart.calculate_sub_total()
    total_cost = request.POST.get("total_cost", 0)

    # Instantiate the form without any data if the request method is not POST
    delivery_form = DeliveryInfoForm()

    if request.method == "POST":
        # Instantiating the form with POST data only if the request method is POST
        delivery_form = DeliveryInfoForm(request.POST)

    context.update(
        {
            "cart_items": cart.get_cart_items(),
            "cart_items_count": cart.get_cart_items_count(),
            "sub_total": cart_sub_total,
            "chosen_delivery_method": chosen_delivery_method,
            "delivery_cost": delivery_cost,
            "discount_value": discount_value,
            "total_cost": total_cost,
            "delivery_form": delivery_form,
            "order_id": order_id,
        }
    )

    return render(request, "order/process_delivery.html", context)


def process_checkout(request):
    cart = CartHandler(request)
    context = {}

    if request.method == "POST":
        delivery_form = DeliveryInfoForm(request.POST)

        if delivery_form.is_valid():
            delivery_data = delivery_form.cleaned_data
            logger.info(f"Delivery data: {delivery_data}")

            chosen_delivery_method_name = request.POST.get("chosen_delivery_method")
            delivery_cost = request.POST.get("delivery_cost")
            discount_value = request.POST.get("discount_value", "0")
            total_cost = request.POST.get("total_cost")
            delivery_data["total_cost"] = total_cost

            sub_total = cart.calculate_sub_total()
            logger.info("The Checkout Sub total is: ", sub_total)

            logger.info(f"Chosen delivery method: {chosen_delivery_method_name}")
            logger.info(f"Total cost: {total_cost}")

            try:
                delivery_method_instance = DeliveryMethod.objects.get(
                    method=chosen_delivery_method_name
                )
                logger.info(f"Delivery method instance: {delivery_method_instance}")

                order = create_order(
                    request.user, delivery_data, delivery_method_instance
                )

                if order and order.id:
                    logger.info(f"Order created: {order}")
                    order_items = cart.get_cart_items()
                    for item in order_items:
                        price = item.get("price", 0)
                        OrderItem.objects.create(
                            order=order,
                            item=item["item"],
                            quantity=item["quantity"],
                            price=price,
                        )

                    cart.clear_cart()  # clearing the cart after order creation

                    context.update(
                        {
                            "cart_items": cart.get_cart_items(),
                            "cart_items_count": cart.get_cart_items_count(),
                            #'sub_total': float(cart.calculate_sub_total()),
                            "sub_total": sub_total,
                            "chosen_delivery_method": chosen_delivery_method_name,
                            "delivery_cost": delivery_cost,
                            "discount_value": discount_value,
                            "total_cost": total_cost,
                            "delivery_form": delivery_form,
                            "delivery_form_data": delivery_data,
                            "order_id": order.id,
                        }
                    )
                    return render(request, "order/checkout.html", context)

                else:
                    logger.error("Order creation failed. Check delivery details.")
                    context = {
                        "error_message": "Order creation failed. Please check your delivery details.",
                        "cart_items": cart.get_cart_items(),
                        "total_cost": total_cost,
                    }
                    return render(request, "order/checkout.html", context)
            except DeliveryMethod.DoesNotExist:
                logger.error("The chosen delivery method does not exist.")
                context = {
                    "error_message": "The chosen delivery method does not exist.",
                    "cart_items": cart.get_cart_items(),
                    "total_cost": total_cost,
                }
                return render(request, "order/checkout.html", context)
        else:
            logger.error("Form is not valid.")
            logger.error(f"Form errors: {delivery_form.errors}")
            context = {
                "error_message": "There was an error with your delivery details. Please check and try again.",
                "cart_items": cart.get_cart_items(),
                "total_cost": request.POST.get("total_cost"),
                "delivery_form": delivery_form,
            }
            return render(request, "order/checkout.html", context)
    return redirect("process-delivery")
