from django.urls import path

from .views import add_review_view, catalog_view, product_detail_view, toggle_wishlist_view, wishlist_view

urlpatterns = [
    path('', catalog_view, name='catalog'),
    path('category/<slug:category_slug>/', catalog_view, name='products_by_category'),
    path('product/<slug:product_slug>/', product_detail_view, name='product_detail'),
    path('product/<slug:product_slug>/wishlist/', toggle_wishlist_view, name='toggle_wishlist'),
    path('product/<slug:product_slug>/review/', add_review_view, name='add_review'),
    path('wishlist/', wishlist_view, name='wishlist'),
]
