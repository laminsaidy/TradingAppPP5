# marketplace/urls.py 
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls', namespace='products')),  
    path('dashboard/', include('dashboard.urls')),
    path('conversation/', include('conversation.urls')),
    path('items/', include('item.urls')),
]