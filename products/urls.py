from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'products'

urlpatterns = [
    path('items/', include('item.urls')),
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('new/', views.new, name='new'),
    path('items/', views.items, name='items'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('logout/', views.custom_logout, name='logout'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
