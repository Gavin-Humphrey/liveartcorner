import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from item.models import CardItems, Item
from order.models import OrderItem
from services.models import Booking
from base.forms import ArtistAvailabilityForm
from user.models import User, ArtistAvailability


logger = logging.getLogger(__name__)


@login_required
def artist_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)
    availabilities = ArtistAvailability.objects.filter(artist=user).order_by(
        "date", "start_time"
    )
    bookings = Booking.objects.filter(availability__artist=user).order_by(
        "-availability__date"
    )
    ordered_items = OrderItem.objects.filter(item__card__user=user).select_related(
        "order", "item"
    )

    if not user.is_artist:
        messages.error(request, "This user is not an artist.")
        return redirect("home")

    if request.user != user:
        messages.error(request, "You are not authorized to view this dashboard.")
        return redirect("home")

    try:
        card_items = CardItems.objects.get(user=user)
        items = card_items.items.all()
        items_count = card_items.items.count()
    except CardItems.DoesNotExist:
        items = []
        items_count = 0
    # Debugging output to console
    print("Debug: Items in dashboard view:", items)
    print("Debug: Items count in dashboard view:", items_count)

    context = {
        "user": user,
        "items": items,
        "items_count": items_count,
        "availabilities": availabilities,
        "bookings": bookings,
        "ordered_items": ordered_items,
    }
    return render(request, "dashboard/artist_dashboard.html", context)


@login_required
def manage_items(request):
    user = request.user

    try:
        card_items = CardItems.objects.get(user=user)
    except CardItems.DoesNotExist:
        messages.error(request, "You have no items to manage.")
        return redirect("home")

    items = card_items.items.all()

    if request.method == "POST":
        any_changes = False
        for item in items:
            quantity_field = f"quantity_{item.id}"
            if quantity_field in request.POST:
                new_quantity = request.POST[quantity_field]
                try:
                    new_quantity = int(new_quantity)
                    if new_quantity != item.quantity:
                        item.quantity = new_quantity
                        item.save()
                        any_changes = True
                except ValueError:
                    messages.error(request, f"Invalid quantity for {item.title}")

        if any_changes:
            messages.success(request, "Item quantities updated successfully.")
        else:
            messages.info(request, "No changes were made.")

        return redirect("manage-items")
    return render(request, "item/manage_items.html", {"items": items})


@login_required
def manage_items_availability(request):
    user = request.user

    try:
        card_items = CardItems.objects.get(user=user)
    except CardItems.DoesNotExist:
        messages.error(request, "You have no items to manage.")
        return redirect("home")

    items = card_items.items.all()

    if request.method == "POST":
        any_changes = False
        for item in items:
            availability_field = f"is_available_{item.id}"
            new_availability = availability_field in request.POST

            if new_availability != item.is_available:
                item.is_available = new_availability
                item.save()
                any_changes = True

        if any_changes:
            messages.success(request, "Item availability updated successfully.")
        else:
            messages.info(request, "No changes were made.")

        # return redirect('manage-availability')
        return redirect("manage-items-availability")

    return render(request, "item/manage_availability.html", {"items": items})


@login_required
def create_artist_availability_calendar(request):
    if request.method == "POST":
        form = ArtistAvailabilityForm(request.POST)
        if form.is_valid():
            form.instance.artist = request.user
            form.save()
            return redirect("artist-availability-calendar")
    else:
        form = ArtistAvailabilityForm()

    context = {
        "form": form,
        "form_title": "Add Your Availability",
        "button_text": "Add",
    }
    return render(request, "item/items_form.html", context)


@login_required
def artist_availability_calendar(request):
    user = request.user
    availabilities = ArtistAvailability.objects.filter(artist=user).order_by(
        "date", "start_time"
    )
    context = {"availabilities": availabilities}
    return render(request, "dashboard/artist_availability_calendar.html", context)


@login_required
def update_artist_availability_calendar(request, pk):
    try:
        artist_availability = ArtistAvailability.objects.get(artist=request.user, pk=pk)
    except ArtistAvailability.DoesNotExist:
        # If no matching availability record is found, display an error message
        messages.error(request, "No availability record found for this artist.")
        return redirect("artist-dashboard", user_id=request.user.id)

    if request.method == "POST":
        form = ArtistAvailabilityForm(request.POST, instance=artist_availability)
        if form.is_valid():
            form.save()
            return redirect("artist-availability-calendar")
    else:
        form = ArtistAvailabilityForm(instance=artist_availability)

    context = {
        "form": form,
        "form_title": "Update Your Availability",
        "button_text": "Update",
    }
    return render(request, "item/items_form.html", context)


@login_required
def delete_artist_availability(request, pk):
    artist_availability = get_object_or_404(ArtistAvailability, pk=pk)
    user = request.user
    if user.is_vetted_artist:
        if request.method == "POST":
            artist_availability.delete()
            return redirect("artist-availability-calendar")
        else:
            return render(
                request,
                "user/user_confirm_delete.html",
                {"artist_availability": artist_availability},
            )
    else:
        return redirect("artist-availability-calendar")


def get_artist_bookings(request):
    user = request.user
    bookings = Booking.objects.filter(availability__artist=user).order_by(
        "-availability__date"
    )  # filter by artist's availability
    logger.error("These are your bookings: ", bookings)
    context = {
        "bookings": bookings,
    }
    return render(request, "dashboard/artist_bookings.html", context)


@login_required
def artist_ordered_items(request):
    user = request.user

    # Get all order items where the item belongs to the current artist
    ordered_items = OrderItem.objects.filter(item__card__user=user).select_related(
        "order", "item"
    )
    for order_item in ordered_items:
        print("Order Item Price:", order_item.price)
    context = {
        "ordered_items": ordered_items,
    }
    return render(request, "dashboard/artist_ordered_items.html", context)


@login_required
def upload_files(request):
    return render(request, "upload_files.html")
