import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.core.mail import send_mail # Later
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from base.forms import RegisterForm, ArtistProfileForm, UserProfileForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, ArtistProfile




logger = logging.getLogger(__name__)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request,
            "Your email has been confirmed! Now you can log in to your account.",
        )
        logger.debug("Redirecting to login")
        return redirect("login")
    else:
        messages.error(request, "Activation link is invalid!")
        logger.debug("Redirecting to home due to invalid activation link")
    return redirect("home")


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string(
        "user/email_template.html",
        {
            "user": user.username,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(
            request,
            f"Hi {user}, an activation link has been sent to {to_email}, please click on it to confirm and complete your registration. \nYou may need to check your spam folder.",
        )
    else:
        messages.error(
            request,
            f"There's a problem sending email to {to_email}, check if you typed it correctly.",
        )




def login_view(request):
    page = "login"

    if request.user.is_authenticated:
        logger.debug("User already authenticated, redirecting to home")
        return redirect("login")

    try:
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                logger.debug("Login successful, redirecting to home")
                return redirect("home")
            else:
                raise ValueError("Invalid username or password")
        else:
            form = AuthenticationForm()

    except Exception as e:
        logger.error(f"An error occurred in loginPage view: {e}")
        messages.error(request, "Invalid name or password.")

    context = {"page": page, "form": form}
    return render(request, "user/login_signup.html", context)




def logout_view(request):
    logout(request)
    return redirect("home")



def registerUser(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_artist = form.cleaned_data.get('is_artist')
            user.is_active = False  # Set is_active to False until the user activates their account
            user.save()
            activateEmail(request, user, form.cleaned_data.get("email"))
            return redirect("login")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = RegisterForm()

    return render(
        request=request, template_name="user/login_signup.html", context={"form": form}
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
