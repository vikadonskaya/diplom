from django.db import models
from authreg.models import *
from www.models import *

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return self.address


class Card(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    number = models.IntegerField(verbose_name="Номер карты")
    code = models.IntegerField(verbose_name="Код карты")
    date_cart = models.IntegerField(verbose_name="Срок действия карты")

    def __str__(self):
        return str(self.number)


class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name="Статус заказа")

    def __str__(self):
        return self.name


import random

class Orders(models.Model):
    order_number = models.CharField(max_length=4, unique=True, blank=True, verbose_name="Номер заказа")
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Адрес")
    card = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name="Карта")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.order_number} - {self.username.username}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_unique_order_number()
        super().save(*args, **kwargs)

    def _generate_unique_order_number(self):
        while True:
            num = f"{random.randint(1000, 9999)}"
            if not Orders.objects.filter(order_number=num).exists():
                return num


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.IntegerField(verbose_name="Количество")

    def __str__(self):
        return str(self.quantity)


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
