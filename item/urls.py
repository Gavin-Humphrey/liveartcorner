from django.urls import path
from . import views


urlpatterns = [
    path("upload-item/", views.upload_item, name="upload-item"),
    path("update-item/<int:item_id>/", views.update_item, name="update-item"),
    path("delete-item/<int:item_id>/", views.delete_item, name="delete-item"),
    path("item/<int:item_id>/", views.item_detail, name="item-detail"),
    path("search/", views.search_items, name="search-items"),
]
