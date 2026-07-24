from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Product

from .models import Cart, CartItem


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/cart.html', {'cart': cart})


@login_required
def add_to_cart_view(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_active=True)
    if request.method == 'POST':
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += 1
        if item.quantity > product.stock:
            messages.error(request, 'Нельзя добавить больше товаров, чем есть в наличии.')
        else:
            item.save()
            messages.success(request, 'Товар добавлен в корзину.')
    return redirect(request.POST.get('next') or 'product_detail', product_slug=product.slug)


@login_required
def update_cart_item_view(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = request.POST.get('quantity', '')
        if quantity.isdigit() and int(quantity) > 0:
            if int(quantity) <= item.product.stock:
                item.quantity = int(quantity)
                item.save()
                messages.success(request, 'Количество обновлено.')
            else:
                messages.error(request, 'Количество превышает остаток товара.')
        else:
            item.delete()
            messages.info(request, 'Товар удалён из корзины.')
    return redirect('cart')


@login_required
def remove_cart_item_view(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.info(request, 'Товар удалён из корзины.')
    return redirect('cart')
