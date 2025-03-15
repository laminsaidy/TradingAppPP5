# products/views.py
from django.shortcuts import render

def inbox(request):
    return render(request, 'conversation/inbox.html')

def index(request):
    return render(request, 'dashboard/index.html')

def menu(request):
    return render(request, 'products/menu.html')

def index(request):
    return render(request, 'products/index.html')

def about(request):
    return render(request, 'products/about.html')

def contact(request):
    return render(request, 'products/contact.html')

def signup(request):
    return render(request, 'products/signup.html')

def login(request):
    return render(request, 'products/login.html')

def new(request):
    return render(request, 'products/new.html')

def items(request):
    return render(request, 'products/items.html')