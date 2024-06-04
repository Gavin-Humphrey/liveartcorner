import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from base.forms import RegisterForm, ArtistProfileForm, UserProfileForm, ArtistAvailabilityForm
from .models import User, ArtistProfile, ArtistAvailability
from item.models import CardItems, Item
from services.models import Booking



logger = logging.getLogger(__name__)


def registerUser(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_artist = form.cleaned_data.get('is_artist')
            user.save()
            return redirect("login")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = RegisterForm()

    return render(
        request=request, template_name="user/signup_login.html", context={"form": form}
    )


@login_required
def artist_profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    try:
        artist_profile = profile_user.artistprofile
    except ArtistProfile.DoesNotExist:
        artist_profile = None

    artist_profile_form_data = {
        "Bio": artist_profile.bio,
        "Portfolio URL": artist_profile.portfolio_url,
        "Phone Number": artist_profile.phone_number,
        "Location": artist_profile.location,
        "Artistic Medium": artist_profile.artistic_medium,
        "Experience Education": artist_profile.experience_education,
    } if artist_profile else {}

    context = {
        "user": profile_user,
        "artist_profile_form_data": artist_profile_form_data,
    }
    return render(request, "user/user_profile.html", context)


@login_required
def update_artist_profile(request):
    user = request.user
    if not user.is_vetted_artist:
        messages.error(request, "You are not authorized to update artist profile.")
        return redirect("home")

    try:
        artist_profile = user.artistprofile
    except ArtistProfile.DoesNotExist:
        artist_profile = ArtistProfile(user=user)

    if request.method == "POST":
        logger.debug("POST data: %s", request.POST)
        logger.debug("FILES data: %s", request.FILES)
        
        user_form = UserProfileForm(request.POST, instance=user)
        profile_form = ArtistProfileForm(request.POST, request.FILES, instance=artist_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("artist-profile", user_id=user.id)
        else:
            logger.error("User form errors: %s", user_form.errors)
            logger.error("Profile form errors: %s", profile_form.errors)
            messages.error(request, "Error updating your profile.")
    else:
        user_form = UserProfileForm(instance=user)
        profile_form = ArtistProfileForm(instance=artist_profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "form_title": "Update Your Profile",
        "button_text": "Save Changes"
    }
    return render(request, "user/update_artist_profile.html", context)



@login_required
def artist_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)
    

    if not user.is_artist:
        messages.error(request, "This user is not an artist.")
        return redirect("home")

    if request.user != user:
        messages.error(request, "You are not authorized to view this dashboard.")
        return redirect("home")

    try:
        card_items = CardItems.objects.get(user=user)
        items_count = card_items.items.count()
    except CardItems.DoesNotExist:
        items_count = 0


    context = {
        'user': user,
        'items_count': items_count,
        #'availability': availability,
    }
    return render(request, 'user/artist_dashboard.html', context)


@login_required
def manage_items(request):
    user = request.user

    try:
        card_items = CardItems.objects.get(user=user)
    except CardItems.DoesNotExist:
        messages.error(request, "You have no items to manage.")
        return redirect('home')

    items = card_items.items.all()

    if request.method == 'POST':
        any_changes = False
        for item in items:
            quantity_field = f'quantity_{item.id}'
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

        return redirect('manage-items')

    return render(request, 'item/manage_items.html', {'items': items})


@login_required
def manage_availability(request):
    user = request.user

    try:
        card_items = CardItems.objects.get(user=user)
    except CardItems.DoesNotExist:
        messages.error(request, "You have no items to manage.")
        return redirect('home')

    items = card_items.items.all()

    if request.method == 'POST':
        any_changes = False
        for item in items:
            availability_field = f'is_available_{item.id}'
            new_availability = availability_field in request.POST  
            
            if new_availability != item.is_available:
                item.is_available = new_availability
                item.save()
                any_changes = True

        if any_changes:
            messages.success(request, "Item availability updated successfully.")
        else:
            messages.info(request, "No changes were made.")

        return redirect('manage-availability')

    return render(request, 'item/manage_availability.html', {'items': items})


@login_required
def create_artist_availability_calendar(request):
    if request.method == 'POST':
        form = ArtistAvailabilityForm(request.POST)
        if form.is_valid():
            form.instance.artist = request.user
            form.save()
            return redirect('artist-availability-calendar')  
    else:
        form = ArtistAvailabilityForm()

    context = {"form": form, "form_title": "Add Your Availability", "button_text": "Add"}
    return render(request, "item/items_form.html", context)


@login_required
def artist_availability_calendar(request):
    user = request.user
    availabilities = ArtistAvailability.objects.filter(artist=user).order_by('date', 'start_time')
    context = {'availabilities': availabilities}
    return render(request, 'user/artist_availability_calendar.html', context)


@login_required
def update_artist_availability_calendar(request, pk):
    try:
        artist_availability = ArtistAvailability.objects.get(artist=request.user, pk=pk)
    except ArtistAvailability.DoesNotExist:
        # If no matching availability record is found, display an error message
        messages.error(request, "No availability record found for this artist.")
        return redirect('artist-dashboard', user_id=request.user.id)

    if request.method == 'POST':
        form = ArtistAvailabilityForm(request.POST, instance=artist_availability)
        if form.is_valid():
            form.save()
            return redirect('artist-availability-calendar')  
    else:
        form = ArtistAvailabilityForm(instance=artist_availability)

    context = {"form": form, "form_title": "Update Your Availability", "button_text": "Update"}
    return render(request, "item/items_form.html", context)


@login_required
def delete_artist_availability(request, pk):
    artist_availability = get_object_or_404(ArtistAvailability, pk=pk)
    user = request.user
    if user.is_vetted_artist:
        if request.method == 'POST':
            artist_availability.delete()
            return redirect("artist-availability-calendar")
        else:
            return render(request, "user/user_confirm_delete.html", {"artist_availability": artist_availability})
    else:
        return redirect('artist-availability-calendar')
    

def get_artist_bookings(request):
    user = request.user
    bookings = Booking.objects.filter(availability__artist=user).order_by('-availability__date')  # filter by artist's availability
    logger.error("These are your bookings: ", bookings)
    context = {'bookings': bookings,}
    return render(request, 'user/artist_bookings.html', context)

@login_required
def upload_files(request):
    return render(request, 'upload_files.html')
