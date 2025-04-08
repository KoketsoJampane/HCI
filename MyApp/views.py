# MyApp/views.py
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import UserActivity  # If using activity tracking


def home(request):
    return render(request,'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('services')  # If already logged in, redirect to dashboard
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('services')  # Redirect to dashboard after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')  # Redirect to login page after signup
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='login')
def services(request):
    return render(request, 'services.html')
    
    # Add additional context if needed
    try:
        context['recent_activity'] = UserActivity.objects.filter(user=user).order_by('-timestamp')[:5]
    except:
        pass
    
    return render(request, 'dashboard.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, "You've been successfully logged out.")
    return redirect('home')