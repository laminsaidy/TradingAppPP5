# products/views.py
from django.shortcuts import render, redirect

from item.models import Category, Item

from .forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:login')  
    else:
        form = SignupForm()

    return render(request, 'products/signup.html', {
        'form': form
    })


def menu(request):
    return render(request, 'products/menu.html')

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'products/index.html', {
        'categories': categories,
        'items': items,
    })

def about(request):
    return render(request, 'products/about.html')

def contact(request):
    return render(request, 'products/contact.html')


def login(request):
    return render(request, 'products/login.html')

def new(request):
    return render(request, 'products/new.html')

def items(request):
    return render(request, 'products/items.html')