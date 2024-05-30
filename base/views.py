import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import RegisterForm, ArtistProfileForm, UserProfileForm,  ItemForm, ContactForm
from django.core.mail import send_mail
from decouple import config

from item.models import CardItems, Item
from cart.shopping_cart import CartHandler 
#from wishlist.views import get_wishlist_items, get_wishlist_items_count
from wishlist.views import my_wishlist,  get_wishlist_items_count


logger = logging.getLogger(__name__)



def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    try:
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect("home")
            else:
                raise ValueError("Invalid username or password")
        else:
            form = AuthenticationForm()

    except Exception as e:
        logger.error(f"An error occurred in loginPage view: {e}")
        messages.error(request, "Invalid name or password.")

    context = {"page": page, "form": form}
    return render(request, "user/signup_login.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")


def home(request):
    card_items = CardItems.objects.all()  # Query all CardItems objects
    # cart = ShoppingCart(request)
    cart = CartHandler(request)
    cart_items_count = cart.get_cart_items_count()
    wishlist_items_count = get_wishlist_items_count(request)
    popular_items = Item.objects.filter(popularity=5)[:4]
    context = {"card_items": card_items, 'cart_items_count': cart_items_count, 'wishlist_items_count': wishlist_items_count, 'popular_items': popular_items}# 
    return render(request, "base/home.html", context)



# Contact to become a seller
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data and send email
            firstname = form.cleaned_data["firstname"]
            lastname = form.cleaned_data["lastname"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            send_mail(
                f"Contact Form Submission - {subject}",
                f"Firstame: {firstname}\nLastname: {lastname}\nEmail: {email}\nSubject: {subject}\nMessage: {message}",
                "noreply@film.junkiez.com",
                [config("WEBSITE_EMAIL", default="backup@example.com")],
                fail_silently=False,
            )
            return render(request, "base/thank_you.html", {"firstname": firstname})
    else:
        form = ContactForm()

    return render(request, "base/contact.html", {"form": form})