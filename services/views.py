from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from base.forms import ServiceForm
from services.models import Service
from user.models import ArtistAvailability
from django.contrib.auth.decorators import login_required
import datetime
from datetime import timedelta
from .models import Booking


@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.artist = request.user  # Set the artist to the current user
            service.save()
            messages.success(request, "Service added successfully!")
            return redirect('artist-dashboard', user_id=request.user.id)
        else:
            messages.error(request, "There was an error adding the service.")
    else:
        form = ServiceForm()
    return render(request, 'services/add_service.html', {'form': form})

def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/services_list.html', {'services': services})

### Do this later
def service_detail(request, service_id):
    service = Service.objects.get(pk=service_id)
    return render(request, 'services/service_detail.html', {'service': service})


@login_required
def update_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            user = request.user
            if user.is_vetted_artist:
                form.save()
                return redirect("services-list")
            else:
                # Redirect or show message indicating restricted access
                return redirect('services-list')
    else:
        form = ServiceForm(instance=service)
    context = {"form": form, "form_title": "Update Your Service", "button_text": "Update"}
    return render(request, "item/items_form.html", context)



@login_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    user = request.user
    if user.is_vetted_artist:
        if request.method == 'POST':
            service.delete()
            return redirect("services-list")
        else:
            return render(request, "services/service_confirm_delete.html", {"service": service})
    else:
        # Redirect or show message indicating restricted access
        return redirect('services-list')
    

@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    artist = service.artist
    user = request.user

    # Get available artist time slots for the service
    available_slots = ArtistAvailability.objects.filter(
        artist=artist,
        booked=False
    ).select_related('artist') 

    if request.method == 'POST':
        selected_slot_id = request.POST.get('availability_slot')
        selected_slot = ArtistAvailability.objects.get(pk=selected_slot_id)

        # Check if the selected slot is already booked
        if selected_slot.booked:
            # Handle error: Slot already booked

            booking = Booking.objects.create(
            user=request.user,
            availability_slot=selected_slot,
            service=service  
        )

        # Update booked flag for the selected slot
        selected_slot.booked = True
        selected_slot.save()

        # Handle successful booking (confirmation message, emails, etc.)

    return render(request, "services/service_booking.html", {
        "service": service,
        "available_slots": available_slots
    })


    

