from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from item.models import Category, Item
from .forms import SignupForm

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    return render(request, 'products/index.html', {
        'categories': categories,
        'items': items,
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                base_url = reverse('products:index')
                query_string = '?message=Login successful!'
                return HttpResponseRedirect(f"{base_url}{query_string}")
    else:
        form = AuthenticationForm()

    return render(request, 'products/login.html', {'form': form})

def contact(request):
    return render(request, 'products/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            base_url = reverse('products:login')
            query_string = '?message=Signup successful!'
            return HttpResponseRedirect(f"{base_url}{query_string}")
    else:
        form = SignupForm()

    return render(request, 'products/signup.html', {'form': form})

def new(request):
    return render(request, 'products/new.html')

def items(request):
    items_list = Item.objects.filter(is_sold=False)
    return render(request, 'products/items.html', {'items': items_list})

def menu(request):
    return render(request, 'products/menu.html')

def about(request):
    return render(request, 'products/about.html')

def custom_logout(request):
    logout(request)
    base_url = reverse('products:login')
    query_string = '?message=Logout successful!'
    return HttpResponseRedirect(f"{base_url}{query_string}")
