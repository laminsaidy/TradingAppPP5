# conversation/urls.py
from django.urls import path
from . import views

app_name = 'conversation'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
]
