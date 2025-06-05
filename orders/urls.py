from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order/create/<int:product_id>/', order_create, name='order_create'),
    path('orders/history', history, name='history'),
    path('add_address/', add_address, name='add_address'),
    path('add_cart/', add_cart, name='add_cart'),
    path('massage/', massage, name='massage'),
    path('delete_address/<int:address_id>/', delete_address, name='delete_address'),
    path('delete_card/<int:card_id>/', delete_card, name='delete_card'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
