import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from base.forms import RegisterForm, ArtistProfileForm, UserProfileForm
from .models import User, ArtistProfile
from item.models import CardItems





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


# @login_required
# def artist_profile_view(request, username):
#     try:
#         profile_user = User.objects.get(username=username)
#         artist_profile = profile_user.artistprofile
#     except User.DoesNotExist:
#         messages.error(request, "User not found.")
#         return redirect("home")
#     except ArtistProfile.DoesNotExist:
#         artist_profile = None

#     artist_profile_form_data = {
#         "Bio": artist_profile.bio,
#         "Portfolio URL": artist_profile.portfolio_url,
#         "Phone Number": artist_profile.phone_number,
#         "Location": artist_profile.location,
#         "Artistic Medium": artist_profile.artistic_medium,
#         "Experience Education": artist_profile.experience_education,
#     } if artist_profile else {}

#     context = {
#         "user": profile_user,
#         "artist_profile_form_data": artist_profile_form_data,
#     }
#     return render(request, "user/user_profile.html", context)

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


# @login_required
# def update_artist_profile(request):
#     user = request.user
#     if not user.is_vetted_artist:
#         messages.error(request, "You are not authorized to update artist profile.")
#         return redirect("home")

#     try:
#         artist_profile = user.artistprofile
#     except ArtistProfile.DoesNotExist:
#         artist_profile = ArtistProfile(user=user)

#     if request.method == "POST":
#         logger.debug("POST data: %s", request.POST)
#         logger.debug("FILES data: %s", request.FILES)
        
#         user_form = UserProfileForm(request.POST, instance=user)
#         profile_form = ArtistProfileForm(request.POST, request.FILES, instance=artist_profile)
        
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, "Profile updated successfully.")
#             return redirect("artist-profile", username=user.username)
#         else:
#             logger.error("User form errors: %s", user_form.errors)
#             logger.error("Profile form errors: %s", profile_form.errors)
#             messages.error(request, "Error updating your profile.")
#     else:
#         user_form = UserProfileForm(instance=user)
#         profile_form = ArtistProfileForm(instance=artist_profile)

#     context = {
#         "user_form": user_form,
#         "profile_form": profile_form,
#         "form_title": "Update Your Profile",
#         "button_text": "Save Changes"
#     }
#     return render(request, "user/update_artist_profile.html", context)

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

# @login_required
# def artist_dashboard(request, username):
#     user = get_object_or_404(User, username=username)

#     if not user.is_artist:
#         messages.error(request, "This user is not an artist.")
#         return redirect("home")

#     if request.user != user:
#         messages.error(request, "You are not authorized to view this dashboard.")
#         return redirect("home")

#     try:
#         card_items = CardItems.objects.get(user=user)
#         items_count = card_items.items.count()
#     except CardItems.DoesNotExist:
#         items_count = 0

#     context = {
#         'user': user,
#         'items_count': items_count,
#         # Add other context data as needed
#     }
#     return render(request, 'user/artist_dashboard.html', context)

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
        # Add other context data as needed
    }
    return render(request, 'user/artist_dashboard.html', context)

@login_required
def manage_items(request):
    # Placeholder view for managing items
    return render(request, 'manage_items.html')

@login_required
def manage_availability(request):
    # Placeholder view for managing availability
    return render(request, 'manage_availability.html')

@login_required
def manage_calendar(request):
    # Placeholder view for managing calendar
    return render(request, 'manage_calendar.html')

@login_required
def upload_files(request):
    # Placeholder view for uploading files
    return render(request, 'upload_files.html')
