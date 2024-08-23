from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from item.models import Item, CardItems
from .shopping_cart import CartHandler
from .models import DeliveryMethod, DiscountCode
from wishlist.models import WishList, WishListItem
from django.contrib.messages import info
from base.forms import DeliveryInfoForm
from django.contrib.auth.models import AnonymousUser


def add_to_cart(request, item_id):
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        item = get_object_or_404(
            Item, id=item_id
        )  # Fetch the Item instance using item_id

        if not isinstance(request.user, AnonymousUser):
            wishlist = WishList.objects.filter(user=request.user).first()
            if wishlist:
                # Remove the specific item from the wishlist
                wishlist_item = WishListItem.objects.filter(
                    wishlist=wishlist, item=item
                ).first()
                if wishlist_item:
                    wishlist_item.delete()

        if item.quantity >= quantity:
            cart = CartHandler(request)
            cart.add_to_cart(
                item, quantity=quantity
            )  # Pass the Item instance instead of item_id
            # return redirect("home")

        else:
            messages.error(
                request, f"Sorry, there are only {item.quantity} items available."
            )
            return redirect("home")
        messages.success(request, "Item added to your cart.")
        return redirect(request.META.get("HTTP_REFERER", "home"))
    else:
        return redirect("home")


def view_cart(request):
    cart = CartHandler(request)
    delivery_methods = DeliveryMethod.objects.all()

    # Retrieve cart items and count
    cart_items_count = cart.get_cart_items_count()

    # Check for empty cart and add message
    if not cart_items_count:
        info(request, "Your cart is empty.")

    context = {
        "cart_items": cart.get_cart_items(),
        "cart_items_count": cart.get_cart_items_count(),
        "sub_total": cart.calculate_sub_total(),
        "delivery_methods": delivery_methods,
    }

    return render(request, "cart/cart.html", context)


def update_item_quantity(request, item_id):

    if request.method == "POST":
        quantity = int(request.POST.get("quantity"))
        cart = CartHandler(request)
        cart.update_quantity(item_id, quantity)
        return redirect("view-cart")


def update_cart_total_cost(request):
    cart = CartHandler(request)
    delivery_methods = DeliveryMethod.objects.all()
    delivery_form = DeliveryInfoForm(request.POST)

    if request.method == "POST":
        selected_delivery_method_id = request.POST.get("selected_delivery_method_id")
        discount_code = request.POST.get("discount_code", "").strip()

        try:
            # Calculate total cost based on delivery method and discount code
            total_cost = cart.calculate_total_with_delivery(
                selected_delivery_method_id, discount_code
            )

            # Retrieve other relevant information for the summary
            cart_items = cart.get_cart_items()

            sub_total = cart.calculate_sub_total()
            chosen_delivery_method = get_object_or_404(
                DeliveryMethod, id=selected_delivery_method_id
            )
            context = {
                "cart_items": cart_items,
                "sub_total": sub_total,
                "chosen_delivery_method": (
                    chosen_delivery_method.method
                    if chosen_delivery_method.method
                    else None
                ),  # Get the delivery method name
                "delivery_cost": (
                    chosen_delivery_method.cost if chosen_delivery_method.cost else 0
                ),
                "total_cost": total_cost,
                "delivery_form": delivery_form,
            }
            # Only include discount value if it exists
            if discount_code:
                discount_code = cart.add_discount(discount_code)
                context["discount_value"] = discount_code.value

            # Return the updated cart page with the new total cost
            return render(request, "cart/cart.html", context)
        # except ValueError as e:
        #     messages.error(request, str(e))
        except (ValueError, TypeError) as e:
            messages.error(
                request,
                "An error occurred while processing your request. Please ensure all fields are correctly filled.",
            )

    return redirect(
        "view-cart"
    )  # Redirect back to the cart if no POST request or if there's an error


def remove_from_cart(request, item_id):
    if request.method == "POST":
        cart = CartHandler(request)
        cart.remove_item(item_id)
        return redirect("view-cart")
