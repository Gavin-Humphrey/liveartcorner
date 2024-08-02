from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from item.models import Item
from .models import WishList, WishListItem
from django.contrib.auth.decorators import login_required


@login_required
def add_to_wishlist(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    wishlist, created = WishList.objects.get_or_create(user=request.user)
    if not WishListItem.objects.filter(wishlist=wishlist, item=item).exists():
        WishListItem.objects.create(wishlist=wishlist, item=item)
        messages.success(request, "Item added to your wishlist.")
    else:
        messages.error(request, "Item is already in your wishlist.")
    return redirect("item-detail", item_id=item_id)


@login_required
def my_wishlist(request):
    try:
        wishlist = WishList.objects.get(user=request.user)
        wishlist_items = wishlist.wishlist_items.all()
        if not wishlist_items:
            #messages.success(request, "Your Wishlist Is Empty.")
            return redirect("home")
    except WishList.DoesNotExist:
        wishlist = None
        wishlist_items = []

    return render(
        request,
        "wishlist/wishlist.html",
        {"wishlist": wishlist, "wishlist_items": wishlist_items},
    )


@login_required
def get_wishlist_items_count(request):
    try:
        wishlist = WishList.objects.get(user=request.user)
        wishlist_items_count = wishlist.wishlist_items.count()
    except WishList.DoesNotExist:
        wishlist_items_count = 0
    return wishlist_items_count


@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    wishlist = get_object_or_404(WishList, user=request.user)
    wishlist_item = get_object_or_404(WishListItem, wishlist=wishlist, item=item)
    wishlist_item.delete()
    return redirect("my-wishlist")
