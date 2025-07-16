# marketplace/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404  # Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),  
    path('dashboard/', include('dashboard.urls')),
    path('conversation/', include('conversation.urls')),
    path('items/', include('item.urls')), 
]

# Add this at the very bottom of the file
handler404 = 'django.views.defaults.page_not_found'