from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('', views.items, name='index'),  
    path('detail/<int:pk>/', views.detail, name='detail'),  
    path('create/', views.create_item, name='create'), 
    path('<int:pk>/delete/', views.delete, name='delete'), 
]

