from www.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('shop', shop, name='shop'),  # This path does not require a category_id
    path('stocks', stocks, name='stocks'),
    path('cart', cart, name='cart'),
    path('remove_cart_item/<int:item_id>', remove_cart_item, name='remove_cart_item'),
    path('update_cart_item/<int:item_id>', update_cart_item, name='update_cart_item'),
    path('shop_single/<int:id>', shop_single, name='shop_single'),
    path('acc', acc, name='acc'),
    path('about', about, name='about'),
    path('orders', orders, name='orders'),
    path('products/category/<int:category_id>/', shop, name='products_by_category'),
    path('product/<int:id>/add_comment/', add_comment, name='add_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
