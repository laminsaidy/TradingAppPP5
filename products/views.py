from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from item.models import Category, Item
from .forms import SignupForm, ContactForm

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('products:contact_thanks')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ContactForm()
    return render(request, 'products/contact.html', {'form': form})

def contact_thanks(request):
    return render(request, 'products/contact_thanks.html')

def menu(request):
    trending_items = Item.objects.filter(is_sold=False).order_by('-created_at')[:12]
    if not trending_items.exists():
        messages.info(request, 'No trending items available at the moment.')
    return render(request, 'products/menu.html', {
        'trending_items': trending_items
    })

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    
    if not items.exists():
        messages.info(request, 'No featured items available yet.')
    
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
                messages.success(request, f'Welcome back, {username}!')
                return redirect('products:index')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'products/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('products:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()
    return render(request, 'products/signup.html', {'form': form})

def about(request):
    return render(request, 'products/about.html')

def custom_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('products:login')

def privacy_policy(request):
    return render(request, 'products/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'products/terms_of_service.html')