from django.urls import path
from .views import *
from django.contrib.auth import views as auth_viws
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('auth', auth, name='auth'),
    path('reg', reg, name='reg'),
    path('logout', logout_view, name='logout'),
    path('edit_profile', edit_profile, name='edit_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)