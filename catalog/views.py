from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Product
from shop.models import Review, Wishlist


def catalog_view(request, category_slug=None):
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True).select_related('category')
    current_category = None

    if category_slug:
        current_category = get_object_or_404(categories, slug=category_slug)
        products = products.filter(category=current_category)

    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'catalog/catalog.html', {
        'categories': categories,
        'products': products,
        'current_category': current_category,
        'query': query,
    })


def product_detail_view(request, product_slug):
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('images'),
        slug=product_slug,
        is_active=True,
    )
    recommended_products = Product.objects.filter(
        category=product.category,
        is_active=True,
    ).exclude(pk=product.pk)[:4]

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'recommended_products': recommended_products,
    })


@login_required
def toggle_wishlist_view(request, product_slug):
    if request.method != 'POST':
        return redirect('product_detail', product_slug=product_slug)
    product = get_object_or_404(Product, slug=product_slug, is_active=True)
    item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, 'Товар добавлен в избранное.')
    else:
        item.delete()
        messages.info(request, 'Товар удалён из избранного.')
    return redirect(request.POST.get('next') or 'product_detail', product_slug=product_slug)


@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related('product', 'product__category')
    return render(request, 'catalog/wishlist.html', {'items': items})


@login_required
def add_review_view(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_active=True)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        if rating not in {'1', '2', '3', '4', '5'}:
            messages.error(request, 'Выберите оценку от 1 до 5.')
        else:
            Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={'rating': int(rating), 'comment': comment},
            )
            messages.success(request, 'Ваш отзыв сохранён.')
    return redirect('product_detail', product_slug=product.slug)
