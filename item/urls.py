from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('', views.browse_items, name='browse_items'),  # Changed from 'index' to 'browse_items'
    path('new/', views.create_item, name='create_item'),  # Changed from 'create' to 'create_item'
    path('<int:pk>/', views.item_detail, name='item_detail'),  # Changed from 'detail' to 'item_detail'
    path('<int:pk>/delete/', views.delete_item, name='delete_item'),  # Changed from 'delete' and function name
    path('<int:pk>/edit/', views.edit_item, name='edit_item'),  # Changed from 'edit' and function name
]
