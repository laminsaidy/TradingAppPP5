# marketplace/urls.py
from django.contrib import admin
from django.urls import path, include
from item.views import debug_categories

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),  
    path('dashboard/', include('dashboard.urls')),
    path('conversation/', include('conversation.urls')),
    
    path('debug-categories/', debug_categories),

    path('items/', include('item.urls')), 
]