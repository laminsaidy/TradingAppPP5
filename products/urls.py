# products/urls.py
from django.urls import path
from . import views

app_name = 'products'  

urlpatterns = [
    path('', views.index, name='index'), 
    path('contact/', views.contact, name='contact'),  
    path('signup/', views.signup, name='signup'),  
    path('login/', views.login, name='login'), 
    path('new/', views.new, name='new'),  
    path('items/', views.items, name='items'), 
    path('menu/', views.menu, name='menu'),  
    path('about/', views.about, name='about'),

]