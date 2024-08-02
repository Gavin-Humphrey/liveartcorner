import logging
from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import send_mail
from decouple import config
from item.models import CardItems, Item
from cart.shopping_cart import CartHandler
from wishlist.views import get_wishlist_items_count


logger = logging.getLogger(__name__)


def home(request):
    card_items = CardItems.objects.all()  # Query all CardItems objects
    # cart = ShoppingCart(request)
    cart = CartHandler(request)
    cart_items_count = cart.get_cart_items_count()
    wishlist_items_count = get_wishlist_items_count(request)
    popular_items = Item.objects.filter(popularity=5)[:4]
    context = {
        "card_items": card_items,
        "cart_items_count": cart_items_count,
        "wishlist_items_count": wishlist_items_count,
        "popular_items": popular_items,
    }  #
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


# live_art_corner footer contents

def faq(request):
    return render(request, 'base/faq.html')

def about_us(request):
    return render(request, 'base/about_us.html')

def terms_conditions(request):
    return render(request, 'base/terms_conditions.html')

def our_services(request):
    return render(request, 'base/our_services.html')

def privacy_policy(request):
    return render(request, 'base/privacy_policy.html')

def returns(request):
    return render(request, 'base/returns.html')

def affiliate_program(request):
    return render(request, 'base/affiliate_program.html')
