"""
Accounts Views
User authentication and profile management views.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm


# ---------------- REGISTER ----------------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('detection:dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('detection:dashboard')
        else:
            messages.error(request, 'Registration failed.')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


# ---------------- LOGIN ----------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('detection:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f'Welcome {username}!')
                return redirect('detection:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


# ---------------- LOGOUT ----------------
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('accounts:login')


# ---------------- PROFILE ----------------
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'accounts/profile.html', context)