from django.contrib import admin

from orders.models import *

admin.site.register(Address)
admin.site.register(Card)
admin.site.register(Orders)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Status)
admin.site.register(OrderItem)
