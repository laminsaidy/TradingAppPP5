# marketplace/urls.py
from django.contrib import admin
from django.urls import path, include
from products import views as product_views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),  
    path('dashboard/', include('dashboard.urls')),
    path('conversation/', include('conversation.urls')),
    path('items/', include('item.urls')), 
]

# ✅ Point to your custom 404 view
handler404 = product_views.custom_404_view
