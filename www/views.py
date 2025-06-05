from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation.template import context_re
from django.contrib import messages
from authreg.forms import UserProfileForm
from orders.forms import *
from orders.models import *
from www.models import Product


def index(request):
    cat = Category.objects.all()
    products = Product.objects.all()
    category_id = request.GET.get('категория')

    if category_id:
        try:
            products = products.filter(category_id=category_id)
        except Category.DoesNotExist:
            products = Product.objects.none()

    # Получаем ID последних просмотренных товаров из сессии
    viewed_ids = request.session.get('viewed_products', [])
    viewed_products = Product.objects.filter(id__in=viewed_ids)

    # Чтобы сохранить порядок просмотра, сортируем вручную по списку viewed_ids
    viewed_products = sorted(viewed_products, key=lambda x: viewed_ids.index(x.id))

    form = OrderForm(user=request.user) if request.user.is_authenticated else None

    context = {
        'products': products,
        'cat': cat,
        'form': form,
        'viewed_products': viewed_products,
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def stocks(request):
    return render(request, 'stocks.html')


def shop(request, category_id=None):
    cat = Category.objects.all()

    if category_id:
        product = Product.objects.filter(category__id=category_id)
        brands = Brand.objects.filter(category__id=category_id)
        selected_category = get_object_or_404(Category, id=category_id)
    else:
        product = Product.objects.all()
        brands = Brand.objects.all()
        selected_category = None

    min_price = request.GET.get('minPrice')
    max_price = request.GET.get('maxPrice')
    brand_id = request.GET.get('brand')
    query = request.GET.get('query', '').strip()

    if min_price:
        product = product.filter(price__gte=min_price)
    if max_price:
        product = product.filter(price__lte=max_price)
    if brand_id and brand_id != 'all':
        product = product.filter(brand__id=brand_id)
    if query:
        product = product.filter(name__icontains=query)

    context = {
        'product': product,
        'cat': cat,
        'selected_category': selected_category,
        'brands': brands,
        'query': query,
    }
    return render(request, 'shop.html', context)


def update_cart_item(request, item_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove item if quantity is 0

    return redirect('cart')


def remove_cart_item(request, item_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request):
    cart = Cart.objects.get(user=request.user)
    total = cart.total_price
    return render(request, 'cart.html', {'cart': cart, 'total': total})


def shop_single(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    comments = Comment.objects.filter(product=product).order_by('-created_at')

    # Подсчет количества комментариев
    comment_count = comments.count()

    # Вычисление средней оценки
    if comment_count > 0:
        average_rating = sum(comment.rating for comment in comments) / comment_count
    else:
        average_rating = 0

    # Получение продуктов из той же категории
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)

    viewed = request.session.get('viewed_products', [])
    if id in viewed:
        viewed.remove(id)
    viewed.insert(0, id)  # Добавляем текущий товар в начало списка
    viewed = viewed[:5]  # Оставляем только 5 последних
    request.session['viewed_products'] = viewed
    request.session.modified = True

    context = {
        'product': product,
        'user': user,
        'comments': comments,
        'comment_count': comment_count,
        'average_rating': average_rating,
        'related_products': related_products,
    }
    return render(request, 'shop-single.html', context)


def acc(request):
    user = request.user
    address = Address.objects.filter(user=user)
    card = Card.objects.filter(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('acc')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserProfileForm(instance=user)

    context = {
        'user': user,
        'address': address,
        'card': card,
        'form': form
    }
    return render(request, 'user.html', context)


def orders(request):
    user = request.user
    orders = Orders.objects.filter(username=user).exclude(status__in=[3, 4]).prefetch_related(
        'items__product').order_by('-id')
    context = {
        'user': user,
        'orders': orders,
    }
    return render(request, 'orders/order_success.html', context)


def send_order_delivery_email(user_email, order_number):
    subject = 'Ваш заказ доставлен!'
    message = f'Здравствуйте!\n\nВаш заказ номер {order_number} был доставлен. Спасибо за покупку!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f'Ошибка при отправке письма: {e}')


def add_comment(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            return redirect('history')  # Перенаправление после успешного добавления
    else:
        form = CommentForm()
    return render(request, 'orders/history.html', {'product': product, 'form': form})
