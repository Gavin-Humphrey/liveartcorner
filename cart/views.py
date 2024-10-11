from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from item.models import Item
from .shopping_cart import CartHandler
from .models import DeliveryMethod, CartItem


def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart = CartHandler(request)

    if request.method == "POST":
        # Check if the item already exists in the cart
        existing_cart_item = CartItem.objects.filter(cart=cart.cart, item=item).first()

        if existing_cart_item:
            # Ask for confirmation to add another copy
            if request.POST.get("confirm"):
                # Create a new CartItem for the same item
                CartItem.objects.create(cart=cart.cart, item=item)
                # messages.success(request, "Another copy of the item has been added to your cart.")
                return redirect("item-detail", item_id=item.id)

            # messages.info(request, "Item already in your cart. Would you like to add another?")
            return render(request, "cart/confirm_add.html", {"item": item})

        # If not already in the cart, add it
        CartItem.objects.create(cart=cart.cart, item=item)
        # messages.success(request, "Item added to your cart.")
        return redirect(request.META.get("HTTP_REFERER", "home"))

    return redirect("home")


def update_item_quantity(request, item_id):

    if request.method == "POST":
        quantity = int(request.POST.get("quantity"))
        cart = CartHandler(request)
        cart.update_quantity(item_id, quantity)
        return redirect("view-cart")


def update_cart(request):
    cart = CartHandler(request)
    delivery_methods = DeliveryMethod.objects.all()

    if request.method == "POST":
        cart_item_id = request.POST.get("cart_item_id")

        if not cart_item_id:
            messages.error(request, "Cart item ID is missing.")
            return redirect("view-cart")

        try:
            cart_item_id = int(cart_item_id)
        except ValueError:
            messages.error(request, "Invalid Cart Item ID format.")
            return redirect("view-cart")

        try:
            cart_item = cart.cart_items.filter(id=cart_item_id).first()

            if not cart_item:
                messages.error(request, "The specified cart item does not exist.")
                return redirect("view-cart")

            selected_delivery_method_id = request.POST.get(
                "selected_delivery_method_id"
            )
            discount_code = request.POST.get("discount_code", "").strip()

            cart.update_cart_item(
                cart_item_id, selected_delivery_method_id, discount_code
            )

            # Refresh cart items
            cart_items = cart.get_cart_items()
            cart_items_count = cart.get_cart_items_count()

            item_total_cost = {
                ci.id: cart.calculate_item_total_cost(ci) for ci in cart_items
            }
            cart_sub_total = cart.calculate_sub_total()
            total_cost = cart.calculate_cart_total_cost()

            # Check if all cart items have a delivery method selected
            all_items_have_delivery_method = all(
                ci.delivery_method for ci in cart_items
            )

            context = {
                "cart_items": cart_items,
                "cart_items_count": cart_items_count,
                "item_total_cost": item_total_cost,
                "cart_sub_total": cart_sub_total,
                "total_cost": total_cost,
                "delivery_methods": delivery_methods,
                "discount_code": discount_code,
                "all_items_have_delivery_method": all_items_have_delivery_method,
            }

            return render(request, "cart/cart.html", context)

        except (ValueError, TypeError) as e:
            messages.error(
                request,
                "An error occurred while processing your request. Please ensure all fields are correctly filled.",
            )
            # print(f"Error: {e}")
            return redirect("view-cart")

    # Ensure `cart_items` is defined even if not handling POST
    cart_items = cart.get_cart_items()
    cart_items_count = cart.get_cart_items_count()

    item_total_cost = {ci.id: cart.calculate_item_total_cost(ci) for ci in cart_items}
    cart_sub_total = cart.calculate_sub_total()
    total_cost = cart.calculate_cart_total_cost()

    # Check if all cart items have a delivery method selected
    all_items_have_delivery_method = all(ci.delivery_method for ci in cart_items)

    context = {
        "cart_items": cart_items,
        "cart_items_count": cart_items_count,
        "item_total_cost": item_total_cost,
        "cart_sub_total": cart_sub_total,
        "total_cost": total_cost,
        "delivery_methods": delivery_methods,
        "order_id": 0,
        "all_items_have_delivery_method": all_items_have_delivery_method,
    }
    return render(request, "cart/cart.html", context)


def view_cart(request):
    cart = CartHandler(request)
    delivery_methods = DeliveryMethod.objects.all()

    cart_items = cart.get_cart_items()
    cart_items_count = cart.get_cart_items_count()

    # Calculate item total costs
    item_total_cost = {ci.id: cart.calculate_item_total_cost(ci) for ci in cart_items}
    cart_sub_total = cart.calculate_sub_total()
    total_cost = cart.calculate_cart_total_cost()

    # Check if all cart items have a delivery method selected
    all_items_have_delivery_method = all(
        cart_item.delivery_method for cart_item in cart_items
    )  ###

    if not cart_items_count:
        messages.info(request, "Your cart is empty.")

    if not all_items_have_delivery_method:
        messages.warning(
            request,
            "Please select a delivery method for all items before proceeding to checkout.",
        )  

    context = {
        "cart_items": cart_items,
        "cart_items_count": cart_items_count,
        "item_total_cost": item_total_cost,
        "cart_sub_total": cart_sub_total,
        "delivery_methods": delivery_methods,
        "total_cost": total_cost,
        "order_id": 0,
        "all_items_have_delivery_method": all_items_have_delivery_method,
    }
    return render(request, "cart/cart.html", context)


def remove_from_cart(request, item_id):
    if request.method == "POST":
        # Get the specific CartItem instance and delete it
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        return redirect("view-cart")
