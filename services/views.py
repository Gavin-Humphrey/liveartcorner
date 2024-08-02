from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from base.forms import ServiceForm, BookingForm
from services.models import Service
from user.models import ArtistAvailability
from django.contrib.auth.decorators import login_required
from .models import Booking


@login_required
def add_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.artist = request.user  # Set the artist to the current user
            service.save()
            messages.success(request, "Service added successfully!")
            return redirect("artist-dashboard", user_id=request.user.id)
        else:
            messages.error(request, "There was an error adding the service.")
    else:
        form = ServiceForm()
    return render(request, "services/add_service.html", {"form": form})


def service_list(request):
    services = Service.objects.all()
    return render(request, "services/services_list.html", {"services": services})


### Do this later
def service_detail(request, service_id):
    service = Service.objects.get(pk=service_id)
    return render(request, "services/service_detail.html", {"service": service})


@login_required
def update_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            user = request.user
            if user.is_vetted_artist:
                form.save()
                return redirect("services-list")
            else:
                # Redirect or show message indicating restricted access
                return redirect("services-list")
    else:
        form = ServiceForm(instance=service)
    context = {
        "form": form,
        "form_title": "Update Your Service",
        "button_text": "Update",
    }
    return render(request, "item/items_form.html", context)


@login_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    user = request.user
    if user.is_vetted_artist:
        if request.method == "POST":
            service.delete()
            return redirect("services-list")
        else:
            return render(
                request, "services/service_confirm_delete.html", {"service": service}
            )
    else:
        # Redirect or show message indicating restricted access
        return redirect("services-list")


# def service_booking(request, service_id):
#     service = get_object_or_404(Service, id=service_id)
#     artist = service.artist
#     available_slots = ArtistAvailability.objects.filter(artist=artist, booked=False)


#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             selected_slot_id = request.POST.get('availability_slot')
#             selected_slot = ArtistAvailability.objects.get(pk=selected_slot_id)
#             if selected_slot.booked:
#                 error_message = 'Selected slot is already booked. Please choose another time.'
#                 return render(request, "services/service_booking.html", {"service": service, "available_slots": available_slots, "form": form, "error_message": error_message})
#             # Save the user information
#             booking = form.save(commit=False)
#             booking.user = request.user
#             booking.service = service
#             booking.availability = selected_slot
#             booking.save()
#             selected_slot.booked = True
#             selected_slot.save()
#             # Redirect to a view to display booking summary
#             return redirect('booking-summary', service_id=service_id, booking_id=booking.id)
#         else:
#             error_message = 'Invalid form data. Please try again.'
#             return render(request, "services/service_booking.html", {"service": service, "available_slots": available_slots, "form": form, "error_message": error_message})
#     else:
#         form = BookingForm()  # Create a booking form instance
#     context = {
#         "service": service,
#         "available_slots": available_slots,
#         "form": form,
#     }
#     return render(request, "services/service_booking.html", context)
def service_booking(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    artist = service.artist
    available_slots = ArtistAvailability.objects.filter(artist=artist, booked=False)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            selected_slot_id = request.POST.get("availability_slot")
            selected_slot = get_object_or_404(ArtistAvailability, pk=selected_slot_id)

            # Save the user information
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.availability = selected_slot
            booking.save()

            # Mark the slot as booked
            selected_slot.booked = True
            selected_slot.save()

            # Redirect to a view to display booking summary
            return redirect(
                "booking-summary", service_id=service_id, booking_id=booking.id
            )

    else:
        form = BookingForm()  # Create a booking form instance

    context = {
        "service": service,
        "available_slots": available_slots,
        "form": form,
    }
    return render(request, "services/service_booking.html", context)


def booking_summary(request, service_id, booking_id):
    service = get_object_or_404(Service, id=service_id)
    booking = get_object_or_404(Booking, id=booking_id)
    context = {
        "service": service,
        "booking": booking,
    }
    return render(request, "services/booking_summary.html", context)
