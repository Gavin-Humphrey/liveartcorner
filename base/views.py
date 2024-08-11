import logging
from django.shortcuts import render
from django_secure_contact_form.forms import ContactForm
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
    }  
    return render(request, "base/home.html", context)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            #custom_field = form.cleaned_data.get("custom_field", "") # Use when customize form

            try:
                send_mail(
                    f"Contact Form Submission - {subject}",
                    f"Full Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}", # Use when customize form # \nCustom Field: {custom_field} 
                    config("WEBSITE_EMAIL", default="backup@example.com"),  
                    [config("WEBSITE_EMAIL", default="backup@example.com")], 
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error and add a form error message
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to send email: {e}")
                form.add_error(None, "There was a problem sending your message. Please try again later.")
                return render(request, "base/contact.html", {"form": form})

            return render(request, "base/thank_you.html", {"name": name})
    else:
        form = ContactForm()

    return render(request, "base/contact.html", {"form": form})


# footer contents

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
