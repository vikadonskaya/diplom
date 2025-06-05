from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('add_product', add_product, name='add_product'),
    path('a_product/<int:id>', admin_product, name='a_product'),
    path('del_product/<int:id>', delete_product, name='del_product'),
    path('a_user', a_user, name='a_user'),
    path('a_orders', a_orders, name='a_orders'),
    path('a_brend', a_brend, name='a_brend'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)