from django.contrib import admin
from django.urls import path, include
from products import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('conversation/', include('conversation.urls')),
    path('items/', include('item.urls')),
    path('protected/', product_views.protected_view, name='protected_view'),
]

# ✅ Point to your custom 404 view
handler404 = product_views.custom_404_view

# ✅ Point to your custom 401 view
handler401 = product_views.custom_401_view
