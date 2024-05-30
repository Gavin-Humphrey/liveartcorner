from django.shortcuts import render, redirect, get_object_or_404
from base.forms import  ItemForm
from django.contrib.auth.decorators import login_required
from .models import CardItems, Item
from cart.shopping_cart import CartHandler 
#from wishlist.views import get_wishlist_items, get_wishlist_items_count
from wishlist.views import my_wishlist,  get_wishlist_items_count






@login_required
def upload_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            if user.is_vetted_artist:
                card_items, created = CardItems.objects.get_or_create(user=user)
                form.instance.card = card_items
                form.save()
                return redirect("home")
            else:
                # Redirect or show message indicating restricted access
                return redirect('home')
    else:
        form = ItemForm()
    context = {"form": form, "form_title": "Upload Your Product", "button_text": "Submit"}
    return render(request, "item/items_form.html", context)

@login_required
def update_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            user = request.user
            if user.is_vetted_artist:
                form.save()
                return redirect("home")
            else:
                # Redirect or show message indicating restricted access
                return redirect('home')
    else:
        form = ItemForm(instance=item)
    context = {"form": form, "form_title": "Update Your Product", "button_text": "Update"}
    return render(request, "item/items_form.html", context)

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    user = request.user
    if user.is_vetted_artist:
        if request.method == 'POST':
            item.delete()
            return redirect("home")
        else:
            return render(request, "item/confirm_delete.html", {"item": item})
    else:
        # Redirect or show message indicating restricted access
        return redirect('home')

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart = CartHandler(request)
    cart_items_count = cart.get_cart_items_count()
    #wishlist_items_count = get_wishlist_items_count(request)
    #wishlist_items = get_wishlist_items(request)
    wishlist_items = my_wishlist(request)
    context = {'item': item, 'cart_items_count': cart_items_count, 'wishlist_items': wishlist_items}
    return render(request, 'item/items_detail.html', context)