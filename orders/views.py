from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import *
from .models import *

from django.shortcuts import render, redirect
from .models import Orders, Product


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    quantity = int(request.POST.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(user=user)
    cart_item = cart.items.filter(product=product).first()

    if cart_item:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)

    return redirect('cart')


def order_create(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = OrderOneForm(request.POST, user=request.user)
        if form.is_valid():
            order = Orders.objects.create(
                username=request.user,
                address=form.cleaned_data['address'],
                card=form.cleaned_data['card'],
                status=Status.objects.get(name='В обработке')  # или нужный статус
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=form.cleaned_data['quantity']
            )

            return redirect('orders')

    else:
        form = OrderOneForm(user=request.user)

    return render(request, 'index.html', {'form': form, 'product': product})


def checkout(request):
    cart = Cart.objects.get(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart.items.all())

    if request.method == 'POST':
        form = OrderForm(request.user, request.POST)
        if form.is_valid():
            order = Orders.objects.create(
                username=request.user,
                address=form.cleaned_data['address'],
                card=form.cleaned_data['card'],
                status=Status.objects.get(name='В обработке')  # или соответствующий статус
            )
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )
            cart.items.all().delete()  # Очистить корзину
            return redirect('massage')
    else:
        form = OrderForm(request.user)

    return render(request, 'orders/create.html', {'form': form, 'total_price': total_price})

def massage(request):
    return render(request, 'orders/massage.html')

def add_address(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        Address.objects.create(address=address, user=request.user)
        referer = request.META.get('HTTP_REFERER')  # URL страницы, с которой пришёл запрос
        if referer:
            return redirect(referer)
        else:
            return redirect('acc')


def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    return redirect('acc')


def add_cart(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        code = request.POST.get('code')
        date_cart = request.POST.get('date_cart')
        Card.objects.create(number=number, code=code, date_cart=date_cart, user=request.user)

        referer = request.META.get('HTTP_REFERER')  # URL страницы, с которой пришёл запрос
        if referer:
            return redirect(referer)
        else:
            return redirect('acc')


def delete_card(request, card_id):
    card = get_object_or_404(Card, id=card_id, user=request.user)
    card.delete()
    return redirect('acc')


def history(request):
    orders = Orders.objects.filter(username=request.user, status__in=[3, 4])
    order_items = OrderItem.objects.filter(order__in=orders).select_related('product')

    product_ids = order_items.values_list('product__id', flat=True).distinct()
    comments = Comment.objects.filter(product__in=product_ids).order_by('-created_at')

    form = CommentForm()  # например, форма для добавления комментария

    context = {
        'products': order_items,
        'comments': comments,
        'form': form,  # передаем форму
    }
    return render(request, 'orders/history.html', context)
