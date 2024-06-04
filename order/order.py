from .models import Order, OrderItem, DeliveryInfo



def create_order(user, delivery_data, chosen_delivery_method):
    # Create delivery info
    delivery_info = DeliveryInfo.objects.create(
        full_name=delivery_data['full_name'],
        address=delivery_data['address'],
        email=delivery_data['email'],
        phone_number=delivery_data['phone_number']
    )

    # Determine user and order type
    if user.is_authenticated:
        order_user = user
        order_type = 'authenticated'
    else:
        order_user = None
        order_type = 'guest'

    # Create the order
    order = Order.objects.create(
        user=order_user,
        order_type=order_type,
        total_cost=delivery_data['total_cost'],
        delivery_method=chosen_delivery_method,  # Chosen_delivery_method is an instance
        order_status='Pending',
        delivery_info=delivery_info
    )

    return order



