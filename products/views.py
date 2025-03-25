from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from item.models import Category, Item
from .forms import SignupForm, ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:contact_thanks')
    else:
        form = ContactForm()
    return render(request, 'products/contact.html', {'form': form})

def contact_thanks(request):
    return render(request, 'products/contact_thanks.html')

def menu(request):
    trending_items = Item.objects.filter(is_sold=False).order_by('-created_at')[:12]
    return render(request, 'products/menu.html', {
        'trending_items': trending_items
    })

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
                return redirect('products:index')
    else:
        form = AuthenticationForm()
    return render(request, 'products/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:login')
    else:
        form = SignupForm()
    return render(request, 'products/signup.html', {'form': form})

def about(request):
    return render(request, 'products/about.html')

def custom_logout(request):
    logout(request)
    return redirect('products:login')