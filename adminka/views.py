from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from pyexpat.errors import messages

from adminka.forms import ProductForm, BrandForm
from authreg.models import CustomUser
from orders.models import Orders, Status
from www.models import *


def add_product(request):
    categories = Category.objects.all()  # Получаем все категории
    brands = Brand.objects.all()  # Получаем все бренды
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        photo = request.FILES.get('photo')
        quantity = request.POST.get('quantity')
        category_id = request.POST.get('category')  # Получаем выбранную категорию
        brand_id = request.POST.get('brand')  # Получаем выбранный бренд

        # Проверка на наличие всех необходимых полей
        if not all([name, price, description, quantity, photo, category_id, brand_id]):
            messages.error(request, 'Пожалуйста, заполните все поля.')
            return render(request, 'adminka/adminka.html', {'categories': categories, 'brands': brands})

        # Создание нового продукта
        product = Product(
            name=name,
            price=price,
            description=description,
            photo=photo,
            quantity=quantity,
            brand_id=brand_id,  # Привязываем выбранный бренд к продукту
            category_id=category_id  # Привязываем выбранную категорию к продукту
        )
        product.save()

        return redirect('index')  # Перенаправление на страницу со списком товаров

    return render(request, 'adminka/adminka.html', {'categories': categories, 'brands': brands})


def admin_product(request, id):
    product = get_object_or_404(Product, id=id)
    categories = Category.objects.all()
    brands = Brand.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'categories': categories,
        'brands': brands
    }

    return render(request, 'adminka/a_product.html', context)


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('index')


def a_user(request):
    users = CustomUser.objects.all()
    context = {
        'users': users
    }
    return render(request, 'adminka/a_user.html', context)


def a_brend(request):
    brands = Brand.objects.all()

    if request.method == 'POST':
        if 'add_brand' in request.POST:
            form = BrandForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('a_brend')  # Redirect to the same page after adding
        elif 'delete_brand' in request.POST:
            brand_id = request.POST.get('brand_id')
            brand = get_object_or_404(Brand, id=brand_id)
            brand.delete()
            return redirect('a_brend')  # Redirect to the same page after deletion

    context = {
        'brands': brands,
        'form': BrandForm()  # Pass the form to the template
    }
    return render(request, 'adminka/a_brend.html', context)


def a_orders(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status_id = request.POST.get('status_id')

        order = get_object_or_404(Orders, id=order_id)
        status = get_object_or_404(Status, id=status_id)

        order.status = status
        order.save()

        # Отправка письма, если статус "доставлен"
        if status.name.lower() == 'доставлен':
            subject = f'Заказ {order.order_number} доставлен'
            message = f'Ваш заказ №{order.order_number} был успешно доставлен. Назовите номер заказа сотруднику для получения.'
            from_email = 'your-email@example.com'  # Обычно берется из settings.DEFAULT_FROM_EMAIL
            recipient_list = [order.username.email]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            except Exception as e:
                print(f"Ошибка при отправке почты: {e}")

        return redirect('a_orders')

    order = Orders.objects.all().order_by('-created_at')
    statuses = Status.objects.all()
    context = {
        'order': order,
        'statuses': statuses
    }
    return render(request, 'adminka/a_orders.html', context)
