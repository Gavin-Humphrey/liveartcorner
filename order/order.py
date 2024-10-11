from .models import Order, DeliveryInfo

# import sys
# import os
# sys.stdout = open(os.devnull, 'w')


def create_order(user, delivery_data):
    total_cost = delivery_data.get("total_cost", 0)

    # Create delivery info
    delivery_info = DeliveryInfo.objects.create(
        full_name=delivery_data["full_name"],
        email=delivery_data["email"],
        address=delivery_data["address"],
        city=delivery_data["city"],
        postcode=delivery_data["postcode"],
        country=delivery_data["country"],
        phone_number=delivery_data["phone_number"],
    )

    # Determine user and order type
    order_user = user if user.is_authenticated else None
    order_type = "authenticated" if user.is_authenticated else "guest"

    # Create the order
    order = Order.objects.create(
        user=order_user,
        order_type=order_type,
        total_cost=total_cost,
        order_status="Pending",
        delivery_info=delivery_info,
    )

    return order
