from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('', views.browse_items, name='browse_items'),
    path('new/', views.create_item, name='create_item'),
    path('<int:pk>/', views.item_detail, name='item_detail'),
    path('<int:pk>/delete/', views.delete_item, name='delete_item'),
    path('<int:pk>/edit/', views.edit_item, name='edit_item'),
]