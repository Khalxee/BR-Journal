from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def home(request):
    """Home page view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'web/home.html')


@login_required
def dashboard(request):
    """Dashboard view for authenticated users"""
    context = {
        'is_admin': request.user.is_staff or request.user.is_superuser,
        'user_count': User.objects.count(),
    }
    return render(request, 'web/dashboard.html', context)


def signin(request):
    """Sign in page view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'web/signin.html')


def signup(request):
    """Sign up page view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        
        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'web/signup.html')
        
        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'web/signup.html')
        
        # Create new user
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name.split()[0] if name else '',
                last_name=' '.join(name.split()[1:]) if len(name.split()) > 1 else ''
            )
            messages.success(request, f'Account created successfully! Welcome, {name}!')
            return redirect('signin')
        except Exception as e:
            messages.error(request, 'An error occurred while creating your account.')
    
    return render(request, 'web/signup.html')
