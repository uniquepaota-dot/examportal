from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import StudentRegistrationForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome to the Exam Portal!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
        for field in form.fields:
            form.fields[field].widget.attrs.update({'class': 'form-control'})
        
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')

def dashboard_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_admin or request.user.is_superuser:
            return redirect('exams:admin_dashboard')
        else:
            return redirect('exams:student_dashboard')
    return redirect('accounts:login')

def is_admin(user):
    return user.is_authenticated and (user.is_admin or user.is_superuser)

@login_required
@user_passes_test(is_admin)
def admin_change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('exams:admin_dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    # Style the form fields
    for field in form.fields:
        form.fields[field].widget.attrs.update({'class': 'form-control'})
        
    return render(request, 'accounts/change_password.html', {'form': form})
