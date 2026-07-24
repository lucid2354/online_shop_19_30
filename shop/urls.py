from django.urls import path

from .views import add_to_cart_view, cart_view, remove_cart_item_view, update_cart_item_view

urlpatterns = [
    path('', cart_view, name='cart'),
    path('add/<slug:product_slug>/', add_to_cart_view, name='add_to_cart'),
    path('item/<int:item_id>/update/', update_cart_item_view, name='update_cart_item'),
    path('item/<int:item_id>/remove/', remove_cart_item_view, name='remove_cart_item'),
]
