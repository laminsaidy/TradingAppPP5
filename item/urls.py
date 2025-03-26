from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('', views.browse_items, name='index'), 
    path('create/', views.create_item, name='create'),  
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.DeleteButton, name='delete'), 
    path('edit/<int:pk>/', views.EditButton, name='edit'),  
]