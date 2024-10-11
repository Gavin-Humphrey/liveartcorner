from django.shortcuts import render
from base.forms import DeliveryInfoForm
from .models import OrderItem
from cart.shopping_cart import CartHandler
from .order import create_order
from cart.models import DeliveryMethod
from django.contrib import messages
from django.db import transaction
import logging


logger = logging.getLogger(__name__)


def process_delivery(request, order_id=None, context=None):
    # Initialize the cart and retrieve cart items
    cart = CartHandler(request)
    cart_items = cart.get_cart_items()
    cart_items_count = cart.get_cart_items_count()

    # If context is not provided, create an empty dictionary
    if context is None:
        context = {}

    # Retrieve chosen delivery method details and discount value from session
    chosen_delivery_method_id = request.session.get("chosen_delivery_method")
    chosen_delivery_method = DeliveryMethod.objects.filter(
        id=chosen_delivery_method_id
    ).first()
    delivery_cost = request.session.get("delivery_cost", 0)
    discount_value = request.session.get("discount_value", "0")

    # Initialize item_total_costs for display
    item_total_costs = {ci.id: cart.calculate_item_total_cost(ci) for ci in cart_items}

    # Calculate the cart total and subtotal (calculated once, used in all cases)
    cart_sub_total = cart.calculate_sub_total()
    total_cost = cart.calculate_cart_total_cost()

    # Handle form submission (POST request)
    if request.method == "POST":
        delivery_form = DeliveryInfoForm(request.POST)

        # Update the context with valid form data and cart details
        context.update(
            {
                "cart_items": cart_items,
                "cart_items_count": cart_items_count,
                "chosen_delivery_method": chosen_delivery_method,
                "delivery_cost": delivery_cost,
                "discount_value": discount_value,
                "item_total_costs": item_total_costs,
                "cart_sub_total": cart_sub_total,
                "total_cost": total_cost,
                "delivery_form": delivery_form,
            }
        )

        # Redirect to the checkout page
    return render(request, "order/process_delivery.html", context)


def process_checkout(request):
    # Initialize the cart and retrieve cart items
    cart = CartHandler(request)
    cart_items = cart.get_cart_items()
    cart_items_count = cart.get_cart_items_count()

    chosen_delivery_method = request.session.get("chosen_delivery_method", None)
    delivery_cost = request.session.get("delivery_cost", 0)
    discount_value = request.session.get("discount_value", "0")
    delivery_data = request.session.get("delivery_data", {})

    item_total_costs = {ci.id: cart.calculate_item_total_cost(ci) for ci in cart_items}
    cart_sub_total = cart.calculate_sub_total()
    total_cost = cart.calculate_cart_total_cost()

    if request.method == "POST":
        delivery_form = DeliveryInfoForm(request.POST)

        if delivery_form.is_valid():
            delivery_data = delivery_form.cleaned_data
            delivery_data["total_cost"] = (
                total_cost  # Adding total cost to delivery data
            )

            try:
                # Use transaction to ensure atomicity of order and order item creation
                with transaction.atomic():

                    # Create the order
                    order = create_order(request.user, delivery_data)

                    if order and order.id:
                        print(f"Order created successfully: {order.id}")

                        # Process each CartItem and create corresponding OrderItem
                        for cart_item in cart_items:
                            print(
                                f"Processing CartItem {cart_item.id} with Item {cart_item.item}"
                            )

                            # Ensure the CartItem has a valid related Item
                            if cart_item.item:
                                try:
                                    # Create an OrderItem from the CartItem
                                    order_item = OrderItem.objects.create(
                                        order=order,
                                        item=cart_item.item,  # Link to the actual item
                                        delivery_method=cart_item.delivery_method,  # Use delivery method from cart item
                                        discount_code=cart_item.discount_code,  # Use discount code from cart item
                                        item_total_cost=cart.calculate_item_total_cost(
                                            cart_item
                                        ),
                                    )

                                    print(
                                        f"OrderItem created: {order_item.id} for CartItem {cart_item.id}"
                                    )
                                except Exception as e:
                                    print(
                                        f"Failed to create OrderItem for CartItem {cart_item.id}: {e}"
                                    )
                            else:
                                print(
                                    f"CartItem {cart_item.id} has no valid item. Skipping."
                                )

                        # Prepare the response context
                        context = {
                            "cart_items": cart_items,
                            "cart_items_count": cart_items_count,
                            "delivery_form_data": delivery_data,
                            "cart_sub_total": cart_sub_total,
                            "total_cost": total_cost,
                            "order_id": order.id,
                        }

                        response = render(request, "order/checkout.html", context)
                        # Clear the cart only after all items are processed
                        cart.clear_cart()
                        print(f"Cart cleared after successful order {order.id}")
                        print("This is the context rendered on template: ", context)
                        return response

            except Exception as e:
                print(f"Checkout process failed: {e}")

        else:
            context = {
                "cart_items": cart_items,
                "cart_items_count": cart_items_count,
                "delivery_data": delivery_data,
                "item_total_costs": item_total_costs,
                "cart_sub_total": cart_sub_total,
                "total_cost": total_cost,
                "delivery_method": chosen_delivery_method,
                "delivery_cost": delivery_cost,
                "discount_value": discount_value,
            }

            return render(request, "order/process_delivery.html", context)
